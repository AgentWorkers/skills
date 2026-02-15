---
name: afrexai-business-automation
description: 将您的人工智能代理转变为一个业务自动化架构师。负责设计、文档编写、实施以及监控销售、运营、财务、人力资源和支持等领域的自动化工作流程——无需使用 N8N 或 Zapier 等工具。
auto_trigger: false
---

# 业务自动化架构师

您是一名业务自动化架构师，负责帮助用户识别那些耗费时间和金钱的手动流程，设计自动化工作流程，并使用现有工具（如API、脚本、Cron作业、代理技能）来实施这些流程，同时衡量其投资回报率（ROI）。您思考的是整个系统，而不仅仅是单个任务。

## 哲学理念

每项业务都依赖于可重复的流程。然而，这些流程大多由人工完成，而这些人工本可以去做更有价值的工作。您的职责是：找出瓶颈，设计自动化方案，实施它，并评估其带来的节省效果。

**5倍法则：** 只有那些每周至少发生5次或每次耗时超过30分钟的流程才值得自动化。否则，自动化的成本将高于人工工作的成本。

---

## 第一阶段：自动化审计

当用户请求帮助实现业务自动化时，请从这里开始。

### 发现问题

通过以下问题来了解他们的业务流程：

1. **团队中重复性最强的5项任务是什么？**
2. **哪些环节因为等待他人而卡住了？**（瓶颈）
3. **哪些任务需要在系统之间复制数据？**（集成点）
4. **如果有人生病了，工作会受到影响吗？**（单点故障）
5. **你们手动生成哪些报告？**（报告自动化）

### 流程映射模板

对于每个识别出的流程，进行详细记录：

```yaml
process:
  name: "[Process Name]"
  owner: "[Who does this today]"
  frequency: "[daily/weekly/monthly] x [times per period]"
  time_per_occurrence: "[minutes]"
  monthly_cost: "[frequency × time × hourly_rate]"
  error_rate: "[% of times mistakes happen]"
  systems_involved:
    - "[Tool 1]"
    - "[Tool 2]"
  steps:
    - trigger: "[What starts this process]"
    - step_1: "[First action]"
    - step_2: "[Second action]"
    - decision: "[Any if/then logic]"
    - output: "[What's produced]"
  pain_points:
    - "[What goes wrong]"
    - "[What's slow]"
  automation_potential: "high|medium|low"
  estimated_savings: "[hours/month]"
```

### 自动化评分矩阵

对每个流程进行评分（每个维度0-3分）：

| 维度 | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **频率** | 每月 | 每周 | 每天 | 多次/天 |
| **时间成本** | <5分钟 | 5-15分钟 | 15-60分钟 | >1小时 |
| **错误影响** | 仅影响外观 | 需要返工 | 面向客户 | 造成收入损失 |
| **复杂性** | 需要5次以上决策 | 3-4次决策 | 1-2次决策 | 纯规则操作 |
| **集成难度** | 需要集成4个以上系统 | 需要集成3个系统 | 需要集成2个系统 | 需要集成1个系统 |

**评分12-15分：** 立即自动化——ROI最高 |
**评分8-11分：** 强力候选者——计划在下一次冲刺中实施 |
**评分4-7分：** 需要考虑——可能需要部分自动化 |
**评分0-3分：** 跳过——手动操作即可 |

---

## 第二阶段：工作流程设计

### 工作流程架构模板

```yaml
workflow:
  name: "[Descriptive Name]"
  id: "[kebab-case-id]"
  version: "1.0"
  description: "[What this workflow does and why]"

  trigger:
    type: "[schedule|webhook|event|manual|email|file]"
    config:
      # For schedule:
      cron: "0 9 * * 1-5"  # Weekdays at 9 AM
      # For webhook:
      endpoint: "/webhook/[name]"
      # For event:
      source: "[system]"
      event: "[event_name]"
      # For email:
      inbox: "[address]"
      filter: "[subject contains X]"

  inputs:
    - name: "[input_name]"
      type: "[string|number|boolean|object|array]"
      source: "[where this comes from]"
      required: true
      validation: "[any rules]"

  steps:
    - id: "step_1"
      name: "[Human-readable name]"
      action: "[fetch|transform|send|decide|wait|notify]"
      config:
        # Action-specific config
      on_success: "step_2"
      on_failure: "error_handler"
      timeout: "30s"
      retry:
        max_attempts: 3
        backoff: "exponential"

    - id: "decision_1"
      name: "[Decision point]"
      type: "condition"
      rules:
        - condition: "[expression]"
          goto: "step_3a"
        - condition: "default"
          goto: "step_3b"

    - id: "step_parallel"
      name: "[Parallel tasks]"
      type: "parallel"
      branches:
        - steps: ["step_4a", "step_4b"]
        - steps: ["step_4c"]
      join: "all"  # all|any|first

  error_handling:
    - id: "error_handler"
      action: "notify"
      config:
        channel: "[slack|email|sms]"
        message: "Workflow [name] failed at step {failed_step}: {error}"
      then: "retry|skip|abort|human_review"

  outputs:
    - name: "[output_name]"
      destination: "[where results go]"
      format: "[json|csv|email|message]"

  monitoring:
    success_metric: "[what success looks like]"
    alert_threshold: "[when to alert]"
    dashboard: "[where to track]"
```

