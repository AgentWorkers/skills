---
name: lulu-monitor
description: 这是一款基于人工智能技术的 LuLu 防火墙辅助工具，专为 macOS 设计。它能够监控防火墙警报，利用人工智能技术分析网络连接，并通过 Telegram 发送包含“允许”/“阻止”按钮的通知。您可以在配置 LuLu 防火墙集成、处理防火墙回调或排查 LuLu Monitor 相关问题时使用该工具。
---
# LuLu Monitor

这是一个专为 [LuLu Firewall](https://objective-see.org/products/lulu.html) 在 macOS 上设计的智能辅助工具。

![LuLu Monitor 屏幕截图](screenshot.png)

## 功能概述

1. 监控 LuLu 防火墙的警报弹窗。
2. 提取连接信息（进程、IP、端口、DNS）。
3. 通过 AI 分析这些连接。
4. 通过 Telegram 发送风险评估通知。
5. 提供四个操作选项：始终允许、允许一次、始终阻止、阻止一次。
6. 用户点击按钮后，LuLu 防火墙会执行相应的操作。

## 自动执行模式（可选）

为了减少干扰，可以启用自动执行模式。当 AI 对连接的判断结果为“安全”（例如：curl、brew、node、git 等程序连接到正常目标）时，系统会：
1. 自动执行“允许”操作。
2. 仍然会通过 Telegram 发送通知，说明为何允许该连接。

**启用方法：**
```bash
# Create config.json in install directory
cat > ~/.openclaw/lulu-monitor/config.json << 'EOF'
{
  "telegramId": "YOUR_TELEGRAM_ID",
  "autoExecute": true,
  "autoExecuteAction": "allow-once"
}
EOF
```

**配置选项：**
- `autoExecute`：`false`（默认值）——所有警报都需要手动操作。
- `autoExecuteAction`：`"allow-once"`（默认值，较为保守）或 `"allow"`（永久性规则）。

## 安装

### 先决条件

请先运行检查脚本：
```bash
bash scripts/check-prerequisites.sh
```

**所需软件：**
- **LuLu Firewall**：`brew install --cask lulu`
- **Node.js**：`brew install node`
- **OpenClaw Gateway**：已配置并正在运行，且与 Telegram 频道关联。
- **系统权限**：进入“系统设置” > “隐私” > “辅助功能”，然后启用“终端/OSScript”。

### Gateway 配置（必需）

该工具通过 OpenClaw 的 `/tools/invoke` HTTP API 调用 `sessions_spawn` 功能。此功能默认被阻止，请在 `~/.openclaw/openclaw.json` 文件中将其添加到允许列表中：
```json5
{
  "gateway": {
    "tools": {
      "allow": ["sessions_spawn"]
    }
  }
}
```

如果不进行此配置，虽然可以检测到警报，但无法将其转发（日志中会显示 404 错误）。

### 安装步骤

```bash
bash scripts/install.sh
```

安装过程包括：
1. 将代码仓库克隆到 `~/.openclaw/lulu-monitor/`。
2. 安装所需的 npm 依赖项。
3. 设置 launchd 服务以实现自动启动。
4. 启动该服务。

### 验证安装结果

执行以下命令，应返回 `{"running": true,...}`：
```bash
curl http://127.0.0.1:4441/status
```

## 使用内联按钮发送警报

**注意：** `message` 工具的 `buttons`/`components` 参数不适用于 Telegram 的内联按钮。必须通过 CLI 来发送警报：
```bash
openclaw message send --channel telegram --target <chat_id> \
  --message "🔔 LuLu Alert: <summary>" \
  --buttons '[[{"text":"✅ Always Allow","callback_data":"lulu:allow"},{"text":"✅ Allow Once","callback_data":"lulu:allow-once"}],[{"text":"❌ Always Block","callback_data":"lulu:block"},{"text":"❌ Block Once","callback_data":"lulu:block-once"}]]'
```

通过 CLI 发送警报后，请使用 `NO_REPLY` 命令回复，以避免重复通知。

## 处理回调事件

当用户点击 Telegram 中的按钮时，OpenClaw 会收到回调信息：
```
callback_data: lulu:allow
callback_data: lulu:allow-once
callback_data: lulu:block
callback_data: lulu:block-once
```

要处理这些回调，需要调用相应的本地端点：
```bash
curl -X POST http://127.0.0.1:4441/callback \
  -H "Content-Type: application/json" \
  -d '{"action":"allow"}'  # or "block", "allow-once", "block-once"
```

该操作会：
1. 在 LuLu 防火墙的警报窗口中点击相应的按钮。
2. 将规则的有效时间设置为“始终”或“进程生命周期”。
3. 更新 Telegram 消息以显示处理结果。

## 常见问题及解决方法

### 服务未运行
```bash
# Check status
launchctl list | grep lulu-monitor

# View logs
tail -f ~/.openclaw/lulu-monitor/logs/stdout.log

# Restart
launchctl unload ~/Library/LaunchAgents/com.openclaw.lulu-monitor.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.lulu-monitor.plist
```

### 系统权限问题
AppleScript 需要权限才能控制 LuLu 防火墙。请进入“系统设置” > “隐私与安全” > “辅助功能”，并启用“终端”或您使用的其他终端应用程序。

### 无法检测到警报
- 确保 LuLu 防火墙正在运行：`pgrep -x LuLu`
- 检查警报窗口是否存在：`osascript -e 'tell application "System Events" to tell process "LuLu" to get every window'`

## 卸载程序
```bash
bash ~/.openclaw/lulu-monitor/skill/scripts/uninstall.sh
```