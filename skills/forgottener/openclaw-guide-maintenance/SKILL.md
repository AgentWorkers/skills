---
name: openclaw-guide-maintenance
description: >
  **OpenClaw 安装、配置、使用及故障排除综合指南**  
  本指南适用于需要了解 OpenClaw 设置、配置、渠道管理（包括 WhatsApp/Telegram/Discord/Slack/iMessage 等）、模型提供商配置、网关操作、多代理路由、安全加固、故障排除以及与本地 OpenClaw 安装相关的维护任务的用户。同时，也适用于遇到 `openclaw` 命令行工具（CLI）或网关守护进程（daemon）相关错误的情况。
  **OpenClaw 简介：**  
  OpenClaw 是一个自托管的多通道 AI 代理网关，支持多种通信协议，可灵活配置和管理多个 AI 代理。它提供了强大的功能，帮助用户高效地构建和部署 AI 应用程序。
  **主要内容：**  
  1. **安装指南**：详细介绍如何在您的系统上安装 OpenClaw。  
  2. **配置指南**：讲解如何根据实际需求配置 OpenClaw 的各项参数和设置。  
  3. **使用指南**：介绍如何使用 OpenClaw 的核心功能，包括代理管理、模型调用等。  
  4. **故障排除**：提供针对常见问题的解决方案和排查步骤。  
  5. **安全加固**：指导用户如何增强 OpenClaw 的安全性，防止潜在的安全风险。  
  6. **维护与升级**：介绍如何对 OpenClaw 进行定期维护和升级，以确保其稳定运行。
  **适用场景：**  
  - 对 OpenClaw 的安装和配置有疑问的用户  
  - 需要管理多个通信渠道的用户  
  - 需要使用 OpenClaw 连接外部模型服务或代理的用户  
  - 遇到系统或应用程序故障的用户  
  **注意事项：**  
  - 请确保您已具备必要的系统权限和软件依赖项（如 Python、Node.js 等）。  
  - 在进行任何配置更改之前，请务必备份数据，以防意外情况发生。  
  - 如遇到技术问题，请参考官方文档或联系技术支持团队。
version: 2026.3.8
tags: openclaw, gateway, devops, self-hosted, multi-channel, ai-agent
license: MIT
---
# OpenClaw 维护技能

OpenClaw 是一个自托管的开源（MIT 许可）网关，能够同时将 AI 代理路由到 WhatsApp、Telegram、Discord、Slack、iMessage、Signal 以及 15 个以上的其他渠道。它支持在 macOS、Linux 或 Windows 上运行。

## 参考文件

