---
name: lulu-monitor
description: 一款基于人工智能的 LuLu 防火墙辅助工具，专为 macOS 设计。该工具能够监控防火墙警报，利用人工智能分析网络连接，并通过 Telegram 发送包含“允许”/“阻止”按钮的通知。适用于配置 LuLu 防火墙集成、处理防火墙回调事件或排查 LuLu Monitor 相关问题时使用。
---

# LuLu Monitor

这是一个为 [LuLu Firewall](https://objective-see.org/products/lulu.html) 在 macOS 上设计的智能辅助工具。

![LuLu Monitor 屏幕截图](screenshot.png)

## 功能概述

1. 监控 LuLu 防火墙的警报弹窗。
2. 提取连接信息（进程、IP 地址、端口号、DNS）。
3. 通过 AI 分析这些连接信息（以俳句的形式呈现）。
4. 通过 Telegram 发送风险评估通知。
5. 提供四个操作选项：始终允许、允许一次、始终阻止、阻止一次。
6. 用户点击按钮后，LuLu 防火墙会立即执行相应的操作。

## 自动执行模式（可选）

为了减少干扰，可以启用自动执行模式。当 AI 对连接的安全性有较高信心时（例如，`curl`、`brew`、`node`、`git` 等安全程序连接到正常目标时），系统会自动执行允许操作，并通过 Telegram 发送通知说明原因。

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
- `autoExecute`：`false`（默认值）——所有警报都需要用户手动点击按钮处理。
- `autoExecuteAction`：`"allow-once"`（默认值，较为保守）或 `"allow"`（永久性规则）。

## 安装流程

### 先决条件

请先运行检查脚本：
```bash
bash scripts/check-prerequisites.sh
```

**所需软件：**
- **LuLu Firewall**：`brew install --cask lulu`
- **Node.js**：`brew install node`
- **OpenClaw Gateway**：已配置并正在运行，且与 Telegram 频道关联。
- **系统访问权限**：进入“系统设置” > “隐私” > “辅助功能”，然后启用“终端/OSScript”功能。

### 安装步骤

```bash
bash scripts/install.sh
```

安装过程包括：
1. 将代码仓库克隆到 `~/.openclaw/lulu-monitor/` 目录。
2. 安装所需的 npm 依赖项。
3. 配置 `launchd` 服务以实现自动启动。
4. 启动该服务。

### 验证安装结果

执行以下命令后，应返回 `{"running": true,...}`：

```bash
curl http://127.0.0.1:4441/status
```

## 处理回调事件

当用户点击 Telegram 中的按钮时，OpenClaw 会收到回调信息。此时，需要调用本地端点来处理该事件：
```bash
curl -X POST http://127.0.0.1:4441/callback \
  -H "Content-Type: application/json" \
  -d '{"action":"allow"}'  # or "block", "allow-once", "block-once"
```

系统会执行以下操作：
1. 在 LuLu 防火墙的警报窗口中点击相应的按钮。
2. 将规则的有效范围设置为“endpoint”。
3. 将规则的有效时间设置为“始终有效”或“进程生命周期”。
4. 更新 Telegram 消息以显示处理结果。

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

### 系统访问权限问题
AppleScript 需要权限来控制 LuLu 防火墙。请进入“系统设置” > “隐私与安全” > “辅助功能”，并启用“终端”或您使用的其他终端应用程序。

### 无法检测到警报
- 确保 LuLu 防火墙正在运行：`pgrep -x LuLu`
- 检查警报窗口是否存在：`osascript -e 'tell application "System Events" to tell process "LuLu" to get every window'`

## 卸载方法

```bash
bash ~/.openclaw/lulu-monitor/skill/scripts/uninstall.sh
```