#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-businesses.mjs [--limit N]");
  process.exit(2);
}

const limit = Number.parseInt(named.limit ?? "20", 10);
const data = await tmrFetch("GET", `/businesses/?limit=${limit}`);

console.log(`## Businesses (${data.items?.length ?? 0})\n`);
for (const b of data.items ?? []) {
  console.log(`- ${b.id} | ${b.brand_name_en ?? b.brand_name_zh ?? "—"} | ${b.status ?? "—"}`);
}
console.log(JSON.stringify(data, null, 2));
