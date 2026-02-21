# 人工智能治理与负责任的人工智能引擎

这是一个完整的框架，用于建立人工智能治理程序，确保遵守法规（欧盟《人工智能法案》、NIST人工智能风险管理框架（AI RMF）和ISO 42001标准，管理算法风险，并构建可信的人工智能系统。在制定人工智能政策、进行人工智能影响评估、对人工智能系统风险进行分类、建立模型治理机制、设立人工智能伦理委员会或为特定于人工智能的法规做准备时，可以使用该框架。

---

## 第一阶段：治理成熟度评估

在开始任何工作之前，首先评估您当前的状况。

### 人工智能治理成熟度模型（每个维度评分1-5分）

| 维度 | 1 — 非正式 | 3 — 明确定义 | 5 — 最优化 |
|-----------|-----------|------------|--------------|
| **政策** | 无特定于人工智能的政策 | 有书面政策，部分实施 | 活跃的政策，自动执行 |
| **风险管理** | 无人工智能风险流程 | 对高风险系统进行风险评估 | 持续监控，自动警报 |
| **责任追究** | 无明确的责任归属 | 角色定义不明确，执行不一致 | 嵌入了RACI框架，人工智能伦理委员会活跃 |
| **透明度** | 无文档记录 | 部分系统有模型卡片 | 全部系统都有完整记录，可解释性 |
| **公平性** | 无偏见测试 | 临时进行偏见检查 | 系统性测试、监控和纠正 |
| **数据治理** | 无人工智能数据标准 | 有针对人工智能的数据质量规则 | 数据来源可追溯，有数据使用同意机制 |
| **合规性** | 不了解人工智能法规 | 了解法规，部分合规 | 主动合规，准备好接受审计，持续合规 |
| **文化** | 缺乏人工智能素养 | 仅为人工智能团队提供培训 | 全组织范围内的人工智能素养计划 |

**评分标准：**
- 8-16分：**基础阶段** — 立即进入第二至第三阶段
- 17-28分：**发展阶段** — 重点关注风险分类和责任追究 |
- 29-40分：**高级阶段** — 优化监控和持续合规

### 治理概况 YAML

```yaml
organization:
  name: "[Company]"
  industry: "[sector]"
  size: "[employees]"
  ai_maturity: "[foundation/developing/advanced]"

ai_landscape:
  total_ai_systems: [count]
  customer_facing: [count]
  decision_making: [count]  # Systems that make/influence decisions about people
  generative_ai: [count]
  third_party_ai: [count]   # Vendor AI embedded in your stack

regulatory_exposure:
  eu_ai_act: [yes/no]       # Serve EU customers or employees?
  nist_ai_rmf: [yes/no]     # US federal contracts or alignment?
  iso_42001: [yes/no]       # Certification target?
  sector_specific: "[HIPAA AI, FDA SaMD, SEC AI, etc.]"

current_state:
  ai_policy_exists: [yes/no]
  ai_inventory_complete: [yes/no]
  bias_testing_process: [yes/no]
  incident_response_for_ai: [yes/no]
  ai_ethics_board: [yes/no]

priority: "[compliance/risk reduction/trust building/competitive advantage]"
timeline: "[3/6/12 months]"
```

---

## 第二阶段：人工智能系统清单与风险分类

只有了解存在的情况，才能进行治理。

### 人工智能系统清单 YAML

```yaml
system:
  id: "AI-[sequential]"
  name: "[descriptive name]"
  description: "[what it does in plain language]"
  owner: "[team/person accountable]"
  
  classification:
    type: "[predictive/generative/recommendation/automation/detection/optimization]"
    eu_ai_act_risk: "[unacceptable/high/limited/minimal]"
    internal_risk_tier: "[critical/high/medium/low]"
    
  scope:
    users_affected: "[internal only/customers/public]"
    decisions_influenced: "[what decisions does this affect?]"
    autonomy_level: "[advisory/human-in-loop/human-on-loop/autonomous]"
    reversibility: "[easily reversed/difficult to reverse/irreversible]"
    
  data:
    training_data_sources: ["[list sources]"]
    personal_data: [yes/no]
    sensitive_categories: ["[race/gender/age/disability/etc. if applicable]"]
    data_freshness: "[static/periodic refresh/real-time]"
    
  technical:
    model_type: "[LLM/classifier/regression/ensemble/rule-based/hybrid]"
    vendor: "[in-house/vendor name]"
    version: "[current version]"
    last_evaluated: "[date]"
    
  governance:
    impact_assessment_completed: [yes/no]
    bias_audit_completed: [yes/no]
    explainability_method: "[SHAP/LIME/attention/rule extraction/none]"
    monitoring_active: [yes/no]
    human_override_available: [yes/no]
```

