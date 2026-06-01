import { readFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
export const projectRoot = dirname(here);

function loadDotenv() {
  const envPath = join(projectRoot, ".env");
  if (!existsSync(envPath)) return;

  const lines = readFileSync(envPath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#") || !trimmed.includes("=")) continue;
    const [key, ...rest] = trimmed.split("=");
    if (!process.env[key]) process.env[key] = rest.join("=");
  }
}

loadDotenv();

export function getConfig() {
  return {
    port: Number(process.env.PORT || 4021),
    x402Mode: process.env.X402_MODE || "mock",
    serviceName: process.env.SERVICE_NAME || "agent-commerce-alpha-signal",
    priceUsd: process.env.PRICE_USD || "0.001",
    network: process.env.NETWORK || "eip155:84532",
    payTo: process.env.PAY_TO || "0x0000000000000000000000000000000000000402",
    facilitatorUrl: process.env.FACILITATOR_URL || "https://x402.org/facilitator",
    pactFile: resolve(projectRoot, process.env.PACT_FILE || "policies/caw-pact-x402-base-sepolia.json"),
    agentMode: process.env.AGENT_MODE || "mock"
  };
}
