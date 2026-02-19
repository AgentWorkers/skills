---
name: web-markdown-navigator
description: 从网页中获取内容，并返回格式化后的 Markdown 文本（而非原始 HTML）。适用于需要 Markdown 格式输出的任务，如 URL 读取、数据提取和内容摘要生成。当网页依赖大量 JavaScript 或采用单页应用（SPA）架构时，如果提取的数据量较少，可优先使用浏览器原生功能进行数据提取。
---
# Web Markdown Navigator

此技能用于从指定的URL中提取Markdown内容。

## 使用流程

1. 运行脚本：
   - `cd /Users/pedrogonzalez/clawd/skills/web-markdown-navigator/scripts`
   - `node fetch-markdown.mjs "<url>" --max-chars 50000`
2. 如果脚本的退出代码为`0`，则返回提取到的Markdown内容。
3. 如果退出代码为`3`或`4`，或者提取到的内容过于简短（缺乏实质性内容），则使用`browser`工具作为备用方案来捕获页面的渲染结果，并返回该内容的Markdown摘要。

## 脚本说明

`node scripts/fetch-markdown.mjs <url> [--max-chars N] [--timeout-ms N] [--json]`

**工作原理：**
- 第一层：获取HTML内容，并使用Mozilla Readability插件进行格式化处理，随后将其转换为Markdown格式。
- 第二层：如果提取到的Markdown内容过于简短或缺乏实质性内容，会自动切换为纯文本格式的Markdown。

**注意事项：**
- 脚本会自动过滤掉本地主机（`localhost`）和私有IPv4地址的URL。

## 输出要求：
- 仅返回Markdown格式的内容（不包括原始的HTML代码）。
- 响应中必须包含原始URL。
- 如果提取的内容被截断，需要注明截断的原因。
- 如果使用了备用方案（`readability`或`fallback-text`），也需要在输出中说明。

## 错误处理：
- `1`：参数错误。
- `2`：URL无效或被屏蔽。
- `3`：网络问题或获取内容时出现错误。
- `4`：提取失败或提取到的内容过于简短。

**扩展说明与故障排除：**
- 详细的使用说明和故障排除信息请参阅：
- `/Users/pedrogonzalez/clawd/skills/web-markdown-navigator/references/usage.md`