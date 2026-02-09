# Heartbeat

## OpenClaw Minecraft (every 30 seconds)
1. Observe: `GET /v1/bots/{botId}/state`.
2. If `metadata.currentTaskId` exists or `metadata.queueLength` > 0, wait 2 seconds and end this heartbeat.
3. Plan: decide an action bundle (up to 10 steps) based on `nearby`, `health`, `hunger`, and persona `priorityRules`.
   - If the previous bundle failed, choose a safer fallback bundle.
4. Announce plan in Minecraft chat:
   - Use persona `chatTemplate`, e.g., `[plan][carpenter] {plan}`.
   - Example: `[plan][carpenter] Heading to nearby oak to gather wood.`
   - `POST /v1/bots/{botId}/act` with `action: "chat"` and the template above.
5. Act: send each step in order using `POST /v1/bots/{botId}/act` with `queue: "queue"`.
    - Use `mode: until` or `mode: loop` and set `timeoutMs`.
    - If a step fails, stop the remaining steps and use a fallback bundle next heartbeat.
    - Example bundle: move_to -> dig -> move_to.
6. Log decisions in `memory/mc-autonomy.json` with timestamps.

Example 10-step bundle:
1) move_to (nearest tree)
2) dig (tree block)
3) dig (tree block)
4) move_to (next tree)
5) dig (tree block)
6) move_to (safe point)
7) place (crafting table)
8) equip (tool)
9) move_to (resource)
10) dig (resource)

## Decision Hints
- If health is low, move to a safe spot or stop.
- If idle, explore by moving to a nearby random point.
- If interesting blocks are nearby, move closer and inspect.
- Avoid spamming actions; one action per heartbeat.
