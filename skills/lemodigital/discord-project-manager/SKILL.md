---
name: discord-project-manager
description: OpenClaw代理的Discord项目协作基础设施。用于管理论坛频道、帖子、参与者权限以及提及功能（mention mode）。支持三层架构（论坛频道 → 帖子 → 默认频道），以实现多代理项目之间的协调。
metadata:
  openclaw:
    requires:
      config:
        - path: "~/.openclaw/openclaw.json"
          access: "read/write"
          reason: "Reads bot token and agent account mappings; writes channel permission entries and triggers config reload"
      credentials:
        - name: "Discord bot token"
          source: "channels.discord.accounts.*.token in OpenClaw config"
          reason: "Used for Discord REST API calls (forum channel creation)"
      permissions:
        - "Discord bot: Manage Channels (for forum/thread creation)"
    sideEffects:
      - "Patches ~/.openclaw/openclaw.json (channel permission entries)"
      - "Sends SIGUSR1 to gateway process for config reload (2-5s restart)"
      - "Falls back to 'openclaw gateway restart' if SIGUSR1 fails"
---
# Discord 项目管理员

这是一个用于 OpenClaw 多代理团队的自动化 Discord 项目协作工具。它能够创建论坛频道和帖子，管理发言权限，并控制帖子的“仅可被提及”模式——所有这些操作都可以通过命令行界面（CLI）完成。

## 先决条件

- 已配置了 Discord 频道的 OpenClaw；
- 你的 Discord 机器人需要在目标公会中拥有“管理频道”（Manage Channels）的权限；
- 确保你的系统安装了 Python 3.8 或更高版本。

## 快速入门

```bash
SKILL_DIR="/path/to/discord-project-manager"

# 1. Initialize (first time only)
python3 "$SKILL_DIR/scripts/discord-pm.py" config init
python3 "$SKILL_DIR/scripts/discord-pm.py" registry init
python3 "$SKILL_DIR/scripts/discord-pm.py" forum-channel set-default <forum_channel_id>

# 2. Create a project thread
python3 "$SKILL_DIR/scripts/discord-pm.py" thread create \
  --name "my-feature" \
  --owner agent-a \
  --participants "agent-a,agent-b"
```

此命令会在你的默认论坛中创建一个新帖子，赋予 `agent-a` 发言权（即帖子的所有者），并将 `agent-b` 设置为“仅可被提及”模式。

## 命令

### 配置设置

```bash
discord-pm.py config init                # Auto-detect guild ID from OpenClaw config
discord-pm.py config get                 # Show current config
discord-pm.py config set-guild <id>      # Set guild ID manually
discord-pm.py config set-forum <id>      # Set default forum channel
```

### 代理注册

```bash
discord-pm.py registry init             # Auto-collect agent info from OpenClaw config
discord-pm.py registry list             # List all registered agents
```

### 论坛频道管理

```bash
# Create a new Forum Channel (uses Discord REST API directly)
discord-pm.py forum-channel create <name> [--emoji <emoji>] [--description <text>]

# Manage forum channels
discord-pm.py forum-channel set-default <channel_id>
discord-pm.py forum-channel add <channel_id> <name>    # Register existing channel
discord-pm.py forum-channel remove <name>
discord-pm.py forum-channel list
```

### 帖子管理

```bash
# Create thread (uses default forum unless --forum-channel specified)
discord-pm.py thread create \
  --name <name> \
  --owner <agent> \
  --participants <agent1,agent2,...> \
  [--forum-channel <id>] \
  [--no-mention] \
  [--message <text>]

discord-pm.py thread archive <thread_id>    # Remove all permissions
discord-pm.py thread status <thread_id>     # Show permissions and participants
```

### 权限管理

```bash
discord-pm.py permissions add <thread_id> <agent1> [agent2...] [--no-mention]
discord-pm.py permissions remove <thread_id> <agent1> [agent2...]
discord-pm.py permissions mention-mode <thread_id> <on|off> <agents...|--all>
```

### 项目管理

```bash
discord-pm.py project list [--active] [--archived] [--agent <name>]
discord-pm.py project info <thread_id>
discord-pm.py project describe <thread_id> <text>
discord-pm.py project update <thread_id> --next-action <text>
```

