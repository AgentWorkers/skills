# OpenClaw Integration

Use this only when the user is explicitly building on OpenClaw.

## Integration Pattern

1. Store private values in config or environment variables
2. Keep behavior policy in workspace docs
3. Keep runtime logic in scripts
4. Trigger the companion from scheduled `systemEvent` handlers

## Files To Touch

Typical mapping:
- persona/behavior rules:
  - `SOUL.md`
  - `HEARTBEAT.md`
- runtime script:
  - `workspace/scripts/companion_ping.sh`
- optional share source:
  - `workspace/scripts/fetch_x_hotspots.py`
- state:
  - `workspace/state/companion-state.json`
  - `workspace/state/x-hotspots.json`

## What Must Stay Configurable

- owner chat target
- owner session key
- generator target/session
- workspace root
- recent message log path
- state paths
- Chrome binary path
- X source URL

## Handler Shape

For each scheduled mode, the handler only needs to:
1. invoke the companion script with `afternoon|evening|night`
2. report execution status

Keep the handler thin. Put logic in scripts, not markdown prose.

## Safety Notes

- Do not use direct in-turn restart paths for gateway restarts.
- Do not let proactive behavior leak into non-owner chats.
- Do not make outbound sharing/posting actions implicit.
