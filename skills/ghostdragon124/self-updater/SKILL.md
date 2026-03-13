---
name: self-updater
version: 1.4.2
description: >
  ⭐ 开源项目！GitHub地址：github.com/GhostDragon124/openclaw-self-updater  
  ⭐ 这是唯一一个支持Cron任务调度和空闲时间检测功能的工具！它可以自动更新OpenClaw的核心组件及各个功能模块，分析用户的Cron任务安排，避免与用户的日常任务冲突；在系统处于空闲状态时执行更新；通过人工智能进行风险评估；高风险更新需要用户批准；同时提供智能通知功能。  
  适用场景：自动更新、系统维护、Cron任务管理、智能调度、技能管理、系统重启、健康检查、监控以及运维操作。
repository:
  type: git
  url: https://github.com/GhostDragon124/openclaw-self-updater
homepage: https://github.com/GhostDragon124/openclaw-self-updater#readme
required_binaries:
  - pwsh (PowerShell 5.1+)
  - npm
  - clawhub
optional_envs:
  - TELEGRAM_BOT_TOKEN
  - FEISHU_APP_ID
  - FEISHU_APP_SECRET
---
# 自动更新工具

⭐ **唯一支持Cron任务调度和系统空闲检测的OpenClaw更新工具！**

这是一个智能的自动更新工具，能够在不影响您已安排的任务的情况下检查并下载更新。

## 为什么选择这个工具？

| 功能 | 其他更新工具 | 本工具 |
|---------|---------------|------------|
| 支持Cron任务调度 | ❌ | ✅ 避免干扰您的定时任务 |
| 系统空闲检测 | ❌ | ✅ 等待系统处于空闲状态后再进行更新 |
| 人工智能风险评估 | ❌ | ✅ 评估更新带来的风险 |
| 用户确认 | ❌ | ✅ 对高风险更新需要用户确认 |
| 智能通知 | ⚠️ 基础功能 | ✅ 通知方式灵活（包括Telegram和Feishu） |

## 主要功能

- **🔒 支持Cron任务调度**：读取`~/.openclaw/cron/jobs.json`文件，确保不会干扰您的定时任务。
- **⏳ 系统空闲检测**：在系统空闲时才进行更新，避免中断操作。
- **🧠 人工智能风险评估**：在更新前评估风险等级（低/中/高）。
- **✅ 用户确认**：对于高风险更新，会暂停更新并请求用户确认。
- **📲 智能通知**：自动检测用户是否在Telegram或Feishu上，并发送简洁的更新通知。
- **🔄 双重更新**：同时更新OpenClaw核心组件和已安装的扩展技能。
- **🛡️ 自动重启**：更新完成后自动重启服务。
- **🌐 自动检测端口**：从配置文件中自动读取网关端口。

## 快速开始

```powershell
# Check for updates
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1

# Auto-update with smart timing
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1 -AutoUpdate -SmartTiming

# Full automation (for cron)
powershell -ExecutionPolicy Bypass -File scripts/self-updater.ps1 -AutoUpdate -SmartTiming -AutoApprove -Quiet
```

## 人工智能风险评估

通过以下5个因素来计算风险等级：

| 因素 | 权重 | 说明 |
|--------|--------|-------------|
| 版本更新的影响 | 30% | 包括重大更新、次要更新和补丁更新 |
| 需要更新的扩展技能数量 | 25% | 需要更新的扩展技能数量 |
| 重启服务的影响 | 20% | 重启服务可能带来的影响 |
| 自上次更新以来的时间 | 15% | 自上次更新以来的时间（以小时计） |
| 与下一个Cron任务的距离 | 10% | 与下一个Cron任务的间隔时间 |

**风险等级**：
- 🟢 **低**（风险评分<50）：自动更新
- 🟡 **中**（风险评分50-74）：显示警告但自动更新
- 🔴 **高**（风险评分≥75）：需要用户确认

## 用户确认流程

当风险等级为**高**时：
1. 显示包含风险评估详情的警告信息。
2. 等待用户确认（超时60秒）。
3. 如果用户确认 → 继续更新。
4. 如果用户拒绝或跳过更新 → 优雅地取消更新。

使用`-AutoApprove`参数可设置为无人值守模式。

## 智能通知

**更新前**：
```
🔄 OpenClaw Update Check
• Core: 1.2.3 → 1.3.0 (Minor)
• Skills: 3 to update
• Risk: 🟡 Medium
```

**更新后**：
```
✅ OpenClaw Updated
• Core: v1.3.0
• Skills: 3 updated
• Gateway: ✅ OK
```

自动通过Telegram或Feishu发送通知。

## 使用场景

- ✅ 实现每周自动维护
- ✅ 确保OpenClaw始终保持最新状态
- ✅ 避免干扰已安排的爬虫任务
- ✅ 在更新时及时收到通知
- ✅ 具有风险控制的自动更新机制

## 参数设置

| 参数 | 默认值 | 说明 |
|-----------|---------|-------------|
| AutoUpdate | false | 自动应用更新 |
| SmartTiming | false | 等待系统空闲并检查Cron任务 |
| AutoApprove | false | 对于Cron任务调度，跳过用户确认 |
| NoNotify | false | 禁用通知 |
| UpdateSkillsOnly | false | 仅更新扩展技能 |
| Port | auto | 自动读取网关端口 |
| IdleThreshold | 5 | 系统空闲等待时间（分钟） |
| CronLookAhead | 60 | 查看下一个Cron任务的间隔时间（分钟） |
| MaxWait | 30 | 最大等待时间（分钟） |

## 系统要求

- PowerShell 5.1及以上版本（pwsh）
- npm及clawhub CLI工具
- Windows系统（支持系统空闲检测）
- 需要读取以下配置文件：`~/.openclaw/openclaw.json`（仅获取网关端口信息）和`~/.openclaw/cron/jobs.json`

### 可选的环境变量

| 变量 | 说明 |
|----------|-------------|
| TELEGRAM_BOT_TOKEN | 用于发送通知的Telegram机器人token |
| FEISHU_APP_ID | 用于发送通知的Feishu应用ID |
| FEISHU_APP_SECRET | 用于发送通知的Feishu应用密钥 |

> **注意：** 本工具仅从配置文件中读取网关端口信息，不会对外传输任何敏感数据。

## 标签

auto-update, maintenance, cron, smart-schedule, skills, gateway, restart, healthcheck, monitoring, ops, openclaw, updater, self-maintenance, ai-assessment, user-approval, notification