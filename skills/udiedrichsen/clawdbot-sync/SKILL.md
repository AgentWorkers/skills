---
name: clawdbot-sync
version: 1.0.0
description: "在多个Clawdbot实例之间同步内存、偏好设置和技能数据。支持通过Tailscale使用SSH/rsync进行双向同步。适用于需要与其他Clawdbot同步数据、在实例间共享内存或保持多个代理同步的场景。触发命令包括：/sync、'sync with mac'、'update other clawdbot'、'share this with my other bot'。"
author: clawdbot
license: MIT
metadata:
  clawdbot:
    emoji: "🔄"
    triggers: ["/sync"]
    requires:
      bins: ["rsync", "ssh", "jq"]
  tags: ["sync", "multi-agent", "collaboration", "backup"]
---

# Clawdbot 同步 🔄

通过 Tailscale/SSH 在多个 Clawdbot 实例之间同步内存、偏好设置和技能数据。

## 特点

- **双向同步**：支持 Clawdbot 实例之间的数据交换
- **智能冲突解决**：采用最新文件覆盖旧文件，或选择合并方式处理日志文件
- **选择性同步**：用户可自定义需要同步的文件
- **通过 Tailscale 进行对等节点发现**
- **预览模式**：提供同步前的预览功能

## 命令

| 命令 | 功能 |
|---------|--------|
| `/sync` | 显示同步状态及已配置的对等节点 |
| `/sync status` | 检查与所有对等节点的连接状态 |
| `/sync now [peer]` | 与指定的对等节点同步数据 |
| `/sync push [peer]` | 将本地更改推送到对等节点 |
| `/sync pull [peer]` | 从对等节点拉取更改 |
| `/sync add <name> <host> [user> [path>` | 添加新的对等节点 |
| `/sync remove <name>` | 删除指定的对等节点 |
| `/sync diff [peer]` | 显示需要同步的文件差异 |
| `/sync history` | 查看同步历史记录 |

## 设置步骤

### 1. 配置对等节点

```bash
handler.sh add mac-mini 100.95.193.55 clawdbot /Users/clawdbot/clawd $WORKSPACE
handler.sh add server 100.89.48.26 clawdbot /home/clawdbot/clawd $WORKSPACE
```

### 2. 确保 SSH 访问权限

两台机器都需要配置 SSH 密钥认证：
```bash
ssh-copy-id clawdbot@100.95.193.55
```

### 3. 测试连接

```bash
handler.sh status $WORKSPACE
```

## 同步内容

| 同步项 | 默认值 | 备注 |
|------|---------|-------|
| `memory/` | ✅ 是 | 所有内存文件和技能数据 |
| `MEMORY.md` | ✅ 是 | 主内存文件 |
| `USER.md` | ✅ 是 | 用户配置文件 |
| `IDENTITY.md` | ❌ 否 | 每个实例都有独立的身份信息 |
| `skills/` | ⚙️ 可选 | 安装的技能信息 |
| `config/` | ❌ 否 | 仅实例特定的配置信息 |

## 处理命令

```bash
handler.sh status $WORKSPACE                    # Check peers and connection
handler.sh sync <peer> $WORKSPACE               # Bi-directional sync
handler.sh push <peer> $WORKSPACE               # Push to peer
handler.sh pull <peer> $WORKSPACE               # Pull from peer
handler.sh diff <peer> $WORKSPACE               # Show differences
handler.sh add <name> <host> <user> <path> $WS  # Add peer
handler.sh remove <name> $WORKSPACE             # Remove peer
handler.sh history $WORKSPACE                   # Sync history
handler.sh auto <on|off> $WORKSPACE             # Auto-sync on heartbeat
```

## 冲突解决机制

1. **基于时间戳**：使用最新文件覆盖旧文件
2. **日志文件合并**：采用只读追加的方式合并文件
3. **跳过冲突文件**：可选择忽略存在冲突的文件
4. **手动解决**：标记需要人工审核的冲突文件

## 数据文件存储位置

数据文件存储在 `$WORKSPACE/memory/clawdbot-sync/` 目录下：

| 文件名 | 用途 |
|------|---------|
| `peers.json` | 配置的对等节点信息 |
| `history.json` | 同步历史记录 |
| `config.json` | 同步后的偏好设置 |
| `conflicts/` | 存在冲突的文件 |

## 示例使用流程

```
User: /sync now mac-mini
Bot: 🔄 Syncing with mac-mini (100.95.193.55)...

     📤 Pushing: 3 files changed
     • memory/streaming-buddy/preferences.json
     • memory/2026-01-26.md
     • MEMORY.md
     
     📥 Pulling: 1 file changed
     • memory/2026-01-25.md
     
     ✅ Sync complete! 4 files synchronized.
```

## 所需软件/环境

- `rsync`：用于高效文件同步 |
- `ssh`：确保安全的数据传输 |
- Tailscale 或直接的网络连接 |
- 配置好的 SSH 密钥认证

## 安全性

- 所有数据传输均通过 SSH 进行（加密处理） |
- 不存储任何密码（仅使用密钥认证） |
- 同步路径受工作空间限制 |
- 系统文件不会被同步 |