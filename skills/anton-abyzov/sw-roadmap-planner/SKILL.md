---
name: roadmap-planner
description: 产品路线图与功能优先级制定专家，熟练运用 RICE、MoSCoW 和 Kano 策略框架。在制定产品路线图、确定各开发阶段的优先功能、定义成功指标（KPIs）时具备丰富的经验。擅长进行投资回报率（ROI）分析、与利益相关者沟通以及制定季度工作计划。
---

# 路线图规划器 - 战略产品规划

**目的**：为产品路线图、功能优先级框架、成功指标的定义以及与利益相关者的沟通提供专业指导。

**使用场景**：
- 规划产品路线图（季度、年度）
- 在多个开发阶段中优先处理功能
- 定义成功指标和关键绩效指标（KPI）
- 向利益相关者传达技术决策
- 分析投资回报率（ROI）和业务影响

---

## 功能优先级框架

### RICE评分法

**计算公式**：`RICE = (影响范围 × 影响程度 × 确信度) / 所需工作量`

**评分要素**：
- **影响范围**：该功能每个季度将影响多少用户/客户？
- **影响程度**：该功能对每个用户的影响有多大？（0.25 = 极小影响，0.5 = 低影响，1 = 中等影响，2 = 高影响，3 = 非常大影响）
- **确信度**：你对这些估计的信心有多高？（50% = 低信心，80% = 中等信心，100% = 高信心）
- **所需工作量**：实现该功能需要多少人周/月？

**示例**：
```
Feature: Real-time Collaboration
- Reach: 8000 users/quarter (80% of user base)
- Impact: 3 (Massive impact on user satisfaction)
- Confidence: 70% (some unknowns in WebSocket scalability)
- Effort: 8 person-weeks

RICE = (8000 × 3 × 0.7) / 8 = 2100

Higher RICE = Higher Priority
```

**适用场景**：
- 功能积压较多（50个以上功能）的情况
- 依赖数据驱动的产品团队
- 拥有大量用户群的B2C产品
- 需要客观比较不同功能的情况

**RICE评分表示例**：
```markdown
| Feature | Reach | Impact | Confidence | Effort | RICE Score | Priority |
|---------|-------|--------|------------|--------|------------|----------|
| Real-time Collaboration | 8000 | 3 | 70% | 8 | 2100 | P1 |
| Dark Mode | 6000 | 1 | 90% | 2 | 2700 | P1 |
| Advanced Search | 4000 | 2 | 60% | 6 | 800 | P2 |
| Mobile App | 10000 | 3 | 50% | 20 | 750 | P2 |
| AI Suggestions | 5000 | 2 | 40% | 12 | 333 | P3 |
```

---

### MoSCoW优先级排序法

**分类**：
- **必备功能**：对最小可行产品（MVP）至关重要，缺少这些功能会导致产品失败
  - 无法协商的要求
  - 法律/合规性要求
  - 核心价值主张

- **应具备功能**：虽然重要但非必需，有替代方案
  - 能显著提升产品价值
  - 必要时可以推迟实现
  - 用于提升用户体验

- **可选功能**：虽然有价值但非必需
  - 可选的功能
  - 实现难度较低
  - 用于优化产品细节

- **不会包含的功能**：超出当前版本范围的功能
  - 未来版本才会实现的功能
  - 用于解决技术遗留问题
  - 边缘性功能

**示例**：
```markdown
## Feature Prioritization (Q1 2026 MVP)

### Must Have (P1)
| Feature | Reason |
|---------|--------|
| User Authentication | Foundation for all other features, security requirement |
| Task CRUD Operations | Core value proposition, minimum viable product |
| Real-time Synchronization | Key differentiator vs competitors |

### Should Have (P2)
| Feature | Reason |
|---------|--------|
| File Attachments | Requested by 60% of beta users, improves collaboration |
| Task Comments | Team collaboration feature, workaround: use Slack |

### Could Have (P3)
| Feature | Reason |
|---------|--------|
| Dark Mode | UI polish, low effort, nice-to-have |
| Custom Themes | Requested by enterprise customers, can wait for v2 |

### Won't Have (This Release)
- Mobile apps (Q2 2026 roadmap)
- Advanced analytics dashboard (Q3 2026)
- API for third-party integrations (Q4 2026)
- Offline mode (technical complexity too high for MVP)
```

