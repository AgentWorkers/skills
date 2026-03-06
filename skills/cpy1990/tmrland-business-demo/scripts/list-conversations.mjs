#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help, named } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-conversations.mjs [--limit N]");
  process.exit(2);
}

const limit = Number.parseInt(named.limit ?? "20", 10);
const data = await tmrFetch("GET", `/messages/conversations?limit=${limit}`);

console.log(`## Conversations (${data.items?.length ?? 0})\n`);
for (const c of data.items ?? []) {
  console.log(`- Order ${c.order_id ?? "—"} | Unread: ${c.unread_count ?? 0} | Last: ${c.last_message_at ?? "—"}`);
}
console.log(JSON.stringify(data, null, 2));
