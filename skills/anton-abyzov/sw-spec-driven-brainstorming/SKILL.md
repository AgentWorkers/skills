---
name: spec-driven-brainstorming
description: **专家级技能：以规范为导向的头脑风暴与产品发现**  
擅长协助团队构思产品功能、分解大型项目任务、开展故事地图绘制会议（story mapping），并运用MoSCoW/RICE/Kano等方法进行任务优先级排序。同时，通过精益创业（lean startup）的思维方式验证各种创意的可行性。具备丰富的经验，能够有效推动头脑风暴、产品探索、功能规划、优先级确定等流程的顺利进行。  

**核心能力涵盖：**  
- **头脑风暴与创意生成**：引导团队高效产生新想法  
- **产品需求分析**：深入理解用户需求，明确产品功能  
- **任务分解与规划**：将复杂项目拆解为可管理的任务  
- **优先级评估**：运用科学方法（如MoSCoW/RICE/Kano）确定任务的优先级  
- **精益创业方法**：应用精益创业理念优化项目流程  
- **产品 backlog 管理**：有效管理产品待办事项列表  
- **MVP（最小可行产品）设计**：快速构建可测试的初步产品版本  

**适用场景：**  
- 产品开发团队  
- 创新项目团队  
- 软件设计团队  

**专业工具与方法：**  
- MoSCoW/RICE/Kano 等优先级评估工具  
- Lean Startup 方法论  
- Story Mapping 技术  
- Agile 开发框架  

**服务目标：**  
- 提升团队创新效率  
- 帮助团队明确产品方向  
- 优化项目执行流程  

**经验总结：**  
- 在多家科技公司担任产品经理和敏捷开发团队负责人，负责多个软件产品的规划与实施  
- 深谙产品开发中的关键流程与工具  
- 擅长通过技术手段解决实际问题，推动团队达成项目目标
---

# 规范驱动的头脑风暴技巧  
（Spec-Driven Brainstorming Skills）  

作为产品发现、功能构思及规范驱动的头脑风暴技术的专家，我擅长帮助团队通过结构化的引导方法，将模糊的想法转化为具体、明确的规范。  

## 核心引导技巧（Core Facilitation Techniques）  

### 1. 用户故事映射（User Story Mapping）  
**目的**：可视化用户旅程，并识别每个环节中能带来价值的特性。  
**流程**：  
```
Step 1: Define User Activities (horizontal backbone)
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ Discover     │ Browse       │ Purchase     │ Receive      │
│ Products     │ & Compare    │ & Checkout   │ & Review     │
└──────────────┴──────────────┴──────────────┴──────────────┘

Step 2: Break down into User Tasks (vertical slices)
Discover Products:
├─ Search by keyword
├─ Filter by category
├─ View trending products
└─ Get personalized recommendations

Browse & Compare:
├─ View product details
├─ Read reviews
├─ Compare products side-by-side
└─ Save to wishlist

Purchase & Checkout:
├─ Add to cart
├─ Apply discount code
├─ Select shipping method
└─ Enter payment info

Step 3: Prioritize by Walking Skeleton (MVP = top row)
┌────────────────────────────────────────────────────────┐
│ MVP (Release 1): Walking Skeleton                      │
├────────────────────────────────────────────────────────┤
│ Search → View Details → Add to Cart → Checkout        │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Release 2: Enhanced Discovery                          │
├────────────────────────────────────────────────────────┤
│ Filters, Trending, Recommendations, Reviews            │
└────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Release 3: Advanced Features                           │
├────────────────────────────────────────────────────────┤
│ Wishlist, Compare, Discount Codes, Saved Payments     │
└────────────────────────────────────────────────────────┘
```  
**输出**：根据用户旅程优先排序的特性列表。  

### 2. 事件风暴（Event Storming）  
**目的**：通过协作建模来发现业务事件和业务流程。  
**流程**：  
```markdown
## Event Storming Workflow

### Step 1: Identify Domain Events (orange sticky notes)
- OrderPlaced
- PaymentProcessed
- OrderShipped
- OrderDelivered
- OrderCancelled

### Step 2: Identify Commands (blue sticky notes)
- PlaceOrder
- ProcessPayment
- ShipOrder
- CancelOrder

### Step 3: Identify Aggregates (yellow sticky notes)
- Order (handles PlaceOrder, CancelOrder)
- Payment (handles ProcessPayment)
- Shipment (handles ShipOrder)

### Step 4: Identify External Systems (pink sticky notes)
- PaymentGateway (Stripe)
- ShippingProvider (FedEx API)
- InventorySystem

### Step 5: Identify Policies (purple sticky notes)
- WHEN OrderPlaced THEN ProcessPayment
- WHEN PaymentProcessed THEN ReserveInventory
- WHEN InventoryReserved THEN ShipOrder
- WHEN OrderCancelled AND PaymentProcessed THEN RefundPayment
```  
**输出**：业务流程的可视化图表及相关边界。  

