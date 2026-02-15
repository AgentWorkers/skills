# YouTube Studio 技能

Clawdbot 提供全面的 YouTube 频道管理功能，包括监控分析数据、上传视频、管理评论以及生成内容创意。

## 概述

**youtube-studio** 提供以下全面的 YouTube 频道管理功能：
- 实时频道统计和分析数据
- 带元数据的视频上传及上传计划设置
- 评论监控及基于 AI 的回复建议
- 根据趋势和受众群体生成内容创意
- 速率限制与错误恢复机制
- 支持 OAuth 2.0 认证

## 设置

### 1. YouTube Data API v3 凭据

#### 获取 API 密钥和 OAuth 凭据

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建一个新的项目（例如：“Clawdbot YouTube Studio”）
3. 启用 **YouTube Data API v3**：
   - 搜索 “YouTube Data API v3”
   - 点击 “启用”
4. 创建 OAuth 2.0 凭据：
   - 转到 “凭据” 部分
   - 点击 “创建凭据” → “OAuth 客户端 ID”
   - 选择 “桌面应用程序”
   - 下载 JSON 文件（保存为 `credentials.json`）
5. 创建 API 密钥（用于公共请求）：
   - 点击 “创建凭据” → “API 密钥”
   - 复制密钥

#### 文件结构
```
~/.clawd-youtube/
├── credentials.json       # OAuth credentials (from step 4)
├── tokens.json           # Generated after first OAuth flow
└── config.env            # API keys and settings
```

### 2. 环境配置

将 `.env.example` 文件复制到 `~/.clawd-youtube/config.env`：

```bash
# YouTube API
YOUTUBE_API_KEY=your_api_key_here
YOUTUBE_CLIENT_ID=your_client_id.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REDIRECT_URI=http://localhost:8888/oauth2callback

# Channel Settings
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxx
YOUTUBE_CHANNEL_NAME=YourChannelName

# AI Model (for suggestions & replies)
AI_MODEL=openrouter/anthropic/claude-haiku-4.5
AI_API_KEY=your_api_key

# Rate Limiting
API_QUOTA_PER_DAY=1000000
BATCH_SIZE=50

# Logging
LOG_LEVEL=info
LOG_DIR=./logs
```

### 3. OAuth 2.0 流程

该技能在首次运行时会自动处理 OAuth 认证流程：

```bash
youtube-studio auth
# Opens browser to Google login
# Exchanges auth code for refresh token
# Saves tokens to tokens.json
```

**后续运行** 会使用已保存的刷新令牌，无需重新认证。

## 命令

### 检查频道统计数据
```bash
youtube-studio stats
youtube-studio stats --days 7        # Last 7 days
youtube-studio stats --json          # JSON output
```

**输出内容：**
- 总播放量、订阅者数量、观看时长
- 最新视频的播放表现（前 5 个）
- 增长趋势
- 互动指标（平均播放量、点赞数、每视频的评论数）

### 上传视频
```bash
youtube-studio upload \
  --file video.mp4 \
  --title "My Devotional Series #5" \
  --description "Join me for another..." \
  --tags "devotional,faith,inspiration" \
  --privacy public \
  --schedule "2024-01-15T10:00:00Z"
```

**选项：**
- `--file`（必选）：视频文件路径（mp4、mov、avi、mkv 格式）
- `--title`（必选）：视频标题
- `--description`：完整描述（支持 Markdown 格式）
- `--tags`：用逗号分隔的标签（最多 500 个字符）
- `--privacy`：公开、未公开、私有（默认：未公开）
- `--thumbnail`：自定义缩略图路径
- `--playlist`：按名称添加到现有播放列表
- `--schedule`：指定上传时间的 ISO 8601 格式字符串
- `--category`：视频类别（音乐、人物等）

### 列出最新评论
```bash
youtube-studio comments
youtube-studio comments --video-id xxxxx    # Specific video
youtube-studio comments --unread            # Unread only
youtube-studio comments --limit 50          # Limit results
youtube-studio comments --json              # JSON output
```

### 回复评论
```bash
youtube-studio reply \
  --comment-id Qmxxxxxxxxxxxxxxxx \
  --text "Thanks for watching!" \
  --suggest                    # Show AI suggestions first
```

**标志参数：**
- `--suggest`：在回复前生成 3 个回复建议
- `--template`：使用预设的回复模板（感谢、教育性、推广性）
- `--dry-run`：预览回复内容而不实际发送

### 生成视频创意
```bash
youtube-studio ideas
youtube-studio ideas --niche devotional
youtube-studio ideas --trending          # Based on YouTube trends
youtube-studio ideas --json              # JSON output
youtube-studio ideas --count 10          # Number of ideas
```

**输出内容：**
- 视频标题建议
- 描述模板
- 目标受众分析
- SEO 关键词
- 预计搜索量
- 缩略图创意

## 速率限制

YouTube API 的使用配额如下：
- **每日配额：** 1,000,000 个请求单位（默认值）
- **各方法的成本：**
  - `channels.list`：1 个请求单位
  - `videos.list`：1 个请求单位
  - `videos.insert`：1,600 个请求单位（用于视频上传）
  - `commentThreads.list`：1 个请求单位
  - `comments.insert`：1 个请求单位

**该技能具备以下功能：**
- 自动跟踪使用配额
- 批量处理请求
- 在遇到 403 错误时采用指数级重试策略
- 每日自动重置配额使用情况
- 当配额使用量超过 80% 时发出警报

```bash
youtube-studio quota-status    # Check remaining quota
```

## 错误处理

