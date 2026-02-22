---
name: openclaw-whatsapp
description: OpenClaw的WhatsApp桥接功能：支持发送/接收消息、自动回复、二维码配对、消息搜索以及联系人同步。
---
# openclaw-whatsapp

这是一个用于将 OpenClaw 代理与 WhatsApp 连接的桥接工具。它支持发送消息、使用 AI 自动回复私信、搜索消息历史记录以及同步联系人信息——所有这些功能都通过一个 Go 编写的二进制文件实现。

## 快速参考

```bash
# Check status
openclaw-whatsapp status

# Send a message
openclaw-whatsapp send "NUMBER@s.whatsapp.net" "Your message"

# View logs (if running as service)
journalctl --user -u openclaw-whatsapp.service -f

# View worker logs
tail -f /tmp/openclaw-wa-agent/worker.log
```

## 完整设置（自助服务）

按照以下步骤从零开始设置 WhatsApp 自动回复功能：

### 第 1 步：安装二进制文件

```bash
curl -fsSL https://raw.githubusercontent.com/0xs4m1337/openclaw-whatsapp/main/install.sh | bash
```

验证安装是否成功：
```bash
openclaw-whatsapp version
```

### 第 2 步：找到 OpenClaw 二进制文件的路径

```bash
which openclaw
# Example output: /home/USER/.nvm/versions/node/v22.22.0/bin/openclaw
```

保存该路径——您将在第 4 步中使用它。

### 第 3 步：安装中继脚本

从该工具目录中复制所需的脚本：

```bash
SKILL_DIR="$(dirname "$(realpath "$0")")"  # or use absolute path to skill

# Copy scripts
sudo cp "$SKILL_DIR/scripts/wa-notify.sh" /usr/local/bin/wa-notify.sh
sudo cp "$SKILL_DIR/scripts/wa-notify-worker.sh" /usr/local/bin/wa-notify-worker.sh
sudo chmod +x /usr/local/bin/wa-notify.sh /usr/local/bin/wa-notify-worker.sh
```

如果您以代理模式运行，可以直接使用工具目录的路径：
```bash
cp ~/clawd/skills/openclaw-whatsapp/scripts/wa-notify.sh /usr/local/bin/
cp ~/clawd/skills/openclaw-whatsapp/scripts/wa-notify-worker.sh /usr/local/bin/
chmod +x /usr/local/bin/wa-notify.sh /usr/local/bin/wa-notify-worker.sh
```

### 第 4 步：配置工作脚本

编辑 `/usr/local/bin/wa-notify-worker.sh` 文件，并将 `PATH` 变量设置为第 2 步中获得的 OpenClaw 二进制文件路径：

```bash
# Find this line near the top:
export PATH="/home/oussama/.nvm/versions/node/v22.22.0/bin:$PATH"

# Change it to your actual path:
export PATH="/home/YOUR_USER/.nvm/versions/node/vXX.XX.X/bin:$PATH"
```

同时更新 `/usr/local/bin/wa-notify.sh` 文件中的工作脚本路径：
```bash
# Find this line near the bottom:
nohup /home/oussama/dev/openclaw-whatsapp/scripts/wa-notify-worker.sh

# Change to:
nohup /usr/local/bin/wa-notify-worker.sh
```

### 第 5 步：创建配置文件

```bash
mkdir -p ~/.openclaw-whatsapp
cat > ~/.openclaw-whatsapp/config.yaml << 'EOF'
port: 8555
data_dir: ~/.openclaw-whatsapp
auto_reconnect: true
reconnect_interval: 30s
log_level: info

agent:
  enabled: true
  mode: "command"
  command: "/usr/local/bin/wa-notify.sh '{name}' '{message}' '{chat_jid}' '{message_id}'"
  ignore_from_me: true
  dm_only: true
  timeout: 30s
  system_prompt: |
    You are a helpful WhatsApp assistant. Be concise and natural.
EOF
```

### 第 6 步：创建 systemd 服务（推荐）

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/openclaw-whatsapp.service << 'EOF'
[Unit]
Description=OpenClaw WhatsApp Bridge
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/openclaw-whatsapp start -c %h/.openclaw-whatsapp/config.yaml
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reload
systemctl --user enable openclaw-whatsapp.service
systemctl --user start openclaw-whatsapp.service
```

### 第 7 步：配置 WhatsApp 连接

1. 检查桥接服务是否正在运行：`openclaw-whatsapp status`
2. 打开 QR 代码页面：`http://localhost:8555/qr`
3. 在您的手机上：进入 WhatsApp → 设置 → 关联设备 → 关联设备
4. 扫描 QR 代码

