---
name: openclaw-guide-maintenance
description: >
  **OpenClaw 安装、配置、使用及故障排除综合指南**
  本指南适用于需要了解 OpenClaw 安装、配置、操作及故障排除的用户。OpenClaw 是一个自托管的多通道 AI 代理网关，支持与 WhatsApp、Telegram、Discord、Slack、iMessage 等平台进行通信。本指南涵盖了以下内容：
  - **安装流程**：指导用户如何在不同操作系统（如 Linux、macOS 和 Windows）上安装 OpenClaw。
  - **配置指南**：详细介绍如何配置 OpenClaw 的各项参数，以满足特定需求（如通道设置、模型源配置等）。
  - **操作指南**：说明如何使用 OpenClaw 的核心功能（如发送消息、接收消息、管理代理等）。
  - **故障排除**：提供针对常见问题的解决方案，帮助用户快速定位并解决问题。
  - **维护与优化**：介绍如何对 OpenClaw 进行维护和优化，以确保其稳定运行。
  **适用场景**：
  - 当用户询问 OpenClaw 的安装或配置方法时。
  - 当用户需要管理 OpenClaw 支持的通信渠道时。
  - 当用户遇到与 OpenClaw 相关的错误或问题时（例如，`openclaw` 命令或网关守护进程出现异常）。
  **使用建议**：
  - 在用户遇到技术问题时，首先查阅本指南以获取基本解决方案。
  - 如果问题仍未解决，请查阅 OpenClaw 的官方文档或联系技术支持。
  - 请确保您已阅读并理解本指南中的所有步骤和注意事项，以确保正确安装和配置 OpenClaw。
  希望本指南能帮助您更好地使用 OpenClaw！
version: 2026.3.9
tags: openclaw, gateway, devops, self-hosted, multi-channel, ai-agent
license: MIT
---
# OpenClaw 维护技能

OpenClaw 是一个自托管的开源（MIT 许可）工具，它能够同时将 AI 代理路由到 WhatsApp、Telegram、Discord、Slack、iMessage、Signal 以及 15 种以上的其他渠道。该工具支持在 macOS、Linux 或 Windows 上运行。

## 参考文件

