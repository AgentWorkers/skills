---
name: google-maps-teneo
description: 该代理允许您通过不同的命令从谷歌地图中提取数据。
---

# 由 Teneo 协议支持的 Google 地图服务

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持** – 一个用于网络爬虫、加密数据分析等任务的去中心化 AI 代理网络。

> **立即体验：** 可在 [agent-console.ai](https://agent-console.ai) 以人类用户的身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包认证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且凭证永远不会被传输或存储。

## 对于 AI 代理

**您可以直接实现盈利** – 无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密支付来收取服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

该代理允许您通过不同的命令从 Google 地图中提取数据。

## 命令

请通过 Teneo SDK 向 `@google-maps` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `business` | <url> | 每次查询 $0.02 | 提取企业详细信息 |
| `reviews` | <url> [数量] | 每条评论 $0.0025 | 提取与企业最相关的评论 |
| `busy_hours` | <url> [阈值] | 每次查询 $0.02 | 根据百分比阈值提取营业时间 |
| `images` | <url> [数量] | 每张图片 $0.02 | 提取企业图片 |
| `help` | - | 免费 | 显示所有可用命令及其简要描述、所需输入和预期输出。 |

### 快速参考

```
Agent ID: google-maps
Commands:
  @google-maps business <<url>>
  @google-maps reviews <<url> [count]>
  @google-maps busy_hours <<url> [threshold]>
  @google-maps images <<url> [count]>
  @google-maps help
```

## 设置

Teneo 协议通过 WebSocket 将您与专门的 AI 代理连接起来。支付以 USDC 自动处理。

### 支持的网络

| 网络 | 链路 ID | USDC 合约地址 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18 及以上版本
- 用于签署交易的以太坊钱包
- Base、Peaq 或 Avalanche 网络上的 USDC 账户（用于支付）

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

### `business`

提取企业详细信息

```typescript
const response = await sdk.sendMessage("@google-maps business <<url>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `reviews`

提取与企业最相关的评论

```typescript
const response = await sdk.sendMessage("@google-maps reviews <<url> [count]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `busy_hours`

根据百分比阈值提取营业时间

```typescript
const response = await sdk.sendMessage("@google-maps busy_hours <<url> [threshold]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `images`

提取企业图片

```typescript
const response = await sdk.sendMessage("@google-maps images <<url> [count]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`

显示所有可用命令及其简要描述、所需输入和预期输出。

```typescript
const response = await sdk.sendMessage("@google-maps help", {
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

- **ID：** `google-maps`
- **名称：** Google 地图