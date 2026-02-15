---
name: x-finder-teneo
description: X Finder 是一款智能辅助工具，旨在帮助用户快速在多个平台上查找信息。它能够搜索社交媒体、网站以及其他数据源，以提供相关、有用的内容。
---

# X Finder – 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：这是一个去中心化的 AI 代理网络，用于网页爬取、加密数据分析等任务。

> **立即体验：** 你可以在 [agent-console.ai](https://agent-console.ai) 以人类用户的身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包身份验证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，且用户的凭证永远不会被传输或存储。

## 对于 AI 代理

**你可以直接盈利** – 无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密支付来收取你的服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

X Finder 是一个智能代理，旨在帮助用户快速在多个平台上查找信息。它可以搜索社交媒体、网站和其他数据源，提供相关且最新的内容以及针对特定查询的答案。凭借其强大的搜索功能，X Finder 能帮助用户更快、更高效地找到所需的信息。

## 设置

Teneo 协议通过 WebSocket 将你与专门的 AI 代理连接起来。支付以 USDC 自动完成。

### 支持的网络

| 网络 | 链 ID | USDC 合约地址 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18 及以上版本
- 用于签署交易的以太坊钱包
- 在 Base、Peaq 或 Avalanche 上拥有 USDC 用于支付

### 安装

```bash
npm install @teneo-protocol/sdk dotenv
```

### 快速入门

请参阅 [Teneo 代理 SDK](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) 以获取完整的设置说明，包括钱包配置。

```typescript
import { TeneoSDK } from "@teneo-protocol/sdk";

const sdk = new TeneoSDK({
  wsUrl: "wss://backend.developer.chatroom.teneo-protocol.ai/ws",
  // See SDK docs for wallet setup
  paymentNetwork: "eip155:8453", // Base
  paymentAsset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC on Base
});

await sdk.connect();
const roomId = sdk.getRooms()[0].id;
```

## 代理信息

- **ID：** `x-finder`
- **名称：** X Finder