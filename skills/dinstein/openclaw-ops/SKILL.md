---
name: openclaw-ops
version: 1.2.1
description: >
  **使用说明：**  
  适用于在同一台机器上诊断、修复或维护 OpenClaw Gateway 时使用。专为救援人员设计，用于修复故障的 Gateway 或检查其运行状态。支持 Linux（systemd）和 macOS（launchd）系统。
repository: https://github.com/dinstein/openclaw-ops-skill
requirements:
  - Shell access on the same machine as the OpenClaw Gateway
  - Read/write access to ~/.openclaw/ (config, agents, sessions)
  - Read access to systemd user service config (Linux) or LaunchAgents (macOS)
  - Node.js 18+ and npm (for openclaw CLI)
  - Optional: Tailscale CLI (for reverse proxy troubleshooting)
security_notes:
  - This skill instructs the agent to read and modify OpenClaw config files
  - The agent will access env files containing tokens (but is instructed never to print them)
  - Config edits are always preceded by timestamped backups
  - Destructive operations require user confirmation
---
# OpenClaw 操作指南

## 设计理念

本技能仅适用于 **两个核心场景**：

1. **救援**：当 OpenClaw 主网关出现故障或无法正常运行时，您（救援人员）需要诊断问题的根本原因，进行修复，并使网关重新上线。
2. **健康检查**：当 OpenClaw 主网关正在运行时，您需要验证其运行状态，清理资源，或执行升级等维护任务。

**本技能不适用于以下场景：**
- 日常业务配置（添加通道、配置代理、设置集成）
- 应用层问题（代理行为、提示设置、技能管理）
- 初始部署或首次设置（请使用 `openclaw daemon install` 和 `openclaw configure`）

**操作原则：** 诊断 → 判断 → 行动 → 验证。切勿跳过任何步骤。

## 平台检测

首先检测操作系统类型——Linux（使用 systemd）和 macOS（使用 launchd）的命令有所不同：

```bash
OS=$(uname -s)  # "Linux" or "Darwin"
echo "Platform: $OS"
```

## 端口检测

不要默认使用端口 18789，应先检测实际配置的端口：

```bash
PORT=$(openclaw config get gateway.port 2>/dev/null | grep -oE '[0-9]+')
PORT=${PORT:-18789}  # fallback to default only if config unavailable
echo "Gateway port: $PORT"
```

在本指南中，所有与端口相关的命令中均使用 `$PORT` 变量。

---

# 场景 A：救援（网关故障）

当主网关无法运行时，请按以下步骤操作：

## A1. 评估情况

```bash
# Is the service running at all?
# Linux:
systemctl --user status openclaw-gateway
# macOS:
launchctl list | grep openclaw

# Is the process alive?
pgrep -af openclaw

# Is the port listening?
# Linux:
ss -tlnp | grep $PORT
# macOS:
lsof -iTCP:$PORT -sTCP:LISTEN
```

## A2. 查看日志以确定根本原因

**Linux:**
```bash
journalctl --user -u openclaw-gateway --since "1 hour ago" --no-pager | grep -iE "error|crash|fatal|SIGTERM|OOM"

# Last 50 lines for context
journalctl --user -u openclaw-gateway -n 50 --no-pager
```

**macOS:**
```bash
LOG_DIR="$HOME/.openclaw/logs"
grep -iE "error|crash|fatal" "$LOG_DIR/gateway.log" | tail -20
tail -50 "$LOG_DIR/gateway.log"

# Also check unified log
log show --predicate 'process == "node"' --last 1h | grep -iE "error|crash|fatal"
```

### 常见故障模式

| 日志信息 | 含义 | 解决方法 |
|------------|---------|-----|
| `EADDRINUSE` | 端口已被占用 | 查找占用该端口的进程：`ss -tlnp \| grep $PORT`（Linux）或 `lsof -iTCP:$PORT`（macOS），终止该进程或更换端口 |
| `ENOMEM` / `JavaScript heap` | 内存不足 | 查看 `free -h`（Linux）/ `vm_stat`（macOS），关闭占用大量内存的进程或增加 Node.js 的堆内存 |
| `SyntaxError` 在配置文件中 | `openclaw.json` 中的 JSON 格式错误 | 请参见 A3 部分中的配置修复方法 |
| `MODULE_NOT_FOUND` | 缺少依赖项 | 执行 `cd $(npm root -g)/openclaw && npm install --production` |
| `Invalid token` / `401` / `403` | 认证失败 | 检查环境文件中的认证令牌 |
| `ECONNREFUSED` | 上游服务器无法连接 | 检查网络连接、Tailscale 服务或 API 端点 |

