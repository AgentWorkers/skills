---
name: causal-inference
description: 为代理（agent）的操作添加因果推理功能。当任何具有可观察结果的高级操作发生时（例如：发送电子邮件、消息、修改日历、执行文件操作、调用API、接收通知、设置提醒、完成购买、进行部署等），都应触发该功能。该功能可用于规划干预措施、排查故障、预测结果、补充历史数据以供分析，或回答“如果我执行X会怎样？”这样的问题。在回顾过去的操作时，该功能也能帮助理解哪些操作成功了、哪些失败了以及原因何在。
---

# 因果推断（Causal Inference）

这是一个轻量级的因果推理层，用于预测行为结果。它不是通过匹配相关性来预测，而是通过建模干预措施和反事实情景来实现这一目标。

## 核心原则

**每个行为都必须能够被表示为对因果模型的一种明确干预，包括预测的效果、不确定性以及可验证的审计追踪（audit trail）。**

计划必须具备“因果有效性”（causally valid），而不仅仅是看似合理（plausible）。

## 何时触发该功能

**在任何高级行为（high-level action）上都可以触发此功能**，包括但不限于以下领域：

| 领域（Domain） | 需要记录的行为（Actions to Log） |
|--------|---------------|
| **通信（Communication）** | 发送邮件、发送消息、回复、跟进、通知、提及（mention） |
| **日历（Calendar）** | 创建/修改/取消会议、设置提醒、回复邀请（RSVP） |
| **任务（Tasks）** | 创建/完成/推迟任务、设置优先级、分配任务（assign） |
| **文件（Files）** | 创建/编辑/共享文档、提交代码（commit code）、部署（deploy） |
| **社交（Social）** | 发布内容、互动、评论、分享、私信（DM） |
| **购买（Purchases）** | 下单、订阅、取消、退款（cancel/refund） |
| **系统（System）** | 配置更改、权限授予、集成设置（configuration change/permission grant/integration setup） |

此外，在以下情况下也应触发该功能：
- **审查结果** — “那封邮件收到回复了吗？” → 记录结果并更新预估（Review outcomes → Log outcome, update estimates）
- **调试故障** — “为什么这个操作没有成功？” → 追踪因果关系（Debug failures → Trace causal graph）
- **补充历史数据** — “分析我过去的邮件/日历记录” → 解析日志并重建行为（Backfill history → Analyze past emails/calendars, reconstruct actions）
- **规划** — “我现在发送还是稍后发送？” → 查询因果模型（Planning → Should I send now or later? → Query causal model）

## 从历史数据中恢复信息（Backfill from Historical Data）

不要从头开始。解析现有日志以重建过去的行为和结果。

### 邮件数据恢复（Email Backfill）
```bash
# Extract sent emails with reply status
gog gmail list --sent --after 2024-01-01 --format json > /tmp/sent_emails.json

# For each sent email, check if reply exists
python3 scripts/backfill_email.py /tmp/sent_emails.json
```

### 日历数据恢复（Calendar Backfill）
```bash
# Extract past events with attendance
gog calendar list --after 2024-01-01 --format json > /tmp/events.json

# Reconstruct: did meeting happen? was it moved? attendee count?
python3 scripts/backfill_calendar.py /tmp/events.json
```

### 消息数据恢复（WhatsApp/Discord/Slack）
```bash
# Parse message history for send/reply patterns
wacli search --after 2024-01-01 --from me --format json > /tmp/wa_sent.json
python3 scripts/backfill_messages.py /tmp/wa_sent.json
```

### 通用数据恢复模式（Generic Backfill Pattern）
```python
# For any historical data source:
for record in historical_data:
    action_event = {
        "action": infer_action_type(record),
        "context": extract_context(record),
        "time": record["timestamp"],
        "pre_state": reconstruct_pre_state(record),
        "post_state": extract_post_state(record),
        "outcome": determine_outcome(record),
        "backfilled": True  # Mark as reconstructed
    }
    append_to_log(action_event)
```

## 架构（Architecture）

### A. 行为日志（Action Log，必备）

每个执行的操作都会生成一个结构化的事件记录：
```json
{
  "action": "send_followup",
  "domain": "email",
  "context": {"recipient_type": "warm_lead", "prior_touches": 2},
  "time": "2025-01-26T10:00:00Z",
  "pre_state": {"days_since_last_contact": 7},
  "post_state": {"reply_received": true, "reply_delay_hours": 4},
  "outcome": "positive_reply",
  "outcome_observed_at": "2025-01-26T14:00:00Z",
  "backfilled": false
}
```

