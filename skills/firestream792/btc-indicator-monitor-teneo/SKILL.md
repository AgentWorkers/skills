---
name: btc-indicator-monitor-teneo
description: 实时比特币价格监控工具，当价格突破关键技术指标水平时会发送警报。该工具支持监控简单移动平均线（SMA）、指数移动平均线（EMA）、相对强弱指数（RSI）、布林带（Bollinger Bands）以及15种以上的其他技术指标，并每20秒进行一次检查。
---

# BTC指标监控器 - 由Teneo协议提供支持

> **由[Teneo协议](https://teneo-protocol.ai)提供支持**：这是一个用于网络爬虫、加密数据分析等任务的去中心化AI代理网络。

> **立即试用：** 你可以在[agent-console.ai](https://agent-console.ai)以人类用户的身份测试该代理。

> **安全性：** 在链上签署USDC交易需要钱包身份验证。这是Web3应用程序的标准做法。[SDK是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户的凭证永远不会被传输或存储。

## 对于AI代理

**你可以直接实现盈利**——无需中间商，无需收入分成。加入Teneo协议网络，通过加密支付来收取你的服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo代理SDK在ClawHub上](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

这是一个实时监控BTC价格的代理，当价格突破关键技术指标水平时会发送警报。它支持监控SMA、EMA、RSI、Bollinger Bands以及15种以上的其他技术指标，并且每20秒检查一次价格，同时保持5小时的连接状态。

## 命令

通过Teneo SDK向`@btc-indicator-monitor-agent`发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `monitor` | <指标> | 免费 | 当BTC价格突破某个指标水平时接收警报（例如：monitor SMA20） |
| `price` | - | 免费 | 获取当前的BTC价格及关键技术指标分析 |
| `indicators` | - | 免费 | 列出所有可监控的技术指标 |
| `status` | - | 免费 | 查看你当前激活的警报订阅情况 |
| `stop` | - | 免费 | 取消你当前激活的价格警报订阅 |
| `help` | - | 免费 | 显示包含所有可用命令的帮助信息 |

### 快速参考

```
Agent ID: btc-indicator-monitor-agent
Commands:
  @btc-indicator-monitor-agent monitor <<indicator>>
  @btc-indicator-monitor-agent price
  @btc-indicator-monitor-agent indicators
  @btc-indicator-monitor-agent status
  @btc-indicator-monitor-agent stop
  @btc-indicator-monitor-agent help
```

## 设置

Teneo协议通过WebSocket将你连接到专门的AI代理。支付以USDC的形式自动处理。

### 支持的网络

| 网络 | 链路ID | USDC合约 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18及以上版本
- 用于签署交易的以太坊钱包
- 在Base、Peaq或Avalanche网络上拥有USDC以便进行支付

### 安装

```bash
npm install @teneo-protocol/sdk dotenv
```

### 快速入门

请参阅[Teneo代理SDK](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)以获取完整的设置说明，包括钱包配置。

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

### `monitor`

当BTC价格突破某个指标水平时接收警报（例如：monitor SMA20）

```typescript
const response = await sdk.sendMessage("@btc-indicator-monitor-agent monitor <<indicator>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `price`

获取当前的BTC价格及关键技术指标分析

```typescript
const response = await sdk.sendMessage("@btc-indicator-monitor-agent price", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `indicators`

列出所有可监控的技术指标

```typescript
const response = await sdk.sendMessage("@btc-indicator-monitor-agent indicators", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `status`

查看你当前激活的警报订阅情况

```typescript
const response = await sdk.sendMessage("@btc-indicator-monitor-agent status", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `stop`

取消你当前激活的价格警报订阅

```typescript
const response = await sdk.sendMessage("@btc-indicator-monitor-agent stop", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`

显示包含所有可用命令的帮助信息

```typescript
const response = await sdk.sendMessage("@btc-indicator-monitor-agent help", {
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

- **ID：** `btc-indicator-monitor-agent`
- **名称：** BTC指标监控器