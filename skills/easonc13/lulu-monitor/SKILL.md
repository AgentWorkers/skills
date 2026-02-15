---
name: lulu-monitor
description: AI驱动的LuLu防火墙辅助工具，专为macOS设计。该工具可监控防火墙警报，利用人工智能分析网络连接，并通过Telegram发送包含“允许/阻止”按钮的通知。适用于配置LuLu防火墙集成、处理防火墙回调事件或排查LuLu Monitor相关问题时使用。
---

# LuLu Monitor

这是一个专为 [LuLu Firewall](https://objective-see.org/products/lulu.html) 在 macOS 上设计的 AI 助手工具。

![LuLu Monitor 屏幕截图](screenshot.png)

## 功能概述

1. 监控 LuLu 防火墙的警报弹窗。
2. 提取连接信息（进程、IP 地址、端口、DNS）。
3. 通过 AI 分析这些连接。
4. 通过 Telegram 发送风险评估通知。
5. 提供四个操作按钮：始终允许、允许一次、始终阻止、阻止一次。
6. 用户点击按钮后，LuLu 防火墙会执行相应的操作。

## 自动执行模式（可选）

为了减少干扰，可以启用自动执行模式。当 AI 对连接的安全性有较高信心时（例如，`curl`、`brew`、`node`、`git` 等程序连接到正常目标时），它会：
1. 自动执行“允许”操作。
2. 仍然会发送 Telegram 通知，说明为何允许该连接。

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

**选项：**
- `autoExecute`: `false`（默认值）——所有警报都需要手动操作。
- `autoExecuteAction`: `"allow-once"`（默认值，较为谨慎）或 `"allow"`（永久性规则）。

## 安装

### 先决条件

首先运行检查脚本：
```bash
bash scripts/check-prerequisites.sh
```

**所需软件：**
- **LuLu Firewall**: `brew install --cask lulu`
- **Node.js**: `brew install node`
- **OpenClaw Gateway**: 已配置并正在运行，且已关联 Telegram 账号。
- **系统访问权限**：系统设置 > 隐私 > 访问能力 > 启用 Terminal/osascript。

### Gateway 配置（必需）

该工具通过 OpenClaw 的 `/tools/invoke` HTTP API 调用 `sessions_spawn` 功能。此功能默认被阻止，需要在 `~/.openclaw/openclaw.json` 文件中将其添加到允许列表中：
```json5
{
  "gateway": {
    "tools": {
      "allow": ["sessions_spawn"]
    }
  }
}
```

如果不进行此配置，虽然可以检测到警报，但无法将其转发（日志中会出现 404 错误）。

### 安装步骤

```bash
bash scripts/install.sh
```

安装过程包括：
1. 将代码仓库克隆到 `~/.openclaw/lulu-monitor/` 目录。
2. 安装 npm 依赖项。
3. 设置 launchd 服务以实现自动启动。
4. 启动该服务。

### 验证安装结果

安装完成后，应返回如下结果：
`{"running": true,...}`

## 处理回调

当用户点击 Telegram 上的按钮时，OpenClaw 会收到回调信息：
```
callback_data: lulu:allow
callback_data: lulu:allow-once
callback_data: lulu:block
callback_data: lulu:block-once
```

为了处理这些回调，需要调用相应的本地端点：
```bash
curl -X POST http://127.0.0.1:4441/callback \
  -H "Content-Type: application/json" \
  -d '{"action":"allow"}'  # or "block", "allow-once", "block-once"
```

该操作会：
1. 在 LuLu 防火墙的警报界面中点击相应的按钮。
2. 将规则的有效期设置为“始终”或“进程生命周期”。
3. 更新 Telegram 消息以显示处理结果。

## 故障排除

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

### 访问权限问题
AppleScript 需要系统权限才能控制 LuLu 防火墙。请前往：
系统设置 > 隐私与安全 > 访问能力
启用 Terminal、iTerm 或您使用的其他终端应用程序。

### 未检测到警报
- 确保 LuLu 防火墙正在运行：`pgrep -x LuLu`
- 检查警报窗口是否存在：`osascript -e 'tell application "System Events" to tell process "LuLu" to get every window'`

## 卸载

```bash
bash ~/.openclaw/lulu-monitor/skill/scripts/uninstall.sh
```