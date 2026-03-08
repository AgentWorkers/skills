---
name: openclaw-genie
version: 1.2.0
description: 当用户询问有关 OpenClaw 的内容时，可以使用以下信息进行解答：包括 OpenClaw 的安装方法、配置步骤、代理（agents）的设置、通信渠道（channels）的配置、内存管理、可用的工具（tools）、钩子（hooks）的功能、技能（skills）的运用、部署方案、Docker 的集成方式、多代理（multi-agent）的支持、OAuth 认证机制、网关（gateway）的配置、命令行界面（CLI）的使用方法、浏览器（browser）的集成、执行命令（exec commands）、PDF 文件的处理、语音功能（voice support）、秘钥管理（secret management）、沙箱环境（sandboxing）的设置、会话管理（session management）、定时任务（cron jobs）、Webhook 的使用、心跳检测（heartbeat mechanism）、子代理（sub-agents）的配置、节点（nodes）的管理、配套设备（companion devices）的集成、Canvas 用户界面、摄像头（camera）的支持，以及与消息传递平台（messaging platforms）的集成方式等。
  Use when the user asks about OpenClaw — installation, configuration, agents,
  channels, memory, tools, hooks, skills, deployment, Docker, multi-agent,
  OAuth, gateway, CLI, browser, exec, PDF, voice, secrets, sandboxing, sessions,
  cron, webhooks, heartbeat, sub-agents, nodes, companion devices, canvas,
  camera, or messaging platform integration.
---
# OpenClaw Genie

OpenClaw 是一个自托管的个人 AI 代理网关（采用 MIT 许可证，开源项目）。它通过单一的网关进程，将大型语言模型（LLM）代理连接到 22 种以上的消息平台（如 WhatsApp、Telegram、Discord、Slack、Signal、iMessage、MS Teams、Matrix 等），并支持与 50 多个第三方服务的集成（如 Gmail、GitHub、Obsidian、Spotify 等）。所有数据都存储在本地。

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
        ↓
    Nodes    ← companion devices (macOS/iOS/Android): camera, canvas, screen
