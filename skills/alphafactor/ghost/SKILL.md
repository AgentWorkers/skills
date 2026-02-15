---
name: ghost
description: 通过 Admin API 管理 Ghost CMS 的博客文章。支持创建、更新、删除和列出文章。新增功能：可以上传图片并为文章设置特色图片。适用于需要通过编程方式管理 Ghost 博客内容的情况。需要使用 `GHOST_API_URL` 和 `GHOST_ADMIN_API_KEY` 环境变量。
---

# Ghost CMS Admin API

通过 Admin API 以编程方式管理您的 Ghost 博文。

## 功能

- 📝 **创建/更新/删除帖子** - 完整的 CRUD 操作
- 🖼️ **上传图片** - 将图片上传到 Ghost 并获取图片链接
- 🎨 **设置封面图片** - 为帖子设置封面图片
- 📊 **查看帖子列表** - 查看带有状态的最新帖子
- 🏷️ **支持标签** - 为帖子添加标签

## 先决条件

### 1. 获取 Admin API 密钥

1. 登录到您的 Ghost 管理面板（`https://your-blog.com/ghost/`）
2. 转到 **设置** → **集成**
3. 点击 **“添加自定义集成”**
4. 复制 **Admin API 密钥**（格式：`id:secret`）

### 2. 配置凭据

创建配置文件：
```bash
mkdir -p ~/.config/ghost
```

将其添加到 `~/.config/ghost/credentials`：
```bash
export GHOST_API_URL="https://your-blog.com/ghost/api/admin/"
export GHOST_ADMIN_API_KEY="your-id:your-secret"
```

设置权限：
```bash
chmod 600 ~/.config/ghost/credentials
```

### 3. 安装依赖项

```bash
pip3 install requests pyjwt --user
```

## Python API 使用方法

### 基本设置

```python
import sys
import os
sys.path.insert(0, os.path.expanduser("~/.openclaw/workspace/ghost/scripts"))
import ghost

config = ghost.get_config()
```

### 创建帖子

```python
# Create post with HTML content
result = ghost.create_post(
    config=config,
    title="My Article Title",
    content="<h1>Title</h1><p>Content...</p>",  # HTML format
    status="published",  # or "draft"
    tags=["tech", "news"]
)
```

### 上传图片

```python
# Upload image and get URL
image_url = ghost.upload_image(config, "/path/to/image.jpg")
print(f"Image URL: {image_url}")
```

### 创建带封面图片的帖子

```python
# Upload cover image first
cover_image_url = ghost.upload_image(config, "cover.jpg")

# Create post with feature image
result = ghost.create_post(
    config=config,
    title="Article with Cover",
    content="<p>Article content...</p>",
    status="published",
    feature_image=cover_image_url,  # Set cover image
    tags=["featured"]
)
```

### 查看帖子列表

```python
posts = ghost.list_posts(config, limit=20)
for post in posts:
    print(f"{post['title']} - {post['status']}")
```

### 更新帖子

```python
ghost.update_post(
    config=config,
    post_id="post-id-here",
    title="New Title",
    status="published"
)
```

## CLI 使用方法

### 设置

```bash
# Install dependencies
pip3 install requests pyjwt --user

# Source credentials
source ~/.config/ghost/credentials
```

### 创建帖子

**作为草稿（默认）：**
```bash
python3 scripts/ghost.py create "My Article Title" "<p>Article content in HTML</p>"
```

**立即发布：**
```bash
python3 scripts/ghost.py create "Breaking News" "<p>Content here</p>" --status published
```

**带有标签：**
```bash
python3 scripts/ghost.py create "Tech News" "<p>Content</p>" --status published --tags "tech,news,ai"
```

### 更新帖子

```bash
# Update title
python3 scripts/ghost.py update 5f8c3c2e8c3d2e1f3a4b5c6d --title "New Title"

# Update content
python3 scripts/ghost.py update 5f8c3c2e8c3d2e1f3a4b5c6d --content "<p>New content</p>"

# Publish a draft
python3 scripts/ghost.py update 5f8c3c2e8c3d2e1f3a4b5c6d --status published
```

### 删除帖子

```bash
python3 scripts/ghost.py delete 5f8c3c2e8c3d2e1f3a4b5c6d
```

### 查看帖子列表

```bash
# List 10 most recent posts (default)
python3 scripts/ghost.py list

# List 20 posts
python3 scripts/ghost.py list 20
```

## 常见工作流程

### 带封面图片发布

```python
import ghost

config = ghost.get_config()

# Upload cover image
image_url = ghost.upload_image(config, "/path/to/cover.jpg")

# Create post with cover
result = ghost.create_post(
    config=config,
    title="Featured Article",
    content="<p>Article content...</p>",
    status="published",
    feature_image=image_url,
    tags=["featured", "tech"]
)

print(f"Published: {result['url']}")
```

### 批量操作

```bash
# List all drafts
python3 scripts/ghost.py list 100 | grep "🟡"

# Update specific post
python3 scripts/ghost.py update <id> --tags "featured"
```

## API 参考

### `ghost.create_post(config, title, content, status='draft', tags=None, feature_image=None)`

创建新帖子。

**参数：**
- `config` - 包含 `api_url` 和 `admin_api_key` 的配置字典
- `title` - 帖子标题
- `content` - HTML 内容
- `status` - 'draft' 或 'published'
- `tags` - 标签列表
- `feature_image` - 封面图片的 URL（可选）

**返回值：** 包含 id、url 和 status 的帖子字典

### `ghost.upload_image(config, image_path)`

将图片上传到 Ghost。

**参数：**
- `config` - 配置字典
- `image_path` - 图片文件的本地路径

**返回值：** 图片链接字符串

### `ghost.list_posts(config, limit=10)`

查看最新帖子。

**返回值：** 帖子字典列表

### `ghost.update_post(config, post_id, **kwargs)**

更新现有帖子。

**参数：**
- `post_id` - 要更新的帖子 ID
- `title` - 新标题（可选）
- `content` - 新内容（可选）
- `status` - 新状态（可选）
- `tags` - 新标签（可选）

### `ghost.delete_post(config, post_id)`

删除帖子。

## 故障排除

**错误：未找到名为 'jwt' 的模块**
→ 安装：`pip3 install pyjwt --user`

**错误：401 未经授权**
→ 检查您的 Admin API 密钥是否正确且未过期

**错误：404 未找到**
→ 确认 GHOST_API_URL 以 `/ghost/api/admin/` 结尾

**图片上传失败**
→ 检查图片文件是否存在且大小小于 10MB
→ 支持的格式：JPG、PNG、GIF

## 参考资料

- API 文档：[references/api.md](references/api.md)
- Ghost 官方文档：https://ghost.org/docs/admin-api/