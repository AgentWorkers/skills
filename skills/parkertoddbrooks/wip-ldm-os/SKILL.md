---
name: wip-ldm-os
description: LDM操作系统……为AI代理提供了共享的基础设施。它涵盖了身份管理、内存管理、权限控制、协作功能、兼容性保障以及支付系统等核心功能。这是一个统一的管理平台，适用于您所有的AI系统。
license: MIT
interface: [cli, skill]
metadata:
  display-name: "LDM OS"
  version: "0.2.5"
  homepage: "https://github.com/wipcomputer/wip-ldm-os"
  author: "Parker Todd Brooks"
  category: infrastructure
  capabilities:
    - extension-install
    - interface-detection
    - agent-identity
    - extension-registry
    - health-check
  requires:
    bins: [git, npm, node]
  openclaw:
    requires:
      bins: [git, npm, node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-ldm-os"
        bins: [ldm]
        label: "Install LDM OS via npm"
    emoji: "🧠"
compatibility: Requires git, npm, node. Node.js 18+.
---
# LDM 操作系统（LDM OS）

您使用的工具包括 Claude Code、GPT、OpenClaw 等。这些工具之间不共享内存，也不了解彼此的功能，更不知道如何协同工作。LDM 操作系统（LDM OS）则充当了它们之间的共享基础设施层。只需安装一次，您使用的所有 AI 工具就能获得以下功能：

- **身份识别**：每个 AI 都拥有自己独特的行为、个性和技能；
- **共享内存**：所有 AI 都可以使用安全、受保护的共享内存，且这些内存可以随时被您带走；
- **数据所有权**：您与 AI 之间的所有交互以及产生的数据都归您所有，这些数据是加密的且可移植的，永远不会被锁定；
- **协作能力**：AI 可以相互通信、共享工具并协同工作；
- **兼容性**：任何技能、插件或工具都能与所有 AI 兼容。只需安装一次，即可在任何地方使用；
- **支付机制**：当 AI 需要付费时，您可以通过 Face ID 或 Apple Pay 进行支付。

## 平台兼容性

| 接口 | 需要的条件 | 示例 |
|---------|------------------|---------|
| **命令行界面（CLI）** | 需要 shell 访问权限（可运行 bash 或 node 命令） | `ldm init`, `ldm install`, `ldm doctor` |
| **技能插件** | 需要 SKILL.md 文件（该文件可在 Claude Code 和 OpenClaw 中使用） | 您现在正在阅读的文档就是这样的文件 |

**LDM 操作系统基于以下平台构建并经过测试：**
- **Claude Code CLI**：完全支持（支持 shell 和 CLI 命令）；
- **OpenClaw**：完全支持（支持 shell 和 CLI 命令）。

## 操作规则

- **务必先进行模拟测试**：在安装或进行任何更改之前，使用 `--dry-run` 选项运行程序，以便用户能够清楚地了解实际效果。只有得到用户的明确许可后，才能继续下一步操作。
- **切勿修改重要数据**：安装程序绝对不会覆盖 `crystal.db`、代理数据、密钥或状态文件。代码可以更新，但数据将保持不变。

## 安装流程

### 第一步：安装 LDM 操作系统

```bash
npm install -g @wipcomputer/wip-ldm-os
ldm init --dry-run
```

向用户展示模拟测试的结果，并解释各个目录的作用：
- `~/.ldm/extensions/`：存放工具和插件；
- `~/.ldm/agents/`：每个 AI 的身份、个性和内存数据存储在这里；
- `~/.ldm/memory/`：所有 AI 共享的内存；
- `~/.ldm/state/`：存储配置信息和同步状态数据。

当用户同意安装后，继续执行下一步。

### 第二步：安装技能插件

LDM 操作系统自带一个技能插件目录。向用户展示可用的插件及其功能：

| 技能名称 | 功能描述 | 状态 |
|---------|-------------------|---------|
| **Memory Crystal**（推荐使用） | 提供持久化的内存存储、搜索、数据整合功能 | 稳定版本 |
| **AI DevOps Toolbox** | 用于 AI 的发布、部署、许可和代码库管理 | 稳定版本 |
| **1Password** | 为 AI 代理提供安全的数据存储服务 | 稳定版本 |
| **Markdown Viewer** | 支持 AI 之间的实时 Markdown 文本编辑 | 稳定版本 |
| **xAI Grok** | 提供网络搜索、数据提取和图像生成功能 | 稳定版本 |
| **X Platform** | 提供与 X 平台交互的功能（如阅读帖子、搜索推文、上传媒体） | 稳定版本 |
| **OpenClaw** | 作为 AI 代理的运行平台，支持身份识别、内存管理和工具使用 | 稳定版本 |
| **Dream Weaver Protocol** | 用于 AI 代理的内存数据整合协议 | 稳定版本 |
| **Bridge** | 实现 Claude Code 与 OpenClaw 之间的跨平台通信 | 稳定版本 |

要安装某个技能插件，请执行相应的命令（此处应展示具体的安装步骤）。

**注意：** 如果某些技能是通过其他方式（如 `crystal init`、`wip-install` 或手动设置）安装的，它们可能不会自动显示在插件目录中。此时可以运行 `ldm install <org/repo>` 来重新注册这些插件。

### 第三步：验证安装结果

```bash
ldm doctor
```

系统会检查以下内容：
- LDM 操作系统的根目录是否存在；
- `version.json` 文件是否有效；
- 插件注册表是否完整；
- 所有插件是否已成功部署；
- 所有的钩子（hooks）是否配置正确；
- MCP 服务器是否已正确注册。

## 常用命令

| 命令 | 功能 |
|---------|---------|
| `ldm init` | 创建 `~/.ldm/` 目录结构并生成 `version.json` 文件 |
| `ldm install <org/repo>` | 从指定仓库克隆并安装插件 |
| `ldm install /path/to/repo` | 从本地路径安装插件 |
| `ldm install` | 更新所有已注册的插件 |
| `ldm doctor` | 检查所有插件的运行状态 |
| `ldm status` | 显示系统版本和插件列表 |
| `ldm --version` | 显示系统版本信息 |

所有命令都支持 `--dry-run`（预览安装效果）和 `--json`（生成机器可读的输出格式）选项。

## 接口检测机制

当您运行 `ldm install` 时，系统会自动检测仓库支持的接口类型，并将其部署到相应的位置：

| 接口类型 | 检测方式 | 部署位置 |
|---------|------------------|-----------------|
| **命令行界面（CLI）** | 通过 `package.json` 文件中的 `bin` 项 | 使用 `npm install -g` 安装 |
| **MCP Server** | 通过 `mcp-server.mjs` 或 `mcp-server.js` 文件 | 使用 `claude mcp add --scope user` 安装 |
| **OpenClaw 插件** | 通过 `openclaw.plugin.json` 文件 | 存放在 `~/.ldm/extensions/` 和 `~/.openclaw/extensions/` 目录中 |
| **技能插件** | 通过 `SKILL.md` 文件或 `skills/` 目录 | 存放在 `~/.openclaw/skills/` 目录中 |
| **钩子（Hook）** | 通过 `package.json` 文件中的 `guard.mjs` 或 `claudeCode.hook` 文件 | 配置在 `~/.claude/settings.json` 中 |
| **模块（Module）** | 通过 `package.json` 文件中的 `main` 或 `exports` 项 | 可通过 `node_modules` 进行导入 |

无需手动配置，只需指定仓库路径，系统会自动完成其余的部署工作。

## 升级

如果 LDM 操作系统已经安装，可以使用以下命令进行升级：

```bash
ldm status        # show current version and extensions
ldm install       # update all registered extensions
ldm doctor        # verify everything works
```

升级过程会部署新的代码，但不会修改现有的 `crystal.db`、代理文件、密钥或状态数据。

## LDM 操作系统的组成部分

LDM 操作系统本身是一个运行时环境，各种技能插件可以在此基础上扩展其功能：
- **Memory Crystal**：`wipcomputer/memory-crystal`
- **AI DevOps Toolbox**：`wipcomputer/wip-ai-devops-toolbox`
- **1Password**：`wipcomputer/wip-1password`
- **Markdown Viewer**：`wipcomputer/wip-markdown-viewer`
- **xAI Grok**：`wipcomputer/wip-xai-grok`
- **X Platform**：`wipcomputer/wip-xai-x`
- **OpenClaw**：`openclaw/openclaw`
- **Dream Weaver Protocol**：`wipcomputer/dream-weaver-protocol`
- **Bridge**：`wipcomputer/wip-bridge`

只需运行 `ldm install` 即可添加新的技能插件。