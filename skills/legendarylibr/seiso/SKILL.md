---
name: seisoai
description: SeisoAI x402 protocol skill for OpenClaw/Claw agents. Pay-per-request AI inference via USDC on Base.
metadata: {"openclaw":{"homepage":"https://seisoai.com","emoji":":art:"}}
version: 2.0.0
last_synced: 2026-02-13
---

# SeisoAI x402 Skill for OpenClaw

Base URL: `https://seisoai.com`

## Overview

SeisoAI provides AI inference tools (image, video, music, 3D, audio) accessible via x402 payment protocol. External agents authenticate by paying - no API key or JWT required.

**Payment network**: Base mainnet (eip155:8453)
**Payment asset**: USDC

## Quick Start

1. Call any gateway endpoint without auth
2. Receive 402 Payment Required with price
3. Sign payment to the `payTo` wallet
4. Retry with `payment-signature` header
5. Receive result or job ID for polling

## Gateway Endpoints

All x402-enabled endpoints are under `/api/gateway/`:

### Discovery (No Auth Required)

| Endpoint | Description |
|----------|-------------|
| `GET /api/gateway` | Gateway info, categories, endpoints |
| `GET /api/gateway/tools` | List all tools |
| `GET /api/gateway/tools?category=X` | Filter by category |
| `GET /api/gateway/tools?q=X` | Search tools |
| `GET /api/gateway/tools/:toolId` | Get tool details |
| `GET /api/gateway/price/:toolId` | Get pricing |
| `GET /api/gateway/schema` | OpenAPI schema |
| `GET /api/gateway/mcp-manifest` | MCP manifest |
| `GET /api/gateway/agents` | List registered agents |

### Invocation (x402 Payment Required)

| Endpoint | Description |
|----------|-------------|
| `POST /api/gateway/invoke/:toolId` | Invoke a tool |
| `POST /api/gateway/invoke` | Invoke with `toolId` in body |
| `POST /api/gateway/batch` | Batch multiple calls |
| `POST /api/gateway/orchestrate` | Multi-step workflow |

### Jobs (No Auth Required)

| Endpoint | Description |
|----------|-------------|
| `GET /api/gateway/jobs/:jobId` | Poll job status |
| `GET /api/gateway/jobs/:jobId/result` | Get job result |

## Available Tool Categories

- `image-generation` - Text to image (FLUX, etc.)
- `image-editing` - Edit/blend images
- `image-processing` - Upscale, extract layers
- `video-generation` - Text/image to video (Veo3, Kling, etc.)
- `video-editing` - Animate images, edit video
- `music-generation` - Generate music
- `audio-generation` - TTS, video-to-audio
- `audio-processing` - Transcribe, stem separation
- `3d-generation` - Image/text to 3D
- `vision` - Image description
- `training` - Train LoRA models

## x402 Payment Flow

### Step 1: Initial Request (No Auth)

```http
POST /api/gateway/invoke/image.generate.flux-2
Host: seisoai.com
Content-Type: application/json

{"prompt": "a cyberpunk cityscape at sunset", "aspect_ratio": "16:9"}
```

### Step 2: Receive 402 Challenge

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json

{
  "x402Version": 2,
  "error": "Payment required",
  "resource": {
    "url": "https://seisoai.com/api/gateway/invoke/image.generate.flux-2",
    "description": "Invoke any AI tool via the gateway",
    "mimeType": "application/json"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "maxAmountRequired": "32500",
      "asset": "USDC",
      "payTo": "0xa0aE05e2766A069923B2a51011F270aCadFf023a",
      "extra": {
        "priceUsd": "$0.0325"
      }
    }
  ]
}
```

### Step 3: Sign Payment

Sign an x402 payment payload using the OpenClaw host's payment signer:
- Amount: `accepts[0].maxAmountRequired` (USDC in smallest units, 6 decimals)
- Recipient: `accepts[0].payTo` (exact wallet from challenge)
- Network: `eip155:8453` (Base mainnet)

### Step 4: Retry with Payment

```http
POST /api/gateway/invoke/image.generate.flux-2
Host: seisoai.com
Content-Type: application/json
payment-signature: <signed-x402-payload>

