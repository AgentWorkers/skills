# 知识管理系统

> 将部落知识转化为可搜索、可维护的组织智慧。防止人员离职时导致专业知识流失。

## 第一阶段：知识审计

### 当前状态评估

对每个维度评分1-5分（1=不存在，5=优秀）：

| 维度 | 评分 | 依据 |
|-----------|-------|----------|
| 文档覆盖范围 | | 已记录的流程百分比 |
| 可查找性 | | 新员工能否在5分钟内找到答案？ |
| 时效性 | | 过去6个月内更新的文档百分比 |
| 贡献文化 | | 积极贡献的团队成员百分比 |
| 新员工入职效果 | | 新员工达到生产力的时间 |
| 知识保留 | | 人员离职时的影响 |
| 跨团队共享 | | 团队能否访问其他团队的知识 |

**总分：___/35**

**解读：**
- 28-35分：成熟 — 需要优化和维护 |
- 21-27分：发展中 — 需要系统地填补空白 |
- 14-20分：基础水平 — 需要基础工作 |
- 7-13分：危急 — 知识面临风险 |

### 知识风险登记

```yaml
knowledge_risk:
  single_points_of_failure:
    - person: "[Name]"
      unique_knowledge: "[What only they know]"
      risk_if_leaves: "high|medium|low"
      extraction_priority: 1
      extraction_method: "interview|shadowing|recording|pair-work"
  
  undocumented_processes:
    - process: "[Name]"
      frequency: "daily|weekly|monthly|quarterly"
      complexity: "high|medium|low"
      current_owner: "[Name]"
      documentation_priority: 1
  
  tribal_knowledge:
    - topic: "[What people 'just know']"
      holders: ["[Name1]", "[Name2]"]
      impact_area: "[What breaks without it]"
      capture_method: "interview|workshop|write-up"
```

### 知识提取访谈指南

对于每个存在知识缺失的成员：

1. **背景**：“我正在记录[X]，这样团队就不会依赖任何一个人。这也能保护你——减少干扰。”
2. **流程演示**：“从头到尾跟我讲解[X]，我会记录下来。”
3. **决策点**：“你在哪些环节做出判断？考虑了哪些因素？”
4. **特殊情况**：“会出现哪些奇怪的情况？你如何处理？”
5. **工具与访问权限**：“你需要哪些工具、凭证或访问权限？”
6. **历史背景**：“为什么这样做？之前尝试过什么方法？”
7. **常见错误**：“哪些地方容易出错？”

**输出格式**：编写成操作手册（参见第三阶段的模板）。

---

## 第二阶段：知识架构

### 分类法设计

```yaml
knowledge_taxonomy:
  # Level 1: Knowledge Types
  types:
    how_to:
      description: "Step-by-step procedures and guides"
      examples: ["Deploy to production", "Process a refund", "Set up dev environment"]
      template: "runbook"
      
    reference:
      description: "Facts, specs, configurations to look up"
      examples: ["API endpoints", "Config values", "Vendor contacts", "Pricing tables"]
      template: "reference_doc"
      
    explanation:
      description: "Why things work the way they do"
      examples: ["Architecture decisions", "Policy rationale", "Historical context"]
      template: "explainer"
      
    decision:
      description: "How to make specific judgment calls"
      examples: ["Escalation criteria", "Approval thresholds", "Priority frameworks"]
      template: "decision_tree"
      
    troubleshooting:
      description: "Diagnosis and fix for known problems"
      examples: ["Error codes", "Common failures", "Debug procedures"]
      template: "troubleshooting_guide"

  # Level 2: Domains (customize per org)
  domains:
    - engineering
    - product
    - sales
    - operations
    - finance
    - hr_people
    - customer_success
    - security
    - legal_compliance

  # Level 3: Topics (within each domain)
  # Example for engineering:
  engineering_topics:
    - architecture
    - deployment
    - monitoring
    - incident_response
    - development_workflow
    - testing
    - security
    - infrastructure
```

