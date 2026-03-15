---
name: forge
description: 通过THORChain实现跨链交易路由。用户可以获取44种以上资产（包括BTC、ETH、RUNE、AVAX、USDC等）的交易报价，并构建相应的交易订单。该服务采用非托管模式——系统会返回交易所需的保管库地址和备注信息，用户需自行在钱包中执行交易。每笔成功路由的交易，forgemb将获得0.5%的佣金。
version: 0.1.0
author: MoreBetter Studios
homepage: https://morebetterstudios.com
repository: https://github.com/morebetterclaw/forge
api: https://forge-api-production-50de.up.railway.app
mcp: https://forge-api-production-50de.up.railway.app/mcp
tags:
  - crypto
  - defi
  - thorchain
  - swap
  - cross-chain
  - bitcoin
  - ethereum
  - rune
---
# FORGE — 跨链交易代理

这是一个由 THORChain 提供的非托管型跨链交易服务，能够通过 THORNode API 直接路由 44 种以上资产的交易请求。每次交易都会向 `forgemb` 协议支付 0.5% 的佣金，该佣金以 RUNE 作为结算方式，且完全去中心化、无需信任机制。

## 实时 API

```
Base:      https://forge-api-production-50de.up.railway.app
MCP:       https://forge-api-production-50de.up.railway.app/mcp
Discovery: https://forge-api-production-50de.up.railway.app/.well-known/mcp.json
```

## MCP 工具（Claude Desktop / Cursor / 任意 MCP 客户端）

```json
{
  "mcpServers": {
    "forge": {
      "url": "https://forge-api-production-50de.up.railway.app/mcp",
      "transport": "streamable-http"
    }
  }
}
```

**可用工具：** `forge_quote` · `forge_execute` · `forge_assets` · `forge_status`

## REST API

```bash
# Get a quote
curl -X POST https://forge-api-production-50de.up.railway.app/swap/quote \
  -H "Content-Type: application/json" \
  -d '{"fromAsset":"ETH.ETH","toAsset":"BTC.BTC","amount":"0.1"}'

# Build swap transaction (returns vault address + memo — no funds sent)
curl -X POST https://forge-api-production-50de.up.railway.app/swap/execute \
  -H "Content-Type: application/json" \
  -d '{"fromAsset":"ETH.ETH","toAsset":"THOR.RUNE","amount":"0.05","destinationAddress":"thor1..."}'

# List supported assets
curl https://forge-api-production-50de.up.railway.app/swap/assets
```

## 工作原理

1. 调用 `/swap/execute` 接口，传入源资产、目标资产以及目标地址。
2. FORGE 会返回一个 **保险库存款地址** 和一个 **THORChain 交易备忘录**。
3. 用户需要将资金发送到该保险库地址，并在交易数据中包含该备忘录作为附加信息。
4. THORChain 协议会负责完成交易路由；FORGE 本身不会持有任何资金。
5. `forgemb` 会从交易备忘录中获取 0.5% 的佣金，并以 RUNE 的形式直接获得收益。

## 资产格式

所有资产均采用 `CHAIN.TICKER` 格式进行表示：
- `ETH.ETH` — 以太坊原生资产
- `BTC.BTC` — 比特币
- `THOR.RUNE` — THORChain 原生资产
- `AVAX.AVAX` — Avalanche 原生资产
- `ETH.USDC-0xA0b86...` — 包含合约地址的 ERC-20 代币

## 环境变量（适用于自托管环境）

```bash
FEE_RECIPIENT_ADDRESS=forgemb   # THORName or thor1... address for affiliate fees
SWAP_FEE_BPS=50                 # 50 = 0.5%
PORT=3000
ALLOWED_ORIGINS=*
```

## 收益模式

通过 FORGE 进行的每笔交易都会向 `forgemb`（THORChain 中的账户名：`thor1yfrfgjgnzkjqqgv02yxn3j3kv50pe0rnhvs8zw`）支付 0.5% 的佣金。佣金会直接包含在 THORChain 的交易备忘录中，并由协议自动结算，无需额外开票或离链对账。