---
name: openclaw-expert
description: OpenClaw（前身为Clawdbot/MoltBot）是一款自托管的AI代理框架。每当用户提到OpenClaw、Clawdbot、MoltBot、openclaw.json、openclaw gateway、openclaw channels、openclaw nodes、openclaw models、openclaw skills、openclaw doctor、AGENTS.md、SOUL.md、USER.md、HEARTBEAT.md、MEMORY.md、IDENTITY.md、TOOLS.md、BOOTSTRAP.md、ClawHub、openclaw workspace、openclaw config、openclaw sessions、openclaw pairing、openclaw docker、openclaw sandbox、openclaw heartbeat、openclaw compaction、memorySearch、multi-agent、bindings或dmPolicy时，务必参考本文档。本文档涵盖了OpenClaw的安装、配置、故障排除、安全加固、通道设置、技能开发、内存调优以及Docker部署等方面的内容。同时，在配置更改后，若遇到与“my bot”、“my agent”、“Lobster”或代理相关的问题，也可参考本文档进行解决。
---
# OpenClaw 专家技能

## 核心原则：文档优先 + 备份优先

OpenClaw 使用 CalVer 版本控制（格式为 YYYY.M.D-N），并且版本更新频繁。**在每次修改之前**，请务必执行以下步骤：

1. **检查版本**：`openclaw --version`
2. **获取实时文档**：使用 `web_fetch` 下载相关文档页面的 URL（这些 URL 存在于参考文件中）
3. **搜索社区建议**：使用 `web_search` 查找最新的解决方法
4. **创建备份**：切勿在未备份的情况下修改配置文件
5. **执行修改**
6. **验证修改**：修改前后使用 `openclaw doctor` 进行验证
7. **重启网关**：`systemctl --user restart openclaw-gateway`
8. **进行测试**：使用 `openclaw status` 检查系统状态，并在相关频道中进行功能测试

---

## 架构概览

```
Messaging-Kanäle (WhatsApp, Telegram, Slack, Discord, Signal, iMessage, Teams, Matrix, Google Chat, Zalo, WebChat…)
        │
        ▼
┌───────────────────────────────┐
│          Gateway              │  ← ws://127.0.0.1:18789
│     (Control-Plane, RPC)      │  ← Config: ~/.openclaw/openclaw.json (JSON5)
│     systemd user service      │  ← Dashboard: http://127.0.0.1:18789
└──────────────┬────────────────┘
               │
        ┌──────┴──────┐
        │  Agent(s)   │  ← Workspace: ~/.openclaw/workspace/
        │  Runtime    │  ← Sessions: ~/.openclaw/agents/<id>/sessions/
        └──────┬──────┘
               │
        ┌──────┴──────────────────────────┐
        │  Nodes (optional)               │
        │  iOS / Android / macOS / Pi     │
        │  + Canvas / A2UI                │
        └─────────────────────────────────┘
```

### 目录结构
```
~/.openclaw/
├── openclaw.json          # Haupt-Config (JSON5 – Kommentare + trailing commas!)
├── credentials/           # API-Keys (chmod 600!)
│   ├── anthropic
│   ├── openai
│   └── openrouter
├── agents/
│   └── <agentId>/
│       └── sessions/      # Session-Logs (*.jsonl)
├── skills/                # Managed/lokale Skills
└── workspace/             # Agent-Workspace (= das "Gehirn")
    ├── AGENTS.md          # Betriebsanweisungen (in JEDER Session geladen)
    ├── SOUL.md            # Persönlichkeit, Ton, Grenzen (jede Session)
    ├── USER.md            # Nutzerprofil (jede Session)
    ├── TOOLS.md           # Tool-Hinweise (jede Session)
    ├── IDENTITY.md        # Name, Emoji, Vibe
    ├── HEARTBEAT.md       # Scheduled-Tasks / Cron-Checkliste
    ├── MEMORY.md          # Langzeit-Gedächtnis (nur private Sessions!)
    ├── BOOTSTRAP.md       # Einmal-Setup (nach Ausführung gelöscht)
    ├── memory/            # Tages-Logs (YYYY-MM-DD.md)
    ├── skills/            # Workspace-Skills
    └── .git/              # Git-Backup (empfohlen!)
```

