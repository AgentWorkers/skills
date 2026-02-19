# SRE与事件管理平台

这是一个完整的站点可靠性工程（Site Reliability Engineering）系统，涵盖了从服务水平目标（Service Level Objectives, SLOs）的定义，到事件响应（Incident Response）、混沌工程（Chaos Engineering），以及运营卓越性（Operational Excellence）的整个流程。该系统完全不依赖于任何外部依赖。

---

## 第一阶段：可靠性评估

在开始任何建设之前，首先评估当前的系统状况。

### 服务目录条目

```yaml
service:
  name: ""
  tier: ""  # critical | important | standard | experimental
  owner_team: ""
  oncall_rotation: ""
  dependencies:
    upstream: []    # services we call
    downstream: []  # services that call us
  data_classification: ""  # public | internal | confidential | restricted
  deployment_frequency: ""  # daily | weekly | biweekly | monthly
  architecture: ""  # monolith | microservice | serverless | hybrid
  language: ""
  infra: ""  # k8s | ECS | Lambda | VM | bare-metal
  traffic_pattern: ""  # steady | diurnal | spiky | seasonal
  peak_rps: 0
  storage_gb: 0
  monthly_cost_usd: 0
```

### 成熟度评估（每个维度评分1-5分）

| 维度 | 1（临时） | 3（已定义） | 5（优化） | 总分 |
|---------|---------|-------------|---------------|-------|
| 服务水平目标（SLOs） | 未定义SLOs | SLOs已定义，每季度审查 | 数据驱动的SLOs，自动错误预算 | |
| 监控 | 基本健康检查 | 重要指标（Golden Signals）+ 仪表盘 | 全面可观测性，异常检测 | |
| 事件响应 | 无事件响应流程 | 有文档化的流程和事后分析 | 自动检测，结构化的事件响应系统（ICS） | |
| 自动化 | 手动部署 | 持续集成/持续交付（CI/CD）管道，部分自动化 | 自愈能力，自动扩展，GitOps | |
| 混沌工程 | 无测试 | 基本的故障注入 | 在生产环境中进行持续的混沌测试 | |
| 容量规划 | 反应式扩展 | 每季度预测 | 预测性自动扩展 | |
| 工作量管理 | 超过50%的工作量 | 工作量被记录，有减少计划 | <25%的工作量，系统化减少 | |
| 值班人员健康状况 | 疲劳问题，24/7值班 | 有轮换机制，有升级路径 | 负载均衡，每班次<2页警报 | |

**评分解释：**
- 8-16分：处于紧急应对阶段——从定义SLOs和事件响应流程开始
- 17-24分：基础建设完成——加入混沌工程和减少工作量
- 25-32分：逐步成熟——优化错误预算和容量规划
- 33-40分：处于高级阶段——专注于预测性可靠性建设和文化培养

---

## 第二阶段：SLI/SLO框架

### 按服务类型选择SLI

| 服务类型 | 主要SLI | 辅助SLI |
|-------------|-------------|----------------|
| API/后端 | 请求成功率 | 响应时间（p50/p95/p99），吞吐量 |
| 前端/Web | 页面加载时间（LCP） | 响应时间（FID/INP），错误率 |
| 数据管道 | 数据新鲜度 | 数据正确性，完整性，吞吐量 |
| 存储 | 稳定性 | 可用性，延迟 |
| 流媒体 | 处理延迟 | 吞吐量，排序，数据丢失率 |
| 批量作业 | 成功率 | 执行时间，服务水平协议（SLA）合规性 |
| 机器学习模型 | 预测延迟 | 精确度变化，特征更新频率 |

### SLI规范模板

```yaml
sli:
  name: "request_success_rate"
  description: "Proportion of valid requests served successfully"
  type: "availability"  # availability | latency | quality | freshness
  measurement:
    good_events: "HTTP responses with status < 500"
    total_events: "All HTTP requests excluding health checks"
    source: "load balancer access logs"
    aggregation: "sum(good) / sum(total) over rolling 28-day window"
  exclusions:
    - "Health check endpoints (/healthz, /readyz)"
    - "Synthetic monitoring traffic"
    - "Requests from blocked IPs"
    - "4xx responses (client errors)"
```

### SLO目标选择指南

| 九个九（9s） | 运行时间百分比 | 每月停机时间 | 适用于 |
|-------|----------|----------------|-----------------|
| 2个九 | 99% | 7小时18分钟 | 内部工具，开发环境 |
| 2.5个九 | 99.5% | 3小时39分钟 | 非关键服务，后台服务 |
| 3个九 | 99.9% | 43分钟50秒 | 标准生产服务 |
| 3.5个九 | 99.95% | 21分钟55秒 | 关键客户服务 |
| 4个九 | 99.99% | 4分钟23秒 | 关键服务，支付系统，认证功能 |
| 5个九 | 99.999% | 26秒 | 关键服务，如生命安全，金融清算 |