### 欧盟《人工智能法案》风险分类决策树

```
1. Does the system manipulate behavior, exploit vulnerabilities, 
   or enable social scoring?
   → YES: UNACCEPTABLE (banned) — Stop. Do not deploy.

2. Is it used in any of these domains?
   - Biometric identification (real-time in public)
   - Critical infrastructure (energy, transport, water)
   - Education (access, assessment)
   - Employment (recruitment, evaluation, termination)
   - Essential services (credit, insurance, benefits)
   - Law enforcement (risk assessment, evidence evaluation)
   - Migration/asylum (applications, surveillance)
   - Justice (sentencing, parole)
   → YES: HIGH-RISK — Full compliance required (Phase 3-8)

3. Does it interact directly with people?
   (Chatbots, deepfake generators, emotion recognition)
   → YES: LIMITED RISK — Transparency obligations (disclose AI)

4. None of the above?
   → MINIMAL RISK — Voluntary codes of practice encouraged
```

### 内部风险等级（超出欧盟分类标准）

| 因素 | 权重 | 低（1） | 中等（3） | 高（5） |
|--------|--------|---------|------------|----------|
| **对人员的影响** | 25% | 提供便利功能 | 影响决策 | 决定结果 |
| **规模** | 20% | 用户少于100人 | 100-10,000人 | 超过10,000人 |
| **可逆性** | 20% | 容易逆转 | 部分可逆 | 不可逆转 |
| **数据敏感性** | 15% | 公共数据 | 个人数据 | 敏感类别 |
| **自主性** | 10% | 仅提供咨询 | 人工干预 | 自主决策 |
| **声誉** | 10% | 可见度低 | 面向客户 | 受到公众/媒体关注 |

**等级分配：**
- 分数1.0-2.0：**低风险** — 采用标准开发实践 |
- 分数2.1-3.5：**中等风险** — 需要进行影响评估和偏见审查 |
- 分数3.6-5.0：**高风险/关键风险** — 需要完整的治理生命周期 |

---

## 第三阶段：人工智能影响评估（AIIA）

所有高风险和中等风险系统都必须进行此评估。

### 影响评估模板

```yaml
assessment:
  system_id: "AI-[ref]"
  assessor: "[name/team]"
  date: "[YYYY-MM-DD]"
  review_type: "[initial/periodic/triggered]"

purpose_and_necessity:
  problem_statement: "[What problem does this solve?]"
  necessity_test: "[Why AI specifically? Could rules/heuristics work?]"
  proportionality: "[Is the AI approach proportional to the problem?]"
  alternatives_considered: ["[list non-AI alternatives evaluated]"]

stakeholder_analysis:
  direct_users: "[who uses the system]"
  affected_parties: "[who is affected by system outputs]"
  vulnerable_groups: "[any vulnerable populations affected?]"
  stakeholder_consultation: "[how were affected parties consulted?]"

rights_impact:
  privacy: "[how personal data is used, consent mechanism]"
  non_discrimination: "[bias risk, protected characteristics]"
  autonomy: "[does it restrict individual choices?]"
  dignity: "[does it treat people as means or ends?]"
  due_process: "[can decisions be challenged/appealed?]"
  transparency: "[can affected parties understand the decision?]"

risk_register:
  - risk: "[description]"
    likelihood: "[rare/unlikely/possible/likely/almost certain]"
    impact: "[insignificant/minor/moderate/major/catastrophic]"
    mitigation: "[planned mitigation]"
    residual_risk: "[low/medium/high]"
    owner: "[who monitors this]"

fairness_assessment:
  protected_characteristics_tested: ["[list: age, gender, race, etc.]"]
  bias_metrics_used: ["[demographic parity, equalized odds, etc.]"]
  disparate_impact_found: [yes/no]
  remediation_plan: "[if yes, what's the plan]"

explainability:
  method: "[SHAP/LIME/counterfactual/rule extraction/attention]"
  audience: "[who needs explanations — users/affected/regulators]"
  format: "[natural language/feature importance/decision factors]"
  individual_explanations: [yes/no]

controls:
  human_oversight: "[type and frequency]"
  monitoring: "[what metrics, what frequency]"
  kill_switch: "[how to disable quickly]"
  incident_response: "[link to playbook]"
  audit_trail: "[what's logged]"

decision:
  recommendation: "[approve/approve with conditions/reject/defer]"
  conditions: ["[list any conditions for approval]"]
  review_date: "[next scheduled review]"
  approver: "[who has authority to approve]"
```

### 必要性检查清单