### 信息架构规则

1. **最多3层深度** — 如果更深，请重新组织
2. **每个主题只有一个官方文档** — 避免重复
3. **每个页面都有负责人** — 避免文档无人管理
4. **每个页面都有更新日期** — 在6个月内被审核或标记为过时
5. **通过引用避免重复** — “参见[X]”比直接复制更好
6. **以搜索为主的设计** — 假设人们会搜索，而不是浏览

### 命名规范

```
[DOMAIN]-[TYPE]-[TOPIC]-[SPECIFICS]

Examples:
eng-howto-deploy-production
eng-ref-api-endpoints-v3
sales-decision-pricing-enterprise
ops-troubleshoot-billing-failed-charges
product-explain-auth-architecture
```

### 导航结构

```yaml
knowledge_base:
  homepage:
    - quick_links:  # Top 10 most-accessed pages
    - recently_updated:  # Last 10 changes
    - needs_review:  # Stale docs flagged
    
  by_audience:
    new_hire: "[Onboarding path → essential reading list]"
    engineer: "[Dev setup → architecture → deployment → debugging]"
    manager: "[Policies → processes → templates → reports]"
    customer_facing: "[Product knowledge → troubleshooting → escalation]"
    
  by_domain: "[Taxonomy Level 2 domains]"
  by_type: "[How-to | Reference | Explanations | Decisions | Troubleshooting]"
```

---

## 第三阶段：文档模板

### 操作手册模板（如何操作）

```markdown
# [Title]: [Action verb] + [Object]

**Owner:** [Name]  
**Last verified:** [YYYY-MM-DD]  
**Estimated time:** [X minutes]  
**Difficulty:** Easy | Medium | Advanced  

## Prerequisites
- [ ] [Access/tool/permission needed]
- [ ] [Knowledge assumed]

## Steps

### 1. [First action]
[Specific instruction with exact commands, clicks, or actions]

> ⚠️ [Warning about common mistake at this step]

### 2. [Second action]
[Instructions]

**Expected result:** [What you should see/get]

### 3. [Continue...]

## Verification
- [ ] [How to confirm it worked]
- [ ] [What to check]

## Troubleshooting
| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| [Symptom] | [Why] | [Steps] |

## Related
- [Link to related runbook]
- [Link to reference doc]
```

### 参考文档模板

```markdown
# [Subject] Reference

**Owner:** [Name]  
**Last verified:** [YYYY-MM-DD]  
**Scope:** [What this covers and doesn't cover]

## Overview
[1-2 sentence summary of what this reference contains]

## [Main content organized as tables, lists, or structured data]

| Item | Value | Notes |
|------|-------|-------|
| | | |

## Quick Lookup
[Most frequently needed items at the top]

## Change Log
| Date | Change | By |
|------|--------|-----|
| | | |
```

### 架构决策记录（ADR）

```markdown
# ADR-[NNN]: [Title]

**Status:** Proposed | Accepted | Deprecated | Superseded by ADR-[NNN]  
**Date:** [YYYY-MM-DD]  
**Deciders:** [Names]  

## Context
[What situation or problem prompted this decision?]

## Decision
[What was decided and why?]

## Alternatives Considered
| Option | Pros | Cons | Why rejected |
|--------|------|------|-------------|
| [A] | | | |
| [B] | | | |

## Consequences
- **Positive:** [Benefits]
- **Negative:** [Tradeoffs accepted]
- **Risks:** [What could go wrong]

## Review Date
[When should this be revisited?]
```

### 故障排除指南模板

```markdown
# Troubleshooting: [System/Process Name]

**Owner:** [Name]  
**Last verified:** [YYYY-MM-DD]

## Quick Diagnostic

```
[流程图（文本形式）]
[X] 发生了吗？
  → 是：转到问题A
  → 否：[Y] 发生了吗？
    → 是：转到问题B
    → 否：转到问题C
