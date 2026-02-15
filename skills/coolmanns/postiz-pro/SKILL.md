---
name: postiz
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

支持直接通过 API 发布社交媒体内容，无需使用 n8n 工作流程。

## 快速参考

| 平台 | 集成 ID | 字符限制 | 处理方式 |
|----------|---------------|-----------------|--------|
| X/Twitter | `cml5lbs3h0001o6l6gagj9gcq` | **280** | @CoolmannSa |
| LinkedIn | `cml5k1d710001s69hwekkhx1p` | **3,000** | kuhlmannsascha |
| Bluesky | `cml5mre6w0009o6l6svc718ej` | **300** | coolmanns.bsky.social |

## 平台内容指南

### X/Twitter（280 个字符）
- 内容简短、精炼
- 最多使用 1-2 个标签
- 链接算作 23 个字符（使用 t.co 短链接）
- 长内容可使用多条推文（线程形式）

### LinkedIn（3,000 个字符）
- 保持专业语气
- 可以写得更长
- 标签放在内容末尾（建议使用 3-5 个）
- 预览显示前 140 个字符，请确保这些字符包含关键信息！

### Bluesky（300 个字符）
- 与 X 类似，但允许稍长的内容
- 不支持官方标签（请谨慎使用）
- 主要面向技术/开发者群体

## 认证

```bash
# Login and save cookie (required before any API call)
curl -s -c /tmp/postiz-cookies.txt \
  'https://postiz.home.mykuhlmann.com/api/auth/login' \
  -H 'Content-Type: application/json' \
  -d '{"email":"sascha@mykuhlmann.com","password":"Postiz2026!","provider":"LOCAL"}'
```

Cookie 会定期过期。如果遇到 401 错误，请重新登录。

## 查找下一个可用时间槽

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://postiz.home.mykuhlmann.com/api/posts/find-slot/INTEGRATION_ID'
```

返回指定渠道的下一个可用时间槽，便于自动调度以避免冲突。

## 从 URL 上传媒体文件

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://postiz.home.mykuhlmann.com/api/media/upload-from-url' \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com/image.png"}'
```

## 创建帖子

### 单平台发布

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://postiz.home.mykuhlmann.com/api/posts' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "schedule",
    "date": "2026-02-05T15:00:00Z",
    "posts": [{
      "integration": {"id": "cml5lbs3h0001o6l6gagj9gcq"},
      "value": [{"content": "Your tweet here (max 280 chars)", "image": []}],
      "settings": {"__type": "x"}
    }]
  }'
```

### 多平台发布（内容适配）

```bash
curl -s -b /tmp/postiz-cookies.txt \
  'https://postiz.home.mykuhlmann.com/api/posts' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "schedule",
    "date": "2026-02-05T15:00:00Z",
    "posts": [
      {
        "integration": {"id": "cml5lbs3h0001o6l6gagj9gcq"},
        "value": [{"content": "Short X version (280 chars max)", "image": []}],
        "settings": {"__type": "x"}
      },
      {
        "integration": {"id": "cml5k1d710001s69hwekkhx1p"},
        "value": [{"content": "Longer LinkedIn version with more context and professional tone. Can be up to 3000 characters.", "image": []}],
        "settings": {"__type": "linkedin"}
      },
      {
        "integration": {"id": "cml5mre6w0009o6l6svc718ej"},
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
  'https://postiz.home.mykuhlmann.com/api/posts?startDate=2026-02-01T00:00:00Z&endDate=2026-02-08T00:00:00Z' \
  | jq '.posts[] | {id, state, publishDate, platform: .integration.providerIdentifier, content: .content[0:60]}'
```

### 发布前检查重复内容

```bash
# Get recent posts and check content similarity
curl -s -b /tmp/postiz-cookies.txt \
  'https://postiz.home.mykuhlmann.com/api/posts?startDate=2026-02-01T00:00:00Z&endDate=2026-02-08T00:00:00Z' \
  | jq -r '.posts[] | "\(.integration.providerIdentifier): \(.content[0:80])"'
```

## 帖子状态

| 状态 | 描述 |
|-------|-------------|
| `QUEUE` | 已调度，等待发布 |
| `PUBLISHED` | 发布成功 |
| `ERROR` | 发布失败 |
| `DRAFT` | 保存但未调度 |

## 媒体上传

### 上传图片

```bash
# Upload returns {id, path}
curl -s -b /tmp/postiz-cookies.txt \
  'https://postiz.home.mykuhlmann.com/api/media/upload-simple' \
  -F 'file=@/path/to/image.png'
```

### 在帖子中使用媒体文件

```json
"value": [{
  "content": "Post with image",
  "image": [{"id": "MEDIA_ID", "path": "/uploads/..."}]
}]
```

## Twitter/X 的多条推文

对于较长的内容，可以在 X 上创建多条推文：

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
  'https://postiz.home.mykuhlmann.com/api/posts/POST_ID'
```

### 更新调度计划

```bash
curl -s -b /tmp/postiz-cookies.txt -X PUT \
  'https://postiz.home.mykuhlmann.com/api/posts/POST_ID/date' \
  -H 'Content-Type: application/json' \
  -d '{"date": "2026-02-06T10:00:00Z"}'
```

## 最佳实践

### 避免重复
1. 在创建新帖子前务必查询现有帖子
2. 在内容中使用唯一的标识符（如日期、具体引用）
3. 检查帖子的 `QUEUE` 和 `PUBLISHED` 状态

### 调度建议
- 每个平台之间的发布间隔至少为 2-4 小时
- 最佳发布时间：上午 9 点、中午 12 点、下午 5 点（根据目标受众时区）
- 避免同时向所有平台发布相同内容

### 内容适配
- 不要简单截断内容！请针对每个平台重新撰写：
- **X**：包含吸引人的开头、关键观点和行动号召（CTA）
- **LinkedIn**：提供背景信息、价值主张和互动问题
- **Bluesky**：采用轻松、适合技术读者的表达方式

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

## Web 界面

- 控制台：https://postiz.home.mykuhlmann.com
  - 可视化日历视图
  - 支持拖放式调度
  - 提供分析和互动统计数据

## 故障排除

### 401 未授权错误
- 重新运行登录请求以刷新 Cookie。

### 帖子无法发布
1. 确认帖子状态为 `QUEUE` 而非 `DRAFT`
2. 确认发布日期在未来
3. 检查 UI 中的集成是否仍然正常连接

### 帖子重复
- 在创建新帖子前务必检查现有内容。API 不会自动删除重复帖子。