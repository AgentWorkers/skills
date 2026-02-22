---
name: ghost
description: "通过 Admin API v5.x 来管理 Ghost CMS 的内容。适用场景包括：  
(1) 创建、编辑或发布博客文章或静态页面；  
(2) 管理标签；  
(3) 上传图片；  
(4) 查看会员信息、新闻通讯内容或层级信息；  
(5) 检查站点设置。  
**不适用场景**：  
- 主题管理（需要使用 Ghost CLI）；  
- Webhook 配置；  
- 自动发送邮件（在内容发布时自动触发）；  
- 内容导入/导出（请使用 Ghost 的 Admin 界面）；  
- 多站点设置。"
homepage: https://github.com/rwx-g/openclaw-skill-ghost
compatibility: Python 3.9+ · requests · network access to Ghost instance · Admin API Key
metadata:
  {
    "openclaw": {
      "emoji": "👻",
      "requires": { "env": ["GHOST_URL", "GHOST_ADMIN_KEY"] },
      "primaryEnv": "GHOST_ADMIN_KEY"
    }
  }
ontology:
  reads: []
  writes: [posts, pages, tags, images, members]
---
# Ghost Skill

这是一个完整的 Ghost Admin API v5 客户端。使用标准库（stdlib）进行 HS256 JWT 验证；除了 `requests` 之外，不依赖任何外部库。

**凭证：** `~/.openclaw/secrets/ghost_creds`  
**配置文件：** `skill` 目录下的 `config.json`。

## 触发语句

当用户说出以下语句时，立即加载此技能：

- “创建/编写/草拟一篇博客文章”
- “发布这篇文章”，“将这篇文章发布到 Ghost 上”
- “更新/编辑[文章标题或 slug]”，“更改我的文章标题”
- “取消发布/恢复为草稿状态[文章]”
- “创建/添加标签”，“查看我在 Ghost 上的标签”
- “创建/更新/发布页面”
- “将这张图片上传到 Ghost”
- “查看我的文章/草稿”，“显示草稿列表”
- “为这篇文章安排发布时间”
- “我的 Ghost 网站上有什么内容？”，“显示网站信息”

## 快速入门

```bash
python3 scripts/ghost.py config    # verify credentials + active config
python3 scripts/ghost.py site      # test connection + show site info
python3 scripts/ghost.py posts --limit 3 --fields "id,title,status"
```

## 设置

```bash
python3 scripts/setup.py   # interactive: credentials + permissions + connection test
python3 scripts/init.py    # validate all configured permissions against live instance
```

**手动设置：** 将 `~/.openclaw/secrets/ghost_creds` 文件的权限设置为 `chmod 600`：
```
GHOST_URL=https://your-ghost.example.com
GHOST_ADMIN_KEY=id:secret_hex
```
**获取 Admin API 密钥：**  
进入 Ghost Admin → 设置 → 集成 → 添加自定义集成 → 复制 **Admin API 密钥**。

**config.json** 中的配置选项及其作用：

| 参数 | 默认值 | 功能 |
|-------|---------|--------|
| `allow_publish` | `true` | 允许文章状态为“已发布”（`false` 仅允许草稿状态） |
| `allow_delete` | `false` | 允许删除文章/页面/标签 |
| `allow_member_access` | `false` | 启用成员的读写权限 |
| `default_status` | `"draft"` | 未指定状态时使用的默认状态 |
| `default_tags` | `[]` | 新文章会自动添加这些标签 |
| `readonly_mode` | `false` | 取消默认设置：禁止所有写入操作 |

## 模块使用方法

```python
from scripts.ghost import GhostClient
gc = GhostClient()
post = gc.create_post("My Title", html="<p>Body</p>", status="draft")
gc.publish_post(post["id"])
```

## 命令行接口（CLI）参考