```

## Problem A: [Symptom Description]

**Likely causes (in order of probability):**
1. [Most common cause]
2. [Second most common]
3. [Rare but possible]

**Fix for Cause 1:**
[Step-by-step resolution]

**Fix for Cause 2:**
[Step-by-step resolution]

**Escalation:** If none of the above work → [who to contact, what info to provide]

## Problem B: [Next symptom]
[Same structure]
```

### 决策树模板

```markdown
# Decision Guide: [Topic]

**Owner:** [Name]  
**Last verified:** [YYYY-MM-DD]

## When to use this guide
[Situation that triggers this decision]

## Decision Flow

### Step 1: [First question]
- **If [condition A]** → [Action/next step]
- **If [condition B]** → [Action/next step]
- **If unsure** → [Default action or escalation]

### Step 2: [Second question based on Step 1 answer]
[Continue branching]

## Override conditions
[When to ignore this guide and escalate instead]

## Examples
| Scenario | Decision | Reasoning |
|----------|----------|-----------|
| [Real example] | [What was decided] | [Why] |
```

---

## 第四阶段：贡献系统

### 编写标准

**4C测试**（每份文档都必须满足以下四个标准）：
1. **清晰** — 新员工能理解吗？避免使用未经定义的术语。
2. **正确** — 是否经过验证或测试？不是凭记忆编写。
3. **最新** — 是否反映了当前的工作方式？不是6个月前的情况。
4. **简洁** — 是否可以删减内容而不影响意义？如果可以，就删减。

**格式规则：**
- 标题：以行动为导向（例如“部署到生产环境”而不是“Production Deployment”）
- 步骤：编号，每个步骤只描述一个动作，使用祈使句
- 警告：在步骤前标注（而不是之后）
- 代码/命令：准确无误，可直接复制，且经过测试
- 屏幕截图：仅在必要时使用（否则会很快过时）
- 链接：指向官方来源，不要直接粘贴完整的URL

### 贡献工作流程

```yaml
contribution_workflow:
  create:
    trigger: "New knowledge identified (incident learnings, process change, new tool)"
    steps:
      - choose_template: "Match content type to template"
      - draft: "Write using template structure"
      - self_review: "Run 4C Test checklist"
      - peer_review: "SME validates accuracy"
      - publish: "Add to knowledge base in correct location"
      - announce: "Notify relevant teams/channels"
    
  update:
    trigger: "Existing doc is wrong, incomplete, or stale"
    steps:
      - flag: "Mark as needs-update with reason"
      - update: "Make changes, update 'Last verified' date"
      - review: "If significant change, get peer review"
      - publish: "Update in place"
      - notify: "If behavioral change, announce"
    
  retire:
    trigger: "Doc no longer relevant (deprecated system, changed process)"
    steps:
      - mark: "Status: Deprecated, add redirect to replacement"
      - archive: "Move to archive after 30 days"
      - redirect: "Ensure all links point to replacement"
```

### 激励贡献

**减少阻碍：**
- 提供预先填充好的模板
- “快速记录”渠道 — 新员工可以先记录原始笔记，之后由他人整理
- 事件发生后： “什么会有帮助？” → 变成文档
- 新员工入职后：记录令人困惑的内容
- 会议记录 → 行动项中包括“记录[X]”

**提高可见性（社交认可）：**
- 每月表扬“最佳贡献者”
- 设立“文档大使”轮值制度 — 每个冲刺周期由一个人负责文档的维护
- 将文档编写纳入绩效评估标准
- 在团队会议中进行知识分享（5分钟的“今天我学到了什么”环节）

**培养习惯（文化规范）：**
- “如果你回答了一个问题两次，就把它写下来”
- 提交代码请求（PR）时包括“文档是否更新？”
- 事件事后分析包括“需要创建/更新哪些文档”

---

## 第五阶段：搜索与发现

### 搜索优化