**设置目标的原则：**
1. 初始目标可以设定得比实际需求低一些——以后可以逐步提高
2. SLO应低于服务水平协议（SLA）——通常保留0.1-0.5%的缓冲余地
3. 内部服务的SLO应低于外部服务的SLO——以便在客户发现问题之前解决内部问题
4. 达到每个“九个九”的目标通常需要更高的成本
5. 如果无法衡量某个指标，就无法为其设定SLO |

### SLO文档模板

```yaml
slo:
  service: ""
  sli: ""
  target: 99.9  # percentage
  window: "28d"  # rolling window
  error_budget: 0.1  # 100% - target
  error_budget_minutes: 40  # per 28-day window
  
  burn_rate_alerts:
    - name: "fast_burn"
      burn_rate: 14.4  # exhausts budget in 2 hours
      short_window: "5m"
      long_window: "1h"
      severity: "page"
    - name: "medium_burn"
      burn_rate: 6.0   # exhausts budget in ~5 hours
      short_window: "30m"
      long_window: "6h"
      severity: "page"
    - name: "slow_burn"
      burn_rate: 1.0   # exhausts budget in 28 days
      short_window: "6h"
      long_window: "3d"
      severity: "ticket"
  
  review_cadence: "monthly"
  owner: ""
  stakeholders: []
  
  escalation_when_budget_exhausted:
    - "Halt non-critical deployments"
    - "Redirect engineering to reliability work"
    - "Escalate to VP Engineering if no improvement in 48h"
```

---

## 第三阶段：错误预算管理

### 错误预算政策

```yaml
error_budget_policy:
  service: ""
  
  budget_states:
    healthy:
      condition: "remaining_budget > 50%"
      actions:
        - "Normal development velocity"
        - "Feature work prioritized"
        - "Chaos experiments allowed"
    
    warning:
      condition: "remaining_budget 25-50%"
      actions:
        - "Increase monitoring scrutiny"
        - "Review recent changes for risk"
        - "Limit risky deployments to business hours"
        - "No chaos experiments"
    
    critical:
      condition: "remaining_budget 0-25%"
      actions:
        - "Feature freeze — reliability work only"
        - "All deployments require SRE approval"
        - "Mandatory rollback plan for every change"
        - "Daily error budget review"
    
    exhausted:
      condition: "remaining_budget <= 0"
      actions:
        - "Complete deployment freeze"
        - "All engineering redirected to reliability"
        - "VP Engineering notified"
        - "Postmortem required for budget exhaustion"
        - "Freeze maintained until budget recovers to 10%"
  
  exceptions:
    - "Security patches always allowed"
    - "Regulatory compliance changes always allowed"
    - "Data loss prevention always allowed"
  
  reset: "Rolling 28-day window (no manual resets)"
```

### 错误预算消耗计算

```
Burn rate = (error rate observed) / (error rate allowed by SLO)

Example:
- SLO: 99.9% (error budget = 0.1%)
- Current error rate: 0.5%
- Burn rate = 0.5% / 0.1% = 5x

At 5x burn rate → budget exhausted in 28d / 5 = 5.6 days
```

### 错误预算仪表盘

每周跟踪以下指标：

| 指标 | 当前值 | 趋势 | 状态 |
|--------|---------|-------|--------|
| 剩余预算百分比 | | ↑↓→ | 🟢🟡🔴 |
| 本周消耗的预算 | | | |
| 每小时/每6小时/每24小时的错误预算消耗率 | | | |
| 消耗预算的事件数量 | | | |
| 最主要的错误来源 | | | |

---

## 第四阶段：监控与警报架构

### 四个重要指标

| 指标 | 需要监控的内容 | 在什么情况下触发警报 |
|--------|----------------|------------|
| **响应时间** | p50、p95、p99的响应时间 | 如果p99的响应时间超过基线值的2倍，持续5分钟 |
| **流量** | 每秒请求数量，同时在线用户数 | 如果流量下降超过30%或激增超过50%，可能表示上游问题 |
| **错误率** | 5xx错误率，超时率，异常率 | 如果错误率超过SLO允许的错误预算阈值 |
| **饱和度** | CPU、内存、磁盘、连接数、队列深度 | 如果这些指标持续超过80%超过10分钟 |

### 使用方法（基础设施）

对于每种资源，监控以下指标：
- **利用率**：使用的容量百分比（0-100%）
- **饱和度**：队列深度或等待时间（0表示无等待）
- **错误率**：错误总数或错误率

