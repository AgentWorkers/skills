---
name: campaign-orchestrator
description: ShapeScale销售的多渠道跟进活动管理工具：该工具能够根据CRM系统中的数据安排并执行短信（SMS）和电子邮件（Email）发送序列，同时在收到回复时自动终止相关流程。适用于跟进潜在客户或管理外展营销活动。
homepage: https://github.com/kesslerio/shapescale-moltbot-skills
metadata: {"moltbot":{"emoji":"📋","requires":{"env":["DIALPAD_API_KEY","ATTIO_API_KEY","GOG_KEYRING_PASSWORD"]},"primaryEnv":"DIALPAD_API_KEY"}}
---

# Campaign Orchestrator 技能

这是一个用于 ShapeScale 销售的多渠道跟进活动编排工具。它能够通过 CRM 系统执行预定的短信（SMS）和电子邮件（Email）发送序列，并在收到回复时自动终止活动。

## 概述

**活动（Campaign）** 是一系列按时间顺序执行的步骤（短信/电子邮件）。当潜在客户（lead）回复任何消息时，该活动会自动终止。

### 主要特性

- **多渠道**：支持短信（Dialpad）和电子邮件（Gmail）发送
- **定时执行**：基于 Cron 表达式的定时任务，可配置延迟时间
- **个性化**：模板内容从 Attio CRM 系统中获取
- **自动终止**：收到回复后，所有后续的预定步骤都会停止
- **日志记录**：所有操作都会被记录在 Attio 系统中

## 设置

**所需的环境变量：**
```bash
DIALPAD_API_KEY=your_dialpad_api_key
ATTIO_API_KEY=your_attio_api_key
GOG_KEYRING_PASSWORD=your_google_password  # For Gmail access
```

**还需确保：**
- Dialpad 的 Webhook 被配置为能够触发服务器响应
- Attio 中已包含潜在客户的记录
- 已为销售邮件启用 Gmail API 访问权限

## 使用方法

### 启动活动

```bash
# Start primary follow-up campaign for a lead
python3 campaign.py start "primary" --lead "Apex Fitness"

# Start with custom delay override (hours)
python3 campaign.py start "primary" --lead "Apex Fitness" --delay 2

# Start with Attio deal/company ID
python3 campaign.py start "post-demo" --lead "Apex Fitness" --attio-id "deal-uuid"
```

### 活动启动前的检查（必填）

在启动任何活动之前，请务必进行以下检查：
1. **客户状态检查**：
   - 在数据库或 CRM 系统中查找“已经是客户”或“已购买”的标记
   - 确认潜在客户不在排除列表中
   - 验证潜在客户的电子邮件域名是否存在于客户数据库中
2. **电子邮件格式检查**（针对电子邮件步骤）：
   - 预览模板内容，确保其显示为正确的段落格式
   - 每段内容包含 2-4 句话，段落之间使用空行分隔
   - 避免出现单独的、没有上下文的句子
   - 段落内不要使用硬换行符
3. **语气检查**：
   - 语言要专业，避免使用道歉性或敷衍的语气（例如“没关系”、“抱歉打扰您”）
   - 语言要表明专业态度，而非表现出迫切的需求

**除非客户明确要求进行升级销售，否则切勿向现有客户发送活动。**

### 检查活动状态

```bash
# Status for specific lead
python3 campaign.py status "Apex Fitness"

# All active campaigns
python3 campaign.py list
```

### 停止活动

```bash
# Manual termination (lead replied, not interested, etc.)
python3 campaign.py stop "Apex Fitness" --reason "replied_interested"
```

### 删除潜在客户记录

```bash
# Remove lead from campaigns (opted out, not interested)
python3 campaign.py remove "Apex Fitness"
```

### 检查回复情况

```bash
# Check if lead has responded to any prior messages
python3 campaign.py check "Apex Fitness"
# Shows response status for each completed step
# Warns if responses detected (safe to proceed or terminate)
```

### 查看待执行的步骤

```bash
# Show all pending campaign steps sorted by time
python3 campaign.py pending
# Useful for seeing what's due soon across all campaigns
```

### 模板管理

```bash
# List available templates
python3 campaign.py templates

# Preview a template
python3 campaign.py preview "primary"
```

## 活动模板

