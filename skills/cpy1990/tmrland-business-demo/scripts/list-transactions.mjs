#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-transactions.mjs [--limit N]");
  process.exit(2);
}

const limit = Number.parseInt(named.limit ?? "20", 10);
const data = await tmrFetch("GET", `/wallet/transactions?limit=${limit}`);

console.log(`## Transactions (${data.items?.length ?? 0})\n`);
for (const t of data.items ?? []) {
  console.log(`- ${t.id} | ${t.type ?? "—"} | ${t.amount ?? "—"} ${t.currency ?? ""} | ${t.created_at ?? "—"}`);
}
console.log(JSON.stringify(data, null, 2));