### RED方法（服务）

对于每种服务，监控以下指标：
- **请求率**：每秒请求数量
- **错误率**：每秒失败请求数量
- **延迟分布**：延迟的时间分布

### 警报设计规则
1. **所有警报都必须附带事件响应流程的链接**——无一例外
2. **所有警报都必须具有可操作性**——如果无法根据警报采取行动，应立即删除该警报
3. **优先处理症状而非根本原因**——例如，当问题是由于“用户无法访问系统”时触发警报，而不是“数据库CPU使用率高”时触发警报
4. **多窗口、多错误预算阈值**——避免使用单一阈值触发警报
5. **仅对影响客户的服务显示警报**——其他情况应通过工单处理

### 警报严重程度分级

| 严重程度 | 响应时间 | 通知方式 | 例子 |
|----------|--------------|-------------|----------|
| P0/紧急 | <5分钟 | PagerDuty + 电话 | SLO错误预算严重超标，数据丢失，安全漏洞 |
| P1/紧急 | <30分钟 | Slack + PagerDuty | 服务性能下降，错误率升高 |
| P2/工单 | 下一个工作日 | 自动创建工单 | 功能运行缓慢，非关键组件故障 |
| P3/日志 | 每周审查 | 仅通过仪表盘显示 | 信息性警报，用于趋势分析 |

### 结构化日志标准

```json
{
  "timestamp": "2026-02-17T11:24:00.000Z",
  "level": "error",
  "service": "payment-api",
  "trace_id": "abc123",
  "span_id": "def456",
  "message": "Payment processing failed",
  "error_type": "TimeoutException",
  "error_message": "Gateway timeout after 30s",
  "http_method": "POST",
  "http_path": "/api/v1/payments",
  "http_status": 504,
  "duration_ms": 30012,
  "customer_id": "cust_xxx",
  "payment_id": "pay_yyy",
  "amount_cents": 4999,
  "retry_count": 2,
  "environment": "production",
  "host": "payment-api-7b4d9-xk2p1",
  "region": "us-east-1"
}
```

---

## 第五阶段：事件响应框架

### 严重程度分类矩阵

| 严重程度 | 影响范围：1%用户 | 影响范围：<25%用户 | 影响范围：>25%用户 | 影响范围：所有用户 |
|----------------|----------------|----------------|-------------------|
| **核心功能故障** | SEV3 | SEV2 | SEV1 | SEV1 |
| **性能下降** | SEV4 | SEV3 | SEV2 | SEV1 |
| **非核心功能故障** | SEV4 | SEV3 | SEV3 | SEV3 |
| **外观/次要问题** | SEV4 | SEV4 | SEV3 | SEV3 |

**自动升级触发条件：**
- 任何数据丢失 → 至少触发SEV1级别的警报
- 涉及个人身份信息（PII）的安全漏洞 → 触发SEV1级别的警报
- 影响收入的情况 → 自动升级一个等级

### 事件指挥系统（ICS）

| 角色 | 负责内容 | 指定人员 |
|------|---------------|----------|
| **事件指挥官（Incident Commander, IC）** | 负责解决问题，做出决策，管理事件处理流程 |
| **沟通协调员（Communications Lead）** | 更新事件状态，与利益相关者沟通，向客户传达信息 |
| **运营负责人（Operations Lead）** | 直接操作，执行修复工作 |
| **专家（Subject Matter Expert）** | 对受影响系统有深入了解 |

**IC规则：**
1. 事件指挥官不负责调试问题——他们负责协调处理流程 |
2. 当团队意见不一致时，事件指挥官有最终决策权 |
3. 事件指挥官可以在任何时候升级事件的严重程度 |
4. 事件处理结束后，事件指挥官负责交接工作 |
| **事件指挥官负责事件结束后的总结工作** |

### 事件响应工作流程

```
DETECT → TRIAGE → RESPOND → MITIGATE → RESOLVE → REVIEW

Step 1: DETECT (0-5 min)
├── Alert fires OR user report received
├── On-call acknowledges within SLA
└── Quick assessment: is this real? What severity?

Step 2: TRIAGE (5-15 min)
├── Classify severity using matrix above
├── Assign IC and roles
├── Open incident channel (#inc-YYYY-MM-DD-title)
├── Post initial status update
└── Start timeline document

Step 3: RESPOND (15 min - ongoing)
├── IC briefs team: "Here's what we know, here's what we don't"
├── Operations Lead begins investigation
├── Check: recent deployments? Config changes? Dependency issues?
├── Parallel investigation tracks if needed
└── 15-minute check-ins for SEV1, 30-min for SEV2

Step 4: MITIGATE (ASAP)
├── Priority: STOP THE BLEEDING
├── Options (fastest first):
│   ├── Rollback last deployment
│   ├── Feature flag disable
│   ├── Traffic shift / failover
│   ├── Scale up / circuit breaker
│   └── Manual data fix
├── Mitigated ≠ Resolved — temporary fix is OK
└── Update status: "Impact mitigated, root cause investigation ongoing"

Step 5: RESOLVE
├── Root cause identified and fixed
├── Verification: SLIs back to normal for 30+ minutes
├── All-clear communicated
└── IC declares incident resolved

Step 6: REVIEW (within 5 business days)
├── Blameless postmortem written
├── Action items assigned with owners and deadlines
├── Postmortem review meeting
└── Action items tracked to completion
```