---

## 参考文件 — 何时阅读哪些文件

本技能包包含详细的参考文件。**在执行任何操作之前，请务必阅读相应的参考文件**。这些文件位于 `references/` 目录下。

| 任务 | 参考文件 | 内容 |
|---|---|---|
| 安装与入门 | `references/installation.md` | npm/pnpm、Docker、VPS 设置、入职向导 |
| 修改 `openclaw.json` 配置 | `references/config-reference.md` | 基于实际配置的字段参考（包括 auth、models、agents、tools、gateway 等） |
| 仪表板（控制界面） | `references/dashboard.md` | 仪表板的各个部分、访问权限、故障排除 |
| 编写工作区文件 | `references/workspace-files.md` | AGENTS.md、SOUL.md、USER.md、HEARTBEAT.md、MEMORY.md 模板 |
| 设置通道 | `references/channels.md` | Telegram、WhatsApp、Discord、Slack、Signal 的使用方法及故障排除 |
| 调优内存与压缩机制 | `references/memory-system.md` | memoryFlush、memorySearch、Compaction、语义搜索、数据衰减机制 |
| Docker 部署 | `references/docker-setup.md` | docker-compose、沙箱环境、alpine/openclaw、权限设置 |
| 安全加固 | `references/security-hardening.md` | dmPolicy、令牌轮换、白名单、沙箱机制、CIS 标准 |
| 开发/安装技能 | `references/skills-guide.md` | SKILL.md 格式、ClawHub、工作区技能、安全审查流程 |
| 多代理路由 | `references/multi-agent.md` | agents.list、bindings、accountId、agentId、隔离机制 |
| CLI 参考 | `references/cli-reference.md` | 所有命令的用法及示例 |
| 仪表板/控制界面 | `references/dashboard.md` | 侧边栏导航、功能区域、CORS 设置、故障排除 |
| 节点与远程访问 | `references/nodes-and-remote.md` | 节点类型、配对方式、无头节点、Bonjour/mDNS、执行权限 |
| Tailscale 集成 | `references/tailscale-integration.md` | Tailscale 服务集成方法、SSH 隧道、认证配置示例 |
| 实用案例 | `references/examples.md` | 7 个完整的部署场景（从入门到多代理配置，再到成本优化） |
| 故障排除 | `references/troubleshooting.md` | 常见问题、日志记录、诊断步骤 |
| 技巧与高级技巧 | `references/tricks-and-hacks.md` | 社区分享的实用技巧、成本节省方法、Obsidian 使用技巧、Surge 功能、Watchdog 监控工具 |

---

## 快速参考：最重要的 CLI 命令

```bash
# Status & Diagnose
openclaw --version                    # CalVer-Version
openclaw doctor                       # Gesundheitscheck (IMMER!)
openclaw doctor --fix                 # Auto-Fix
openclaw status                       # Kurzer Status
openclaw dashboard                    # Browser-UI (Port 18789)

# Gateway
openclaw gateway start|stop|restart|status
openclaw gateway install              # systemd user service
openclaw gateway log                  # Logs (= journalctl --user -u openclaw-gateway -f)

# Channels
openclaw channels list|add|remove|restart
openclaw channels status --probe      # Live-Check

# Models
openclaw models list|set <provider/model>

# Skills
openclaw skills list|reload
clawhub search|install|update <name>

# Memory & Sessions
openclaw sessions list|clean
openclaw memory flush

# Update
pnpm add -g openclaw@latest && pnpm approve-builds -g && openclaw doctor

# Nodes & Devices
openclaw nodes status                 # Verbundene Nodes anzeigen
openclaw nodes describe --all         # Node-Capabilities auflisten
openclaw nodes run --node <id> -- <cmd>  # Befehl auf Node ausführen
openclaw devices list                 # Pairing-Requests anzeigen
openclaw devices approve <requestId>  # Node-Pairing genehmigen

# Channel-Pairing
openclaw pairing list|approve <channel> <code>

# Config
openclaw config list|get|set|validate

# Security
openclaw token:rotate --force --length 64
openclaw security audit --deep
```