| 文件名 | 内容覆盖 |
|---|---|
| [channels.md] | 各渠道的设置（WhatsApp、Telegram、Discord 等） |
| [channel_troubleshooting.md] | 各渠道的故障特征及故障排除步骤 |
| [tools.md] | 工具清单（配置文件、群组、所有内置工具） |
| [exec.md] | 执行工具：参数、配置、PATH、安全性、进程工具 |
| [exec_approvals.md] | 执行权限审批：允许列表、安全策略、审批流程 |
| [browser.md] | 浏览器工具：配置文件、CDP、中继、SSRF、控制 API |
| [web_tools.md] | Web 工具：Brave、Perplexity、Gemini 搜索提供者 |
| [pdf_tool.md] | PDF 工具：原生/备用模式、配置、页面筛选 |
| [elevated.md] | 提高权限模式：/elevated 指令、沙箱突破 |
| [lobster.md] | Lobster：带审批功能的流程运行工具 |
| [llm_task.md] | LLM 任务：用于结构化输出的 JSON 格式任务 |
| [openprose.md] | OpenProse：多代理程序运行环境 |
| [plugins.md] | 插件：官方列表、配置、管理、命令行接口（CLI） |
| [skills.md] | 技能：位置信息、配置、ClawHub、观察器、令牌影响 |
| [providers.md] | 模型提供者设置 |
| [multi_agent.md] | 多代理路由 |
| [nodes.md] | 节点（iOS/Android/macOS/无头节点） |
| [security.md] | 安全性强化 |
| [secrets.md] | 秘密管理（SecretRef、保险库） |
| [sandboxing.md] | 沙箱机制（Docker 隔离） |
| [config_reference.md] | 完整配置字段参考 |
| [gateway_ops.md] | 网关操作 |
| [remote_access.md] | 远程访问、SSH、Tailscale、Web 控制面板 |
| [sessions.md] | 会话管理、私信隔离、生命周期、数据压缩 |
| [hooks.md] | 钩子：内部事件钩子、HTTP Webhook、命令行接口（CLI） |
| [automation.md] | Cron 作业、Webhook、Gmail Pub/Sub |
| [acpAgents.md] | ACP 代理：启动外部 AI 运行时（Codex、Claude 等） |
| [install.md] | 安装、更新、回滚、迁移、卸载 |
| [web_ui.md] | Web 界面：控制面板、控制 UI、WebChat |
| [slash_commands.md] | 聊天快捷命令（/new、/model、/acp 等） |
| [platforms.md] | 平台特定指南（macOS、iOS、Android、Linux、Windows） |
| [diffs_firecrawl.md] | Diffs 插件 + Firecrawl 反机器人机制 |
| [subagents.md] | 子代理：嵌套启动、线程绑定、通知、工具策略 |
| [memory.md] | 内存系统、向量搜索、混合 BM25、数据压缩、QMD 后端 |
| [architecture.md] | 网关架构、通信协议、配对规则 |
| [agent_runtime.md] | 代理运行时、启动文件、代理循环、钩子、超时设置 |
| [streaming.md] | 流式传输与分块处理：块传输、合并、预览模式 |
| [queue.md] | 命令队列：模式（引导/跟进/收集）、并发处理、会话级处理 |
| [model_failover.md] | 模型故障转移、OAuth、认证配置、冷却时间、计费禁用 |
| [clawhub.md] | ClawHub：公共技能注册表、CLI 命令、发布/安装 |
| [thinking.md] | 思维层次、详细指令、推理可见性 |
| [polls.md] | 投票功能（Telegram、WhatsApp、Discord、MS Teams） |
| [voice.md] | 语音交互模式 + 语音唤醒（唤醒词） |
| [presence_discovery.md] | 在线状态检测系统、发现机制（Bonjour/Tailscale） |
| [gateway_internals.md] | 网关内部机制、网络模型、健康检查、日志记录、后台执行 |
| [heartbeat.md] | 心跳机制：配置、传输、可见性 |
| [bonjour.md] | Bonjour/mDNS：TXT 密钥、广域 DNS-SD、调试模式 |
| [pairing.md] | 网关配对：节点审批、CLI、API、自动审批、存储 |
| [tui.md] | 图形用户界面（TUI）：快捷键、快捷命令、本地 shell、传输功能 |
| [media.md] | 媒体处理：摄像头捕获、图片、音频/语音笔记、转录 |

## 快速参考

### 关键路径

| 路径 | 用途 |
|---|---|
| `~/.openclaw/openclaw.json` | 主配置文件（JSON5 格式） |
| `~/.openclaw/.env` | 全局环境变量 |
| `~/.openclaw/workspace` | 默认代理工作空间 |
| `~/.openclaw/agents/<id>/` | 代理状态及会话信息 |
| `~/.openclaw/agents/<id>/qmd/` | QMD 内存后端状态 |
| `~/.openclaw/agents/<id>/agent/auth-profiles.json` | 认证配置文件及 OAuth 令牌 |
| `OPENCLAW_CONFIG_PATH` | 配置文件路径覆盖选项 |
| `OPENCLAW_STATE_DIR` | 状态目录覆盖选项 |
| `OPENCLAW_HOME` | 主目录覆盖选项 |

