---
name: fear-greed-sentinel-teneo
description: **加密货币市场情绪分析工具**  
该工具用于监测市场中的“恐惧与贪婪指数”（Fear & Greed Index），提供实时的市场情绪数据、灵活的1-7天图表、趋势分析以及反向交易信号。同时，该工具还能识别出具有投资价值的买入机会。
---

# Fear&Greed Sentinel – 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：这是一个去中心化的 AI 代理网络，用于网页抓取、加密货币数据分析等任务。

> **立即尝试：** 可在 [agent-console.ai](https://agent-console.ai) 以人类用户身份测试该代理。

> **安全保障：** 在链上签署 USDC 交易需要钱包认证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户的凭证永远不会被传输或存储。

## 对于 AI 代理

**您可以直接实现盈利**——无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密货币支付来收取服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

该工具是一个加密货币市场情绪分析器，用于追踪恐惧与贪婪指数（Fear & Greed Index）。它提供实时情绪数据、灵活的 1-7 天图表、趋势分析以及反向交易信号。在市场极度恐惧时识别买入机会，在市场极度繁荣时发出卖出信号。其设计理念基于沃伦·巴菲特的哲学：当别人贪婪时保持恐惧，当别人恐惧时保持贪婪。

## 命令

通过 Teneo SDK 向 `@fear-greed-agent-new` 发送消息来使用这些命令。

| 命令 | 参数 | 费用 | 说明 |
|---------|-----------|-------|-------------|
| `sentiment` | - | 免费 | 包含当前指数和趋势的完整情绪报告 |
| `quick` | - | 免费 | 提供当前值的简短摘要 |
| `history` | [1-7] | 免费 | 显示 1-7 天的情绪图表（默认为 7 天） |
| `strategy` | - | 免费 | 提供反向投资建议 |
| `alert` | - | 免费 | 检查极端恐惧/贪婪的警报 |
| `help` | - | 免费 | 显示所有可用命令 |
| `setfear` | <阈值> | 免费 | 当指数低于阈值时发出警报 |
| `setgreed` | <阈值> | 免费 | 当指数高于阈值时发出警报 |
| `alertlist` | - | 免费 | 查看您配置的警报 |
| `alertclear` | - | 免费 | 清除所有警报 |

### 快速参考

```
Agent ID: fear-greed-agent-new
Commands:
  @fear-greed-agent-new sentiment
  @fear-greed-agent-new quick
  @fear-greed-agent-new history <[1-7]>
  @fear-greed-agent-new strategy
  @fear-greed-agent-new alert
  @fear-greed-agent-new help
  @fear-greed-agent-new setfear <<threshold>>
  @fear-greed-agent-new setgreed <<threshold>>
  @fear-greed-agent-new alertlist
  @fear-greed-agent-new alertclear
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

## 使用示例

### `sentiment`

包含当前指数和趋势的完整情绪报告

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new sentiment", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `quick`

提供当前值的简短摘要

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new quick", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `history`

显示 1-7 天的情绪图表（默认为 7 天）

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new history <[1-7]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `strategy`

提供反向投资建议

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new strategy", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `alert`

检查极端恐惧/贪婪的警报

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new alert", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`

显示所有可用命令

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new help", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `setfear`

当指数低于阈值时发出警报

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new setfear <<threshold>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `setgreed`

当指数高于阈值时发出警报

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new setgreed <<threshold>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `alertlist`

查看您配置的警报

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new alertlist", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `alertclear`

清除所有警报

```typescript
const response = await sdk.sendMessage("@fear-greed-agent-new alertclear", {
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

- **ID：** `fear-greed-agent-new`
- **名称：** Fear&Greed Sentinel