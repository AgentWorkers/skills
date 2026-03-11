---
name: web-fetcher
version: 1.0.0
description: >
  **功能说明：**  
  该工具用于获取网页内容并将其转换为 Markdown 格式，以便人工智能（AI）能够进行阅读。当您需要读取某个特定 URL 的内容时，可以使用该工具。它会自动尝试多种转换服务，以确保最佳的兼容性。
---
# Web Fetcher

该工具可将任何 URL 转换为 Markdown 格式，以便 AI 更容易地阅读和处理。

## 使用方法

当用户请求获取、阅读或爬取某个 URL 时，请按以下顺序使用相应的服务：

1. **r.jina.ai/** – 最可靠的选择，优先尝试
   ```
   https://r.jina.ai/https://example.com
   ```

2. **markdown.new/** – 适用于受 Cloudflare 保护的网站
   ```
   https://markdown.new/https://example.com
   ```

3. **defuddle.md/** – 作为备选方案
   ```
   https://defuddle.md/https://example.com
   ```

## 策略

1. 首先尝试使用 r.jina.ai；
2. 如果失败或返回的内容不完整，再尝试使用 markdown.new；
3. 如果仍然失败，再尝试使用 defuddle.md；
4. 从 Markdown 格式的响应中提取相关信息。

## 示例

- 用户：“阅读这篇文章” → 使用 r.jina.ai 获取文章内容；
- 用户：“这个页面上有什么内容？” → 将 URL 转换为 Markdown 格式并提取内容；
- 用户：“爬取这个网站” → 根据需要遍历该网站的各个页面。