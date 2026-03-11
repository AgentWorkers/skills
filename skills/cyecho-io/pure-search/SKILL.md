---
name: pure-search
version: 1.0.0
description: "这是一个基于 DuckDuckGo 和 Trafilatura 的轻量级网络搜索工具，无需使用 API 密钥。该工具能够返回高度相关的网页链接以及格式清晰的 Markdown 内容。"
metadata: {"openclaw":{"emoji":"🔍","category":"search"}, "acceptLicenseTerms": true}
acceptLicenseTerms: true
---
# Pure Search 🔍

这是一个轻量级且功能强大的搜索工具，**无需任何API密钥**。它使用DuckDuckGo来获取链接，并通过`trafilatura`来提取干净、高质量的Markdown内容。

## 工作原理

1. 向DuckDuckGo查询前N个相关链接（绕过商业API的限制）。
2. 使用`trafilatura`仅提取网页的主要内容，去除导航栏、页脚、侧边栏和广告。
3. 返回包含搜索结果、标题、URL以及纯净Markdown内容的JSON格式数据。

## 设置

首先，请确保已安装所有依赖项：

```bash
pip install duckduckgo-search trafilatura
```

## 快速入门

```bash
# Basic search (Default fetches top 3 results)
./scripts/search.py "Rust vs Go in 2026"

# Advanced search with more results
./scripts/search.py "Latest AI trends" --max-results 5
```

## 输出格式

输出结果始终采用结构化的JSON格式，这使得代理程序能够非常容易地处理这些数据：

```json
{
  "query": "Rust vs Go in 2026",
  "results": [
    {
      "title": "A detailed comparison...",
      "url": "https://example.com/article",
      "markdown_content": "## Performance\n... (Pure clean text)"
    }
  ],
  "errors": []
}
```

## 为什么选择Pure Search？

- **零配置**：无需注册任何令牌即可立即使用。
- **极简设计**：仅依赖一个Python脚本，遵循“KISS”原则（Keep It Simple, Stupid）。
- **友好兼容性**：仅向大型语言模型（LLM）代理发送纯净的Markdown格式数据，避免HTML标签，从而节省上下文窗口的使用空间。