---

## 安全基本规则（务必遵守！）

1. **网关绑定地址**：始终使用 `loopback`，切勿使用 `lan` 或 `0.0.0.0`（除非使用了 Tailscale/VPN）
2. **dmPolicy 配置**：在生产环境中严禁使用 `open` 模式
3. **令牌长度**：令牌长度至少为 64 个字符：`openclaw token:rotate --force --length 64`
4. **凭证文件权限**：设置 `chmod 600`：`chmod 600 ~/.openclaw/credentials/*`
5. **代码审查**：安装前请检查源代码，使用 ClawHub 的 “Hide Suspicious” 功能
6. **避免使用 root 权限**：以普通用户身份运行 OpenClaw
7. **工作区数据**：将数据备份到私有 Git 仓库中，切勿在公共组中共享 `MEMORY.md` 文件
8. **API 使用限制**：在启用 Heartbeat 功能之前，请先设置 API 使用限制
9. **工具的沙箱环境**：尽可能使用 `tools.exec.host: "sandbox"` 来运行工具

---

## 文档查阅流程

### 官方文档链接（用于 `web_fetch`）

```
https://docs.openclaw.ai                          # Hauptseite
https://docs.openclaw.ai/install/docker           # Docker
https://docs.openclaw.ai/concepts/agent-workspace # Workspace
https://docs.openclaw.ai/concepts/memory          # Memory
https://docs.openclaw.ai/concepts/multi-agent     # Multi-Agent
https://docs.openclaw.ai/channels/<name>          # Channel-Guides
https://docs.openclaw.ai/models                   # Models
https://docs.openclaw.ai/tools/skills             # Skills
https://docs.openclaw.ai/security                 # Security
```

备用文档镜像：`https://openclaw.im/docs/`

### 社区资源搜索（用于 `web_search`）

```
"openclaw <Thema> 2026 tips"
"openclaw <Problem> fix workaround github issue"
"openclaw.json <Section> advanced configuration"
```

优先查阅的社区资源：
1. `github.com/openclaw/openclaw`（问题报告、讨论区、agents.md 文档）
2. `docs.openclaw.ai` / `openclaw.im/docs`
3. 社区教程（如 Simon Willison 的 TIL 文章、Substack、Medium 等平台）
4. Reddit 的 r/selfhosted 和 Hacker News 论坛

---

## 备份策略（每次修改前都必须执行）

```bash
# Snapshot der Config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak

# Versioniertes Backup
tar czf ~/openclaw-backup-$(date +%Y%m%d_%H%M%S).tar.gz ~/.openclaw/

# Git-Backup des Workspace (empfohlen)
cd ~/.openclaw/workspace && git add -A && git commit -m "backup: $(date +%Y%m%d_%H%M%S)"
```

---

## 安全地修改配置文件

1. 首先执行 `openclaw --version` 以记录当前版本号
2. 阅读相关的参考文件（参见上面的表格）
3. 使用 `web_fetch` 下载最新的文档文件
4. 将 `~/.openclaw/openclaw.json` 备份到 `~/.openclaw/openclaw.json.bak`
5. 执行修改
6. 使用 `openclaw doctor` 验证修改内容
7. 重启网关：`systemctl --user restart openclaw-gateway`
8. 使用 `openclaw status` 检查系统状态，并在相关频道中进行功能测试
9. 如果遇到问题：恢复备份文件并重启网关：`cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json && systemctl --user restart openclaw-gateway`