**适用场景**：
- MVP规划（重点关注“必备功能”）
- 敏捷开发冲刺（在时间范围内优先处理功能）
- 需要明确功能优先级的场景
- 资源有限的团队

---

### Kano模型

**分类**：
- **基本需求**（门槛属性）：
  - 用户默认期望具备的功能
  - 缺少这些功能会导致用户不满
  - 具备这些功能也不会显著提升用户满意度
  - 例如：身份验证、数据持久化、安全性

- **性能需求**（线性属性）：
  - 功能越多越好
  - 用户满意度随功能质量的提升而线性增加
  - 例如：速度、可靠性、系统稳定性、准确性

- **惊喜需求**（提升用户体验的功能）：
  - 超出用户预期的功能，能带来惊喜
  - 缺少这些功能不会导致用户不满
  - 具备这些功能能带来竞争优势
  - 例如：人工智能建议、美观的用户界面、贴心的设计细节

**示例分析**：
```markdown
## Kano Model Analysis: Task Management App

### Basic Needs (Must Work)
- User authentication (email/password)
- Create, read, update, delete tasks
- Data persistence (don't lose my tasks!)
- Secure data storage (HTTPS, encrypted)
- Basic search functionality

### Performance Needs (More is Better)
- **Speed**: Task creation < 100ms
- **Reliability**: 99.9% uptime SLA
- **Accuracy**: Search finds relevant tasks
- **Capacity**: Support 10K+ tasks per user
- **Responsiveness**: UI updates instantly

### Excitement Needs (Delighters)
- **AI-powered task suggestions**: "You might want to schedule a follow-up"
- **Beautiful, minimalist UI**: Thoughtful animations, delightful interactions
- **Smart reminders**: Context-aware notifications
- **Collaboration magic**: Seamless real-time updates
- **Voice input**: "Add task: Buy milk"
```

**适用场景**：
- 理解用户需求
- 与竞争对手区分产品差异
- 在“基本需求”和“惊喜需求”之间取得平衡
- 进行用户体验/产品设计决策

---

## 产品路线图制作

### 季度路线图模板

**结构**：主题 → 功能 → 成功指标

