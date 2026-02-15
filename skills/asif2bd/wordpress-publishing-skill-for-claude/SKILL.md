---
name: wordpress-publisher
description: 通过 REST API 直接将内容发布到 WordPress 网站，并完全支持 Gutenberg 块格式。支持创建和发布文章/页面，自动从网站中加载并选择分类，生成优化过的 SEO 标签，在发布前预览文章内容，以及为表格、图片、列表和富格式内容生成相应的 Gutenberg 块。适用于用户需要将内容发布到 WordPress、在博客中发布文章、更新 WordPress 文章，或将 Markdown 格式转换为 Gutenberg 块的情况。
author: xCloud
version: 1.0.0
---

# WordPress 发布器

使用 REST API 直接将内容发布到 WordPress 网站，支持完整的 Gutenberg 块格式、自动分类选择、SEO 标签生成和预览功能。

## 完整工作流程概述

```
1. CONNECT    → Authenticate with WordPress site
2. ANALYZE    → Load categories from site, analyze content for best match
3. GENERATE   → Create SEO-optimized tags based on content
4. CONVERT    → Transform markdown/HTML to Gutenberg blocks
5. PREVIEW    → Create draft and verify rendering
6. PUBLISH    → Publish or schedule the post
7. VERIFY     → Confirm live post renders correctly
```

---

## 第 1 步：连接设置

### 获取凭据
向用户索取以下信息：
- WordPress 网站地址（例如：`https://example.com`）
- WordPress 用户名
- 应用程序密码（非常规密码）

### 如何创建应用程序密码
指导用户：
1. 进入 WordPress 管理后台的 **用户 → 个人资料**  
2. 移动到 **应用程序密码** 部分  
3. 输入名称：`Claude Publisher`  
4. 点击 **添加新的应用程序密码**  
5. 复制生成的密码（仅显示一次，包含空格）

### 测试连接
```python
from scripts.wp_publisher import WordPressPublisher

wp = WordPressPublisher(
    site_url="https://example.com",
    username="admin",
    password="xxxx xxxx xxxx xxxx xxxx xxxx"  # Application password
)

# Test connection
user_info = wp.test_connection()
print(f"Connected as: {user_info['name']}")
```

---

## 第 2 步：加载和选择分类

### 从网站自动加载分类
```python
# Get all categories from the WordPress site
categories = wp.get_categories_with_details()

# Returns list like:
# [
#   {'id': 1, 'name': 'Uncategorized', 'slug': 'uncategorized', 'count': 5},
#   {'id': 2, 'name': 'Tutorials', 'slug': 'tutorials', 'count': 12},
#   {'id': 3, 'name': 'Cloud Hosting', 'slug': 'cloud-hosting', 'count': 8},
# ]
```

### 智能分类选择
系统会分析内容并选择最合适的分类：

```python
# Analyze content and suggest best category
suggested_category = wp.suggest_category(
    content=article_content,
    title=article_title,
    available_categories=categories
)

# Or let user choose from available options
print("Available categories:")
for cat in categories:
    print(f"  [{cat['id']}] {cat['name']} ({cat['count']} posts)")
```

### 分类选择逻辑
1. **精确匹配** - 标题/内容包含分类名称  
2. **关键词匹配** - 分类别名与主题关键词匹配  
3. **父分类** - 如果没有匹配，则选择更广泛的父分类  
4. **创建新分类** - 如果没有合适的分类，则创建新分类（需用户批准）

---

## 第 3 步：生成 SEO 优化标签

### 自动标签生成
生成有助于提高 Google 搜索可见性的标签：

```python
# Generate tags based on content analysis
tags = wp.generate_seo_tags(
    content=article_content,
    title=article_title,
    max_tags=10
)

# Returns list like:
# ['n8n hosting', 'workflow automation', 'self-hosted n8n', 
#  'affordable hosting', 'docker deployment', 'node.js hosting']
```

### 标签生成规则
1. **主要关键词** - 始终作为第一个标签  
2. **次要关键词** - 包含 2-3 个相关术语  
3. **长尾关键词** - 包含 3-4 个具体短语  
4. **实体标签** - 包含提到的产品/品牌名称  
5. **主题标签** - 包含更广泛的分类术语  

### 在 WordPress 中创建/获取标签
```python
# Get or create all tags, returns list of tag IDs
tag_ids = wp.get_or_create_tags(tags)
```

---

## 第 4 步：将内容转换为 Gutenberg 块

### 将 Markdown 转换为 Gutenberg
```python
from scripts.content_to_gutenberg import convert_to_gutenberg

# Convert markdown content
gutenberg_content = convert_to_gutenberg(markdown_content)
```

### 支持的转换类型

| Markdown | Gutenberg 块 |
|----------|-----------------|
| `# 标题` | `wp:heading` |
| `**粗体**` | `<strong>` 标签在段落中 |
| `- 列表项` | `wp:list` |
| `1. 有序列表` | `wp:list {"ordered":true}` |
| `\`\`\`代码\`\`\` | `wp:code` |
| `> 引用` | `wp:quote` |
| `![alt](url)` | `wp:image` |
| `\| 表格 \|` | `wp:table` |

### 表格转换（对 AI 内容至关重要）
表格会以正确的 Gutenberg 结构进行转换：

```python
# Input markdown:
| Feature | Plan A | Plan B |
|---------|--------|--------|
| Price   | $10    | $20    |

# Output Gutenberg:
<!-- wp:table -->
<figure class="wp-block-table"><table>
  <thead><tr><th>Feature</th><th>Plan A</th><th>Plan B</th></tr></thead>
  <tbody><tr><td>Price</td><td>$10</td><td>$20</td></tr></tbody>
