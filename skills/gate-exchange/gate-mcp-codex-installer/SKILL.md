---
name: gate-mcp-codex-installer
description: Codex中提供了一键安装工具，用于安装Gate MCP及其所有相关技能。该工具会安装Gate MCP服务器（包括main、dex、info和news四个部分，用户可自行选择）以及来自gate-skills仓库中的所有技能。默认情况下，系统会同时安装所有的MCP组件和所有技能；所有技能都会被完整地安装到位。
---
# 一键安装器（技能：MCP + Skills）

当用户请求“一键安装Gate”、“安装Gate MCP和Skills”或“通过Codex安装Gate-MCP”等时，请使用此技能，且用户正在使用**Codex**。

## 资源

| 类型 | 名称 | 端点/配置 |
|------|------|-------------------|
| MCP | Gate（主组件） | `npx -y gate-mcp`，详见 [gate-mcp](https://github.com/gate/gate-mcp) |
| MCP | Gate Dex | https://api.gatemcp.ai/mcp/dex（已修复x-api-key问题） |
| MCP | Gate Info | https://api.gatemcp.ai/mcp/info |
| MCP | Gate News | https://api.gatemcp.ai/mcp/news |
| Skills | gate-skills | https://github.com/gate/gate-skills（所有技能均安装于此目录下） |

## 行为规则

1. **默认情况**：当用户未指定要安装的MCP时，将安装**所有MCP**（主组件、Dex、信息、新闻）以及**所有Skills**。
2. **可选MCP**：用户可以选择仅安装特定的MCP（例如仅安装主组件或仅安装Dex等），系统会按照用户的选择进行安装。
3. **Skills**：除非用户指定`--no-skills`，否则会自动安装`gate-skills`仓库中`skills/**`目录下的所有Skills。

## 安装步骤

### 1. 确认用户选择（MCP）

- 如果用户未指定要安装的MCP，则安装所有MCP：主组件、Dex、信息、新闻。
- 如果用户指定了具体的MCP（如“仅安装xxx”），则仅安装该MCP。

### 2. 编写Codex MCP配置文件

- 用户级配置文件：`~/.codex/config.toml`（或 `$CODEX_HOME/config.toml`）。如果文件不存在，系统会创建该文件并添加`[mcp_servers]`部分。
- 如果配置文件已存在，系统会仅添加新的MCP配置信息，而不会覆盖原有内容。
- 配置详情：
  - **Gate（主组件）**：使用`stdio`方式配置，命令为`command = "npx"`, 参数为`["-y", "gate-mcp"]`。
  - **Gate Dex**：使用流式HTTP协议进行配置，`url`设置为`http_headers["x-api-key"]`（已修复为`MCP_AK_8W2N7Q`），并且`http_headers["Authorization"]`设置为`Bearer ${GATE_MCP_TOKEN}`。
  - **Gate Info / Gate News**：同样使用流式HTTP协议进行配置，`url`为相应的API地址。

### 3. 安装Skills

- 从`https://github.com/gate/gate-skills`下载`skills/**`目录下的所有子目录，并将其复制到`$CODEX_HOME/skills/`（默认路径为`~/.codex/skills/`）。
- 如果用户仅希望安装MCP而不安装Skills，可以在脚本中添加`--no-skills`参数。

### 4. 安装后的提示

- 通知用户已安装的MCP列表以及“所有Skills均已安装”（除非使用了`--no-skills`参数）。
- 提示用户重新启动Codex以加载MCP服务器和Skills。
- **获取API密钥**：如果用户使用Gate（主组件）进行现货/期货交易，系统会提示用户访问`https://www.gate.com/myaccount/profile/api-key/manage`来创建API密钥，并设置`GATE_API_KEY`和`GATE_API_SECRET`。
- **Gate-Dex授权**：如果安装了Gate-Dex且查询返回需要授权的提示，系统会提示用户先访问`https://web3.gate.com/`创建或绑定钱包，之后助手会提供可点击的Google授权链接以便用户完成OAuth认证。

## 脚本

使用此技能目录中的`scripts/install.sh`脚本来完成一键安装：

- 使用方法：
  `./scripts/install.sh [--mcp main|dex|info|news] ... [--no-skills]`
  - 如果未指定`--mcp`参数，将安装所有MCP；
  - 如果指定了多个`--mcp`参数，将仅安装指定的MCP；
  - 使用`--no-skills`参数时，将仅安装MCP。
- DEX的x-api-key被设置为`MCP_AK_8W2N7Q`，并写入`config.toml`文件中。

从GitHub下载此技能后，请在仓库根目录下运行以下命令：
`bash skills/gate-mcp-codex-installer/scripts/install.sh`
或者（仅安装MCP时）：
`bash skills/gate-mcp-codex-installer/scripts/install.sh --no-skills`