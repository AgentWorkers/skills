---
name: openclaw-genie
description: 当用户询问有关 OpenClaw 的内容时，可以使用以下信息进行解答：包括安装、配置、代理、通道、内存管理、工具、钩子（hooks）、技能（skills）、部署方式、Docker 支持、多代理（multi-agent）功能、OAuth 认证、网关（gateway）设置、命令行界面（CLI）的使用方法、浏览器集成、执行命令（exec）、沙箱环境（sandboxing）的配置、会话管理（sessions）、定时任务（cron）、Webhook 的实现、心跳检测（heartbeat）、子代理（sub-agents）的设置，以及与消息平台的集成（integration with messaging platforms）等。
  Use when the user asks about OpenClaw — installation, configuration, agents,
  channels, memory, tools, hooks, skills, deployment, Docker, multi-agent,
  OAuth, gateway, CLI, browser, exec, sandboxing, sessions, cron, webhooks,
  heartbeat, sub-agents, or messaging platform integration.
---
# OpenClaw Genie

OpenClaw 是一个自托管的个人 AI 代理网关（采用 MIT 许可协议，在 GitHub 上拥有约 22.9 万个星标）。它通过一个统一的网关进程，将大型语言模型（LLM）代理连接到 38 种以上的消息平台（包括 WhatsApp、Telegram、Discord、Slack、Signal、iMessage、MS Teams、Matrix 等）。所有数据都存储在本地。

---

## 快速入门

```bash
# One-liner install (macOS/Linux, requires Node 22+)
curl -fsSL https://openclaw.ai/install.sh | bash

# Or via npm
npm install -g openclaw@latest

# Interactive setup — gateway, workspace, channels, skills
openclaw onboard --install-daemon

# Verify
openclaw status
openclaw gateway status
```

Web 控制界面：`http://127.0.0.1:18789/`

---

## 核心架构

```
Channels (WhatsApp, Discord, Telegram, Slack, Signal, …)
        ↓
    Gateway  ← WebSocket control plane (port 18789), single source of truth
        ↓
    Agents   ← isolated workspaces, sessions, memory, tools
        ↓
    Tools    ← exec, browser, skills, hooks, messaging, sub-agents
```

- **网关（Gateway）**：支持 WebSocket、HTTP 和控制界面的多路复用功能；允许动态重新加载配置。
- **代理（Agents）**：每个代理都有独立的工作空间、会话存储、内存、认证配置以及沙箱环境。
- **通道（Channels）**：可以同时运行 38 种以上的适配器；消息会按照预设的路由规则返回给相应的发送方。
- **会话（Sessions）**：会话文件的格式为 `agent:<agentId>:<channel>:<scope>:<chatId>`；私信的范围包括 `main`、`per-peer`、`per-channel-peer` 和 `per-account-channel-peer`。

---

## 代理配置

代理的工作空间文件位于 `~/.openclaw/workspace/`（默认代理）或 `~/.openclaw/workspace-<agentId>/` 目录下：

| 文件名 | 用途 |
|------|---------|
| `SOUL.md` | 代理的个性化和系统提示信息 |
| `IDENTITY.md` | 代理的名称、表情符号和头像 |
| `USER.md` | 用户配置信息 |
| `MEMORY.md` | 代理的长期存储数据 |
| `memory/YYYY-MM-DD.md` | 每日的会话日志（仅可追加） |
| `TOOLS.md` | 工具使用指南 |
| `BOOTSTRAP.md` | 一次性初始化任务（首次运行后会被删除） |
| `HEARTBEAT.md` | 定期检查指令 |

配置文件的加载顺序为：IDENTITY → SOUL → USER → MEMORY → 日志 → 技能（Skills） → 会话数据。

每个代理的配置信息存储在 `openclaw.json` 文件中的 `agents.list[]` 和 `bindings[]` 数组中（详情请参阅 `references/multi-agent.md`）。

---

## openclaw.json 配置文件

配置文件位于 `~/.openclaw/openclaw.json`，采用 JSON5 格式（允许注释和文件末尾添加逗号）。

