---
name: "product-manager-toolkit"
description: 这是一个为产品经理设计的综合工具包，包含RICE优先级排序方法、客户访谈分析工具、产品需求文档（PRD）模板、发现框架以及市场推广策略等内容。该工具包可用于功能优先级的确定、用户研究结果的整理、需求文档的编写以及产品策略的制定。
---
# 产品经理工具包

这是一套用于现代产品管理的必备工具和框架，涵盖了从需求发现到产品交付的整个流程。

---

## 目录

- [快速入门](#quick-start)
- [核心工作流程](#core-workflows)
  - [功能优先级排序](#feature-prioritization-process)
  - [客户需求发现](#customer-discovery-process)
  - [产品需求文档（PRD）开发](#prd-development-process)
- [工具参考](#tools-reference)
  - [RICE 优先级评估工具](#rice-prioritizer)
  - [客户访谈分析工具](#customer-interview-analyzer)
- [输入/输出示例](#inputoutput-examples)
- [集成点](#integration-points)
- [常见误区及避免方法](#common-pitfalls-to-avoid)

---

## 快速入门

### 功能优先级排序
```bash
# Create sample data file
python scripts/rice_prioritizer.py sample

# Run prioritization with team capacity
python scripts/rice_prioritizer.py sample_features.csv --capacity 15
```

### 客户访谈分析
```bash
python scripts/customer_interview_analyzer.py interview_transcript.txt
```

### 产品需求文档（PRD）创建
1. 从 `references/prd_templates.md` 中选择模板。
2. 根据需求发现的结果填写相关内容。
3. 与工程团队讨论可行性。
4. 使用项目管理工具进行版本控制。

---

## 核心工作流程

### 功能优先级排序流程

```
Gather → Score → Analyze → Plan → Validate → Execute
```

#### 第一步：收集功能需求
- 客户反馈（支持工单、访谈记录）
- 销售需求（CRM 系统中的阻碍因素）
- 技术债务（工程团队的建议）
- 战略性项目（领导层的目标）

#### 第二步：使用 RICE 评分方法进行评估
```bash
# Input: CSV with features
python scripts/rice_prioritizer.py features.csv --capacity 20
```

详细信息请参阅 `references/frameworks.md`，了解 RICE 评分公式和指南。

#### 第三步：分析产品组合
- 评估哪些项目是“快速胜利”（短期见效），哪些是“大赌注”（长期投资）。
- 确定工作重点，避免涉及过于复杂的项目（XL 项目）。
- 检查项目组合是否符合公司战略目标。

#### 第四步：制定路线图
- 分配季度工作量。
- 识别项目之间的依赖关系。
- 制定与利益相关者的沟通计划。

#### 第五步：验证结果
在最终确定路线图之前：
- 将优先级与战略目标进行对比。
- 进行敏感性分析（假设估算错误20%会怎样？）。
- 与关键利益相关者讨论可能遗漏的问题。
- 检查功能之间的依赖关系是否完整。
- 与工程团队确认工作量估算的准确性。

#### 第六步：执行并迭代
- 与团队分享路线图。
- 监控实际工作量与预估工作量的差异。
- 每季度重新评估优先级。
- 根据反馈更新优先级排序。

---

### 客户需求发现流程

```
Plan → Recruit → Interview → Analyze → Synthesize → Validate
```

#### 第一步：规划调研
- 明确调研问题。
- 确定目标用户群体。
- 编写访谈脚本（详见 `references/frameworks.md`）。

#### 第二步：招募受访者
- 每个目标群体进行5-8次访谈。
- 包括核心用户和流失用户。
- 适当提供激励措施。

#### 第三步：进行访谈
- 使用半结构化的访谈方式。
- 重点关注用户遇到的问题，而非解决方案。
- 征得受访者同意后进行录音。
- 访谈过程中尽量少做笔记。

#### 第四步：分析访谈结果
```bash
python scripts/customer_interview_analyzer.py transcript.txt
```

提取以下信息：
- 用户的痛点及其严重程度。
- 用户的功能需求。
- 用户需要完成的任务模式。
- 用户的情绪和主要观点。
- 重要的反馈语句。

#### 第五步：整合分析结果
- 将相似的痛点归类。
- 识别常见的问题模式（出现3次以上即视为模式）。
- 使用“机会解决方案树”（Opportunity Solution Tree）将这些模式映射到产品机会上。
- 根据问题的频率和严重程度对机会进行优先级排序。

#### 第六步：验证解决方案
在开始开发之前：
- 提出解决方案的初步假设（详见 `references/frameworks.md`）。
- 使用低保真原型进行测试。
- 测量用户实际行为与用户表达的偏好。
- 根据反馈进行迭代。
- 记录分析结果，以便后续调研使用。

---

### 产品需求文档（PRD）开发流程

```
Scope → Draft → Review → Refine → Approve → Track
```

#### 第一步：选择模板
从 `references/prd_templates.md` 中选择合适的模板：
| 模板 | 适用场景 | 开发周期 |
|----------|----------|----------|
| 标准产品需求文档 | 复杂功能，跨团队协作 | 6-8周 |
| 一页产品需求文档 | 简单功能，单团队负责 | 2-4周 |
| 功能概述 | 项目探索阶段 | 1周 |
| 敏捷开发框架下的产品需求文档 | 基于冲刺的交付 | 持续更新 |

#### 第二步：起草内容
- 以问题陈述作为开头。
- 明确项目的范围。
- 明确说明不在项目范围内的内容。
- 包括线框图或原型图。

#### 第三步：多轮评审
- 工程团队：评估可行性及所需工作量。
- 设计团队：检查用户体验方面的问题。
- 销售团队：验证市场潜力。
- 技术支持团队：评估对运营的影响。

#### 第四步：根据反馈完善文档
- 解决技术上的限制。
- 调整项目范围以适应时间表。
- 记录各项权衡决策。

#### 第五步：审批与启动
- 得到利益相关者的签字确认。
- 进行冲刺计划整合。
- 与整个团队沟通项目计划。

#### 第六步：跟踪执行情况
产品发布后：
- 对比实际指标与目标。
- 进行用户反馈收集。
- 记录哪些措施有效，哪些无效。
- 更新工作量估算数据。
- 与团队分享分析结果。

---

## 工具参考

### RICE 优先级评估工具

这是一个高级的 RICE 优先级评估工具，支持产品组合分析。
- 支持自定义权重的 RICE 评分。
- 可生成基于工作量的季度路线图。
- 提供多种输出格式（文本、JSON、CSV）。

**CSV 输入格式示例：**
```csv
name,reach,impact,confidence,effort,description
User Dashboard Redesign,5000,high,high,l,Complete redesign
Mobile Push Notifications,10000,massive,medium,m,Add push support
Dark Mode,8000,medium,high,s,Dark theme option
```

**相关命令：**
```bash
# Create sample data
python scripts/rice_prioritizer.py sample

# Run with default capacity (10 person-months)
python scripts/rice_prioritizer.py features.csv

# Custom capacity
python scripts/rice_prioritizer.py features.csv --capacity 20

# JSON output for integration
python scripts/rice_prioritizer.py features.csv --output json

# CSV output for spreadsheets
python scripts/rice_prioritizer.py features.csv --output csv
```

---

### 客户访谈分析工具

这是一个基于自然语言处理（NLP）的访谈分析工具，用于提取可操作的洞察。
- 可提取用户的痛点及其严重程度。
- 识别和分类用户的功能需求。
- 识别用户需要完成的任务模式。
- 分析用户的情感和主要观点。
- 检测竞争对手的相关信息。

**相关命令：**
```bash
# Analyze interview transcript
python scripts/customer_interview_analyzer.py interview.txt

# JSON output for aggregation
python scripts/customer_interview_analyzer.py interview.txt json
```

---

## 输入/输出示例
详细内容请参阅 `references/input-output-examples.md`。

---

## 集成点

以下工具和平台可以与本工具集成功集成：
| 类别 | 平台名称 |
|----------|-----------|
| **分析工具** | Amplitude, Mixpanel, Google Analytics |
| **路线图工具** | ProductBoard, Aha!, Roadmunk, Productplan |
| **设计工具** | Figma, Sketch, Miro |
| **开发工具** | Jira, Linear, GitHub, Asana |
| **调研工具** | Dovetail, UserVoice, Pendo, Maze |
| **沟通工具** | Slack, Notion, Confluence |

**CSV 输出格式支持与大多数工具的集成：**
```bash
# Export for Jira import
python scripts/rice_prioritizer.py features.csv --output json > priorities.json

# Export for dashboard
python scripts/customer_interview_analyzer.py interview.txt json > insights.json
```

---

## 常见误区及避免方法

| 常见误区 | 描述 | 避免方法 |
|---------|-------------|------------|
| **先开发解决方案** | 在未理解问题之前就直接开始开发功能。 | 每份产品需求文档都应以问题陈述开头。 |
| **分析过度** | 花费过多时间进行研究而迟迟不发布产品。 | 为调研阶段设定时间限制。 |
| **盲目开发功能** | 在未评估影响之前就发布功能。 | 在开始开发前明确成功指标。 |
| **忽视技术债务** | 未为系统维护预留足够时间。 | 为系统维护预留20%的工作量。 |
| **利益相关者意外** | 不及时、不频繁地与利益相关者沟通。 | 每周进行异步更新，每月举行演示会议。 |
| **过度关注表面指标** | 优化表面指标而非实际用户价值。 | 将指标与用户实际获得的价值挂钩。 |

---

## 最佳实践

**编写优秀的产品需求文档（PRD）：**
- 从问题出发，而非解决方案。
- 明确列出成功指标。
- 明确说明项目范围。
- 使用可视化工具（如线框图、流程图）。
- 将技术细节放在附录中。
- 对所有更改进行版本控制。

**有效进行优先级排序：**
- 结合“快速胜利”项目和“大赌注”项目。
- 考虑延迟带来的机会成本。
- 考虑功能之间的依赖关系。
- 为意外工作预留20%的时间。
- 每季度重新评估优先级。
- 在沟通决策时提供充分的背景信息。

**客户需求发现：**
- 重复询问“为什么”，以找出问题的根本原因。
- 关注用户过去的行为，而非未来的意图。
- 避免使用引导性问题（例如“您肯定希望……”）。
- 在用户自然的环境中进行访谈。
- 注意用户的情绪反应（用户的痛点往往就是机会）。
- 用定量数据验证定性分析的结果。

---

## 快速参考

```bash
# Prioritization
python scripts/rice_prioritizer.py features.csv --capacity 15

# Interview Analysis
python scripts/customer_interview_analyzer.py interview.txt

# Generate sample data
python scripts/rice_prioritizer.py sample

# JSON outputs
python scripts/rice_prioritizer.py features.csv --output json
python scripts/customer_interview_analyzer.py interview.txt json
```

---

## 参考文档

- `references/prd_templates.md` - 不同场景下的产品需求文档模板。
- `references/frameworks.md` - 详细的技术框架文档（包括 RICE 评分方法、MoSCoW、Kano 方法、JTBD 等）。