---
name: rss-feed-generator
description: 从那些包含文章列表但缺乏原生RSS/Atom feed的网页中生成有效的RSS 2.0或Atom 1.0 feed。该功能会在遇到如下短语时触发：`generate a feed for`、`create an RSS feed from`、`make an Atom feed for`、`this page has no RSS`，或任何请求从博客/新闻/文章列表页面生成feed URL或feed XML的指令。该工具会获取页面内容，提取文章元数据，并输出格式正确的feed XML，同时提供一个可自托管的HTML封装页面，其中包含嵌入的feed发现链接标签。
license: See LICENSE.txt
---
# RSS / Atom 订阅源生成器（v1.0.0）

该工具可以从任何列出帖子、文章或新闻条目的网页生成有效的 **RSS 2.0** 或 **Atom 1.0** XML 订阅源，但这些网页本身并不提供自己的订阅源。

---

## 默认设置

| 参数                | 默认值                                      |
|-------------------|----------------------------------------|
| 首选格式            | RSS 2.0（根据请求也可选择 Atom 1.0）                  |
| 最大条目数量          | 20条（最新条目优先显示）                        |
| 日期替代值           | 页面抓取日期（ISO 8601, UTC格式）                     |
| 描述                | 帖子摘录的前280个字符                         |
| 编码                | UTF-8                                      |
| 输出格式            | 原始XML · HTML页面 · 两者兼备                         |
| 用户交互风格          | 友好且专业                               |

---

## 触发指令

| 用户指令            | 动作                                        |
|-------------------|-----------------------------------------|
| T1                | “为 {url} 生成RSS/Atom订阅源”                        | 获取页面内容 → 识别帖子 → 生成XML           |
| T2                | “该页面没有订阅源：{url}”                          | 执行与T1相同的操作                        |
| T3                | “从 {url} 创建订阅源”                            | 执行与T1相同的操作                        |
| T4                | “将 {url} 的帖子转换为RSS格式”                        | 执行与T1相同的操作                        |
| T5                | “为 {url} 创建可自托管的订阅源”                        | 生成包含HTML封装的XML                     |
| T6                | “更新/刷新 {url} 的订阅源”                        | 重新抓取数据并重新生成订阅源                   |

---

## 操作流程

1. **页面抓取** — 通过调用 `WEB_FETCH` 函数获取目标URL（该函数定义在 `https://linkeddata.uriburner.com/chat/functions/openapi.yaml` 的 `/WEB-fetch` 端点）。支持 REST、MCP、OPAL 或 curl 协议。必需参数：`url`。可选参数：`headers`、`max_redirects`、`timeout_seconds`。`WEB_FETCH` 会像浏览器一样获取页面内容，并返回整个页面数据以供后续处理。具体调用方式请参考 [protocol-routing.md](./references/protocol-routing.md)。
2. **订阅源检测** — 检查页面中的 `<link rel="alternate">` 标签。如果已存在订阅源，则报告该信息并停止操作（可选择代理或镜像该订阅源）。
3. **帖子提取** — 使用 `references/extraction-rules.md` 中的规则来识别帖子信息（标题、URL、日期、作者、摘要）。
4. **订阅源生成** — 根据 `references/feed-templates.md` 中的模板构建XML结构，并使用 `references/validation-checklist.md` 进行验证。
5. **输出结果** — 将生成的XML内容以代码块的形式展示；可选择使用 `references/html-wrapper-template.md` 中的HTML模板进行包装。
6. **文件保存** — 将生成的 `.xml` 文件保存到 `/mnt/user-data/outputs/` 目录，并提供下载链接。

---

## 提取规则（详细规则请参见 references/）

### 需要关注的结构特征

- 包含重复出现的 `<article>`、`<li>` 或 `<div>` 块，且这些块具有统一的类名（例如 `post`、`entry`、`article`、`blog-post`、`card`）。
- 每个块内的 `<h1>`/`<h2>`/`<h3>` 标题 → 用于表示帖子标题。
- 标题附近或内部的 `<a href>` 链接 → 用于表示帖子链接（解析为相对URL）。
- 标签 `<time datetime="…">` 或符合日期格式的文本 → 用于表示发布日期。
- 每个块内的第一个 `<p>` 标签（长度不超过280个字符） → 用于表示帖子描述或摘要。
- 标签 `<span class="author">` 或作者署名 → 用于表示作者信息。

