---
name: openclaw-watchdog
description: OpenClaw网关的自我修复监控系统：能够自动检测故障、修复崩溃问题，并通过Telegram发送警报。
homepage: https://github.com/Abdullah4AI/openclaw-watchdog
metadata: {"openclaw":{"emoji":"🐕","disableModelInvocation":true,"requires":{"bins":["python3","openssl"],"env":["TELEGRAM_TOKEN","TELEGRAM_CHAT_ID"]},"install":[{"id":"setup","kind":"script","script":"scripts/setup.sh","label":"Install watchdog service (LaunchAgent/systemd user)","persistence":"user-level","service":true}]}}
---

# openclaw-watchdog

**描述：** 专为 OpenClaw 网关设计的自修复监控系统。该系统能够监控网关的运行状态，在发生故障时自动重启，并通过 Telegram 发送警报。所有诊断信息和日志分析都在设备上本地完成。警报通知会发送到用户的 Telegram 账号。适用于需要设置网关监控、故障检测或自动恢复功能的用户。

## 先决条件
- **Telegram 账号** — 需要通过 [@BotFather](https://t.me/BotFather) 创建一个 Telegram 账号，并获取相应的 Token（格式为 `123456:ABC-DEF...`）
- **Telegram 聊天 ID** — 用于接收警报的个人聊天 ID
- **Python 3** — 监控服务需要 Python 3 环境
- **OpenClaw** — 确保 OpenClaw 已安装并正在运行

## 关键词
- 监控（monitoring）、自动修复（auto-repair）、网关健康（gateway health）、自修复（self-healing）、自动恢复（auto-recovery）、故障检测（watchdog）

## 设置流程

请向用户发送一条包含所有必要信息的消息：

---

🐕 **Watch Dog — 自修复网关监控工具**

Watch Dog 是一个后台服务，每 15 秒会向您的 OpenClaw 网关发送一次 Ping 请求。如果网关出现故障，它会自动尝试重启，并通过 Telegram 向您发送警报，确保您随时了解网关的状态。所有诊断信息都在您的设备上本地处理。

要设置该服务，请提供以下信息：
1. **Telegram 账号 Token** — 通过 [@BotFather](https://t.me/BotFather) 在 Telegram 上创建一个账号，并将 Token 发送给我（格式为 `123456:ABC-DEF...`）
2. **您的 Telegram 聊天 ID** — 向您的账号发送 `/start` 命令，然后访问 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` 以获取您的聊天 ID

请将 Token 和聊天 ID 发送给我，其余步骤我会为您完成（包括进行测试以确保一切正常运行！）

---

## 收到凭据后

请按照以下顺序执行操作：

### 1. 验证凭据
```bash
python3 ~/.openclaw/workspace/openclaw-watchdog/scripts/validate.py "$TELEGRAM_TOKEN"
```

### 2. 运行设置脚本
```bash
chmod +x ~/.openclaw/workspace/openclaw-watchdog/scripts/setup.sh
~/.openclaw/workspace/openclaw-watchdog/scripts/setup.sh \
  --telegram-token "$TELEGRAM_TOKEN" \
  --telegram-chat-id "$TELEGRAM_CHAT_ID"
```

### 3. 通过 Telegram 连接（配对）
```bash
python3 ~/.openclaw/workspace/openclaw-watchdog/scripts/test-message.py "$TELEGRAM_TOKEN" "$TELEGRAM_CHAT_ID"
```
等待用户确认收到 Telegram 消息后再继续下一步。

### 4. 验证服务是否正在运行
```bash
# Check service status
if [[ "$(uname)" == "Darwin" ]]; then
  launchctl list | grep openclaw.watchdog
else
  systemctl --user status openclaw-watchdog
fi

# Check logs
tail -20 ~/.openclaw/watchdog/watchdog.log
```

### 5. 告知用户服务状态
向用户确认 Watch Dog 已经启动、监控的内容，以及如果出现故障会发送 Telegram 警报。

## 工作原理
- 每 15 秒向 `localhost:3117/health` 发送一次 Ping 请求
- 如果连续三次检测到网关故障，会尝试重启网关
- 最多尝试两次重启后，会通过 Telegram 请求用户的重启权限
- 用户需要运行 `touch ~/.openclaw/watchdog/approve-reinstall` 来批准重启
- 未经批准时，系统仅发送警报，不会执行任何破坏性操作
- 采用 AES-256 加密算法对用户凭据进行加密（使用设备特有的密钥）

## 卸载
```bash
if [[ "$(uname)" == "Darwin" ]]; then
  launchctl unload ~/Library/LaunchAgents/com.openclaw.watchdog.plist 2>/dev/null
  rm -f ~/Library/LaunchAgents/com.openclaw.watchdog.plist
else
  systemctl --user stop openclaw-watchdog 2>/dev/null
  systemctl --user disable openclaw-watchdog 2>/dev/null
  rm -f ~/.config/systemd/user/openclaw-watchdog.service
fi
rm -rf ~/.openclaw/watchdog
```