### 3. 影响映射（Impact Mapping）  
**目的**：通过用户影响将业务目标与具体特性联系起来。  
**流程**：  
```
GOAL: Increase revenue by 20% in Q2

WHY? (Impact)
├─ Increase conversion rate (5% → 8%)
│  ├─ WHO? (Actors)
│  │  ├─ New visitors
│  │  └─ Returning customers
│  ├─ HOW? (Features)
│  │  ├─ Simplify checkout (1-click purchase)
│  │  ├─ Add product recommendations
│  │  └─ Offer guest checkout
│  └─ WHAT? (Deliverables)
│     ├─ US-001: 1-click checkout for logged-in users
│     ├─ US-002: ML-based product recommendations
│     └─ US-003: Guest checkout flow
│
├─ Increase average order value ($50 → $65)
│  ├─ WHO? (Actors)
│  │  └─ Existing customers
│  ├─ HOW? (Features)
│  │  ├─ Bundle discounts (buy 3, get 10% off)
│  │  ├─ Free shipping threshold ($75+)
│  │  └─ Upsell related products
│  └─ WHAT? (Deliverables)
│     ├─ US-004: Bundle discount engine
│     ├─ US-005: Dynamic shipping calculator
│     └─ US-006: Related product suggestions
│
└─ Reduce cart abandonment (40% → 25%)
   ├─ WHO? (Actors)
   │  └─ Users with items in cart
   ├─ HOW? (Features)
   │  ├─ Cart abandonment emails
   │  ├─ Save cart across devices
   │  └─ Show trust signals (reviews, secure badges)
   └─ WHAT? (Deliverables)
      ├─ US-007: Automated cart recovery emails
      ├─ US-008: Persistent cart sync
      └─ US-009: Trust badge UI components
```  
**输出**：与业务成果直接相关的特性列表。  

## 优先级框架（Priority Frameworks）  

### 1. MoSCoW 方法  
**定义**：将特性分为“必须实现（Must）”、“应该实现（Should）”、“可以尝试（Could）”和“不会实现（Won’t）”三类。  
**适用场景**：MVP（最小可行产品）范围定义、时间限制的发布计划。  

### 2. RICE 评分（Reach, Impact, Confidence, Effort）  
**公式**：`RICE 评分 = (达成度 × 影响力 × 信心) / 工作量`  
**适用场景**：基于数据的优先级排序、路线图规划。  

### 3. Kano 模型  
**分类**：  
- **基本需求（Must-be）**：缺失会导致不满，存在也不会带来额外惊喜；  
- **性能需求（One-dimensional）**：数量越多越好（线性满意度）；  
- **兴奋需求（Delighters）**：缺失不会造成负面影响，存在会带来愉悦感。  
**适用场景**：理解客户满意度驱动因素、制定差异化策略。  

## 精益创业验证（Lean Startup Validation）  