### 日期处理规则

- 如果页面中包含 `<time datetime="…">` 标签，直接使用其表示的日期。
- 对于可读的日期文本，使用符合RFC 822标准的格式进行解析。
- 如果未找到日期信息，使用当前日期（UTC时间）并添加注释 `<!-- estimated -->`。
- 对于相对日期（如“3天前”），根据抓取时间计算实际日期。

### URL规范化

所有帖子链接（`<link>` 标签）必须为 **绝对URL**。如果页面包含 `<base href>` 标签，则使用该地址进行解析；否则使用页面的原始URL进行解析。

---

## 订阅源格式规范

### RSS 2.0 必需元素

```
<rss version="2.0">
  <channel>
    <title>, <link>, <description>   ← required channel fields
    <item>
      <title>, <link>, <guid>        ← required per item
      <pubDate>                      ← RFC 822 (e.g. Mon, 01 Jan 2024 00:00:00 +0000)
      <description>                  ← plain text or CDATA-wrapped HTML
```

### Atom 1.0 必需元素

```
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>, <id>, <updated>           ← required feed fields
  <entry>
    <title>, <id>, <updated>         ← required per entry
    <link href="…" rel="alternate"/> ← post URL
    <summary> or <content>           ← excerpt or full body
```

完整模板请参见 `references/feed-templates.md`。

---

## 输出格式

| 格式                | 描述                                                         |
|-------------------|---------------------------------------------------------------------|
| `xml`                | 原始XML格式，以代码块形式展示                           |
| `file`                | 将XML文件保存到 `/mnt/user-data/outputs/<slug>-feed.xml` 并提供下载链接       |
| `html`                | 包含 `<link rel="alternate">` 标签的HTML页面                   |
| `both`                | 同时生成 `file` 和 `html` 文件（保存为 `<slug>-feed-page.html`）         |

默认输出格式为 `file`（生成XML文件并提供下载链接）。

---

## 错误处理

| 错误类型              | 处理方式                                      |
|-------------------|---------------------------------------------------------|
| 页面返回非200状态码        | 报告HTTP状态码，并建议用户检查URL或权限设置                |
| 未找到重复的帖子结构       | 显示原始HTML结构，并请求用户提供正确的帖子格式             |
| 订阅源已存在           | 报告现有订阅源的URL，并提供镜像或补充数据选项             |
| 日期格式无法解析         | 使用当前日期，并在XML中添加注释 `<!-- date-estimated -->`         |
| 相对URL无法解析         | 请求用户提供网站的基URL并进行解析                         |

---

## 命令行参数

| 命令                | 功能描述                                      |
|-------------------|---------------------------------------------------------|
| `/help`                | 提供该工具的使用说明                                  |
| `/format [rss|atom]`          | 设置输出格式（RSS或Atom）                         |
| `/limit [n]`            | 设置订阅源的最大条目数量                         |
| `/fulltext`            | 尝试获取每篇帖子的完整内容                         |
| `/validate`            | 运行 `references/validation-checklist.md` 中的验证规则         |
| `/preview`            | 先以Markdown格式显示前3条帖子内容，再展示XML格式         |

---

## 运行规则

- 在生成新的订阅源之前，务必检查是否存在已有的订阅源。
- 严禁伪造帖子内容，仅使用页面上实际存在的文本。
- 在文本节点中需要对 `&`、`<`、`>` 进行转义处理；HTML描述部分应使用 `CDATA` 标签。
- 所有的 `<guid>` 或 Atom `<id>` 值必须指向帖子的实际URL。
- 默认情况下，条目按发布日期降序排列（`pubDate` 降序）。
- 不要请求或存储用户的凭据；仅抓取公开可访问的页面内容。
- 明确标注生成的订阅源为合成内容（添加 `<generator>` 标签）。
- 遵守 `robots.txt` 文件的规则，不要抓取禁止爬虫访问的页面。