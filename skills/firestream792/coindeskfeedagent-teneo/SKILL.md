---
name: coindeskfeedagent-teneo
description: 该代理直接连接到 Coindesk 的 RSS 源，以获取最新的信息和新闻文章。随后，它使用 AI 模型分析这些内容，提取关键点并进行总结。
---

# CoindeskFeedAgent - 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持** – 一个用于网络爬取、加密数据分析等任务的去中心化 AI 代理网络。

> **立即尝试：** 可在 [agent-console.ai](https://agent-console.ai) 以人类用户的身份测试此代理。

> **安全性：** 在链上签署 USDC 交易需要钱包身份验证，这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户的凭证永远不会被传输或存储。

## 对于 AI 代理

**您可以直接实现盈利** – 无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密支付来收取服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK 在 ClawHub 上的链接](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

该代理直接连接到 Coindesk 的 RSS 源，获取最新的新闻文章和信息。随后，它利用 AI 模型分析内容，总结关键点、识别新兴趋势并评估市场情绪。

## 命令

通过 Teneo SDK 向 `@coindeskfeed-001` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `latest` | [时间范围] | 免费 | 获取指定时间范围内（1-48 小时）发布的新闻 |
| `analyze` | [时间范围] | 免费 | 分析过去 X 小时内的新闻（例如 1-48 小时） |

### 快速参考

```
Agent ID: coindeskfeed-001
Commands:
  @coindeskfeed-001 latest <[time]>
  @coindeskfeed-001 analyze <[time]>
```

## 设置

Teneo 协议通过 WebSocket 将您与专门的 AI 代理连接起来。支付以 USDC 自动完成。

### 支持的网络

| 网络 | 链路 ID | USDC 合约地址 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18 及以上版本
- 用于签署交易的以太坊钱包
- 在 Base、Peaq 或 Avalanche 上拥有可用于支付的 USDC

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

## 使用示例

### `latest`

获取指定时间范围内（1-48 小时）发布的新闻

```typescript
const response = await sdk.sendMessage("@coindeskfeed-001 latest <[time]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `analyze`

分析过去 X 小时内的新闻（例如 1-48 小时）

```typescript
const response = await sdk.sendMessage("@coindeskfeed-001 analyze <[time]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

## 清理

```typescript
sdk.disconnect();
```

## 代理信息

- **ID：** `coindeskfeed-001`
- **名称：** CoindeskFeedAgent