在部署任何人工智能系统之前，请回答以下问题：
- [ ] 我们是否明确界定了人工智能要解决的问题？
- [ ] 我们是否考虑了非人工智能的替代方案？
- [ ] 人工智能的方法是否与风险相匹配？
- [ ] 我们是否有足够的高质量训练数据？
- [ ] 我们能否向受影响方解释系统的决策？
- [ ] 是否有明确的人工监督机制？
- [ ] 我们是否识别了所有利益相关者，包括弱势群体？
- [ ] 系统是否可以在不影响业务连续性的情况下被关闭？

**如果任何答案为“否”，**请在继续之前解决这些问题。

---

## 第四阶段：人工智能政策框架

### 核心政策（按此顺序制定）

#### 1. 人工智能可接受使用政策（AUP）

```markdown
# AI Acceptable Use Policy

## Purpose
Defines acceptable and prohibited uses of AI systems within [Organization].

## Scope
All employees, contractors, and vendors using or developing AI systems.

## Permitted Uses
- [List approved AI tools and their approved purposes]
- Internal productivity (with data handling rules)
- Customer-facing features (with transparency requirements)

## Prohibited Uses
- Processing sensitive data through unapproved AI tools
- Using AI to make final decisions about [employment/credit/etc.] without human review
- Generating content represented as human-created without disclosure
- Using personal/sensitive data for AI training without consent
- Deploying AI systems not registered in the AI inventory
- Using AI to profile or score individuals on protected characteristics

## Data Rules
- Never input [PII/PHI/financial data/trade secrets] into external AI tools
- All AI-generated outputs must be reviewed before external use
- Customer data used for AI must comply with privacy policy and consent

## Accountability
- Each AI system must have a designated owner
- Violations reported to [AI governance team/ethics board]
- [Consequences for violations]
```

#### 2. 人工智能开发与部署标准

```markdown
# AI Development Lifecycle Standard

## Pre-Development Gate
- [ ] Problem statement approved
- [ ] AI necessity confirmed (non-AI alternatives evaluated)
- [ ] Risk classification completed
- [ ] Data governance review passed
- [ ] Impact assessment initiated (if medium/high risk)

## Development Standards
- [ ] Training data documented (source, quality, bias assessment)
- [ ] Model selection justified and documented
- [ ] Bias testing performed on protected characteristics
- [ ] Explainability method chosen and implemented
- [ ] Performance metrics defined with minimum thresholds
- [ ] Adversarial testing / red-teaming completed

## Pre-Deployment Gate
- [ ] Impact assessment completed and approved
- [ ] Model card published to AI registry
- [ ] Human oversight mechanism tested
- [ ] Monitoring dashboards configured
- [ ] Incident response playbook reviewed
- [ ] Audit logging verified
- [ ] User disclosure/transparency implemented

## Post-Deployment
- [ ] Performance monitoring active
- [ ] Bias monitoring active (demographic metrics)
- [ ] Drift detection configured
- [ ] User feedback collection active
- [ ] Periodic review scheduled (quarterly for high-risk)
```

#### 3. 人工智能供应商评估清单

对于任何第三方人工智能产品（供应商工具、API、嵌入式人工智能）：
- [ ] 供应商是否提供模型文档？
- [ ] 数据处理流程是否明确记录（数据去向、保留方式）？
- [ ] 供应商是否允许进行偏见审计或提供偏见报告？
- [ ] 合同中是否包含特定于人工智能的条款（责任、知识产权、数据使用）？
- [ ] 供应商的训练数据是否不包含您的专有数据（未经同意）？
- [ ] 是否有退出策略（数据可迁移性、模型独立性）？
- [ ] 供应商是否遵守相关的人工智能法规？ |

---

## 第五阶段：公平性与偏见管理

### 偏见测试协议

#### 第一步：定义受保护的特征

在所有相关的受保护特征上进行测试：
- 年龄、性别/性别、种族/民族、残疾、宗教
- 另外还包括：社会经济地位、地理位置、语言
- 行业特定特征：信用记录（贷款）、健康状况（保险）

#### 第二步：选择公平性指标

| 指标 | 定义 | 适用场景 |
|--------|-----------|----------|
| **人口统计平等** | 各组之间的正面预测率相等 | 选择/审批决策 |
| **机会平等** | 各组的真正阳性率（TPR）和假阳性率（FPR）相等 | 基于已知结果的分类 |
| **预测平等** | 各组的精确度相等 | 风险评分系统 |
| **个体公平性** | 相似的个体得到相似的预测结果 | 个性化系统 |
| **反事实公平性** | 改变受保护属性不会改变预测结果 | 任何决策系统 |

