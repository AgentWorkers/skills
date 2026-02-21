---
name: clawhub-quarantine-installer
description: 在隔离的隔离环境中安装并审计 ClawHub 的技能，以便进行安全分析。这允许您在将技能推广到生产环境之前审查其中的风险。使用此技能可以测试 ClawHub 标记为可疑的第三方技能，调查它们的依赖关系和行为，并生成基本的审计报告。
homepage: https://github.com/alessandropcostabr/clawhub-quarantine-installer
---
# ClawHub 隔离安装器

## 概述

该工具可自动将 ClawHub 中的技能安装到专门的隔离目录（`$HOME/.openclaw/clawhub-quarantine/skills/`），并执行基本的审计脚本以识别潜在风险。其设计目的是在将技能集成到您的 OpenClaw 生产环境之前，允许您更安全地进行手动分析。

## 使用流程

1. **将技能安装到隔离目录：**
   * 运行 `scripts/install_and_audit.sh` 脚本，并传入所需的技能名称。
   * 例如：`bash ~/.openclaw/workspace/skills/clawhub-quarantine-installer/scripts/install_and_audit.sh <技能名称>`
   * **注意：** `install_and_audit.sh` 脚本会使用 `npx clawhub install --force` 命令。该命令会从 npm 注册表中下载并执行远程代码。**务必仅在隔离环境中（如虚拟机或 Docker 容器）运行此脚本，以避免访问敏感数据或生产环境。** 隔离环境旨在降低风险，但无法完全消除风险。
   * **备注：** 使用 `--force` 标志是为了安装 ClawHub 标记为可疑的技能。

2. **查看审计报告：**
   * 审计报告将生成在 `$HOME/.openclaw/clawhub-quarantine/reports/<技能名称>-audit-<时间戳>.txt` 文件中。
   * 该报告会列出技能文件，并使用 `ripgrep` 工具查找潜在的风险模式（如危险命令、网络访问、密码泄露迹象）。

3. **深入手动检查：**
   * 访问技能的隔离目录（`$HOME/.openclaw/clawhub-quarantine/skills/<技能名称>`）。
   * 查看技能的 `SKILL.md` 文件及其源代码文件（如果有的话），以及依赖项，以了解其功能。
   * 检查外部依赖项，并在可能的情况下，查看其在 GitHub 上的仓库以获取安全问题或额外信息。

4. **手动移至生产环境：**
   * 如果经过手动检查和审计后，确认技能安全，可以将其手动移至 `~/.openclaw/workspace/skills/` 目录。

## 脚本

### `scripts/install_and_audit.sh`

该脚本是技能安装的核心组件，它：
   * 接收技能名称作为参数。
   * 如果不存在，则创建隔离目录和报告目录。
   * 使用 `npx clawhub install --force` 将技能安装到隔离目录（`$HOME/.openclaw/clawhub-quarantine/skills/`）。
   * 调用 `clawhub-quarantine.sh audit` 脚本生成安全报告，传入技能路径和报告目录。

### `scripts/clawhub-quarantine.sh`

该辅助脚本负责执行审计操作。目前，它支持 `audit` 命令，该命令：
   * 接收技能的完整路径和报告保存目录。
   * 使用 `ripgrep` 工具在技能代码中查找潜在的危险模式（例如：执行外部命令、访问敏感环境变量、网络请求）。
   * 生成包含审计结果的详细报告。

## 先决条件

为确保该工具正常运行，运行 OpenClaw 的环境中必须安装以下软件，并将其添加到 PATH 变量中：
- **Node.js**：版本 `>=22`（`npm` 和 `npx` 的必备版本）。
- **`clawhub` CLI**：可以通过 `npm i -g clawhub` 全局安装。
- **`ripgrep`（`rg`）：一种快速的模式匹配工具，用于审计脚本中的代码检查。

## 发现与经验教训（以 'gram' 技能为例）

- **安全警报：** ClawHub 通过 “VirusTotal Code Insight” 识别可疑技能（例如：使用加密密钥、外部 API、`eval`）。这是审查的关键起点。
- **隔离机制的有效性：** 将技能安装到隔离目录（`$HOME/.openclaw/clawhub-quarantine/skills/`）可以有效控制分析过程中的风险。
- **基于模式的审计：** `clawhub-quarantine.sh audit` 脚本会查找常见的风险模式。
- **高风险依赖项：** 有些技能可能依赖于与操作系统底层交互的库（例如：`sweet-cookie` 用于访问浏览器 cookie、解密密钥环中的密码以及通过 `child_process` 执行外部命令）。这些依赖项需要特别关注。
- **API 不兼容性：** 即使经过身份验证，第三方 API（如 Instagram）也可能因用户代理不匹配、无效的媒体 ID 或请求过多等原因而阻止或禁用自动化功能，从而影响技能的可用性。