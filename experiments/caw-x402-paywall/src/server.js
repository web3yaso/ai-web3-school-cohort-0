import http from "node:http";
import { getConfig } from "./config.js";
import { buildPaymentRequirements, decodeMockPayment, endpointHash } from "./mock-payment.js";
import { recordAudit } from "./audit.js";

const config = getConfig();
const once = process.argv.includes("--once");

async function startRealX402Server() {
  const express = (await import("express")).default;
  const { paymentMiddleware, x402ResourceServer } = await import("@x402/express");
  const { ExactEvmScheme } = await import("@x402/evm/exact/server");
  const { HTTPFacilitatorClient } = await import("@x402/core/server");

  const app = express();
  const facilitatorClient = new HTTPFacilitatorClient({ url: config.facilitatorUrl });

  app.use(
    paymentMiddleware(
      {
        "GET /api/inference": {
          accepts: [
            {
              scheme: "exact",
              price: `$${config.priceUsd}`,
              network: config.network,
              payTo: config.payTo
            }
          ],
          description: `${config.serviceName} paid inference`,
          mimeType: "application/json"
        }
      },
      new x402ResourceServer(facilitatorClient).register(config.network, new ExactEvmScheme())
    )
  );

  app.get("/api/inference", async (_req, res) => {
    await recordAudit({
      side: "seller",
      type: "result_delivered",
      mode: "real-x402",
      network: config.network,
      payTo: config.payTo
    });

    res.json(buildInferenceResult("real-x402"));
    if (once) setTimeout(() => process.exit(0), 250);
  });

  app.listen(config.port, () => {
    console.log(`x402 paywall listening on http://127.0.0.1:${config.port} (${config.x402Mode})`);
  });
}

function buildInferenceResult(mode) {
  return {
    service: config.serviceName,
    mode,
    result: {
      signal: "agent-commerce-fit: high",
      rationale: "The request paid within a bounded pact, then received the protected result.",
      confidence: 0.86
    }
  };
}

async function handleMockRequest(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (req.method !== "GET" || url.pathname !== "/api/inference") {
    res.writeHead(404, { "content-type": "application/json" });
    res.end(JSON.stringify({ error: "not_found" }));
    return;
  }

  const payment = decodeMockPayment(req.headers["x-payment"]);
  if (!payment) {
    const body = buildPaymentRequirements({ method: req.method, pathname: url.pathname, config });
    await recordAudit({
      side: "seller",
      type: "payment_required",
      mode: "mock",
      requirements: body.accepts[0]
    });

    res.writeHead(402, { "content-type": "application/json" });
    res.end(JSON.stringify(body, null, 2));
    return;
  }

  await recordAudit({
    side: "seller",
    type: "payment_settled",
    mode: "mock",
    payment,
    endpointHash: endpointHash(req.method, url.pathname)
  });

  const receipt = {
    paymentId: payment.paymentId,
    network: payment.network,
    payTo: payment.payTo,
    amount: payment.amount,
    settlementTx: payment.settlementTx
  };

  await recordAudit({
    side: "seller",
    type: "result_delivered",
    mode: "mock",
    receipt
  });

  res.writeHead(200, {
    "content-type": "application/json",
    "x-payment-receipt": Buffer.from(JSON.stringify(receipt), "utf8").toString("base64url")
  });
  res.end(JSON.stringify({ ...buildInferenceResult("mock"), receipt }, null, 2));

  if (once) setTimeout(() => process.exit(0), 250);
}

if (config.x402Mode === "real") {
  startRealX402Server().catch(error => {
    console.error(error);
    process.exit(1);
  });
} else {
  http.createServer((req, res) => {
    handleMockRequest(req, res).catch(error => {
      console.error(error);
      res.writeHead(500, { "content-type": "application/json" });
      res.end(JSON.stringify({ error: "internal_error" }));
    });
  }).listen(config.port, () => {
    console.log(`x402 paywall listening on http://127.0.0.1:${config.port} (${config.x402Mode})`);
  });
}