**关键规则：**没有单一指标能够完全反映公平性。至少使用两个指标。记录选择这些指标的原因。**

#### 第三步：测试频率

| 系统风险 | 部署前 | 部署后 | 触发条件 |
|-------------|-----------|-------------|-----------|
| **高风险** | 全面审计 | 每月 | 有任何投诉或数据变更时 |
| **中等风险** | 重点审计 | 每季度 | 模型有重大更新时 |
| **低风险** | 基本检查 | 每年 | 有重大投诉时 |

#### 第四步：偏见审计报告模板

```yaml
audit:
  system_id: "AI-[ref]"
  date: "[YYYY-MM-DD]"
  auditor: "[internal/external name]"
  
characteristics_tested:
  - attribute: "[e.g., gender]"
    groups: ["[male, female, non-binary]"]
    sample_sizes: [n1, n2, n3]
    
metrics:
  - name: "[demographic_parity]"
    results:
      - group: "[group A]"
        rate: [0.XX]
      - group: "[group B]"
        rate: [0.XX]
    disparity_ratio: [0.XX]
    threshold: [0.80]  # 4/5ths rule
    pass: [yes/no]
    
findings:
  - finding: "[description]"
    severity: "[critical/high/medium/low]"
    recommendation: "[action]"
    
overall_assessment: "[pass/conditional pass/fail]"
next_review: "[date]"
```

---

## 第六阶段：透明度与可解释性

### 模型卡片模板

每个人工智能系统都会有一张模型卡片（参考Mitchell等人的研究改编）。

```yaml
model_card:
  system_id: "AI-[ref]"
  version: "[X.Y.Z]"
  last_updated: "[date]"
  
overview:
  name: "[system name]"
  purpose: "[what it does, in plain language]"
  intended_users: "[who should use this]"
  out_of_scope_uses: "[explicitly, what this should NOT be used for]"
  
performance:
  primary_metric: "[metric name]: [value]"
  secondary_metrics:
    - "[metric]: [value]"
  evaluation_data: "[description of test dataset]"
  known_limitations: ["[list known failure modes]"]
  
fairness:
  tested_characteristics: ["[list]"]
  metrics_used: ["[list]"]
  results_summary: "[pass/conditional/fail with details]"
  
data:
  training_data: "[description — types, sources, size, date range]"
  preprocessing: "[key transformations applied]"
  known_data_gaps: ["[what's underrepresented]"]
  
ethical_considerations:
  risks: ["[identified risks]"]
  mitigations: ["[what was done about them]"]
  
technical:
  model_type: "[architecture]"
  training_compute: "[if relevant]"
  inference_latency: "[p50/p99]"
  
contact:
  owner: "[team/person]"
  feedback: "[how to report issues]"
```

### 可解释性选择指南

| 对象 | 需求 | 方法 | 格式 |
|----------|------|--------|--------|
| **最终用户** | “为什么我得到这个结果？” | 反事实分析、特征亮点 | 自然语言解释 |
| **受影响者** | “为什么我被拒绝？” | LIME/SHAP方法 | 简单语言解释 + 上诉流程 |
| **监管机构** | “系统是如何工作的？” | 模型卡片 + 全局SHAP解释 | 技术文档 |
| **内部审计** | “系统是否正常运行？” | 完整的SHAP解释 + 混淆矩阵 | 仪表板 + 详细报告 |
| **开发人员** | “为什么在这里出问题？” | SHAP解释 + 错误分析 | 技术探索工具 |

### 透明度要求清单

- [ ] 用户知道他们正在与人工智能交互（必须披露）
- [ ] 人工智能生成的内容必须有标签（尤其是深度伪造/合成媒体）
- [ ] 受影响方可以要求解释人工智能的影响决策 |
- [ ] 必须有上诉/人工审查流程，并且要告知相关方 |
- [ ] 数据来源和总体逻辑必须用简单语言描述 |
- [ ] 模型卡片必须在内部发布（对于高风险系统还需对外发布） |
- [ ] 对人工智能系统的任何更改都必须通知受影响方 |

---

## 第七阶段：人工智能事件响应

### 人工智能特定事件类型

| 事件类型 | 例子 | 严重程度 |
|---------------|---------|----------------|
| **偏见事件** | 系统对受保护群体存在歧视 | 如果面向客户，则为严重事件（SEV-1） |
| **错误信息生成** | 生成了被采纳的虚假信息 | 如果造成伤害，则为严重事件（SEV-2） |
| **数据泄露** | 训练数据包含/泄露个人身份信息（PII） | 总是严重事件（SEV-1） |
| **对抗性攻击** | 诱导性输入、模型被操纵 | 严重事件（SEV-2）；如果数据被泄露，则为更严重的事件（SEV-1） |
| **模型性能下降** | 模型准确率低于阈值 | 严重事件（SEV-3）；如果影响决策，则为更严重的事件（SEV-2） |
| **意外行为** | 系统超出预期范围运行 | 根据影响程度而定 |

