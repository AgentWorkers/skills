---
name: outreach-sequencer
description: 创建并管理多步骤的外展序列——包括 LinkedIn 消息、冷邮件以及带有个性化内容的跟进邮件。当需要执行以下操作时，请使用此功能：发送外展邮件、创建邮件序列、跟进潜在客户、启动邮件营销活动、发送 LinkedIn 消息或执行任何自动化的多步骤沟通流程。
metadata: { "openclaw": { "emoji": "📨" } }
---
# 外展序列器 — 多步骤个性化营销活动

设计、安排并执行跨 LinkedIn 和电子邮件的多步骤外展序列。每条消息都会根据 DuckDB 中的潜在客户资料进行个性化定制。

## 序列模板

### 模板 1：LinkedIn 加入好友 + 消息
```
Day 0: Send LinkedIn connection request (with note)
Day 1: If accepted → Send intro message
Day 3: If no reply → Follow-up message
Day 7: If no reply → Break-up / value-add message
```

### 模板 2：冷邮件序列
```
Day 0: Initial cold email
Day 3: Follow-up (reply to original thread)
Day 7: Value-add email (case study, resource)
Day 14: Break-up email ("closing the loop")
```

### 多渠道营销
```
Day 0: LinkedIn connection request
Day 2: Cold email (if not connected on LinkedIn)
Day 4: LinkedIn message (if connected) OR email follow-up
Day 7: Final touch (whichever channel they engaged on)
```

## 个性化引擎

每条消息都是根据潜在客户的 DuckDB 资料生成的。使用以下变量：

| 变量 | 来源 | 示例 |
|----------|--------|---------|
| `{first_name}` | 名字字段 | "Jane" |
| `{company}` | 公司名称 | "Acme Corp" |
| `{title}` | 职位 | "首席技术官 (CTO)" |
| `{mutual}` | 共享的联系人/背景信息 | "斯坦福大学" |
| `{trigger}` | 现在联系的原因 | "看到了您的 A 轮融资信息" |
| `{value_prop}` | 您提供的价值 | "基于人工智能的分析服务" |
| `{pain_point}` | 潜在客户可能面临的挑战 | "工程团队的扩展问题" |

### 个性化规则
- **切勿使用通用的开场白**，例如“希望您一切安好”
- **提及具体内容**：最近的帖子、公司新闻或共同的背景信息
- **LinkedIn 消息长度控制在 300 字以内**（符合 LinkedIn 的限制）
- **冷邮件长度控制在 150 字以内**（以尊重接收者的注意力）
- **针对不同级别的潜在客户调整语言风格**：高层管理人员接收的消息应简洁且具有战略性，内部员工接收的消息则可更技术化或平级交流
- **根据职位调整语气**：高层管理人员需要简洁明了的信息，内部员工则需要更详细的技术性内容

### 消息生成模式
```
1. Read lead profile from DuckDB
2. Identify personalization hooks:
   - Shared background (school, company, location)
   - Recent company news (web search if needed)
   - Role-specific pain points
3. Select message template for sequence step
4. Generate personalized message
5. Store message + status in DuckDB
```

## 执行方式

### LinkedIn 消息（通过浏览器发送）
```
browser → open LinkedIn messaging
browser → search for recipient
browser → open conversation
browser → type personalized message
browser → send
→ Update DuckDB status: "Sent"
```

### 电子邮件（通过 gog CLI 发送）
```bash
gog gmail send \
  --to "{email}" \
  --subject "{subject}" \
  --body "{personalized_body}" \
  --account patrick@candlefish.ai
```

### 回复处理（针对邮件对话）
```bash
gog gmail reply \
  --thread-id "{thread_id}" \
  --body "{follow_up_body}"
```

## 序列状态跟踪

使用以下字段在 DuckDB 中跟踪序列状态：

| 字段 | 值 | 备注 |
|-------|--------|-------|
| 外展状态 | 待处理、已发送、已回复、转化、被拒收、已退订 | 主要状态 |
| 序列步骤 | 1、2、3、4 | 当前所处的步骤 |
| 最后一次外展 | 日期 | 最后一条消息的发送时间 |
| 下一步外展 | 日期 | 下一步的预定时间 |
| 外展渠道 | LinkedIn、电子邮件、两者皆可 | 当前使用的渠道 |
| 是否收到回复 | 布尔值 | 如果收到回复则显示为“已收到回复” |
| 邮件对话 ID | 文本 | 电子邮件对话的 ID |

```sql
-- Find leads due for next sequence step
SELECT "Name", "Email", "Outreach Status", "Sequence Step", "Next Outreach"
FROM v_leads
WHERE "Outreach Status" = 'Sent'
  AND "Reply Received" = false
  AND "Next Outreach" <= CURRENT_DATE
ORDER BY "Next Outreach";
```

## Cron 任务集成

设置自动化序列执行：

```
Schedule: Every 2 hours during business hours (9am-5pm Mon-Fri)
Action:
1. Query leads due for next step
2. For each due lead:
   a. Generate personalized message for their current step
   b. Send via appropriate channel
   c. Update status + advance step
   d. Set next outreach date
3. Report: "Sent 12 messages (8 LinkedIn, 4 email). 3 replies received."
```

### OpenClaw 的 Cron 任务配置
```json
{
  "name": "Outreach Sequencer",
  "schedule": { "kind": "cron", "expr": "0 9,11,13,15 * * 1-5", "tz": "America/Denver" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run outreach sequence check. Query DuckDB for leads with Next Outreach <= today. Send personalized messages for their current sequence step. Update statuses. Report results.",
    "timeoutSeconds": 300
  }
}
```

## 安全性与合规性

- **每日发送限制**：LinkedIn 加入好友请求每天最多 50 次，电子邮件每天最多 100 封
- **电子邮件发送限制**：每天最多发送 100 封冷邮件（避免被标记为垃圾邮件）
- **退订处理**：如果收到“不感兴趣”或“取消订阅”的回复，立即将状态设置为“已退订”，并不再联系该客户
- **邮件被拒收处理**：如果邮件被拒收，标记为“被拒收”，并尝试使用其他邮件地址
- **CAN-SPAM 合规性**：在邮件中包含发件人身份、物理地址选项和退订机制
- **LinkedIn 使用条款**：保持联系信息的专业性，避免发送垃圾邮件
- **冷却期**：如果潜在客户在整个序列结束后仍未回复，等待 90 天后再尝试联系

## 分析

每次序列执行后，记录以下数据：
```
Active Sequences: 85 leads
├── Step 1 (Initial): 20 leads
├── Step 2 (Follow-up): 35 leads
├── Step 3 (Value-add): 18 leads
├── Step 4 (Break-up): 12 leads
│
Outcomes:
├── Replied: 23 (27% reply rate)
├── Converted: 8 (9.4% conversion)
├── Opted Out: 3 (3.5%)
├── Bounced: 2 (2.4%)
└── No Response (completed): 15 (17.6%)
```