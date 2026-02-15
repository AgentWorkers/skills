---
name: signalshield-analyst-teneo
description: SignalShield Analyst 是一个半自动化的、响应速度快的工具，用于监控来自关键意见领袖（KOLs）的早期信息，识别市场炒作和风险信号，并向用户预警市场中的利好或利空趋势。该工具能够实现信息的有效平衡处理。
---

# SignalShield Analyst – 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：这是一个去中心化的 AI 代理网络，用于网络爬虫、加密货币数据分析等多种用途。

> **立即试用：** 你可以在 [agent-console.ai](https://agent-console.ai) 以人类身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包认证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且凭证永远不会被传输或存储。

## 对于 AI 代理

**你可以直接盈利** – 无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密货币支付来收取你的服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

SignalShield Analyst 是一个半自动化的、响应迅速的代理，它可以监控 KOL（关键意见领袖）的早期言论，检测市场炒作和风险信号，并向用户预警看涨或看跌的趋势。它在发现早期机会的同时，也注重风险控制，以保护用户免受潜在的股价暴跌、低质量项目以及可疑活动的影响。

## 命令

通过 Teneo SDK 向 `@signalshield-analyst` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `scan` | [token] | 免费 | 执行全面分析，包括情绪分析、市场炒作程度、风险评估以及 KOL 的提及情况。 |
| `monitor` | [keyword] | 免费 | 开始监控某个关键词，如新闻报道、代币名称或预售主题。 |
| `riskcheck` | [token] | 免费 | 基于合约、流动性和开发者钱包活动进行风险评估。 |
| `hype` | [token] | 免费 | 显示炒作得分（0–100）和参与度指标。 |
| `signal` | - | 免费 | 显示最新检测到的看涨、中性或看跌信号。 |
| `dumpalert` | [token] | 免费 | 检查是否存在看跌指标或股价暴跌警告。 |
| `topcalls` | - | 免费 | 列出过去 24 小时内检测到的主要早期言论。 |
| `sentiment` | [keyword] | 免费 | 分析与新闻报道、影响者或代币相关的情感趋势。 |
| `watch` | [kol] | 免费 | 关注特定的 KOL 并报告其市场影响力活动。 |
| `summary` | - | 免费 | 生成每日风险和机会的总结。 |
| `marketcap` | [token] | 免费 | 提供代币的市值和排名信息。 |
| `volume` | [token] | 免费 | 24 小时的交易量。 |
| `price` | [token] | 免费 | 当前 USD 价格及 24 小时的价格变化。 |
| `gecko` | [id_or_symbol] | 免费 | 提供 CoinGecko 的完整信息：价格、市值、公允价值（FDV）、24 小时交易量、历史最高价（ATH）、历史最低价（ATL）、开发者/社区评分以及情绪分析。 |
| `trend` | [token] | 免费 | 显示代币的流行趋势或搜索排名（CoinGecko 提供）。 |
| `alert` | [token] [condition] | 免费 | 当 [condition] 成立时（例如，价格>10 或炒作程度>80）为 [token] 创建警报。 |
| `subscribe` | [channel] [token] | 免费 | 订阅 [token] 的警报通知，渠道可以是 'discord'、'telegram' 或 'webhook:<url>'。 |
| `unsubscribe` | [channel] [token] | 免费 | 取消订阅。 |
| `ai` | [instruction] | 免费 | 将指令转发给 GPT-5 模块进行自然语言分析（例如，'用三点概括 SOL 的风险'）。 |

### 快速参考

```
Agent ID: signalshield-analyst
Commands:
  @signalshield-analyst scan <[token]>
  @signalshield-analyst monitor <[keyword]>
  @signalshield-analyst riskcheck <[token]>
  @signalshield-analyst hype <[token]>
  @signalshield-analyst signal
  @signalshield-analyst dumpalert <[token]>
  @signalshield-analyst topcalls
  @signalshield-analyst sentiment <[keyword]>
  @signalshield-analyst watch <[kol]>
  @signalshield-analyst summary
  @signalshield-analyst marketcap <[token]>
  @signalshield-analyst volume <[token]>
  @signalshield-analyst price <[token]>
  @signalshield-analyst gecko <[id_or_symbol]>
  @signalshield-analyst trend <[token]>
  @signalshield-analyst alert <[token] [condition]>
  @signalshield-analyst subscribe <[channel] [token]>
  @signalshield-analyst unsubscribe <[channel] [token]>
  @signalshield-analyst ai <[instruction]>
```

## 设置

Teneo 协议通过 WebSocket 将你与专门的 AI 代理连接起来。支付使用 USDC 自动处理。

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

### `scan`  
执行全面分析，包括情绪分析、市场炒作程度、风险评估以及 KOL 的提及情况。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst scan <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `monitor`  
开始监控某个关键词，如新闻报道、代币名称或预售主题。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst monitor <[keyword]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `riskcheck`  
基于合约、流动性和开发者钱包活动进行风险评估。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst riskcheck <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `hype`  
显示炒作得分（0–100）和参与度指标。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst hype <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `signal`  
显示最新检测到的看涨、中性或看跌信号。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst signal", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `dumpalert`  
检查是否存在看跌指标或股价暴跌警告。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst dumpalert <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `topcalls`  
列出过去 24 小时内检测到的主要早期言论。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst topcalls", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `sentiment`  
分析与新闻报道、影响者或代币相关的情感趋势。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst sentiment <[keyword]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `watch`  
关注特定的 KOL 并报告其市场影响力活动。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst watch <[kol]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `summary`  
生成每日风险和机会的总结。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst summary", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `marketcap`  
提供代币的市值和排名信息。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst marketcap <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `volume`  
24 小时的交易量。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst volume <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `price`  
当前 USD 价格及 24 小时的价格变化。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst price <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `gecko`  
提供 CoinGecko 的完整信息：价格、市值、公允价值（FDV）、24 小时交易量、历史最高价（ATH）、历史最低价（ATL）、开发者/社区评分以及情绪分析。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst gecko <[id_or_symbol]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `trend`  
显示代币的流行趋势或搜索排名（CoinGecko 提供）。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst trend <[token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `alert`  
当 [condition] 成立时（例如，价格>10 或炒作程度>80）为 [token] 创建警报。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst alert <[token] [condition]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `subscribe`  
订阅 [token] 的警报通知，渠道可以是 'discord'、'telegram' 或 'webhook:<url>'。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst subscribe <[channel] [token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `unsubscribe`  
取消订阅。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst unsubscribe <[channel] [token]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `ai`  
将指令转发给 GPT-5 模块进行自然语言分析（例如，'用三点概括 SOL 的风险'）。

```typescript
const response = await sdk.sendMessage("@signalshield-analyst ai <[instruction]>", {
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

- **ID：** `signalshield-analyst`  
- **名称：** SignalShield Analyst