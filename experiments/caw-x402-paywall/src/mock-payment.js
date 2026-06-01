import { createHash, randomUUID } from "node:crypto";

export function usdToAtomic(priceUsd) {
  return String(Math.round(Number(priceUsd) * 1_000_000));
}

export function endpointHash(method, pathname) {
  return `0x${createHash("sha256").update(`${method} ${pathname}`).digest("hex")}`;
}

export function buildPaymentRequirements({ method, pathname, config }) {
  const paymentId = randomUUID();
  return {
    x402Version: 1,
    error: "X402_PAYMENT_REQUIRED",
    accepts: [
      {
        scheme: "exact",
        network: config.network,
        payTo: config.payTo,
        asset: "USDC",
        maxAmountRequired: usdToAtomic(config.priceUsd),
        price: `$${config.priceUsd}`,
        resource: `${method} ${pathname}`,
        description: `${config.serviceName} paid inference`,
        paymentId,
        expiresAt: new Date(Date.now() + 5 * 60 * 1000).toISOString()
      }
    ]
  };
}

export function encodeMockPayment(requirement) {
  const payload = {
    scheme: requirement.scheme,
    network: requirement.network,
    payTo: requirement.payTo,
    asset: requirement.asset,
    amount: requirement.maxAmountRequired,
    paymentId: requirement.paymentId,
    signedBy: "mock-caw-agent",
    settlementTx: `mock://settlement/${requirement.paymentId}`
  };

  return Buffer.from(JSON.stringify(payload), "utf8").toString("base64url");
}

export function decodeMockPayment(header) {
  if (!header) return null;
  try {
    return JSON.parse(Buffer.from(header, "base64url").toString("utf8"));
  } catch {
    return null;
  }
}
