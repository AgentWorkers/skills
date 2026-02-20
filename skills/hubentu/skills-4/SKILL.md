---
name: coala-client
description: >
  如何使用 coala-client CLI 与大型语言模型（LLMs）、MCP 服务器以及各种技能进行交互？  
  当用户需要了解如何使用 coala、启动 coala 聊天功能、添加 MCP 服务器、导入 CWL 工具集、列出或调用 MCP 工具、导入或加载技能，或者使用 sandbox 的 `run_command` 工具时，可以参考以下操作步骤。
---
# Coala 客户端

Coala 生态系统的一部分。这是一个命令行工具（CLI），用于与兼容 OpenAI 的大型语言模型（LLM，如 OpenAI、Gemini、Ollama）以及 MCP（Model Context Protocol）服务器进行聊天。该客户端支持将 CWL（CWL Tools Library）工具集导入作为 MCP 服务器使用，支持导入技能，并提供可选的沙箱环境来运行 shell 命令。

## 配置路径

- MCP 配置和工具集：`~/.config/coala/mcps/`  
  - `mcp_servers.json` — 服务器定义文件  
  - `<toolset>/` — 各工具集的目录，其中包含 `run_mcp.py` 文件和 CWL 文件  
- 技能（Skills）：`~/.config/coala/skills/`（每个导入的来源对应一个子文件夹）  
- 环境变量（Env）：`~/.config/coala/env`（可选；格式为键=值，用于配置提供商和 MCP 环境）

## 快速入门

1. **首次初始化**  
   `coala init` — 创建 `~/.config/coala/mcps/mcp_servers.json` 和 `env` 文件。

2. **设置 API 密钥**  
   例如：`export OPENAI_API_KEY=...` 或 `export GEMINI_API_KEY=...`。Ollama 不需要 API 密钥。

3. **聊天**  
   `coala` 或 `coala chat` — 与 MCP 工具进行交互式聊天。  
   `coala ask "question"` — 向 MCP 提出问题。

4. **选项**  
   `-p, --provider`（openai|gemini|ollama|custom）——指定使用哪个提供商  
   `-m, --model` — 指定使用的模型  
   `--no-mcp` — 禁用 MCP 功能  
   `--sandbox` — 启用沙箱模式

## MCP：CWL 工具集

导入、列出或调用 MCP 工具集时不需要 API 密钥，这些操作仅用于与 LLM 进行聊天或提问。

- **导入**  
  `coala mcp-import <TOOLSET> <SOURCES...>` 或使用别名 `coala mcp ...`  
  `SOURCES`：本地 `.cwl` 文件、`.zip` 文件，或指向 `.cwl` 或 `.zip` 文件的 HTTP URL。  
  需要安装 `coala` 包（其中包含 `run_mcp.py` 文件）。

- **列出**  
  `coala mcp-list` — 列出所有可用的服务器名称。  
  `coala mcp-list <SERVER_NAME>` — 显示每个服务器的详细信息（名称、描述、输入格式）。

- **调用**  
  `coala mcp-call <SERVER>.<TOOL> --args '<JSON>'`  
  例如：`coala mcp-call gene-variant.ncbi_datasets_gene --args '{"data": [{"gene": "TP53", "taxon": "human"}]}'`

## 技能（Skills）

- **导入**  
  将技能导入到 `~/.config/coala/skills/` 目录中（每个来源对应一个子文件夹）：  
  `coala skill <SOURCES...>`  
  `SOURCES`：GitHub 仓库的树形结构 URL（例如 `https://github.com/owner/repo/tree/main/skills`）、ZIP 文件链接，或本地 ZIP 文件目录。

- **在聊天中使用技能**  
  使用 `/skill` 命令可以列出已安装的技能。  
  使用 `/skill <name>` 命令可以从 `~/.config/coala/skills/<name>/`（例如 SKILL.md 文件）加载特定技能到聊天上下文中。

## 沙箱模式（Sandbox）

`coala --sandbox` 或 `coala ask "..." --sandbox` — 启用沙箱模式，允许 LLM 运行基本的 shell 命令（超时时间为 30 秒）。可以通过参数设置 `timeout` 和 `cwd` 来调整这些选项。

## 聊天命令

- `/help` — 显示帮助信息  
- `/exit` — 退出程序  
- `/quit` — 立即退出  
- `/clear` — 清除聊天记录  
- `/tools` — 列出所有可用的 MCP 工具  
- `/servers` — 列出已连接的 MCP 服务器  
- `/skill` — 列出所有技能；`/skill <name>` — 加载指定的技能  
- `/model` — 显示模型信息  
- `/switch <provider>` — 切换使用的提供商  

## 关闭/开启 MCP 功能

- **全部关闭**：`coala --no-mcp`（或 `coala ask "..." --no-mcp`）  
- **关闭单个服务器**：从 `~/.config/coala/mcp_servers.json` 中删除该服务器的记录。  
- **开启 MCP 功能**：默认情况下，如果未使用 `--no-mcp` 选项，则 MCP 功能处于开启状态；可以通过修改 `mcp_servers.json` 文件来添加或恢复服务器。

## 提供商（Providers）和环境变量（Environment）

- 使用 `-p` 参数或环境变量 `PROVIDER` 来指定提供商。  
- 为每个提供商设置相应的 API 密钥和 URL（例如 `OPENAI_API_KEY`、`GEMINI_API_KEY`、`OLLAMA_BASE_URL`）。  
- 可以将配置信息保存在 `~/.config/coala/env` 文件中。  
- `coala config` — 显示当前的配置路径和提供商/模型信息。