---
name: openclaw-watchdog
description: OpenClaw网关的自我修复监控系统：能够自动检测故障、修复崩溃问题，并通过Telegram发送警报。
homepage: https://github.com/Abdullah4AI/openclaw-watchdog
metadata: {"openclaw":{"emoji":"🐕","disableModelInvocation":true,"requires":{"bins":["python3","openssl"],"env":["TELEGRAM_TOKEN","TELEGRAM_CHAT_ID"]},"install":[{"id":"setup","kind":"script","script":"scripts/setup.sh","label":"Install watchdog service (LaunchAgent/systemd user)","persistence":"user-level","service":true}]}}
---
# openclaw-watchdog

**描述：** 专为 OpenClaw 网关设计的自修复监控系统。该系统可监控网关的运行状态，在网关出现故障时自动重启，并通过 Telegram 发送警报。所有诊断信息和日志分析都在设备上本地完成。警报通知会发送到用户的 Telegram 聊天机器人。适用于需要设置网关监控、故障监控或自动恢复功能的用户。

## 先决条件
- **Telegram 聊天机器人令牌** — 需要通过 [@BotFather](https://t.me/BotFather) 创建一个 Telegram 聊天机器人，并获取相应的令牌（格式为 `123456:ABC-DEF...`）
- **您的 Telegram 聊天 ID** — 用于接收警报的个人聊天 ID
- **Python 3** — 监控服务需要 Python 3 环境
- **OpenClaw** — 已安装并正在运行中

## 关键词
- 监控（monitoring）、自动修复（auto-repair）、网关健康（gateway health）、自修复（self-healing）、自动恢复（auto-recovery）、故障监控（watchdog）

## 设置流程

请向用户发送一条包含所有所需信息的消息：

---

🐕 **故障监控工具 — OpenClaw 网关自修复监控系统**

“故障监控工具”是一个后台服务，每 15 秒会向您的 OpenClaw 网关发送一次检测请求。如果网关出现故障，它会自动尝试重启，并通过 Telegram 向您发送警报，确保您随时了解网关的状态。所有诊断信息都在您的设备上本地处理。

要设置该服务，请提供以下信息：
1. **Telegram 聊天机器人令牌** — 通过 [@BotFather](https://t.me/BotFather) 创建一个聊天机器人，并将令牌发送给我（格式示例：`123456:ABC-DEF...`）
2. **您的 Telegram 聊天 ID** — 向聊天机器人发送 `/start` 命令，然后访问 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` 以获取您的聊天 ID

请将令牌和聊天 ID 发送给我，其余步骤我会为您完成（包括进行测试以确保一切正常运行！）

---

## 收到凭据后

请按以下顺序执行操作：

### 1. 验证凭据
```bash
python3 ~/.openclaw/workspace/openclaw-watchdog/scripts/validate.py "$TELEGRAM_TOKEN"
```

### 2. 运行设置脚本
```bash
chmod +x ~/.openclaw/workspace/openclaw-watchdog/scripts/setup.sh
~/.openclaw/workspace/openclaw-watchdog/scripts/setup.sh \
  --telegram-token "$TELEGRAM_TOKEN" \
  --telegram-chat-id "$TELEGRAM_CHAT_ID" \
  --gateway-port "$GATEWAY_PORT"  # optional, auto-detected from openclaw.json
```

### 3. 通过 Telegram 进行配置（配对）
```bash
python3 ~/.openclaw/workspace/openclaw-watchdog/scripts/test-message.py "$TELEGRAM_TOKEN" "$TELEGRAM_CHAT_ID"
```
请等待用户确认已收到 Telegram 消息后再继续下一步。

### 4. 确认服务是否已启动
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

### 5. 通知用户
告知用户故障监控工具已启动、监控的内容，以及一旦出现问题会通过 Telegram 发送警报。

## 工作原理
- 每 15 秒向网关的健康检查端点发送一次检测请求（端点地址从配置文件中自动获取，或通过 `--gateway-port` 参数手动设置）
- 如果连续三次检测失败，系统会尝试重启网关
- 最多尝试两次重启后，系统会通过 Telegram 请求用户的重启许可
- 用户需要运行 `touch ~/.openclaw/watchdog/approve-reinstall` 命令来批准重启
- 未经用户批准，系统仅发送警报，不会执行任何破坏性操作
- 采用 AES-256 算法对用户凭据进行加密（使用设备特有的密钥）
- 该服务可在 macOS 的 LaunchAgent 或 Linux 的 systemd 中作为用户服务运行

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