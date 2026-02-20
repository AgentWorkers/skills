---
name: coala-client
description: >
  如何使用 coala-client CLI 与大型语言模型（LLMs）、MCP 服务器以及各种技能进行交互？  
  当用户询问如何使用 coala、启动 coala 聊天功能、添加 MCP 服务器、导入 CWL 工具集、列出或调用 MCP 工具，或导入/加载技能时，可以使用该 CLI。
homepage: https://github.com/coala-info/coala_client
metadata: {"clawdbot":{"emoji":"🧬","requires":{"bins":["coala-client"]},"install":[{"id":"uv","kind":"uv","package":"coala-client","bins":["coala-client"],"label":"Install coala-client (uv)"}]}}
---
# Coala 客户端

Coala 生态系统的一部分，这是一个命令行工具（CLI），用于与兼容 OpenAI 的大型语言模型（如 OpenAI、Gemini、Ollama）以及 MCP（Model Context Protocol）服务器进行聊天。该客户端支持将 CWL（Common Workflow Language）工具集导入作为 MCP 服务器，并支持导入各种技能。

## 配置路径

- MCP 配置和工具集：`~/.config/coala/mcps/`
  - `mcp_servers.json` — 服务器定义文件
  - `<toolset>/` — 各工具集的目录，其中包含 `run_mcp.py` 文件和 CWL 文件
- 技能：`~/.config/coala/skills/`（每个导入的来源对应一个子文件夹）
- 环境变量：`~/.config/coala/env`（可选；用于存储提供商和 MCP 的环境变量，格式为键=值）

## 快速入门

1. **首次初始化**
   `coala init` — 创建 `~/.config/coala/mcps/mcp_servers.json` 和 `env` 文件。

2. **设置 API 密钥**
   例如：`export OPENAI_API_KEY=...` 或 `export GEMINI_API_KEY=...`。Ollama 不需要 API 密钥。

3. **聊天**
   `coala` 或 `coala chat` — 与 MCP 工具进行交互式聊天。
   `coala ask "question"` — 向 MCP 提出问题。

4. **选项**
   `-p, --provider`（openai|gemini|ollama|custom） — 指定使用哪个提供商
   `-m, --model` — 指定使用哪个模型
   `--no-mcp` — 禁用 MCP 功能

## MCP：CWL 工具集

导入、列出或调用 MCP 工具集时不需要 API 密钥，这些操作仅用于与大型语言模型进行聊天或提问。

- **导入**（将工具集导入到 `~/.config/coala/mcps/<TOOLSET>/` 并注册服务器）：
  `coala mcp-import <TOOLSET> <SOURCES...>` 或使用别名 `coala mcp ...`
  `SOURCES`：本地 `.cwl` 文件、`.zip` 文件，或指向 `.cwl` 或 `.zip` 文件的 HTTP URL。
  需要安装 `coala` 包（其中包含 `run_mcp.py` 文件）。

- **列出**：
  `coala mcp-list` — 列出所有可用的服务器名称。
  `coala mcp-list <SERVER_NAME>` — 显示每个服务器的详细信息（名称、描述、输入格式）。

- **调用**：
  `coala mcp-call <SERVER>.<TOOL> --args '<JSON>'`
  例如：`coala mcp-call gene-variant.ncbi_datasets_gene --args '{"data": [{"gene": "TP53", "taxon": "human"}]}'`

## 技能

- **导入**（将技能导入到 `~/.config/coala/skills/`，每个来源对应一个子文件夹）：
  `coala skill <SOURCES...>`
  `SOURCES`：GitHub 仓库的树形结构 URL（例如 `https://github.com/owner/repo/tree/main/skills`）、ZIP 文件路径，或本地 ZIP 文件目录。

- **在聊天中使用技能**：
  `/skill` — 列出已安装的技能。
  `/skill <name>` — 从 `~/.config/coala/skills/<name>/`（例如 SKILL.md 文件）加载特定技能到当前对话中。

## 聊天命令

- `/help` — 显示帮助信息
- `/exit` — 退出程序
- `/quit` — 强制退出
- `/clear` — 清除聊天记录
- `/tools` — 列出所有可用的 MCP 工具
- `/servers` — 列出已连接的 MCP 服务器
- `/skill` — 列出所有技能；`/skill <name>` — 加载指定的技能
- `/model` — 显示当前使用的模型信息
- `/switch <provider>` — 切换使用的提供商

## 控制 MCP 功能的开关

- **关闭所有 MCP 服务器**：
  `coala --no-mcp` （或 `coala ask "..." --no-mcp`）
- **关闭单个服务器**：从 `~/.config/coala/mcp_servers.json` 中删除该服务器的记录。
- **启用 MCP 服务器**：默认情况下，如果不使用 `--no-mcp` 选项，则所有服务器都会被启用；可以通过 `mcp_servers.json` 文件添加或恢复服务器。

## 提供商和环境设置

- 通过 `-p` 参数或环境变量 `PROVIDER` 设置提供商。
- 为每个提供商设置相应的密钥和 URL（例如 `OPENAI_API_KEY`、`GEMINI_API_KEY`、`OLLAMA_BASE_URL`）。
- 可选：将配置信息保存在 `~/.config/coala/env` 文件中。
- `coala config` — 显示当前的配置路径和提供商/模型信息。