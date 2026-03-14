---
name: gate-mcp-claude-installer
description: Claude Code（Claude CLI）中提供了Gate MCP及所有Gate技能的一键安装工具。该工具会安装Gate MCP服务器（包括main、dex、info、news四个目录，用户可根据需要选择安装），以及来自gate-skills仓库中的所有技能。默认情况下，系统会同时安装所有的MCP组件和所有技能，且所有技能都会被完整地安装到位。
---
# 一键安装器（Claude 代码：MCP + Skills）

当用户请求“一键安装 Gate”、“安装 Gate MCP 和 Skills”或“使用 Claude 安装 gate-mcp”等时，请使用此技能，且用户正在使用 **Claude 代码（Claude CLI）**。

## 资源

| 类型 | 名称 | 端点 / 配置 |
|------|------|-------------------|
| MCP | Gate（主组件） | `npx -y gate-mcp`，详见 [gate-mcp](https://github.com/gate/gate-mcp) |
| MCP | Gate Dex | https://api.gatemcp.ai/mcp/dex（需要设置 x-api-key） |
| MCP | Gate Info | https://api.gatemcp.ai/mcp/info |
| MCP | Gate News | https://api.gatemcp.ai/mcp/news |
| Skills | gate-skills | https://github.com/gate/gate-skills（所有技能都会被安装到此仓库中） |

## 行为规则

1. **默认情况**：当用户未指定要安装的 MCP 时，将安装 **所有 MCP**（主组件、Dex、信息、新闻）以及 **所有 Skills**。
2. **可选 MCP**：用户可以选择仅安装特定的 MCP（例如仅安装主组件或仅安装 Dex）；系统会按照用户的选择进行安装。
3. **Skills**：除非使用了 `--no-skills` 选项，否则会从 `gate-skills` 仓库的 `skills/` 目录中安装 **所有 Skills**。

## 安装步骤

### 1. 确认用户选择（MCP）

- 如果用户未指定要安装的 MCP -> 安装所有 MCP（主组件、Dex、信息、新闻）。
- 如果用户指定了具体的 MCP（如 “仅安装 xxx”） -> 仅安装指定的 MCP。

### 2. 编写 Claude 代码中的 MCP 配置

- 用户级配置文件：`~/.claude.json`（Windows 用户：`%USERPROFILE%\.claude.json`）。如果使用目录格式，请将配置文件放在 `~/.claude/` 目录下。
- 如果配置文件已存在，将其 **合并** 到现有的 `mcpServers` 配置中，不要覆盖其他配置。
- 配置详情：
  - **Gate（主组件）**：`stdio`, `command: npx`, `args: ["-y", "gate-mcp"]`
  - **Gate-Dex**：`http`, `url` + `headers["x-api-key"]`（设置为 `MCP_AK_8W2N7Q`），`headers["Authorization"]` 设置为 `Bearer ${GATE_MCP_TOKEN}``
  - **Gate-Info / Gate-News**：`http`, `url`

### 3. 安装 Skills（所有 Skills）

- 从 `https://github.com/gate/gate-skills` 下拉取 `skills/` 目录下的所有子目录，并将其复制到 `~/.claude/skills/`（或当前环境的相应目录）。
- 如果仅需要安装 MCP 而不需要 Skills，可以在脚本中添加 `--no-skills` 选项。

### 4. 安装后的提示

- 告知用户已安装的 MCP 列表以及“所有 Skills 已成功安装”（除非使用了 `--no-skills`）。
- 提示用户重新打开 Claude 代码或启动新会话以加载已安装的 MCP。
- **获取 API 密钥**：如果用户使用 Gate（主组件）进行现货/期货交易，提示他们访问 https://www.gate.com/myaccount/profile/api-key/manage 以创建 API 密钥，并设置 `GATE_API_KEY` 和 `GATE_API_SECRET`。
- **Gate-Dex 认证**：如果安装了 Gate-Dex 并且查询返回需要认证的提示，提示用户先访问 https://web3.gate.com/ 创建或绑定钱包，之后助手会提供可点击的 Google 认证链接以便用户完成 OAuth 认证。

## 脚本

使用此技能目录中的 `scripts/install.sh` 脚本进行一键安装。

- 使用方法：
  `./scripts/install.sh [--mcp main|dex|info|news] ... [--no-skills]`
  - 如果未传递 `--mcp`，则安装所有 MCP；
  - 传递多个 `--mcp` 选项可以仅安装指定的 MCP；
  - 传递 `--no-skills` 选项则仅安装 MCP。
- DEX 的 x-api-key 被设置为 `MCP_AK_8W2N7Q` 并保存在配置文件中。

从 GitHub 下载此技能后，请在仓库根目录下运行以下命令：
`bash skills/gate-mcp-claude-installer/scripts/install.sh`
或者（仅安装 MCP）：
`bash skills/gate-mcp-claude-installer/scripts/install.sh --no-skills`