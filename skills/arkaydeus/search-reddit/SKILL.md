---
name: search-reddit
description: 使用 OpenAI 的 web_search 功能实时搜索 Reddit，并结合相关增强功能（如用户互动数据和热门评论）。当您需要获取最新的 Reddit 帖子、按子版块筛选的结果或快速查看链接列表时，可以使用此方法。
---

# 在 Reddit 上搜索

本功能利用 OpenAI 的 `web_search` API 实现实时搜索，并对搜索结果进行丰富处理（包括帖子的评分、评论以及热门评论的摘录）。

## 设置

请设置您的 OpenAI API 密钥：

```bash
clawdbot config set skills.entries.search-reddit.apiKey "sk-YOUR-KEY"
```

或者使用环境变量：
```bash
export OPENAI_API_KEY="sk-YOUR-KEY"
```

您也可以使用共享密钥：
```bash
clawdbot config set skills.entries.openai.apiKey "sk-YOUR-KEY"
```

## 命令

### 基本搜索
```bash
node {baseDir}/scripts/search.js "Claude Code tips"
```

### 按时间筛选
```bash
node {baseDir}/scripts/search.js --days 7 "AI news"
```

### 按子版块筛选
```bash
node {baseDir}/scripts/search.js --subreddits machinelearning,openai "agents"
node {baseDir}/scripts/search.js --exclude bots "real discussions"
```

### 输出选项
```bash
node {baseDir}/scripts/search.js --json "topic"        # JSON results
node {baseDir}/scripts/search.js --compact "topic"     # Minimal output
node {baseDir}/scripts/search.js --links-only "topic"  # Only Reddit links
```

## 在聊天中的使用示例

**用户：**“在 Reddit 上搜索关于 Claude Code 的内容”
**操作：**运行搜索命令：“Claude Code”

**用户：**“查找来自 r/OpenAI 的过去一周内的帖子”
**操作：**运行搜索命令：“--subreddits openai --days 7”

**用户：**“获取关于 Kimi K2.5 的 Reddit 链接”
**操作：**运行搜索命令：“--links-only Kimi K2.5”

## 工作原理

该功能通过 OpenAI 的 `responses` API（路径：`/v1/responses`）和 `web_search` 工具来实现：
- 允许访问的域名：`reddit.com`
- 通过获取 Reddit 的 JSON 数据（路径：`/r/.../comments/.../.json`）来丰富每个帖子的内容
- 根据 `created_utc` 字段更新帖子的创建时间，并仅显示过去 N 天内的帖子
- 计算帖子的互动量（如点赞、评论数等），并提取热门评论的摘录

## 环境变量

- `OPENAI_API_KEY` - OpenAI API 密钥（必需）
- `SEARCH_REDDIT_MODEL` - 可选的模型（默认值：gpt-5.2）
- `SEARCH_REDDIT_days` - 搜索的天数（默认值：30）