### 1. 构建-测量-学习循环（Build-Measure-Learn Loop）  
```markdown
## Hypothesis Testing: Feature X

### BUILD
**Hypothesis**: Adding product recommendations will increase average order value by 15%.

**Minimum Viable Test**:
- Implement simple "Customers also bought" section
- Show on 50% of product pages (A/B test)
- Track: clicks, add-to-cart rate, order value

**Effort**: 1 week (backend + frontend)

### MEASURE
**Metrics to Track**:
- Click-through rate on recommendations
- Add-to-cart conversion from recommendations
- Average order value (treatment vs control)
- Revenue per visitor

**Success Criteria**:
- CTR > 5%
- AOV increase > 10%
- Statistical significance (p < 0.05)

**Data Collection Period**: 2 weeks (minimum 10,000 visitors)

### LEARN
**Scenario A: Hypothesis Validated**
- AOV increased 18% (exceeded target!)
- CTR on recommendations: 12%
- **Action**: Roll out to 100%, invest in ML-based recommendations

**Scenario B: Hypothesis Rejected**
- AOV increased 2% (below target)
- CTR on recommendations: 1% (low engagement)
- **Action**: Pivot - test alternative hypothesis (e.g., bundle discounts)

**Scenario C: Mixed Results**
- AOV increased 12% (close to target)
- High CTR but low conversion
- **Action**: Iterate - improve recommendation quality (ML model)
```  
### 2. MVP 定义框架（MVP Definition Canvas）  
```markdown
## MVP Canvas: Task Management SaaS

### Target Users
- Solo freelancers and small teams (2-5 people)
- Knowledge workers (designers, developers, writers)
- Currently using: Spreadsheets, Trello, Notion

### Problem Being Solved
- Task prioritization is manual and time-consuming
- No visibility into blockers and dependencies
- Team collaboration requires constant status updates

### Unique Value Proposition
Auto-prioritized task list using AI + team workload balancing.

### MVP Features (Walking Skeleton)
**Core Flow**: Create task → AI prioritizes → Assign → Complete

**Must-Have Features**:
- [ ] Task creation (title, description, due date)
- [ ] AI prioritization (urgency + importance algorithm)
- [ ] Task assignment to team members
- [ ] Task status updates (To Do, In Progress, Done)
- [ ] Team dashboard (workload overview)

**NOT in MVP**:
- ❌ Time tracking
- ❌ Custom workflows
- ❌ Integrations (Slack, GitHub)
- ❌ Mobile app
- ❌ Advanced reporting

### Success Metrics
- **Activation**: 70% of signups create 3+ tasks in first week
- **Retention**: 40% weekly active users (WAU) after 4 weeks
- **Engagement**: Average 5 tasks completed/week per user

### Risks & Assumptions
- **Assumption**: Users trust AI prioritization
  - **Test**: Survey 50 users after 2 weeks, ask "Do you trust the priority scores?"
- **Risk**: AI prioritization is inaccurate
  - **Mitigation**: Manual override, feedback loop to improve model
- **Assumption**: Teams of 2-5 are willing to pay $10/user/month
  - **Test**: Offer paid tier after 2-week trial, track conversion rate
```  

## 头脑风暴技巧（Brainstorming Techniques）  

### 1. 疯狂8秒（Crazy 8s）  
**流程**：8分钟内完成8个草图（每个想法1分钟）。  
**适用场景**：快速生成大量创意。  

### 2. 六顶思考帽（Six Thinking Hats）  
**目的**：从不同角度探索问题。  
**适用场景**：激发创新思维。  

### 3. “我们如何实现……”（How Might We, HMW）问题  
**目的**：将问题重新定义为机会。  
**适用场景**：促进问题解决的创新思路。  

## 特性分解模板（Feature Breakdown Templates）  
**流程**：从“史诗级任务（Epic）”分解为“特性（Features）”，再细化为“用户故事（User Stories）”。  
**模板示例**：  
```markdown
## Epic: User Onboarding Experience

### Feature 1: Account Creation
**User Story US-001**: Email/Password Registration
- **As a** new user
- **I want to** create an account with email/password
- **So that** I can access personalized features

**Acceptance Criteria**:
- Email validation (RFC 5322 format)
- Password complexity (8+ chars, 1 uppercase, 1 number, 1 special)
- Duplicate email detection
- Verification email sent within 5 minutes

**User Story US-002**: Social Login (Google, GitHub)
- **As a** new user
- **I want to** sign up with my Google/GitHub account
- **So that** I don't have to remember another password

**Acceptance Criteria**:
- OAuth 2.0 integration
- Consent screen shown
- Email auto-verified for social logins

### Feature 2: Profile Setup
**User Story US-003**: Basic Profile Information
- **As a** new user
- **I want to** set my display name and avatar
- **So that** other users can recognize me

**User Story US-004**: Preferences Configuration
- **As a** new user
- **I want to** configure notification preferences
- **So that** I only receive relevant updates

### Feature 3: Guided Tour
**User Story US-005**: Interactive Product Tour
- **As a** first-time user
- **I want** a guided tour of key features
- **So that** I understand how to use the product

**User Story US-006**: Sample Data Pre-population
- **As a** new user
- **I want** sample data to explore
- **So that** I can try features without manual setup
```  

## 协作工作坊形式（Collaborative Workshop Formats）  

### 1. 远程头脑风暴（Miro/FigJam）  
**议程**（90分钟）：  
```
00:00 - 00:10  Introduction & Problem Statement
00:10 - 00:25  Individual Ideation (silent brainstorming)
00:25 - 00:45  Group Sharing (2 min per person)
00:45 - 01:00  Affinity Grouping (cluster similar ideas)
01:00 - 01:15  Dot Voting (3 votes per person)
01:15 - 01:30  Discussion & Action Items
```  
**工具**：  
- Miro 画布及相关模板  
- 用于时间控制的计时器  
- 匿名投票工具  

