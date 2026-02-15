---
name: hn-extract
description: 将 HackerNews 上的一篇文章及其评论提取为简洁的 Markdown 格式，以便快速阅读或输入到大型语言模型（LLM）中。
metadata:  {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://github.com/guoqiao/skills/blob/main/hn-extract/hn-extract/SKILL.md","os":["darwin","linux","win32"],"tags":["hn","hackernews","comments","extract","markdown","python","uv","scraper","rss","reader","summarize"],"requires":{"bins":["uv"]}}}
---

# HackerNews 提取工具

该工具可以将 HackerNews 的一篇文章及其评论提取为格式良好的 Markdown 文件，便于快速阅读或输入到大型语言模型（LLM）中。

**参考示例**：[https://github.com/guoqiao/skills/blob/main/hn-extract/examples](https://github.com/guoqiao/skills/blob/main/hn-extract/examples)

## 功能概述：
- 接受 HackerNews 的文章 ID 或 URL 作为输入。
- 下载对应的 HTML 文件，对其进行清洗和格式化处理。
- 获取文章的元数据和评论信息。
- 输出一个包含原始文章、按主题排序的评论以及关键元数据的可读性强的 Markdown 文件。

## 系统要求：
- 必须安装 `uv` 并将其添加到系统的 PATH 环境变量中。

## 安装说明：
无需额外安装其他软件；只需确保 `uv` 已安装即可。运行此脚本时，`uv` 会自动在虚拟环境（venv）中安装所需的依赖项。

## 使用流程（代理程序必须遵循）：
当代理程序被要求提取 HackerNews 文章时，请按照以下步骤操作：
1. **运行脚本**，并指定输出路径：`uv run --script ${baseDir}/hn-extract.py <input> -o /tmp/hn-<id>.md`。
2. **发送一条合并消息**：在同一请求中上传生成的 Markdown 文件并提出问题。可以使用 `message` 工具（设置 `action=send`、`filePath="/tmp/hn-<id>.md"`、`message="提取完成。需要我为您总结内容吗？"`）。
3. **除非特别要求，否则不要在聊天界面直接显示文章全文或摘要**。

## 其他使用方式：
- 如果省略 `-o` 选项，脚本会将结果输出到标准输出（stdout）。
- `-o` 选项指定的目录会自动创建。

**注意事项**：
- 支持对 HTTP 请求进行重试。
- 评论会根据其所属的讨论线程深度进行缩进显示。
- 部分网站可能需要身份验证；如果网站禁止爬取，提取操作可能会失败。