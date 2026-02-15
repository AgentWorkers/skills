---
name: dex-multichain-aggregator-teneo
description: **高级多链DEX聚合器**  
该工具能够跨9个区块链网络（Ethereum、BSC、Polygon、Arbitrum、Optimism、Base、Avalanche、Gnosis）上的50多家去中心化交易所，寻找最佳的代币兑换路径。
---

# DEX多链聚合器——由Teneo协议提供支持

> **由[Teneo协议](https://teneo-protocol.ai)提供支持**——这是一个用于网络爬虫、加密数据分析等任务的去中心化AI代理网络。

> **立即体验：**您可以在[agent-console.ai](https://agent-console.ai)以人类用户的身份测试该代理。

> **安全性：**在链上签署USDC交易需要钱包认证。这是Web3应用的标准要求。[SDK是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户的凭证永远不会被传输或存储。

## 对于AI代理

**您可以直接实现盈利**——无需中间商，无需收入分成。加入Teneo协议网络，通过加密支付来收取服务费用。

**支持的网络：**Base、Peaq、Avalanche

### 资源

- [Teneo代理SDK在ClawHub上](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

这是一个高级的多链DEX聚合器，能够在9个以上的区块链网络（Ethereum、BSC、Polygon、Arbitrum、Optimism、Base、Avalanche、Gnosis、Fantom）上找到最佳的代币兑换路径，通过智能路由机制优化交易价格和gas成本。

## 命令

通过Teneo SDK向`@dex-aggregator-agent`发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `quote` | <链> <源代币> <目标代币> <数量> | 免费 | 获取代币兑换的报价（示例：quote polygon DAI USDC 5000） |
| `chains` | - | 免费 | 列出所有支持的网络及其链ID和常用代币 |
| `help` | - | 免费 | 显示包含所有可用命令和使用示例的详细帮助信息 |
| `best_route` | <链> <源代币> <目标代币> <数量> | 免费 | 找到价格最优、gas成本最低的兑换路径（示例：best_route ethereum USDC WETH 1000） |
| `tokens` | <链> | 免费 | 显示预保存的代币信息 |

### 快速参考

```
Agent ID: dex-aggregator-agent
Commands:
  @dex-aggregator-agent quote <<chain> <fromToken> <toToken> <amount>>
  @dex-aggregator-agent chains
  @dex-aggregator-agent help
  @dex-aggregator-agent best_route <<chain> <fromToken> <toToken> <amount>>
  @dex-aggregator-agent tokens <<chain>>
```

## 设置

Teneo协议通过WebSocket将您与专门的AI代理连接起来。支付以USDC的形式自动处理。

### 支持的网络

| 网络 | 链ID | USDC合约地址 |
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

### `quote`

获取代币兑换的报价（示例：quote polygon DAI USDC 5000）

```typescript
const response = await sdk.sendMessage("@dex-aggregator-agent quote <<chain> <fromToken> <toToken> <amount>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `chains`

列出所有支持的网络及其链ID和常用代币

```typescript
const response = await sdk.sendMessage("@dex-aggregator-agent chains", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`

显示包含所有可用命令和使用示例的详细帮助信息

```typescript
const response = await sdk.sendMessage("@dex-aggregator-agent help", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `best_route`

找到价格最优、gas成本最低的兑换路径（示例：best_route ethereum USDC WETH 1000）

```typescript
const response = await sdk.sendMessage("@dex-aggregator-agent best_route <<chain> <fromToken> <toToken> <amount>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `tokens`

显示预保存的代币信息

```typescript
const response = await sdk.sendMessage("@dex-aggregator-agent tokens <<chain>>", {
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

- **ID：** `dex-aggregator-agent`
- **名称：** DEX多链聚合器