**每份文档都应可以通过以下方式找到：**
1. **标题** — 描述性强的标题，包含关键词
2. **标签** — 包括领域、类型、目标受众和技术
3. **同义词** — 包含用户可能使用的替代词
4. **问题描述** — 使用“当[X]发生时”这样的表述

**标签模板：**
```yaml
document_tags:
  domain: "[engineering|product|sales|ops|finance|hr|cs|security|legal]"
  type: "[howto|reference|explanation|decision|troubleshooting]"
  audience: "[all|engineering|management|customer-facing|new-hire]"
  technology: "[list relevant tools/systems]"
  status: "[current|needs-review|deprecated]"
  difficulty: "[beginner|intermediate|advanced]"
```

### 发现机制

1. **上下文链接** — 每页底部提供相关文档的链接
2. **常见问题解答** — 按领域分类的常见问题及完整文档链接
3 **入职引导路径** — 根据角色定制的阅读列表
4. **Slack/聊天机器人** — 输入“询问知识库”可以搜索并返回相关文档
5. **每周摘要** — 发送“本周新增和更新的文档”邮件/消息
6. **错误页面链接** — 应用程序错误页面链接到故障排除文档

### 质量指标

根据以下标准优先显示搜索结果：
- **时效性** — 最近更新的文档优先显示
- **验证情况** — 经过同行评审的文档优先显示
- **使用频率** — 使用频率高的文档优先显示
- **完整性** — 结构完整的文档优先显示

---

## 第六阶段：知识捕获工作流程

### 事件后的知识捕获

每次事件发生后：
1. **立即**（24小时内）：记录事件的时间线和解决步骤
2. **事后分析**（5天内）：根本原因、影响因素和行动项
3. **知识提取**（10天内）：
   - 需要新的故障排除指南？ → 根据事后分析创建
   - 需要新的操作手册？ → 根据解决步骤创建
   - 现有文档错误？ → 用正确信息更新
   - 需要制定架构决策？ → 编写架构决策记录
   - 需要监控的内容？ → 记录需要监控的内容

### 会议后的知识捕获

必须生成知识文档的会议类型：
- **架构评审** → 生成架构决策记录（ADR）
- **流程变更** → 更新操作手册
- **战略决策** → 生成决策记录
- **客户反馈** → 更新产品相关文档
- **回顾性会议** → 生成流程改进文档

### 新员工的知识捕获

**入职前30天——新员工需要记录：**
- 入职期间遇到的困惑
- 现有文档未解答的问题
- 现有文档中的错误
- 改进建议

**新员工反馈模板：**
```yaml
onboarding_feedback:
  week: "[1|2|3|4]"
  couldnt_find: 
    - topic: "[What they looked for]"
      where_looked: "[Where they searched]"
      how_resolved: "[Asked someone? Found eventually? Still unclear?]"
  wrong_or_outdated:
    - doc: "[Which document]"
      issue: "[What's wrong]"
  suggestions:
    - "[Free text improvements]"
```

### 离职时的知识转移

当有人离职时：
1. **识别独特知识** — 他们掌握的他人不知道的知识
2. **安排知识提取会议** — 每个主要主题领域1-2小时
3. **尽可能记录** — 复杂流程的视频讲解
4. **配对指导** — 由继任者跟随指导2周
5. **审核他们编写的文档** — 文档是否完整？分配新的负责人
6. **记录部落知识** — 仅他们能回答的“为什么”问题

---

## 第七阶段：维护与时效性

### 时效性政策

```yaml
freshness_policy:
  review_frequency:
    critical_operations: "quarterly"  # Deployment, incident response, security
    standard_processes: "semi-annually"  # Regular workflows
    reference_docs: "annually"  # Specs, contacts, architecture
    explanations: "annually"  # Background, history, rationale
    
  review_process:
    - owner_notified: "2 weeks before due date"
    - review_actions:
        - verify: "Is this still accurate? Test/confirm."
        - update: "Fix any outdated information"
        - stamp: "Update 'Last verified' date"
        - skip: "If can't review, reassign or flag"
    - escalation: "Unreviewed after 30 days → manager notified"
    - stale_threshold: "2x review period without update → flagged as stale"
```