### 第 8 步：测试

使用另一部手机向已关联的 WhatsApp 账号发送消息，并检查结果：
```bash
# Bridge logs
journalctl --user -u openclaw-whatsapp.service -n 20

# Worker logs
cat /tmp/openclaw-wa-agent/worker.log
```

## 架构

```
WhatsApp DM → Bridge → wa-notify.sh (enqueue)
  → wa-notify-worker.sh (background, file-locked)
  → Fetches last 10 messages for context
  → openclaw agent (processes message)
  → openclaw-whatsapp send <JID> <reply>
  → WhatsApp reply sent
```

**主要特性：**
- **快速排队**：桥接工具不会等待代理处理消息
- **去重**：通过跟踪消息 ID 来防止重复回复
- **单个工作进程**：采用文件锁机制进行顺序处理，避免竞态条件
- **容错性**：队列数据在系统重启后仍会保留

## 自定义系统提示信息

编辑 `~/.openclaw-whatsapp/config.yaml` 文件，并更新 `systemprompt` 字段：

```yaml
agent:
  system_prompt: |
    You are a sales assistant for Acme Corp.
    Be friendly and professional.
    When someone wants to book a demo:
    - Book via: mcporter call composio.GOOGLECALENDAR_CREATE_EVENT ...
    - Notify team via: message action=send channel=telegram target=CHAT_ID ...
```

修改完成后重启系统：
```bash
systemctl --user restart openclaw-whatsapp.service
```

## 允许列表 / 取消允许列表

您可以限制代理响应的手机号码范围：

```yaml
agent:
  allowlist: ["971586971337"]  # only these (empty = all)
  blocklist: ["spammer123"]     # never these
```

## 命令行接口 (CLI) 参考

```bash
openclaw-whatsapp start [-c config.yaml]  # Start the bridge
openclaw-whatsapp status [--addr URL]      # Check connection status
openclaw-whatsapp send NUMBER MESSAGE      # Send a message
openclaw-whatsapp stop                     # Stop the bridge
openclaw-whatsapp version                  # Print version
```

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| QR 代码失效 | 重新访问 `http://localhost:8555/qr`（每 3 秒自动刷新）|
| 桥接服务断开 | 查看 `openclaw-whatsapp status`；系统会自动重新连接|
| 代理未响应 | 查看 `/tmp/openclaw-wa-agent/worker.log` 文件以获取错误信息|
| 出现 “stream replaced” 错误 | 可能有多个桥接实例运行，请确保只有一个实例在运行（使用 `systemctl --user status openclaw-whatsapp` 和 `pgrep openclaw-whatsapp` 命令检查）|
| 报错 “openclaw: not found” | 确保 `wa-notify-worker.sh` 文件中的 `PATH` 设置正确，包含 OpenClaw 二进制文件的路径|
| 报错 “未登录” | 重新扫描 QR 代码——可能是会话已过期|

## 相关文件

| 文件路径 | 说明 |
|------|-------------|
| `~/.openclaw-whatsapp/config.yaml` | 桥接配置文件 |
| `~/.openclaw-whatsapp/messages.db` | SQLite 消息存储数据库 |
| `~/.openclaw-whatsapp/sessions/` | WhatsApp 会话数据目录 |
| `/tmp/openclaw-wa-agent/queue.jsonl` | 消息队列文件 |
| `/tmp/openclaw-wa-agent/worker.log` | 工作进程日志文件 |
| `/tmp/openclaw-wa-agent/seen_message_ids.txt` | 去重列表文件 |

## API 接口

| 方法 | 路径 | 说明 |
|--------|------|-------------|
| `GET` | `/status` | 获取连接状态 |
| `GET` | `/qr` | 显示 QR 代码页面 |
| `POST` | `/send/text` | 发送消息（格式：`{"to": "...", "message": "..."}`） |
| `GET` | `/chats` | 显示所有聊天记录 |
| `GET` | `/chats/{jid}/messages?limit=10` | 查看指定聊天的消息 |
| `GET` | `/messages/search?q=keyword` | 全文搜索 |

更多 API 文档请参阅 [references/api-reference.md](references/api-reference.md)。