### 通信模板

**内部初始通知：**
```
🔴 INCIDENT: [Title]
Severity: SEV[X]
Impact: [Who/what is affected]
Status: Investigating
IC: [Name]
Channel: #inc-[date]-[slug]
Next update: [time]
```

**面向客户的状况通知：**
```
[Service] - Investigating increased error rates

We are currently investigating reports of [symptom]. 
Some users may experience [user-visible impact].
Our team is actively working on a resolution.
We will provide an update within [time].
```

**问题解决通知：**
```
✅ RESOLVED: [Title]
Duration: [X hours Y minutes]
Impact: [Summary]
Root cause: [One sentence]
Postmortem: [Link] (within 5 business days)
```

---

## 第六阶段：事后分析框架

### 无责备的事后分析模板

```yaml
postmortem:
  title: ""
  date: ""
  severity: ""  # SEV1-4
  duration: ""  # total incident duration
  authors: []
  reviewers: []
  status: "draft"  # draft | in-review | final
  
  summary: |
    One paragraph: what happened, what was the impact, how was it resolved.
  
  impact:
    users_affected: 0
    duration_minutes: 0
    revenue_impact_usd: 0
    slo_budget_consumed_pct: 0
    data_loss: false
    customer_tickets: 0
  
  timeline:
    - time: ""
      event: ""
      # Chronological, every significant event
      # Include detection time, escalation, mitigation attempts
  
  root_cause: |
    Technical explanation of WHY it happened.
    Go deep — surface causes are not root causes.
  
  contributing_factors:
    - ""  # What made it worse or delayed resolution?
  
  detection:
    how_detected: ""  # alert | user report | manual check
    time_to_detect_minutes: 0
    could_have_detected_sooner: ""
  
  resolution:
    how_resolved: ""
    time_to_mitigate_minutes: 0
    time_to_resolve_minutes: 0
  
  what_went_well:
    - ""  # Explicitly call out what worked
  
  what_went_wrong:
    - ""
  
  where_we_got_lucky:
    - ""  # Things that could have made it worse
  
  action_items:
    - id: "AI-001"
      type: ""  # prevent | detect | mitigate | process
      description: ""
      owner: ""
      priority: ""  # P0 | P1 | P2
      deadline: ""
      status: "open"  # open | in-progress | done
      ticket: ""
```

### 根本原因分析方法

**五问法（简单事件）：**
1. 为什么用户会看到错误？ → API返回了500状态码？
2. 为什么API返回500状态码？ → 数据库连接池耗尽
3. 为什么连接池会耗尽？ → 长时间运行的查询占用了连接资源
4. 为什么查询会运行这么长时间？ → 新列没有索引
5. 为什么没有索引？ → 迁移过程中没有包含索引；持续集成（CI）过程中没有进行查询性能检查

**根本原因：** 迁移过程中没有自动化查询性能检查
**行动：** 将查询性能检查添加到持续集成的代码审查流程中

**鱼骨图/石川图（复杂事件）：**

```
Categories to investigate:
├── People: Training? Fatigue? Communication?
├── Process: Runbook? Escalation? Change management?
├── Technology: Bug? Config? Capacity? Dependency?
├── Environment: Network? Cloud provider? Third party?
├── Monitoring: Detection gap? Alert fatigue? Dashboard gap?
└── Testing: Test coverage? Load testing? Chaos testing?
```

**影响因素分类：**
| 分类 | 需要探讨的问题 |
|----------|-----------|
| 触发因素 | 是什么变化或事件导致了问题？ |
| 传播因素 | 问题为什么没有得到控制？ |
| 检测因素 | 为什么问题没有在早期被发现？ |
| 解决因素 | 什么阻碍了问题的快速解决？ |
| 过程因素 | 哪些流程环节导致了问题？ |

### 事后分析会议（60分钟）

