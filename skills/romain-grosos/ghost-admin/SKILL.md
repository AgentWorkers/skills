---
name: ghost
description: "通过 Admin API v5.x 进行 Ghost CMS 内容管理。适用场景包括：  
（1）创建、编辑或发布博客文章或静态页面；  
（2）管理标签；  
（3）上传图片；  
（4）查看会员信息、新闻通讯内容或层级信息；  
（5）检查站点设置。  
**不适用场景**：  
- 主题管理（需使用 Ghost CLI）；  
- Webhook 配置；  
- 自动发送电子邮件（在内容发布时自动触发）；  
- 内容导入/导出（请使用 Ghost Admin 界面）；  
- 多站点设置。"
homepage: https://github.com/rwx-g/openclaw-skill-ghost
compatibility: Python 3.9+ · network access to Ghost instance · Admin API Key
metadata:
  {
    "openclaw": {
      "emoji": "👻",
      "requires": { "env": ["GHOST_URL", "GHOST_ADMIN_KEY"] },
      "primaryEnv": "GHOST_ADMIN_KEY"
    }
  }
ontology:
  reads: [posts, pages, tags, site, members, newsletters, tiers, users]
  writes: [posts, pages, tags, images]
---
# Ghost Skill

这是一个完整的 Ghost Admin API v5 客户端。使用 HS256 JWT 进行身份验证，所有 HTTP 请求均通过标准库（urllib）完成，完全不依赖任何外部库。  
**凭证存储路径：** `~/.openclaw/secrets/ghost_creds`  
**配置文件：** `~/.openclaw/config/ghost/config.json`

## 触发语句  
当用户执行以下操作时，该技能会立即被触发：  
- “创建/编写/草拟博客文章”  
- “发布这篇文章”  
- “更新/编辑文章标题或 slug”  
- “取消发布/将文章恢复为草稿状态”  
- “创建/添加标签”  
- “创建/更新/发布页面”  
- “将图片上传到 Ghost”  
- “查看我的文章/草稿”  
- “为文章安排发布时间”  
- “我的 Ghost 网站有哪些内容？”  

## 快速入门  
（相关代码块请参见 **```bash
python3 scripts/ghost.py config    # verify credentials + active config
python3 scripts/ghost.py site      # test connection + show site info
python3 scripts/ghost.py posts --limit 3 --fields "id,title,status"
```**）  

## 设置  
（相关代码块请参见 **```bash
python3 scripts/setup.py       # interactive: credentials + permissions + connection test
python3 scripts/init.py        # validate all configured permissions against live instance
```**）  
`init.py` 仅在 `allow_delete=true` 时运行写入/删除功能的测试。当 `allow_delete=false` 时，写入测试会被跳过，因此不会生成任何测试结果文件。  

**手动配置：**  
将 `Admin API Key` 复制到 `~/.openclaw/secrets/ghost_creds` 文件中（文件权限设置为 `chmod 600`）。  
（相关代码块请参见 **```
GHOST_URL=https://your-ghost.example.com
GHOST_ADMIN_KEY=id:secret_hex
```**）  

**config.json** 中的配置选项：  
| 参数 | 默认值 | 功能说明 |  
|---------|-----------|-----------|  
| `allow_publish` | `false` | 禁止发布文章（需显式设置为 `true` 才可发布）  
| `allow_delete` | `false` | 禁止删除文章/页面/标签  
| `allow_member_access` | `false` | 禁止成员进行读写操作  
| `default_status` | `"draft"` | 未指定状态时默认使用“草稿”状态  
| `default_tags` | `[]` | 新文章会自动添加这些标签  
| `readonly_mode` | `false` | 禁止所有写入操作  

## 存储与凭证管理  
该技能会读取和写入以下路径中的数据：  
- `~/.openclaw/secrets/ghost_creds`：存储 Ghost 的凭证信息（GHOST_URL、GHOST_ADMIN_KEY），文件权限设置为 `chmod 600`。  
- `~/.openclaw/config/ghost/config.json`：配置行为限制（如是否允许发布、删除等）。这些配置不会随 ClawHub 的更新而丢失。  

凭证也可以通过环境变量（`GHOST_URL`、`GHOST_ADMIN_KEY`）提供。该技能会优先使用环境变量中的值。  

**卸载时的清理操作：**  
执行 `clawhub uninstall ghost-admin` 命令会删除该技能相关的目录及配置文件。  

## 模块使用方法  
（相关代码块请参见 **```python
from scripts.ghost import GhostClient
gc = GhostClient()
post = gc.create_post("My Title", html="<p>Body</p>", status="draft")
gc.publish_post(post["id"])
```**）  

## 命令行接口（CLI）参考  
（相关代码块请参见 **```bash
# Posts
python3 scripts/ghost.py posts --status published --limit 10
python3 scripts/ghost.py posts --tag devops --fields "id,title,published_at"
python3 scripts/ghost.py post <id_or_slug>
python3 scripts/ghost.py post-create "Title" --html "<p>...</p>" --status draft
python3 scripts/ghost.py post-create "Title" --html-file body.html --tags "DevOps,Linux"
python3 scripts/ghost.py post-create "Title" --html-file body.html --feature-image "https://..."
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
```**）  

## 模板说明：  
- **草稿 → 审核 → 发布**  
- **研究 → 结构化文章撰写**  
- **按标签筛选内容**  
- **批量创建标签**  
（相关代码块请参见 **```python
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
```** 至 **```python
for name in ["DevOps", "Security", "Linux", "Cloud"]:
    try:
        gc.create_tag(name, slug=name.lower())
    except Exception:
        pass  # already exists
```**）  

## 使用建议：  
- 将 `allow_publish` 设置为 `false`，`default_status` 设置为 `draft`，以实现“仅建议”模式。  
- 在配置文件中使用 `default_tags` 以实现自动标签添加（例如，始终添加 “AI-assisted” 标签）。  
- 先从研究摘要中生成草稿，分享预览链接，待人工审核后再发布。  
- 使用 `posts --status draft` 命令查看待处理的草稿内容。  
- 先上传功能图片，然后在文章 HTML 中嵌入生成的图片链接。  

## 注意事项：  
- 如果未指定 `updated_at`，`update_post`/`update_page` 会自动获取文章的更新时间。  
- Ghost v5 内部使用 Lexical 格式存储内容，但 `html` 格式也能被正确解析。  
- 当 `allow_publish` 设置为 `false` 时，文章状态会自动设置为 “草稿”；不会引发错误。  
- JWT 令牌会为每次请求生成新的令牌（有效期为 5 分钟），无需缓存。  
- 如果未指定 slug，系统会自动从文章标题生成 slug；可以使用 `--slug` 参数自定义 slug 以获得更清晰的 URL。  

## 可与其他技能结合使用：  
| 技能 | 工作流程 |  
|---------|---------|  
| **summarize** | 从 URL 或 PDF 文件生成 Ghost 文章草稿 |  
| **tavily-search** | 搜索主题后生成结构化的 Ghost 草稿 |  
| **nextcloud** | 将草稿保存到 NextCloud，审核后发布到 Ghost |  
| **gmail** | 从邮件转发内容生成 Ghost 文章草稿 |  
| **api-gateway (linkedin)** | 将 Ghost 文章发布到 LinkedIn 并同步显示摘要 |  

## API 参考：  
详细端点信息、NQL 过滤条件、字段列表及错误代码请参阅 `references/api.md`。  
常见问题及解决方法请参阅 `references/troubleshooting.md`。