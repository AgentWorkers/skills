---
name: social-scheduler-extended
description: |
  Schedule and manage social media posts via Postiz API (self-hosted or cloud).
  Direct API integration — no n8n dependency.
  Supports X/Twitter, LinkedIn, Bluesky with platform-specific character limits.
  Includes deduplication, scheduling, media upload, and thread creation.

  WHAT IT CAN DO:
  - Schedule posts to 28+ channels (X, LinkedIn, Bluesky, Reddit, Instagram, Facebook, Threads, YouTube, TikTok, Pinterest, Mastodon, and more)
  - Multi-platform posting in a single API call with platform-adapted content
  - X/Twitter thread creation for longer content
  - Media upload (file and URL)
  - Find next available posting slot per channel
  - List, query, update, and delete scheduled posts
  - Deduplication workflow (check existing before posting)
  - Platform-specific character limits and content tone guidance
  - Post state management (QUEUE, PUBLISHED, ERROR, DRAFT)
  - Helper script for quick posting with auto-validation

  USE WHEN: scheduling social media posts, creating multi-platform content, managing a posting calendar, uploading media for social posts, checking post status, creating X/Twitter threads, or automating social media workflows.
---

# Postiz 社交媒体调度器

提供直接的社交媒体发布 API 集成功能，无需使用 n8n 工作流程。

## 快速参考

| 平台 | 集成 ID | 字符限制 | 处理方式 |
|----------|---------------|-----------------|--------|
| X/Twitter | `YOUR_X_INTEGRATION_ID` | **280** | @YourHandle |
| LinkedIn | `YOUR_LINKEDIN_INTEGRATION_ID` | **3,000** | your-linkedin |
| Bluesky | `YOUR_BLUESKY_INTEGRATION_ID` | **300** | your.bsky.social |

## 平台内容指南

### X/Twitter（280 个字符）
- 内容简短、精炼
- 最多使用 1-2 个标签
- 链接算作 23 个字符（使用 t.co 简化链接）
- 长内容可分多条推文发布

### LinkedIn（3,000 个字符）
- 采用专业的语气
- 可以写得更长
- 标签放在内容末尾（建议使用 3-5 个）
- 预览显示前 140 个字符——请确保这些字符对用户有吸引力！

### Bluesky（300 个字符）
- 与 X 类似，但允许稍长的内容
- 不支持官方标签（请谨慎使用）
- 主要面向技术/开发者群体

## 认证

```bash
# Login and save cookie (required before any API call)
curl -s -c /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email":"your-email@example.com","password":"your-password","provider":"LOCAL"}'
```

Cookie 会定期过期。如果遇到 401 错误，请重新登录。

## 查找下一个可用时间段

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/posts/find-slot/INTEGRATION_ID'
```

返回指定频道的下一个可用时间段，便于自动调度以避免冲突。

## 从 URL 上传媒体

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/media/upload-from-url' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com/image.png"}'
```

## 创建帖子

### 单一平台发布安排

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/posts' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "schedule",
    "date": "2026-02-05T15:00:00Z",
    "posts": [{
      "integration": {"id": "YOUR_X_INTEGRATION_ID"},
      "value": [{"content": "Your tweet here (max 280 chars)", "image": []}],
      "settings": {"__type": "x"}
    }]
  }'
```

### 多平台发布（内容适配）

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/posts' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "schedule",
    "date": "2026-02-05T15:00:00Z",
    "posts": [
      {
        "integration": {"id": "YOUR_X_INTEGRATION_ID"},
        "value": [{"content": "Short X version (280 chars max)", "image": []}],
        "settings": {"__type": "x"}
      },
      {
        "integration": {"id": "YOUR_LINKEDIN_INTEGRATION_ID"},
        "value": [{"content": "Longer LinkedIn version with more context and professional tone. Can be up to 3000 characters.", "image": []}],
        "settings": {"__type": "linkedin"}
      },
      {
        "integration": {"id": "YOUR_BLUESKY_INTEGRATION_ID"},
        "value": [{"content": "Bluesky version (300 chars max)", "image": []}],
        "settings": {"__type": "bluesky"}
      }
    ]
  }'
```

