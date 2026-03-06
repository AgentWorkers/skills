---
name: jina-reader
description: 使用 Jina.ai Reader 从任何 URL 获取干净、适合 AI 处理的 Markdown 内容。该工具可以绕过付费墙，处理 Twitter/X 的帖子，渲染包含大量 JavaScript 的页面，并返回带有标题和元数据的结构化内容。当您需要在搜索后从网页中读取或提取内容，或者处理需要 JavaScript 渲染的付费网站、Twitter/X 页面或单页应用程序（SPA）时，可以使用此工具。
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["node"]}}}
---
# Jina.ai Reader

从任何 URL 获取干净、适合 AI 处理的 Markdown 内容。无需 API 密钥。

## 特点

- ✅ 可绕过付费墙（已在 Every.to、Medium 等网站上进行测试）
- ✅ 支持 Twitter/X 的帖子和话题
- ✅ 可渲染包含大量 JavaScript 的页面（可选：等待 JavaScript 加载完成）
- ✅ 返回格式规范的 Markdown 内容
- **免费使用，无需 API 密钥**

## 基本用法

```bash
node {baseDir}/scripts/jina-reader.mjs "https://example.com/article"
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `--wait-ms N` | 等待 JavaScript 加载完成 N 毫秒 |
| `--with-images` | 在输出中包含图片标题 |
| `--with-links` | 在输出中包含所有链接 |

## 示例

```bash
# Basic fetch
node {baseDir}/scripts/jina-reader.mjs "https://every.to/article"

# Twitter/X post
node {baseDir}/scripts/jina-reader.mjs "https://twitter.com/user/status/123456"

# Wait for JavaScript rendering
node {baseDir}/scripts/jina-reader.mjs "https://spa-site.com/page" --wait-ms 5000

# With images and links
node {baseDir}/scripts/jina-reader.mjs "https://blog.example.com/post" --with-images --with-links
```

## 使用场景

- **搜索后阅读**：在 Tavily/desearch 找到 URL 后，使用该工具阅读实际内容
- **Twitter/X**：大多数工具无法处理 Twitter 的内容，但 Jina.ai 可以
- **需要登录的网站**：适用于许多需要登录的网站
- **包含大量 JavaScript 的页面**：使用 `--wait-ms` 选项等待脚本加载完成

## 注意事项

- 无需 API 密钥
- 高频使用可能会受到速率限制
- 对于分页内容，可能需要手动获取多页数据