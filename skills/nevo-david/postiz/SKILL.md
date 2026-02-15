---
name: postiz
description: Postiz 是一款用于安排社交媒体和聊天平台发布内容的工具，支持发布到 28 个以上的平台，包括：X（原 Twitter）、LinkedIn、LinkedIn Page、Reddit、Instagram、Facebook Page、Threads、YouTube、Google My Business、TikTok、Pinterest、Dribbble、Discord、Slack、Kick、Twitch、Mastodon、Bluesky、Lemmy、Farcaster、Telegram、Nostr、VK、Medium、Dev.to、Hashnode 和 WordPress。
homepage: https://docs.postiz.com/public-api/introduction
metadata: {"clawdbot":{"emoji":"🌎","requires":{"bins":[],"env":["POSTIZ_API_URL","POSTIZ_API_KEY"]}}}
---

| 属性 | 值 |
|----------|-------|
| **名称** | Postiz |
| **描述** | 一个用于在28个以上平台上自动发布内容的社交媒体管理命令行工具（CLI） |
| **支持的工具** | Bash (Postiz:*) |

---

## 核心工作流程

使用Postiz CLI的基本步骤如下：

1. **发现** - 列出可用的集成工具并获取它们的配置信息 |
2. **获取数据** - 使用集成工具获取动态数据（如徽章、播放列表、公司信息等） |
3. **准备** - 如有需要，上传媒体文件 |
4. **发布** - 创建包含内容、媒体以及平台特定设置的帖子 |
5. **分析** - 通过平台及帖子级别的分析来监控发布效果 |

```bash
# 1. Discover
postiz integrations:list
postiz integrations:settings <integration-id>

# 2. Fetch (if needed)
postiz integrations:trigger <integration-id> <method> -d '{"key":"value"}'

# 3. Prepare
postiz upload image.jpg

# 4. Post
postiz posts:create -c "Content" -m "image.jpg" -i "<integration-id>"

# 5. Analyze
postiz analytics:platform <integration-id> -d 30
postiz analytics:post <post-id> -d 7
```

---

## 必需命令

### 设置

```bash
# Required environment variable
export POSTIZ_API_KEY=your_api_key_here

# Optional custom API URL
export POSTIZ_API_URL=https://custom-api-url.com
```

### 发现集成工具

```bash
# List all connected integrations
postiz integrations:list

# Get settings schema for specific integration
postiz integrations:settings <integration-id>

# Trigger integration tool to fetch dynamic data
postiz integrations:trigger <integration-id> <method-name>
postiz integrations:trigger <integration-id> <method-name> -d '{"param":"value"}'
```

### 创建帖子

```bash
# Simple post (date is REQUIRED)
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -i "integration-id"

# Draft post
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -t draft -i "integration-id"

# Post with media
postiz posts:create -c "Content" -m "img1.jpg,img2.jpg" -s "2024-12-31T12:00:00Z" -i "integration-id"

# Post with comments (each with own media)
postiz posts:create \
  -c "Main post" -m "main.jpg" \
  -c "First comment" -m "comment1.jpg" \
  -c "Second comment" -m "comment2.jpg,comment3.jpg" \
  -s "2024-12-31T12:00:00Z" \
  -i "integration-id"

# Multi-platform post
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -i "twitter-id,linkedin-id,facebook-id"

# Platform-specific settings
postiz posts:create \
  -c "Content" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"subreddit":[{"value":{"subreddit":"programming","title":"My Post","type":"text"}}]}' \
  -i "reddit-id"

# Complex post from JSON file
postiz posts:create --json post.json
```

### 管理帖子

```bash
# List posts (defaults to last 30 days to next 30 days)
postiz posts:list

# List posts in date range
postiz posts:list --startDate "2024-01-01T00:00:00Z" --endDate "2024-12-31T23:59:59Z"

# Delete post
postiz posts:delete <post-id>
```

### 分析

```bash
# Get platform analytics (default: last 7 days)
postiz analytics:platform <integration-id>

# Get platform analytics for last 30 days
postiz analytics:platform <integration-id> -d 30

# Get post analytics (default: last 7 days)
postiz analytics:post <post-id>

# Get post analytics for last 30 days
postiz analytics:post <post-id> -d 30
```

该命令会返回一系列指标（如粉丝数、浏览量、点赞数、评论数），并附带每日数据点及变化百分比。

### 上传媒体文件