### 人工智能事件响应手册

```
DETECTION
├── Automated: monitoring alert, drift detection, bias threshold breach
├── User report: complaint, feedback, support ticket
└── External: media report, regulator inquiry, researcher disclosure

TRIAGE (within 1 hour)
├── Classify severity (SEV-1 to SEV-4)
├── Identify affected population and scale
├── Determine: is the system still causing harm?
│   └── YES → proceed to immediate containment
└── Assign incident commander

CONTAINMENT (SEV-1: immediate, SEV-2: <4 hours)
├── Option A: Disable AI system entirely (kill switch)
├── Option B: Revert to previous model version
├── Option C: Add human-in-loop gate
├── Option D: Restrict to subset of users/use cases
└── Document containment decision and rationale

INVESTIGATION
├── Root cause analysis (model? data? deployment? adversarial?)
├── Impact quantification (how many affected, how severely)
├── Timeline reconstruction
├── Bias audit if discrimination suspected
└── Preserve all evidence (model version, data, logs)

REMEDIATION
├── Fix root cause (retrain, patch, redesign)
├── Validate fix with held-out test including affected demographic
├── Update model card and documentation
├── Re-run impact assessment if significant change
└── Get approval before redeployment

COMMUNICATION
├── Internal: stakeholders, leadership, legal
├── Affected parties: notification if required by law or policy
├── Regulators: if required (EU AI Act: 72-hour notification for serious incidents)
└── Public: if media attention or significant impact

POST-INCIDENT
├── Blameless post-mortem (focus on systemic fixes)
├── Update AI risk register
├── Update monitoring to catch similar incidents
├── Share lessons learned across AI teams
└── Schedule follow-up review (30 days)
```

### 沟通模板

**内部升级（SEV-1）：**
```
🚨 AI INCIDENT — [System Name] — SEV-1

What happened: [Brief description]
Impact: [Who affected, how many, what harm]
Current status: [Contained/Active/Investigating]
Containment action: [What was done]
Next steps: [Immediate actions]
Incident commander: [Name]
War room: [Link/channel]
```

**受影响方通知：**
```
Subject: Important notice about [service/decision]

We identified an issue with [system/service] that may have affected 
[your application/recommendation/score].

What happened: [Plain language, no jargon]
Who was affected: [Scope]
What we've done: [Containment + fix]
What this means for you: [Practical impact]
Your options: [Appeal, review, contact]

We take this seriously and have [actions taken to prevent recurrence].

Contact: [dedicated email/phone for questions]
```

---

## 第八阶段：法规合规性深入分析

### 欧盟《人工智能法案》合规计划（2025年8月生效）

**针对高风险人工智能系统（第6-51条）：**

| 要求 | 所需内容 | 证据 |
|------------|---------------|----------|
| **风险管理**（第9条） | 持续的风险识别和缓解 | 风险管理计划 + 注册记录 + 审查记录 |
| **数据治理**（第10条） | 训练数据的质量、相关性和代表性 | 数据文档 + 质量指标 + 偏见测试 |
| **技术文档**（第11条） | 详细的系统描述 | 模型卡片 + 架构 + 测试结果 |
| **记录保存**（第12条） | 系统操作的自动记录 | 审计日志 + 保留政策 |
| **透明度**（第13条） | 使用说明、功能和使用限制 | 用户文档 + 模型卡片 |
| **人工监督**（第14条） | 有效的人工监督措施 | 监督设计 + 培训记录 |
| **准确性和鲁棒性**（第15条 | 适当的准确性和错误抵抗力 | 性能基准 + 对抗性测试 |
| **合规性评估**（第43条） | 上市前评估（自我评估或第三方评估） | 评估报告 + CE标志 |
| **注册**（第49条） | 在欧盟数据库注册 | 注册确认 |
| **上市后监控**（第61条） | 持续监控计划 | 监控计划 + 事件报告 |
| **严重事件报告**（第62条） | 在规定时间内向当局报告 | 事件报告 + 通知记录 |

**针对通用人工智能（GPAI）模型：**
- 关于训练和测试的技术文档 |
- 版权政策合规性 |
- 训练数据摘要 |
- 系统性风险评估（针对具有系统性风险的人工智能）

### NIST人工智能风险管理框架（AI RMF 1.0）