**示例**：
```markdown
# Product Roadmap 2026

## Q1 2026: Foundation (MVP)
**Theme**: Core Task Management
**Goal**: Launch with 100 beta users
**Team Focus**: Backend + Frontend (1:1 split)

### Features
- ✅ User Authentication (Weeks 1-2) - COMPLETED
  - Email/password login
  - Password reset flow
  - Session management

- ✅ Task CRUD Operations (Weeks 3-4) - COMPLETED
  - Create, read, update, delete tasks
  - Task properties: title, description, due date, priority
  - Basic filtering and sorting

- 🔄 Real-time Synchronization (Weeks 5-7) - IN PROGRESS
  - WebSocket-based live updates
  - Conflict resolution (Operational Transform)
  - Offline queue with sync on reconnect

- ⏳ File Attachments (Weeks 8-9) - PLANNED
  - Upload files (images, PDFs, docs)
  - S3 storage integration
  - Virus scanning

- ⏳ Beta Launch (Week 10) - PLANNED
  - Onboarding flow
  - User feedback mechanism
  - Analytics instrumentation

### Success Metrics
- **User Acquisition**: 100 active beta users
- **Engagement**: >70% weekly active usage
- **Performance**: <5 min average onboarding time
- **Quality**: <5 critical bugs reported per week

### Risks & Mitigations
- **Risk**: WebSocket scalability issues at 100 concurrent users
  - **Mitigation**: Load testing with 200 users, fallback to polling
- **Risk**: Low beta signups
  - **Mitigation**: ProductHunt launch, Reddit outreach

---

## Q2 2026: Collaboration
**Theme**: Team Features
**Goal**: 1K paying customers, $50K MRR
**Team Focus**: Backend + Frontend + Mobile (2:2:1 split)

### Features
- Team workspaces (multi-tenant architecture)
- Role-based permissions (owner, admin, member, viewer)
- Task comments and @mentions
- Activity feeds (real-time notifications)
- Mobile apps (iOS/Android React Native)

### Success Metrics
- **Revenue**: $50K MRR (avg $5/user/month)
- **Growth**: 1K paying customers
- **Retention**: <2% monthly churn rate
- **Activation**: 60% of signups create a team within 7 days

---

## Q3 2026: Integrations
**Theme**: Workflow Automation
**Goal**: 5K customers, $200K MRR

### Features
- Slack integration (notifications, create tasks from Slack)
- GitHub integration (link tasks to PRs, auto-close on merge)
- Zapier webhooks (connect to 3000+ apps)
- Public API for third-party apps (REST + GraphQL)
- Workflow automation (IFTTT-style rules)

### Success Metrics
- **Integration Adoption**: 40% of teams use at least one integration
- **API Usage**: 500K API calls/month
- **Revenue**: $200K MRR
- **NPS**: >50 (promoters significantly outnumber detractors)

---

## Q4 2026: Enterprise
**Theme**: Scale & Compliance
**Goal**: 10K customers, $500K MRR

### Features
- SSO (SAML, OAuth for enterprise)
- Advanced permissions (custom roles, granular ACLs)
- Audit logs (compliance requirements)
- SOC 2 Type II compliance
- Custom SLAs for enterprise customers

### Success Metrics
- **Enterprise Customers**: 50 companies (>100 seats each)
- **Revenue**: $500K MRR ($200K from enterprise tier)
- **Compliance**: SOC 2 Type II certification
- **Uptime**: 99.99% SLA for enterprise tier
```

---

## 成功指标与关键绩效指标（KPIs）

### OKRs（目标与关键结果）框架

**示例**：
```yaml
objective: "Become the #1 task management tool for remote teams"

key_results:
  KR1:
    metric: "Daily Active Users (DAU)"
    target: "70% of registered users"
    measurement: "Track unique logins per day (Mixpanel)"
    current: "52%"
    target_date: "2026-Q2"

  KR2:
    metric: "Feature Adoption - Real-time Collaboration"
    target: "50% of teams use real-time editing within first week"
    measurement: "Track WebSocket connections per team"
    current: "0% (feature not launched)"
    target_date: "2026-Q1"

  KR3:
    metric: "Customer Satisfaction (NPS)"
    target: "NPS > 40"
    measurement: "In-app survey after 1 week of use"
    current: "28"
    target_date: "2026-Q3"

  KR4:
    metric: "Revenue Growth"
    target: "$200K MRR by end of Q3"
    measurement: "Stripe dashboard (MRR)"
    current: "$15K MRR"
    target_date: "2026-Q3"
```

### 指标分类

**用户参与度指标**：
- 日活跃用户（DAU）
- 周活跃用户（WAU）
- 月活跃用户（MAU）
- DAU/MAU比率（用户粘性）
- 会话时长
- 功能采用率

**性能指标**：
- API响应时间（50%分位数、95%分位数、99%分位数）
- 页面加载时间（< 2秒）
- 数据同步延迟（< 100毫秒）
- 错误率（< 0.1%）
- 系统可用性SLA（99.9% → 99.99%）

**业务指标**：
- 月度经常性收入（MRR）
- 客户获取成本（CAC）
- 客户生命周期价值（LTV）
- LTV与CAC比率（应大于3:1）
- 客户流失率（每月< 2%）
- 客户推荐评分（NPS）