### 基本命令

```
openclaw status                    # Overall status
openclaw gateway status            # Gateway daemon status
openclaw gateway status --deep     # Deep scan including system services
openclaw doctor                    # Diagnose config/service issues
openclaw doctor --fix              # Auto-fix safe issues
openclaw logs --follow             # Tail gateway logs
openclaw channels status --probe   # Channel health check
openclaw security audit            # Security posture check
openclaw security audit --fix      # Auto-fix security issues
openclaw update                    # Self-update
openclaw dashboard                 # Open Control UI in browser
openclaw tui                       # Terminal UI (interactive REPL, auto-infers agent from cwd)
openclaw agent                     # Direct agent interaction via CLI
openclaw health                    # Health check
openclaw usage                     # Usage tracking
openclaw config validate           # Validate config file
openclaw config file               # Print active config path
openclaw sessions cleanup          # Session disk cleanup
openclaw agents bindings           # Agent-channel bindings
openclaw agents bind               # Bind agent to account
openclaw agents unbind             # Unbind agent
openclaw update --dry-run          # Preview update
openclaw backup create             # Create local state archive
openclaw backup verify             # Verify backup integrity
openclaw system presence           # View connected clients/nodes
openclaw system heartbeat last     # Last heartbeat info
openclaw system heartbeat now      # Trigger heartbeat immediately
openclaw memory search <query>     # CLI memory search
openclaw docs <query>              # Search OpenClaw docs
openclaw nodes pending             # List pending pairing requests
openclaw nodes approve <id>        # Approve node pairing
openclaw health --json             # Full health snapshot (JSON)
openclaw message send --media <p>  # Send media message
```

### 默认网关设置

- 绑定地址：`127.0.0.1:18789`（回环地址）
- 控制面板地址：`http://127.0.0.1:18789/`
- 协议：WebSocket（JSON 文本帧）

## 核心工作流程

### 故障诊断

请始终按照以下步骤进行故障排查：

1. `openclaw status` — 快速概览
2. `openclaw gateway status` — 服务是否运行？RPC 探针是否正常？
3. `openclaw logs --follow` — 监控错误日志
4. `openclaw doctor` — 配置/服务诊断
5. `openclaw channels status --probe` — 检查各渠道的状态

### 启动/重启网关

```bash
# Foreground with verbose logging
openclaw gateway --port 18789 --verbose

# Force-kill existing listener then start
openclaw gateway --force

# Service management (launchd on macOS, systemd on Linux)
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
```

### 配置修改

可以通过任何方式修改配置：

```bash
# Interactive wizard
openclaw onboard                    # Full setup
openclaw configure                  # Config wizard

# CLI one-liners
openclaw config get <path>          # Read value
openclaw config set <path> <value>  # Set value (JSON5 or raw string)
openclaw config unset <path>        # Remove value

# Direct edit
# Edit ~/.openclaw/openclaw.json (JSON5 format)
# Gateway hot-reloads on save (if gateway.reload.mode != "off")
```

### 最小配置示例：

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

### 渠道设置

有关各渠道的详细设置，请参阅 [references/channels.md]。
有关各渠道的故障排除（故障特征、设置步骤），请参阅 [references/channel_troubleshooting.md]。
有关添加新渠道（如 Matrix、Nostr、MS Teams 等）的插件，请参阅 [references/plugins.md]。

### 快速添加渠道：

```bash
# Interactive wizard
openclaw channels add

# Non-interactive
openclaw channels add --channel telegram --account default --name "My Bot" --token $BOT_TOKEN
openclaw channels login --channel whatsapp     # QR pairing for WhatsApp
openclaw channels status --probe               # Verify
```

### 模型提供者设置

有关模型提供者的详细设置，请参阅 [referencesproviders.md]。

```bash
# Set default model
openclaw models set anthropic/claude-sonnet-4-5

# List available models
openclaw models list --all

# Check auth/token status
openclaw models status --probe

# Add auth interactively
openclaw models auth add
```

