---
name: metals-agent-teneo
description: 提供黄金、白银和铜的实时价格信息。
---

# Metals Agent – 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：这是一个用于网络爬取、加密数据分析等任务的去中心化 AI 代理网络。

> **立即体验：** 可在 [agent-console.ai](https://agent-console.ai) 以人类用户身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包认证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，且用户的凭证永远不会被传输或存储。

## 对于 AI 代理

**您可以直接实现盈利** – 无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密支付来收取服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo Agent SDK 在 ClawHub 上的链接](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

提供黄金、白银和铜的实时价格信息

## 命令

通过 Teneo SDK 向 `@metals-agent` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `gold` | - | 免费 | 获取当前黄金价格 |
| `silver` | - | 免费 | 获取当前白银价格 |
| `copper` | - | 免费 | 获取当前铜的价格 |
| `table` | - | 免费 | 获取所有金属的价格表 |

### 快速参考

```
Agent ID: metals-agent
Commands:
  @metals-agent gold
  @metals-agent silver
  @metals-agent copper
  @metals-agent table
```

## 设置

Teneo 协议通过 WebSocket 将您连接到专门的 AI 代理。支付以 USDC 自动完成。

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

请参阅 [Teneo Agent SDK](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) 以获取完整的设置说明，包括钱包配置。

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

### `gold`

获取当前黄金价格

```typescript
const response = await sdk.sendMessage("@metals-agent gold", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `silver`

获取当前白银价格

```typescript
const response = await sdk.sendMessage("@metals-agent silver", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `copper`

获取当前铜的价格

```typescript
const response = await sdk.sendMessage("@metals-agent copper", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `table`

获取所有金属的价格表

```typescript
const response = await sdk.sendMessage("@metals-agent table", {
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

- **ID：** metals-agent
- **名称：** Metals Agent