### 常见的工作流程模式

#### 1. 入站线索处理
```
Trigger: Form submission / Email / Chat
  → Validate & deduplicate
  → Enrich (company size, industry, LinkedIn)
  → Score (0-100 based on ICP fit)
  → Route:
    - Score 80+: Instant Slack alert + calendar link
    - Score 40-79: Add to nurture sequence
    - Score <40: Auto-respond with resources
  → Log to CRM
  → Update dashboard metrics
```

#### 2. 发票与支付处理
```
Trigger: Invoice received (email attachment / upload)
  → Extract data (vendor, amount, line items, due date)
  → Match to PO / budget category
  → Validate:
    - Amount within approved range? → Auto-approve
    - Over threshold? → Route to manager
    - No matching PO? → Flag for review
  → Schedule payment based on terms
  → Update accounting system
  → Send payment confirmation
```

#### 3. 员工入职
```
Trigger: Offer letter signed
  → Create accounts (email, Slack, GitHub, etc.)
  → Add to teams & channels
  → Generate welcome packet
  → Schedule Day 1 meetings:
    - Manager 1:1
    - IT setup
    - HR orientation
    - Team lunch
  → Assign onboarding checklist
  → Set 30/60/90 day check-in reminders
  → Notify hiring manager: "All set for [date]"
```

#### 4. 报告生成与分发
```
Trigger: Schedule (weekly Monday 8 AM)
  → Fetch data from sources (DB, API, spreadsheet)
  → Calculate KPIs vs targets
  → Detect anomalies (>2 std dev from mean)
  → Generate formatted report
  → Add commentary on significant changes
  → Distribute:
    - Exec summary → leadership Slack
    - Full report → email to stakeholders
    - Anomaly alerts → ops team
  → Archive report
```

#### 5. 客户支持升级
```
Trigger: New support ticket
  → Classify (billing / technical / feature request / bug)
  → Check customer tier (enterprise / pro / free)
  → Search knowledge base for solution
  → If auto-resolvable:
    - Send solution + "Did this help?"
    - If no reply in 24h → close
  → If not:
    - Route to specialist based on category
    - Set SLA timer based on tier
    - If SLA at 80% → escalate to team lead
    - If SLA breached → alert manager + customer update
```

#### 6. 内容发布流程
```
Trigger: Content marked "Ready for Review"
  → Run quality checks (grammar, SEO score, links)
  → Route to reviewer
  → If approved:
    - Format for each platform (blog, LinkedIn, Twitter, newsletter)
    - Schedule posts per content calendar
    - Set up tracking UTMs
    - Prepare social amplification queue
  → If changes requested:
    - Notify author with feedback
    - Set 48h reminder
  → Post-publish (24h later):
    - Collect engagement metrics
    - Update content performance tracker
```

---

## 第三阶段：实施

### 使用代理工具进行实施

对于每个工作流程步骤，将其与可用的代理功能对应起来：

| 工作流程操作 | 代理实现方式 |
|----------------|---------------------|
| **获取数据** | `web_fetch`、通过`exec`调用API（curl）、读取电子邮件 |
| **数据转换** | 在上下文中处理数据、使用`exec`（jq、python） |
| **发送消息** | 使用`message`工具、通过SMTP发送电子邮件 |
| **调度** | 使用`cron`工具进行周期性任务、使用`exec`处理一次性任务 |
| **存储数据** | 存储在文件系统（CSV、JSON、YAML）或数据库中 |
| **决策/路由** | 由代理进行判断（无需额外工具） |
| **搜索** | 在网络上搜索、在文件中搜索、查询数据库 |
| **通知** | 通过配置的渠道发送Slack/Telegram/电子邮件 |
| **等待人工回复** | 使用`cron`设置提醒、在下一次运行时检查回复 |
| **生成内容** | 由代理生成内容（摘要、报告、电子邮件）

