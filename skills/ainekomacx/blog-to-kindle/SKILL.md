---
name: blog-to-kindle
description: 该工具可用于抓取博客或文章网站的内容，并将其编译成适合在 Kindle 上阅读的 EPUB 格式电子书。同时，该工具还支持自动生成电子书的封面图片。具体应用场景包括：将博客内容下载到 Kindle 设备上阅读、将文章转换为电子书格式、或将博客存档发送到 Kindle。目前支持的网站包括 Paul Graham、Kevin Kelly、Derek Sivers、Wait But Why、Astral Codex Ten 以及用户自定义的网站。
---

# 将博客内容转换为Kindle格式

该工具可以从博客或文章网站抓取内容，将其编译成带有封面图片的EPUB格式文件，并发送到用户的Kindle设备上。

## 快速入门

```bash
# 1. Fetch essays from a supported site
uv run scripts/fetch_blog.py --site paulgraham --output ./pg-essays

# 2. Generate cover (uses Nano Banana Pro)
# See nano-banana-pro skill for cover generation

# 3. Compile to EPUB with cover
uv run scripts/compile_epub.py --input ./pg-essays --cover ./cover.png --output essays.epub

# 4. Send to Kindle
uv run scripts/send_to_kindle.py --file essays.epub --kindle-email user@kindle.com
```

## 工作流程（必须按照以下顺序执行）：

1. **获取数据**：从博客网站下载所有文章或帖子。
2. **生成封面图片**：使用`nano-banana-pro`技能生成封面图片（此步骤必不可少）。
3. **编译文件**：将所有内容合并成包含封面图片的EPUB格式文件。
4. **发送文件**：通过电子邮件将EPUB文件发送到用户的Kindle邮箱地址。

⚠️ **发送文件前必须先生成并添加封面图片。** 严禁在没有封面图片的情况下发送文件。

## 支持的网站列表

| 网站名称 | 关键字 | 网址模式 |
|------|-----|-------------|
| Paul Graham | `paulgraham` | paulgraham.com/articles.html |
| Kevin Kelly | `kevinkelly` | kk.org/thetechnium |
| Derek Sivers | `sivers` | sive.rs/blog |
| Wait But Why | `waitbutwhy` | waitbutwhy.com/archive |
| Astral Codex Ten | `acx` | astralcodexten.com |

对于未列出的网站，可以使用`--site custom --url <archive-url>`参数进行自定义操作。

## 封面图片生成

使用`nano-banana-pro`技能生成封面图片。模板提示如下：

```
Book cover for '[Author Name]: [Subtitle]'. 
Minimalist design with elegant typography. 
[Brand color] accent. Clean white/cream background. 
Simple geometric or abstract motif related to [topic].
Professional literary feel. No photos, no faces.
Portrait orientation book cover dimensions.
```

建议生成2K分辨率的封面图片，以确保图片质量的同时文件大小不会过大。

## Kindle文件发送

默认的Kindle发送地址（Simon）：`simonpilkington74_8oVjpj@kindle.com`

通过AppleScript使用Mail.app发送文件。请确保：
- 发件人的电子邮件地址在Kindle的允许发送列表中。
- 文件大小不超过50MB（EPUB格式文件通常压缩效果较好）。

## 状态跟踪

相关状态文件存储在`~/.clawdbot/state/blog-kindle/`目录下：
- `{site}-last-fetch.json`：最后一次数据获取的时间戳及文章数量。
- `{site}-sent.json`：已发送文章的ID列表。

该目录用于实现增量更新（仅获取新发布的文章）。

## 手动工作流程（无需脚本）

如果无法使用脚本，可以按照以下步骤操作：

1. **获取数据**：使用curl命令访问网站档案页面，解析文章链接，然后逐一下载文章内容。
2. **合并内容**：将下载到的Markdown格式文章与包含标题、作者信息的YAML元数据合并。
3. **生成封面图片**：使用`nano-banana-pro`技能生成封面图片。
4. **转换文件**：使用`pandoc`命令将合并后的Markdown文件转换为EPUB格式（命令示例：`pandoc combined.md -o output.epub --epub-cover-image=cover.png --toc`）。
5. **发送文件**：通过AppleScript的Mail.app应用程序发送文件，并附加EPUB文件。

详细操作步骤请参阅`references/manual-workflow.md`文件。