### 内容健康状况仪表盘

```yaml
kb_health:
  date: "[YYYY-MM-DD]"
  
  coverage:
    total_documents: 0
    by_type:
      howto: 0
      reference: 0
      explanation: 0
      decision: 0
      troubleshooting: 0
    by_domain: {}
    gaps_identified: []
    
  freshness:
    current: 0  # Reviewed within policy
    needs_review: 0  # Due for review
    stale: 0  # Past review deadline
    deprecated: 0
    freshness_rate: "0%"  # current / (current + needs_review + stale)
    
  quality:
    peer_reviewed: "0%"
    using_templates: "0%"
    has_owner: "0%"
    has_tags: "0%"
    
  usage:
    searches_per_week: 0
    failed_searches: 0  # Searches with no results
    top_10_pages: []
    pages_never_accessed: 0
    
  contribution:
    docs_created_this_month: 0
    docs_updated_this_month: 0
    unique_contributors: 0
    contribution_rate: "0%"  # contributors / total team size
```

### 季度知识审查

**议程（60分钟）：**
1. 仪表盘审查（10分钟） — 健康指标趋势
2. 缺口分析（15分钟） — 缺少什么？哪些问题反复出现？
3. 过时文档处理（15分钟） — 更新、降级或重新分配负责人
4. 搜索失败分析（10分钟） — 人们搜索什么但找不到？
5. 流程改进（10分钟） — 哪些方法有效，哪些无效？

---

## 第八阶段：知识驱动的自动化

### 自动化的知识触发机制

```yaml
automation_triggers:
  incident_resolved:
    action: "Create task: 'Write troubleshooting guide for [incident title]'"
    assignee: "Incident commander"
    due: "+10 days"
    
  new_hire_started:
    action: "Generate personalized onboarding reading list from KB by role"
    
  doc_stale:
    action: "Notify owner, CC manager if unreviewed after 14 days"
    
  repeated_question:
    threshold: "Same question asked 3+ times in support/Slack"
    action: "Create task: 'Document answer to [question]'"
    
  process_changed:
    trigger: "PR merged that changes workflow/process"
    action: "Check if related docs need updating, create task if yes"
    
  failed_search:
    threshold: "Same search term fails 5+ times/week"
    action: "Flag as gap, create task to write missing doc"
```

### 基于知识的聊天机器人设计

```yaml
kb_chatbot:
  flow:
    1_receive_question: "User asks in designated channel"
    2_search: "Semantic search across KB"
    3_respond:
      found_match: "Return relevant doc link + summary"
      partial_match: "Return closest docs + 'Did you mean...?'"
      no_match: "Log as gap, route to human expert, create doc task"
    4_feedback: "Was this helpful? 👍/👎"
    5_improve: "Use feedback to tune search, identify doc improvements"
    
  sources:
    - knowledge_base_docs
    - slack_saved_answers  # Curated from Slack threads
    - incident_postmortems
    - meeting_notes_tagged_as_knowledge
```

---

## 第九阶段：跨团队知识共享

### 知识共享机制

| 机制 | 频率 | 格式 | 目标受众 |
|-----------|-----------|--------|----------|
| “今天我学到了什么”频道 | 每日 | 短文（1-3句话+链接） | 所有团队 |
| 布朗袋午餐会 | 每两周一次 | 20分钟演讲+问答 | 跨团队 |
| 架构评审 | 每月 | 45分钟深度讨论+架构决策记录（ADR） | 工程团队 |
| 客户洞察分享 | 每月 | 最常见的5个模式及影响 | 产品团队+客户服务+销售团队 |
| 事件事后分析 | 每次事件后 | 书面记录+可选讲解 | 工程团队+运营团队 |
| 新工具/技术演示 | 根据需要 | 15分钟演示+文档链接 | 相关团队 |
| 季度知识回顾 | 每季度 | 仪表盘+缺口分析 | 领导团队 |

