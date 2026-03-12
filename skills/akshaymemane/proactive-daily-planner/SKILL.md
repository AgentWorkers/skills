---
name: proactive-daily-planner
description: "这是一个主动的日常规划助手，它能帮助你整理一天的工作安排、跟踪任务进度，并提供动力支持。它就像你的个人助理一样，主动为你规划每一天的事情。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📅",
        "author": "Akshay Memane",
        "version": "1.0.0",
        "category": "productivity",
        "tags": ["planning", "productivity", "proactive", "assistant", "daily"],
      },
  }
---
# 日常计划助手技能

这是一个主动型的个人助手，可帮助您规划每一天、跟踪任务并保持动力。

## 🎯 功能介绍

- **晨间规划**：帮助您设定每日目标并安排任务优先级
- **进度跟踪**：全天监控任务完成情况
- **激励系统**：提供鼓励和提醒
- **晚间回顾**：帮助您总结当天的成就并为明天做准备
- **主动提醒**：预测您的需求并自动开始规划

## 🚀 快速入门

### 安装

```bash
# Clone or copy the skill to your OpenClaw skills directory
cp -r daily-planner ~/.openclaw/workspace/skills/
```

### 配置

编辑 `config.json` 文件以自定义以下内容：
- 您的名字和时区
- 规划时间（早晨/下午/晚上）
- 任务类别和优先级
- 激励信息

### 使用方法

该技能会根据您的时间表自动运行，您也可以手动触发它：

```bash
# Manual trigger
openclaw skill daily-planner plan morning
openclaw skill daily-planner check-progress
openclaw skill daily-planner evening-review
```

## ⚙️ 配置文件（config.json）

```json
{
  "user": {
    "name": "Akshay",
    "timezone": "Asia/Kolkata",
    "workHours": "9:00-18:00"
  },
  "schedule": {
    "morningCheckin": "8:00",
    "afternoonCheckin": "13:00",
    "eveningReview": "20:00"
  },
  "tasks": {
    "categories": ["work", "learning", "fitness", "personal"],
    "defaultPriority": "medium"
  },
  "notifications": {
    "enabled": true,
    "channel": "telegram",
    "motivationFrequency": "2h"
  }
}
```

## 📋 功能详情

### 1. 晨间规划
- 设定每日目标和优先级
- 查看日历事件
- 生成当天的任务列表
- 提供励志语录

### 2. 进度跟踪
- 跟踪任务完成情况
- 提供进度更新
- 如果进度落后，会建议进行调整
- 为达成里程碑而庆祝

### 3. 激励系统
- 提供 50 多条励志信息
- 根据进度提供鼓励
- 为重要任务设置提醒系统
- 实施正向强化

### 4. 晚间回顾
- 总结当天的成就
- 分析哪些方面做得好
- 为明天制定计划
- 为当天画上圆满的句号

## 🔧 集成

### 与 OpenClaw 主动助手集成
- 根据时间表自动运行
- 通过配置的渠道发送通知
- 将规划数据存储在内存文件中
- 与其他技能（日历、电子邮件等）协同工作

### 与外部服务集成
- **日历**：查看已安排的事件（未来功能）
- **电子邮件**：查看重要邮件（未来功能）
- **任务管理器**：与 Todoist/Things 等工具同步（未来功能）

## 📊 数据存储

规划数据存储在以下位置：
- `~/.openclaw/workspace/memory/daily-plan-YYYY-MM-DD.md` - 每日计划
- `~/.openclaw/workspace/memory/task-history.json` - 任务完成历史记录
- `~/.openclaw/workspace/memory/progress-stats.json` - 进度统计信息

## 🎨 自定义

### 模板
编辑 `templates/` 目录下的模板文件以进行自定义：
- `morning.md` - 晨间规划模板
- `afternoon.md` - 下午检查模板
- `evening.md` - 晚间回顾模板

### 激励信息
将您自己的励志信息添加到 `config.json` 文件中：
```json
"motivationMessages": [
  "You've got this! 💪",
  "One task at a time, you're making progress! 🚀",
  "Remember why you started. Keep going! 🌟"
]
```

## 🤝 贡献方式

1. 克隆仓库
2. 创建一个功能分支
3. 进行修改
4. 彻底测试
5. 提交 pull 请求

## 📝 许可证

MIT 许可证 - 详情请参阅 LICENSE 文件。

## 🙏 致谢

- 本技能专为 OpenClaw AI 助手开发
- 受到主动型助手模式的启发
- 旨在提升个人生产力

---

**祝您规划顺利！**愿您的每一天都充满成效和满足感。📅✨