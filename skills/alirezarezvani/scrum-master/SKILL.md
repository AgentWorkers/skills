---
name: "scrum-master"
description: "高级Scrum Master技能：用于数据驱动的敏捷团队分析与指导。当用户咨询冲刺计划、进度跟踪、回顾会议组织、待办事项整理、故事点估算、燃尽图制作、障碍物解决或敏捷团队健康状况时，可提供专业支持。通过运行Python脚本来分析从Jira或其他类似工具导出的冲刺数据：`velocity_analyzer.py`用于蒙特卡洛冲刺预测；`sprint_health_scorer.py`用于多维度团队健康状况评估；`retrospective_analyzer.py`用于跟踪改进措施和讨论主题。能够为表现优异的Scrum团队生成置信区间预测报告、健康状况评估报告以及进度提升趋势分析。"
license: MIT
metadata:
  version: 2.0.0
  author: Alireza Rezvani
  category: project-management
  domain: agile-development
  updated: 2026-02-15
  python-tools: velocity_analyzer.py, sprint_health_scorer.py, retrospective_analyzer.py
  tech-stack: scrum, agile-coaching, team-dynamics, data-analysis
---
# Scrum Master专家

这位Scrum Master具备数据驱动的技能，结合了Sprint分析、概率预测以及团队发展辅导。其独特价值在于三款Python分析脚本及其工作流程——更多关于框架的详细信息，请参阅`references/`和`assets/`。

---

## 目录

