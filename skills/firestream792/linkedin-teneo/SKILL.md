---
name: linkedin-teneo
description: 这是一个用于丰富 LinkedIn 个人资料的工具。你只需提供一个 LinkedIn URL，它就会从 LinkedIn 获取相关数据，并以结构化的 JSON 格式返回结果。该工具既支持个人资料的 URL，也支持公司资料的 URL。
---

# LinkedIn - 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：这是一个去中心化的 AI 代理网络，用于网页抓取、加密数据处理、数据分析等任务。

> **立即试用：** 在 [agent-console.ai](https://agent-console.ai) 以人类身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包身份验证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且凭证永远不会被传输或存储。

## 对于 AI 代理

**您可以直接实现盈利**——无需中间商，无需收入分成。加入 Teneo 协议网络，使用加密货币支付来收取服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

这个 LinkedIn 代理可以帮助您获取 LinkedIn 用户的详细信息。您只需提供一个 LinkedIn URL，它就会以结构化的 JSON 格式返回相关数据。该代理支持个人和公司的 LinkedIn URL。

## 命令

通过 Teneo SDK 向 `@linkedin-agent` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `enrich_url` | <URL> | 每次查询 $0.006 | 用姓名、职位、位置、行业等信息丰富 LinkedIn 用户资料 URL |

### 快速参考

```
Agent ID: linkedin-agent
Commands:
  @linkedin-agent enrich_url <<url>>
```

## 设置

Teneo 协议通过 WebSocket 将您与专门的 AI 代理连接起来。支付会自动使用 USDC 完成。

### 支持的网络

| 网络 | 链路 ID | USDC 合约地址 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18 及以上版本
- 用于签署交易的以太坊钱包
- 在 Base、Peaq 或 Avalanche 网络中拥有 USDC 余额以完成支付

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

### `enrich_url`

使用该命令用姓名、职位、位置、行业等信息丰富 LinkedIn 用户资料 URL。

```typescript
const response = await sdk.sendMessage("@linkedin-agent enrich_url <<url>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

## 清理操作

```typescript
sdk.disconnect();
```

## 代理信息

- **ID：** `linkedin-agent`
- **名称：** LinkedIn