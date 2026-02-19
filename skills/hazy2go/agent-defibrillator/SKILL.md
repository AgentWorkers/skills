---
name: agent-defibrillator
description: 这是一个监控您的AI代理网关的守护进程，当代理崩溃时会自动重启它。该守护进程会在以下事件发生时被触发：安装除颤器（install defibrillator）、代理守护进程启动（agent watchdog）、网关监控（gateway monitor）、自动重启代理（auto-restart agent）或保持代理运行状态（keep agent alive）。它是一个macOS的launchd服务，并支持可选的Discord通知功能。
---
# 代理除颤器（Agent Defibrillator）

这是一个监控您的 AI 代理网关并在其崩溃时自动重启的守护服务。

## 功能说明：

- 每 10 分钟检查一次网关的运行状态
- 检测网关是否崩溃或存在异常运行的进程
- 自动重启网关，并设置重启间隔时间（防频繁重启）
- 可选：在重启时通过 Discord 发送通知
- 检测更新后是否存在版本不匹配的问题

## 安装

**推荐方式（请先查看代码）：**
```bash
git clone https://github.com/hazy2go/agent-defibrillator.git
cd agent-defibrillator
./install.sh
```

## 验证安装结果

```bash
launchctl list | grep defib
```

## 配置

编辑文件 `~/.openclaw/scripts/defibrillator.sh`：

| 变量          | 默认值         | 说明                          |
|-----------------|--------------|-------------------------------------------|
| `DEFIB_GATEWAY_LABEL` | `ai.openclaw.gateway` | launchd 服务的名称标签                 |
| `DEFIB_RETRY_DELAY` | `10`         | 重试间隔时间（秒）                     |
| `DEFIB_MAX_RETRIES` | `3`         | 最大重试次数                     |
| `DEFIB_COOLDOWN` | `300`         | 两次重启之间的间隔时间（秒）                 |
| `DISCORD_CHANNEL` | （空）         | 用于接收通知的 Discord 频道 ID                 |

## 命令操作

```bash
# View logs
tail -f ~/.openclaw/logs/defibrillator.log

# Manual check
~/.openclaw/scripts/defibrillator.sh

# Stop watchdog
launchctl bootout gui/$(id -u)/com.openclaw.defibrillator

# Restart watchdog
launchctl kickstart -k gui/$(id -u)/com.openclaw.defibrillator
```

## 卸载

```bash
launchctl bootout gui/$(id -u)/com.openclaw.defibrillator
rm ~/Library/LaunchAgents/com.openclaw.defibrillator.plist
rm ~/.openclaw/scripts/defibrillator.sh
```

## 系统要求：

- macOS 系统（使用 launchd 服务进行管理）
- 通过 launchd 运行的 AI 代理程序（如 OpenClaw 等）