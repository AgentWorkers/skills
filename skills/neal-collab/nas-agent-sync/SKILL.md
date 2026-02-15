---
name: nas-agent-sync
version: 1.1.0
description: **OpenClaw 的 Synology NAS 集成：通过 SSH 为多代理团队提供集中式文件存储**

OpenClaw 是一个用于管理和监控分布式系统的开源工具，而 Synology NAS（网络附加存储设备）则提供了便捷的文件存储解决方案。通过将 OpenClaw 与 Synology NAS 集成，团队可以高效地存储、共享和访问文件，从而实现更强大的协作能力。

### 集成步骤：

1. **安装 OpenClaw 和相关依赖**：
   首先，确保您的系统上已安装 OpenClaw 及其所有必要的依赖库。

2. **配置 SSH 连接**：
   在 OpenClaw 中配置 SSH 连接信息，以便能够访问 Synology NAS。您需要提供 Synology NAS 的 IP 地址、用户名和密码。

3. **配置文件共享**：
   在 Synology NAS 中，启用文件共享功能，并设置共享目录的访问权限。确保 OpenClaw 用户具有访问这些共享目录的权限。

4. **在 OpenClaw 中使用共享目录**：
   在 OpenClaw 中，将 Synology NAS 上的共享目录添加到可访问的目录列表中。这样，团队成员就可以通过 OpenClaw 直接访问这些共享目录，就像访问本地文件一样方便。

5. **部署监控任务**：
   使用 OpenClaw 部署监控任务，将需要监控的文件或目录添加到任务列表中。这些文件或目录将自动从 Synology NAS 下载到本地，并在任务执行时进行监控。

### 优势：

- **集中式存储**：所有团队成员都可以从同一个中央位置访问文件，提高了数据管理和协作的效率。
- **安全性**：Synology NAS 提供了强大的访问控制和加密功能，确保数据的安全性。
- **灵活性**：您可以根据需要配置文件共享的权限和访问规则。

通过这种集成方案，OpenClaw 可以成为多代理团队中不可或缺的文件管理和监控工具，帮助团队更高效地协作和完成任务。
emoji: 📦
tags:
  - nas
  - synology
  - file-storage
  - ssh
  - multi-agent
  - backup
---

# NAS代理同步——用于OpenClaw代理的Synology文件存储

使用Synology NAS（或任何可通过SSH访问的存储设备）来集中管理多代理团队之间的文件存储。其中一个代理充当**文件主节点**（File Master），所有其他代理都通过该节点路由文件请求。

## 问题

多代理设置会在多个工作空间中生成文件。如果没有集中存储：
- 文件会在代理会话之间丢失
- 没有备份策略
- 代理会重复工作
- 没有统一的文件信息来源

## 解决方案

指定一个代理作为**文件主节点**。所有文件操作都通过`sessions_send`函数发送到该代理。文件主节点负责管理：
- 与NAS的SSH连接
- 每个代理的文件夹结构
- 文件的存储和检索
- 跨代理的文件共享

## 架构

```
┌──────────┐    sessions_send     ┌────────────┐     SSH      ┌─────────┐
│ Agent A  │ ──────────────────► │ FILE MASTER │ ──────────► │   NAS   │
│ (Finance)│ "store invoice.pdf" │ (Tech Lead) │             │         │
└──────────┘                     └────────────┘             └─────────┘
                                       │
┌──────────┐    sessions_send          │  SSH
│ Agent B  │ ──────────────────►       │
│ (Sales)  │ "get sales report"        ▼
└──────────┘                     ┌─────────────┐
                                 │ _agents/     │
                                 │ ├── agent-a/ │
                                 │ ├── agent-b/ │
                                 │ ├── agent-c/ │
                                 │ └── _shared/ │
                                 └─────────────┘
```

## 设置

### 1. NAS要求

- Synology NAS（任何型号）或任何支持SSH的Linux服务器
- 支持基于密钥的SSH身份验证
- 建议使用VPN或Tailnet以实现安全的远程访问

### 2. 创建文件夹结构

```bash
SSH_HOST="user@your-nas-ip"

# Create agent folders (customize agent names to match your team)
ssh $SSH_HOST "mkdir -p ~/_agents/{coordinator,techops,finance,sales,marketing}"

# Create shared folders
ssh $SSH_HOST "mkdir -p ~/_shared/{config,templates}"

# Create agent directory file
ssh $SSH_HOST 'cat > ~/_shared/config/agent-directory.json << EOF
{
  "agents": {
    "coordinator": { "role": "Coordinator", "path": "~/_agents/coordinator/" },
    "techops": { "role": "File Master", "path": "~/_agents/techops/" },
    "finance": { "role": "Finance", "path": "~/_agents/finance/" }
  },
  "shared": "~/_shared/",
  "basePath": "~/"
}
EOF'
```

