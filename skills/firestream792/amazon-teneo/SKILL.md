---
name: amazon-teneo
description: 该代理允许您通过不同的命令从亚马逊（Amazon）提取数据。
---

# 由 Teneo 协议支持的 Amazon 服务

> **由 [Teneo 协议](https://teneo-protocol.ai) 提供支持** – 一个用于网络爬取、加密数据分析等任务的去中心化 AI 代理网络。

> **立即体验：** 你可以在 [agent-console.ai](https://agent-console.ai) 以人类用户的身份测试该代理。

> **安全性：** 在链上签署 USDC 交易需要钱包身份验证。这是 Web3 应用的标准做法。[SDK 是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户的凭证永远不会被传输或存储。

## 关于 AI 代理

**你可以直接实现盈利** – 无需中间商，无需收入分成。加入 Teneo 协议网络，通过加密支付来收取你的服务费用。

**支持的网络：** Base、Peaq、Avalanche

### 资源

- [Teneo 代理 SDK（在 ClawHub 上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM 包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub 仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

该代理允许你通过不同的命令从 Amazon 获取数据。

## 命令

通过 Teneo SDK 向 `@amazon` 发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 说明 |
|---------|-----------|-------|-------------|
| `product` | <ASIN> [domain] | 每次查询 $0.0025 | 提取产品详情 |
| `search` | <关键词> [页面] [域名] [货币] [排序方式] | 每次查询 $0.0025 | 在 Amazon 上搜索产品，支持分页、国家筛选和排序。结果可以按畅销产品、最新发布、价格从低到高、价格从高到低、特色产品或平均评分排序。多词查询需使用引号（例如：“word1 word2”）。 |
| `reviews` | <ASIN> [域名] [货币] | 每次查询 $0.001 | 提取产品评论 |
| `help` | - | 免费 | 显示所有可用命令及其简要说明、所需输入和预期输出。 |

### 快速参考

```
Agent ID: amazon
Commands:
  @amazon product <<ASIN> [domain]>
  @amazon search <<keywords> [page] [domain] [currency] [sort-by]>
  @amazon reviews <<ASIN> [domain] [currency]>
  @amazon help
```

## 设置

Teneo 协议通过 WebSocket 将你连接到专门的 AI 代理。支付以 USDC 自动完成。

### 支持的网络

| 网络 | 链路 ID | USDC 合约地址 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18 及以上版本
- 用于签署交易的以太坊钱包
- 在 Base、Peaq 或 Avalanche 网络中拥有 USDC 账户以进行支付

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

### `product`  
提取产品详情

```typescript
const response = await sdk.sendMessage("@amazon product <<ASIN> [domain]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `search`  
在 Amazon 上搜索产品，支持分页、国家筛选和排序。结果可以按畅销产品、最新发布、价格从低到高、价格从高到低、特色产品或平均评分排序。多词查询需使用引号（例如：“word1 word2”）。

```typescript
const response = await sdk.sendMessage("@amazon search <<keywords> [page] [domain] [currency] [sort-by]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `reviews`  
提取产品评论

```typescript
const response = await sdk.sendMessage("@amazon reviews <<ASIN> [domain] [currency]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`  
显示所有可用命令及其简要说明、所需输入和预期输出。

```typescript
const response = await sdk.sendMessage("@amazon help", {
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

- **ID：** `amazon`  
- **名称：** Amazon