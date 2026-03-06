#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, positional } = parseArgs(process.argv);
if (help || !positional[0]) {
  console.error("Usage: get-dispute-votes.mjs <order-id>");
  process.exit(2);
}

const data = await tmrFetch("GET", `/orders/${positional[0]}/dispute/votes`);
console.log(`## Dispute Votes for order ${positional[0]}\n`);
for (const v of data.votes ?? data.items ?? data) {
  console.log(`- Juror: ${v.juror_id ?? "—"} | Verdict: ${v.verdict ?? "—"}`);
}
console.log(JSON.stringify(data, null, 2));
