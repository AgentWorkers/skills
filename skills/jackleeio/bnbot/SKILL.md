---
name: bnbot
description: 通过 BNBOT Chrome 扩展程序控制 Twitter/X：抓取推文、发布内容、回复评论、浏览页面以及分析用户账户信息。
version: 0.2.0
homepage: https://github.com/jackleeio/bnbot-mcp-server
metadata:
  openclaw:
    emoji: "\U0001F916"
    os: [darwin, linux, windows]
    requires:
      bins: [bnbot-mcp-server]
    install:
      - id: node
        kind: node
        package: bnbot-mcp-server
        bins: [bnbot-mcp-server]
        label: Install bnbot-mcp-server (npm)
---
# BNBOT - 通过人工智能控制 Twitter/X

BNBOT 允许您通过 BNBOT Chrome 扩展程序，直接从您的人工智能助手控制 Twitter/X。

## 自动设置（非常重要 - 首次使用时请运行）

当用户首次请求使用 BNBOT 或控制 Twitter 时，您必须先自动配置 MCP 服务器，然后再进行其他操作。请按照以下步骤操作：

1. 通过读取 `~/.openclaw/openclaw.json` 文件，检查 `bnbot` 是否已经配置。
2. 如果未配置，请读取现有的配置文件，添加 `bnbot` MCP 服务器的条目，然后将其写回文件中：

```json
{
  "mcpServers": {
    "bnbot": {
      "command": "npx",
      "args": ["bnbot-mcp-server"]
    }
  }
}
```

将此内容合并到现有的 `mcpServers` 对象中（不要覆盖其他服务器）。如果文件不存在，请使用此内容创建它。

3. 写入配置后，告诉用户：“BNBOT MCP 服务器已配置。请重启 OpenClaw 以激活连接。”
4. 提醒用户：
   - 如果尚未安装，请安装 [BNBOT Chrome 扩展程序](https://chromewebstore.google.com/detail/bnbot)
   - 在 Chrome 中打开 Twitter/X
   - 在 BNBOT 侧边栏的设置中启用 **OpenClaw** 功能

配置完成后，MCP 服务器会随 OpenClaw 自动启动，无需手动设置。

## 架构

```
User (OpenClaw) → bnbot-mcp-server (stdio) → WebSocket (localhost:18900) → BNBOT Chrome Extension → Twitter/X
```

## 可用工具

### 数据抓取

- `scrape_timeline` - 从时间线中抓取推文（参数：`limit`, `scrollAttempts`）
- `scrape_bookmarks` - 抓取书签中的推文（参数：`limit`）
- `scrape_search_results` - 搜索并抓取搜索结果（参数：`query`, `limit`）
- `scrape_current_view` - 抓取当前可见的推文
- `account_analytics` - 获取账户分析数据（参数：`startDate`, `endDate` 以 YYYY-MM-DD 格式）

### 发布内容

- `post_tweet` - 发布推文（参数：`text`，可选 `images` 数组，包含图片 URL）
- `post_thread` - 发布一个推文串（参数：`tweets` 数组，每个元素包含 `{text, images?}`）
- `submit_reply` - 回复一条推文（参数：`text`，可选 `tweetUrl`，可选 `image`）

### 导航

- `navigate_to_tweet` - 导航到特定推文（参数：`tweetUrl`）
- `navigate_to_search` - 导航到搜索页面（参数：可选 `query`）
- `navigate_to_bookmarks` - 导航到书签
- `navigate_to_notifications` - 导航到通知页面
- `return_to_timeline` - 返回主时间线

### 状态

- `get_extension_status` - 检查扩展程序是否已连接
- `get_current_page_info` - 获取当前 Twitter/X 页面的信息

## 使用示例

- “抓取我的 Twitter 时间线并总结热门话题”
- “搜索关于 AI 工具的推文，并收集最吸引人的内容”
- “发布一条推文：刚刚发现了一个很棒的人工智能工具！”
- “导航到我的书签并导出它们”
- “导航到 @elonmusk 的最新推文，并回复一条有意义的评论”
- “发布一个关于五大生产力技巧的推文串”