四个核心功能 — 映射、测量、管理、治理：

**治理：**
- [ ] 建立了人工智能治理结构 |
- [ ] 明确了角色和责任 |
- [ ] 政策反映了组织价值观 |
- [ ] 为人工智能设定了风险容忍度 |
- [ ] 映射了法律/法规要求 |

**映射：**
- [ ] 记录了人工智能系统的目的 |
- [ ] 识别了利益相关者和受影响的社区 |
- [ ] 描述了收益、成本和风险 |
- [ ] 确定了风险背景（运营环境） |

**测量：**
- [ ] 为可信赖性特征确定了指标 |
- [ ] 评估了系统的偏见、安全性和隐私性 |
- [ ] 收集了来自受影响社区的反馈 |
- [ ] 随时间跟踪指标（模型性能的变化） |

**管理：**
- [ ] 优先处理并记录了风险 |
- [ ] 实施了风险处理计划 |
- [ ] 测试了对已识别风险的响应 |
- [ ] 持续改进过程正在运行 |

### ISO 42001（人工智能管理系统）概述

认证的关键条款：
- **第4条：**背景 — 与人工智能相关的利益相关者和范围 |
- **第5条：**领导层 — 高层管理层对负责任的人工智能的承诺 |
- **第6条：**规划 — 人工智能风险评估和处理 |
- **第7条：**支持 — 资源、能力和对人工智能的认识 |
- **第8条：**运营 — 人工智能系统的生命周期管理 |
- **第9条：**性能评估 — 监控人工智能的有效性 |
- **第10条：**改进 — 对人工智能问题的纠正措施 |

---

## 第九阶段：人工智能伦理委员会设计

### 委员会结构

```yaml
ai_ethics_board:
  name: "AI Ethics Advisory Board"
  charter: "[link to charter document]"
  
  composition:  # Diverse perspectives required
    - role: "Chair"
      background: "[senior leader with ethics/compliance background]"
    - role: "Technical Lead"
      background: "[ML/AI engineering expertise]"
    - role: "Legal/Compliance"
      background: "[regulatory, privacy law]"
    - role: "Product/Business"
      background: "[understands use cases and customers]"
    - role: "External Ethicist"
      background: "[academic or independent ethics expert]"
    - role: "Affected Community Representative"
      background: "[represents those impacted by AI decisions]"
    - role: "Data/Privacy"
      background: "[data governance, privacy engineering]"
  
  mandate:
    - Review all high-risk AI impact assessments
    - Advise on ethical edge cases
    - Review AI incident post-mortems
    - Recommend policy updates
    - Annual AI governance program review
    
  authority: "[advisory/approval required for high-risk/veto power]"
  
  cadence:
    regular_meetings: "Monthly"
    urgent_review: "Within 48 hours for SEV-1 incidents"
    annual_review: "Full program assessment"
    
  decision_process:
    quorum: "[minimum members for decisions]"
    voting: "[consensus preferred, majority if needed]"
    conflicts: "[recusal process for conflicts of interest]"
    documentation: "[all decisions documented with rationale]"
```

### 向伦理委员会升级

| 触发条件 | 响应时间 | 委员会行动 |
|---------|--------------|-------------|
| 新出现的高风险人工智能系统 | 下次会议 | 审查影响评估，批准/拒绝 |
| 偏见事件（SEV-1） | 48小时 | 紧急审查，提供补救建议 |
| 监管调查 | 48小时 | 审查响应，提供法律建议 |
| 新颖的用例（无先例） | 下次会议 | 伦理评估，设定先例 |
| 员工/公众的伦理问题 | 2周 | 调查，提出行动建议 |
| 年度计划审查 | 定期 | 全面的治理健康检查 |

---

## 第十阶段：监控与持续治理

### 人工智能治理仪表板 YAML

```yaml
dashboard:
  period: "[month]"
  
  inventory_health:
    total_ai_systems: [count]
    fully_documented: [count]
    impact_assessments_current: [count]
    overdue_reviews: [count]
    
  compliance_status:
    high_risk_systems: [count]
    fully_compliant: [count]
    gaps_identified: [count]
    remediation_in_progress: [count]
    
  fairness:
    systems_with_active_monitoring: [count]
    bias_incidents_this_period: [count]
    open_bias_remediation: [count]
    
  incidents:
    total_ai_incidents: [count]
    sev1: [count]
    mean_time_to_contain: "[hours]"
    post_mortems_completed: [count]
    
  transparency:
    model_cards_published: "[X of Y]"
    user_disclosures_active: "[X of Y]"
    explanation_requests_fulfilled: [count]
    
  governance_health_score: "[0-100]"
```

