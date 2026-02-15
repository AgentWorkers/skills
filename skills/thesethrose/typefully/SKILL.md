---
name: typefully
description: |
  X, LinkedIn, Mastodon, Threads, and Bluesky scheduling via Typefully API.

  Create drafts, schedule posts, and manage content across multiple social platforms.
metadata: 
  {"clawdbot":{"emoji":"🐦","requires":{"env":["TYPEFULLY_API_KEY"]}}}
---

# Typefully Skill  
通过 Typefully API，您可以安排并发布内容到 X（原帖平台）、LinkedIn、Mastodon、Threads 和 Bluesky 等平台。  

## 设置  
1. 在 [https://typefully.com](https://typefully.com) 注册一个 Typefully 账户。  
2. 在 Typefully 中连接您的社交媒体账户。  
3. 在 Typefully 设置中生成 API 密钥。  
4. 设置 `TYPEFULLY_API_KEY` 环境变量。  

```bash
export TYPEFULLY_API_KEY="your-typefully-api-key"
```  

## 环境变量  
| 变量 | 是否必需 | 说明 |  
|---------|---------|---------|  
| TYPEFULLY_API_KEY | 是 | 您的 Typefully API 密钥 |  

## 命令  

### 用户与账户  
```bash
typefully me                    # Get current user info
typefully social-sets           # List connected social accounts
typefully social-set <id>       # Get details for a specific account
```  

### 草稿  
```bash
typefully drafts                     # List all drafts for an account
typefully draft <id>                 # Get a specific draft
typefully create-draft "content"     # Create a new draft
typefully update-draft <id> "text"   # Update a draft
typefully delete-draft <id>          # Delete a draft
```  

### 草稿选项  
| 选项 | 说明 |  
|--------|---------|  
| --social-set-id <id> | 草稿所需的账户 ID |  
| --schedule <time> | ISO 8601 格式的日期时间 |  
| --now | 创建后立即发布 |  
| --next-free-slot | 选择最佳发布时间进行安排 |  
| --title <text> | 草稿的标题 |  
| --share | 生成公共分享链接 |  
| --thread | 将内容作为多行帖子发布 |  
| --reply-to <url> | 回复到指定的帖子 URL |  
| --community <id> | 在指定社区中发布 |  

### 过滤草稿  
```bash
typefully drafts                  # Default 10 drafts sorted by updated
typefully drafts --status draft   # Only draft status
typefully drafts --status scheduled  # Only scheduled
typefully drafts --status published  # Only published
typefully drafts --limit 25       # More results per page
typefully drafts --offset 10      # Skip first 10 results
typefully drafts --order-by created_at  # Sort by date
```  

### 标签  
```bash
typefully tags                  # List tags for an account
typefully create-tag "name"     # Create a new tag
typefully delete-tag "slug"     # Delete a tag
```  

### 媒体  
```bash
typefully upload-media <filename>    # Get upload URL for media
typefully media-status <id>          # Check media processing status
```  

## 示例  
### 创建简单帖子  
```bash
# Get your account ID
typefully social-sets

# Create a draft
typefully create-draft "Hello world! This is my first post." \
  --social-set-id 12345

# Create and publish immediately
typefully create-draft "Breaking news!" \
  --social-set-id 12345 --now
```  

### 创建多行帖子（Thread）  
```bash
typefully create-draft "1/ I am excited to share some updates...
2/ We have been working hard on new features...
3/ Here is what we have been building...
4/ Stay tuned for more!" \
  --social-set-id 12345 --thread
```  

### 延迟发布  
```bash
# Schedule for specific time
typefully create-draft "Mark your calendars! Launching next week." \
  --social-set-id 12345 \
  --schedule "2025-01-25T09:00:00Z"

# Schedule for optimal posting time
typefully create-draft "Best time to post..." \
  --social-set-id 12345 \
  --next-free-slot
```  

### 回复帖子  
```bash
typefully create-draft "Great thread! I completely agree." \
  --social-set-id 12345 \
  --reply-to "https://x.com/username/status/1234567890"
```  

### 在社区中发布  
```bash
typefully create-draft "Sharing with the community..." \
  --social-set-id 12345 \
  --community 1493446837214187523
```  

### 使用标签  
```bash
# List available tags
typefully tags --social-set-id 12345

# Create a tag
typefully create-tag "announcements" --social-set-id 12345

# Create draft with tag
typefully create-draft "Big announcement!" \
  --social-set-id 12345 \
  --tags announcements
```  

### 上传媒体  
```bash
# Get upload URL
typefully upload-media screenshot.png --social-set-id 12345

# Check status
typefully media-status <media-id> --social-set-id 12345
```  

## API 端点  
| 方法 | 端点 | 说明 |  
|--------|---------|---------|  
| GET | /v2/me | 获取当前用户信息 |  
| GET | /v2/social-sets | 列出所有社交媒体设置 |  
| GET | /v2/social-sets/{id} | 获取特定社交媒体设置的详细信息 |  
| GET | /v2/social-sets/{id}/drafts | 列出该设置的草稿 |  
| POST | /v2/social-sets/{id}/drafts | 创建新草稿 |  
| GET | /v2/social-sets/{id}/drafts/{id} | 获取特定草稿的详细信息 |  
| PATCH | /v2/social-sets/{id}/drafts/{id} | 更新草稿 |  
| DELETE | /v2/social-sets/{id}/drafts/{id} | 删除草稿 |  
| GET | /v2/social-sets/{id}/tags | 列出该设置的标签 |  
| POST | /v2/social-sets/{id}/tags | 创建新标签 |  
| DELETE | /v2/social-sets/{id}/tags/{slug} | 删除标签 |  
| POST | /v2/social-sets/{id}/media/upload | 上传媒体文件并获取上传链接 |  
| GET | /v2/social-sets/{id}/media/{id} | 检查媒体文件的上传状态 |  

## 支持的平台  
- X  
- LinkedIn  
- Mastodon  
- Threads  
- Bluesky  

## X 自动化规则  
在使用此功能时，请遵守 X 的自动化规则：  
- 不要在多个账户上发布相似内容。  
- 不要使用自动化工具操纵热门话题。  
- 仅向已同意接收自动回复的用户发送自动回复。  
- 每次用户互动仅发送一次自动回复。  
- 禁止自动点赞和批量关注。  
- 禁止自动将用户添加到列表中。  
- 所有自动化内容必须遵守 X 的媒体政策。  
- 如果发布包含图片的媒体，请将相关账户标记为敏感账户。  
- 不得使用自动化工具冒充他人。  
- 不得发布误导性链接。  

## 注意事项  
- 所有请求都需要 `TYPEFULLY_API_KEY` 环境变量。  
- 草稿默认为私密状态。  
- 使用 `--share` 选项可生成公共分享链接。  
- 使用 `--now` 选项会立即发布内容（不保存草稿）。  
- 如果未使用 `--now`，草稿会被保存以供后续审核。  
- 每个用户和每个社交媒体设置都有速率限制，请遵守这些限制。  
- 禁止尝试绕过速率限制。  

## 资源  
- Typefully 官网：[https://typefully.com](https://typefully.com)  
- Typefully API 文档：[https://docs.typefully.com](https://docs.typefully.com)  
- X 自动化规则：[https://help.x.com/en/rules-and-policies/x-automation](https://help.x.com/en/rules-and-policies/x-automation)