```
1. Timeline walk-through (15 min)
   - Author presents chronology
   - Attendees add context ("I remember seeing X at this point")

2. Root cause deep-dive (15 min)  
   - Do we agree on root cause?
   - Are there additional contributing factors?

3. Action item review (20 min)
   - Are these the RIGHT actions?
   - Are they prioritized correctly?
   - Do owners agree on deadlines?

4. Process improvements (10 min)
   - Could we have detected this sooner?
   - Could we have resolved this faster?
   - What would have prevented this entirely?
```

---

## 第七阶段：混沌工程

### 混沌工程成熟度模型

| 级别 | 名称 | 活动内容 |
|-------|------|-----------|
| 0 | 无 | 不进行混沌测试 |
| 1 | 探索性 | 在测试环境中手动引发故障 |
| 2 | 系统性 | 在测试环境中定期进行混沌实验 |
| 3 | 生产环境 | 在生产环境中进行受控的混沌测试（称为“游戏日”） |
| 4 | 持续性 | 在生产环境中进行自动化的混沌测试，并有安全控制措施 |

### 混沌实验模板

```yaml
experiment:
  name: ""
  hypothesis: "When [fault], the system will [expected behavior]"
  
  steady_state:
    metrics:
      - name: ""
        baseline: ""
        acceptable_range: ""
  
  method:
    fault_type: ""  # network | compute | storage | dependency | data
    target: ""      # which service/component
    blast_radius: ""  # single pod | single AZ | percentage of traffic
    duration: ""
    
  safety:
    abort_conditions:
      - "SLO burn rate exceeds 10x"
      - "Customer-visible errors detected"
      - "Alert fires that we didn't expect"
    rollback_plan: ""
    required_approvals: []
    
  results:
    outcome: ""  # confirmed | disproved | inconclusive
    observations: []
    action_items: []
```

### 混沌实验库

| 分类 | 实验内容 | 验证目标 |
|----------|-----------|-----------|
| **网络** | 在数据库请求中增加200毫秒的延迟 | 处理超时，设置断路器 |
| **网络** | 将5%的数据包丢弃 | 重试逻辑，错误处理 |
| **计算** | 每10分钟随机终止一个容器 | 自动重启，负载均衡 |
| **计算** | 将某个节点的CPU使用率提高到95% | 自动扩展，优雅降级 |
| **计算** | 将磁盘使用率提高到95% | 监控磁盘使用情况，轮换日志 |
| **存储** | 将数据库延迟增加5倍 | 处理连接池超时 |
| **存储** | 模拟缓存故障（例如Redis故障） | 使用缓存替代方案，设置数据库备份 |
| **依赖关系** | 阻止外部API的访问（例如支付服务） | 设置断路器，进行重试 |
| **依赖关系** | 从认证服务返回429状态码 | 设置请求速率限制，进行重试 |
| **数据** | 部分节点的时间戳不一致 | 处理时间戳问题，确保数据排序正确 |
| **扩展** | 在5分钟内流量激增10倍 | 自动扩展，调整队列深度 |

### “游戏日”运行手册

```
PRE-GAME (1 week before):
□ Experiment designed and reviewed
□ Steady-state metrics identified
□ Abort conditions defined
□ All participants briefed
□ Runbacks tested in staging
□ Stakeholders notified

GAME DAY:
□ Verify steady state (15 min baseline)
□ Announce in #engineering: "Chaos Game Day starting"
□ Inject fault
□ Observe and document
□ If abort condition hit → rollback immediately
□ Run for planned duration
□ Remove fault
□ Verify recovery to steady state

POST-GAME (same day):
□ Results documented
□ Surprises noted
□ Action items created
□ Share findings in team meeting
```

---

## 第八阶段：工作量管理

### 工作量识别

**定义：** 手动执行、重复性高、可自动化、缺乏长期价值的工作，且会随着服务规模的扩大而线性增长。

### 工作量清单模板

```yaml
toil_item:
  name: ""
  category: ""  # deployment | scaling | config | data | access | monitoring | recovery
  frequency: ""  # daily | weekly | monthly | per-incident
  time_per_occurrence_min: 0
  occurrences_per_month: 0
  total_hours_per_month: 0
  teams_affected: []
  automation_difficulty: ""  # low | medium | high
  automation_value: 0  # hours saved per month
  priority_score: 0  # value / difficulty
```

### 工作量减少优先级矩阵

| 工作量 | 需要投入的努力时间（每小时） | 推荐处理方式 | 计划措施 |
|---------|----------------|----------------|-------------------|
| **高价值工作**（>10小时/小时） | 首先自动化处理 | 接着考虑优化 | 计划进一步减少 |
| **中等价值工作**（2-10小时/小时） | 先自动化处理 | 接着考虑优化 | 评估是否需要进一步减少 |
| **低价值工作**（<2小时/小时） | 快速完成 | 可以跳过 | 不需要额外投入 |

