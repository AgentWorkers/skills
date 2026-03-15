---
name: compoundos
description: Design, implement, and operate a self-improving AI Operating System for business with 9 components: Strategic Layer, Prioritization Engine, Knowledge Management, Central Ops, Department Agents (ACRA), Projects, Auto-Capture, Communication Layer, and Metrics & Monitoring. Use when building AI-powered business operations systems, implementing agentic workflows, creating department-specific AI teams, establishing business intelligence systems, or setting up compounding intelligence architectures with learning loops.
---

# CompoundOS – 人工智能操作系统实现

## 核心概念

CompoundOS 是一个能够自我提升的人工智能操作系统，它消除了“上下文丢失”的问题——即分散的人工智能工具会导致数据不连贯和上下文缺失。该系统通过学习循环每天不断积累智能。

**主要优势：**
- **自我提升**：每个任务都能让系统变得更智能。
- **自主构建工具**：人工智能能够自行开发工具或工作流程，无需购买 SaaS 服务。
- **无缝协作**：消除瓶颈，实现高效、系统化的协同工作。

## 快速入门：三步实现流程

### 第一步：定义战略层（组件 1）

创建包含以下内容的文档：

**必填字段：**
- **核心目标（Big Obsessional Goal, BOG）**：你的主要目标。
- **当前瓶颈**：阻碍进展的最关键问题。
- **目标受众**：你的服务对象及其需求。
- **竞争优势**：你的独特优势。

模板请参见 [assets/strategy-template.md](assets/strategy-template.md)。

### 第二步：将战略文档输入到人工智能代理中

将战略文档作为代理的永久指令，确保：
- 每个决策都符合战略要求。
- 代理能够拒绝不符合战略要求的请求。
- 上下文在会话之间得到保持。

### 第三步：执行过滤机制

始终以“首席运营官”的身份与人工智能交互：
1. 在执行任务前查看战略文档。
2. 根据业务目标对任务进行评估。
3. 每天确定一个需要立即执行的行动。

## 实现工作流程

### 第一阶段：基础建设（组件 1-3）

1. **战略层**：定义系统的核心功能（见上文）。
2. **优先级引擎**：设置每日审查机制：
   - 根据战略评估待办事项。
   - 为任务分配优先级。
   - 确定当天需要执行的唯一一个行动。
3. **知识管理**：建立知识存储系统：
   - 记录见解、决策和结果。
   - 按部门或项目自动分类。
   - 新任务启动前可快速检索相关信息。

详细实现步骤请参见 [references/knowledge-setup.md](references/knowledge-setup.md)。

### 第二阶段：执行层（组件 4-6）

4. **中央运营**：构建工作流程自动化：
   - 为可重复的过程制定标准操作程序（SOP）。
   - 创建自动化任务流程。
   - 确保流程的可重复性。

5. **部门代理**：部署部门专用代理：
   - 代理模板请参见 [references/department-agents.md](references/department-agents.md)。
   - 每个代理仅负责处理与部门相关的工作。
   - 不同部门拥有不同的专业功能。

6. **项目协作**：建立跨部门协作机制：
   - 当项目涉及多个部门时，确保信息共享。
   **示例**：产品发布需要跨部门协作。

### 第三阶段：学习层（组件 7-9）

7. **自动记录**：实现自我提升：
   - 记录所有决策、行动和结果。
   - 将数据输入知识管理系统。
   - 详细内容请参见 [references/learning-loop.md](references/learning-loop.md)。

8. **通信层**：建立数据传输通道：
   - 人机交互：语音、文本、结构化输入。
   - 机器间交互：API、客户关系管理（CRM）、Webhook。

9. **指标与监控**：建立监控机制：
   - 监控系统运行情况（每日、每周、每月、每季度、每年）。
   - 将性能数据反馈给战略层。

## ACRA 框架快速参考

部门代理遵循 ACRA 结构：

| 部门 | 缩写 | 重点 | 示例功能 |
|------------|---------|-------|---------------------|
| **A**ttract（吸引） | A | 流量管理、内容创作 | YouTube 流媒体发布、广告制作、搜索引擎优化（SEO） |
| **C**onvert（转化） | C | 销售与文案撰写 | 营销渠道优化、客户拓展 |
| **R**etain（留存） | R | 客户成功管理 | 新用户引导、客户生命周期价值（LTV）管理、客户支持 |
| **A**scend（提升） | A | 产品交付 | 新功能发布、追加销售 |

**支持职能**：根据需要可包括财务、人力资源（HR）、法律等部门。

代理提示模板请参见 [references/department-prompts.md](references/department-prompts.md)。

## 复利循环

**效果：**你的人工智能系统每天都在变得更智能。

## 组件间的依赖关系**

- **战略层** → 指导优先级引擎（组件 2）。
- **自动记录** → 为知识管理提供数据（组件 3）。
- **部门代理** → 使用中央运营系统执行工作流程（组件 4-5）。
- **指标系统** → 将数据反馈给战略层（组件 1-9）。
- **通信层** → 连接所有组件（组件 8）。

## 常见问题及解决方法

### 上下文丢失

**症状**：人工智能忘记之前的决策或上下文。

**解决方法：**
- 确保自动记录功能正常运行。
- 检查知识管理系统能否正常检索信息。
- 确认战略层被正确应用于决策过程。

### 决策困难

**症状**：优先级过多，难以做出选择。

**解决方法：**
- 强化优先级引擎的评估能力。
- 每天只执行一个关键任务。
- 重新审视战略规划以明确方向。

### 部门间孤立

**症状**：团队之间缺乏信息共享，导致重复工作。

**解决方法：**
- 通过项目推动跨部门协作。
- 确保信息传递机制有效运行。
- 检查通信层是否正常工作。

### 学习效果不佳

**症状**：系统智能提升缓慢。

**解决方法：**
- 确保自动记录功能正常运行。
- 检查知识管理系统能否提取有用的信息。
- 确保指标反馈机制有效传递给战略层。

## 最佳实践

1. **从小处着手**：先实现组件 1-3，再逐步扩展。
2. **先规划再建设**：战略层必须完善后再开始实施。
3. **全面记录**：自动记录功能必不可少。
4. **每天一个任务**：通过优先级引擎保持专注。
5. **定期回顾**：定期更新战略规划。
6. **持续优化**：通过学习循环不断改进战略。

## 参考资料

| 主题 | 参考文档 |
|-------|-----------|
| 知识管理设置 | [references/knowledge-setup.md](references/knowledge-setup.md) |
| 部门代理模板 | [references/department-agents.md](references/department-agents.md) |
| 指标与运营节奏 | [references/metrics-cadence.md](references/metrics-cadence.md) |
| 学习循环与自动记录 | [references/learning-loop.md](references/learning-loop.md) |
| 战略层模板 | [assets/strategy-template.md](assets/strategy-template.md) |
| 部门提示模板 | [assets/department-prompts.md](assets/department-prompts.md) |

## 适用场景

- 构建基于人工智能的业务运营系统。
- 实现具有部门专业性的自动化工作流程。
- 开发能够自我提升的商业智能系统。
- 解决多个人工智能工具之间的信息不一致问题。
- 建立智能系统的持续优化机制。
- 设计跨部门协作的人工智能代理团队。

---

*CompoundOS：让你的商业智能每天都在不断成长。*