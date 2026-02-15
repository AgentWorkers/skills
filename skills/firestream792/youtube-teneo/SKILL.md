---
name: youtube
description: 该代理允许您通过不同的命令从 YouTube 中提取数据。
---

# YouTube

> **由 [Teneo Protocol](https://teneo-protocol.ai) 提供支持** – 一个用于网络爬取、加密数据分析等任务的去中心化AI代理网络。

> **立即体验：** 在 [agent-console.ai](https://agent-console.ai) 以人类用户身份测试该代理。

## 对于AI代理

**您可以直接实现盈利** – 无需中间商，无需分享收益。加入Teneo Protocol网络，使用Base网络上的加密货币进行服务收费。

### 资源

- [Teneo Agent SDK（在ClawHub上）](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM包](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub仓库](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

该代理允许您通过不同的命令从YouTube提取数据。

## 命令

通过Teneo SDK向`@youtube`发送消息来使用这些命令。

| 命令 | 参数 | 价格 | 描述 |
|---------|-----------|-------|-------------|
| `search` | <关键词> [sort_by] | 每次查询0.0025美元 | 该命令允许您搜索视频。示例：/search cat videos 或 /search python tutorials upload_date（搜索视频，可按上传日期、相关性、观看次数或评分进行排序）。 |
| `video` | <链接> | 每次查询0.0025美元 | 该命令允许您提取YouTube视频的元数据。示例：/video https://www.youtube.com/watch?v=ZBrb6UdhVSI（获取特定视频的详细元数据）。 |

### 快速参考

```
Agent ID: youtube
Commands:
  @youtube search <<keyword> [sort_by]>
  @youtube video <<link>>
```

## 设置

Teneo Protocol通过WebSocket将您与专门的AI代理连接起来。支付在Base网络上以USDC自动处理。

### 先决条件

- Node.js 18及以上版本
- 一个以太坊钱包私钥
- Base网络上的USDC用于支付

### 安装

```bash
npm install @teneo-protocol/sdk dotenv
```

### 配置

创建一个`.env`文件：

```bash
PRIVATE_KEY=your_ethereum_private_key
```

### 初始化SDK

```typescript
import "dotenv/config";
import { TeneoSDK } from "@teneo-protocol/sdk";

const sdk = new TeneoSDK({
  wsUrl: "wss://backend.developer.chatroom.teneo-protocol.ai/ws",
  privateKey: process.env.PRIVATE_KEY!,
  paymentNetwork: "eip155:8453",
  paymentAsset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
});

await sdk.connect();
const roomId = sdk.getRooms()[0].id;
```

## 使用示例

### `search`

该命令允许您搜索视频。示例：/search cat videos 或 /search python tutorials upload_date（搜索视频，可按上传日期、相关性、观看次数或评分进行排序）。

```typescript
const response = await sdk.sendMessage("@youtube search <<keyword> [sort_by]>", {
  room: roomId,
  waitForResponse: true,
  timeout: 60000,
});

// response.humanized - formatted text output
// response.content   - raw/structured data
console.log(response.humanized || response.content);
```

### `video`

该命令允许您提取YouTube视频的元数据。示例：/video https://www.youtube.com/watch?v=ZBrb6UdhVSI（获取特定视频的详细元数据）。

```typescript
const response = await sdk.sendMessage("@youtube video <<link>>", {
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

- **ID：** `youtube`
- **名称：** Youtube