## A3. 配置修复

**务必先备份配置文件：**
```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%s)
```

**JSON 格式验证：**
```bash
python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json'))"
```

常见的 JSON 错误包括：末尾多余的逗号、缺少引号、未转义的字符。错误信息会显示出出错的行和位置。

**配置模式验证：**
```bash
openclaw config get gateway  # check gateway config section
openclaw config get channels  # check channels config section
```

**常见配置错误：**

| 错误症状 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| “设备身份不匹配” | 服务环境中的令牌与配置文件中的令牌不一致 | 请同步环境文件和 `openclaw.json` 中的令牌 |
| 代理无法正常路由 | `bindings` 配置错误 | 请确保 `bindings` 配置位于配置文件的顶层，而不是 `agents.list[]`.routing` 内部 |

**修复后，请进行验证：**
```bash
python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json')); print('JSON OK')"
openclaw status
```

## A4. 清理资源

```bash
# Disk space
df -h ~

# Memory (Linux)
free -h
# Memory (macOS)
vm_stat | head -5

# Node.js available?
node -v
which openclaw
openclaw --version
```

## A5. 重启并验证

**只有在确定并修复了根本原因后，才能重启网关。**

**Linux:**
```bash
systemctl --user restart openclaw-gateway
sleep 3
systemctl --user status openclaw-gateway
journalctl --user -u openclaw-gateway -n 20 --no-pager
```

**macOS:**
```bash
launchctl kickstart -k "gui/$(id -u)/com.openclaw.gateway"
sleep 3
launchctl list | grep openclaw
tail -20 ~/.openclaw/logs/gateway.log
```

**如果服务完全无法启动：**
```bash
# Manual foreground start for better error output
openclaw gateway start
```

**最终验证：**
```bash
openclaw status
openclaw doctor --non-interactive
```

---

# 场景 B：健康检查（网关正常运行）

对于正常运行的网关，请按照以下步骤进行常规维护检查：

## B1. 快速健康检查

```bash
# Comprehensive check — start here
openclaw doctor

# If issues found, auto-fix safe ones
openclaw doctor --fix
```

## B2. 更新与升级

```bash
# Check versions
CURRENT=$(openclaw --version)
LATEST=$(npm view openclaw version)
echo "Current: $CURRENT  Latest: $LATEST"
```

**执行更新：**
```bash
# 1. Save doctor baseline
openclaw doctor --non-interactive 2>&1 | tee /tmp/doctor-before.txt

# 2. Backup config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.pre-upgrade.$(date +%s)

# 3. Update
npm update -g openclaw
openclaw --version

# 4. Restart
# Linux:
systemctl --user restart openclaw-gateway
# macOS:
launchctl kickstart -k "gui/$(id -u)/com.openclaw.gateway"