### 常见的工作量优化目标（按影响程度排序）

1. **手动部署** → 使用持续集成/持续交付（CI/CD）管道和GitOps |
2. **访问权限配置** → 提供自助服务，并对低风险操作设置自动审批流程 |
3. **证书续期** → 使用自动续期系统（如Let's Encrypt） |
4. **扩展决策** | 使用自动扩展机制（HPA）和预测性自动扩展 |
5. **日志排查** | 使用结构化的日志记录系统，进行关联分析，并通过仪表盘监控 |
6. **数据修复** | 使用自助管理工具，并在数据摄入时进行验证 |
7. **配置更改** | 将配置信息编码化，并通过自动化流程进行部署 |
8. **事件响应** | 为已知问题创建自动化事件响应流程 |
9. **容量报告** | 使用自动化仪表盘和预测模型 |
10. **值班安排** | 减少不必要的手动工作，并优化处理流程 |

### 工作量预算规则
**目标：SRE工作时间的25%用于处理工作量相关任务。**每月进行监控。如果实际工作量超过25%，应优先考虑自动化改进。

---

## 第九阶段：容量规划

### 容量规划模板

```yaml
capacity_model:
  service: ""
  bottleneck_resource: ""  # CPU | memory | storage | connections | bandwidth
  
  current_state:
    peak_utilization_pct: 0
    headroom_pct: 0
    cost_per_month_usd: 0
    
  growth_forecast:
    metric: ""  # MAU | requests/sec | storage_gb
    current: 0
    monthly_growth_pct: 0
    projected_6mo: 0
    projected_12mo: 0
    
  scaling_strategy:
    type: ""  # horizontal | vertical | hybrid
    auto_scaling: true
    min_instances: 0
    max_instances: 0
    scale_up_threshold: 80  # % utilization
    scale_down_threshold: 30
    cooldown_seconds: 300
    
  cost_projection:
    current_monthly: 0
    projected_6mo_monthly: 0
    projected_12mo_monthly: 0
```

### 容量规划频率

| 定期频率 | 需要执行的操作 |
|-----------|--------|
| 每日 | 审查自动扩展情况，检查异常情况 |
| 每周 | 审查资源使用趋势，检查是否有扩展空间 |
| 每月 | 更新容量预测模型，评估成本 |
| 每季度 | 进行全面容量审查，制定预算计划 |
| 上线前 | 进行负载测试，确保系统能够承受预期峰值的两倍负载 |

### 负载测试基准

| 测试场景 | 测试方法 | 测试时间 | 目标 |
|----------|--------|----------|--------|
| 基线测试 | 在当前峰值负载下进行测试 | 30分钟 | 确保指标准确 |
| 增长测试 | 在负载达到当前峰值的2倍时进行测试 | 15分钟 | 确保系统能够扩展 |
| 峰值测试 | 在负载达到正常值的10倍时进行测试 | 5分钟 | 检查系统是否能够稳定运行 |
| 扩容测试 | 在负载达到正常值的1.5倍时进行测试 | 4小时 | 确保系统没有内存泄漏或性能下降 |
| 压力测试 | 逐步增加负载，直到系统出现故障 | 直到系统无法承受为止 |

---

## 第十阶段：值班安排优化

### 值班人员健康状况指标

| 指标 | 正常情况 | 警告情况 | 危急情况 |
|--------|---------|---------|---------|
| 每班次的页面访问量 | <2 | 2-5 | >5 |
| 非工作时间内的页面访问量 | <1/周 | 1-3/周 | >3/周 |
| 响应时间 | <5分钟 | 5-15分钟 | >15分钟 |
| 问题处理时间 | <30分钟 | 30-60分钟 | >60分钟 |
| 警报误报率 | <10% | 10-30% | >30% |
| 升级请求率 | <20% | 20-40% | >40% |
| 值班人员的满意度 | >4/5 | 3-4/5 | <3/5 |

### 值班安排的最佳实践

1. **最小轮换人数：5人**（每周轮换一次）
2. **避免连续两周值班**（除非团队规模太小）
3. **全球团队应遵循“跟随太阳作息时间”原则**（避免在凌晨3点安排值班）
4. **必须同时安排主要值班人员和备用值班人员**
5. **交接时必须提交详细文档**——包括未解决的问题、最近的部署情况、已知风险 |
6. **提供相应的补偿**——如加班费用或休假安排 |

### 值班交接模板

