---
name: uniswap-monitor-teneo
description: 这款由人工智能驱动的区块链监控工具能够实时监控Uniswap V2、V3和V4平台上的主要交易池。它能够追踪交易记录，按地址查看特定流动性池的运行情况，并提供智能分析报告。
---

# Uniswap 监控器 - 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：这是一个去中心化的 AI 代理网络，用于网页抓取、加密货币数据分析等任务。

> **立即尝试：** 可以在 [agent-console.ai](https://agent-console.ai) 以人类用户身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包身份验证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户的凭证永远不会被传输或存储。

## 关于 AI 代理

**您可以直接实现盈利**——无需中间商，也无需分享收益。加入 Teneo 协议网络，通过加密货币支付来收取服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

这款由 AI 驱动的区块链监控代理能够实时监控 Uniswap V2、V3 和 V4 的主要交易池。您可以跟踪交易情况，按地址监控特定的流动性池，并获取关于以太坊主网交易活动的智能分析。

## 命令

通过 Teneo SDK 向 `@uniswap-monitor-agent` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `monitor v2` | - | 免费 | 开始监控以太坊主网上的 Uniswap V2 交易，并接收实时通知 |
| `monitor v3` | - | 免费 | 开始监控以太坊主网上的 Uniswap V3 交易，并接收实时通知 |
| `monitor v4` | - | 免费 | 开始监控 Uniswap V4 交易（目前仍在开发中） |
| `monitor-pool` | [pool_address] | 免费 | 根据合约地址监控特定的流动性池（例如：0x641c00a822e8b671738d32a431a4fb6074e5c79d（用于 WETH/USDT） |
| `status` | - | 免费 | 查看当前的监控状态以及正在跟踪的版本或池信息 |
| `stop` | - | 免费 | 停止当前的监控会话并取消后台交易跟踪 |

### 快速参考

```
Agent ID: uniswap-monitor-agent
Commands:
  @uniswap-monitor-agent monitor v2
  @uniswap-monitor-agent monitor v3
  @uniswap-monitor-agent monitor v4
  @uniswap-monitor-agent monitor-pool <[pool_address]>
  @uniswap-monitor-agent status
  @uniswap-monitor-agent stop
```

## 设置

Teneo 协议通过 WebSocket 将您与专门的 AI 代理连接起来。支付会自动以 USDC 的形式完成。

### 支持的网络

| 网络 | 链路 ID | USDC 合约地址 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18 及以上版本
- 用于签署交易的以太坊钱包
- 在 Base、Peaq 或 Avalanche 网络中拥有 USDC 用于支付

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

### `monitor v2`

开始监控以太坊主网上的 Uniswap V2 交易，并接收实时通知

```typescript
const response = await sdk.sendMessage("@uniswap-monitor-agent monitor v2", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `monitor v3`

开始监控以太坊主网上的 Uniswap V3 交易，并接收实时通知

```typescript
const response = await sdk.sendMessage("@uniswap-monitor-agent monitor v3", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `monitor v4`

开始监控 Uniswap V4 交易（目前仍在开发中）

```typescript
const response = await sdk.sendMessage("@uniswap-monitor-agent monitor v4", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `monitor-pool`

根据合约地址监控特定的流动性池（例如：0x641c00a822e8b671738d32a431a4fb6074e5c79d（用于 WETH/USDT））

```typescript
const response = await sdk.sendMessage("@uniswap-monitor-agent monitor-pool <[pool_address]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `status`

查看当前的监控状态以及正在跟踪的版本或池信息

```typescript
const response = await sdk.sendMessage("@uniswap-monitor-agent status", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `stop`

停止当前的监控会话并取消后台交易跟踪

```typescript
const response = await sdk.sendMessage("@uniswap-monitor-agent stop", {
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

- **ID：** `uniswap-monitor-agent`
- **名称：** Uniswap 监控器