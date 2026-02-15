---
name: postiz
description: Postiz 是一个用于安排社交媒体和聊天帖子发布时间的工具，支持发布到 28 个以上的平台，包括：X（原 Twitter）、LinkedIn、LinkedIn Page、Reddit、Instagram、Facebook Page、Threads、YouTube、Google My Business、TikTok、Pinterest、Dribbble、Discord、Slack、Kick、Twitch、Mastodon、Bluesky、Lemmy、Farcaster、Telegram、Nostr、VK、Medium、Dev.to、Hashnode 和 WordPress。
homepage: https://docs.postiz.com/public-api/introduction
metadata: {"clawdbot":{"emoji":"🌎","requires":{"bins":[],"env":["POSTIZ_API_URL","POSTIZ_API_KEY"]}}}
---

| 属性 | 值 |
|----------|-------|
| **名称** | Postiz |
| **描述** | 一个用于在28个以上平台上自动发布内容的社交媒体自动化命令行工具（CLI） |
| **支持的工具** | Bash (Postiz:*) |

---

## 核心工作流程

使用Postiz CLI的基本步骤如下：

1. **发现** - 列出可用的集成工具并获取它们的配置信息 |
2. **获取数据** - 使用集成工具来检索动态数据（如徽章、播放列表、公司信息等） |
3. **准备** - 如有需要，上传媒体文件 |
4. **发布** - 创建包含内容、媒体以及平台特定设置的帖子 |

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
```

---

## 常用命令

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

### 上传媒体

**⚠️ 重要提示：** 在使用媒体文件之前，务必先将其上传到Postiz。许多平台（如TikTok、Instagram、YouTube）要求使用经过验证的URL，否则会拒绝外部链接。**

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

- **Reddit** - 获取子版块的徽章：  
  ```bash
  postiz searchSubreddits --subreddit "example-subreddit" getFlairs
  ```
- **YouTube** - 获取播放列表：  
  ```bash
  postiz getPlaylists
  ```
- **LinkedIn** - 以公司身份发布内容：  
  ```bash
  postiz getCompanies --organization "example-company"
  ```

### 模式2：发布前上传媒体文件

在发布帖子之前，先上传所需的媒体文件。

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

### 模式3：在Twitter上创建多条评论

可以在一条帖子中创建多条评论。

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

### 模式4：多平台发布活动

同时在一个或多个平台上发布内容。

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

### 模式5：发布前验证配置信息

确保所有配置信息都是正确的。

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

### 模式6：批量调度

批量安排多个帖子的发布时间。

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

在遇到错误时，系统会自动重试相应的操作。

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

许多集成工具需要动态数据（如ID、标签、播放列表等），这些数据无法硬编码。Postiz通过以下步骤实现这些数据的获取与使用：

1. **检查可用工具**：`integrations:settings` 返回一个包含所有可用工具的数组。
2. **查看工具的详细信息**：每个工具都有 `methodName`、`description` 和 `dataSchema`。
3. **触发工具**：使用 `integrations:trigger` 函数并传入必要的参数。
4. **使用工具返回的数据**：工具会将处理后的数据返回，以便在帖子中设置相关内容。

**按平台划分的工具示例：**
- **Reddit**：`getFlairs`、`searchSubreddits`、`getSubreddits`
- **YouTube**：`getPlaylists`、`getCategories`、`getChannels`
- **LinkedIn**：`getCompanies`、`getOrganizations`
- **Twitter/X**：`getListsowned`、`getCommunities`
- **Pinterest**：`getBoards`、`getBoardSections`

### 提供商配置结构

平台特定的配置信息使用 `__type` 字段进行区分：

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

可以直接传递配置参数：

```bash
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" --settings '{"subreddit":[...]}' -i "reddit-id"
# Backend automatically adds "__type" based on integration ID
```

### 评论与多条评论

帖子可以包含评论（在Twitter/X上表现为多条评论，在其他平台上表现为回复）。每条评论都可以附带媒体文件。

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

### 日期处理

所有日期格式均遵循ISO 8601标准：
- **安排帖子发布时间**：`-s "2024-12-31T12:00:00Z"`
- **列出帖子**：`--startDate "2024-01-01T00:00:00Z" --endDate "2024-12-31T23:59:59Z"`
- **默认值**：`posts:list` 会自动选择30天前的日期到30天后的日期范围。

### 媒体上传响应

上传媒体文件后，系统会返回包含文件路径和元数据的JSON格式数据：

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

### JSON模式与CLI参数

- **CLI参数**：适用于简单帖子的快速操作。
- **JSON模式**：适用于涉及多个平台和复杂配置的复杂帖子。

**JSON模式支持的功能：**
- 多个平台及每个平台不同的内容设置
- 复杂的供应商特定配置
- 安排好的发布时间
- 包含多条评论的帖子
- 设置评论之间的延迟时间

---

## 平台特定示例

- **Reddit**  
  ```bash
  postiz post --title "Example Post" --media "path/to/image.jpg" --subreddit "example-subreddit"
  ```
- **YouTube**  
  ```bash
  postiz post --video "path/to/video.mp4" --channel "example-channel" --playlist "example-playlist"
  ```
- **TikTok**  
  ```bash
  postiz post --video "path/to/video.mp4" --tag "example-tag"
  ```
- **X（Twitter）**  
  ```bash
  postiz post --title "Example Post" --media "path/to/image.jpg" --thread "example-thread"
  ```
- **LinkedIn**  
  ```bash
  postiz post --title "Example Post" --organization "example-company"
  ```

---

## 支持资源

- **详细文档**：
  - [HOW_TO_RUN.md](./HOW_TO_RUN.md)：安装与配置指南
  - [COMMAND_LINE_GUIDE.md](./COMMAND_LINE_GUIDE.md)：完整的命令语法参考
  - [PROVIDER_SETTINGS.md](./PROVIDER_SETTINGS.md)：所有28个以上平台的配置信息
  - [INTEGRATION_TOOLS_WORKFLOW.md](./INTEGRATION_TOOLS_WORKFLOW.md)：集成工具使用指南
  - [INTEGRATION_SETTINGS_DISCOVERY.md](./INTEGRATION_SETTINGS_DISCOVERY.md)：配置信息发现流程
  - [SUPPORTED_FILE_TYPES.md](./SUPPORTED_FILE_TYPES.md)：支持的媒体格式列表
  - [PROJECT_structure.md](./PROJECT_structure.md)：代码架构
  - [PUBLISHING.md](./PUBLISHING.md)：npm发布指南

- **即用示例**：
  - [examples/EXAMPLES.md](./examples/EXAMPLES.md)：完整的使用示例
  - [examples/basic-usage.sh](./examples/basic-usage.sh)：Shell脚本使用示例
  - [examples/ai-agent-example.js](./examples/ai-agent-example.js)：Node.js代理示例
  - [examples/post-with-comments.json](./examples/post-with-comments.json)：包含评论的帖子示例
  - [examples/multi-platform-with-settings.json](./examples/multi-platform-with-settings.json)：多平台发布示例
  - [examples/youtube-video.json](./examples/youtube-video.json)：包含标签的YouTube帖子示例
  - [examples/reddit-post.json](./examples/reddit-post.json)：包含子版块的Reddit帖子示例
  - [examples/tiktok-video.json](./examples/tiktok-video.json)：包含隐私设置的TikTok帖子示例

---

## 常见问题与注意事项

1. **API密钥未设置**：在使用CLI之前，务必执行 `export POSTIZ_API_KEY=value`。
2. **集成ID无效**：运行 `integrations:list` 命令以获取当前的集成ID。
3. **配置信息不匹配**：检查 `integrations:settings` 中是否包含所有必需的字段。
4. **必须先上传媒体文件**：⚠️ **重要提示**：TikTok、Instagram、YouTube等平台仅接受经过验证的URL。请先使用 `postiz upload` 命令上传媒体文件，然后在帖子中使用返回的URL。外部链接将被拒绝。
5. **Shell中的JSON编码**：使用单引号来传递JSON数据：`--settings '{...}'`。
6. **日期格式**：必须使用ISO 8601格式（例如 `2024-12-31T12:00:00Z`）。
7. **工具未找到**：请在 `integrations:settings` 的输出中确认所需的工具是否可用。
8. **字符限制**：不同平台有不同的字符长度限制，请参考配置文件中的 `maxLength` 设置。
9. **必需的配置项**：某些平台有特定的配置要求（例如Reddit需要标题，YouTube需要标题字段）。
10. **媒体文件格式**：CLI会根据文件扩展名自动检测媒体格式，请确保文件格式正确。

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

# Help
postiz --help                                     # Show help
postiz posts:create --help                        # Command help
```