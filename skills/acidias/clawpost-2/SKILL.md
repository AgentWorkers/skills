---
name: clawpost
description: 基于人工智能的社交媒体发布工具，适用于 LinkedIn 和 X（Twitter），具备算法优化和日程安排功能。
version: 0.1.3
metadata:
  openclaw:
    emoji: "📱"
    homepage: https://clawpost.dev
    primaryEnv: CLAW_API_KEY
    requires:
      env:
        - CLAW_API_KEY
      bins:
        - curl
---
# 社交媒体发布工具 Skill

ClawPost 可帮助您创建、管理和发布内容到 LinkedIn 和 X（Twitter）——支持人工智能辅助写作、草稿编辑、日程安排以及通过 API 直接发布内容。

## 入门

如果用户还没有账号或 API 密钥，请按照以下步骤操作：

1. **在 [clawpost.dev](https://clawpost.dev) 注册**——使用 LinkedIn 登录。
2. **连接平台**——在仪表板中，连接 LinkedIn 和/或 X（Twitter）账号。
3. **充值信用点数**——进入仪表板 → 账单，然后充值信用点数（最低 5 美元）。信用点数用于使用人工智能生成功能。
4. **生成 API 密钥**——进入仪表板 → 设置 → API 密钥 → 生成新密钥。密钥以 `claw_` 开头。
5. **设置环境变量**：
   ```bash
   export CLAW_API_KEY="claw_your_key_here"
   ```

## 设置

**必需的环境变量：**
- `CLAW_API_KEY` — 您的 API 密钥（以 `claw_` 开头）。请按照上述步骤生成密钥。

**可选环境变量：**
- `CLAW_API_URL` — 默认值为 `https://clawpost.dev`。仅在使用自托管实例时设置此变量。

所有端点的路径均为 `{{CLAW_API_URL}}/api/claw/v1/`（默认：`https://clawpost.dev/api/claw/v1/`）。

## 认证

每个请求都需要包含以下头部信息：
```
Authorization: Bearer {{CLAW_API_KEY}}
```

## 重要提示：在 shell 命令中传递 JSON 数据时

使用 `curl` 传输 JSON 数据时，**务必使用 heredoc 格式**，以避免引号和特殊字符导致的转义问题：
```bash
curl -s -X POST URL \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"key": "value"}
EOF
```
以下所有示例都遵循此格式。**切勿** 使用 `-d '{...}'` 与单引号结合——因为当内容包含引号、换行符或特殊字符时，这种方式会出错。

## 响应格式

所有响应都遵循以下结构：
```json
{
  "success": true,
  "message": "Human-readable summary",
  "data": { ... },
  "error": { "code": "ERROR_CODE", "details": "..." }
}
```

请务必查看 `message` 字段——该字段设计用于直接显示给用户。

## 端点

### 检查状态
验证您的 API 密钥是否有效，并查看已连接的平台。
```bash
curl -s {{CLAW_API_URL}}/api/claw/v1/status \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```

### 列出已连接的平台
```bash
curl -s {{CLAW_API_URL}}/api/claw/v1/platforms \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```

### 查看信用点数
```bash
curl -s {{CLAW_API_URL}}/api/claw/v1/credits \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```

### 列出帖子
可以按状态（`draft`、`published`、`scheduled`、`failed`）和平台（`linkedin`、`twitter`）进行筛选。
```bash
curl -s "{{CLAW_API_URL}}/api/claw/v1/posts?status=draft&platform=linkedin&limit=10" \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```

### X（Twitter）发布历史记录
从缓存的个人资料数据中检索您的 X（Twitter）发布历史记录。这是一个只读端点，不消耗信用点数。

查询参数：
- `type` - `posts`、`replies` 或 `all`（默认：`all`）
- `limit` - 最大结果数量，1-100 条（默认：20 条）
- `period` - `7d`、`30d`、`90d` 或 `all`（默认：`all`）

```bash
curl -s "{{CLAW_API_URL}}/api/claw/v1/history/x?type=posts&period=30d&limit=10" \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```

响应中包含一个 `summary` 对象，其中包含汇总指标（`totalPosts`、`totalReplies`、`totalLikes`、`totalRetweets`、`totalRepliesReceived`、`totalImpressions`、`topPost`），以及一个 `posts` 数组，其中包含每条帖子的详细信息、指标、媒体内容和回复上下文。

### 获取单条帖子
```bash
curl -s {{CLAW_API_URL}}/api/claw/v1/posts/POST_ID \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```
每条帖子都包含一个 `availableActions` 数组（例如：`["publish", "schedule", "update", "delete"]`）。

#### 帖子对象字段

每条帖子都包含一个 `postType` 字段：
- `"original"` — 由用户发布的普通帖子
- `"quote"` — 引用其他帖子的推文（仅限 X）
- `"reply"` — 对其他帖子的回复（仅限 X）
- `"remix"` — 受其他帖子启发的原创推文（仅限 X）

当 `postType` 为 `"quote"`、`reply` 或 `"remix` 时，帖子还会包含一个 `reference` 对象，其中包含原始帖子的上下文：
```json
{
  "postType": "quote",
  "content": "User's commentary text",
  "reference": {
    "tweetId": "1234567890",
    "text": "The original tweet text that was quoted",
    "author": "originalAuthor"
  }
}
```
这可以让您清楚地看到被引用或回复的内容以及用户自己的文本。

### 创建草稿
```bash
curl -s -X POST {{CLAW_API_URL}}/api/claw/v1/drafts \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"content": "Your post text here", "platform": "linkedin"}
EOF
```
平台可以是 `"linkedin"` 或 `"twitter"`。Twitter 的内容长度必须 ≤ 280 个字符。

### 更新草稿
```bash
curl -s -X PUT {{CLAW_API_URL}}/api/claw/v1/posts/POST_ID \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"content": "Updated post text"}
EOF
```

### 删除草稿
```bash
curl -s -X DELETE {{CLAW_API_URL}}/api/claw/v1/posts/POST_ID \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```

### 发布草稿
```bash
curl -s -X POST {{CLAW_API_URL}}/api/claw/v1/posts/POST_ID/publish \
  -H "Authorization: Bearer {{CLAW_API_KEY}}"
```

### 直接发布（无需草稿步骤）
```bash
curl -s -X POST {{CLAW_API_URL}}/api/claw/v1/publish \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"content": "Publishing this directly!", "platform": "linkedin"}
EOF
```

### 安排草稿的发布时间
```bash
curl -s -X POST {{CLAW_API_URL}}/api/claw/v1/posts/POST_ID/schedule \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"scheduledAt": "2026-06-15T10:00:00Z"}
EOF
```

### 直接安排发布时间（无需草稿步骤）
```bash
curl -s -X POST {{CLAW_API_URL}}/api/claw/v1/schedule \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"content": "Scheduled post!", "platform": "linkedin", "scheduledAt": "2026-06-15T10:00:00Z"}
EOF
```

### 通过 AI 生成帖子
让 AI 根据您的提示生成帖子。可选参数：`tone` 和 `platform`。
```bash
curl -s -X POST {{CLAW_API_URL}}/api/claw/v1/ai/generate \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"prompt": "Write about the importance of code reviews", "platform": "linkedin"}
EOF
```

### 通过 AI 优化帖子
根据指示对现有内容进行优化。
```bash
curl -s -X POST {{CLAW_API_URL}}/api/claw/v1/ai/refine \
  -H "Authorization: Bearer {{CLAW_API_KEY}}" \
  -H "Content-Type: application/json" \
  -d @- <<'EOF'
{"content": "Original post text...", "instructions": "Make it shorter and punchier", "platform": "linkedin"}
EOF
```

## 工作流程提示

1. **快速发布**：使用 `/publish` 立即发布帖子，无需创建草稿。
2. **审核流程**：先使用 `/drafts` 创建草稿，然后使用 `/ai/refine` 优化内容，最后使用 `/posts/ID/publish` 发布。
3. **跨平台发布**：分别为 LinkedIn 和 Twitter 发送请求——因为它们是独立的帖子。
4. **发布前检查**：调用 `/platforms` 确认目标平台已连接。
5. **Twitter 发布限制**：推文长度必须 ≤ 280 个字符。API 会拒绝超过此长度的内容，并给出明确提示。

## 错误代码

| 代码 | 含义 |
|------|---------|
| `UNAUTHORIZED` | API 密钥无效或已被吊销 |
| `NOT_FOUND` | 帖子或资源不存在 |
| `VALIDATION_ERROR` | 输入错误（缺少内容、内容过长、日期无效） |
| `CONFLICT` | 无法执行操作（例如，帖子已发布） |
| `PLATFORM_NOT_CONNECTED` | 目标社交平台未连接 |
| `INSUFFICIENT_CREDITS` | 用于 AI 操作的信用点数不足 |
| `NO.AI_KEY` | 未配置 AI API 密钥 |
| `RATE_LIMITED` | 请求次数过多（普通请求每分钟 60 次，发布请求每分钟 10 次） |
| `INTERNAL_ERROR` | 服务器端出现错误 |