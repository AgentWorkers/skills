# Web搜索与研究MCP

该MCP为AI代理提供了全面的网络浏览、搜索和研究功能，包括PDF提取、YouTube视频字幕提取、文本摘要生成以及语义搜索等功能。

## 概述

该MCP为AI代理提供了与网络交互的一整套工具：
- 集成了Google搜索功能
- 可从网页中提取文本内容
- 能够从网页中提取链接
- 可从PDF文档中提取文本
- 可获取YouTube视频的字幕
- 支持文本摘要生成
- 提供文本嵌入和语义搜索功能
- 支持自动化研究工作流程

## 主要功能

- **搜索**：执行Google搜索并获取结构化搜索结果
- **页面提取**：从网页中提取纯净的文本内容
- **链接提取**：从网页中获取所有链接
- **PDF处理**：从PDF文档中提取文本
- **YouTube字幕**：获取YouTube视频的字幕
- **摘要生成**：生成文本内容的简洁摘要
- **文本嵌入**：使用语义嵌入技术存储和搜索文本
- **研究**：支持自动化多步骤研究工作流程

## 提供的工具

- `search`：执行Google搜索并返回结果
- `open_page`：从网页中提取文本
- `extract_links`：从网页中提取链接
- `extract_pdf`：从PDF文件中提取文本
- `youtube_transcript`：获取YouTube视频的字幕
- `summarize`：生成文本内容的摘要
- `embed`：使用语义嵌入技术存储文本
- `semantic_search`：搜索存储的文本嵌入数据
- `research`：执行自动化研究任务

## 安装

```bash
npm install
```

## 使用方法

运行MCP服务器：
```bash
node index.js <tool_name> <json_input>
```

示例：
```bash
node index.js search '{"query":"artificial intelligence"}'
```

## 所需依赖库

- axios：用于发送HTTP请求
- cheerio：用于解析HTML文档
- natural：用于文本处理
- pdf-parse：用于从PDF文件中提取文本
- youtube-transcript：用于获取YouTube视频的字幕