```
## On-Call Handoff: [Date]

### Open Issues
- [Issue]: [Status, next steps]

### Recent Changes (last 7 days)
- [Deployment/config change]: [Risk level, rollback plan]

### Known Risks
- [Event/condition]: [What to watch for]

### Scheduled Maintenance
- [When]: [What, duration, rollback plan]

### Runbook Updates
- [Any new/updated runbooks since last rotation]
```

### 事件响应流程模板

```yaml
runbook:
  title: ""
  alert_name: ""  # exact alert that triggers this
  last_updated: ""
  owner: ""
  
  overview: |
    What this alert means in plain English.
    
  impact: |
    What users/systems are affected and how.
    
  diagnosis:
    - step: "Check service health"
      command: ""
      expected: ""
      if_unexpected: ""
    - step: "Check recent deployments"
      command: ""
      expected: ""
      if_unexpected: "Rollback: [command]"
    - step: "Check dependencies"
      command: ""
      expected: ""
      if_unexpected: ""
      
  mitigation:
    - option: "Rollback"
      when: "Recent deployment suspected"
      steps: []
    - option: "Scale up"
      when: "Traffic spike"
      steps: []
    - option: "Failover"
      when: "Single component failure"
      steps: []
      
  escalation:
    after_minutes: 30
    contact: ""
    context_to_provide: ""
```

---

## 第十一阶段：可靠性审查与治理

### 每周SRE审查（30分钟）

```
1. SLO Status (5 min)
   - Budget remaining per service
   - Any burn rate alerts this week?

2. Incident Review (10 min)
   - Incidents this week: count, severity, duration
   - Open postmortem action items: status check

3. On-Call Health (5 min)
   - Pages this week (total, off-hours, false positives)
   - Any on-call feedback?

4. Reliability Work (10 min)
   - Automation shipped this week
   - Toil reduced (hours saved)
   - Chaos experiments run
   - Capacity concerns
```

### 每月可靠性报告

```yaml
monthly_report:
  period: ""
  
  slo_summary:
    services_meeting_slo: 0
    services_breaching_slo: 0
    worst_performing: ""
    
  incidents:
    total: 0
    by_severity: { SEV1: 0, SEV2: 0, SEV3: 0, SEV4: 0 }
    mttr_minutes: 0
    mttd_minutes: 0
    repeat_incidents: 0
    
  error_budget:
    services_in_healthy: 0
    services_in_warning: 0
    services_in_critical: 0
    services_exhausted: 0
    
  toil:
    hours_spent: 0
    hours_automated_away: 0
    pct_of_sre_time: 0
    
  on_call:
    total_pages: 0
    off_hours_pages: 0
    false_positive_pct: 0
    avg_ack_time_min: 0
    
  action_items:
    open: 0
    completed_this_month: 0
    overdue: 0
    
  highlights: []
  concerns: []
  next_month_priorities: []
```

### 生产环境准备情况审查

在任何新服务上线之前，需要完成以下检查：

| 检查项目 | 状态 | 是否满足要求 |
|----------|-------|--------|
| **服务水平目标（SLOs）** | SLOs已定义并得到监控 | |
| **服务水平目标（SLOs）** | SLO目标已与利益相关者确认并设定 | |
| **错误预算政策** | 错误预算政策已文档化 | |
| **监控系统** | 重要指标已显示在仪表盘上 | |
| **警报系统** | 警报机制已配置并能够触发警报 | |
| **日志记录** | 已实施结构化的日志记录系统 | |
| **事件响应流程** | 已建立完善的事件响应流程 | |
| **容量规划** | 系统已进行负载测试，确保能够承受预期峰值 | |
| **自动扩展机制** | 自动扩展功能已配置并经过测试 | |
| **资源限制** | 已设置资源使用限制（如CPU、内存） | |
| **系统弹性** | 已实现优雅降级机制 | |
| **容错机制** | 已设置断路器等容错措施 | |
| **恢复机制** | 设置了超时处理机制 | |
| **部署流程** | 部署流程已经过测试 | |
| **部署准备** | 部署流程已准备好，包括 Canary测试和蓝绿部署（Canary/Blue-Green Deployment） |
| **安全措施** | 已实施认证和授权机制 | |
| **数据安全** | 重要数据已妥善保管 | |
| **文档记录** | 代码结构和文档齐全 | |
| **运行手册** | 运维相关的运行手册已编写完成 | |

---

## 第十二阶段：高级实践

### 自动化修复机制

