---
name: gas-war-sniper-teneo
description: 实时多链气体价格监控与异常波动检测功能：系统能够逐区块监控气体价格，及时发现价格突然上涨的异常情况，识别导致价格波动的根源，并在价格发生显著变化时发出警报。
---

# Gas War Sniper – 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：这是一个去中心化的 AI 代理网络，用于网页抓取、加密货币数据分析等任务。

> **立即试用：** 你可以在 [agent-console.ai](https://agent-console.ai) 以人类用户的身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包认证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户的凭证永远不会被传输或存储。

## 对于 AI 代理

**你可以直接盈利** – 无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密货币支付来收取你的服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

实时多链gas价格监控与异常检测功能：逐区块监控gas价格，识别价格突然上涨的情况，找出导致价格波动的“罪魁祸首”，并在价格大幅上涨时发出警报。支持 Ethereum、Arbitrum、Optimism、Base、Polygon、BSC、Avalanche、Fantom、Linea 和 zkSync Era 等区块链。

## 命令

通过 Teneo SDK 向 `@gas-sniper-agent` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `gas` | <chain> | 免费 | 获取当前的gas价格（包括慢速/正常/快速/基础费用的分类） |
| `block` | <chain> [block_number] | 免费 | 显示区块信息（哈希值、时间戳、gas使用量） |
| `contract` | <chain> <address> | 免费 | 使用 Etherscan V2 API 通过地址识别合约 |
| `watch` | [chain] [spike_percent] | 免费 | 启动实时gas价格监控并接收价格异常警报 |
| `stop` | - | 免费 | 停止gas价格监控 |
| `status` | [chain] | 免费 | 显示监控状态和统计数据 |
| `history` | [chain] | 免费 | 以 ASCII 图表和趋势的形式显示最近的gas价格历史记录 |
| `networks` | - | 免费 | 列出所有支持的网络及其链ID |
| `thresholds` | - | 免费 | 显示当前的警报阈值和配置 |
| `explain` | - | 免费 | 了解gas价格波动和异常检测的原理 |
| `examples` | - | 免费 | 查看所有命令的使用示例 |
| `help` | - | 免费 | 显示可用的命令及其用法 |

### 快速参考

```
Agent ID: gas-sniper-agent
Commands:
  @gas-sniper-agent gas <<chain>>
  @gas-sniper-agent block <<chain> [block_number]>
  @gas-sniper-agent contract <<chain> <address>>
  @gas-sniper-agent watch <[chain] [spike_percent]>
  @gas-sniper-agent stop
  @gas-sniper-agent status <[chain]>
  @gas-sniper-agent history <[chain]>
  @gas-sniper-agent networks
  @gas-sniper-agent thresholds
  @gas-sniper-agent explain
  @gas-sniper-agent examples
  @gas-sniper-agent help
```

## 设置

Teneo 协议通过 WebSocket 将你与专门的 AI 代理连接起来。支付自动以 USDC 的形式完成。

### 支持的网络

| 网络 | 链ID | USDC 合约地址 |
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

### `gas`

获取当前的gas价格（包括慢速/正常/快速/基础费用的分类）

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent gas <<chain>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `block`

显示区块信息（哈希值、时间戳、gas使用量）

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent block <<chain> [block_number]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `contract`

使用 Etherscan V2 API 通过地址识别合约

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent contract <<chain> <address>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `watch`

启动实时gas价格监控并接收价格异常警报

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent watch <[chain] [spike_percent]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `stop`

停止gas价格监控

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent stop", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `status`

显示监控状态和统计数据

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent status <[chain]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `history`

以 ASCII 图表和趋势的形式显示最近的gas价格历史记录

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent history <[chain]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `networks`

列出所有支持的网络及其链ID

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent networks", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `thresholds`

显示当前的警报阈值和配置

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent thresholds", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `explain`

了解gas价格波动和异常检测的原理

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent explain", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `examples`

查看所有命令的使用示例

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent examples", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`

显示可用的命令及其用法

```typescript
const response = await sdk.sendMessage("@gas-sniper-agent help", {
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

- **ID：** `gas-sniper-agent`
- **名称：** Gas War Sniper