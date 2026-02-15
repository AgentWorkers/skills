---
name: bearblog
description: 在 Bear Blog (bearblog.dev) 上创建和管理博客文章。支持扩展的 Markdown 格式、自定义属性以及基于浏览器的发布功能。
metadata: {"clawdbot":{"emoji":"🐻","homepage":"https://bearblog.dev","requires":{"config":["browser.enabled"]}}}
---

# Bear Blog 使用技巧

在 [Bear Blog](https://bearblog.dev) 上创建、编辑和管理文章——这是一个简洁、快速的博客平台。

## 认证

Bear Blog 需要基于浏览器的认证。通过浏览器工具登录一次后，cookie 将会持续有效。

```
browser action:navigate url:https://bearblog.dev/accounts/login/
```

## 创建文章

### 第一步：导航到文章编辑器

```
browser action:navigate url:https://bearblog.dev/<subdomain>/dashboard/posts/new/
```

### 第二步：填写编辑器内容

Bear Blog 使用 **纯文本标题格式**。

编辑器字段包括：
- `div#header_content`（可编辑内容）：属性（每行一个）
- `textarea#body_content`：Markdown 正文

**注意：** 对这两个字段使用 `fill`/`type` 方法进行填充，然后点击 **发布**（或 **保存为草稿**）。无需使用 `evaluate` 方法。

**标题格式：**
```
title: Your Post Title
link: custom-slug
published_date: 2026-01-05 14:00
tags: tag1, tag2, tag3
make_discoverable: true
is_page: false
class_name: custom-css-class
meta_description: SEO description for the post
meta_image: https://example.com/image.jpg
lang: en
canonical_url: https://original-source.com/post
alias: alternative-url
```

**正文格式：** 标准 Markdown，支持扩展语法（详见下文）。

模板中使用 `___`（三个下划线）来分隔标题和正文。

### 第三步：发布

点击发布按钮，或通过 `publish: true` 提交表单。

## 文章属性参考

| 属性 | 描述 | 示例 |
|-----------|-------------|---------|
| `title` | 文章标题（必填） | `title: 我的文章` |
| `link` | 自定义 URL 缩写 | `link: my-custom-url` |
| `published_date` | 发布日期/时间 | `published_date: 2026-01-05 14:30` |
| `tags` | 用逗号分隔的标签 | `tags: tech, ai, coding` |
| `make_discoverable` | 是否显示在发现页面中 | `make_discoverable: true` |
| `is_page` | 静态页面还是博客文章 | `is_page: false` |
| `class_name` | 自定义 CSS 类名（使用缩写形式） | `class_name: featured` |
| `meta_description` | SEO 元描述 | `meta_description: 一篇关于...的文章` |
| `meta_image` | Open Graph 图片 URL | `meta_image: https://...` |
| `lang` | 语言代码 | `lang: fr` |
| `canonical_url` | SEO 用的规范 URL | `canonical_url: https://...` |
| `alias` | 替代 URL 路径 | `alias: old-url` |

## 扩展 Markdown 语法

Bear Blog 使用 [Mistune](https://github.com/lepture/mistune) 及其插件：

### 文本格式
- `~~strikethrough~~` → **删除线**
- `^superscript^` → 上标
- `~subscript~` → 下标
- `==highlighted==` → **高亮显示**
- `**bold**` 和 `*italic*` — **粗体** 和 **斜体**

### 脚注
```markdown
Here's a sentence with a footnote.[^1]

[^1]: This is the footnote content.
```

### 任务列表
```markdown
- [x] Completed task
- [ ] Incomplete task
```

### 表格
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
```

### 代码块
````markdown
```python
def hello():
    print("Hello, world!")
```
```

代码块使用 Pygments 进行语法高亮（在代码块前指定语言，例如：````python`）。

### 数学公式（LaTeX）
- **内联公式**：`$E = mc^2$
- **块级公式**：`$$\int_0^\infty e^{-x^2} dx$$`

### 缩写词
```markdown
*[HTML]: Hypertext Markup Language
The HTML specification is maintained by the W3C.
```

### 警告提示
```markdown
.. note::
   This is a note admonition.

.. warning::
   This is a warning.
```

### 目录
```markdown
.. toc::
```

## 动态变量

在内容中可以使用 `{{ variable }}`：

### 博客变量
- `{{ blog_title }}` — 博客标题
- `{{ blog_description }}` — 博客元描述
- `{{ blog_created_date }}` — 博客创建日期
- `{{ blog_last_modified }}` — 最后修改时间
- `{{ blog_last_posted }}` — 最后发布时间
- `{{ blog_link }}` — 博客完整 URL
- `{{ tags }}` — 带链接的标签列表

### 文章变量（在文章模板中）
- `{{ post_title }}` — 当前文章标题
- `{{ post_description }}` — 文章元描述
- `{{ post_published_date }}` — 发布日期
- `{{ post_last_modified }}` — 最后修改时间
- `{{ post_link }}` — 文章完整 URL
- `{{ next_post }}` — 下一篇文章链接
- `{{ previous_post }}` — 上一篇文章链接

### 文章列表
```markdown
{{ posts }}
{{ posts limit:5 }}
{{ posts tag:"tech" }}
{{ posts tag:"tech,ai" limit:10 order:asc }}
{{ posts description:True image:True content:True }}
```

参数：
- `tag:` — 通过逗号分隔的标签进行过滤
- `limit:` — 文章数量上限
- `order:` — `asc` 或 `desc`（默认：desc）
- `description:True` — 显示元描述
- `image:True` — 显示元图片
- `content:True` — 显示全文（仅限页面显示）

### 电子邮件注册（仅限高级博客）
```markdown
{{ email-signup }}
{{ email_signup }}
```

## 链接

### 标准链接
```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Title text")
```

### 在新标签页中打开链接
在链接前加上 `tab:` 前缀：
```markdown
[External link](tab:https://example.com)
```

### 标题链接
标题会自动转换为 slug 形式的 ID：
```markdown
## My Section Title
```
例如：`#my-section-title`

## 排版格式

Markdown 支持以下自动替换：
- `(c)` → ©
- `(C)` → ©
- `(r)` → ®
- `(R)` → ®
- `(tm)` → ™
- `(TM)` → ™
- `(p)` → ℗
- `(P)` → ℗
- `+-` → ±

## 原始 HTML

Markdown 直接支持 HTML 格式：

```html
<div class="custom-class" style="text-align: center;">
  <p>Centered content with custom styling</p>
</div>
```

**注意：** 对于免费账户，`<script>`, `<object>`, `<embed>`, `<form>` 等标签会被删除。IFrame 只允许来自以下来源：
- youtube.com, youtube-nocookie.com
- vimeo.com
- soundcloud.com
- spotify.com
- codepen.io
- google.com（文档、驱动、地图）
- bandcamp.com
- apple.com（音乐嵌入）
- archive.org
- 以及更多...

## 仪表盘 URL

将 `<subdomain>` 替换为你的博客子域名：

- **博客列表：** `https://bearblog.dev/dashboard/`
- **仪表盘：** `https://bearblog.dev/<subdomain>/dashboard/`
- **文章列表：** `https://bearblog.dev/<subdomain>/dashboard/posts/`
- **新建文章：** `https://bearblog.dev/<subdomain>/dashboard/posts/new/`
- **编辑文章：** `https://bearblog.dev/<subdomain>/dashboard/posts/<uid>/`
- **样式：** `https://bearblog.dev/<subdomain>/dashboard/styles/`
- **导航：** `https://bearblog.dev/<subdomain>/dashboard/nav/`
- **分析：** `https://bearblog.dev/<subdomain>/dashboard/analytics/`
- **设置：** `https://bearblog.dev/<subdomain>/dashboard/settings/`

## 示例：完整文章

**标题内容：**
```
title: Getting Started with AI Assistants
link: ai-assistants-intro
published_date: 2026-01-05 15:00
meta_description: A beginner's guide to working with AI assistants
tags: ai, tutorial, tech
is_page: false
lang: en
```

**正文内容：**
```markdown
AI assistants are changing how we work. Here's what you need to know.

## Why AI Assistants?

They help with:
- [x] Writing and editing
- [x] Research and analysis
- [ ] Making coffee (not yet!)

> "The best tool is the one you actually use." — Someone wise

## Getting Started

Check out [OpenAI](tab:https://openai.com) or [Anthropic](tab:https://anthropic.com) for popular options.

---

*What's your experience with AI? Let me know!*

{{ previous_post }} {{ next_post }}
```

## 使用技巧

1. **发布前预览** — 使用预览按钮检查格式。
2. **使用模板** — 在仪表盘设置中配置文章模板，以保持标题的一致性。
3. **安排文章发布时间** — 设置未来的发布日期。
4. **草稿模式** — 点击“发布”时选择“保存为草稿”。
5. **自定义 CSS** — 为文章添加 `class_name` 并在博客的 CSS 中进行样式设置。
6. **SEO** — 确保设置 `meta_description` 和 `meta_image`。

## 故障排除

- **文章未显示？** 检查 `publish` 状态和 `published_date`。
- **标签无法使用？** 使用逗号分隔标签，不要使用引号。
- **样式问题？** 确保 `class_name` 使用了正确的 slug 形式（小写，使用连字符）。
- **日期格式错误？** 使用 `YYYY-MM-DD HH:MM` 格式。