```

- **网关（Gateway）**：支持 WebSocket、HTTP 和控制界面的多路复用功能；支持热重载配置。
- **代理（Agents）**：每个代理都有独立的工作空间、会话存储、内存、认证配置和沙箱环境。
- **通道（Channels）**：可以同时运行 22 种以上的原生适配器；消息会按照原始发送的通道返回。
- **节点（Nodes）**：配对的辅助设备可以通过 `node.invoke` 方法暴露 `canvas.*`、`camera.*`、`screen.*`、`device.*`、`notifications.*` 等功能。
- **会话（Sessions）**：会话的键格式为 `agent:<agentId>:<channel>:<scope>:<chatId>`；私信的范围包括 `main`、`per-peer`、`per-channel-peer`、`per-account-channel-peer`。

---

## 代理配置

代理的工作空间文件位于 `~/.openclaw/workspace/`（默认代理）或 `~/.openclaw/workspace-<agentId>/` 目录下：

| 文件 | 用途 |
|------|---------|
| `SOUL.md` | 代理的个性化和系统提示 |
| `IDENTITY.md` | 名称、表情符号、头像 |
| `USER.md` | 用户配置信息 |
| `MEMORY.md` | 管理的长期记忆数据 |
| `memory/YYYY-MM-DD.md` | 每日的只读会话日志 |
| `TOOLS.md` | 工具使用指南 |
| `BOOTSTRAP.md` | 一次性初始化任务（首次运行后删除） |
| `HEARTBEAT.md` | 定期检查指令 |

配置流程为：IDENTITY → SOUL → USER → MEMORY → 日志 → 技能 → 会话。

每个文件的字符限制为 20,000 个，总字符数最多为 150,000 个（可配置）。

多代理配置需要使用 `openclaw.json` 文件中的 `agents.list[]` 和 `bindings[]` 配置项（详见 `references/multi-agent.md`）。

---

## openclaw.json 配置文件

配置文件位于 `~/.openclaw/openclaw.json`（使用 JSON5 格式，允许注释和末尾的逗号）。

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

- **环境变量（Env vars）**：存储在 `~/.openclaw/.env` 文件中，配置字符串中可以使用 `${VAR}` 进行替换。
- **`$include`**：支持嵌套文件导入（最多 10 层）。
- **热重载（Hot reload）**：默认采用 `hybrid` 模式，安全变更会立即生效，关键变更需要重启；重载间隔为 300 毫秒。
- **严格验证（Strict validation）**：未知的配置键会导致网关无法启动。

有关完整配置信息，请参阅 `references/configuration.md`。

---

## 各通道快速参考

| 通道（Channel） | 设置方式（Setup） | 备注（Notes） |
|---------|-------|-------|
| Discord | `openclaw channels add discord` | 使用 Bot API 和网关；支持服务器消息、私信、线程、斜杠命令和语音功能 |
| Telegram | `openclaw channels add telegram` | 支持语法分析、群组、论坛、内联按钮和 Webhook 模式 |
| WhatsApp | `openclaw channels add whatsapp` | 支持 QR 配对、媒体上传和投票功能 |
| Slack | `openclaw channels add slack` | 使用 Bolt SDK；支持 Socket 或 HTTP 模式，支持原生流媒体 |
| Signal | `openclaw channels add signal` | 使用 signal-cli；注重隐私保护，支持自动后台运行 |
| iMessage | `openclaw channels add bluebubbles` | 支持表情反应、编辑和群组功能 |
| Google Chat | `openclaw channels add googlechat` | 使用 HTTP Webhook 应用 |
| IRC | `openclaw channels add irc` | 支持 NickServ、频道和私信 |
| MS Teams | `openclaw plugins install @openclaw/msteams` | 支持自适应卡片和投票功能 |
| Matrix | `openclaw plugins install @openclaw/matrix` | 支持端到端加密、线程和房间功能 |
| Mattermost | `openclaw plugins install @openclaw/mattermost` | 支持自托管 |
| Nextcloud Talk | `openclaw plugins install @openclaw/nextcloud-talk` | 支持自托管 |
| WebChat | 内置 Web UI；可以通过网关 URL 进行浏览器访问 |

**访问控制**：支持私信策略（`pairing`/`allowlist`/`open`/`disabled`）、群组策略和提及控制。每个通道支持多个账户。

详细信息请参阅 `references/channels.md`。

---

## 内存系统

- **每日日志（Daily logs）**：`memory/YYYY-MM-DD.md` 文件会在会话开始时加载当天的和昨天的日志。
- **长期存储（Long-term storage）**：`MEMORY.md` 文件存储精选的事实、决策和偏好设置（仅限私有会话）。
- **工具（Tools）**：提供 `memory_search`（向量检索，每次检索约 400 个词元）和 `memory_get`（文件读取）功能。
- **混合搜索（Hybrid search）**：结合 BM25（精确匹配）和向量搜索（基于语义），支持自定义权重。
- **后处理（Post-processing）**：采用 MMR 算法进行去重处理，数据保留时间为 30 天。
- **数据提供者（Providers）**：自动选择本地数据源、OpenAI、Gemini、Voyage 或 Mistral。
- **QMD 后端（QMD backend）**：可选的本地优先处理方式（结合 BM25 和向量搜索结果）。

有关完整的内存配置信息，请参阅 `references/memory.md`。

---

## 工具概述

| 工具（Tools） | 用途 |
|------|---------|
| `exec` | 执行 Shell 命令（在沙箱、网关或节点上） |
| `process` | 管理后台进程 |
| `browser` | 使用 Chromium 自动化功能（导航、点击、输入、截图） |
| `web_search` | 使用 Brave Search API 进行搜索 |
| `web_fetch` | 从 URL 提取 Markdown 内容 |
| `memory_search` | 对内存数据进行语义向量搜索 |
| `memory_get` | 直接读取内存文件内容 |
| `message` | 支持跨通道消息传递（发送、回复、创建线程、固定消息、发起投票） |
| `sessions_spawn` | 启动子代理（一次性或持久化，最多支持 5 层嵌套） |
| `canvas` | 在连接的设备上显示 HTML 内容 |
| `nodes` | 控制配对设备（拍照/截图、屏幕录制、显示通知、使用 Canvas UI） |
| `pdf` | 支持原生 PDF 分析（最多处理 10 个 PDF 文件，支持 Anthropic/Google 的原生解析方式） |

**访问控制**：支持不同的用户配置级别（`minimal`、`coding`、`messaging`、`full`），以及工具使用权限控制（如 `group:fs`、`group:runtime` 等）。默认配置为 `messaging`（自 2026.3.2 版本起）。

有关所有工具、技能和钩子的详细信息，请参阅 `references/tools.md`。

---

## 钩子（Hooks）与自动化（Automation）

**钩子（Hooks）**：位于 `<workspace>/hooks/` 目录下的 TypeScript 事件处理程序：

| 事件（Event） | 触发条件（Trigger） |
|-------|---------|
| `command:new/reset/stop` | 会话生命周期相关操作 |
| `agent:bootstrap` | 初始化前执行（可修改配置文件） |
| `gateway:startup` | 通道加载完成后执行 |
| `message:received/sent` | 消息处理相关操作 |
| `tool_result_persist` | 同步处理工具返回的结果 |

**自动化（Automation）**：内置在网关中：
- **Cron**：支持定时任务（使用 Cron 表达式或间隔执行，支持单独执行或与主会话关联）。
- **Webhooks**：`/hooks/wake`（系统事件触发），`/hooks/agent`（针对特定代理的触发）。
- **Heartbeat**：定期检查机制（默认每 30 分钟执行一次）。

**语音功能（Voice）**：在 macOS/iOS 上支持唤醒词和语音交互；在 Android 上支持 ElevenLabs 或系统 TTS；支持 OpenAI 兼容的文本转语音（STT）服务（`messages.tts.openai.baseUrl`）。

---

## 部署选项（Deployment Options）

**云部署（Cloud Deployment）**：支持 Fly.io、Railway、Render、GCP、Hetzner、Cloudflare Workers 和 Ansible 等平台。
**沙箱环境（Sandbox）**：为不受信任的会话提供 Docker 隔离环境。支持 `off`、`non-main`、`all` 三种模式；配置范围包括 `session`、`agent` 和 `shared`。
**远程访问（Remote access）**：推荐使用 Tailscale/VPN，必要时可切换到 SSH 隧道。

有关完整的部署指南，请参阅 `references/deployment.md`。

---

## 命令行接口（CLI Essentials）

| 命令（Command） | 用途 |
|---------|---------|
| `openclaw onboard` | 交互式的首次设置 |
| `openclaw gateway start/stop/status` | 管理网关服务 |
| `openclaw channels add/list/status/login` | 管理通道 |
| `openclaw models list/set/auth/scan` | 管理模型配置和认证 |
| `openclaw skills list/info/check` | 管理技能 |
| `openclaw hooks list/enable/disable/install` | 管理钩子 |
| `openclaw agent --message "..."` | 控制单个代理 |
| `openclaw agents list/add/delete` | 管理多个代理 |
| `openclaw sessions` | 查看和管理会话 |
| `openclaw browser` | 提供浏览器控制接口（支持 50 多个子命令） |
| `openclaw cron list/add/run` | 安排定时任务 |
| `openclaw nodes status` | 查看配对的辅助节点状态 |
| `openclaw devices list/approve` | 管理设备配对请求 |
| `openclaw config get/set/unset/validate` | 帮助配置文件（启动前进行验证） |
| `openclaw doctor [--fix]` | 检查系统健康状况并进行自动修复 |
| `openclaw security audit [--deep]` | 进行安全审计 |
| `openclaw logs [--follow]` | 查看网关日志 |
| `openclaw memory search "query"` | 执行向量搜索 |
| `openclaw dns setup` | 配置 CoreDNS 和 Tailscale 发现服务 |
| `openclaw tui` | 提供终端界面 |

**全局参数（Global flags）**：`--dev`、`--profile <name>`、`--json`、`--no-color` 等。

---

## 参考文件说明

- 如需了解 `openclaw.json` 的完整内容、模型提供者、环境变量、认证设置、OAuth 配置等，请参阅 `references/configuration.md`。
- 有关各通道的设置、路由规则、访问控制、流媒体传输、多账户支持等信息，请参阅 `references/channels.md`。
- 了解内存文件、向量搜索、QMD、嵌入技术、混合搜索等细节，请参阅 `references/memory.md`。
- 关于工具的使用、代理管理、节点配置等，请参阅 `references/tools.md`。
- 有关 Docker 部署、云服务部署、沙箱环境、原生安装和安全性设置，请参阅 `references/deployment.md`。
- 了解多代理配置、代理绑定、广播功能、子代理管理等内容，请参阅 `references/multi-agent.md`。