```bash
# Posts
python3 scripts/ghost.py posts --status published --limit 10
python3 scripts/ghost.py posts --tag devops --fields "id,title,published_at"
python3 scripts/ghost.py post <id_or_slug>
python3 scripts/ghost.py post-create "Title" --html "<p>...</p>" --status draft
python3 scripts/ghost.py post-create "Title" --html-file body.html --tags "DevOps,Linux"
python3 scripts/ghost.py post-update <id> --fields-json '{"title":"New","custom_excerpt":"..."}'
python3 scripts/ghost.py post-publish <id>
python3 scripts/ghost.py post-unpublish <id>
python3 scripts/ghost.py post-delete <id>          # requires allow_delete: true

# Pages
python3 scripts/ghost.py pages
python3 scripts/ghost.py page-create "About" --html "<p>...</p>"
python3 scripts/ghost.py page-publish <id>

# Tags
python3 scripts/ghost.py tags
python3 scripts/ghost.py tag-create "DevOps" --slug devops --desc "DevOps content"
python3 scripts/ghost.py tag-delete <id>           # requires allow_delete: true

# Images
python3 scripts/ghost.py image-upload ./image.png --alt "Description"

# Members & newsletters (read)
python3 scripts/ghost.py members --limit 20        # requires allow_member_access: true
python3 scripts/ghost.py newsletters
python3 scripts/ghost.py tiers

# Account
python3 scripts/ghost.py site
python3 scripts/ghost.py me
python3 scripts/ghost.py config
```

## 模板

### 草稿 → 审核 → 发布
```python
gc = GhostClient()
# 1. Create draft
post = gc.create_post(
    title="My Article",
    html=article_html,
    tags=[{"name": "DevOps"}, {"name": "Linux"}],
    meta_description="Short SEO description",
    status="draft",
)
draft_url = f"{gc.base_url}/ghost/#/editor/post/{post['id']}"
# 2. Return preview link to user for review
# → f"Draft created: {draft_url}"
# 3. After user approval:
gc.publish_post(post["id"])
# → f"Published: {post['url']}"
```

### 研究 → 结构化文章
```python
# Create a post with full SEO metadata
post = gc.create_post(
    title="Why Rust is Taking Over Systems Programming",
    html=content_html,
    custom_excerpt="A technical deep-dive into Rust's memory model and adoption trends.",
    meta_title="Rust Systems Programming 2025",
    meta_description="Why Rust is replacing C++ in systems programming in 2025.",
    og_title="Rust is Taking Over Systems Programming",
    tags=[{"name": "Rust"}, {"name": "Systems"}],
    feature_image="https://example.com/rust.png",
    status="draft",
)
```

### 按标签审核内容
```python
result = gc.list_posts(limit="all", tag="devops", fields="id,title,status,published_at")
posts  = result["posts"]
drafts    = [p for p in posts if p["status"] == "draft"]
published = [p for p in posts if p["status"] == "published"]
# → summarize backlog for user
```

### 批量创建标签
```python
for name in ["DevOps", "Security", "Linux", "Cloud"]:
    try:
        gc.create_tag(name, slug=name.lower())
    except Exception:
        pass  # already exists
```

## 建议：
- 将 `allow_publish` 设置为 `false`，`default_status` 设置为 `draft`，以实现“仅建议”模式。
- 在配置文件中使用 `default_tags` 选项进行自动标签添加（例如，始终添加 “AI-assisted” 标签）。
- 从研究摘要创建草稿，分享预览链接，经过人工审核后再发布。
- 使用 `posts --status draft` 命令列出所有草稿文章，以便进行优先处理。
- 先上传功能图片，然后在文章 HTML 中嵌入返回的图片链接。

## 注意事项：
- **`updated_at` 冲突处理**：`update_post`/`update_page` 会自动获取 `updated_at` 时间戳（如果未提供）。
- **HTML 内容**：Ghost v5 内部使用 Lexical 格式存储内容，但使用 `html` 标签仍可正常导入。
- 当 `allow_publish` 设置为 `false` 时，文章状态会自动设置为 “draft”，不会引发错误。
- **JWT 令牌**：每次请求都会生成新的令牌（有效期 5 分钟），无需缓存。
- **Slug**：如果未提供标题，系统会自动生成 Slug。可以使用 `--slug` 参数自定义 Slug 以获得更清晰的网址。

## 可与其他技能结合使用：

| 技能 | 工作流程 |
|-------|----------|
| **summarize** | 将 URL 或 PDF 文件内容总结后，生成 Ghost 文章草稿 |
| **tavily-search** | 搜索某个主题后，生成包含来源信息的 Ghost 草稿 |
| **nextcloud** | 将 `.md` 草稿文件保存到 NextCloud，审核后发布到 Ghost |
| **gmail** | 将邮件或文章转发后，生成 Ghost 文章草稿 |
| **api-gateway (linkedin)** | 发布 Ghost 文章后，将其摘录内容发布到 LinkedIn |

## API 参考

有关端点详情、NQL 过滤器、字段列表和错误代码，请参阅 `references/api.md`。

## 故障排除

有关常见错误及其解决方法，请参阅 `references/troubleshooting.md`。