**示例测量计划**：
```markdown
## Measurement Plan: Real-time Collaboration Feature

### Instrumentation
1. **Analytics Events** (Mixpanel/Amplitude)
   - `collaboration_session_started`
   - `collaboration_edit_made`
   - `collaboration_conflict_resolved`
   - `collaboration_session_ended`

2. **Performance Monitoring** (Grafana/Datadog)
   - WebSocket connection metrics
   - Message round-trip latency (p50, p95, p99)
   - Concurrent user count per workspace
   - Operational Transform conflict rate

3. **User Feedback** (In-app surveys)
   - NPS survey after 1 week of use
   - "How would you rate the real-time collaboration feature?" (1-5 stars)
   - "What could we improve?"

### Success Criteria (Go/No-Go Decision)
- ✅ **PASS**: 50%+ teams adopt feature within 1 week
- ✅ **PASS**: p95 latency < 200ms
- ✅ **PASS**: < 1% conflict rate requiring manual merge
- ✅ **PASS**: NPS improvement of +10 points

- ❌ **FAIL**: Adoption < 30% after 2 weeks → Investigate UX issues
- ❌ **FAIL**: p95 latency > 500ms → Performance optimization required
```

---

## 与利益相关者的沟通

### 将技术细节转化为业务影响

**输入**：技术架构决策
**输出**：易于理解的业务解释及投资回报率（ROI）

**示例**：
```markdown
## Stakeholder Update: Microservices Architecture Migration

### Executive Summary
We're proposing a shift from our current monolithic architecture to microservices. This is a significant technical change that will deliver measurable business benefits.

### Business Impact Summary

**Benefits**:

1. **Faster Feature Delivery** (30% improvement)
   - **Current**: Teams block each other, 3-week average time-to-market
   - **Future**: Teams work independently, 2-week average time-to-market
   - **Impact**: Ship features 33% faster, respond to customer requests quicker
   - **Revenue Impact**: Faster iteration → better product-market fit → higher conversion

2. **Better Scalability** (2x cost efficiency)
   - **Current**: Scale entire system even if only one feature needs it ($100K/year infrastructure)
   - **Future**: Scale only the parts that need it ($50K/year infrastructure)
   - **Impact**: Save $50K/year in AWS costs
   - **Example**: During Black Friday, scale only payment service, not entire app

3. **Reduced Risk** (99.9% → 99.99% uptime)
   - **Current**: If one service fails, entire app goes down (8 hours downtime/year)
   - **Future**: If one service fails, others keep running (1 hour downtime/year)
   - **Impact**: 7 hours less downtime = $200K revenue protected
   - **Customer Trust**: Fewer incidents = better reputation

**Costs**:
- **Engineering Time**: 8 weeks of dedicated migration work
- **New Tools**: +$5K/year for monitoring and orchestration (Kubernetes, Datadog)
- **Short-term Risk**: Temporary productivity dip during migration

**ROI Analysis**:
- **Costs**: $150K (8 weeks × 3 engineers × $75K salary + $5K tools)
- **Benefits Year 1**: $250K ($50K infra savings + $200K revenue protection)
- **Net Benefit Year 1**: $100K
- **Break-even**: 6 months
- **Payback Period**: 18 months for 3x ROI

**Recommendation**: Approve for Q3 implementation
**Timeline**: 8 weeks (Q3 2026)
**Team**: 3 backend engineers, 1 DevOps engineer
**Risk Level**: Medium (well-established pattern, many success stories)
```

---

## 与SpecWeave的集成

**产品经理（PM）应何时使用路线图规划器**：
- 当用户询问“我们应该优先处理哪些功能？”时
- 当用户提到“路线图”、“RICE评分法”、“MoSCoW优先级排序法”或“Kano模型”时
- 当用户需要制定季度规划或功能排名时

**产品经理的工作流程**：
1. 收集功能需求（来自用户、功能积压列表或利益相关者）
2. 将需求委托给路线图规划器进行优先级排序
3. 呈现排序后的路线图及理由
4. 为“必备功能”制定优先级最高的开发计划（P1阶段）
5. 将“次要功能”推迟到后续开发阶段（P2/P3阶段）

---

## 相关技能**：
- **产品经理（PM）**：使用路线图规划器进行战略规划
- **开发计划员**：根据路线图执行具体功能开发
- **需求文档生成器**：为优先级高的功能生成详细的技术规范

---

## 版本历史记录

- **v1.0.0**（2025-11-21）：初始版本，为提高模块化程度而从产品经理工具中分离出来