---
name: summarize
description: 使用 `summarize` CLI 工具可以总结 URL 或文件的内容（包括网页、PDF 文件、图片、音频文件以及 YouTube 视频）。
homepage: https://summarize.sh
metadata: {"clawdbot":{"emoji":"🧾","requires":{"bins":["summarize"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/summarize","bins":["summarize"],"label":"Install summarize (brew)"}]}}
---

# 概述

这是一个快速的命令行工具（CLI），用于总结URL、本地文件和YouTube链接的内容。

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

如果未设置模型，则默认使用 `google/gemini-3-flash-preview`。

## 有用的参数

- `--length short|medium|long|xl|xxl|<chars>`：指定摘要的长度（字符数）
- `--max-output-tokens <count>`：限制输出的最大token数
- `--extract-only`：仅提取URL内容
- `--json`：以机器可读的JSON格式输出结果
- `--firecrawl auto|off|always`：控制是否自动执行网络爬取（作为备用选项）
- `--youtube auto`：在设置了 `APIFY_API_TOKEN` 时，使用Apify作为YouTube内容的备用来源

## 配置

可选配置文件：`~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

可选配置项：
- `FIRECRAWL_API_KEY`：用于访问被屏蔽的网站
- `APIFY_API_TOKEN`：作为YouTube内容的备用访问令牌