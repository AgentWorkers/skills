---
name: atxp
description: 您可以访问 ATXP 的付费 API 工具，这些工具支持网页搜索、AI 图像生成、音乐创作、视频制作以及 X/Twitter 搜索功能。当用户需要实时网页搜索、AI 生成的媒体内容（图片、音乐、视频），或进行 X/Twitter 搜索时，可以使用这些工具。使用前需通过 `npx atxp login` 进行身份验证。
---

# ATXP 工具

通过命令行界面（CLI）访问 ATXP 的付费 API 工具。

## 认证

```bash
# Check if authenticated
echo $ATXP_CONNECTION

# If not set, login:
npx atxp login
source ~/.atxp/config
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `npx atxp search <查询>` | 实时网络搜索 |
| `npx atxp image <提示>` | 人工智能图像生成 |
| `npx atxp music <提示>` | 人工智能音乐生成 |
| `npx atxp video <提示>` | 人工智能视频生成 |
| `npx atxp x <查询>` | X/Twitter 搜索 |

## 使用方法

1. 确保 `$ATXP_CONNECTION` 变量已设置；
2. 运行相应的命令；
3. 解析并显示搜索结果。

## 程序化访问

```typescript
import { atxpClient, ATXPAccount } from '@atxp/client';

const client = await atxpClient({
  mcpServer: 'https://search.mcp.atxp.ai',
  account: new ATXPAccount(process.env.ATXP_CONNECTION),
});

const result = await client.callTool({
  name: 'search_search',
  arguments: { query: 'your query' },
});
```

## MCP 服务器

| 服务器 | 工具 |
|--------|------|
| `search.mcp.atxp.ai` | `search_search` |
| `image.mcp.atxp.ai` | `image_create_image` |
| `music.mcp.atxp.ai` | `music_create` |
| `video.mcp.atxp.ai` | `create_video` |
| `x-live-search.mcp.atxp.ai` | `x_live_search` |