| 文件名 | 内容覆盖 |
| --- | --- |
| [channels.md] | 各渠道的设置（WhatsApp、Telegram、Discord 等） |
| [channel_troubleshooting.md] | 各渠道的故障特征及排查步骤 |
| [tools.md] | 所有内置工具的清单 |
| [exec.md] | 执行工具：参数、配置、PATH、安全性、进程管理 |
| [exec_approvals.md] | 执行权限审批：允许列表、安全策略、审批流程 |
| [browser.md] | 浏览器工具：配置文件、CDP、中继、SSRF、控制 API |
| [web_tools.md] | Web 工具：Brave、Perplexity、Gemini 搜索提供者 |
| [pdf_tool.md] | PDF 工具：原生/备用模式、配置、页面筛选 |
| [elevated.md] | 提升模式：特殊指令、沙箱隔离 |
| [lobster.md] | Lobster 工作流运行时（支持审批） |
| [llm_task.md] | LLM 任务：用于结构化输出的 JSON 格式 |
| [openprose.md] | OpenProse：多代理程序运行时 |
| [plugins.md] | 插件列表、配置、管理、命令行接口（CLI） |
| [skills.md] | 技能系统：位置信息、配置、ClawHub、监控机制、令牌影响 |
| [providers.md] | 模型提供者设置 |
| [multi_agent.md] | 多代理路由 |
| [nodes.md] | 节点配置（iOS/Android/macOS/无头服务器） |
| [security.md] | 安全性强化 |
| [secrets.md] | 秘密管理（SecretRef、安全库） |
| [sandboxing.md] | 沙箱隔离（Docker） |
| [config_reference.md] | 完整配置字段参考 |
| [gateway_ops.md] | 网关操作 |
| [remote_access.md] | 远程访问（SSH、Tailscale、Web 控制面板） |
| [sessions.md] | 会话管理、私信隔离、生命周期管理 |
| [hooks.md] | 内部事件钩子、HTTP Webhook、命令行接口（CLI） |
| [automation.md] | Cron 任务、Webhook、Gmail Pub/Sub |
| [acpAgents.md] | ACP 代理：启动外部 AI 运行时（如 Codex、Claude 等） |
| [install.md] | 安装、更新、回滚、迁移、卸载 |
| [web_ui.md] | Web 界面（控制面板、WebChat） |
| [slash_commands.md] | 聊天命令（/new、/model 等） |
| [platforms.md] | 平台特定指南（macOS、iOS、Android、Linux、Windows） |
| [diffs_firecrawl.md] | Diffs 插件与 Firecrawl 反机器人机制 |
| [subagents.md] | 子代理管理（嵌套启动、线程绑定、通知机制） |
| [memory.md] | 内存系统、向量搜索、混合 BM25 索引、数据压缩 |
| [architecture.md] | 网关架构、通信协议、节点配对规则 |
| [agent_runtime.md] | 代理运行时、启动文件、代理循环、钩子机制 |
| [streaming.md] | 流式传输与分块处理 |
| [queue.md] | 命令队列（不同执行模式、并发处理、会话管理） |
| [model_failover.md] | 模型故障转移、OAuth 认证 |
| [clawhub.md] | ClawHub 技能注册系统、CLI 命令 |
| [thinking.md] | 思维模式、详细指令、推理可视化 |
| [polls.md] | 调查功能（Telegram、WhatsApp、Discord、MS Teams） |
| [voice.md | 语音交互功能及唤醒机制 |
| [presence_discovery.md] | 在线状态检测与发现机制 |
| [gateway_internals.md] | 网关内部机制（网络模型、锁机制、健康检查） |
| [heartbeat.md] | 心跳机制：配置与日志记录 |
| [bonjour.md] | Bonjour/mDNS 协议、DNS-SD 功能、调试工具 |
| [pairing.md] | 网关配对机制（节点审批、CLI、API、自动配对） |
| [tui.md] | 图形用户界面（TUI）：快捷键、命令行操作 |
| [media.md] | 媒体处理（摄像头采集、图片、音频/语音记录） |
| [channel_routing.md] | 渠道路由与会话管理 |

## 快速参考

### 关键路径

| 路径 | 用途 |
| --- | --- |
| `~/.openclaw/openclaw.json` | 主配置文件（JSON5 格式） |
| `~/.openclaw/.env` | 全局环境变量 |
| `~/.openclaw/workspace` | 默认代理工作区 |
| `~/.openclaw/agents/<id>/` | 代理状态及会话信息 |
| `~/.openclaw/agents/<id>/qmd/` | QMD 内存后端状态 |
| `~/.openclaw/agents/<id>/agent/auth-profiles.json` | 认证配置与 OAuth 令牌 |
| `OPENCLAW_CONFIG_PATH` | 配置文件路径覆盖选项 |
| `OPENCLAW_STATE_DIR` | 状态数据目录覆盖选项 |
| `OPENCLAW_HOME` | 主程序安装目录覆盖选项 |

### 常用命令

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

### 默认配置

- 绑定代理：`127.0.0.1:18789`（回环地址）
- 控制面板：`http://127.0.0.1:18789/`
- 协议：WebSocket（JSON 文本帧）

## 核心工作流程

### 故障排查

请按照以下步骤进行故障排查：

1. `openclaw status` — 获取系统概览
2. `openclaw gateway status` — 检查守护进程是否运行正常
3. `openclaw logs --follow` — 监控错误日志
4. `openclaw doctor` — 查看配置与服务诊断信息
5. `openclaw channels status --probe` — 检查各渠道状态

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

可以通过任意方式修改配置文件：

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

**最小配置示例：**

```json5
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
  channels: { whatsapp: { allowFrom: ["+15555550123"] } },
}
```

### 渠道设置

详细配置指南请参见 [references/channels.md]。
针对各渠道的故障排查及设置步骤，请参阅 [references/channel_troubleshooting.md]。
如需添加新渠道（Matrix、Nostr、MS Teams 等），请参考 [references/plugins.md]。

**快速添加渠道：**

```bash
# Interactive wizard
openclaw channels add

# Non-interactive
openclaw channels add --channel telegram --account default --name "My Bot" --token $BOT_TOKEN
openclaw channels login --channel whatsapp     # QR pairing for WhatsApp
openclaw channels status --probe               # Verify
```

### 模型提供者配置

详细配置指南请参见 [references/providers.md]。

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

**配置示例：**

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],
      },
    },
  },
}
```

### 多代理路由

详细配置指南请参见 [references/multi_agent.md]。

```bash
openclaw agents add <id>                # Create agent
openclaw agents list --bindings         # Show agent-channel bindings
openclaw agents delete <id>             # Remove agent
```

### 节点配置（iOS / Android / macOS / 无头服务器）

详细节点配置指南请参见 [references/nodes.md]。

```bash
openclaw nodes status                   # List connected nodes
openclaw nodes describe --node <id>     # Node capabilities
openclaw devices list                   # Pending device approvals
openclaw devices approve <requestId>    # Approve a device
openclaw node run --host <host> --port 18789  # Start headless node host
```

### 安全性

安全强化措施请参见 [references/security.md]。
秘密管理（SecretRef、安全库集成）请参阅 [references/secrets.md]。
沙箱隔离（Docker）请参阅 [references/sandboxing.md]。
完整配置字段参考请参见 [references/config_reference.md]。
远程访问（SSH、Tailscale、VPN）请参阅 [references/remote_access.md]。

```bash
openclaw security audit                 # Check posture
openclaw security audit --deep          # Live gateway probe
openclaw security audit --fix           # Auto-fix safe issues
openclaw secrets reload                 # Re-resolve secret refs
openclaw secrets audit                  # Scan for plaintext leaks
```

### 安装/卸载

安装、更新、回滚及迁移指南请参见 [references/install.md]。

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

详细工具文档请参见 [references/tools.md]。

具体工具说明：
- [references/exec.md]：执行工具详解
- [references/exec_approvals.md]：执行权限审批与允许列表
- [references/browser.md]：浏览器自动化功能
- [references/web_tools.md]：多源搜索与数据获取
- [references/lobster.md]：Lobster 工作流运行时
- [references/llm_task.md]：用于结构化输出的 LLM 任务
- [references/openprose.md]：OpenProse 多代理程序
- [references/plugins.md]：插件系统（安装、管理）
- [references/skills.md]：技能系统（加载、配置、管理）

关于 ACP 代理（Codex、Claude Code、Gemini CLI 等），请参阅 [references/acpAgents.md]。
Diffs 插件与 Firecrawl 反机器人机制请参阅 [references/diffs_firecrawl.md]。
聊天命令（/new、/model 等）请参阅 [references/slash_commands.md]。

高级内部机制与功能请参阅：
- [references/thinking.md]：思维模式与详细设置
- [references/polls.md]：调查功能（Telegram、WhatsApp、Discord、MS Teams）
- [references/voice.md]：语音交互与唤醒机制
- [references/architecture.md]：网关架构与通信协议
- [references/agent_runtime.md]：代理运行时与循环逻辑
- [references/queue.md]：命令队列系统
- [references/model_failover.md]：模型故障转移与 OAuth 认证
- [references/clawhub.md]：ClawHub 技能注册系统
- [references/presence_discovery.md]：在线状态检测与发现机制
- [references/streaming.md]：流式传输与数据分块
- [references/gateway_internals.md]：网关内部机制
- [references/heartbeat.md]：心跳机制与日志记录
- [references/bonjour.md]：Bonnier/mDNS 协议与调试工具
- [references/pairing.md]：网关节点配对
- [references/tui.md]：图形用户界面（TUI）
- [references/media.md]：媒体处理（摄像头、图片、音频）
- [references/channel_routing.md]：渠道路由与会话管理

**工具配置文件示例**：`minimal`、`coding`、`messaging`、`full`（默认值）。

**工具分组**（用于权限控制）：
- `group:runtime`：执行相关工具（如 exec、bash、进程管理）
- `group:fs`：文件读写、编辑、应用补丁
- `group:sessions`：会话管理（列表、历史记录、发送、启动）
- `group:memory`：内存搜索、数据获取
- `group:web`：Web 搜索与数据获取
- `group:ui`：浏览器、画布操作
- `group:automation`：Cron 任务、网关控制
- `group:messaging`：消息传递
- `group:nodes`：节点管理
- `group:openclaw`：所有内置 OpenClaw 工具（不包括插件）

## 常见故障原因及解决方法

| 错误 | 原因 | 解决方案 |
| --- | --- |
| “拒绝绑定网关……未提供认证信息” | 未使用令牌进行回环绑定 | 设置 `gateway.auth.token` 或 `gateway.auth.password` |
| “另一个网关实例正在监听” / `EADDRINUSE` | 端口冲突 | 使用 `openclaw gateway --force` 或更改端口 |
| “网关启动失败” | 未启用本地模式 | 设置 `gateway.mode="local"` |
| “未经授权” / 重新连接循环 | 令牌/密码不匹配 | 检查 `OPENCLAW_GATEWAY_TOKEN` 或配置文件中的认证信息 |
| “需要设备身份验证” | 客户端未完成连接流程 | 确保客户端完成认证流程 |
| 机器人无响应 | 配置问题或允许列表设置 | 检查 `openclaw pairing list`、私信策略 |
| “嵌入提供者认证失败（401）” | 配置文件中的 API 密钥为占位符 | 更换为实际 API 密钥并重启网关 |
| “配置更改需重启网关” | 插件配置无法热加载 | 完整重启网关或使用 `launchctl kickstart -k` |
| “启动失败：输入/输出错误” | LaunchAgent plist 文件损坏 | 先安装网关，再使用 `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` |
| “配置文件中引用变量缺失” | 配置文件中的变量未定义 | 在 `~/.openclaw/.env` 中添加变量并重启网关 |

## 环境变量

| 变量 | 用途 |
| --- | --- |
| `OPENCLAW_GATEWAY_TOKEN` | 网关认证令牌 |
| `OPENCLAW_GATEWAY_PASSWORD` | 网关认证密码 |
| `OPENCLAW_GATEWAY_PORT` | 网关端口 |
| `OPENCLAW_CONFIG_PATH` | 配置文件路径 |
| `OPENCLAW_STATE_DIR` | 状态数据目录 |
| `OPENCLAW_HOME` | 主程序安装目录 |
| `OPENCLAW_LOAD_SHELL_ENV` | 设置 shell 环境变量 |
| `OPENCLAW_VERBOSE` | 日志记录级别 |
| `OPENCLAW_LOG_FILE` | 日志文件路径 |
| `OPENCLAW_LOG_LEVEL` | 日志记录级别控制 |
| `OPENCLAW_SHELL` | 由 OpenClaw 在运行时设置 |
| `OPENCLAW THEME` | 终端主题（light 或 dark） |
| `OPENCLAW_BIND_mount'options` | Podman SELinux 配置选项 |
| `BRAVE_API_KEY` | Web 搜索工具相关 |
| `FIRECRAWL_API_KEY` | Firecrawl 反机器人机制相关 |
| `ELEVENLABS_API_KEY` | 语音交互相关 |
| `ELEVENLABS_VOICE_ID` | 默认语音设置 |
| `CLAWHUB_TOKEN` | ClawHub API 令牌 |
| `CLAWHUB_WORKDIR` | ClawHub 工作目录 |
| `CLAWHUB_REGISTRY` | ClawHub 注册表 API 地址 |
| `OLLAMA_API_KEY` | Ollama 嵌入模型相关 |