---
name: DECK-0
description: 与 DECK-0 数字收藏品平台进行交互，可以浏览收藏品、购买卡片包、打开卡片包、查看排行榜，以及申请成为平台发布者。当用户需要收集交易卡片、购买 NFT 包、管理自己的收藏品或创建自己的卡片收藏时，可以使用该平台。
homepage: https://app.deck-0.com
metadata: {"openclaw":{"emoji":"🃏","requires":{"bins":["cast","curl","jq","shasum"],"env":["DECK0_PRIVATE_KEY"]},"primaryEnv":"DECK0_PRIVATE_KEY"}}
---

# DECK-0 代理 API

## 概述

DECK-0 是一个数字收藏品平台，用户可以在其中收集并整理卡片。该 API 允许代理执行以下操作：

- **浏览** 商店并查看收藏品详情
- **购买** 卡片包（通过智能合约交易）
- **打开** 卡片包以查看卡片
- **跟踪** 收藏进度和排行榜排名
- **创建** 自己的卡片收藏

**基础 URL**: `https://app.deck-0.com`
**OpenAPI 规范**: `GET /api/agents/v1/openapi`（无需认证）

## 设置

### 钱包优先级

在签署 API 请求或发送交易时，请按照以下顺序使用钱包：

1. 运行时提供的现有代理钱包
2. 运行时提供的现有 Base 钱包
3. **DECK0_PRIVATE_KEY**（仅在以上两种钱包都不存在时使用）

**步骤 3 的备用设置**：

```bash
export DECK0_PRIVATE_KEY="0x..."
```

**可选的备用链覆盖**（仅用于 API 认证签名验证；合约操作使用来自收藏/价格响应的链和您的 RPC 选择）：

```bash
export DECK0_CHAIN_ID=8453
```

请使用经过审核的方法（例如 Homebrew）安装 [Foundry](https://book.getfoundry.sh/getting-started/installation)，然后验证 `cast` 是否可用：

```bash
brew install foundry
cast --version
```

此外，还需要使用以下工具：`curl`、`jq`、`shasum`（在 macOS/Linux 上为标准工具）。

**注意：** 所声明的依赖项（`cast`、`curl`、`jq`、`shasum`、`DECK0_PRIVATE_KEY`）是备用签名和购买/打开流程所必需的。仅用于浏览的功能可能不需要 `DECK0_PRIVATE_KEY` 或 `cast`，并且可以使用运行时提供的钱包。

购买卡片包需要使用原生代币（Apechain 上使用 APE，Base 上使用 ETH）。

## 安全注意事项

- 尽量使用运行时提供的钱包。
- `DECK0_PRIVATE_KEY` 是高度敏感的信息。仅在用户明确同意且任务需要签名或交易时才使用它。
- 严禁打印、记录或显示私钥值。

## 快速参考

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/api/agents/v1/shop/albums` | GET | 浏览可用的收藏品 |
| `/api/agents/v1/collections/{address}` | GET | 获取收藏品详情 |
| `/api/agents/v1/collections/{address}/leaderboard` | GET | 查看排行榜排名 |
| `/api/agents/v1/collections/{address}/price` | GET | 获取购买价格 |
| `/api/agents/v1/me/albums` | GET | 列出您的收藏品 |
| `/api/agents/v1/me/albums/{address}` | GET | 查看您的收藏品进度 |
| `/api/agents/v1/me/packs` | GET | 列出您的卡片包 |
| `/api/agents/v1/me/cards` | GET | 列出您的卡片 |
| `/api/agents/v1/me/pack-opening/{hash}` | GET | 获取卡片包打开的详细信息 |
| `/api/agents/v1/publisher/application` | GET | 检查发布者应用程序的状态 |
| `/api/agents/v1/publisher/application` | POST | 提交发布者应用程序 |
| `/api/agents/v1/openapi` | GET | OpenAPI 规范（无需认证） |

有关完整的请求/响应模式，请参阅 [endpoints.md](./endpoints.md)。

## 认证

所有端点（除 `/openapi` 外）都需要通过自定义头部发送 EIP-191 签名的请求：

| 头部 | 描述 |
|--------|-------------|
| `X-Agent-Wallet-Address` | 小写形式的钱包地址 |
| `X-Agent-Chain-Id` | 用于认证的 EVM 链 ID |
| `X-Agent-Timestamp` | 以毫秒为单位的 Unix 时间戳 |
| `X-Agent-Nonce` | 8-128 个字符的唯一字符串 |
| `X-Agent-Signature` | 标准有效负载的 EIP-191 签名 |

**签名所需的标准有效负载**：

```
deck0-agent-auth-v1
method:{METHOD}
path:{PATH}
query:{SORTED_QUERY}
body_sha256:{SHA256_HEX}
timestamp:{TIMESTAMP}
nonce:{NONCE}
chain_id:{CHAIN_ID}
wallet:{WALLET}
```

有关完整的签名流程及代码示例，请参阅 [auth.md](./auth.md)。

## 智能合约

购买和打开卡片包是在链上进行的操作：

1. **购买卡片包**：首先调用 `GET /api/agents/v1/collections/{address}/price` 获取签名后的价格，然后使用该签名和支付金额调用专辑合约上的 `mintPacks()` 方法。
2. **打开卡片包**：调用专辑合约上的 `openPacks.packIds)` 方法查看卡片，之后每 5 秒再次调用 `GET /api/agents/v1/me/pack-opening/{txHash}?chainId=...` 以获取卡片详情和徽章的详细信息。

**支付公式**：`value = (packPrice * priceInNative * quantity) / 100`

有关 ABI、支付计算和代码示例，请参阅 [smart-contracts.md](./smart-contracts.md)。

## 支持的网络

| 网络 | 链 ID | 货币 | 区块浏览器 |
|---------|----------|----------|----------------|
| Apechain 主网 | 33139 | APE | https://apescan.io |
| Base | 8453 | ETH | https://basescan.org |

## 响应格式

所有响应都遵循标准格式：

```json
// Success
{ "success": true, "data": { ... }, "share": { "url": "...", "imageUrl": "..." } }