### 多代理路由配置

有关多代理的详细配置，请参阅 [references/multi_agent.md]。

```bash
openclaw agents add <id>                # Create agent
openclaw agents list --bindings         # Show agent-channel bindings
openclaw agents delete <id>             # Remove agent
```

### 节点设置（iOS / Android / macOS / 无头节点）

有关节点的详细设置，请参阅 [references/nodes.md]。

```bash
openclaw nodes status                   # List connected nodes
openclaw nodes describe --node <id>     # Node capabilities
openclaw devices list                   # Pending device approvals
openclaw devices approve <requestId>    # Approve a device
openclaw node run --host <host> --port 18789  # Start headless node host
```

### 安全性

有关安全性的详细信息，请参阅 [references/security.md]。
有关秘密管理（SecretRef、保险库集成），请参阅 [references/secrets.md]。
有关沙箱机制（工具的 Docker 隔离），请参阅 [references/sandboxing.md]。
有关完整的配置字段参考，请参阅 [references/config_reference.md]。
有关远程访问（SSH、Tailscale、VPN），请参阅 [references/remote_access.md]。

```bash
openclaw security audit                 # Check posture
openclaw security audit --deep          # Live gateway probe
openclaw security audit --fix           # Auto-fix safe issues
openclaw secrets reload                 # Re-resolve secret refs
openclaw secrets audit                  # Scan for plaintext leaks
```

### 更新/卸载

有关安装、更新、回滚和迁移的详细指南，请参阅 [references/install.md]。

```bash
# Install (recommended)
curl -fsSL https://openclaw.ai/install.sh | bash

# Update
openclaw update                    # Self-update command
# Or: npm install -g openclaw@latest
openclaw doctor                    # Run after update to apply migrations

# Uninstall
openclaw uninstall
```

## 工具参考

有关各工具的详细文档，请参阅 [references/tools.md]。

具体工具的详细信息如下：
- [references/exec.md] — 执行工具的详细说明 |
- [references/exec_approvals.md] — 执行权限审批和允许列表 |
- [references/browser.md] — 浏览器自动化功能的详细说明 |
- [references/web_tools.md] | 多提供者的 Web 搜索/获取功能 |
- [references/lobster.md] | Lobster 流程运行工具 |
- [references/llm_task.md] | 用于结构化 JSON 输出的 LLM 任务 |
- [references/openprose.md] | OpenProse 多代理程序 |
- [references/plugins.md] | 插件系统（安装、管理、分发） |
- [references/skills.md] | 技能系统（加载、配置、ClawHub）

有关 ACP 代理（Codex、Claude Code、Gemini CLI 等），请参阅 [references/acpAgents.md]。
有关 Diffs 插件和 Firecrawl 反机器人机制，请参阅 [references/diffs_firecrawl.md]。
有关聊天快捷命令（/new、/model、/acp 等），请参阅 [references/slash_commands.md]。

有关高级内部机制和功能，请参阅：
- [references/thinking.md] | 思维层次（/think、/verbose、/reasoning） |
- [references/polls.md] | 投票功能（Telegram、WhatsApp、Discord、MS Teams） |
- [references/voice.md] | 语音交互模式和语音唤醒 |
- [references/architecture.md] | 网关架构和通信协议 |
- [references/agent_runtime.md] | 代理运行时和循环细节 |
- [references/queue.md] | 命令队列系统 |
- [references/model_failover.md] | 模型故障转移和 OAuth |
- [references/clawhub.md] | ClawHub 技能注册表 |
- [references/presence_discovery.md] | 在线状态检测和发现机制 |
- [references/streaming.md] | 流式传输和分块处理 |
- [references/gateway_internals.md] | 网关内部机制 |
- [references/heartbeat.md] | 心跳机制 |
- [references/bonjour.md] | Bonjour/mDNS 发现机制 |
- [references/pairing.md] | 网关节点配对 |
- [references/tui.md] | 图形用户界面（TUI） |
- [references/media.md] | 媒体处理（摄像头、图片、音频） |
- [references/channel_routing.md] | 渠道路由和会话密钥

