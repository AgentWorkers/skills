---
name: search-x
version: "1.1.0"
description: 实时X/Twitter搜索功能由Grok-4提供支持。该功能可帮助用户查找推文、热门话题以及带有引用信息的讨论内容。Grok-4.20版本还能够在返回推文引用的同时，一并展示相关图片。
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-search-x
homepage: https://docs.x.ai
triggers:
  - search x
  - search twitter
  - find tweets
  - what's on x about
  - x search
  - twitter search
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      env:
        - XAI_API_KEY
    primaryEnv: XAI_API_KEY
    tags:
      - x
      - twitter
      - search
      - grok
      - real-time
---
# 在 X 上搜索

实时搜索 X/Twitter 的功能由 Grok 的 `x_search` 工具提供，可以获取包含引用信息的真实推文。

## 设置

设置您的 xAI API 密钥：

```bash
openclaw config set skills.entries.search-x.apiKey "xai-YOUR-KEY"
```

或者使用环境变量：
```bash
export XAI_API_KEY="xai-YOUR-KEY"
```

您可以在以下链接获取 API 密钥：https://console.x.ai

## 命令

### 基本搜索
```bash
node {baseDir}/scripts/search.js "AI video editing"
```

### 按时间筛选
```bash
node {baseDir}/scripts/search.js --days 7 "breaking news"
node {baseDir}/scripts/search.js --days 1 "trending today"
```

### 按用户名筛选
```bash
node {baseDir}/scripts/search.js --handles @elonmusk,@OpenAI "AI announcements"
node {baseDir}/scripts/search.js --exclude @bots "real discussions"
```

### 输出选项
```bash
node {baseDir}/scripts/search.js --json "topic"        # Full JSON response
node {baseDir}/scripts/search.js --compact "topic"     # Just tweets, no fluff
node {baseDir}/scripts/search.js --links-only "topic"  # Just X links
```

## 在聊天中的示例用法

**用户：“在 X 上搜索人们对 Claude Code 的评价”**
**操作：** 使用查询 “Claude Code” 运行搜索

**用户：“查找 @remotion_dev 在过去一周内发布的推文”**
**操作：** 使用 `--handles @remotion_dev --days 7` 运行搜索

**用户：“今天 Twitter 上关于 AI 的热门话题是什么？”**
**操作：** 使用 `--days 1 "AI trending"` 运行搜索

**用户：“在 X 上搜索 Remotion 的最佳实践（过去 30 天内）”**
**操作：** 使用 `--days 30 "Remotion best practices"` 运行搜索

## 工作原理

该功能通过 xAI 的 `responses` API（`/v1/responses`）与 `x_search` 工具配合使用：
- 使用的模型：`grok-4-1-fast`（专为高效搜索优化）
- 返回包含链接的真实推文
- 提供引用信息以验证推文的真实性
- 支持按日期和用户名进行筛选

## 响应格式

每个搜索结果包括：
- **@username**（显示名称）
- 推文内容
- 日期/时间
- 推文的直接链接

## 环境变量

- `XAI_API_KEY` - 您的 xAI API 密钥（必填）
- `SEARCH_X_MODEL` - 可选的模型（默认：grok-4-1-fast）
- `SEARCH_X_DAYS` - 默认的搜索天数（默认：30）