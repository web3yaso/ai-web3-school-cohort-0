import { mkdir, appendFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const projectRoot = dirname(here);
const auditPath = join(projectRoot, "audit", "events.jsonl");

export async function recordAudit(event) {
  const entry = {
    ts: new Date().toISOString(),
    ...event
  };

  await mkdir(dirname(auditPath), { recursive: true });
  await appendFile(auditPath, `${JSON.stringify(entry)}\n`);
  return entry;
}

export { auditPath };