</table></figure>
<!-- /wp:table -->
```

---

## 第 5 步：发布前的预览

### 创建草稿进行预览
```python
# Create as draft first
result = wp.create_draft(
    title="Article Title",
    content=gutenberg_content,
    categories=[category_id],
    tags=tag_ids,
    excerpt="Auto-generated or custom excerpt"
)

post_id = result['post_id']
preview_url = result['preview_url']
edit_url = result['edit_url']
```

### 验证预览效果
```python
# Fetch preview page to verify rendering
preview_content = wp.fetch_preview(post_id)

# Check for issues
issues = wp.validate_rendered_content(preview_content)
if issues:
    print("Issues found:")
    for issue in issues:
        print(f"  - {issue}")
```

### 预览检查清单
- [ ] 标题显示正确  
- [ ] 所有标题（H2、H3、H4）都能正确显示  
- [ ] 表格格式正确  
- [ ] 列表（项目符号和编号）显示正确  
- [ ] 代码块有语法高亮显示  
- [ ] 图片已加载（如果有）  
- [ ] 链接可点击  
- [ ] 分类显示正确  
- [ ] 标签在文章中显示  

---

## 第 6 步：发布文章

### 发布草稿
```python
# After preview approval, publish
result = wp.publish_post(post_id)
live_url = result['live_url']
```

### 或者直接创建并发布
```python
# Full publish workflow in one call
result = wp.publish_content(
    title="Article Title",
    content=gutenberg_content,
    category_names=["Cloud Hosting"],  # By name, auto-resolves to ID
    tag_names=["n8n", "hosting", "automation"],
    status="publish",  # or "draft", "pending", "private", "future"
    excerpt="Custom excerpt for SEO",
    slug="custom-url-slug"
)
```

### 安排文章发布时间
```python
# Schedule for future publication
from datetime import datetime, timedelta

publish_date = datetime.now() + timedelta(days=1)
result = wp.publish_content(
    title="Scheduled Post",
    content=content,
    status="future",
    date=publish_date.isoformat()
)
```

---

## 第 7 步：验证已发布的文章

### 查看实时文章
```python
# Verify the published post
verification = wp.verify_published_post(post_id)

print(f"Live URL: {verification['url']}")
print(f"Status: {verification['status']}")
print(f"Categories: {verification['categories']}")
print(f"Tags: {verification['tags']}")
```

### 常见问题及解决方法

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| 表格无法显示 | 缺少表格包装器 | 使用正确的 `wp:table` 块结构 |
| 代码没有高亮显示 | 缺少语言属性 | 在代码块中添加 `{"language":"python"}` |
| 图片无法显示 | URL 错误或媒体文件缺失 | 先将图片上传到 WordPress，然后使用媒体 ID |
| 标签未显示 | 主题不支持显示标签 | 检查主题设置或更换主题 |

---

## 完整示例工作流程

```python
from scripts.wp_publisher import WordPressPublisher
from scripts.content_to_gutenberg import convert_to_gutenberg

# 1. Connect
wp = WordPressPublisher(
    site_url="https://xcloud.host",
    username="admin",
    password="xxxx xxxx xxxx xxxx"
)

# 2. Load categories and select best match
categories = wp.get_categories_with_details()
best_category = wp.suggest_category(content, title, categories)

# 3. Generate SEO tags
tags = wp.generate_seo_tags(content, title, max_tags=10)

# 4. Convert to Gutenberg
gutenberg_content = convert_to_gutenberg(markdown_content)

# 5. Create draft and preview
draft = wp.create_draft(
    title="7 Best n8n Hosting Providers in 2026",
    content=gutenberg_content,
    categories=[best_category['id']],
    tags=wp.get_or_create_tags(tags)
)
print(f"Preview: {draft['preview_url']}")

# 6. After verification, publish
result = wp.publish_post(draft['post_id'])
print(f"Published: {result['live_url']}")
```

---

## 快速参考

### API 端点
| 资源 | 端点 |
|----------|----------|
| 文章 | `/wp-json/wp/v2/posts` |
| 页面 | `/wp-json/wp/v2/pages` |
| 分类 | `/wp-json/wp/v2/categories` |
| 标签 | `/wp-json/wp/v2/tags` |
| 媒体 | `/wp-json/wp/v2/media` |

### 文章状态
| 状态 | 描述 |
|--------|-------------|
| `publish` | 已发布且可见 |
| `draft` | 保存但未显示 |
| `pending` | 待审核 |
| `private` | 仅对管理员可见 |
| `future` | 安排在未来发布 |

### 所需文件
- `scripts/wp_publisher.py` - 主要发布器类  
- `scripts/content_to_gutenberg.py` - Markdown/HTML 转换器  
- `references/gutenberg-blocks.md` - 块格式参考文档

---

## 错误处理

| 错误代码 | 含义 | 解决方案 |
|------------|---------|----------|
| 401 | 凭据无效 | 检查用户名和应用程序密码 |
| 403 | 权限不足 | 用户需要具有编辑者或管理员权限 |
| 404 | 未找到端点 | 确认 REST API 已启用 |
| 400 | 数据无效 | 检查分类/标签 ID 是否存在 |
| 500 | 服务器错误 | 重试或查看 WordPress 错误日志 |

---

## 最佳实践
1. **始终先进行预览** - 先创建草稿，验证后再发布  
2. **使用应用程序密码** - 绝不要使用常规 WordPress 密码  
3. **选择合适的分类** - 有助于网站组织和 SEO  
4. **生成相关标签** - 提高 Google 可发现性  
5. **验证 Gutenberg 块的结构** | 确保块结构正确  
6. **保持摘录长度在 160 个字符以内** | 适合搜索结果展示  
7. **使用描述性的别名** | 在 URL 中包含主要关键词