### 治理健康评分（0-100分）

| 维度 | 权重 | 评分 |
|-----------|--------|---------|
| **清单完整性** | 15% | 已记录和分类的人工智能系统占比 |
| **影响评估** | 20% | 完成且最新的评估占比 |
| **偏见管理** | 20% | 具有活跃公平性监控的系统占比 |
| **透明度** | 15% | 具有模型卡片和用户披露的系统占比 |
| **事件响应准备情况** | 15% | 响应时间和事后完成率 |
| **政策合规性** | 15% | 符合所有政策要求的系统占比 |

### 审查频率

| 活动 | 频率 | 负责人 |
|----------|-----------|-------|
| 人工智能清单更新 | 每月 | 人工智能治理团队 |
| 高风险系统监控审查 | 每月 | 系统所有者 |
| 高风险系统的偏见审计 | 每季度 | 数据科学团队 + 伦理委员会 |
| 影响评估更新 | 每年（或发生重大变化时） | 系统所有者 |
| 政策审查 | 每年 | 人工智能治理团队 + 法律部门 |
| 全面治理计划审计 | 每年 | 人工智能伦理委员会 |
| 监管环境扫描 | 每季度 | 法律部门 + 合规性部门 |
| 人工智能素养培训更新 | 每年 | 人力资源部门 + 人工智能治理团队 |

---

## 第十一阶段：生成式人工智能治理（特别章节）

生成式人工智能带来了独特的治理挑战。

### 生成式人工智能特定风险

| 风险 | 缓解措施 |
|------|-----------|
| **错误信息生成** | 通过基础层（RAG）进行事实核查，对高风险情况实施人工审查 |
| **版权侵犯** | 证明训练数据的来源，过滤输出结果，与供应商签订赔偿条款 |
| **数据泄露** | 对输入数据进行清洗，使用数据丢失防护（DLP）过滤器 |
| **诱导性输入** | 对输入进行验证，加强系统提示的安全性 |
| **深度伪造/合成媒体** | 添加水印，记录内容的来源（C2PA），使用检测工具 |
| **过度依赖** | 对模型进行限制培训，决策时必须有人工干预 |
| **环境影响** | 监控模型的效率，调整模型规模，跟踪碳排放 |

### 生成式人工智能可接受使用矩阵

| 使用场景 | 风险等级 | 要求 |
|----------|-----------|-------------|
| 内部起草/头脑风暴 | 低风险 | 不使用敏感数据 |
| 代码生成/审查 | 中等风险 | 对输出进行安全审查，提示中不得包含秘密信息 |
| 面向客户的聊天机器人 | 高风险 | 设置防护措施，进行监控，提供上诉途径 |
| 内容创作（营销） | 中等风险 | 人工审核，进行事实核查，不得有虚假声明 |
| 决策支持（人力资源/法律） | 高风险 | 必须有人工干预，进行偏见测试，保留审计痕迹 |
| 自主代理 | 关键风险 | 全面的治理生命周期，设置关闭机制，持续监控 |
| 合成数据生成 | 中等风险 | 进行隐私审查，验证数据质量 |

### 生成式人工智能供应商评估（附加问题）

- [ ] 输入数据去向？是否用于训练？ |
- [ ] 是否可以禁用数据保留或自定义保留期限？ |
- [ ] 采取了哪些数据过滤/安全措施？ |
- [ ] 提供商对版权问题有何处理方式？ |
- [ ] 提供商是否对人工智能输出提供赔偿？ |
- [ ] 是否可以定制模型并设置防护措施？ |
- [ ] 提供商对模型问题有何应对措施？ |
- [ ] 是否有针对数据处理的附加协议？ |

---

## 第十二阶段：人工智能素养与文化

### 人工智能素养计划设计

| 对象 | 内容 | 时长 | 频率 |
|----------|---------|----------|-----------|
| **所有员工** | 人工智能基础知识、AUP、数据规则、报告相关事项 | 1小时 | 每年 + 新员工入职培训 |
| **管理者** | 人工智能决策、监督责任、偏见意识 | 2小时 | 每年 |
| **人工智能/数据团队** | 全面的治理生命周期、公平性指标、文档标准 | 4小时 | 每半年 |
| **领导层** | 战略性人工智能治理、监管环境、风险偏好 | 2小时 | 每年 |
| **伦理委员会** | 深入研究新兴问题、案例研究、框架更新 | 持续进行 | 每月阅读 + 每季度研讨会 |

### 文化健康指标

