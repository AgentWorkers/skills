# 废物回收提醒技能

这是一个灵活且高效利用令牌的技能，用于自动发送废物回收提醒。

## 概述

该技能可根据用户定义的日程安排自动发送废物回收提醒。它使用简单的JSON配置文件，以实现最大的灵活性和最小的令牌消耗。

**工作原理：**
该技能会读取用户的配置文件和日程安排，确定需要发送的提醒内容，并以AI助手能够处理的格式输出这些信息。随后，AI助手会将这些提醒消息发送到指定的渠道。

**输出格式：**
```
SEND_TO:recipient_id
CHANNEL:whatsapp
Your message here
---
```

这种设计使得配置简单且令牌使用效率更高——该技能无需API密钥或直接的网络访问权限。

## 主要功能

- 支持多种类型的废物容器
- 自定义提醒日程（每次回收最多可发送4条提醒）
- 灵活的目标设置（群组、个人或升级通知）
- 多渠道支持（WhatsApp、Telegram、Discord、电子邮件）
- 确认系统（避免重复发送提醒）
- 通过一个配置文件管理所有设置
- 高效利用令牌（无需额外生成AI令牌）

## 安装方法
```bash
clawhub install waste-reminder
```

## 用户设置

安装该技能后，AI助手会发送一个配置模板给用户。用户可以用任何语言回复，AI会自动将其转换为正确的格式！

### 示例模板（包含所有选项）

```
I want to set up waste reminders!

My containers:
- blue: Paper (🔵)
- gray: Residual (⚫)
- orange: Plastic (🟠)
- green: Garden (🟢)

Reminder times:
- 18:00: to group_whatsapp (day before, group notification)
- 22:00: to group_whatsapp (evening reminder to group)
- 06:30: to partner_whatsapp (morning, specific person)
- 09:30: to me_telegram (escalation, different channel)

My contacts:
- group_whatsapp: 123456789@g.us
- partner_whatsapp: +31600000001
- me_telegram: 222222222

Upcoming pickups:
- 2026-02-24: orange
- 2026-02-25: gray
- 2026-03-02: blue
```

AI会将该模板转换为正确的JSON格式并完成所有设置。

## 配置文件

配置文件存储路径：
`/data/.openclaw/workspace/data/waste-reminder/`

## 相关文件

```
waste-reminder/
├── config.json      # Your containers, reminder times, targets
└── schedule.json   # Your pickup dates and status
```

### 完整的config.json示例（包含所有选项）

```json
{
  "config_version": "1.0",
  "containers": {
    "blue": {"name": "Paper", "color": "blue", "emoji": "🔵"},
    "gray": {"name": "Residual", "color": "gray", "emoji": "⚫"},
    "orange": {"name": "Plastic", "color": "orange", "emoji": "🟠"},
    "green": {"name": "Garden", "color": "green", "emoji": "🟢"}
  },
  "reminder_times": {
    "18:00": {
      "type": "group",
      "template": "Tomorrow: {container_emoji} {container_name} will be collected!",
      "target": "group_whatsapp"
    },
    "22:00": {
      "type": "group",
      "template": "Not confirmed yet - {container_emoji} needs to go out by 7am!",
      "target": "group_whatsapp"
    },
    "06:30": {
      "type": "personal",
      "template": "⚠️ {container_emoji} put out NOW!",
      "target": "partner_whatsapp"
    },
    "09:30": {
      "type": "escalation",
      "template": "Container still not outside!",
      "target": "me_telegram"
    }
  },
  "targets": {
    "group_whatsapp": {"id": "123456789@g.us", "channel": "whatsapp"},
    "partner_whatsapp": {"id": "+31600000001", "channel": "whatsapp"},
    "partner_telegram": {"id": "111111111", "channel": "telegram"},
    "me_whatsapp": {"id": "+31600000002", "channel": "whatsapp"},
    "me_telegram": {"id": "222222222", "channel": "telegram"},
    "me_discord": {"id": "https://discord.com/api/webhooks/...", "channel": "discord"}
  }
}
```

### 完整的schedule.json示例

```json
{
  "2026-02-24": {
    "orange": {
      "confirmed": false,
      "reminded_18:00": false,
      "reminded_22:00": false,
      "reminded_06:30": false,
      "reminded_09:30": false
    }
  },
  "2026-02-25": {
    "gray": {
      "confirmed": false,
      "reminded_18:00": false,
      "reminded_22:00": false,
      "reminded_06:30": false,
      "reminded_09:30": false
    }
  }
}
```

## Cron作业设置

请添加一个每15分钟运行一次的Cron作业：
- 名称：`Waste Reminder Check`
- 时间安排：每15分钟执行一次
- 脚本路径：`/data/.openclaw/workspace/skills/waste-reminder/waste_cron.py`

该Cron脚本会检查是否有需要发送的提醒，并将结果输出。AI助手会根据Cron作业的触发来发送相应的消息。

## 用户命令

- 确认：`container is out`（表示容器已取出）
- 查看：`waste schedule` 或 `waste status`（查看废物回收日程）
- 添加：`waste add [date] [container]`（添加新的废物回收任务）
- 删除：`waste remove [date] [container]`（删除指定的废物回收任务）

## 相关文件

```
waste-reminder/
├── SKILL.md           # This file
├── waste_reminder.py # CLI tool (manual commands)
└── waste_cron.py      # Cron script (every 15 min)
```

## 模板占位符说明

- `{container_emoji}`：表示废物的emoji符号
- `{container_name}`：废物的名称
- `{date}`：回收任务的日期

## 支持的渠道

- `whatsapp`：使用电话号码或群组ID作为渠道标识
- `telegram`：使用聊天ID作为渠道标识
- `discord`：使用Webhook URL作为渠道标识
- `email`：使用电子邮件地址作为渠道标识

每个目标渠道都需要同时指定`id`和`channel`。

## 目标渠道命名规则

渠道名称的命名规则如下：
- `group_whatsapp`、`group_telegram`、`group_discord`：表示群组渠道
- `me_whatsapp`、`me_telegram`、`me_discord`：表示个人渠道
- `partner_whatsapp`、`partner_telegram`、`partner_discord`：表示合作伙伴渠道

渠道名称中的“group”或“me”会自动识别对应的类型。

## 许可证

本技能遵循MIT许可证。