```yaml
auto_remediation:
  - trigger: "pod_crash_loop"
    condition: "restart_count > 3 in 10 min"
    action: "Delete pod, let scheduler reschedule"
    escalate_if: "Still crashing after 3 auto-remediations"
    
  - trigger: "disk_usage_high"
    condition: "disk_usage > 85%"
    action: "Run log cleanup script, archive old data"
    escalate_if: "Still above 85% after cleanup"
    
  - trigger: "connection_pool_exhausted"
    condition: "available_connections = 0"
    action: "Kill idle connections, increase pool temporarily"
    escalate_if: "Pool exhausted again within 1 hour"
    
  - trigger: "certificate_expiring"
    condition: "days_until_expiry < 14"
    action: "Trigger cert renewal"
    escalate_if: "Renewal fails"
```

### 多地区可靠性保障

| 方案 | 复杂程度 | 恢复时间（RTO, Recovery Time） | 成本 |
|----------|-----------|-----|------|
| 主动-被动模式 | 低 | 几分钟 | 1.5倍 |
| 主动-主动（读写模式） | 中等 | 几秒 | 1.8倍 |
| 主动-主动（全负载模式） | 高 | 接近零 | 2-3倍 |
| 基于单元格的分布式架构 | 非常高 | 每个单元格独立处理 | 2-4倍 |

**决策指南：**
- 如果SLO低于99.9%，可以选择主动-被动模式，并设置良好的备份机制 |
- 如果SLO在99.9%到99.95%之间，选择主动-主动模式，并设置自动故障转移机制 |
- 如果SLO高于99.95%，选择主动-主动（全负载）模式 |
- 如果SLO高于99.99%，选择基于单元格的分布式架构 |

### 可靠性文化指标

**健康指标：**
- 事后分析会议是无责备的，并且所有相关人员都会参与 |
- 错误预算得到严格遵守（避免过度优化导致系统性能下降） |
- 值班安排公平合理，并提供相应的补偿 |
- 工作量得到持续监控，并且每季度都有减少 |
- 定期进行混沌测试 |
- 团队对自己的可靠性负责（而不仅仅是SRE团队）

**警告信号：**
- 出现“英雄主义文化”——总是同一个人解决问题 |
- 事后分析会议只关注问题责任归属 |
- 错误预算被过度消耗，但系统性能没有改善 |
- 值班安排令人畏惧，总是同一批人值班 |
- 总是承诺“等这个功能上线后再解决可靠性问题” |
- SRE团队只是换个名字的运维团队而已

## 质量评估量表（0-100分）

| 评估维度 | 权重 | 0-2分 | 3-4分 | 5分 |
|--------|---------|-----|-----|---|
| 服务水平目标（SLO覆盖） | 20% | 未定义SLO | 关键服务有SLO | 所有服务都有SLO、错误预算和定期审查 |
| 监控系统 | 15% | 仅进行基本健康检查 | 有重要指标和仪表盘 | 全面可观测性，包括异常检测 |
| 事件响应 | 15% | 仅进行临时处理，没有系统化流程 | 有事件响应流程、角色分配、事后分析 | 有结构化的事件响应机制，无责备文化，问题有追踪记录 |
| 自动化 | 15% | 所有操作都手动完成 | 使用持续集成/持续交付（CI/CD），部分自动化 | 具有自愈能力，工作量低于25% |
| 混沌工程 | 10% | 无混沌测试 | 在测试环境中进行简单实验 | 在生产环境中进行持续的、有安全控制的混沌测试 |
| 容量规划 | 10% | 只进行反应式扩展 | 每季度进行预测性规划 | 使用预测性机制，实现自动扩展 |
| 值班安排 | 10% | 存在疲劳问题，依赖性高 | 轮班安排公平，每班次警报数量少于5页 |
| 文档记录 | 0分 | 没有文档记录 | 有事件响应流程 | 文档齐全，实时更新，经过测试 |

---

## 常用命令

- “评估[服务]的可靠性” → 运行成熟度评估 |
- “为[服务]定义服务水平目标（SLOs）” → 按照流程选择和设置SLOs |
- “检查[服务]的错误预算情况” → 计算当前的错误预算状况 |
- “为[问题描述]启动事件响应流程” → 创建事件处理流程，指派事件指挥官，开始处理 |
- “为[事件]生成事后分析报告” → 生成结构化的分析报告 |
- “为[服务]设计混沌实验” → 根据假设设计实验 |
- “评估[团队]的工作量” → 清理工作量，确定优先处理事项 |
- “审查值班安排的健康状况” | 分析警报数量、响应时间和满意度 |
- “进行[服务]的生产环境准备审查” | 完整执行检查清单 |
- “生成每月可靠性报告” | 生成全面的报告 |
- “为[警报类型]设计事件响应流程” | 创建结构化的事件响应流程 |
- “为[服务]的扩展需求制定容量规划” | 根据预测需求制定容量模型 |

---

这些文档涵盖了从系统设计到日常运营的各个方面，确保系统的可靠性、可扩展性和高效性。