# 5. Compare doctor output
sleep 5
openclaw doctor --non-interactive 2>&1 | tee /tmp/doctor-after.txt
diff /tmp/doctor-before.txt /tmp/doctor-after.txt
```

**回滚：**
```bash
npm install -g openclaw@<previous_version>
cp ~/.openclaw/openclaw.json.pre-upgrade.<timestamp> ~/.openclaw/openclaw.json
# Restart (platform-appropriate command above)
```

## B3. 会话与磁盘清理

```bash
# Check disk usage per agent
for agent_dir in ~/.openclaw/agents/*/; do
    agent=$(basename "$agent_dir")
    size=$(du -sh "$agent_dir/sessions/" 2>/dev/null | cut -f1)
    count=$(find "$agent_dir/sessions/" -name "*.jsonl" 2>/dev/null | wc -l)
    echo "$agent: $size ($count transcripts)"
done

# Auto-fix orphans
openclaw doctor --fix

# Manual cleanup: old transcripts (>30 days)
find ~/.openclaw/agents/*/sessions/ -name "*.jsonl" -mtime +30 -exec ls -lh {} \;
# Review, then delete if safe:
find ~/.openclaw/agents/*/sessions/ -name "*.jsonl" -mtime +30 -delete
```

## B4. 备份数据

```bash
BACKUP_DIR=~/openclaw-backup-$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP_DIR"

# Core files
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
[ -f ~/.openclaw/env ] && cp ~/.openclaw/env "$BACKUP_DIR/" || echo "No env file (tokens may be in systemd drop-in or plist)"
cp -r ~/.openclaw/agents "$BACKUP_DIR/"
cp -r ~/.openclaw/devices "$BACKUP_DIR/"
cp -r ~/.openclaw/workspace "$BACKUP_DIR/"

# Service config
if [ "$(uname -s)" = "Linux" ]; then
    cp ~/.config/systemd/user/openclaw-gateway.service "$BACKUP_DIR/" 2>/dev/null
    cp -r ~/.config/systemd/user/openclaw-gateway.service.d "$BACKUP_DIR/" 2>/dev/null
elif [ "$(uname -s)" = "Darwin" ]; then
    cp ~/Library/LaunchAgents/com.openclaw.gateway.plist "$BACKUP_DIR/" 2>/dev/null
fi

echo "Backup saved to $BACKUP_DIR"
```

## B5. 检查 Tailscale 代理服务

如果 OpenClaw 使用 Tailscale 作为反向代理，请执行以下操作：

```bash
tailscale status
tailscale serve status
curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/healthz || echo "Gateway not reachable on localhost"
```

**如果 Tailscale 代理服务出现故障，请重新配置：**
```bash
tailscale serve reset
tailscale serve https / http://localhost:$PORT
tailscale serve status
```

---

# 参考资料

## 故障排除快速指南

| 错误症状 | 对应操作 |
|---------|------|
| 网关无法启动 | A1 → A2 → A3 → A5 |
| 网关崩溃 | A2（查看日志）→ A4（检查资源）→ A3（检查配置）→ A5（重启） |
| 配置文件修改后出现问题 | A3 → A5 |
| 磁盘空间不足 | B3 |
| 升级后出现问题 | B2（执行回滚操作） |
| Tailscale 代理服务无法正常工作 | B5 |

## `openclaw doctor` 命令参考

| 命令参数 | 功能 |
|------|--------|
| (无参数) | 执行交互式健康检查 |
| `--fix` | 执行安全修复操作（如清理无效会话、释放旧锁） |
| `--force` | 执行强力修复操作（可能会覆盖自定义服务配置） |
| `--deep` | 检查系统中是否存在多余的网关实例 |
| `--non-interactive` | 无提示界面，仅执行安全迁移操作 |

**`--fix` 命令的作用：** 清理无效的会话记录、释放旧的会话锁、迁移旧版本的配置文件。  
**`--fix` 命令不会：** 修改 `openclaw.json` 文件、更改服务配置文件（除非使用了 `--force` 参数），也不会删除工作区文件。

## 常用命令

| 命令 | 功能 |
|---------|---------|
| `openclaw status` | 查看快速状态信息（是否正在运行、版本号、基本信息） |
| `openclaw doctor` | 执行深度健康检查（包括服务状态、通道列表、插件信息） |
| `openclaw doctor --fix` | 执行健康检查并自动修复常见问题 |
| `openclaw gateway start` | 以前台模式启动网关（便于调试） |
| `openclaw daemon install` | 将 OpenClaw 作为持久化服务安装（适用于 systemd 或 launchd） |
| `openclaw daemon restart` | 重启服务 |
| `openclaw config get <路径>` | 读取配置文件中的值 |
| `openclaw config set <路径> <值>` | 向配置文件中写入值 |

## 安全注意事项

1. **在任何更改之前，务必查看日志** — 先了解问题的根本原因。
2. **编辑配置文件之前，务必先备份** — 使用带有时间戳的后缀进行备份。
3. **编辑配置文件后，务必验证 JSON 格式** — 一个错误的逗号都可能导致服务崩溃。
4. **切勿泄露敏感信息** — 在查看日志之前，请先确认环境文件的存在。
5. **切勿删除工作区文件** — 如有必要删除文件，请使用 `trash` 命令。
6. **重启后务必进行验证** — 通过查看状态信息和日志来确认操作是否成功。
7. **执行可能破坏数据的操作前，请务必获得用户确认**。

## 文件结构

```
~/.openclaw/
├── openclaw.json              # Main config
├── openclaw.json.bak          # Auto-backup
├── env                        # Environment variables (secrets)
├── logs/                      # macOS: launchd log output
├── agents/                    # Per-agent configs
│   └── <agent>/agent/
│       ├── auth-profiles.json
│       └── models.json
├── devices/
│   └── paired.json
├── workspace/                 # Agent workspace
└── sessions/                  # Session logs

# Linux:
~/.config/systemd/user/
├── openclaw-gateway.service
└── openclaw-gateway.service.d/
    └── env.conf

# macOS:
~/Library/LaunchAgents/
└── com.openclaw.gateway.plist
```