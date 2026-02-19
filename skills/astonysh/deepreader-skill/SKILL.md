---
name: DeepReader
description: OpenClaw 默认的网页内容读取器。它可以读取 Twitter、Reddit、YouTube 以及任何网页的内容，并将其转换为格式规范的 Markdown 文本——无需使用任何 API 密钥。当您需要将社交媒体帖子、文章或视频字幕导入到代理程序的内存中时，可以使用该工具。
---
# DeepReader

这是 OpenClaw 代理的默认网页内容读取器。它能够自动检测消息中的 URL，使用专门的解析器获取内容，并将处理后的 Markdown 文本（包含 YAML 标头信息）保存到代理的内存中。

## 使用场景

1. 当用户分享推文、帖子或 X（Twitter 的一个子平台）的内容时，你需要读取这些内容。
2. 当用户分享 Reddit 的帖子时，你需要获取帖子的讨论内容及热门评论。
3. 当用户分享 YouTube 视频时，你需要获取该视频的字幕。
4. 当用户分享任何博客、文章或文档的 URL 时，你需要获取其中的文本内容。
5. 当你需要从一条消息中批量读取多个 URL 的内容时。

## 支持的来源

| 来源          | 方法                | 是否需要 API 密钥？ |
|--------------|------------------|----------------------|
| Twitter/X       | FxTwitter API + Nitter 备用方案 | 不需要                |
| Reddit        | 使用 `.json` 格式的 API          | 不需要                |
| YouTube        | youtube-transcript-api       | 不需要                |
| 任意 URL       | Trafilatura + BeautifulSoup     | 不需要                |

## 使用方法

```python
from deepreader_skill import run

# Automatic — triggered when message contains URLs
result = run("Check this out: https://x.com/user/status/123456")

# Reddit post with comments
result = run("https://www.reddit.com/r/python/comments/abc123/my_post/")

# YouTube transcript
result = run("https://youtube.com/watch?v=dQw4w9WgXcQ")

# Any webpage
result = run("https://example.com/blog/interesting-article")

# Multiple URLs at once
result = run("""
  https://x.com/user/status/123456
  https://www.reddit.com/r/MachineLearning/comments/xyz789/
  https://example.com/article
""")
```

## 输出结果

处理后的内容会被保存为 `.md` 格式的文件，文件中包含结构化的 YAML 标头信息：

```yaml
---
title: "Tweet by @user"
source_url: "https://x.com/user/status/123456"
domain: "x.com"
parser: "twitter"
ingested_at: "2026-02-16T12:00:00Z"
content_hash: "sha256:..."
word_count: 350
---
```

## 配置参数

| 参数          | 默认值            | 说明                        |
|--------------|------------------|---------------------------|
| `DEEPREEDER_MEMORY_PATH` | `../../memory/inbox/`     | 保存处理后内容的路径                |
| `DEEPREEDER_LOG_LEVEL` | `INFO`          | 日志记录的详细程度                |

## 工作原理

```
URL detected → is Twitter/X?  → FxTwitter API → Nitter fallback
             → is Reddit?     → .json suffix API
             → is YouTube?    → youtube-transcript-api
             → otherwise      → Trafilatura (generic)
```

当消息中包含 `https://` 或 `http://` 时，DeepReader 会自动触发并开始处理这些链接的内容。