---
name: wordpress-api-gutenberg
description: 通过 REST API 创建、编辑和发布 WordPress 文章，同时支持完整的 Gutenberg 方块功能。适用于需要自动化 WordPress 内容发布、程序化生成文章或通过 API 调用管理文章的场景。支持多种认证方式（JWT、应用密码），包括 Gutenberg 方块的序列化处理、特色图片、分类、标签以及文章的草稿/发布工作流程。
---
# 使用Gutenberg的WordPress API

## 概述

本文档提供了关于如何通过WordPress REST API使用Gutenberg块编辑器格式创建和管理文章的全面指导。内容涵盖了身份验证、块序列化、媒体上传以及发布工作流程。

## 快速入门

在使用API之前，请确保满足以下条件：

1. 拥有一个已启用REST API的WordPress站点（默认情况下已启用）。
2. 具备身份验证凭据：
   - **应用程序密码**（WordPress 5.6及以上版本）：在`/wp-admin/admin.php?page=application-passwords`页面生成。
   - 安装了JWT身份验证插件（可选）。
   - 基本身份验证的用户名/密码（不建议在生产环境中使用）。
3. **基础URL**：`https://your-site.com/wp-json/wp/v2`

## 身份验证

### 应用程序密码（推荐）

```bash
# Set environment variables
export WP_URL="https://your-site.com"
export WP_USERNAME="admin"
export WP_APPLICATION_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
```

```python
import requests
import os

wp_url = os.environ.get('WP_URL')
username = os.environ.get('WP_USERNAME')
password = os.environ.get('WP_APPLICATION_PASSWORD')

auth = (username, password)
```

### JWT身份验证

如果使用JWT插件，请先获取令牌：

```python
import requests

wp_url = "https://your-site.com"
username = "admin"
password = "password"

# Get token
resp = requests.post(f"{wp_url}/wp-json/jwt-auth/v1/token", 
                     json={"username": username, "password": password})
token = resp.json()['token']

headers = {"Authorization": f"Bearer {token}"}
```

## 使用Gutenberg块创建文章

WordPress REST API要求文章以Gutenberg的序列化块格式进行传输。内容字段应包含块注释和HTML代码。

### 基本块结构

```python
def create_gutenberg_post(title, content_blocks):
    """
    Create a post with Gutenberg blocks.
    
    Args:
        title: Post title
        content_blocks: List of block dictionaries with 'blockName' and 'attrs'
    
    Returns:
        JSON data for POST request
    """
    # Serialize blocks to Gutenberg format
    block_html = []
    for block in content_blocks:
        block_name = block.get('blockName', 'core/paragraph')
        attrs = block.get('attrs', {})
        inner_html = block.get('innerHTML', '')
        
        # Create block comment
        attrs_json = json.dumps(attrs) if attrs else ''
        block_comment = f'<!-- wp:{block_name} {attrs_json} -->'
        block_html.append(f'{block_comment}{inner_html}<!-- /wp:{block_name} -->')
    
    content = '\n\n'.join(block_html)
    
    return {
        "title": title,
        "content": content,
        "status": "draft",  # or "publish"
        "format": "standard"
    }
```

### 常见块示例

请参阅[references/common_blocks.md](references/common_blocks.md)，了解以下内容的详细示例：
- 带有格式设置的段落块
- 标题块（h2-h4）
- 带有标题和对齐方式的图片块
- 列表块（有序/无序）
- 引用块
- 代码块
- 自定义HTML块
- 列表和布局块

## 完整工作流程

### 第1步：准备身份验证
将凭据设置为环境变量或配置文件中的内容。

### 第2步：创建文章数据
定义文章标题、内容块、分类、标签以及封面图片。

### 第3步：上传媒体（如需要）
```python
def upload_image(image_path, post_id=None):
    """Upload image to WordPress media library."""
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {}
        if post_id:
            data['post'] = post_id
        
        response = requests.post(f"{wp_url}/wp-json/wp/v2/media",
                                 files=files, data=data, auth=auth)
        return response.json()
```

### 第4步：创建文章
```python
def create_post(post_data):
    """Create new WordPress post."""
    response = requests.post(f"{wp_url}/wp-json/wp/v2/posts",
                             json=post_data, auth=auth)
    return response.json()
```

### 第5步：更新文章状态
将文章状态从“草稿”更改为“已发布”：
```python
def publish_post(post_id):
    """Publish a draft post."""
    response = requests.post(f"{wp_url}/wp-json/wp/v2/posts/{post_id}",
                             json={"status": "publish"}, auth=auth)
    return response.json()
```

## 高级功能

### 分类和标签
```python
# Get or create category
def ensure_category(name, slug=None):
    categories = requests.get(f"{wp_url}/wp-json/wp/v2/categories",
                             params={"search": name}, auth=auth).json()
    if categories:
        return categories[0]['id']
    else:
        new_cat = requests.post(f"{wp_url}/wp-json/wp/v2/categories",
                               json={"name": name, "slug": slug or name.lower()},
                               auth=auth).json()
        return new_cat['id']
```

### 封面图片
```python
# Upload image first, then set as featured
image_data = upload_image("path/to/image.jpg")
post_data["featured_media"] = image_data['id']
```

### 自定义字段（ACF）
如果使用了Advanced Custom Fields插件：
```python
post_data["meta"] = {
    "your_field_name": "field_value"
}
```

## 错误处理

务必检查响应状态码：
- 401：身份验证失败
- 403：用户没有权限
- 404：端点未找到（请检查WordPress版本）
- 500：服务器错误（请查看PHP错误日志）

## 脚本

`scripts/`目录中包含了一些辅助工具：
- `wp_publish.py`：完整的发布流程处理脚本
- `block_generator.py`：将Markdown转换为Gutenberg块格式的HTML代码
- `media_uploader.py`：批量上传图片的脚本

## 参考资料

- [common_blocks.md](references/common_blocks.md)：详细的块示例
- [api_reference.md](references/api_reference.md)：完整的WordPress REST API参考文档
- [troubleshooting.md](references/troubleshooting.md)：常见问题及解决方法

## 资源文件

- `templates/article_template.json`：典型文章结构的JSON模板
- `block_samples/`：各种内容类型的示例块HTML代码

## 示例请求

```bash
# Using curl with Application Password
curl -X POST https://your-site.com/wp-json/wp/v2/posts \
  -u "admin:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "content": "<!-- wp:paragraph --><p>Hello World!</p><!-- /wp:paragraph -->",
    "status": "draft"
  }'
```