### 帖子类型
- `schedule` — 在指定日期/时间自动发布
- `draft` — 保存以供审核（不会自动发布）
- `now` — 立即发布

## 列出和查询帖子

### 按日期范围获取帖子（必选！）

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/posts?startDate=2026-02-01T00:00:00Z&endDate=2026-02-08T00:00:00Z' \
  | jq '.posts[] | {id, state, publishDate, platform: .integration.providerIdentifier, content: .content[0:60]}'
```

### 发布前检查重复内容

```bash
# Get recent posts and check content similarity
curl -s -b /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/posts?startDate=2026-02-01T00:00:00Z&endDate=2026-02-08T00:00:00Z' \
  | jq -r '.posts[] | "\(.integration.providerIdentifier): \(.content[0:80])"'
```

## 帖子状态

| 状态 | 描述 |
|-------|-------------|
| `QUEUE` | 已安排，等待发布 |
| `PUBLISHED` | 已成功发布 |
| `ERROR` | 发布失败 |
| `DRAFT` | 保存但未安排 |

## 媒体上传

### 上传图片

```bash
# Upload returns {id, path}
curl -s -b /tmp/postiz-cookies.txt \
  'https://your-postiz-instance.com/api/media/upload-simple' \
  -F 'file=@/path/to/image.png'
```

### 在帖子中使用图片

```json
"value": [{
  "content": "Post with image",
  "image": [{"id": "MEDIA_ID", "path": "/uploads/..."}]
}]
```

## Twitter/X 推文串

对于较长的内容，可以在 X 上创建推文串：

```json
"value": [
  {"content": "Tweet 1/3: Introduction to the topic...", "image": []},
  {"content": "Tweet 2/3: The main point explained...", "image": []},
  {"content": "Tweet 3/3: Conclusion and call to action.", "image": []}
]
```

## 管理帖子

### 删除帖子

```bash
curl -s -b /tmp/postiz-cookies.txt -X DELETE \
  'https://your-postiz-instance.com/api/posts/POST_ID'
```

### 更新发布计划

```bash
curl -s -b /tmp/postiz-cookies.txt -X PUT \
  'https://your-postiz-instance.com/api/posts/POST_ID/date' \
  -H 'Content-Type: application/json' \
  -d '{"date": "2026-02-06T10:00:00Z"}'
```

## 最佳实践

### 避免重复
1. 在创建新帖子前始终查询现有帖子
2. 在内容中使用唯一的标识符（如日期、具体引用）
3. 检查 `QUEUE` 和 `PUBLISHED` 状态

### 发布安排
- 每个平台之间至少间隔 2-4 小时发布
- 最佳发布时间：上午 9 点、中午 12 点、下午 5 点（根据目标受众时区）
- 避免同时向所有平台发布相同内容

### 内容适配
不要简单截断内容！针对每个平台重新编写：
- **X**：吸引人的开头 + 关键信息 + 行动号召
- **LinkedIn**：提供背景信息 + 价值主张 + 互动问题
- **Bluesky**：采用轻松的技术类语言

## 辅助脚本

使用 `scripts/post.py` 可简化发布流程，并自动验证字符长度：

```bash
# Single platform
~/.local/bin/uv run ~/clawd/skills/postiz/scripts/post.py \
  --platform x \
  --content "Your tweet here" \
  --schedule "2026-02-05T15:00:00Z"

# Multi-platform with different content
~/.local/bin/uv run ~/clawd/skills/postiz/scripts/post.py \
  --x "Short X version" \
  --linkedin "Longer LinkedIn version with more detail" \
  --bluesky "Bluesky version" \
  --schedule "2026-02-05T15:00:00Z"
```

## Web 用户界面

- 仪表板：https://your-postiz-instance.com
- 可视化日历视图
- 支持拖放式调度
- 提供分析和互动数据

## 故障排除

### 401 未授权错误
重新运行登录命令以刷新 Cookie。

### 帖子无法发布
1. 确认状态为 `QUEUE` 而非 `DRAFT`
2. 确认发布日期在未来
3. 在用户界面中检查集成是否仍然连接正常

### 帖子重复
创建新帖子前务必检查现有内容。API 不会自动检测重复内容。