### 跨团队知识地图

```yaml
knowledge_map:
  engineering:
    produces: ["Architecture docs", "Runbooks", "API specs", "ADRs"]
    consumes_from:
      product: ["PRDs", "User research", "Roadmap"]
      customer_success: ["Bug patterns", "Feature requests", "Usage data"]
      sales: ["Technical requirements", "Integration needs"]
      
  product:
    produces: ["PRDs", "User research", "Roadmap", "Release notes"]
    consumes_from:
      engineering: ["Technical feasibility", "Architecture constraints"]
      customer_success: ["Feature requests", "Churn reasons"]
      sales: ["Deal requirements", "Competitive intel"]
      
  customer_success:
    produces: ["FAQ", "Troubleshooting guides", "Best practices"]
    consumes_from:
      engineering: ["Release notes", "Known issues"]
      product: ["Feature docs", "Roadmap"]
      
  sales:
    produces: ["Battlecards", "Competitive intel", "Use case docs"]
    consumes_from:
      product: ["Feature docs", "Roadmap", "Pricing"]
      customer_success: ["Case studies", "Success metrics"]
      engineering: ["Technical capabilities", "Integration docs"]
```

---

## 第十阶段：指标与投资回报（ROI）

### 知识管理关键绩效指标（KPIs）

| 指标 | 目标 | 测量方法 |
|--------|--------|-------------|
| 回答时间 | 文档记录的主题应在5分钟内得到回答 | 通过样本测试验证 |
| 新员工达到生产力所需时间 | 减少30% | 根据首次独立完成任务的时间计算 |
| 重复问题 | 6个月内减少50% | 通过支持工单分析 |
| 文档覆盖范围 | 关键流程的文档覆盖率超过80% | 根据流程列表审核 |
| 时效性 | 超过85%的文档在审查政策时间内更新 | 通过仪表盘指标衡量 |
| 贡献率 | 每月有超过40%的团队成员贡献 | 根据贡献者数量计算 |
| 搜索成功率 | 超过80%的搜索能找到所需内容 | 通过搜索分析衡量 |
| 搜索失败率 | 搜索失败率低于10% | 通过搜索分析衡量 |
| 知识复用率 | 超过60%的团队成员每周使用知识库 | 通过使用情况分析衡量 |

### 投资回报（ROI）计算

```
Knowledge Management ROI:

Time Saved:
  Reduced question-answering = [hours/week] × [avg hourly cost] × 52
  Faster onboarding = [weeks saved] × [new hires/year] × [weekly cost]
  Faster incident resolution = [hours saved/incident] × [incidents/year] × [hourly cost]
  
Risk Reduced:
  Key person dependency = [probability of departure] × [knowledge reconstruction cost]
  Compliance documentation = [audit prep hours saved] × [hourly cost]
  
Quality Improved:
  Fewer repeated mistakes = [error rate reduction] × [cost per error]
  Consistent processes = [variance reduction] × [rework cost]
  
Total Annual Value = Time Saved + Risk Reduced + Quality Improved
Investment = Tool cost + Time spent maintaining KB + Training
ROI = (Total Annual Value - Investment) / Investment × 100
```

---

## 第十一阶段：评分与质量评估

### 文档质量评分（0-100分）

