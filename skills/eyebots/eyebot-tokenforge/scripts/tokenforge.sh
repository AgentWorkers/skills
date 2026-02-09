#!/bin/bash
# TokenForge Agent - Token Deployment
API_BASE="${EYEBOT_API:-${EYEBOT_API}}"
curl -s -X POST "${API_BASE}/api/tokenforge" \
  -H "Content-Type: application/json" \
  -d "{\"request\": \"$*\", \"auto_pay\": true}"