**⚠️ 重要提示：** 在使用媒体文件发布帖子之前，务必先将其上传到Postiz。许多平台（如TikTok、Instagram、YouTube）**要求使用经过验证的URL**，否则会拒绝外部链接。

```bash
# Upload file and get URL
postiz upload image.jpg

# Supports: images (PNG, JPG, GIF, WEBP, SVG), videos (MP4, MOV, AVI, MKV, WEBM),
# audio (MP3, WAV, OGG, AAC), documents (PDF, DOC, DOCX)

# Workflow: Upload → Extract URL → Use in post
VIDEO=$(postiz upload video.mp4)
VIDEO_PATH=$(echo "$VIDEO" | jq -r '.path')
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -m "$VIDEO_PATH" -i "tiktok-id"
```

---

## 常见使用模式

### 模式1：发现并使用集成工具

**Reddit - 获取子版块的徽章：**
```bash
# Get Reddit integration ID
REDDIT_ID=$(postiz integrations:list | jq -r '.[] | select(.identifier=="reddit") | .id')

# Fetch available flairs
FLAIRS=$(postiz integrations:trigger "$REDDIT_ID" getFlairs -d '{"subreddit":"programming"}')
FLAIR_ID=$(echo "$FLAIRS" | jq -r '.output[0].id')

# Use in post
postiz posts:create \
  -c "My post content" \
  -s "2024-12-31T12:00:00Z" \
  --settings "{\"subreddit\":[{\"value\":{\"subreddit\":\"programming\",\"title\":\"Post Title\",\"type\":\"text\",\"is_flair_required\":true,\"flair\":{\"id\":\"$FLAIR_ID\",\"name\":\"Discussion\"}}}]}" \
  -i "$REDDIT_ID"
```

**YouTube - 获取播放列表：**
```bash
YOUTUBE_ID=$(postiz integrations:list | jq -r '.[] | select(.identifier=="youtube") | .id')
PLAYLISTS=$(postiz integrations:trigger "$YOUTUBE_ID" getPlaylists)
PLAYLIST_ID=$(echo "$PLAYLISTS" | jq -r '.output[0].id')

postiz posts:create \
  -c "Video description" \
  -s "2024-12-31T12:00:00Z" \
  --settings "{\"title\":\"My Video\",\"type\":\"public\",\"playlistId\":\"$PLAYLIST_ID\"}" \
  -m "video.mp4" \
  -i "$YOUTUBE_ID"
```

**LinkedIn - 以公司名义发布内容：**
```bash
LINKEDIN_ID=$(postiz integrations:list | jq -r '.[] | select(.identifier=="linkedin") | .id')
COMPANIES=$(postiz integrations:trigger "$LINKEDIN_ID" getCompanies)
COMPANY_ID=$(echo "$COMPANIES" | jq -r '.output[0].id')

postiz posts:create \
  -c "Company announcement" \
  -s "2024-12-31T12:00:00Z" \
  --settings "{\"companyId\":\"$COMPANY_ID\"}" \
  -i "$LINKEDIN_ID"
```

### 模式2：发布前上传媒体文件

```bash
# Upload multiple files
VIDEO_RESULT=$(postiz upload video.mp4)
VIDEO_PATH=$(echo "$VIDEO_RESULT" | jq -r '.path')

THUMB_RESULT=$(postiz upload thumbnail.jpg)
THUMB_PATH=$(echo "$THUMB_RESULT" | jq -r '.path')

# Use in post
postiz posts:create \
  -c "Check out my video!" \
  -s "2024-12-31T12:00:00Z" \
  -m "$VIDEO_PATH" \
  -i "tiktok-id"
```

### 模式3：在Twitter上创建多条帖子（线程形式）**

```bash
postiz posts:create \
  -c "🧵 Thread starter (1/4)" -m "intro.jpg" \
  -c "Point one (2/4)" -m "point1.jpg" \
  -c "Point two (3/4)" -m "point2.jpg" \
  -c "Conclusion (4/4)" -m "outro.jpg" \
  -s "2024-12-31T12:00:00Z" \
  -d 2000 \
  -i "twitter-id"
```

### 模式4：多平台发布活动**

