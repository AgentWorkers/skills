---
name: crawl-for-ai
description: 使用本地的 Crawl4AI 实例进行网页抓取。该工具适用于获取包含 JavaScript 渲染内容的完整页面，对于结构复杂的网页来说比 Tavily 更为高效。支持无限次使用。
version: 1.0.1
author: Ania
requiresEnv:
  - CRAWL4AI_URL
metadata:
  clawdbot:
    emoji: "🕷️"
    requires:
      bins: ["node"]
---
# Crawl4AI 网页抓取工具

这是一个用于提取完整网页内容的本地 Crawl4AI 实例，支持 JavaScript 的渲染功能。

## 端点（Endpoints）

**代理（端口 11234）** — 提供清洗后的输出结果，兼容 OpenWebUI
- 返回值：`[{page_content, metadata}]`
- 适用场景：简单的内容提取

**直接访问（端口 11235）** — 提供包含所有数据的完整输出结果
- 返回值：`{results: [{markdown, html, links, media, ...}]}`
- 适用场景：需要获取链接、媒体内容或其他元数据时使用

## 使用方法（Usage）

```bash
# Via script
node {baseDir}/scripts/crawl4ai.js "url"
node {baseDir}/scripts/crawl4ai.js "url" --json
```

**脚本选项（Script options）：**
- `--json` — 以 JSON 格式返回完整数据

**输出结果（Output）：** 从网页中提取的清洗后的 Markdown 内容。

## 配置（Configuration）

**必需的环境变量：**
- `CRAWL4AI_URL` — 你的 Crawl4AI 实例的 URL（例如：`http://localhost:11235`）

**可选（Optional）：**
- `CRAWL4AI_KEY` — 如果你的实例需要身份验证，请设置此 API 密钥

## 主要特点（Features）：**
- **JavaScript 渲染**：能够处理动态内容
- **无限使用次数**：作为本地实例，没有 API 使用次数限制
- **完整内容提取**：包括 HTML、Markdown、链接、媒体文件等
- **对于包含 JavaScript 的复杂网页，性能优于 Tavily**

## API 接口（API）**

该工具使用你的本地 Crawl4AI 实例的 REST API。只有当设置了 `CRAWL4AI_KEY` 时，才会发送身份验证请求头。