每当创建新帖子时，项目会自动被注册；当参与者发生变化或帖子被归档时，项目信息也会更新。“--agent”过滤器仅显示该代理是所有者或参与者的项目，并会显示相应的角色标签。

批量操作：`add` 和 `remove` 命令可以同时处理多个代理名称。所有代理的配置更改会一次性应用，因此只需要重新加载一次 OpenClaw 的配置文件。

`mention-mode` 命令会扫描当前的 OpenClaw 配置，找出所有有权访问该帖子的账户，然后为这些账户统一设置“仅可被提及”模式——包括那些不在代理注册列表中的账户（例如手动配置的机器人）。

## 架构

### 三层项目结构

| 层次 | 用途 | 示例 |
|------|----------|---------|
| 论坛频道 | 包含多个子团队的大型项目 | 📦-产品发布 |
| 帖子 | 单个任务或子项目 | api-refactor |
| 默认频道 | 用于处理简单任务，无需隔离 | #dev-ops |

### 权限模型

- **所有者**：`requireMention: false` — 可自由发言，主导对话；
- **参与者**：`requireMention: true` — 仅在被提及时才会回复；
- **非参与者**：无法访问该频道。

这种权限设置有助于保持帖子的专注性：所有者主导讨论，其他参与者仅在被请求时才参与发言。

### 工作原理

1. **帖子/论坛的创建**：通过 `openclaw message` CLI 命令创建帖子，通过 Discord REST API 创建论坛；
2. **权限管理**：通过修改 OpenClaw 的配置文件 `channels.discord.accounts.<account>.guilds.<guild>.channels.<channel>` 来设置权限；
3. **配置文件重新加载**：触发 SIGUSR1 信号以实现平滑重启（通常需要 2-5 秒）。如果必要，也可以直接重启 OpenClaw 服务。

## 数据文件

```
data/
├── config.json     # Skill config (guild ID, default forum)
├── agents.json     # Agent registry (account IDs, user IDs, channels)
└── projects.json   # Project registry (threads, owners, participants, nextAction)
```

这些数据文件由 `config init` 和 `registry init` 脚本自动生成，不会被包含在 Git 仓库中（属于用户特定数据）。

## 安全性与权限

使用此工具需要访问你的 OpenClaw 配置文件：

- **读取权限**：读取 `~/.openclaw/openclaw.json` 文件以获取 Discord 机器人令牌和代理账户映射；
- **写入权限**：将频道权限信息写入该配置文件（采用文件锁定和原子写操作）；
- **触发重启**：在需要时触发 SIGUSR1 信号以实现平滑重启（必要时也会直接重启 OpenClaw 服务）。

**建议**：
- 在首次使用前，请备份 `~/.openclaw/openclaw.json` 文件；
- 确保你的 Discord 机器人仅具有“管理频道”的权限；
- 如果对权限配置有疑虑，请查看源代码。

## 故障排除

| 问题 | 检查内容 |
|---------|-------|
| 无法创建帖子 | 是否设置了默认论坛？（使用 `forum-channel set-default` 命令） |
| “仅可被提及”模式不起作用 | 代理的配置中是否包含了 `mentionPatterns`？ |
| 创建论坛时出现 403 错误 | 机器人是否在目标公会中拥有“管理频道”的权限？ |
| 权限更改延迟 | 配置文件重新加载需要 2-5 秒。如果问题仍然存在，请尝试重启 OpenClaw 服务。 |

## 源代码结构

```
discord-project-manager/
├── SKILL.md
├── scripts/
│   ├── discord-pm.py     # Unified CLI
│   └── cli.sh            # Bash wrapper
├── lib/
│   ├── discord_api.py    # Discord API (CLI + REST)
│   ├── config.py         # OpenClaw config operations
│   ├── skill_config.py   # Skill-local config
│   ├── registry.py       # Agent registry
│   ├── thread.py         # Thread lifecycle
│   ├── permissions.py    # Permission management
│   ├── forum.py          # Forum channel management
│   ├── projects.py       # Project registry
│   └── validators.py     # Input validation
└── data/                 # Auto-generated, git-ignored
```

---

## 版本：2.2.1  
## 最后更新时间：2026-02-27