```bash
# Create JSON file with platform-specific content
cat > campaign.json << 'EOF'
{
  "integrations": ["twitter-123", "linkedin-456", "facebook-789"],
  "posts": [
    {
      "provider": "twitter",
      "post": [
        {
          "content": "Short tweet version #tech",
          "image": ["twitter-image.jpg"]
        }
      ]
    },
    {
      "provider": "linkedin",
      "post": [
        {
          "content": "Professional LinkedIn version with more context...",
          "image": ["linkedin-image.jpg"]
        }
      ]
    }
  ]
}
EOF

postiz posts:create --json campaign.json
```

### 模式5：发布前验证设置

```javascript
const { execSync } = require('child_process');

function validateAndPost(content, integrationId, settings) {
  // Get integration settings
  const settingsResult = execSync(
    `postiz integrations:settings ${integrationId}`,
    { encoding: 'utf-8' }
  );
  const schema = JSON.parse(settingsResult);

  // Check character limit
  if (content.length > schema.output.maxLength) {
    console.warn(`Content exceeds ${schema.output.maxLength} chars, truncating...`);
    content = content.substring(0, schema.output.maxLength - 3) + '...';
  }

  // Create post
  const result = execSync(
    `postiz posts:create -c "${content}" -s "2024-12-31T12:00:00Z" --settings '${JSON.stringify(settings)}' -i "${integrationId}"`,
    { encoding: 'utf-8' }
  );

  return JSON.parse(result);
}
```

### 模式6：批量调度发布

```bash
#!/bin/bash

# Schedule posts for the week
DATES=(
  "2024-02-14T09:00:00Z"
  "2024-02-15T09:00:00Z"
  "2024-02-16T09:00:00Z"
)

CONTENT=(
  "Monday motivation 💪"
  "Tuesday tips 💡"
  "Wednesday wisdom 🧠"
)

for i in "${!DATES[@]}"; do
  postiz posts:create \
    -c "${CONTENT[$i]}" \
    -s "${DATES[$i]}" \
    -i "twitter-id" \
    -m "post-${i}.jpg"
  echo "Scheduled: ${CONTENT[$i]} for ${DATES[$i]}"
done
```

### 模式7：错误处理与重试

```javascript
const { execSync } = require('child_process');

async function postWithRetry(content, integrationId, date, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const result = execSync(
        `postiz posts:create -c "${content}" -s "${date}" -i "${integrationId}"`,
        { encoding: 'utf-8', stdio: 'pipe' }
      );
      console.log('✅ Post created successfully');
      return JSON.parse(result);
    } catch (error) {
      console.error(`❌ Attempt ${attempt} failed: ${error.message}`);

      if (attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
        console.log(`⏳ Retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw new Error(`Failed after ${maxRetries} attempts`);
      }
    }
  }
}
```

---

## 技术概念

### 集成工具的工作流程

许多集成工具需要动态数据（如ID、标签、播放列表等），这些数据无法硬编码。Postiz通过以下流程来实现这些功能的发现与使用：

1. **检查可用工具** - `integrations:settings` 会返回一个包含所有工具的数组 |
2. **查看工具详情** - 每个工具都包含 `methodName`、`description` 和 `dataSchema` |
3. **触发工具** - 使用 `integrations:trigger` 函数并传入所需参数 |
4. **使用工具返回的数据** - 这些数据将用于帖子的配置中 |

**按平台划分的工具示例：**
- **Reddit**：`getFlairs`、`searchSubreddits`、`getSubreddits`
- **YouTube**：`getPlaylists`、`getCategories`、`getChannels`
- **LinkedIn**：`getCompanies`、`getOrganizations`
- **Twitter/X**：`getListsowned`、`getCommunities`
- **Pinterest**：`getBoards`、`getBoardSections`

### 提供商设置结构

平台特定的设置使用 `__type` 字段进行区分：

```json
{
  "posts": [
    {
      "provider": "reddit",
      "post": [{ "content": "...", "image": [...] }],
      "settings": {
        "__type": "reddit",
        "subreddit": [{
          "value": {
            "subreddit": "programming",
            "title": "Post Title",
            "type": "text",
            "url": "",
            "is_flair_required": false
          }
        }]
      }
    }
  ]
}
```

**直接传递设置：**
```bash
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" --settings '{"subreddit":[...]}' -i "reddit-id"
# Backend automatically adds "__type" based on integration ID
```

### 评论与多条帖子的处理

帖子可以包含评论（在Twitter/X上表现为多条帖子，在其他平台上表现为回复）。每条评论都可以附带媒体文件：

```bash
# Using multiple -c and -m flags
postiz posts:create \
  -c "Main post" -m "image1.jpg,image2.jpg" \
  -c "Comment 1" -m "comment-img.jpg" \
  -c "Comment 2" -m "another.jpg,more.jpg" \
  -s "2024-12-31T12:00:00Z" \
  -d 5000 \  # Delay between comments in ms
  -i "integration-id"
