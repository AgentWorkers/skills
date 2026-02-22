---
name: psychology-master
description: 世界级的心理学专业知识，专注于人类心智的优化。掌握学习科学（针对不同年龄段的语言学习、编程技能培养等）、认知心理学、行为经济学以及伦理营销/转化心理学的相关知识。这些知识可应用于学习程序的设计、理解人类动机、优化用户体验、制定具有说服力的信息传递策略、提高转化率以及分析人类行为模式等方面。涵盖发展心理学、记忆系统、习惯形成机制、决策偏见以及消费者心理学等内容。
---
# 心理学大师

这是一项综合了认知科学、发展心理学、学习科学以及伦理营销心理学的专业技能。它提供了基于证据的框架，帮助我们理解和优化人类行为。

## 快速入门

```
1. Identify domain → Learning OR Marketing OR Both
2. Gather context → Audience, goals, constraints
3. Apply framework → Select from references below
4. Validate → Run ethics and measurement checks
```

## 使用场景

- “为[特定年龄段]设计学习计划，以掌握[某项技能]”
- “[X岁]的孩子应该如何学习[编程/英语/数学]？”
- “如何利用心理学原理来提高转化率？”
- “如何制定具有说服力的信息，同时避免操纵行为？”
- “了解客户的决策过程”
- “打造能够培养用户习惯的产品体验”
- “为[特定主题]制定适合该年龄段的教学策略”
- “对[目标用户群体]进行行为分析”

## 核心能力

### 1. 学习心理学（针对不同年龄段）

为任何年龄段的用户设计基于证据的学习体验：

| 年龄段 | 关键原则 | 参考资料 |
|---------|----------------|-----------|
| 3-6岁 | 以游戏为基础的学习方式，注重感官体验和建立依恋关系 | `references/learning-development.md` |
| 7-12岁 | 从具体到抽象的学习过程，逐步引导学习 | `references/learning-development.md` |
| 13-17岁 | 培养自主性、自我认同感以及同伴影响 | `references/learning-development.md` |
| 18-25岁 | 强调刻意练习和元认知能力 | `references/learning-development.md` |
| 26-64岁 | 提高学习效率，促进知识迁移 | `references/learning-development.md` |
| 65岁以上 | 适应学习节奏，增强学习信心，采用多种学习方式 | `references/learning-development.md` |

**针对特定技能的指导：**
- **语言学习**：参见 `references/skill-acquisition.md#languages`
- **编程**：参见 `references/skill-acquisition.md#programming`
- **数学**：参见 `references/skill-acquisition.md#mathematics`
- **音乐/体育**：参见 `references/skill-acquisition.md#motor-skills`

### 2. 认知心理学

驱动行为的心理过程：

| 心理系统 | 应用场景 | 参考资料 |
|---------|----------------|-----------|
| 记忆 | 编码、检索、记忆间隔策略 | `references/cognitive-systems.md#memory` |
| 注意力 | 注意力集中、多任务处理、工作负荷 | `references/cognitive-systems.md#attention` |
| 决策 | 启发式思维、偏见、选择机制 | `references/cognitive-systems.md#decision` |
| 动机 | 内在动机与外在动机、目标设定 | `references/motivation-frameworks.md` |

### 3. 营销与转化心理学

运用伦理原则进行说服和转化优化：

| 框架 | 应用场景 | 参考资料 |
|---------|----------------|-----------|
| JTBD（Just Because It’s the Best） | 激发客户内在动机 | `references/marketing-psychology.md#jtbd` |
| 行为经济学 | 优化用户选择过程 | `references/marketing-psychology.md#behavioral-econ` |
| 说服科学 | 通过合法途径影响用户决策 | `references/marketing-psychology.md#persuasion` |
| 转化优化 | 提高用户转化率 | `references/conversion-optimization.md` |
| 客户旅程设计 | 设计有效的用户互动点 | `references/customer-psychology.md` |

### 4. 评估与分析

使用相关工具来提供个性化建议：

```bash
# Learner profile assessment
python scripts/learner_assessment.py --age 25 --skill coding --context work

# Conversion audit
python scripts/conversion_audit.py --funnel signup --segment new_users

# Bias detection in messaging
python scripts/bias_detector.py --copy "marketing_copy.txt"

# Search reference files
python scripts/search.py --query "habit formation" --ignore-case
```

## 工作流程

### 第一阶段：收集背景信息

收集必要的背景信息：

**学习方面：**
- 年龄和发展阶段
- 学习者的现有知识和技能
- 可用的时间和时间限制
- 学习者的动机来源
- 学习环境（使用的工具、所需的支持）

**营销方面：**
- 目标受众的人口统计特征
- 当前的转化指标
- 客户的需求和痛点
- 市场竞争状况
- 遵守的伦理规范

