---
name: claw-sync
description: OpenClaw 提供了安全的数据同步功能，用于管理内存和工作区数据。您可以使用以下命令进行操作：  
- `/sync`：用于推送数据到远程服务器  
- `/restore`：用于从远程服务器拉取数据  
- `/sync-status`：用于检查数据同步的状态  

该系统支持版本化的数据快照功能，以及灾难恢复机制（即在数据丢失或损坏时能够快速恢复到之前的正常状态）。
version: 2.0.2
author: arakichanxd
repository: https://github.com/arakichanxd/Claw-Sync
tags:
  - sync
  - github
  - memory
  - skills
  - disaster-recovery
files:
  - name: SKILL.md
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/SKILL.md
  - name: README.md
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/README.md
  - name: index.js
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/index.js
  - name: package.json
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/package.json
  - name: config.example.env
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/config.example.env
  - name: scripts/push.js
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/push.js
  - name: scripts/pull.js
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/pull.js
  - name: scripts/status.js
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/status.js
  - name: scripts/setup-cron.js
    url: https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/setup-cron.js
commands:
  - name: sync
    description: Push memory and skills to remote repository
    usage: /sync [--dry-run]
    run: node skills/claw-sync/index.js sync
  - name: restore
    description: Restore memory and skills from remote
    usage: /restore [latest|<version>] [--force]
    run: node skills/claw-sync/index.js restore
  - name: sync-status
    description: Show sync configuration and local snapshots
    usage: /sync-status
    run: node skills/claw-sync/index.js status
  - name: sync-list
    description: List all available sync versions
    usage: /sync-list
    run: node skills/claw-sync/index.js list
---

# Claw Sync

这是一个用于将 OpenClaw 的内存数据和工作区内容安全地同步到 GitHub 的工具。

**仓库地址：** https://github.com/arakichanxd/Claw-Sync

## 文件列表

| 文件名 | 说明 | 链接 |
|------|-------------|------|
| `SKILL.md` | 人工智能代理的配置说明 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/SKILL.md) |
| `README.md` | 用户使用指南 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/README.md) |
| `index.js` | 命令处理逻辑 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/index.js) |
| `package.json` | NPM 配置文件 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/package.json) |
| `scripts/push.js` | 将数据推送到远程仓库 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/push.js) |
| `scripts/pull.js` | 从远程仓库恢复数据 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/pull.js) |
| `scripts/status.js` | 显示同步状态 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/status.js) |
| `scripts/setup-cron.js` | 自动同步设置 | [查看](https://github.com/arakichanxd/Claw-Sync/blob/main/scripts/setup-cron.js) |

---

## 安装步骤

### 第一步：克隆技能代码
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/arakichanxd/Claw-Sync.git claw-sync
```

### 第二步：创建 GitHub 仓库
1. 访问 https://github.com/
2. 创建一个 **私有的** 仓库（例如：`my-openclaw-sync`）
3. 保持仓库为空（无需添加 `README.md` 文件）

### 第三步：生成 GitHub 访问令牌
1. 访问 https://github.com/settings/tokens?type=beta
2. 点击 “Generate new token”（生成新令牌）
3. 为令牌命名：`openclaw-sync`
4. 选择你的同步仓库
5. 设置权限：允许读取和写入仓库内容
6. 生成令牌并复制它

### 第四步：配置环境变量
创建文件 `~/.openclaw/.backup.env`：
```
BACKUP_REPO=https://github.com/YOUR_USERNAME/YOUR_REPO
BACKUP_TOKEN=ghp_YOUR_TOKEN_HERE
```

### 第五步：测试配置
```bash
/sync-status
```

如果配置正确，你会看到提示 “✅ Configured”（配置成功）。

### 第六步：首次同步
```bash
/sync
```

---

## 命令说明

### `/sync`
将内存数据和技能配置推送到远程仓库。
```
/sync              → Create versioned snapshot
/sync --dry-run    → Preview what would sync (no changes)
```

### `/restore`
从远程仓库恢复数据。
```
/restore                        → Restore latest
/restore latest                 → Same as above
/restore backup-20260202-1430   → Restore specific version
/restore --force                → Skip confirmation
```

### `/sync-status`
显示配置信息和本地数据快照。

### `/sync-list`
列出所有可恢复的版本。

---

## 同步的内容

| 文件名 | 说明 |
|------|-------------|
| `MEMORY.md` | 长期存储的数据 |
| `USER.md` | 用户信息 |
| `SOUL.md` | 代理的个性化设置 |
| `IDENTITY.md` | 代理的身份信息 |
| `TOOLS.md` | 工具配置 |
| `AGENTS.md` | 工作区规则 |
| `memory/*.md` | 每日日志 |
| `skills/*` | 自定义技能配置 |

## 不会同步的内容（出于安全考虑）：
- `openclaw.json`：包含 API 密钥
- `.env`：包含敏感信息

---

## 常见问题及解决方法

### “同步配置未完成”
确保创建了 `~/.openclaw/.backup.env` 文件，并设置了正确的 `BACKUP_REPO` 和 `BACKUP_TOKEN`。

### “仓库地址无效”
仓库地址必须是 HTTPS 格式，并且必须来自 github.com、gitlab.com 或 bitbucket.org。

### “令牌太短”
令牌长度必须至少为 20 个字符。请从 GitHub 重新生成令牌。

### 克隆失败
检查你的令牌是否具有读取和写入仓库内容的权限。

---

## 灾难恢复机制
每次恢复数据之前，系统会自动将本地备份文件保存到指定位置：
```
~/.openclaw/.local-backup/<timestamp>/
```

如果出现问题，可以手动从备份文件中恢复数据。

---

## 自动同步设置
设置每 12 小时自动同步一次：
```bash
node skills/claw-sync/index.js setup
```

---

## 功能特点

- 🏷️ **版本控制**：每次同步都会生成一个可恢复的版本（通过 Git 标签记录）
- 💾 **灾难恢复**：每次恢复前都会进行本地备份
- 🔒 **安全性**：不同步配置文件，并对令牌进行安全处理
- 🖥️ **跨平台支持**：支持 Windows、Mac 和 Linux

---

## 源代码
完整源代码：https://github.com/arakichanxd/Claw-Sync