### 3. 配置文件主节点代理

在文件主节点代理的`AGENTS.md`文件中添加以下内容：

```markdown
## FILE MASTER — Incoming Requests

When another agent sends a file request via sessions_send:

### Store a file:
ssh USER@NAS-IP "mkdir -p ~/_agents/[agent]/[subfolder]/"
# Copy/create file there

### Retrieve a file:
ssh USER@NAS-IP "cat ~/_agents/[agent]/[file]"
# Send content back to requesting agent

### Confirm back:
sessions_send(sessionKey="agent:[requester]:main", message="Done! File at [path]")
```

### 4. 配置其他代理

在每个代理的`AGENTS.md`文件中添加以下内容：

```markdown
## File Operations → File Master

I do NOT access files directly. ALL file ops go through the File Master:

sessions_send(sessionKey="agent:techops:main", message="Store: [details]")
sessions_send(sessionKey="agent:techops:main", message="Retrieve: [path]")
```

## NAS文件夹结构（推荐）

```
~/
├── _agents/
│   ├── coordinator/     # Coordinator files
│   │   ├── journal/     # Daily journals
│   │   └── tracking/    # Task tracking
│   ├── techops/         # Tech docs, scripts
│   │   ├── scripts/
│   │   └── configs/
│   ├── finance/         # Finance
│   │   ├── invoices/
│   │   ├── contracts/
│   │   └── reports/
│   ├── sales/           # Sales
│   │   ├── leads/
│   │   └── proposals/
│   └── [your-agent]/    # Per-agent storage
├── _shared/
│   ├── config/          # Shared configs
│   │   └── agent-directory.json
│   └── templates/       # Shared templates
└── _backups/
    └── memory/          # Memory file backups
```

## 通过VPN/Tailnet进行SSH连接（推荐）

```bash
# Connect via secure tunnel IP (e.g. WireGuard, ZeroTier, or similar)
SSH_HOST="user@10.x.x.x"  # Your VPN/Tailnet IP

# Test connection
ssh $SSH_HOST "echo 'NAS connected!'"
```

## 安全性

- ✅ 使用基于密钥的SSH身份验证（配置文件中不包含密码）
- ✅ 通过VPN/Tailnet建立加密隧道（无需端口转发）
- ✅ 文件主节点的设置限制了SSH访问权限，仅允许一个代理访问
- ✅ 其他代理无法获取SSH凭据
- ❌ 绝不要将SSH密钥存储在代理的`SOUL.md`文件或内存中

## 为什么使用文件主节点模式？

1. **安全性**：只有文件主节点拥有NAS的访问权限
2. **一致性**：文件位置的统一管理
3. **审计追踪**：所有文件操作都通过文件主节点记录下来
4. **简洁性**：其他代理无需了解SSH命令的详细信息

## 备份策略

### 每日自动备份（通过OpenClaw）
设置一个cron作业，将代理的工作空间备份到NAS：

```json5
// Cron job config
{
  "schedule": { "kind": "cron", "expr": "0 3 * * *", "tz": "UTC" },
  "payload": {
    "kind": "agentTurn",
    "message": "Backup all agent workspaces to NAS. For each agent: rsync workspace memory/ folder to NAS _agents/{agent}/memory-backup/. Report any failures."
  },
  "sessionTarget": "isolated"
}
```

### 手动备份命令
```bash
# Backup specific agent
rsync -avz ~/.openclaw/workspace-finance/memory/ user@nas-ip:~/_agents/finance/memory-backup/

# Backup all agents (customize list to your team)
for agent in coordinator techops finance sales marketing; do
  rsync -avz ~/.openclaw/workspace-$agent/memory/ user@nas-ip:~/_agents/$agent/memory-backup/
done
```

## 故障排除

**SSH连接被拒绝：**
→ 检查VPN/Tailnet的状态——NAS是否在线并已连接？
→ 确认NAS上的SSH服务正在运行（Synology：DSM → 控制面板 → 终端 & SNMP）

**权限被拒绝：**
→ SSH密钥未添加：`ssh-copy-id user@nas-ip`
→ NAS的主文件夹未启用（Synology：DSM → 用户 → 高级设置 → 启用主文件夹服务）

**传输速度慢：**
→ 使用直接的VPN连接（避免中间转发）
→ 考虑使用压缩功能：`rsync -avz --compress`

## 兼容的NAS型号

- ✅ Synology（任何支持DSM 7+的型号）
- ✅ QNAP（QTS 5+）
- ✅ TrueNAS / FreeNAS
- ✅ 任何支持SSH访问的Linux服务器
- ✅ 配备外部存储的Raspberry Pi

## 更新日志

### v1.1.0
- 移除了所有针对特定代理和设置的引用
- 优化了文件夹结构和示例代码
- 添加了基于cron的备份策略

### v1.0.0
- 初始版本