| 错误类型 | 处理方式 |
|---------|-----------|
| `401 Unauthorized` | 自动刷新 OAuth 令牌 |
| `403 Quota Exceeded` | 等待次日再尝试，并显示警报 |
| `429 Rate Limited` | 采用指数级重试策略（1 秒、2 秒、4 秒……） |
| `500 Server Error` | 最多尝试 3 次 |
| 网络超时 | 使用断路器机制进行优雅重试 |
| 上传中断 | 从上次中断的位置继续上传 |

## 文件结构
```
youtube-studio/
├── SKILL.md                           # This file
├── README.md                          # User guide
├── scripts/
│   ├── youtube-studio.js              # Main entry point & CLI
│   ├── channel-analytics.js           # Stats & analytics
│   ├── video-uploader.js              # Video upload logic
│   ├── comment-manager.js             # Comment operations
│   ├── content-ideas.js               # Idea generation
│   ├── auth-handler.js                # OAuth flow
│   ├── api-client.js                  # Quota-aware API wrapper
│   └── utils.js                       # Helpers
├── config/
│   ├── templates.json                 # Description templates, tags
│   └── niche-prompts.json             # Prompt templates for ideas
├── .env.example                       # Environment template
├── package.json                       # Dependencies
└── logs/                              # Runtime logs
```

## 模板

### 视频描述模板
```json
{
  "devoted_journey": {
    "title": "Daily Devotional - {topic}",
    "description": "🙏 {hook}\n\n{body}\n\n⏱️ Timestamps:\n{timestamps}\n\n📖 Scripture: {reference}\n\n💬 Reflect: {reflection_question}",
    "tags": ["devotional", "faith", "scripture", "spiritual"]
  }
}
```

### 评论回复模板
- `grateful`：感谢订阅者的支持
- `educational`：深入解释相关概念
- `promotional`：链接到相关视频
- `engagement`：提出后续问题

## 依赖项
```json
{
  "googleapis": "^120.0.0",
  "google-auth-library": "^9.0.0",
  "axios": "^1.6.0",
  "express": "^4.18.0"
}
```

## 故障排除

### 出现 “Invalid grant” 错误
- 删除 `tokens.json` 文件
- 重新运行 `youtube-studio auth` 命令
- 确保 `credentials.json` 文件有效

### 配额超出
- 查看 `youtube-studio quota-status` 命令的输出
- 等待午夜（UTC 时间）以重置配额
- 考虑在 Google Cloud Console 中增加 API 配额

### 上传失败
- 确认文件存在且可读取
- 验证文件格式是否被 YouTube 支持
- 检查视频内容是否违反 YouTube 的规定
- 先使用 `--dry-run` 命令测试元数据是否正确

### 评论未显示
- 确保频道已使用所有者账户进行认证
- 检查评论审核设置
- 确认 `YOUTUBE_CHANNEL_ID` 与你的频道匹配

## API 参考

### 核心方法

#### `authenticateOAuth()`
- 启动 OAuth 2.0 认证流程，并返回刷新令牌。

#### `getChannelStats(options = {})`
- `days`：查看的日期范围（默认：30 天）
- 返回值：`{ views, subscribers, watchHours, videos, topVideos[] }`

#### `uploadVideo(metadata, filePath, options = {})`
- `metadata`：视频的标题、描述、标签、隐私设置
- `filePath`：视频文件路径
- 返回值：`{ videoId, status, scheduledTime }`

#### `listComments(videoId = null, options = {})`
- `videoId`：指定视频 ID；如未指定则查看所有视频
- `unread`：布尔值，仅显示未读评论
- 返回值：`{ comments[], total, pageToken }`

#### `replyToComment(commentId, text, options = {})`
- `template`：使用预设的回复模板
- `suggestFirst`：获取 AI 提供的回复建议
- 返回值：`{ replyId, text }`

#### `generateVideoIdeas(options = {})`
- `niche`：频道所属的类别/领域
- `trending`：包含热门话题
- 返回值：`{ ideas[], keywords[], thumbnail_prompts[] }`

## 示例

### 完整的每日工作流程
```bash
# Check stats
youtube-studio stats --days 1

# Review comments with suggestions
youtube-studio comments --limit 20 --suggest

# Generate new video ideas
youtube-studio ideas --trending --count 5

# Check quota before scheduling uploads
youtube-studio quota-status
```

### 自动上传（脚本实现）
```bash
#!/bin/bash
youtube-studio upload \
  --file ~/Videos/devotional.mp4 \
  --title "Daily Devotional - $(date +%Y-%m-%d)" \
  --description "$(cat description.txt)" \
  --schedule "$(date -d 'tomorrow 10:00' -Iseconds)" \
  --tags "devotional,daily,faith"
```

## 限制条件

- YouTube API 的每日配额为 1,000,000 个请求单位（足以支持每天大约 600 次上传）
- 视频文件大小不能超过 256GB
- 视频标题长度限制为 100 个字符
- 视频描述长度限制为 5,000 个字符
- 每条评论的回复长度限制为 10,000 个字符
- 目前不支持实时流媒体管理功能

## 未来改进计划

- [ ] 实时流媒体监控和评论管理
- [ ] 自动化播放列表管理
- [ ] 使用 Whisper 工具生成字幕
- [ ] 优化缩略图质量
- [ ] 提供分析仪表板
- [ ] 支持多频道管理
- [ ] 提供内容调度功能

## 许可证

MIT 许可证——可在 Clawdbot 生态系统中自由使用

## 技术支持

如有问题，请查看：
1. 在 `~/.clawd-youtube/logs/` 文件中查看调试日志
2. 通过 `youtube-studio auth` 命令检查凭据的有效性
3. 使用 `youtube-studio quota-status` 命令查看 API 配额使用情况
4. 检查网络连接是否正常（可以尝试 Ping Google API 服务器）