```jsonc
{
  "models": {           // primary, fallbacks, aliases, image model
    "primary": "anthropic/claude-sonnet-4-5",
    "fallbacks": ["openai/gpt-4o"]
  },
  "channels": { },      // discord, telegram, whatsapp, slack, signal, …
  "agents": { },        // list, defaults, bindings, broadcast, subagents
  "tools": { },         // profiles, allow/deny, loop detection, exec config
  "skills": { },        // entries, load dirs, install manager
  "browser": { },       // profiles, SSRF policy, executable path
  "sandbox": { },       // mode (off/non-main/all), scope, Docker hardening
  "gateway": { },       // port, auth, discovery, binding
  "automation": { },    // cron, webhooks, heartbeat
  "hooks": { },         // internal hooks config
  "session": { },       // dmScope, resets, sendPolicy, maintenance
  "auth": { }           // OAuth profiles, key rotation, order
}
```

- **环境变量（Env vars）**：存储在 `~/.openclaw/.env` 文件中，配置字符串中可以使用 `${VAR}` 语法进行替换。
- **`$include`**：支持嵌套文件导入（最多 10 层）。
- **动态重新加载（Hot reload）**：默认采用“混合”模式（hybrid），安全更改会立即生效，关键更改需要重启服务；每次更改之间有 300 毫秒的延迟。
- **严格验证（Strict validation）**：如果配置文件中包含未知的键，网关将无法启动。

更多配置细节请参阅 `references/configuration.md`。

---

## 各消息通道的快速参考

| 渠道（Channel） | 设置方式（Setup） | 说明（Notes） |
|---------|-------|-------|
| Discord | `openclaw channels add discord` | 使用 Bot API 和网关连接；支持服务器聊天、私信、线程、斜杠命令和语音功能 |
| Telegram | `openclaw channels add telegram` | 支持群组聊天、论坛、内联按钮和 Webhook 功能 |
| WhatsApp | `openclaw channels add whatsapp` | 支持 QR 配对、媒体文件上传和投票功能 |
| Slack | `openclaw channels add slack` | 使用 Bolt SDK 连接；支持 Socket 或 HTTP 模式以及原生流媒体传输 |
| Signal | `openclaw channels add signal` | 使用 signal-cli 工具；注重隐私保护，支持自动后台运行 |
| iMessage | `openclaw channels add bluebubbles` | 支持表情反应、编辑和群组聊天 |
| Google Chat | `openclaw channels add googlechat` | 通过 HTTP Webhook 连接 |
| IRC | `openclaw channels add irc` | 支持 NickServ 和私信功能 |
| MS Teams | `openclaw plugins install @openclaw/msteams` | 支持自适应卡片和投票功能 |
| Matrix | `openclaw plugins install @openclaw/matrix` | 支持端到端加密（E2EE）、线程和房间功能 |

**访问控制**：支持设置私信策略（`pairing`/`allowlist`/`open`/`disabled`）、群组策略以及提及功能；每个通道支持多个账户。

更多关于各通道的详细信息，请参阅 `references/channels.md`。

---

## 内存系统

- **每日日志（Daily logs）**：`memory/YYYY-MM-DD.md` 文件会在会话开始时加载当天和昨天的日志。
- **长期存储（Long-term storage）**：`MEMORY.md` 文件存储精选的事实、决策和用户偏好设置（仅限私人会话）。
- **工具（Tools）**：提供 `memory_search`（用于快速检索数据，每次最多检索 400 个词元）和 `memory_get`（用于读取内存文件）功能。
- **混合搜索（Hybrid search）**：结合 BM25 算法和向量搜索技术（支持自定义权重）。
- **数据处理（Post-processing）**：采用 MMR 算法进行去重处理，并设置 30 天的数据有效期。
- **数据来源（Providers）**：自动选择本地数据源或 OpenAI、Gemini、Voyage、Mistral 等外部服务。
- **QMD 后端（QMD backend）**：可选的辅助系统（优先使用本地数据，也可使用 BM25、向量搜索和重新排序功能）。

更多关于内存配置的详细信息，请参阅 `references/memory.md`。

---

## 工具概述

| 工具（Tools） | 用途 |
|------|---------|
| `exec` | 执行 Shell 命令（在沙箱或网关环境中） |
| `process` | 管理后台进程 |
| `browser` | 提供 Chromium 自动化功能（用于导航、点击、输入和截图） |
| `web_search` | 使用 Brave Search API 进行网络搜索 |
| `web_fetch` | 从 URL 中提取 Markdown 内容 |
| `memory_search` | 对内存数据进行语义向量搜索 |
| `memory_get` | 直接读取内存文件内容 |
| `message` | 支持跨通道发送消息、接收回复、创建新线程、固定消息显示和发起投票 |
| `sessions_spawn` | 启动子代理（可以是一次性执行，也可以持续运行，最多支持 5 层嵌套） |
| `canvas` | 提供 Node.js Canvas 用户界面（可在连接的设备上显示内容） |

