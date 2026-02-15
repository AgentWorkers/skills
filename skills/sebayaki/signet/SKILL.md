---
name: signet
description: 在Hunt Town中，用户可以通过Interact with Signet onchain advertising功能与Signet的链上广告系统进行交互。该功能允许用户查看广告的价格、列出当前的广告信息或签名数据，以及将URL发布到Signet的广告展示系统中。该系统支持x402支付协议，支持人工智能代理进行程序化广告投放。
---

# Signet

Signet 是一个基于 Base（Hunt Town Co-op）平台的链上广告协议。广告链接会通过竞争来获得展示机会，获胜的链接将获得 HUNT 代币的奖励。

## CLI 工具

请安装并使用 `@signet-base/cli` 工具：

```bash
# Estimate cost for spotlight placement
npx @signet-base/cli estimate --hours 6

# List recent signatures
npx @signet-base/cli list --count 10

# Post a URL (simulate first to check cost)
npx @signet-base/cli post --url https://example.com --hours 6 --simulate

# Post for real (requires PRIVATE_KEY env or --private-key)
PRIVATE_KEY=0x... npx @signet-base/cli post --url https://example.com --hours 6
```

### 命令

- **estimate** — 获取广告发布的预估成本（以 USDC 为单位）。可选参数：`--hours <0-24>`（展示时间，范围 0-24 小时），`--simulate`（模拟广告发布过程）。
- **list** — 列出最近被展示的广告链接。可选参数：`--count <n>`（显示的广告数量）。
- **post** — 通过 x402 支付方式将广告链接发布到展示位。可选参数：`--url <广告链接>`（要发布的广告链接），`--hours <0-24>`（展示时间），`--private-key <私钥>`（用于签名），`--simulate`（模拟支付过程）。

`--simulate` 选项会执行完整的 x402 支付流程（包括成本估算、生成支付请求等），但不会实际提交支付请求。您可以使用该选项在正式发布前验证成本。

## API（直接 HTTP 请求）

Base API 地址：`https://signet.sebayaki.com`

### 估算成本

```bash
curl "https://signet.sebayaki.com/api/x402/estimate?guaranteeHours=0"
```

响应格式：
```json
{
  "guaranteeHours": 0,
  "estimatedUSDC": "12.28",
  "estimatedUSDCRaw": "12280000",
  "spotlightAvailable": true,
  "spotlightRemainingSeconds": 0
}
```

`guaranteeHours`（0-24）：广告展示的保证时间（单位：小时）。0 表示展示时间可以随时被替换。

### 列出广告链接

```bash
curl "https://signet.sebayaki.com/api/signature/list?startIndex=0&endIndex=5"
```

返回格式：
`{ signatures: [{ signatureIndex, url, huntAmount, viewCount, clickCount, metadata, timestamp, userWallet }] }`。

### 发布广告（x402 支付）

```bash
# Step 1: POST without payment → 402 with requirements
curl -X POST https://signet.sebayaki.com/api/x402/spotlight \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","guaranteeHours":0}'

# Step 2: POST with payment header → 200
curl -X POST https://signet.sebayaki.com/api/x402/spotlight \
  -H "Content-Type: application/json" \
  -H "X-402: <encoded-payment>" \
  -d '{"url":"https://example.com","guaranteeHours":0}'
```

x402 支付流程：
1. 服务器返回包含支付信息的 402 请求（包括所需支付的 USDC 金额、收款地址和网络信息）。
2. 客户使用 `@x402/core` 和 `@x402/evm` 工具生成 USDC 支付请求并进行签名。
3. 客户重新发送带有支付信息的请求。
4. 服务器通过中介节点验证请求，然后在链上执行交易并完成支付。