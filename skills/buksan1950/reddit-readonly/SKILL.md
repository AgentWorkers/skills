---
name: reddit-readonly
description: >-
  Browse and search Reddit in read-only mode using public JSON endpoints.
  Use when the user asks to browse subreddits, search for posts by topic,
  inspect comment threads, or build a shortlist of links to review and reply to manually.
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["node"]}}}
---

# Reddit 只读功能

用于 Clawdbot 的只读 Reddit 浏览功能。

## 该功能的用途

- 在一个或多个子版块中查找帖子（热门/新帖/热门帖/有争议的帖/上升趋势的帖）
- 根据查询条件搜索帖子（在某个子版块内或所有子版块中）
- 获取帖子的评论信息以了解上下文
- 生成一个永久链接列表，方便用户直接在 Reddit 上进行回复

## 规则

- **仅限只读操作**。该功能不允许发布帖子、回复、投票或执行管理操作。
- 提出请求时请保持礼貌：
  - 最初建议请求少量数据（5–10 条）。
  - 仅在需要时扩展查询范围。
- 在向用户返回结果时，务必包含永久链接。

## 输出格式

所有命令将以 JSON 格式输出到标准输出（stdout）：
- 成功：`{"ok": true, "data": ... }`
- 失败：`{"ok": false, "error": { "message": "...", "details": "..." }`

## 命令

### 1) 列出某个子版块中的帖子

```bash
node {baseDir}/scripts/reddit-readonly.mjs posts <subreddit> \
  --sort hot|new|top|controversial|rising \
  --time day|week|month|year|all \
  --limit 10 \
  --after <token>
```

### 2) 搜索帖子

```bash
# Search within a subreddit
node {baseDir}/scripts/reddit-readonly.mjs search <subreddit> "<query>" --limit 10

# Search all of Reddit
node {baseDir}/scripts/reddit-readonly.mjs search all "<query>" --limit 10
```

### 3) 获取帖子的评论信息

```bash
# By post id or URL
node {baseDir}/scripts/reddit-readonly.mjs comments <post_id|url> --limit 50 --depth 6
```

### 4) 获取某个子版块中的最新评论

```bash
node {baseDir}/scripts/reddit-readonly.mjs recent-comments <subreddit> --limit 25
```

### 5) 获取帖子及其评论的完整内容

```bash
node {baseDir}/scripts/reddit-readonly.mjs thread <post_id|url> --commentLimit 50 --depth 6
```

### 6) 多子版块搜索辅助功能

当用户提供如下条件时使用该功能：
“在 r/a、r/b 和 r/c 子版块中查找过去 48 小时内发布的关于 X 的帖子，并排除 Y”

```bash
node {baseDir}/scripts/reddit-readonly.mjs find \
  --subreddits "python,learnpython" \
  --query "fastapi deployment" \
  --include "docker,uvicorn,nginx" \
  --exclude "homework,beginner" \
  --minScore 2 \
  --maxAgeHours 48 \
  --perSubredditLimit 25 \
  --maxResults 10 \
  --rank new
```

## 建议的代理工作流程

1. 如有需要，明确搜索范围：子版块 + 关键词 + 时间范围。
2. 使用 `find`（或 `posts`/`search`）命令进行搜索，并设置较小的查询数量。
3. 对于符合条件的 1–3 条帖子，使用 `thread` 命令获取其评论信息。
4. 向用户展示以下内容：
   - 帖子标题、子版块名称、得分、创建时间
   - 永久链接
   - 简要说明为何该帖子符合搜索条件
5. 如用户需要，可以提供一些回复的草稿建议，但请提醒用户自行在 Reddit 上进行回复。

## 故障排除

- 如果 Reddit 返回 HTML 内容，请重新运行命令（脚本会检测到这种情况并返回错误信息）。
- 如果请求多次失败，请减少 `--limit` 的值，或通过环境变量设置更慢的请求速度：

```bash
export REDDIT_RO_MIN_DELAY_MS=800
export REDDIT_RO_MAX_DELAY_MS=1800
export REDDIT_RO_TIMEOUT_MS=25000
export REDDIT_RO_USER_AGENT='script:clawdbot-reddit-readonly:v1.0.0 (personal)'
```