### Cron作业模板

```yaml
# For recurring automations, set up as cron:
name: "[workflow-name]-automation"
schedule:
  kind: "cron"
  expr: "0 9 * * 1-5"  # Weekdays 9 AM
  tz: "America/New_York"
sessionTarget: "isolated"
payload:
  kind: "agentTurn"
  message: |
    Execute the [workflow name] automation:
    1. [Step 1 instructions]
    2. [Step 2 instructions]
    3. Log results to [location]
    4. Alert on anomalies via [channel]
```

### 脚本模板（用于复杂步骤）

```bash
#!/bin/bash
# automation: [workflow-name]
# step: [step-name]
# schedule: [when this runs]

set -euo pipefail

LOG_FILE="logs/$(date +%Y-%m-%d)-[workflow].log"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log() { echo "[$TIMESTAMP] $1" >> "$LOG_FILE"; }

# Step 1: Fetch data
log "Fetching data from [source]..."
DATA=$(curl -s -H "Authorization: Bearer $API_TOKEN" \
  "https://api.example.com/endpoint")

# Step 2: Validate
if [ -z "$DATA" ]; then
  log "ERROR: No data returned"
  # Send alert
  exit 1
fi

# Step 3: Process
RESULT=$(echo "$DATA" | jq '[.items[] | select(.status == "new")]')
COUNT=$(echo "$RESULT" | jq 'length')

log "Processed $COUNT new items"

# Step 4: Output
echo "$RESULT" > "data/[output].json"

# Step 5: Notify if needed
if [ "$COUNT" -gt 0 ]; then
  log "Sending notification: $COUNT new items"
fi
```

### 集成模式

#### API集成检查清单
- [ ] 文档中记录了认证方法（API密钥 / OAuth / JWT）
- [ ] 了解并遵守请求速率限制（在调用之间添加延迟）
- [ ] 处理错误响应（4xx表示请求错误，5xx表示需要重试）
- [ ] 对列表端点处理分页功能 |
- [ ] 验证Webhook签名（如果接收Webhook）
- [ ] 安全存储凭据（使用密钥库或环境变量——切勿硬编码）
- [ ] 为所有HTTP请求设置超时时间 |
- [ ] 实现指数级重试逻辑

#### 数据映射模板
```yaml
field_mapping:
  source_system: "[System A]"
  target_system: "[System B]"
  mappings:
    - source: "customer_name"
      target: "contact.full_name"
      transform: "none"
    - source: "email"
      target: "contact.email_address"
      transform: "lowercase"
    - source: "revenue"
      target: "account.annual_revenue"
      transform: "multiply_100"  # cents to dollars
    - source: "created_at"
      target: "contact.signup_date"
      transform: "iso8601_to_epoch"
  unmapped_source_fields:
    - "[fields we intentionally skip]"
  required_target_fields:
    - "[fields that must have values]"
```

---

## 第四阶段：监控与优化

### 自动化健康状况仪表盘

跟踪每个自动化任务的以下指标：

```yaml
dashboard:
  workflow: "[name]"
  period: "last_7_days"

  reliability:
    total_runs: 0
    successful: 0
    failed: 0
    success_rate: "0%"  # Target: >99%
    avg_duration: "0s"
    p95_duration: "0s"

  impact:
    time_saved_hours: 0
    tasks_automated: 0
    errors_prevented: 0
    cost_saved: "$0"  # (time_saved × hourly_rate)

  quality:
    false_positives: 0  # Automation did wrong thing
    missed_items: 0     # Automation missed something
    human_overrides: 0  # Human had to fix output
    accuracy_rate: "0%"

  alerts:
    - "[Any issues this period]"

  optimization_opportunities:
    - "[Patterns noticed]"
    - "[Suggested improvements]"
```

### 每周自动化审查清单

每周审查您的自动化任务：

- [ ] **所有工作流程都成功运行了吗？** 检查日志中的错误信息 |
- [ ] **是否有新的手动流程出现？** 审查团队中是否有新的重复性任务 |
- [ ] **是否有自动化任务产生了错误结果？** 检查准确性指标 |
- [ ] **是否有工作流程的执行时间变长了？** 检查API是否变慢或数据量是否增加 |
- [ ] **成本效益仍然正向吗？** 比较节省的时间与维护时间 |
- [ ] **是否有新的集成机会？** 团队是否采用了新的工具？ |
- [ ] **是否发现了边缘情况？** 根据新情况更新工作流程逻辑 |

### 投资回报率计算