将这些记录存储在 `memory/causal/action_log.jsonl` 文件中。

### B. 因果图（Causal Graphs，按领域划分）

每个领域从 10-30 个可观测变量开始构建因果图。

- **邮件领域（Email domain）：**
```
send_time → reply_prob
subject_style → open_rate
recipient_type → reply_prob
followup_count → reply_prob (diminishing)
time_since_last → reply_prob
```

- **日历领域（Calendar domain）：**
```
meeting_time → attendance_rate
attendee_count → slip_risk
conflict_degree → reschedule_prob
buffer_time → focus_quality
```

- **消息领域（Messaging domain）：**
```
response_delay → conversation_continuation
message_length → response_length
time_of_day → response_prob
platform → response_delay
```

- **任务领域（Task domain）：**
```
due_date_proximity → completion_prob
priority_level → completion_speed
task_size → deferral_risk
context_switches → error_rate
```

将因果图的定义存储在 `memory/causal/graphs/` 文件中。

### C. 估计（Estimation）

对于每个干预变量（intervention variable），估计其影响效果：

```python
# Pseudo: effect of morning vs evening sends
effect = mean(reply_prob | send_time=morning) - mean(reply_prob | send_time=evening)
uncertainty = std_error(effect)
```

首先使用简单的回归分析或倾向匹配（propensity matching）方法。当因果图足够清晰且需要更精确的预测时，再使用微分计算（do-calculus）方法。

### D. 决策流程（Decision Policy）

在执行操作之前：
1. 确定需要使用的干预变量。
2. 查询因果模型以获取预期的结果分布。
3. 计算预期的效用值及其不确定性范围。
4. 如果不确定性超过阈值或预期危害超过阈值，则拒绝执行该操作或寻求用户确认。
5. 将预测结果记录下来以供后续验证。

## 工作流程（Workflow）

### 对于每个操作（For Every Action）：
```
BEFORE executing:
1. Log pre_state
2. If enough historical data: query model for expected outcome
3. If high uncertainty or risk: confirm with user

AFTER executing:
1. Log action + context + time
2. Set reminder to check outcome (if not immediate)

WHEN outcome observed:
1. Update action log with post_state + outcome
2. Re-estimate treatment effects if enough new data
```

### 规划操作（Planning an Action）：
```
1. User request → identify candidate actions
2. For each action:
   a. Map to intervention(s) on causal graph
   b. Predict P(outcome | do(action))
   c. Estimate uncertainty
   d. Compute expected utility
3. Rank by expected utility, filter by safety
4. Execute best action, log prediction
5. Observe outcome, update model
```

### 调试故障（Debugging a Failure）：
```
1. Identify failed outcome
2. Trace back through causal graph
3. For each upstream node:
   a. Was the value as expected?
   b. Did the causal link hold?
4. Identify broken link(s)
5. Compute minimal intervention set that would have prevented failure
6. Log counterfactual for learning
```

## 快速入门：立即开始使用（Quick Start: Bootstrap Today）：
```bash
# 1. Create the infrastructure
mkdir -p memory/causal/graphs memory/causal/estimates

# 2. Initialize config
cat > memory/causal/config.yaml << 'EOF'
domains:
  - email
  - calendar
  - messaging
  - tasks

thresholds:
  max_uncertainty: 0.3
  min_expected_utility: 0.1

protected_actions:
  - delete_email
  - cancel_meeting
  - send_to_new_contact
  - financial_transaction
EOF

# 3. Backfill one domain (start with email)
python3 scripts/backfill_email.py

# 4. Estimate initial effects
python3 scripts/estimate_effect.py --treatment send_time --outcome reply_received --values morning,evening
```

## 安全限制（Safety Constraints）

定义需要用户明确批准的“受保护变量”（protected variables）：
```yaml
protected:
  - delete_email
  - cancel_meeting
  - send_to_new_contact
  - financial_transaction

thresholds:
  max_uncertainty: 0.3  # don't act if P(outcome) uncertainty > 30%
  min_expected_utility: 0.1  # don't act if expected gain < 10%
```

## 文件目录（File Directories）：
- `memory/causal/action_log.jsonl` — 所有记录的操作及其结果
- `memory/causal/graphs/` — 各领域的因果图定义
- `memory/causal/estimates/` — 学到的干预效果数据
- `memory/causal/config.yaml` — 安全阈值和受保护变量设置

## 参考资料（References）：
- 有关正式的干预语义，请参阅 `references/do-calculus.md`。
- 有关治疗效果估计方法，请参阅 `references/estimation.md`。