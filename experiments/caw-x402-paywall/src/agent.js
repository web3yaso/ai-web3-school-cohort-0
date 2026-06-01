import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { getConfig } from "./config.js";
import { encodeMockPayment } from "./mock-payment.js";
import { recordAudit } from "./audit.js";

const config = getConfig();
const targetUrl = process.argv.find(arg => arg.startsWith("http")) || `http://127.0.0.1:${config.port}/api/inference`;
const modeArg = process.argv.find(arg => arg.startsWith("--mode="));
const mode = modeArg ? modeArg.split("=")[1] : config.agentMode;

async function loadPact() {
  return JSON.parse(await readFile(config.pactFile, "utf8"));
}

function parseUsd(value) {
  if (typeof value === "number") return value;
  return Number(String(value).replace(/^\$/, ""));
}

function requirementPriceUsd(requirement) {
  if (requirement.price) return parseUsd(requirement.price);
  return Number(requirement.maxAmountRequired || requirement.amount || 0) / 1_000_000;
}

function evaluateRequirement(requirement, pact) {
  const policy = pact.policies[0];
  const now = Date.now();
  const notBefore = Date.parse(pact.time_window.not_before);
  const notAfter = Date.parse(pact.time_window.not_after);
  const priceUsd = requirementPriceUsd(requirement);
  const maxPerCall = parseUsd(policy.limits.max_amount_usd_per_call);
  const reasons = [];

  if (requirement.scheme !== policy.when.scheme) reasons.push("scheme_not_allowed");
  if (priceUsd > maxPerCall) reasons.push("price_exceeds_per_call_budget");
  if (!policy.allow.networks.includes(requirement.network)) reasons.push("network_not_allowlisted");
  if (!policy.allow.pay_to.map(x => x.toLowerCase()).includes(requirement.payTo.toLowerCase())) {
    reasons.push("payee_not_allowlisted");
  }
  if (!policy.allow.resources.includes(requirement.resource)) reasons.push("resource_not_allowlisted");
  if (now < notBefore || now > notAfter) reasons.push("outside_time_window");

  return {
    allowed: reasons.length === 0,
    reasons,
    priceUsd,
    maxPerCall
  };
}

async function runMockAgent() {
  const pact = await loadPact();
  const first = await fetch(targetUrl);

  if (first.status !== 402) {
    throw new Error(`Expected HTTP 402, got ${first.status}`);
  }

  const challenge = await first.json();
  const requirement = challenge.accepts[0];
  const decision = evaluateRequirement(requirement, pact);

  await recordAudit({
    side: "buyer-agent",
    type: "policy_decision",
    mode: "mock",
    requirement,
    decision
  });

  if (!decision.allowed) {
    throw new Error(`Pact denied payment: ${decision.reasons.join(", ")}`);
  }

  const paid = await fetch(targetUrl, {
    headers: {
      "x-payment": encodeMockPayment(requirement)
    }
  });

  const body = await paid.json();
  await recordAudit({
    side: "buyer-agent",
    type: "result_received",
    mode: "mock",
    status: paid.status,
    receipt: paid.headers.get("x-payment-receipt"),
    body
  });

  console.log(JSON.stringify(body, null, 2));
}

async function runCawAgent() {
  const pact = await loadPact();
  const maxAmount = pact.policies[0].limits.max_amount_usd_per_call;
  const result = spawnSync("caw", ["fetch", targetUrl, "--max-amount", maxAmount], {
    encoding: "utf8"
  });

  await recordAudit({
    side: "buyer-agent",
    type: "caw_fetch_invoked",
    mode: "caw",
    targetUrl,
    maxAmount,
    status: result.status,
    stderr: result.stderr
  });

  if (result.error) {
    throw new Error(`Unable to run caw CLI: ${result.error.message}`);
  }
  if (result.status !== 0) {
    throw new Error(result.stderr || `caw fetch exited with ${result.status}`);
  }

  console.log(result.stdout);
}

if (mode === "caw") {
  runCawAgent().catch(error => {
    console.error(error.message);
    process.exit(1);
  });
} else {
  runMockAgent().catch(error => {
    console.error(error.message);
    process.exit(1);
  });
}