- [分析工具与使用方法](#analysis-tools--usage)
- [输入要求](#input-requirements)
- [Sprint执行工作流程](#sprint-execution-workflows)
- [团队发展工作流程](#team-development-workflow)
- [关键指标与目标](#key-metrics--targets)
- [局限性](#limitations)

---

## 分析工具与使用方法

### 1. 速度分析器 (`scripts/velocity_analyzer.py`)

该工具可以计算Sprint历史的滚动平均值、线性回归趋势，并进行蒙特卡洛模拟。

**输出**：速度趋势（提升/稳定/下降）、变异系数、50%/70%/85%/95%置信区间的6个Sprint的蒙特卡洛预测结果，以及带有根本原因建议的异常标志。

**验证**：如果输入数据中包含的Sprint少于3个，系统会停止运行并提示用户：“速度分析至少需要3个Sprint的数据。请提供更多Sprint数据。”建议使用6个或更多的Sprint数据以获得具有统计意义的蒙特卡洛预测结果。

---

### 2. Sprint健康评分器 (`scripts/sprint_health_scorer.py`)

该工具从6个维度对团队健康状况进行评分，生成0–100分的总分。

| 维度 | 权重 | 目标 |
|---|---|---|
| 承诺可靠性 | 25% | 超过85%的Sprint目标得以实现 |
| 范围稳定性 | 20% | 中期Sprint内的变更次数低于15% |
| 障碍物解决时间 | 15% | 平均解决时间少于3天 |
| 仪式参与度 | 15% | 参与度超过90% |
| 故事完成情况 | 15% | 完成故事的比例较高 |
| 速度可预测性 | 10% | 变异系数（CV）低于20% |

**输出**：总体健康评分及各个维度的得分、建议措施、Sprint间的趋势变化，以及干预优先级矩阵。

**验证**：需要至少2个包含仪式数据和故事完成情况的Sprint才能进行评分。如果数据缺失，系统会报告无法评分的维度，并要求用户补充相应数据。

---

### 3. 回顾分析器 (`scripts/retrospective_analyzer.py`

该工具跟踪行动项的完成情况、反复出现的主题以及团队成熟度的变化。

**输出**：按优先级和负责人划分的行动项完成率、反复出现的主题的持续程度、团队成熟度等级（形成期/冲突期/规范期/执行期），以及速度提升的趋势。

**验证**：至少需要3次包含行动项跟踪的回顾会议才能使用该工具。如果回顾会议次数较少，系统会提示这一限制，并仅提供部分主题分析结果。

---

## 输入要求

所有脚本都接受符合`assets/sample_sprint_data.json`中定义的JSON格式的数据：

Jira等工具可以导出Sprint数据；在运行脚本之前，请将导出的字段映射到该JSON格式。请参阅`assets/sample_sprint_data.json`以获取包含6个Sprint的示例数据，以及`assets/expected_output.json`以了解预期的输出结果（平均速度20.2分，变异系数12.7%，健康评分78.3/100，行动项完成率46.7%）。

---

## Sprint执行工作流程

### Sprint规划

1. 运行速度分析：`python velocity_analyzer.py sprint_data.json --format text`
2. 将70%置信区间作为Sprint待办事项的推荐上限。
3. 查看健康评分器的“承诺可靠性”和“范围稳定性”得分，以便与产品负责人进行协商。
4. 如果蒙特卡洛预测显示波动性较高（变异系数CV >20%），应以范围估计而非单一预测值的形式向相关方展示。
5. 记录团队能力假设（如人员离开、依赖关系等），以便在回顾会议中进行对比。

### 每日站会

1. 记录参与情况和求助行为，并在Sprint结束时将数据输入`sprint_health_scorer.py`。
2. 记录每个障碍物的开始日期；解决时间将影响“障碍物解决时间”维度的评分。
3. 如果障碍物在2天内未解决，需主动上报并在Sprint数据中记录。

### Sprint回顾

1. 在演示过程中展示速度趋势和健康评分，以便向相关方提供项目进展的背景信息。
2. 记录在回顾会议中提出的范围变更请求，并将其作为范围变更事件记录在Sprint数据中，以供下一次评分使用。

### Sprint回顾会议

1. 在会议开始前运行这三个脚本：
   ```bash
   python sprint_health_scorer.py sprint_data.json --format text > health.txt
   python retrospective_analyzer.py sprint_data.json --format text > retro.txt
   ```
2. 以健康评分和标记为高风险的维度作为讨论的重点。
3. 根据回顾分析器的行动项完成率来判断团队实际能处理的新行动项数量（如果完成率低于60%，目标为≤3个）。
4. 在会议结束前为每个行动项分配负责人和可衡量的成功标准。
5. 将新的行动项记录在`sprint_data.json`中，以便在下一个周期中进行跟踪。

---

## 团队发展工作流程

### 评估

**将回顾分析器的成熟度结果与相应的团队发展阶段对应起来**。
- 结合匿名心理安全度调查（Edmondson 7点量表）和个人一对一观察结果进行评估。
- 如果团队处于“形成期”或“冲突期”，优先考虑提升心理安全度和促进团队协作的干预措施。

### 干预措施

根据团队发展阶段采取相应的引导措施（详细信息见`references/team-dynamics-framework.md`）：

| 阶段 | 重点 |
|---|---|
| 形成期 | 建立结构、流程培训、建立信任 |
| 冲突期 | 促进冲突解决、维护心理安全 |
| 规范期 | 增强团队自主性、明确流程责任 |
| 执行期 | 引入挑战、支持创新 |

### 进度测量

- **Sprint节奏**：定期重新运行健康评分器，目标为每季度整体评分提升5分以上。
- **每月**：进行心理安全度调查，目标为心理安全度得分超过4.0/5.0。
- **每季度**：通过回顾分析器重新评估团队成熟度。
- 如果连续两个Sprint的评分停滞或下降，需调整干预策略（详见`references/team-dynamics-framework.md`）。

---

## 关键指标与目标

| 指标 | 目标 |
|---|---|
| 总体健康评分 | 超过80/100 |
| 心理安全指数 | 超过4.0/5.0 |
| 速度变异系数（可预测性） | 低于20% |
| 承诺可靠性 | 超过85% |
| 范围稳定性 | 中期Sprint内的变更次数低于15% |
| 障碍物解决时间 | 小于3天 |
| 仪式参与度 | 超过90% |
| 回顾会议中行动项的完成率 | 超过70% |

---

## 局限性

- **样本量**：如果Sprint数量少于6个，蒙特卡洛预测的置信度会降低；请始终提供置信区间，而非单一预测值。
- **数据完整性**：如果缺少仪式或故事完成数据，相关评分维度将受到影响——请明确报告数据缺失的情况。
- **环境敏感性**：脚本的建议措施需结合组织环境和团队实际情况进行解读（这些信息在JSON数据中可能无法体现）。
- **定量偏差**：这些指标不能替代定性观察；应将评分结果与团队的实际互动情况结合起来评估。
- **团队规模**：这些方法适用于5–9人的团队；人数较多的团队可能需要调整。
- **外部因素**：跨团队依赖关系和组织约束无法通过单一团队的指标完全反映。

---

## 相关技能

- **敏捷产品负责人**（`product-team/agile-product-owner/`）——用户故事和待办事项的整理有助于Sprint规划。
- **高级项目经理**（`project-management/senior-pm/`）——项目组合的健康发展状况会影响Sprint的优先级制定。

*如需深入了解框架细节，请参阅`references/velocity-forecasting-guide.md`和`references/team-dynamics-framework.md`。相关模板文件请参见`assets/sprint_report_template.md`和`assets/team_health_check_template.md`。*