---
name: telegraph-backlinks
description: 在 Telegraph（telegra.ph）网站上创建用于提高搜索引擎排名（SEO）的回链文章。该网站具有较高的域名权威性（DA 93），且支持“dofollow”链接类型，同时文章可被搜索引擎收录。无需进行身份验证，可通过 API 实现即时发布。适用于需要为 Telegraph 网站构建回链、创建包含链接的 telegra.ph 文章或快速生成大量回链页面的场景。支持单篇创建、批量操作、账户管理以及令牌复用等功能。
---
# Telegraph 回链功能

您可以在 telegra.ph 上发布文章（DA 评分约为 93，属于可被搜索引擎追踪的“可跟随链接”类型），同时文章会附带相关的回链。整个过程非常简单：只需调用一次 API，内容即可立即生效。

## 快速入门

```bash
# Create article with inline content
python3 scripts/telegraph-backlink.py create \
  --target "https://www.example.com" \
  --title "Article Title" \
  --content sections.json \
  --anchors "anchor text 1" "anchor text 2" \
  --author "BrandName"

# Batch create
python3 scripts/telegraph-backlink.py batch --file batch.json --output results.json

# List all pages across saved accounts
python3 scripts/telegraph-backlink.py list

# Create reusable account
python3 scripts/telegraph-backlink.py account --name "BrandName" --url "https://www.example.com"
```

所有路径均相对于此技能目录而言。

## 内容的 JSON 格式

内容由多个章节对象组成：

```json
[
  {"tag": "h3", "text": "Section Heading"},
  {"tag": "p", "text": "Paragraph with {backlink} placed naturally in the text."},
  {"tag": "p", "text": "Regular paragraph without a link."},
  {"tag": "ul", "items": [
    {"term": "Bold term", "desc": "Description"},
    "Simple list item"
  ]},
  {"tag": "blockquote", "text": "A quoted passage."}
]
```

- `{{backlink}}` 占位符会替换为指向目标 URL 的锚链接
- 每个 `{{backlink}}` 会依次使用 `--anchors` 中指定的锚文本
- 支持的标签：`h3`, `h4`, `p`, `ul`, `blockquote`

## 批量处理的 JSON 格式

```json
[
  {
    "target": "https://www.example.com",
    "title": "Article Title",
    "author": "BrandName",
    "anchors": ["anchor 1", "anchor 2"],
    "sections": [
      {"tag": "h3", "text": "Heading"},
      {"tag": "p", "text": "Text with {backlink} here."}
    ]
  }
]
```

## 工作原理

1. **账户创建**：`createAccount` API 用于创建账户，并返回访问令牌（该令牌会保存在 `~/.config/openclaw/telegraph-tokens.json` 文件中以供后续使用）
2. **页面创建**：`createPage` API 用于立即发布内容，并返回页面的实时 URL
3. **作者链接**：作者链接会被设置为目标 URL，以便在文章的作者信息中显示为额外的链接

## 令牌管理

- 令牌会自动保存到 `~/.config/openclaw/telegraph-tokens.json` 文件中
- 当 `--author` 参数与已保存的账户名称匹配时，系统会自动使用该令牌
- 一个账户可以创建无限个页面
- 可以为不同的活动或品牌使用不同的作者名称以区分内容来源

## 内容编写指南

- **建议内容长度至少为 800 字**：过短的内容可能导致搜索引擎降权
- **每篇文章应包含 2 个回链**，且锚文本应多样化
- **内容相关性**：主题一致的内容在 Telegraph 上的排名会更高
- **禁止使用图片**：只能通过 API 发布纯文本或 HTML 内容，以保持内容的丰富性
- Telegraph 支持的标签包括：`h3`, `h4`, `p`, `a`, `ul`, `ol`, `li`, `b`, `i`, `blockquote`, `figure`, `img`, `pre`, `code`, `aside`, `br`, `hr`

## 关键信息

- **DA 评分（Domain Authority）**：约 93（表示较高的权威性）
- **链接类型**：可被搜索引擎追踪（Dofollow）
- **索引情况**：Google 会定期抓取 telegra.ph 的内容
- **发送频率限制**：暂无明确限制，但建议批量发送时间隔 1 秒
- **无需创建专门账户**：令牌会在使用过程中自动生成
- **后续编辑**：可以使用相同的令牌通过 `editPage` API 对页面进行修改
- **作者信息**：作者链接应设置为目标 URL，以增加额外的链接效果