积极信号：
- 团队主动提前注册人工智能实验 |
- 偏见问题被主动提出（而非在事件发生后）
- “我们应该使用人工智能吗？”成为常规问题 |
- 将影响评估视为有价值的活动，而非官僚程序 |
- 在处理边缘问题时咨询伦理委员会

警告信号：
- 发现未注册的“影子人工智能”系统 |
- “快速行动，之后再治理”的态度 |
- 因为赶时间而跳过偏见测试 |
- 没有提出问题或担忧（沉默≠合规） |
- 在“紧急”情况下绕过伦理委员会

## 质量评估标准（0-100分）

| 维度 | 权重 | 0 | 50 | 100 |
|-----------|--------|---|----|----|
| **清单管理** | 15% | 无人工智能清单 | 部分清单 | 完整、最新、分类清晰 |
| **风险评估** | 15% | 无影响评估 | 仅进行临时评估 | 对所有中等风险及以上的系统进行系统化评估 |
| **公平性** | 15% | 无偏见测试 | 仅在部署前进行 | 持续监控 + 纠正措施 |
| **透明度** | 15% | 无文档记录 | 部分系统有模型卡片 | 所有系统都有完整卡片 + 用户披露 |
| **事件响应** | 10% | 无特定于人工智能的流程 | 仅基本响应措施 | 进行过测试、有事后分析 |
| **合规性** | 15% | 不了解法规 | 部分合规 | 准备接受审计，主动合规 |
| **文化** | 10% | 无人工智能素养 | 仅为人工智能团队提供培训 | 全组织范围内，主动进行培训 |

---

## 边缘情况

### 初创企业/小型公司
- 从人工智能清单和可接受使用政策开始——即使是非正式的 |
- 缩小使用此框架的范围：进行简化的影响评估，无需编写长达50页的文档 |
- 指定一名人员作为人工智能治理负责人（通常是CTO或产品负责人） |
- 首先关注面向客户的人工智能 |

### 受监管的行业（金融服务、医疗保健）
- 在现有合规基础上增加人工智能治理 |
- 将人工智能风险纳入现有的风险分类体系中 |
- 尽早与行业特定的监管机构联系（许多行业都有相关指导）
- 对高风险系统考虑外部的人工智能审计

### 大量使用第三方人工智能的情况
- 供应商评估是主要的治理工具 |
- 维护所有供应商提供的人工智能系统的清单（包括SaaS工具中的嵌入式人工智能） |
- 合同中的保护措施至关重要（数据使用、责任、审计权利） |
- 持续监控供应商的合规情况（而不仅仅是采购时）

### 快速采用人工智能/“人工智能无处不在”的情况
- 不要让治理成为瓶颈——分层方法是关键 |
- 低风险：使用自助服务检查表快速处理 |
- 中等风险：进行标准审查（1-2周） |
- 高风险：进行全面评估（4-6周） |
- 将治理纳入开发流程，而不是将其作为障碍 |

### 多国运营
- 根据不同司法管辖区的要求进行映射 |
- 采用最严格的标准（通常是欧盟《人工智能法案》 |
- 记录针对不同司法管辖区的调整 |
- 考虑人工智能的数据本地化要求

### 收购的人工智能系统
- 立即对收购的实体进行人工智能清单管理 |
- 在90天内对所有继承的人工智能系统进行风险分类 |
- 在6个月内将其纳入治理计划 |
- 优先处理面向客户和决策相关的系统 |

---

## 自然语言命令

1. **“评估我们的人工智能治理成熟度”** → 运行第一阶段的成熟度模型，生成评分和优先事项 |
2. **“对这个人工智能系统进行分类”** → 按照欧盟《人工智能法案》和内部风险等级进行分类 |
3. **“对[系统]进行人工智能影响评估”** → 使用第三阶段的模板生成完整的AIIA报告 |
4. **“起草我们的人工智能可接受使用政策”** → 使用第四阶段的模板生成AUP |
5. **“审计[系统]的偏见情况”** **根据第五阶段的流程设计和执行偏见测试** |
6. **“为[系统]创建模型卡片”** **填写第六阶段的模型卡片模板** |
7. **“我们发生了人工智能事件”** **激活第七阶段的事件响应手册** |
8. **“规划我们的人工智能合规性”** **根据第八阶段的清单进行合规性检查** |
9. **“设计我们的人工智能伦理委员会”** **使用第九阶段的模板生成章程** |
10. **“生成我们的人工智能治理仪表板”** **使用第十阶段的仪表板构建治理健康评分** |
11. **“审查我们的人工智能政策”** **根据第十一阶段的生成式人工智能治理框架进行审核** |
12. **“规划人工智能素养培训”** **根据第十二阶段的对象群体设计培训计划**