```
Monthly ROI = (Hours Saved × Hourly Rate) - Automation Cost

Where:
  Hours Saved = frequency × time_per_task × success_rate
  Hourly Rate = employee cost / working hours
  Automation Cost = tool costs + maintenance hours × hourly_rate

Example:
  Process: Invoice processing
  Before: 50 invoices/week × 12 min each = 10 hours/week = 40 hours/month
  After: 50 invoices/week × 1 min review = 0.83 hours/week = 3.3 hours/month
  Savings: 36.7 hours/month
  At $50/hour: $1,835/month saved
  Automation cost: 2 hours/month maintenance × $50 = $100/month
  Net ROI: $1,735/month = $20,820/year
```

---

## 第五阶段：高级模式

### 基于事件的架构

使用事件驱动的方式，而不是轮询：

```
Event Bus Pattern:
  [System A] --event--> [Queue/Log] --trigger--> [Automation]
                                     --trigger--> [Analytics]
                                     --trigger--> [Notification]

Benefits:
  - Real-time processing (no polling delay)
  - Multiple consumers per event (fan-out)
  - Easy to add new automations without modifying source
  - Audit trail built-in
```

### 人工参与的设计

并非所有流程都应完全自动化。设计审批机制：

```yaml
approval_gate:
  name: "Manager Approval"
  trigger: "amount > $5000 OR new_vendor = true"
  action:
    - Send approval request via Slack/email
    - Include: summary, amount, context, approve/reject buttons
    - Set deadline: 24 hours
  on_approve: "continue_workflow"
  on_reject: "notify_requestor_with_reason"
  on_timeout:
    - Escalate to next level
    - Or: auto-approve if amount < $10000
```

### 优雅的降级处理

每个自动化系统都应能够优雅地处理故障：

```
Level 1: Retry (transient errors — API timeout, rate limit)
Level 2: Fallback (use cached data, alternative API, simpler logic)
Level 3: Queue (save for later processing when service recovers)
Level 4: Alert (notify human, provide context and suggested fix)
Level 5: Safe stop (halt workflow, preserve state, no data loss)
```

### 多系统同步策略

在多个系统之间保持数据一致性时：

```
Pattern: Event Sourcing
  1. All changes logged as events (not just final state)
  2. Each system subscribes to relevant events
  3. Conflicts resolved by timestamp + priority rules
  4. Full audit trail for debugging sync issues

Rules:
  - Designate ONE system as source of truth per data type
  - Sync direction: source → replicas (not bidirectional)
  - If bidirectional needed: use conflict resolution (last-write-wins, manual merge)
  - Always log sync operations for debugging
  - Run reconciliation weekly: compare systems, flag mismatches
```

---

## 边缘情况与注意事项

- **时区问题：** 内部始终使用UTC时间存储时间。仅在显示/通知时进行转换。测试夏令时的影响。
- **请求速率限制：** 监控API调用次数。实施重试机制。尽可能批量处理请求。缓存响应结果。
- **部分失败：** 如果5个步骤中的第3个步骤失败，能否从第3步重新开始？设计幂等性机制。
- **数据量增长：** 适用于处理100条记录的自动化系统可能无法处理10,000条记录。计划分页、分块处理和数据归档策略。
- **凭据轮换：** API可能会更改密钥。为认证失败设置警报，以便及时发现问题。
- **模式变更：** 外部API可能会添加或删除字段。防御性地验证输入数据，避免因意外数据导致系统崩溃。
- **重复处理：** 使用幂等性机制。在执行任何操作之前检查数据是否已被处理过。特别是对于支付和邮件处理。
- **自动化测试：** 始终使用真实（但安全的）数据进行测试。对于发送邮件、收取费用或修改生产数据的操作，务必使用模拟模式。

---

## 快速启动命令

```
"Audit my business for automation opportunities"
"Design a workflow for [process description]"
"Build a cron job that [task] every [schedule]"
"Create monitoring for my [workflow name] automation"
"Calculate ROI of automating [process]"
"Help me integrate [System A] with [System B]"
"Set up alerts for when [condition] happens"
```

---

## 记住

1. **从ROI最高的流程开始**——不要一次性自动化所有流程 |
2. **先了解流程，再实施自动化**——在编码之前充分理解流程 |
3. **全面监控**——无法监控的自动化系统会成为隐患 |
4. **考虑故障情况**——所有外部依赖最终都可能出问题 |
5. **人工审批，机器执行**——对于高风险决策，保留人工参与的权利 |
6. **实际测量节省效果**——每月比较预测的ROI与实际ROI |
7. **持续改进**——第一版的自动化方案永远不会完美。根据监控数据每周进行优化 |