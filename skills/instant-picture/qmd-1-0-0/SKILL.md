---
name: qmd
description: 本地搜索/索引命令行工具（BM25算法 + 向量数据 + 重新排序功能），支持MCP模式。
homepage: https://tobi.lutke.com
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":["qmd"]},"install":[{"id":"node","kind":"node","package":"https://github.com/tobi/qmd","bins":["qmd"],"label":"Install qmd (node)"}]}}
---

# qmd

使用 `qmd` 对本地文件进行索引并搜索这些文件。

**索引操作：**
- 添加文件集合：`qmd collection add /path --name docs --mask "**/*.md"`
- 更新索引：`qmd update`
- 查看索引状态：`qmd status`

**搜索操作：**
- 使用 BM25 算法搜索：`qmd search "query"`
- 使用向量模型搜索：`qmd vsearch "query"`
- 混合搜索方式：`qmd query "query"`
- 获取文档内容：`qmd get docs/path.md:10 -l 40`

**注意事项：**
- 嵌入式模型/重新排序功能使用 Ollama（默认地址：`http://localhost:11434`）。
- 索引文件默认存储在 `~/.cache/qmd` 目录下。
- MCP 模式：`qmd mcp`