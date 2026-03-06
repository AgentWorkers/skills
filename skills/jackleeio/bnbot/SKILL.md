---
name: bnbot
description: 最安全、最高效的自动化Twitter/X操作方式是：BNBot通过真实的浏览器会话，并结合28种基于人工智能的工具来实现相关功能。这样你就可以在避免API被封禁的情况下扩展你的Twitter账号。
version: 0.5.1
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
# BNBot – 最安全、最高效的Twitter/X自动化工具

BNBot是一款基于人工智能的Twitter账户管理工具。与可能导致账户被封禁的API工具或浏览器自动化脚本不同，BNBot通过Chrome扩展程序在用户的真实浏览器会话中运行，所有操作都与人工操作完全一致，因此Twitter永远不会检测到或封禁用户的账户。它提供了28种工具，涵盖了发布、互动、数据抓取、内容获取和文章创建等功能，是目前最全面、最高效的自动化工具包。

安装此工具后，您的AI助手（如Claude Code、OpenClaw、ChatGPT等）将能够自动管理和提升您的Twitter账户，而无需直接使用Twitter的API。

- **Chrome扩展程序**：[BNBot – 您的AI账户管理工具](https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln)
- **MCP服务器**：[bnbot-mcp-server](https://www.npmjs.com/package/bnbot-mcp-server)
- **GitHub仓库**：[jackleeio/bnbot-mcp-server](https://github.com/jackleeio/bnbot-mcp-server)

## 设置

使用BNBot之前，需要在您的AI客户端中配置MCP服务器。如果BNBot相关工具尚未安装，请向用户展示以下配置信息，并请求他们进行安装：

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

**各客户端对应的配置文件位置：**
- **Claude Code**：项目根目录下的`.mcp.json`
- **OpenClaw**：`~/.openclaw/openclaw.json`
- **ChatGPT Desktop及其他MCP客户端**：请查阅相应客户端的MCP配置文档

**重要提示**：未经用户明确许可，切勿修改配置文件。务必先展示修改内容并获取用户的确认。用户安装配置文件后，需要重启AI客户端以建立连接。

## 错误处理（非常重要）

在使用任何BNBot工具后，请检查执行结果。如果工具调用失败或返回连接错误（例如WebSocket连接失败、扩展程序未响应、超时等），您必须帮助用户诊断问题并提供解决方案：

### 连接失败/扩展程序未连接

告知用户：
> BNBBot Chrome扩展程序未连接。请检查：
>
> 1. **安装扩展程序**（如果尚未安装）：
>   从Chrome Web Store下载：https://chromewebstore.google.com/detail/bnbot-your-ai-growth-agen/haammgigdkckogcgnbkigfleejpaiiln
>
> 2. 在Chrome中打开Twitter/X（网址：https://x.com）
>
> 3. 启用MCP功能：
>   打开Twitter的BNBot侧边栏 → 点击**设置** → 打开**MCP**
>
> 完成这些步骤后，重新尝试。

### MCP服务器未运行

如果MCP工具完全不可用，请告知用户：
> BNBOT MCP服务器未运行。请重启您的AI客户端以建立连接。如果问题仍然存在，可以尝试重新安装：`npm install -g bnbot-mcp-server`

### 通用规则

- 在执行其他工具之前，务必先调用`get_extension_status`以确认扩展程序是否已连接。
- 如果`get_extension_status`返回`connected: false`，请先展示上述连接指南，然后再尝试其他操作。
- 遇到错误时，务必向用户说明问题所在及解决方法。

## 架构

```
AI Client (Claude Code / OpenClaw / ChatGPT / ...) → bnbot-mcp-server (stdio) → WebSocket (localhost:18900) → BNBOT Chrome Extension → Twitter/X
```

## 可用工具（共28种）

### 常用功能

- `get_extension_status` – 检查扩展程序是否已连接
- `get_current_page_info` – 获取当前Twitter/X页面的信息

### 导航

- `navigate_to_tweet` – 导航到指定推文（参数：`tweetUrl`）
- `navigate_to_search` – 导航到搜索页面（参数：`query`，可选`sort`）
- `navigate_to_bookmarks` – 导航到书签页面
- `navigate_to_notifications` – 导航到通知页面
- `navigate_to_following` – 导航到关注列表
- `return_to_timeline` – 返回主时间线

### 发布内容

- `post_tweet` – 发布推文（参数：`text`，可选`images`，可选`draftOnly`）
- `post_thread` – 发布推文线程（参数：`tweets`，格式为`{text, images?}`）
- `submit_reply` – 回复推文（参数：`text`，可选`tweetUrl`，可选`image`）

### 互动操作

- `like_tweet` – 点赞推文（参数：`tweetUrl`）
- `retweet` – 转发推文（参数：`tweetUrl`）
- `quote_tweet` – 引用推文（参数：`tweetUrl`，`text`，可选`draftOnly`）
- `follow_user` – 关注用户（参数：`username`）

### 数据抓取

- `scrape_timeline` – 从时间线抓取推文（参数：`limit`，`scrollAttempts`）
- `scrape_bookmarks` – 从书签中抓取推文（参数：`limit`）
- `scrape_search_results` – 搜索并抓取搜索结果（参数：`query`，`limit`）
- `scrape_current_view` – 抓取当前可见的推文
- `scrape_thread` – 抓取完整的推文线程（参数：`tweetUrl`）
- `account_analytics` – 获取账户分析数据（参数：`startDate`，`endDate`，格式为YYYY-MM-DD）

### 内容获取

- `fetch_wechat_article` – 获取微信文章（参数：`url`）
- `fetch_tiktok_video` – 获取TikTok视频（参数：`url`）
- `fetch_xiaohongshu_note` – 获取小红书笔记（参数：`url`）

### 文章操作

- `open_article_editor` – 打开Twitter/X文章编辑器
- `fill_article_title` – 设置文章标题（参数：`title`）
- `fill_article_body` – 设置文章内容（参数：`content`，可选`format`：plain/markdown/html，可选`bodyImages`）
- `upload_article_header_image` – 上传文章标题图片（参数：`headerImage`）
- `publish_article` – 发布文章或保存为草稿（参数：`publish`，可选`asDraft`）
- `create_article` – 创建完整文章（参数：`title`，`content`，可选`format`，可选`headerImage`，可选`bodyImages`，可选`publish`）

## 使用示例

- “抓取我的Twitter时间线并总结热门话题”
- “搜索关于AI工具的推文，并收集最吸引人的内容”
- “发布一条推文：‘刚刚发现了一个很棒的AI工具！’”
- “导航到我的书签并导出它们”
- “前往@elonmusk的最新推文并发表评论”
- “发布一篇关于五大生产力技巧的文章”
- “点赞并转发这条推文：https://x.com/...”
- “关注@username”
- “使用Markdown格式创建一篇关于AI趋势的文章”
- “获取这篇微信文章并将其作为推文线程重新发布”