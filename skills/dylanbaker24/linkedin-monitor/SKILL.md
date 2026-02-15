---
name: linkedin-monitor
description: **具备渐进式自主功能的LinkedIn收件箱监控工具**：  
该工具每小时自动检查新消息，可为您用语音录制回复内容，并在有新对话时及时提醒您。支持四种自主程度设置，从仅监控到完全自主操作均可选择。
version: 1.0.0
author: Dylan Baker / lilAgents
---

# LinkedIn Monitor

专为Clawdbot设计的可靠LinkedIn收件箱监控工具。

## 主要功能

- **每小时监控**：全天候每小时检查一次收件箱
- **避免重复通知**：确保用户不会收到重复的通知
- **逐步提升自主性**：从受监督模式开始，逐步过渡到完全自主模式
- **健康检查**：在认证过期或系统出现故障时发出警报
- **个性化回复**：根据用户的沟通风格草拟回复内容

## 快速入门

```bash
# 1. Setup (interactive)
linkedin-monitor setup

# 2. Verify health
linkedin-monitor health

# 3. Run manually (test)
linkedin-monitor check

# 4. Enable cron (hourly)
linkedin-monitor enable
```

## 自主性等级

| 等级 | 名称 | 行为 |
|-------|------|----------|
| 0   | 仅监控 | 仅在新消息到达时发出警报 |
| 1   | 草拟回复 + 审批 | 草拟回复内容，等待用户审批 |
| 2   | 自动回复简单信息 | 自动处理简单的回复和日程安排 |
| 3   | 完全自主 | 以用户的方式回复消息、预约会议、拓展人脉 |

**默认等级：1级** — 可通过 `linkedin-monitor config autonomyLevel 2` 进行更改

## 命令

```bash
linkedin-monitor setup      # Interactive setup wizard
linkedin-monitor health     # Check auth status
linkedin-monitor check      # Run one check cycle
linkedin-monitor enable     # Enable hourly cron
linkedin-monitor disable    # Disable cron
linkedin-monitor status     # Show current state
linkedin-monitor config     # View/edit configuration
linkedin-monitor logs       # View recent activity
linkedin-monitor reset      # Clear state (start fresh)
```

## 配置文件位置

`~/.clawdbot/linkedin-monitor/config.json`

```json
{
  "autonomyLevel": 1,
  "alertChannel": "discord",
  "alertChannelId": "YOUR_CHANNEL_ID",
  "calendarLink": "cal.com/yourname",
  "communicationStyleFile": "USER.md",
  "timezone": "America/New_York",
  "schedule": "0 * * * *",
  "morningDigest": {
    "enabled": true,
    "hour": 9,
    "timezone": "Asia/Bangkok"
  },
  "safetyLimits": {
    "maxMessagesPerDay": 50,
    "escalationKeywords": ["angry", "legal", "refund"],
    "dailyDigest": true
  }
}
```

## 工作原理

### 监控流程

```
1. Health Check
   └── Verify LinkedIn auth (lk CLI)
   
2. Fetch Messages
   └── lk message list --json
   
3. Compare State
   └── Filter: only messages not in state file
   
4. For Each New Message
   ├── Level 0: Alert only
   ├── Level 1: Draft reply → Alert → Wait for approval
   ├── Level 2: Simple = auto-reply, Complex = draft
   └── Level 3: Full autonomous response
   
5. Update State
   └── Record message IDs (prevents duplicates)
```

### 状态管理

状态管理由脚本负责，而非大型语言模型（LLM）。这确保了：
- 不会出现重复通知
- 不同会话间的行为保持一致
- 可以通过状态文件方便地进行调试

状态文件位置：`~/.clawdbot/linkedin-monitor/state/`

## 发送已审批的回复

当处于等级1时，可以使用以下命令来审批草拟的回复：

```
send [name]           # Send draft to [name]
send all              # Send all pending drafts
edit [name] [text]    # Edit draft before sending
skip [name]           # Discard draft
```

## 故障排除

### “认证过期”
```bash
lk auth login
linkedin-monitor health
```

### “未找到消息”
```bash
linkedin-monitor check --debug
```

### 重复通知
```bash
linkedin-monitor reset  # Clear state
linkedin-monitor check  # Fresh start
```

## 所需依赖库

- `lk` CLI（LinkedIn命令行工具）：`npm install -g lk`
- `jq`（JSON处理工具）：`brew install jq`

## 相关文件

```
~/.clawdbot/linkedin-monitor/
├── config.json          # Your configuration
├── state/
│   ├── messages.json    # Seen message IDs
│   ├── lastrun.txt      # Last check timestamp
│   └── drafts.json      # Pending drafts
└── logs/
    └── activity.log     # Activity history
```