// Error
{ "success": false, "error": { "code": "AGENT_...", "message": "...", "details": { ... } } }
```

有关所有错误代码和故障排除方法，请参阅 [errors.md](./errors.md)。

## 分享 URL

大多数响应包含指向 DECK-0 网页应用的 URL。**务必将这些 URL 提供给用户**，以便他们可以在浏览器中查看、分享或进一步探索：

- **`share.url`** — 大多数响应中都会包含此链接。指向相关页面（收藏品、排行榜、商店、卡片包打开详情等）。将此链接提供给用户以供分享。
- **`shareImageUrl`** — 如果可用，包含卡片包封面图片的预览 URL。可用于富媒体嵌入或预览。
- **`data(cards[].url`** — 在卡片包打开的响应中，每个卡片都会包含其详细页面的直接链接。将这些链接提供给用户，以便他们查看或分享单个卡片。

## 速率限制

- **每个钱包**：每分钟 60 次请求
- **每个 IP**：每分钟 120 次请求

速率限制相关的头部信息（`X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset`、`Retry-After`）会包含在 429 状态码的响应中。

## 意图映射

当用户执行以下操作时，系统会执行相应的操作：

- “显示可用的卡片收藏品” → 浏览商店中的专辑
- “告诉我关于收藏品 0x... 的信息” → 获取收藏品详情
- “从收藏品 0x... 中购买 3 个卡片包” → 获取签名后的价格，然后调用 `mintPacks`
- “打开我的卡片包” → 调用合约上的 `openPacks` 方法，然后定期调用 `getPackOpeningDetails` 获取详细信息
- “我得到了哪些卡片？” / “显示我的卡片包打开结果” → 获取卡片包打开的详细信息
- “我的收藏品进度如何？” → 获取我的收藏品列表
- “显示我的卡片包” / “我有哪些卡片包？” → 列出我的卡片包
- “显示我的卡片” / “我有哪些卡片？” → 列出我的卡片
- “显示排行榜” → 获取收藏品排行榜
- “分享我的卡片包打开结果” / “显示我的卡片链接” → 使用响应中的 `share.url` 或 `cards[].url`
- “我想创建自己的卡片收藏” → 提交发布者应用程序

## 支持文件

- **[auth.md](./auth.md)** — 完整的认证流程、签名代码和有效负载构建
- **[endpoints.md](./endpoints.md)** — 完整的 API 参考文档，包含所有请求/响应模式
- **[smart-contracts.md](./smart-contracts.md)** — 链上操作：购买/打开卡片包、ABI、代码示例
- **[examples.md](./examples.md)** — 包含请求/响应对的端到端工作流程示例
- **[errors.md](./errors.md)** — 错误代码、速率限制和故障排除方法