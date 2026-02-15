---
name: imap-idle
description: 基于 IMAP IDLE 协议的事件驱动型电子邮件监控系统。该系统通过 OpenClaw 的 Webhook 实现即时推送通知，替代了传统的轮询机制。适用于设置电子邮件监控任务、替代每小时一次的邮件检查功能，或实现基于事件的电子邮件处理流程。该系统能够监控多个 IMAP 账户，并在新邮件到达时触发相应的 Webhook；在等待新邮件的过程中，系统不会消耗任何资源（即不会消耗任何令牌）。
---

# IMAP IDLE 监听器

使用 IMAP IDLE 协议为 OpenClaw 提供基于事件的电子邮件通知功能。

## 功能简介

该插件将基于轮询的电子邮件检查方式替换为推送通知：

**轮询方式（之前）：**
- 使用 Cron 作业每小时检查一次电子邮件
- 每天检查 16 到 24 次
- 新邮件可能存在长达 1 小时的延迟
- 无新邮件时会导致令牌被消耗

**IMAP IDLE 方式（之后）：**
- 与 IMAP 服务器保持持续连接
- 服务器在新邮件到达时立即发送通知
- 通知延迟小于 1 秒
- 等待期间不会消耗任何令牌

## 快速入门

### 1. 启用 OpenClaw Webhook

编辑 `~/.openclaw/openclaw.json` 文件：

```json
{
  "hooks": {
    "enabled": true,
    "token": "generate-secure-random-token-here",
    "path": "/hooks"
  }
}
```

重启 OpenClaw 服务：`openclaw gateway restart`

### 2. 安装依赖项

```bash
pip3 install imapclient --user --break-system-packages
```

**建议安装（非强制）：** 安装 keyring 以安全存储密码：

```bash
pip3 install keyring --user --break-system-packages
```

通过 keyring，密码将存储在系统的安全密钥链中（macOS Keychain、GNOME Keyring 等），而不会以明文形式保存在配置文件中。

### 3. 运行设置向导

按照向导的提示配置以下内容：
- IMAP 账户信息（主机、端口、用户名、密码）
- OpenClaw Webhook 的 URL 和令牌
- 日志文件的位置

### 4. 启动监听器

```bash
./imap-idle start
```

验证监听器是否已成功启动：

```bash
./imap-idle status
./imap-idle logs
```

### 5. 测试

给自己发送一封电子邮件。你应该看到：
1. 监听器日志中记录了该操作
2. OpenClaw 立即响应并处理邮件
3. 邮件在主会话中得到处理

## 命令行接口（CLI）命令

```bash
imap-idle start    # Start listener in background
imap-idle stop     # Stop listener
imap-idle restart  # Restart listener
imap-idle status   # Check if running
imap-idle logs     # Show recent logs (default: 50 lines)
imap-idle logs N   # Show last N lines
imap-idle setup    # Run interactive setup wizard
```

## 配置文件

配置文件位于：`~/.openclaw/imap-idle.json`

```json
{
  "accounts": [
    {
      "host": "mail.example.com",
      "port": 993,
      "username": "user@example.com",
      "password": "password",
      "ssl": true
    }
  ],
  "webhook_url": "http://127.0.0.1:18789/hooks/wake",
  "webhook_token": "your-webhook-token",
  "log_file": "~/.openclaw/logs/imap-idle.log",
  "idle_timeout": 300,
  "reconnect_interval": 900,
  "debounce_seconds": 10
}
```

**配置字段：**
- `accounts` - 需要监控的 IMAP 账户数组
- `webhook_url` - OpenClaw Webhook 的端点地址
- `webhook_token` - Webhook 认证令牌（来自 `openclaw.json` 文件）
- `log_file` - 日志文件的路径（设置为 `null` 时使用标准输出）
- `idle_timeout` - IDLE 检查的超时时间（单位：秒，默认值：300 秒，即 5 分钟）
- `reconnect_interval` - 重新连接的间隔时间（单位：秒，默认值：900 秒，即 15 分钟）
- `debounce_seconds` - 在发送 Webhook 之前批量处理事件的间隔时间（单位：秒，默认值：10 秒）

## 安全的密码存储（Keyring）

**🔐 建议使用 keyring：** 将密码存储在系统的密钥链中，而非配置文件中。

### 使用 keyring 的设置方法

运行 `./imap-idle setup` 向导时，系统会询问你是否希望使用 keyring。选择“是”后：
- 密码将保存在系统的安全密钥链中
- 配置文件中仅包含用户名，不包含密码
- keyring 使用操作系统级别的加密机制

### 手动将配置文件中的密码迁移到 keyring

如果你现有的配置文件中仍包含明文密码，可以按照以下步骤进行迁移：

```bash
# Install keyring
pip3 install keyring --user --break-system-packages

# Store password for each account
python3 -c "
import keyring, getpass
username = 'user@example.com'
password = getpass.getpass(f'Password for {username}: ')
keyring.set_password('imap-idle', username, password)
"

# Remove password from config
# Edit ~/.openclaw/imap-idle.json and remove "password" field
```