{"prompt": "a cyberpunk cityscape at sunset", "aspect_ratio": "16:9"}
```

### Step 5: Receive Result

For synchronous tools:
```json
{
  "success": true,
  "toolId": "image.generate.flux-2",
  "result": {
    "images": [{"url": "https://..."}]
  },
  "x402": {
    "settled": true,
    "amount": "32500",
    "transactionHash": "0x..."
  }
}
```

For async/queued tools:
```json
{
  "success": true,
  "jobId": "abc123",
  "status": "QUEUED",
  "pollUrl": "/api/gateway/jobs/abc123"
}
```

## Polling Queued Jobs

```http
GET /api/gateway/jobs/{jobId}
Host: seisoai.com
```

Response:
```json
{
  "success": true,
  "jobId": "abc123",
  "status": "COMPLETED",
  "result": { ... }
}
```

Status values: `QUEUED`, `IN_PROGRESS`, `COMPLETED`, `FAILED`

## Example Tool Invocations

### Image Generation

```json
POST /api/gateway/invoke/image.generate.flux-2
{
  "prompt": "a serene japanese garden with cherry blossoms",
  "aspect_ratio": "16:9",
  "num_images": 1
}
```

### Video Generation

```json
POST /api/gateway/invoke/video.generate.veo3
{
  "prompt": "a timelapse of clouds moving over mountains",
  "duration": 5
}
```

### Music Generation

```json
POST /api/gateway/invoke/music.generate
{
  "prompt": "upbeat electronic music for a tech demo",
  "duration": 30
}
```

### Text to Speech

```json
POST /api/gateway/invoke/audio.tts
{
  "text": "Hello, this is a test of the text to speech system.",
  "voice": "alloy"
}
```

### Image to 3D

```json
POST /api/gateway/invoke/3d.image-to-3d
{
  "image_url": "https://example.com/object.png"
}
```

## Pricing

Check pricing before invocation:

```http
GET /api/gateway/price/image.generate.flux-2
```

```json
{
  "success": true,
  "toolId": "image.generate.flux-2",
  "pricing": {
    "usd": 0.0325,
    "usdcUnits": "32500"
  },
  "x402": {
    "network": "eip155:8453",
    "asset": "USDC",
    "amount": "32500"
  }
}
```

## Security

### Server-Side Protections (Enforced)

The gateway enforces these protections - violations will be rejected:

| Protection | Description |
|------------|-------------|
| **Replay prevention** | Payment signatures are one-time use. Resubmitting a used signature returns 402 "Payment signature already used" |
| **Signature deduplication** | Redis-backed (or in-memory fallback) cache prevents double-submission across requests |
| **Wallet verification** | CDP facilitator verifies payment was sent to the correct `payTo` address |
| **Amount verification** | Payment amount must match or exceed the `maxAmountRequired` from challenge |
| **Network verification** | Payment must be on Base mainnet (eip155:8453) |
| **Route boundary** | x402 only works on `/api/gateway/*` routes - other routes reject payment headers |
| **Symbol-based auth** | Verified payments set an unforgeable Symbol flag - cannot be spoofed via headers |

### Payment Signing Rules (MANDATORY)

1. **Use host signer only**: Use the OpenClaw host's payment signer capability
2. **No raw keys**: Never request, store, or derive private keys
3. **Sign only x402 payloads**: Only sign the payment payload from 402 challenges
4. **Exact recipient**: Always pay to the exact `payTo` address from the challenge
5. **Fresh signatures**: Do not reuse payment signatures across requests
6. **Fail closed**: If no signer available, return error instead of skipping payment

### Request Invariants (DO NOT VIOLATE)

1. **Identical intent**: Keep request body identical between challenge and paid retry
2. **Same method/path**: Do not change HTTP method or path between retries
3. **Fresh signatures**: Never reuse stale or previously consumed signatures
4. **Queued = billed**: Treat successful queue submission as billable
5. **Wallet integrity**: Signed payment MUST target the challenge `payTo` address

### What Happens on Violation

| Violation | Server Response |
|-----------|-----------------|
| Replay signature | 402 "Payment signature already used" |
| Wrong recipient | 402 "Payment verification failed" |
| Insufficient amount | 402 "Payment amount insufficient" |
| Wrong network | 402 "Invalid payment network" |
| Non-gateway route | 401 "Authentication required" |
| Spoofed headers | 401 (Symbol flag not set) |

## Rate Limits

| Scope | Limit | Window |
|-------|-------|--------|
| General API | 500 requests | 15 minutes |
| Payment operations | 10 requests | 5 minutes |

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Maximum requests allowed
- `X-RateLimit-Remaining`: Requests remaining in window
- `X-RateLimit-Reset`: Window reset time (ISO-8601)
- `Retry-After`: Seconds until retry allowed (on 429)

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 402 | Payment required | Sign payment, retry |
| 400 | Invalid input | Fix request payload |
| 401 | Auth required (not x402 route) | Use correct gateway endpoint |
| 404 | Tool/route not found | Check tool ID spelling |
| 429 | Rate limited | Read `Retry-After` header, backoff with jitter |
| 500 | Server error | Retry with exponential backoff (max 3 attempts) |

## Common Mistakes

1. **Reusing payment signatures** - Each request needs a fresh signature
2. **Changing payload on retry** - Must be identical to challenged request
3. **Wrong poll endpoint** - Use the `pollUrl` from queue response
4. **Treating 402 as error** - It's the payment handshake, not a failure
5. **Non-gateway endpoints** - Only `/api/gateway/*` routes support x402

## Response Schema

Successful responses include:

```json
{
  "success": true,
  "toolId": "string",
  "result": { ... },
  "x402": {
    "settled": true,
    "amount": "string",
    "transactionHash": "string | null"
  }
}
```

Failed responses:

```json
{
  "success": false,
  "error": "string",
  "code": "string (optional)"
}
```

## Discovery

### Gateway Info

```http
GET /api/gateway
```

Returns gateway metadata, available categories, tool count, and supported protocols.

### List Tools

```http
GET /api/gateway/tools
GET /api/gateway/tools?category=image-generation
GET /api/gateway/tools?q=video
```

### Tool Details

```http
GET /api/gateway/tools/:toolId
```

### Pricing

```http
GET /api/gateway/price/:toolId
```

## Alternative: API Key Auth

Registered agents can also use API keys instead of x402:

```http
POST /api/gateway/invoke/image.generate.flux-2
Host: seisoai.com
Content-Type: application/json
X-API-Key: sk_live_your_api_key

{"prompt": "test"}
```

API keys must start with `sk_live_` and be registered with SeisoAI.
