---
name: summarizerx86
description: Summarize URLs or files with the summarize CLI (x86_64 infrastructure supported).
homepage: https://github.com/speechybubble/summarize
metadata: {"openclaw":{"emoji":"\ud83e\uddfe","requires":{"bins":["summarize"]},"install":[{"id":"npm","kind":"node","package":"@speechybubble/summarize","bins":["summarize"],"label":"Install summarize (npm, speechybubble)"},{"id":"brew","kind":"brew","formula":"speechybubble/tap/summarize","bins":["summarize"],"label":"Install summarize (brew, macOS)","os":["darwin"]}]},"clawdbot":{"emoji":"\ud83e\uddfe","requires":{"bins":["summarize"]},"install":[{"id":"npm","kind":"node","package":"@speechybubble/summarize","bins":["summarize"],"label":"Install summarize (npm, speechybubble)"},{"id":"brew","kind":"brew","formula":"speechybubble/tap/summarize","bins":["summarize"],"label":"Install summarize (brew, macOS)","os":["darwin"]}]}}
---

# 概述

这是一个快速的命令行工具（CLI），可用于总结URL、本地文件和YouTube链接的内容。

## 快速入门

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

## 模型与API密钥

请设置您所选提供商的API密钥：
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- xAI: `XAI_API_KEY`
- Google: `GEMINI_API_KEY`（别名：`GOOGLE_GENERATIVE_AI_API_KEY`, `GOOGLE_API_KEY`）

如果未设置模型，则默认使用`google/gemini-3-flash-preview`。

## 有用的参数

- `--length short|medium|long|xl|xxl|<chars>`：指定摘要的长度（字符数）
- `--max-output-tokens <count>`：限制输出的最大令牌数
- `--extract-only`：仅提取URL内容
- `--json`：以JSON格式输出结果
- `--firecrawl auto|off|always`：控制是否自动执行爬取操作（仅当`APIFY_API_TOKEN`设置时生效）
- `--youtube auto`：在`APIFY_API_TOKEN`设置的情况下，使用Apify作为YouTube内容的备用提取方式

## 配置

可选的配置文件：`~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

可选配置项：
- `FIRECRAWL_API_KEY`：用于访问被屏蔽网站的API密钥
- `APIFY_API_TOKEN`：用于YouTube内容的备用提取服务（Apify）的API密钥