**访问控制**：支持不同的权限级别（`minimal`、`coding`、`messaging`、`full`），以及工具的使用权限管理（按组别划分）。

更多关于工具、技能和自动化功能的详细信息，请参阅 `references/tools.md`。

---

## 钩子（Hooks）与自动化（Automation）

**钩子（Hooks）**：位于 `<workspace>/hooks/` 目录下的 TypeScript 事件处理器：

| 事件（Event） | 触发条件（Trigger） |
|-------|---------|
| `command:new/reset/stop` | 会话生命周期相关的操作 |
| `agent:bootstrap` | 初始化代理前的处理 |
| `gateway:startup` | 通道加载完成后执行的操作 |
| `message:received/sent` | 消息接收/发送时的处理 |
| `tool_result_persist` | 同步处理工具返回的结果 |

**自动化（Automation）**：内置在网关中：
- **Cron**：支持定时任务（支持 Cron 表达式和间隔设置，也可以一次性执行）；可以单独运行或与主会话一起执行。
- **Webhooks**：提供 `/hooks/wake`（系统事件处理）和 `/hooks/agent`（代理相关操作）等接口。
- **Heartbeat**：定期检查代理状态（默认每 30 分钟执行一次），可以批量处理多个检查任务。

---

## 部署选项

**云部署（Deployment options）**

- **云服务（Cloud）**：支持 Fly.io、Railway、Render、GCP、Hetzner、Cloudflare Workers 和 Ansible 等云服务。
- **沙箱环境（Sandboxing）**：为不可信的会话提供 Docker 隔离环境；支持 `off`、`non-main` 和 `all` 三种模式；数据范围包括 `session`、`agent` 和 `shared`。
- **远程访问（Remote access）**：推荐使用 Tailscale 或 VPN，必要时也可以通过 SSH 隧道进行访问。

更多关于部署的详细信息，请参阅 `references/deployment.md`。

---

## 命令行工具（CLI Essentials）

| 命令（Command） | 用途 |
|---------|---------|
| `openclaw onboard` | 交互式的首次设置流程 |
| `openclaw gateway start/stop/status` | 管理网关服务 |
| `openclaw channels add/list/status/login` | 管理消息通道 |
| `openclaw models list/set/auth/scan` | 管理模型配置和认证信息 |
| `openclaw skills list/info/check` | 管理技能信息 |
| `openclaw hooks list/enable/disable/install` | 管理钩子功能 |
| `openclaw agent --message "..."` | 启动或停止单个代理 |
| `openclaw agents list/add/delete` | 管理多个代理 |
| `openclaw sessions` | 查看和管理会话信息 |
| `openclaw browser` | 提供浏览器控制功能（包含 50 多个子命令） |
| `openclaw cron list/add/run` | 安排定时任务 |
| `openclaw config get/set/unset` | 查看/修改配置参数 |
| `openclaw doctor [--fix]` | 进行系统健康检查并自动修复问题 |
| `openclaw security audit [--deep]` | 进行安全审计 |
| `openclaw logs [--follow]` | 查看网关日志 |
| `openclaw memory search "query"` | 进行向量搜索 |
| `openclaw tui` | 提供终端用户界面 |

**全局参数（Global flags）**：`--dev`、`--profile <name>`、`--json`、`--no-color` 等。

---

## 何时查阅参考文件

- 如果你需要了解 OpenClaw 的完整配置信息、模型提供者、环境变量、认证机制和 OAuth 设置，请参阅 `references/configuration.md`。
- 如果需要了解各消息通道的详细设置、路由规则、访问控制、流媒体传输或多账户支持等功能，请参阅 `references/channels.md`。
- 如果需要了解内存管理、向量搜索、QMD、嵌入技术和混合搜索算法等内容，请参阅 `references/memory.md`。
- 如果需要了解工具的使用方法、浏览器自动化功能、钩子机制和子代理的配置，请参阅 `references/tools.md`。
- 如果需要了解 Docker 部署、云服务部署、沙箱环境设置、原生安装方法或安全相关内容，请参阅 `references/deployment.md`。
- 如果需要了解多代理配置、代理之间的数据绑定方式、广播功能以及子代理的详细信息，请参阅 `references/multi-agent.md`。