```

**内部处理机制：**
```json
{
  "posts": [{
    "value": [
      { "content": "Main post", "image": ["image1.jpg", "image2.jpg"] },
      { "content": "Comment 1", "image": ["comment-img.jpg"], "delay": 5000 },
      { "content": "Comment 2", "image": ["another.jpg", "more.jpg"], "delay": 5000 }
    ]
  }]
}
```

### 日期处理

所有日期均采用ISO 8601格式：
- **安排发布时间**：`-s "2024-12-31T12:00:00Z"`
- **列出帖子**：`--startDate "2024-01-01T00:00:00Z" --endDate "2024-12-31T23:59:59Z"`
- **默认值**：`posts:list` 会自动使用过去30天到未来30天内的日期范围

### 媒体文件上传响应

上传完成后，系统会返回包含文件路径和元数据的JSON格式数据：

```json
{
  "path": "https://cdn.postiz.com/uploads/abc123.jpg",
  "size": 123456,
  "type": "image/jpeg"
}
```

**提取文件路径以用于帖子内容：**
```bash
RESULT=$(postiz upload image.jpg)
PATH=$(echo "$RESULT" | jq -r '.path')
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -m "$PATH" -i "integration-id"
```

### JSON模式与CLI命令行参数

**CLI命令行参数** - 适用于简单帖子的快速操作 |
**JSON模式** - 适用于涉及多个平台和复杂设置的场景：

**JSON模式支持的功能：**
- 多个平台及每个平台的不同内容设置 |
- 复杂的提供商特定设置 |
- 定时发布的帖子 |
- 包含大量评论的帖子 |
- 帖子之间的自定义延迟时间设置

---

## 平台特定示例

### Reddit
```bash
postiz posts:create \
  -c "Post content" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"subreddit":[{"value":{"subreddit":"programming","title":"My Title","type":"text","url":"","is_flair_required":false}}]}' \
  -i "reddit-id"
```

### YouTube
```bash
# Upload video first (required!)
VIDEO=$(postiz upload video.mp4)
VIDEO_URL=$(echo "$VIDEO" | jq -r '.path')

postiz posts:create \
  -c "Video description" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"title":"Video Title","type":"public","tags":[{"value":"tech","label":"Tech"}]}' \
  -m "$VIDEO_URL" \
  -i "youtube-id"
```

### TikTok
```bash
# Upload video first (TikTok only accepts verified URLs!)
VIDEO=$(postiz upload video.mp4)
VIDEO_URL=$(echo "$VIDEO" | jq -r '.path')

postiz posts:create \
  -c "Video caption #fyp" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"privacy":"PUBLIC_TO_EVERYONE","duet":true,"stitch":true}' \
  -m "$VIDEO_URL" \
  -i "tiktok-id"
```

### Twitter（X）
```bash
postiz posts:create \
  -c "Tweet content" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"who_can_reply_post":"everyone"}' \
  -i "twitter-id"
```

### LinkedIn
```bash
# Personal post
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -i "linkedin-id"

# Company post
postiz posts:create \
  -c "Content" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"companyId":"company-123"}' \
  -i "linkedin-id"
```

### Instagram
```bash
# Upload image first (Instagram requires verified URLs!)
IMAGE=$(postiz upload image.jpg)
IMAGE_URL=$(echo "$IMAGE" | jq -r '.path')

# Regular post
postiz posts:create \
  -c "Caption #hashtag" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"post_type":"post"}' \
  -m "$IMAGE_URL" \
  -i "instagram-id"

# Story
STORY=$(postiz upload story.jpg)
STORY_URL=$(echo "$STORY" | jq -r '.path')

postiz posts:create \
  -c "" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"post_type":"story"}' \
  -m "$STORY_URL" \
  -i "instagram-id"
