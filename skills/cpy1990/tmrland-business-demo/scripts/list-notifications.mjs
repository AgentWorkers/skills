#!/usr/bin/env node
import { tmrFetch, parseArgs } from "./_lib.mjs";

const { help } = parseArgs(process.argv);
if (help) {
  console.error("Usage: list-notifications.mjs");
  process.exit(2);
}

const data = await tmrFetch("GET", "/notifications/");

console.log(`## Notifications (${data.items?.length ?? 0})\n`);
for (const n of data.items ?? []) {
  console.log(`- ${n.id} | ${n.type ?? "—"} | ${n.read ? "read" : "unread"} | ${n.created_at ?? "—"}`);
}
console.log(JSON.stringify(data, null, 2));
