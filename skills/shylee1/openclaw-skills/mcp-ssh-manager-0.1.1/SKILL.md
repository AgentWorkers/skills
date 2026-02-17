---
name: mcp-ssh-manager
description: 当用户请求执行“运行SSH命令”、“在服务器上执行操作”、“建立SSH会话”、“上传文件”、“下载文件”、“创建SSH隧道”、“检查服务器状态”、“监控服务器”、“部署文件”、“备份服务器”或需要远程服务器管理时，应使用此技能。该技能注重会话的重用、工作目录的有序管理以及内容的持久化，以确保操作的可持续性和高效性。
version: 0.1.0
metadata:
  clawdbot:
    emoji: "🖥️"
    requires:
      mcp_servers: ["ssh-manager"]
---

# MCP SSH管理技能

> **原始MCP服务器**: [mcp-ssh-manager](https://github.com/bvisible/mcp-ssh-manager) 由 [@bvisible](https://github.com/bvisible) 开发

本技能提供了关于如何使用MCP ssh-manager服务器的文档、工作流程和最佳实践。

使用MCP ssh-manager工具来管理远程SSH服务器。重点在于会话的重用、工作目录的组织以及内容的持久化，以实现可持续的操作。

## 快速参考

### 连接管理

| 任务 | 工具 | 示例 |
|------|------|---------|
| 列出服务器 | `ssh_list_servers` | `ssh_list_servers` |
| 执行命令 | `ssh_execute` | `ssh_execute server="rock5t" command="df -h"` |
| 以sudo权限执行命令 | `ssh_execute_sudo` | `ssh_execute_sudo server="rock5t" command="apt update"` |
| 检查连接状态 | `ssh_connection_status` | `ssh_connection_status action="status"` |

### 会话管理

| 任务 | 工具 | 示例 |
|------|------|---------|
| 启动会话 | `ssh_session_start` | `ssh_session_start server="rock5t" name="deploy"` |
| 发送命令 | `ssh_session_send` | `ssh_session_send session="xxx" command="cd /var"` |
| 列出会话 | `ssh_session_list` | `ssh_session_list` |
| 关闭会话 | `ssh_session_close` | `ssh_session_close session="xxx"` |

### 文件操作

| 任务 | 工具 | 示例 |
|------|------|---------|
| 上传文件 | `ssh_upload` | `ssh_upload server="rock5t" localPath="." remotePath="/tmp"` |
| 下载文件 | `ssh_download` | `ssh_download server="rock5t" remotePath="/var/log/syslog" localPath="."` |
| 同步文件 | `ssh_sync` | `ssh_sync server="rock5t" source="local:./dist" destination="remote:/var/www"` |

### 监控

| 任务 | 工具 | 示例 |
|------|------|---------|
| 查看日志尾部内容 | `ssh_tail` | `ssh_tail server="rock5t" file="/var/log/syslog" lines=20` |
| 检查服务器健康状况 | `ssh_health_check` | `ssh_health_check server="rock5t"` |
| 监控资源使用情况 | `ssh_monitor` | `ssh_monitor server="rock5t" type="overview"` |
| 检查服务状态 | `ssh_service_status` | `ssh_service_status server="rock5t" services="nginx,docker"` |

### 隧道创建

| 任务 | 工具 | 示例 |
|------|------|---------|
| 创建隧道 | `ssh_tunnel_create` | `ssh_tunnel_create server="rock5t" type="local" localPort=8080 remoteHost="localhost" remotePort=80` |
| 列出隧道 | `ssh_tunnel_list` | `ssh_tunnel_list` |
| 关闭隧道 | `ssh_tunnel_close` | `ssh_tunnel_close tunnelId="xxx"` |

### 备份

| 任务 | 工具 | 示例 |
|------|------|---------|
| 创建备份 | `ssh_backup_create` | `ssh_backup_create server="rock5t" type="files" name="data"` |
| 列出备份 | `ssh_backup_list` | `ssh_backup_list server="rock5t"` |
| 恢复备份 | `ssh_backup_restore` | `ssh_backup_restore server="rock5t" backupId="xxx"` |
| 安排备份任务 | `ssh_backup_schedule` | `ssh_backup_schedule server="rock5t" schedule="0 2 * * *" type="files" name="daily"` |

## 使用示例

### 示例1：单条命令

```bash
# Simple command - no session needed
ssh_execute server="rock5t" command="df -h"
```

### 示例2：使用会话的多步骤部署

```bash
# Check existing sessions first
ssh_session_list

# Start a persistent session
ssh_session_start server="rock5t" name="deploy"

# Get session ID from previous response
ssh_session_send session="xxx" command="cd /home/imax/project"
ssh_session_send session="xxx" command="git pull origin main"
ssh_session_send session="xxx" command="npm install"
ssh_session_send session="xxx" command="npm run build"
ssh_session_send session="xxx" command="pm2 restart all"

# Close when done
ssh_session_close session="xxx"
```

### 示例3：系统健康检查

```bash
# Check overall health
ssh_health_check server="rock5t"

# Monitor specific resources
ssh_monitor server="rock5t" type="cpu" interval=5 duration=30

# Check specific services
ssh_service_status server="rock5t" services="nginx,docker,postgres"
```

### 示例4：文件部署

```bash
# Upload deployment package
ssh_upload server="rock5t" localPath="./dist/app.tar.gz" remotePath="/tmp/app.tar.gz"

# Extract and restart
ssh_execute server="rock5t" command="cd /tmp && tar -xzf app.tar.gz && cp -r app/* /var/www/ && pm2 restart app"
```

### 示例5：日志监控

```bash
# Tail real-time logs
ssh_tail server="rock5t" file="/var/log/nginx/access.log" lines=50 follow=true

# Filter with grep
ssh_tail server="rock5t" file="/var/log/syslog" grep="error" lines=100
```

### 示例6：创建SSH隧道

```bash
# Local port forward (access remote service locally)
ssh_tunnel_create server="rock5t" type="local" localPort=5432 remoteHost="localhost" remotePort=5432

# Now connect to local:5432 to access remote database
```

## 工作目录管理

将SSH操作的结果保存在 `~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/` 目录中，以便重用和比较。

### 结构

```
~/.ssh-workdir/
└── {hostname}/
    └── {YYYY-MM-DD}-{topic}/
        ├── commands.md    # All executed commands
        ├── output/        # Command outputs
        │   ├── df-h.txt
        │   ├── cpu.txt
        │   └── memory.txt
        ├── status.json    # Host status snapshot
        └── summary.md     # Findings and notes
```

### 创建工作目录

```bash
# Create new workdir
mkdir -p ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/output

# Create commands log
touch ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/commands.md
```

### 记录命令执行结果

```bash
# Add command to log
echo "## $(date)" >> ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/commands.md
echo 'df -h' >> ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/commands.md
```

### 保存输出结果

```bash
# Execute and save
ssh_execute server="{hostname}" command="df -h" > ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/output/df-h.txt
```

### 编写操作总结

```bash
# Write findings
echo '## System Check Findings' >> ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/summary.md
echo '- Disk usage: 75% on /dev/sda1' >> ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/summary.md
echo '- Memory: 4GB/16GB used' >> ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/summary.md
```

### 重用之前的操作上下文

```bash
# Check if recent work exists
ls ~/.ssh-workdir/{hostname}/

# Read previous summary
cat ~/.ssh-workdir/{hostname}/{previous-date}-{topic}/summary.md

# Compare outputs
diff ~/.ssh-workdir/{hostname}/{yesterday}-{topic}/output/df-h.txt \
     ~/.ssh-workdir/{hostname}/{today}-{topic}/output/df-h.txt
```

## 会话管理指南

### 何时使用会话

**适合使用会话的情况：**
- 多步骤部署
- 需要保持状态（如目录切换、环境设置）的任务
- 长时间运行的工作流程（包含多个命令）
- 命令执行顺序重要的任务

**不适合使用会话的情况：**
- 单个快速命令（如 `df -h`、`pwd`）
- 不需要保持状态的无关命令
- 仅用于读取日志的监控任务

### 会话生命周期

```bash
# 1. Check existing sessions first
ssh_session_list

# 2. Reuse existing session if available and still active
ssh_session_send session="existing-id" command="..."

# 3. Start new session only if necessary
ssh_session_start server="{hostname}" name="{task-name}"

# 4. ALWAYS close when done
ssh_session_close session="{session-id}"
```

### 超时处理

- SSH服务器可能会关闭空闲会话（默认为3-5分钟）
- 可以在服务器上配置 `ClientAliveInterval` 以延长会话保持时间
- 对于长时间运行的任务，可以考虑定期发送简单命令来保持会话活跃
- 如果会话无响应，可以创建新的会话

## 最佳实践

### 在执行SSH操作之前：

1. **检查现有的会话**  
   ```bash
   ssh_session_list
   ```

2. **查看最近的工作目录**  
   ```bash
   ls ~/.ssh-workdir/{hostname}/
   ```

3. **如果开始新任务，则创建新的工作目录**  
   ```bash
   mkdir -p ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/output
   ```

### 在执行SSH操作期间：

1. **根据任务选择合适的工具**：
   - 单条命令：使用 `ssh_execute`
   - 多步骤操作：使用 `ssh_session_start` → `ssh_session_send` → `ssh_session_close`
   - 文件传输：使用 `ssh_upload/download/sync`
   - 监控：使用 `ssh_monitor`、`ssh_tail`、`ssh_health_check`

2. **将命令执行结果记录到工作目录中**  
   ```bash
   echo "command" >> ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/commands.md
   ```

3. **保存重要的输出结果**  
   ```bash
   ssh_execute server="{hostname}" command="df -h" > ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/output/df-h.txt
   ```

### 在SSH操作完成后：

1. **关闭会话**  
   ```bash
   ssh_session_close session="{session-id}"
   ```

2. **编写操作总结**  
   ```bash
   echo '## Findings' >> ~/.ssh-workdir/{hostname}/{YYYY-MM-DD}-{topic}/summary.md
   ```

3. **清理资源**：
   - 关闭隧道：`ssh_tunnel_close`
   - 确保所有会话都已关闭：`ssh_session_list`

## 提示：

- 在开始新任务之前，使用 `ssh_session_list` 来查看是否有可重用的会话
- 为每个任务创建工作目录，以保持操作历史的条理清晰
- 编写操作总结，以便快速回顾之前的操作
- 使用 `ssh_connection_status action="status"` 来检查连接状态
- 为了便于跨服务器比较结果，使用统一的文件命名规则
- 完成操作后关闭会话以释放资源
- 如有需要，可以配置服务器端的 `ClientAliveInterval` 以延长会话超时时间

## 额外资源

### 参考文件：

- **`references/sessions.md`** - 会话管理的详细说明
- **`references/workspace.md`** - 工作目录的结构和使用方法
- **`references/comparison.md`** - 如何比较历史数据

### 示例文件：

- **`examples/system-check.md`** - 完整的系统健康检查工作流程
- **`examples/deployment.md`** - 多步骤部署示例
- **`examples/troubleshooting.md`** - 问题诊断工作流程

### 脚本：

- **`scripts/create-workdir.sh`** - 创建新的工作目录结构
- **`scripts/log-command.sh`** - 将命令执行结果记录到工作目录
- **`scripts/save-status.sh`** - 捕获并保存服务器状态信息