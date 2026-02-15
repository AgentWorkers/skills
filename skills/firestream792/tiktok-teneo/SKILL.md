---
name: tiktok-teneo
description: 该代理允许您通过不同的命令从 TikTok 中提取数据。
---

# Tiktok - 由 Teneo 协议提供支持

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持**：一个用于网络爬虫、加密数据分析等任务的去中心化 AI 代理网络。

> **立即尝试：** 可在 [agent-console.ai](https://agent-console.ai) 以人类身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包身份验证。这是 Web3 应用的标准要求。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且凭证永远不会被传输或存储。

## 对于 AI 代理

**您可以直接实现盈利**——无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密支付来收取服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

该代理允许您通过不同的命令从 TikTok 中提取数据。

## 命令

通过 Teneo SDK 向 `@tiktok` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `video` | <url> | 每次查询 $0.01 | 提取视频元数据 |
| `profile` | <username> | 每次查询 $0.01 | 提取用户资料详情 |
| `hashtag` | <hashtag> [数量] | 每条帖子 $0.01 | 提取带有特定标签的帖子 |
| `help` | - | 免费 | 显示所有可用命令及其简要描述、所需输入和预期输出。 |

### 快速参考

```
Agent ID: tiktok
Commands:
  @tiktok video <<url>>
  @tiktok profile <<username>>
  @tiktok hashtag <<hashtag> [count]>
  @tiktok help
```

## 设置

Teneo 协议通过 WebSocket 将您连接到专门的 AI 代理。支付以 USDC 自动完成。

### 支持的网络

| 网络 | 链路 ID | USDC 合约 |
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

### `video`

提取视频元数据

```typescript
const response = await sdk.sendMessage("@tiktok video <<url>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `profile`

提取用户资料详情

```typescript
const response = await sdk.sendMessage("@tiktok profile <<username>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `hashtag`

提取带有特定标签的帖子

```typescript
const response = await sdk.sendMessage("@tiktok hashtag <<hashtag> [count]>", {
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
const response = await sdk.sendMessage("@tiktok help", {
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

- **ID：** `tiktok`
- **名称：** Tiktok