### 2. 设计冲刺（Design Sprint，5天流程）  
**流程**：  
```
Day 1: Map (Understand the problem)
- User journey mapping
- Identify pain points
- Set sprint goal

Day 2: Sketch (Diverge - generate ideas)
- Crazy 8s
- Solution sketches
- Silent critique

Day 3: Decide (Converge - choose solution)
- Dot voting
- Storyboard creation
- Prototype plan

Day 4: Prototype (Build realistic facade)
- High-fidelity mockup
- Interactive prototype (Figma)
- Test script preparation

Day 5: Test (Validate with users)
- 5 user interviews
- Record findings
- Decide: build, iterate, or pivot
```  

## 输出模板（Output Templates）  
### 头脑风暴会议总结（Brainstorming Session Summary）  
```markdown
# Brainstorming Session: [Topic]

**Date**: 2024-01-15
**Participants**: Alice (PM), Bob (Eng), Carol (Design)
**Facilitator**: Alice

## Problem Statement
Users are abandoning checkout at 40% rate (industry avg: 25%).

## Ideas Generated (22 total)

### High Priority (Top 5 by voting)
1. **1-Click Checkout** (8 votes)
   - Rationale: Removes friction for returning users
   - Effort: 2 weeks
   - Impact: Est. 10% reduction in abandonment

2. **Guest Checkout** (7 votes)
   - Rationale: 30% of users don't want accounts
   - Effort: 1 week
   - Impact: Est. 8% reduction in abandonment

3. **Progress Indicator** (6 votes)
   - Rationale: Reduces anxiety about form length
   - Effort: 2 days
   - Impact: Est. 3% reduction in abandonment

4. **Autofill Address** (5 votes)
   - Rationale: Saves time, reduces errors
   - Effort: 1 week (Google Places API)
   - Impact: Est. 5% reduction in abandonment

5. **Save Cart for Later** (4 votes)
   - Rationale: Users can return without starting over
   - Effort: 3 days
   - Impact: Est. 4% recovery of abandoned carts

### Medium Priority (Parking Lot)
- Buy Now Pay Later integration
- Live chat support during checkout
- Trust badges (SSL, money-back guarantee)

### Deferred (Low ROI or High Risk)
- Voice checkout (too experimental)
- AR try-on (out of scope)

## Action Items
- [ ] Alice: Create specs for Top 3 (1-Click, Guest, Progress)
- [ ] Bob: Technical feasibility assessment (3 days)
- [ ] Carol: Mockups for guest checkout flow (5 days)
- [ ] Team: Review specs on Friday standup

## Next Session
- Date: 2024-01-22
- Topic: Refine top 3 ideas into user stories
```  

## 最佳实践（Best Practices）  

### 1. 为所有环节设定时间限制：  
- 构思环节：最多10-15分钟  
- 讨论环节：每个想法5分钟  
- 投票环节：2分钟  

### 2. 先发散再收敛：  
- 先产生大量想法（禁止批评）  
- 后再评估质量（通过结构化投票）  

### 3. 采用可视化方式：  
- 草图优于文字  
- 白板优于文档  
- 原型优于详细规范  

### 4. 包括多元视角：  
- 工程可行性  
- 设计可用性  
- 产品业务价值  
- 客户支持（用户痛点）  

### 5. 记录决策过程：  
- 为什么选择A而非B？  
- 我们做了哪些假设？  
- 我们将如何衡量结果？  

## 参考资源（Resources）  
- [用户故事映射 - Jeff Patton](https://www.jpattonassociates.com/user-story-mapping/)  
- [影响映射 - Gojko Adzic](https://www.impactmapping.org/)  
- [设计冲刺 - Google Ventures](https://www.gv.com/sprint/)  
- [Kano 模型分析](https://en.wikipedia.org/wiki/Kano_model)  

## 常见咨询问题（Activation Questions）：  
- “如何组织一场头脑风暴会议？”  
- “如何使用用户故事映射进行产品发现？”  
- “优先级框架有哪些（MoSCoW、RICE、Kano）？”  
- “如何将大型项目分解为具体特性？”  
- “精益创业的验证方法有哪些？”  
- “MVP的定义和范围界定？”  
- “如何进行特性优先级排序？”  
- “设计冲刺的引导技巧有哪些？”  
- “如何为产品路线图制定影响映射？”