**工具配置文件**：`minimal`、`coding`、`messaging`、`full`（默认）。

**工具组**（用于权限控制）：
- `group:runtime` — 执行工具、bash、进程工具 |
- `group:fs` — 读写、编辑、应用补丁 |
- `group:sessions` — 会话列表/历史记录/发送/启动、会话状态 |
- `group:memory` — 内存搜索、内存获取 |
- `group:web` — Web 搜索、Web 数据获取 |
- `group:ui` — 浏览器、画布工具 |
- `group:automation` | Cron 作业、网关工具 |
- `group:messaging` — 消息工具 |
- `group:nodes` — 节点工具 |
- `group:openclaw` — 所有内置 OpenClaw 工具（不包括插件）

## 常见故障特征

| 错误 | 原因 | 解决方法 |
|---|---|---|
| `拒绝绑定网关……未提供认证` | 未使用令牌进行回环绑定 | 设置 `gateway.auth.token` 或 `gateway.auth.password` |
| `另一个网关实例已在监听` / `EADDRINUSE` | 端口冲突 | 使用 `openclaw gateway --force` 或更改端口 |
| `网关启动受阻` | 未启用本地模式 | 设置 `gateway.mode="local"` |
| `未经授权` / 重新连接循环 | 令牌/密码不匹配 | 检查 `OPENCLAW_GATEWAY_TOKEN` 或配置文件中的认证信息 |
| 需要设备身份验证 | 客户端未完成连接挑战流程 | 确保客户端完成连接挑战 |
| 机器人无响应 | 配对/允许列表/提及限制 | 检查 `openclaw pairing list`、私信策略、提及模式 |

## 环境变量

| 变量 | 用途 |
|---|---|
| `OPENCLAW_GATEWAY_TOKEN` | 网关认证令牌 |
| `OPENCLAW_GATEWAY_PASSWORD` | 网关认证密码 |
| `OPENCLAW_GATEWAY_PORT` | 网关端口覆盖值 |
| `OPENCLAW_CONFIG_PATH` | 配置文件路径覆盖值 |
| `OPENCLAW_STATE_DIR` | 状态目录覆盖值 |
| `OPENCLAW_HOME` | 主目录覆盖值 |
| `OPENCLAW_LOAD_SHELL_ENV` | 导入 shell 环境变量（设置为 `1`） |
| `OPENCLAW_VERBOSE` | 日志记录详细程度 |
| `OPENCLAW_LOG_FILE` | 日志文件路径 |
| `OPENCLAW_LOG_LEVEL` | 日志记录级别控制 |
| `OPENCLAW_SHELL` | 由 OpenClaw 在执行/ACP/TUI 运行时设置 |
| `OPENCLAW THEME` | 终端主题（`light` 或 `dark`） |
| `OPENCLAW_BIND_mount_OPTIONS` | Podman SELinux 的绑定挂载选项（例如：`:z） |
| `BRAVE_API_KEY` | 用于 Web 搜索工具 |
| `FIRECRAWL_API_KEY` | 用于 Firecrawl 反机器人机制 |
| `ELEVENLABS_API_KEY` | 用于语音交互模式 |
| `ELEVENLABS_VOICE_ID` | 语音交互模式的默认语音 |
| `CLAWHUB_TOKEN` | ClawHub API 令牌（用于 CI/自动化） |
| `CLAWHUB_WORKDIR` | ClawHub 工作目录覆盖值 |
| `CLAWHUB_REGISTRY` | ClawHub 注册表 API URL 覆盖值 |
| `OLLAMA_API_KEY` | 用于 Ollama 嵌入模型的 API |