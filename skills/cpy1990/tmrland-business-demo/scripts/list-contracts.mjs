#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-contracts.mjs [--limit N]");
  process.exit(2);
}

const limit = Number.parseInt(named.limit ?? "20", 10);
const data = await tmrFetch("GET", `/contracts/?limit=${limit}`);

console.log(`## Contracts (${data.items?.length ?? 0})\n`);
for (const c of data.items ?? []) {
  console.log(`- ${c.id} | ${c.status ?? "—"} | ${c.created_at ?? "—"}`);
}
console.log(JSON.stringify(data, null, 2));