| 维度 | 权重 | 0-2分（差） | 3-5分（合格） | 6-8分（良好） | 9-10分（优秀） |
|-----------|--------|------------|-----------------|-------------|-------------------|
| 准确性 | 20% | 未经验证，可能错误 | 大部分正确 | 经过验证，准确无误 | 经过测试和同行评审 |
| 完整性 | 15% | 有重大遗漏 | 包含基础知识 | 内容全面 | 包括特殊情况 |
| 清晰度 | 15% | 令人困惑，术语过多 | 易于理解 | 结构清晰 | 新员工也能理解 |
| 可查找性 | 10% | 无标签或标题不明确 | 有标签但标签不准确 | 标签准确，标题清晰 | 包含同义词和引用 |
| 时效性 | 15% | 超过12个月未更新 | 在年度审查范围内 | 在半年度审查范围内 | 在季度审查范围内 |
| 模板合规性 | 10% | 无结构 | 部分使用模板 | 完整使用模板 | 使用完整模板+额外内容 |
| 可操作性 | 10% | 只有理论描述 | 部分步骤 | 步骤清晰 | 可直接复制使用 |
| 负责人制度 | 5% | 无负责人 | 有负责人 | 负责人积极负责 | 负责人+备用负责人 |

**评分解读：**
- 90-100分：其他文档的参考范本 |
- 75-89分：符合标准 |
- 60-74分：需要少量改进 |
- 40-59分：需要大幅改进 |
- 0-39分：需要重新编写 |

### 知识库健康状况评分（0-100分）

| 维度 | 权重 | 指标 |
|-----------|--------|--------|
| 覆盖范围 | 20% | 关键流程的文档覆盖率 |
| 时效性 | 20% | 文档在审查政策范围内的比例 |
| 质量 | 15% | 文档的平均质量分数 |
| 使用率 | 15% | 每周使用知识库的团队成员比例 |
| 贡献率 | 15% | 每月贡献的团队成员比例 |
| 搜索效果 | 15% | 搜索结果满足需求的搜索比例 |

---

## 特殊情况

### 小团队（<10人）
- 从单一共享文档/维基开始，而不是完整的知识库平台
- 重点关注：关键流程的操作手册、入职指南、决策日志
- 由一人兼职负责知识库的维护
- 每季度进行一次审查，而非每月一次

### 远程/分布式团队
- 优先采用书面知识共享
- 记录重要的会议/决策（而非所有会议）
- 异步优先：所有决策都要记录下来
- 考虑时区差异：确保文档涵盖“专家不在时该怎么做”

### 快速成长（6个月内人数翻倍）
- 优先处理入职相关文档
- 从第一天起要求新员工记录所学内容
- 为每位新员工分配知识导师
- 每周为新员工组织问答环节并记录下来

### 受监管的行业
- 将合规要求与文档要求相匹配
- 使用版本控制并保留审计痕迹（谁修改了什么，何时修改）
- 对受监管的内容实施审批流程
- 保留政策要与法规一致

### 合并/收购后
- 对比两个组织的知识结构
- 识别重叠和差距
- 优先处理“当前的工作方式”相关的文档
- 冻结旧系统的文档

### 从分散的文档中迁移知识
- 不要试图迁移所有内容 — 从头开始使用新的结构
- 仅导入仍然准确、频繁使用的文档
- 将旧文档的链接重定向到新位置
- 为旧系统设定截止日期
- “如果不在新知识库中，就视为不存在”（迁移后）

---

## 自然语言命令

| 命令 | 动作 |
|---------|--------|
| “审计我们的知识管理” | 运行第一阶段的评估，生成风险登记 |
| “设计我们的知识库结构” | 创建分类法和导航架构 |
| “为[X]编写操作手册” | 使用操作手册模板生成 |
| “为[X]编写架构决策记录” | 使用架构决策记录模板生成 |
| “为[X]编写故障排除指南” | 使用故障排除指南模板生成 |
| “审查知识库的健康状况” | 生成健康状况仪表盘并识别缺口 |
| “为[某人]安排知识提取会议” | 生成访谈指南并安排时间 |
| “设置时效性跟踪” | 创建审查计划和通知规则 |
| “为[某个角色]设计入职引导路径” | 从知识库中整理阅读列表 |
| “分析搜索失败的原因” | 审查搜索缺口并生成任务 |
| “生成季度知识库报告” | 生成包含建议的完整指标仪表盘 |
| “规划知识库的迁移” | 制定迁移计划并确定优先级 |