---
name: openai-docs-skill
description: 通过 OpenAI Docs MCP 服务器使用 CLI（curl/jq）查询 OpenAI 开发者文档。每当任务涉及 OpenAI API（响应、聊天完成、实时交互等）、OpenAI SDK、ChatGPT 应用 SDK、Codex、MCP 集成、端点架构、参数、限制或迁移，并且需要最新的官方指导时，请使用此方法。
---

# OpenAI 文档 MCP 技能

## 概述

通过 shell 使用 OpenAI 开发者文档 MCP 服务器来搜索和获取官方文档。在进行与 OpenAI 平台相关的工作时，务必使用此方法，而不要依赖记忆或非官方来源。

## 核心规则

- 在遇到与 OpenAI API/SDK/应用程序或 Codex 相关的问题时，或者需要精确、最新的文档时，始终使用此技能。
- 通过 `scripts/openai-docs-mcp.sh` 脚本中的 CLI 包装器来查询 MCP 服务器（不要使用 Codex MCP 工具）。
- 使用 `search` 或 `list` 命令找到最相关的文档页面，然后使用 `fetch` 命令获取该页面的内容。
- 在回复中务必提供所使用的文档 URL，以便明确来源。

## 快速入门

```bash
scripts/openai-docs-mcp.sh search "Responses API" 5
scripts/openai-docs-mcp.sh fetch https://platform.openai.com/docs/guides/migrate-to-responses
```

## 工作流程

1. 发现：使用具体的查询语句进行搜索；如果不确定，可以使用 `list` 命令浏览文档。
2. 阅读：使用 `fetch` 命令获取最相关的文档 URL（可选地指定文档的特定部分）。
3. 应用：总结或引用相关内容，并附上文档的 URL。

## 脚本参考

CLI 包装器位于 `scripts/openai-docs-mcp.sh`，它使用 `curl` 和 `jq` 命令与 `https://developers.openai.com/mcp` 进行交互。

可用命令：
- `init`：初始化并检查服务器功能。
- `tools`：列出 MCP 服务器上可用的工具。
- `search <query> [limit] [cursor]`：从文档索引中返回 JSON 格式的搜索结果。
- `list [limit] [cursor]`：浏览文档索引。
- `fetch <url> [anchor]`：获取文档页面或特定部分的 Markdown 内容。
- `endpoints`：列出 OpenAPI 端点。
- `openapi <endpoint-url> [lang1,lang2] [code-only]`：获取 OpenAPI 的接口描述或代码示例。

环境变量：
- `MCP_URL`：用于覆盖默认的 MCP 端点地址。