### keyring 的工作原理

监听器会首先尝试从 keyring 中获取密码；如果失败，则会从配置文件中获取。具体步骤如下：
1. 尝试使用 `keyring.get_password('imap-idle', username)` 获取密码
2. 如果找不到密码，则使用 `config['password']`
3. 如果仍然无法获取密码，则断开连接

### 安全优势：
- 配置文件中不存在明文密码
- 使用操作系统级别的加密技术（macOS Keychain、GNOME Keyring、Windows Credential Manager）
- 降低 VirusTotal 工具误报的概率
- 提高安全审计的透明度

## 工作流程：
1. **连接**：为每个账户建立持久的 IMAP 连接
2. **进入 IDLE 模式**：进入 IDLE 模式，等待服务器发送通知
3. **等待**：等待服务器发送“新邮件”通知
4. **获取邮件信息**：获取新邮件的头部信息（发件人、主题、邮件预览）
5. **批量处理**：将邮件信息放入缓冲区，等待 10 秒后再批量发送给 Webhook
6. **发送通知**：通过 Webhook 发送批量处理后的邮件信息（可以单独发送或分组发送）
7. **重新进入 IDLE 模式**：完成邮件处理后，再次进入 IDLE 模式

**关键实现细节：**
- **批量处理**：在发送 Webhook 之前，将邮件信息批量处理（等待 10 秒），以防止在高流量时段发送过多请求
- **智能分组**：单封邮件时发送完整信息；多封邮件时发送汇总信息及邮件数量
- **UID 跟踪**：记录每个账户最后处理的邮件 UID，避免重复触发 Webhook
- **保持连接**：每 5 分钟发送一次 NOOP 命令以保持连接活跃
- **自动重连**：每 15 分钟重新建立连接，防止连接中断
- **多线程处理**：每个账户使用单独的线程进行并发监控
- **错误处理**：在连接失败时采用指数级退避策略（5 秒 → 300 秒）

## systemd 服务（可选）

若希望系统启动时自动运行该插件，可以按照以下步骤操作：
1. 生成服务配置文件：
```bash
skill_dir="$(pwd)"
listener_script="$skill_dir/scripts/listener.py"
config_file="$HOME/.openclaw/imap-idle.json"
log_file="$HOME/.openclaw/logs/imap-idle.log"
log_dir="$(dirname "$log_file")"

sed -e "s|%USER%|$USER|g" \
    -e "s|%PYTHON%|$(which python3)|g" \
    -e "s|%LISTENER_SCRIPT%|$listener_script|g" \
    -e "s|%CONFIG_FILE%|$config_file|g" \
    -e "s|%LOG_FILE%|$log_file|g" \
    -e "s|%LOG_DIR%|$log_dir|g" \
    imap-idle.service.template > imap-idle.service
```

2. 安装服务：
```bash
sudo cp imap-idle.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable imap-idle
sudo systemctl start imap-idle
```

3. 检查服务状态：
```bash
sudo systemctl status imap-idle
sudo journalctl -u imap-idle -f
```

## 常见问题及解决方法：

**监听器无法启动：**
- 确保配置文件存在：`cat ~/.openclaw/imap-idle.json`
- 确保已安装 `imapclient`：`python3 -c "import imapclient"`
- 查看日志文件：`imap-idle logs`

**Webhook 被重复触发：**
- 该问题已在版本 2 中得到解决，通过 UID 跟踪机制避免了重复触发
- 查看日志文件中是否有关于 UID 跟踪的记录

**连接中断：**
- 增加配置文件中的 `reconnect_interval` 值
- 确认 IMAP 服务器支持 IDLE 模式（大多数服务器都支持）
- 检查防火墙设置是否允许持续连接

**Webhook 未触发：**
- 手动测试 Webhook 功能：
  ```bash
  curl -X POST http://127.0.0.1:18789/hooks/wake \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"text": "test", "mode": "now"}'
  ```
- 确认 OpenClaw 配置文件中的 `hooks.enabled` 选项设置为 `true`
- 确认两个配置文件中的 Webhook 令牌一致

## 移除旧的轮询机制

一旦 IMAP IDLE 功能启用，建议删除旧的轮询 Cron 作业：

```bash
# List cron jobs
openclaw cron list

# Remove email check job
openclaw cron remove <job-id>
```

## 令牌使用情况：

**轮询方式（之前）：**
- 每天检查 16 到 24 次电子邮件
- 每次检查会消耗约 500 到 1000 个令牌（即使没有新邮件）
- 每天用于电子邮件监控的令牌总数约为 8,000 到 24,000 个

**IMAP IDLE 方式（之后）：**
- 等待期间不消耗令牌
- 仅在实际收到新邮件时才会消耗令牌
- 邮件相关令牌的使用量减少了 90% 以上

## 致谢

本功能的灵感来源于 @claude-event-listeners 在 Moltbook 上对轮询机制与基于事件驱动的架构的评论。具体的实现细节来源于 Moltbook 的文章《事件驱动的电子邮件通知：从轮询到 IMAP IDLE（附带代码示例）》。