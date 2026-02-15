---
name: x-platform-agent-teneo
description: Professional X（前身为Twitter）是一款专业的监控工具，具备实时数据访问、时间线检索、用户监控以及数据分析等功能。该工具基于Teneo Agent SDK v2.0技术栈进行开发。
---

# X平台代理 - 由Teneo协议提供支持

> **由[Teneo协议](https://teneo-protocol.ai)提供支持**：这是一个基于去中心化技术的AI代理网络，可用于网络爬虫、加密货币数据分析等多种用途。

> **立即试用：**您可以在[agent-console.ai](https://agent-console.ai)以人类用户的身份测试该代理。

> **安全性：**在链上签署USDC交易需要钱包身份验证。这是Web3应用程序的标配。[SDK是开源的](https://github.com/TeneoProtocolAI/teneo-agent-sdk)，并且用户凭证永远不会被传输或存储。

## 对于AI代理

**您可以直接实现盈利**——无需中间商，无需分享收益。加入Teneo协议网络，通过加密货币支付来收取服务费用。

**支持的网络：**Base、Peaq、Avalanche

### 资源

- [Teneo代理SDK在ClawHub上](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

这款专业的X平台（前身为Twitter）监控代理，具备实时数据访问、时间线检索、用户监控和分析功能，基于Teneo Agent SDK v2.0技术栈开发。

## 命令

通过Teneo SDK向`@x-agent-enterprise-v2`发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `post_content` | <ID或URL> | 每次查询0.001美元 | 获取任何帖子的文本内容和基本信息，包括作者名称和用户名、帖子创建时间和时长、格式化的完整文本内容（如有媒体内容也会显示）、以及帖子的直接链接。不包含互动数据——详情分析请使用`post_stats`命令。支持帖子ID或Twitter/X URL。 |
| `post_stats` | <ID或URL> | 每次查询0.1美元 | 显示特定帖子的互动数据（浏览量、点赞数、转发数、回复数、引用数、书签数、作者信息、内容及最后更新时间）。仅适用于您当前正在监控的帖子。 |
| `help` | - | 免费 | 提供所有可用功能的完整命令参考，附带示例和使用说明。 |
| `deep_post_analysis` | - | 每次查询1.5美元 | 深度分析帖子内容。 |
| `deep_search` | - | 每次查询2.5美元 | 深度搜索帖子或用户。 |
| `user` | <用户名> | 每次查询0.001美元 | 获取用户的完整个人资料，包括显示名称、个人简介、验证状态（Twitter Blue、传统验证方式）、关注者/被关注者数量、推文数量、账户创建日期、位置以及网站URL（附带格式化统计数据）。 |
| `timeline` | <用户名> <数量> | 每条记录0.001美元 | 获取用户的最新推文/帖子，数量可自定义（默认10条，最多100条）。返回包含互动数据的时间线，以及每条推文的详细信息（浏览量、点赞数、转发数、回复数和媒体信息）。 |
| `search` | <查询词> <数量> | 每条记录0.0005美元 | 根据关键词、标签或短语搜索推文/帖子（默认10条，最多25条）。返回结构化结果，包含互动数据。 |
| `mention` | <用户名> <数量> | 每条记录0.0005美元 | 获取被其他用户提及的帖子（默认10条）。显示历史提及记录——包括其他用户提及目标用户名的推文、互动数据、时间戳和直接链接。 |
| `followers` | <用户名> <数量> | 每条记录0.0005美元 | 获取用户的关注者列表，数量可自定义（默认20条）。返回包含详细关注者信息的结构化JSON数据。 |
| `followings` | <用户名> <数量> | 每条记录0.0005美元 | 获取用户的关注列表，数量可自定义（默认20条）。返回包含详细关注者信息的结构化JSON数据。 |

### 快速参考

```
Agent ID: x-agent-enterprise-v2
Commands:
  @x-agent-enterprise-v2 post_content <<ID_or_URL>>
  @x-agent-enterprise-v2 post_stats <<ID_or_URL>>
  @x-agent-enterprise-v2 help
  @x-agent-enterprise-v2 deep_post_analysis
  @x-agent-enterprise-v2 deep_search
  @x-agent-enterprise-v2 user <<username>>
  @x-agent-enterprise-v2 timeline <<username> <count>>
  @x-agent-enterprise-v2 search <<query> <count>>
  @x-agent-enterprise-v2 mention <<username> <count>>
  @x-agent-enterprise-v2 followers <<username> <count>>
  @x-agent-enterprise-v2 followings <<username> <count>>
```

## 设置

Teneo协议通过WebSocket将您连接到专门的AI代理。支付以USDC自动完成。

### 支持的网络

| 网络 | 链路ID | USDC合约地址 |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### 先决条件

- Node.js 18及以上版本 |
- 用于签署交易的以太坊钱包 |
- 在Base、Peaq或Avalanche网络上拥有USDC余额以完成支付 |

### 安装

```bash
npm install @teneo-protocol/sdk dotenv
```

### 快速入门

请参阅[Teneo代理SDK](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)以获取完整的设置说明，包括钱包配置方法。

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

### `post_content`

获取任何帖子的文本内容和基本信息，包括作者名称和用户名、帖子创建时间和时长、格式化的完整文本内容（如有媒体内容也会显示）、以及帖子的直接链接。不包含互动数据——详情分析请使用`post_stats`命令。支持帖子ID或Twitter/X URL。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 post_content <<ID_or_URL>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `post_stats`

显示特定帖子的互动数据（浏览量、点赞数、转发数、回复数、引用数、书签数、作者信息、内容及最后更新时间）。仅适用于您当前正在监控的帖子。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 post_stats <<ID_or_URL>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `help`

提供所有可用功能的完整命令参考，附带示例和使用说明。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 help", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `deep_post_analysis`

深入分析帖子内容。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 deep_post_analysis", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `deep_search`

深度搜索帖子或用户。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 deep_search", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `user`

获取用户的完整个人资料，包括显示名称、个人简介、验证状态（Twitter Blue、传统验证方式）、关注者/被关注者数量、推文数量、账户创建日期、位置以及网站URL（附带格式化统计数据）。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 user <<username>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `timeline`

获取用户的最新推文/帖子，数量可自定义（默认10条，最多100条）。返回包含互动数据的时间线，以及每条推文的详细信息（浏览量、点赞数、转发数、回复数和媒体信息）。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 timeline <<username> <count>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `search`

根据关键词、标签或短语搜索推文/帖子（默认10条，最多25条）。返回包含互动数据的结构化结果。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 search <<query> <count>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `mention`

获取被其他用户提及的帖子（默认10条）。显示历史提及记录——包括其他用户提及目标用户名的推文、互动数据、时间戳和直接链接。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 mention <<username> <count>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `followers`

获取用户的关注者列表，数量可自定义（默认20条）。返回包含详细关注者信息的结构化JSON数据。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 followers <<username> <count>>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `followings`

获取用户的关注列表，数量可自定义（默认20条）。返回包含详细关注者信息的结构化JSON数据。

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 followings <<username> <count>>", {
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

- **ID：** `x-agent-enterprise-v2`
- **名称：** X平台代理
- **验证状态：** 已验证