| 模板名称 | 发送时间 | 发送渠道 | 发送目的 |
|----------|--------|---------|---------|
| `primary` | +4 小时 | SMS | 回顾演示内容、分享录像 |
| `secondary` | +1 天 | 电子邮件 | 提供价格信息、详细的投资回报分析 |
| `tertiary` | +4 天 | SMS | 迅速跟进 |
| `quaternary` | +7 天 | 电子邮件 | 最终跟进、分享案例研究 |
| `post-demo` | +0 小时 | SMS | 立即发送感谢信息 |

### 模板变量

模板支持变量替换：

```
{name}      - Lead first name
{company}   - Company name
{deal_value} - Deal value from Attio
{owner}     - Sales owner name
{demo_notes} - Notes from demo conversation
{checkout_link} - Personalized checkout URL
```

## 架构

```
campaign-orchestrator/
├── SKILL.md              # This file
├── campaign.py           # Main CLI (start, stop, status, list)
├── webhook_handler.py    # Processes reply → termination
├── primary.md            # SMS follow-up template
├── secondary.md          # Email template
├── post-demo.md          # Immediate follow-up template
└── state/
    └── campaigns.json    # Campaign state persistence
```

## 状态管理

活动状态存储在 `<workspace>/state/campaigns.json` 文件中：

```json
{
  "campaigns": {
    "Apex Fitness": {
      "template": "primary",
      "attio_id": "deal-uuid",
      "started": "2026-01-27T13:00:00Z",
      "steps_completed": ["sms_primary"],
      "next_step": "email_secondary",
      "next_scheduled": "2026-01-28T13:00:00Z",
      "status": "active"
    }
  },
  "templates": {
    "primary": {...},
    "secondary": {...}
  }
}
```

## Cron 任务集成

活动步骤通过 Clawdbot 的 Cron 任务系统来执行：
- **执行器任务**：每 5 分钟运行一次，检查是否有需要执行的步骤
- **每个活动的任务**：为每个预定的步骤创建单独的任务

调度脚本会自动创建和管理这些任务。

## Webhook 处理流程

当 Dialpad 收到对活动消息的回复时：
1. Dialpad 会向服务器发送 Webhook 请求
2. `webhook_handler.py` 脚本解析回复内容
3. 确定该回复属于哪个活动
4. 将该活动标记为已终止
5. 将回复信息记录到 Attio 系统中

## 集成点

### Dialpad SMS 发送
```bash
python3 /home/art/niemand/skills/dialpad/send_sms.py --to "+14155551234" --message "..."
```

### Gmail（通过 gog）
```bash
gog-shapescale --account martin@shapescale.com send-email --to "lead@company.com" --subject "..." --body "..."
```

### Attio CRM
```bash
attio note companies "company-uuid" "Campaign message sent: {message}"
```

## 示例

### 完整的活动工作流程

```bash
# 1. After demo, start campaign
/campaign start "post-demo" --lead "Dr. Smith's Clinic"

# 2. Check status next day
/campaign status "Dr. Smith's Clinic"
# Output: Step 1 sent, Step 2 scheduled for tomorrow

# 3. Lead replies "interested"
# Webhook automatically terminates campaign
# Logs reply to Attio

# 4. Manual follow-up if needed
/campaign start "secondary" --lead "Dr. Smith's Clinic" --delay 0
```

### 监控正在进行的活动

```bash
# List all active
/campaign list

# Output:
# Active Campaigns:
# - Apex Fitness (primary) - Step 2/4, next: email
# - Dr. Smith's Clinic (post-demo) - Complete
# - Wellness Center (tertiary) - Step 1/3, next: sms
```

## 故障排除

**活动未发送：**
- 检查 Cron 任务是否正在运行：`crontab -l`
- 查看日志：`journalctl -u moltbot` 或活动日志
- 验证 API 密钥是否正确：`echo $DIALPAD_API_KEY`

**Webhook 未触发终止：**
- 确认 Dialpad 的 Webhook URL 是否配置正确
- 检查 Webhook 处理脚本是否正在运行
- 查看 `campaigns.json` 文件中是否存在对应的潜在客户记录

**模板变量未填充：**
- 确认潜在客户在 Attio 系统中存在，并且具有所需的字段
- 检查模板语法是否正确（例如使用 `{variable}` 而不是 `{ variable }`）

## 许可证

本功能属于 shapescale-moltbot-skills 的一部分。详细信息请参阅父仓库。