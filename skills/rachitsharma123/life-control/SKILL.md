---
name: life-control
description: "协调 OpenClaw 代理集群的 Life Control CLI 技能：初始化 Life Control 数据库、注册代理角色、连接 Telegram 机器人，并执行日常任务（如早晨整理、身体状态监测、财务状况分析、社交动态监控、工作准备以及系统关闭）。当用户需要创建或运行 Life Control 系统、集成 OpenClaw 技能，或实现个人生活管理的自动化时，请使用该功能。"
---

# 生活管理（Life Control）

## 概述
设置并运行 Life Control 命令行界面（CLI），以便 OpenClaw 能够通过日常任务和 Telegram 通知来管理用户的多个生活领域（健康、财务、时尚、职业、人际关系以及精神成长）。

## 快速入门（OpenClaw）
1. 确保仓库根目录可访问。
2. 导出 Telegram 聊天 ID 和代理机器人令牌。
3. 运行 `skills/life-control/scripts/bootstrap.sh`。
4. 使用 `lc dashboard`、`lc list` 和日常任务脚本来协调各项任务。

如需了解角色映射或 OpenClaw 的特定说明，请查阅 `references/openclaw.md`。

## 核心工作流程

### 1) 初始化代理角色
- 运行 `skills/life-control/scripts/bootstrap.sh`。
- 使用 `lc fleet` 验证代理角色的状态。

### 2) 添加目标与记录
- 使用 `lc add` 和 `lc log` 进行结构化跟踪。
- 使用 `qlog` 快速查看各项指标（蛋白质摄入、水分摄入、锻炼情况、开支、冥想时间等）。

### 3) 运行日常任务
- 日常任务脚本位于 `routines/` 目录下（例如：晨间调整、身体护理、财务检查、社交动态监测、工作准备、睡前放松）。
- 将相关任务添加到 `crontab-template.txt` 中以实现自动调度。

### 4) Telegram 通知
- 使用 `lc notify` 为每个代理角色排队发送通知消息。
- 通过 cron 任务运行 `telegram-sender.sh` 将通知发送给相应的机器人。

## 资源文件

### scripts/
- `bootstrap.sh`：初始化数据库并调用 `setup-agents.sh` 注册代理角色。

### references/
- `openclaw.md`：角色映射信息及 OpenClaw 集成说明。