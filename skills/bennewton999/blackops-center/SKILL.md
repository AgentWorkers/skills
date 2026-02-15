---
name: blackops-center
description: 通过 Clawdbot 控制您的 BlackOps Center 网站——通过 API 创建、发布和管理博客文章。
homepage: https://github.com/BlackOpsCenter/clawdbot-skill
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["curl","jq"]}}}
---

# BlackOps Center 技能

您可以通过 Clawdbot 来管理 BlackOps Center 的各个站点，包括创建、发布和管理博客文章。

## 设置

1. **在 BlackOps Center 中生成 API 令牌**：
   - 进入“设置” → “浏览器扩展程序”
   - 复制您的个人访问令牌（Personal Access Token）。

2. **配置该技能**：
   ```bash
   cd ~/.clawdbot/skills/blackops-center
   cp config.example.yaml config.yaml
   # Edit config.yaml and paste your token
   ```

## 配置文件（config.yaml）

创建 `config.yaml` 文件：

```yaml
api_token: "your-token-here"
base_url: "https://blackopscenter.com"  # or your custom domain
```

## 可用命令

所有命令均使用 `blackops-center` 命令行工具（CLI）进行执行。

### 列出站点

显示您有权访问的所有站点：

```bash
blackops-center list-sites
```

返回包含站点信息以及当前令牌所关联的活跃站点的 JSON 数据。

### 列出文章

列出您所在站点的所有文章：

```bash
# List all posts
blackops-center list-posts

# List only published posts
blackops-center list-posts --status published

# List only drafts
blackops-center list-posts --status draft

# Limit results
blackops-center list-posts --limit 10
```

### 获取文章详情

获取特定文章的详细信息：

```bash
blackops-center get-post <post-id>
```

### 创建文章

创建一篇新的文章草稿：

```bash
blackops-center create-post \
  --title "My Post Title" \
  --content "Post content in markdown" \
  --excerpt "Optional excerpt" \
  --tags "tag1,tag2,tag3"
```

所有新创建的文章默认都为草稿状态。

### 更新文章

更新现有的文章：

```bash
# Update title
blackops-center update-post <post-id> --title "New Title"

# Update content
blackops-center update-post <post-id> --content "New content"

# Publish a draft
blackops-center update-post <post-id> --status published

# Unpublish (back to draft)
blackops-center update-post <post-id> --status draft
```

您可以通过组合多个参数来同时更新多个字段。

### 删除文章

删除文章：

```bash
blackops-center delete-post <post-id>
```

## 在 Clawdbot 中使用该技能

当您通过 Clawdbot 调用此技能时，可以使用自然语言进行操作：

**用户:** “创建一篇关于 AI 代理的博客文章，标题为‘自动化的未来’”

**助手将执行以下操作：**
1. 从您的消息中提取标题和内容
2. 运行 `blackops-center create-post --title "..." --content "..."`
3. 返回文章的 ID 和预览链接

**用户:** “发布文章 abc123”

**助手将执行以下操作：**
1. 运行 `blackops-center update-post abc123 --status published`
2. 确认文章已发布，并提供文章的在线链接

**用户:** “显示我最近的草稿文章”

**助手将执行以下操作：**
1. 运行 `blackops-center list-posts --status draft --limit 10`
2. 以易读的方式展示结果

## API 详情

该技能使用 BlackOps Center 扩展程序的 API (`/api/ext/*`）：

- `GET /api/ext/sites` - 列出所有站点
- `GET /api/ext/posts` - 列出所有文章
- `POST /api/ext/posts` - 创建新文章
- `GET /api/ext/posts/:id` - 获取指定文章的详细信息
- `PUT /api/ext/posts/:id` - 更新指定文章
- `DELETE /api/ext/posts/:id` - 删除指定文章

所有请求都需要包含 `Authorization: Bearer <token>` 头部字段。

## 错误处理

- **401 Unauthorized**：令牌无效或已被撤销。请在 BlackOps Center 中生成新的令牌。
- **404 Site not found**：与您的令牌关联的站点不存在。
- **404 Post not found**：文章 ID 不存在或不属于当前站点。
- **400 Bad Request**：缺少必需的参数（例如创建文章时需要提供标题和内容）。

## 示例

### 创建并发布文章的流程

```bash
# Create draft
POST_ID=$(blackops-center create-post \
  --title "My Post" \
  --content "# My Post\n\nGreat content here." | jq -r '.post.id')

# Review, edit if needed...

# Publish when ready
blackops-center update-post "$POST_ID" --status published
```

### 批量操作

```bash
# Get all draft posts
DRAFTS=$(blackops-center list-posts --status draft)

# Publish all drafts (careful!)
echo "$DRAFTS" | jq -r '.posts[].id' | while read id; do
  blackops-center update-post "$id" --status published
done
```

## 故障排除

- 如果出现 “Unauthorized” 错误：
  - 检查 `config.yaml` 文件中的令牌是否正确。
  - 确认令牌在 BlackOps Center 中未被撤销。
  - 如有需要，生成新的令牌。

- 如果出现 “Site not found” 错误：
  - 每个令牌仅对应一个特定的站点域名。
  - 如果需要管理多个站点，请为每个站点生成单独的令牌。

- 如果某个命令无法执行，请检查 `bin/` 目录是否可执行：`chmod +x ~/.clawdbot/skills/blackops-center/bin/*`
  - 请确保该技能已通过 ClawdHub 安装，或将其链接到 `~/.clawdbot/skills/` 目录下。

## 开发

您可以使用 `curl` 直接测试这些 API：

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://blackopscenter.com/api/ext/posts
```

## 支持信息

- BlackOps Center：https://blackopscenter.com
- 问题反馈：https://github.com/clawdbot/skills （如果技能已发布）
- 文档：本文件