### 第二阶段：选择适用框架

```
Learning Task?
├── What age? → Select developmental approach
├── What skill? → Select acquisition framework
└── What constraint? → Optimize for time/depth/retention

Marketing Task?
├── Awareness stage? → Use attention + salience frameworks
├── Consideration? → Use social proof + comparison
├── Decision? → Use friction removal + risk reduction
└── Retention? → Use habit + loyalty frameworks
```

### 第三阶段：实施计划

根据详细的参考资料，制定具体可行的行动计划。

### 第四阶段：验证结果

在最终输出之前，务必按照 `references/safety-ethics.md` 中的伦理检查清单进行审核。

## 规则与限制

- **严禁提供医疗或心理治疗建议**——请咨询专业人士
- **不得进行任何诊断**——评估工具仅用于提供信息
- **所有说服手段必须符合伦理原则且透明**  
- **针对未成年人时，安全第一**——提供保守的建议，并确保有监护人参与
- **建议需根据具体情况制定**——避免一概而论
- **所有内容都必须基于证据**——引用相关的理论和原则，而非个人经历

## 输出模板

### 学习计划模板

```markdown
## Learning Plan: [Skill] for [Age/Context]

### Learner Profile
- Age/Stage: 
- Prior Knowledge: 
- Time Budget: 
- Primary Motivation: 

### Goals & Milestones
| Week | Goal | Success Indicator |
|------|------|-------------------|

### Method Mix
- Primary Method: 
- Practice Structure: 
- Feedback Mechanism: 

### Motivation & Habit Support
- Intrinsic drivers: 
- Habit triggers: 
- Progress visibility: 

### Risks & Mitigations
| Risk | Mitigation |
|------|------------|
```

### 营销/转化计划模板

```markdown
## Conversion Optimization: [Funnel Stage]

### Audience Profile
- Segment: 
- Job-to-be-Done: 
- Current Behavior: 

### Psychological Levers (Ethical)
| Lever | Application | Why It Works |
|-------|-------------|--------------|

### Messaging Hierarchy
1. Primary Promise: 
2. Proof Point: 
3. Differentiator: 
4. Risk Reducer: 

### Experiment Design
- Hypothesis: 
- Metric: 
- Segment: 
- Duration: 

### Ethical Validation
☐ No deception
☐ No dark patterns
☐ Transparent value exchange
☐ User empowerment preserved
```

## 参考资料加载指南

### 核心参考资料（8份）

| 任务 | 需要加载的参考资料 |  
|------|----------------------|  
| 儿童学习（3-12岁） | `learning-development.md`, `skill-acquisition.md` |  
| 青少年/成人学习 | `learning-development.md`, `motivation-frameworks.md` |  
| 转化优化 | `conversion-optimization.md`, `marketing-psychology.md` |  
| 消息传递/文案写作 | `marketing-psychology.md`, `customer-psychology.md` |  
| 习惯培养 | `motivation-frameworks.md`, `cognitive-systems.md` |  
| 全面评估 | 所有参考资料 + `safety-ethics.md` |  

### 扩展参考资料（12个额外领域）

| 任务 | 需要加载的参考资料 |  
|------|----------------------|  
| 团体动态与社会影响 | `social-psychology.md` |  
| 目标受众细分与人物画像 | `personality-psychology.md` |  
| 用户界面/用户体验设计 | `ux-psychology.md` |  
| 情感设计与同理心 | `emotional-intelligence.md` |  
| 基于大脑的学习原理 | `neuropsychology-basics.md` |  
| 人际沟通与反馈技巧 | `communication-psychology.md` |  
| 商务谈判与薪资协商 | `negotiation-psychology.md` |  
| 设计、品牌与视觉传达 | `color-psychology.md` |  
| 学习时机与最佳安排 | `sleep-circadian.md` |  
| 创新、思维导图与头脑风暴 | `creativity-psychology.md` |  
| 疲劳应对与心理健康 | `stress-resilience.md` |  
| 团队协作与领导力 | `organizational-psychology.md` |  

### 完整参考资料列表（共20份文件）

**学习与发展相关**：`learning-development.md`, `skill-acquisition.md`, `cognitive-systems.md`, `neuropsychology-basics.md`, `sleep-circadian.md`

**动机与行为相关**：`motivation-frameworks.md`, `stress-resilience.md`, `creativity-psychology.md`

**营销与转化相关**：`marketing-psychology.md`, `conversion-optimization.md`, `customer-psychology.md`, `color-psychology.md`

**人际与社会相关**：`social-psychology.md`, `personality-psychology.md`, `emotional-intelligence.md`, `communication-psychology.md`, `negotiation-psychology.md`

**设计与组织相关**：`ux-psychology.md`, `organizational-psychology.md`

**伦理相关**：`safety-ethics.md`