```

---

## 支持资源

**详细文档：**
- [HOW_TO_RUN.md](./HOW_TO_RUN.md) - 安装与设置指南 |
- [COMMAND_LINE_GUIDE.md](./COMMAND_LINE_GUIDE.md) - 完整的命令行语法参考 |
- [PROVIDER_SETTINGS.md](./PROVIDER_SETTINGS.md) - 所有28个以上平台的设置规范 |
- [INTEGRATION_TOOLS_WORKFLOW.md](./INTEGRATION_TOOLS_WORKFLOW.md) - 集成工具使用流程指南 |
- [INTEGRATION_SETTINGS_DISCOVERY.md](./INTEGRATION_SETTINGS_DISCOVERY.md) - 设置发现流程说明 |
- [SUPPORTED_FILE_TYPES.md](./SUPPORTED_FILE_TYPES.md) - 支持的所有媒体格式 |
- [PROJECT_structure.md](./PROJECT_structure.md) - 代码架构 |
- [PUBLISHING.md](./PUBLISHING.md) - npm发布指南

**即用示例：**
- [examples/EXAMPLES.md](./examples/EXAMPLES.md) - 全面示例 |
- [examples/basic-usage.sh](./examples/basic-usage.sh) - 命令行脚本使用示例 |
- [examples/ai-agent-example.js](./examples/ai-agent-example.js) - Node.js代理示例 |
- [examples/post-with-comments.json](./examples/post-with-comments.json) - 包含评论的帖子示例 |
- [examples/multi-platform-with-settings.json](./examples/multi-platform-with-settings.json) - 多平台发布活动示例 |
- [examples/youtube-video.json](./examples/youtube-video.json) - 带标签的YouTube帖子示例 |
- [examples/reddit-post.json](./examples/reddit-post.json) - 带子版块的Reddit帖子示例 |
- [examples/tiktok-video.json](./examples/tiktok-video.json) - 带隐私设置的TikTok帖子示例 |

---

## 常见问题与注意事项

1. **API密钥未设置** - 使用CLI前务必执行 `export POSTIZ_API_KEY=value` |
2. **集成ID无效** - 运行 `integrations:list` 命令获取当前可用的集成ID |
3. **设置格式不匹配** - 查看 `integrations:settings` 以确保所有字段都正确 |
4. **必须先上传媒体文件** - ⚠️ **重要提示：** TikTok、Instagram、YouTube等平台仅接受经过验证的URL。请先使用 `postiz upload` 命令上传文件，然后在帖子中使用返回的URL；外部链接将被拒绝！ |
5. **在Shell环境中处理JSON数据时需注意转义** - 使用单引号来引用JSON字符串：`--settings '{...}'` |
6. **日期格式** - 必须使用ISO 8601格式（例如 `2024-12-31T12:00:00Z`） |
7. **工具未找到** - 请在 `integrations:settings` 的输出中确认工具是否可用 |
8. **字符长度限制** - 不同平台有不同的字符长度限制，请参考设置中的 `maxLength` 参数 |
9. **某些平台有特定要求** - 例如Reddit要求提供标题，YouTube要求提供标题信息 |
10. **媒体文件格式** - CLI会根据文件扩展名自动检测媒体类型，请确保文件格式正确 |

---

## 快速参考

```bash
# Environment
export POSTIZ_API_KEY=key

# Discovery
postiz integrations:list                           # Get integration IDs
postiz integrations:settings <id>                  # Get settings schema
postiz integrations:trigger <id> <method> -d '{}'  # Fetch dynamic data

# Posting (date is REQUIRED)
postiz posts:create -c "text" -s "2024-12-31T12:00:00Z" -i "id"                  # Simple
postiz posts:create -c "text" -s "2024-12-31T12:00:00Z" -t draft -i "id"        # Draft
postiz posts:create -c "text" -m "img.jpg" -s "2024-12-31T12:00:00Z" -i "id"    # With media
postiz posts:create -c "main" -c "comment" -s "2024-12-31T12:00:00Z" -i "id"    # With comment
postiz posts:create -c "text" -s "2024-12-31T12:00:00Z" --settings '{}' -i "id" # Platform-specific
postiz posts:create --json file.json                                             # Complex

# Management
postiz posts:list                                  # List posts
postiz posts:delete <id>                          # Delete post
postiz upload <file>                              # Upload media

# Analytics
postiz analytics:platform <id>                    # Platform analytics (7 days)
postiz analytics:platform <id> -d 30             # Platform analytics (30 days)
postiz analytics:post <id>                        # Post analytics (7 days)
postiz analytics:post <id> -d 30                 # Post analytics (30 days)

# Help
postiz --help                                     # Show help
postiz posts:create --help                        # Command help
```