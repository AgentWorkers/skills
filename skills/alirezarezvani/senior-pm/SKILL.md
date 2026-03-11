---
name: "senior-pm"
description: 企业软件、SaaS 产品及数字化转型项目的高级项目经理。专注于项目组合管理、定量风险分析、资源优化、利益相关者协调以及高管层报告的编制。掌握多种先进方法论，包括 EMV 分析、蒙特卡洛模拟（Monte Carlo simulation）、WSJF 优先级排序（WSJF prioritization）以及多维度项目健康状况评估（multi-dimensional health scoring）。当用户需要关于项目计划、项目状态报告、风险评估、资源分配、项目路线图、里程碑跟踪、团队能力规划、项目组合健康状况审查、项目管理或高管层项目报告的帮助时，可提供专业支持——尤其适用于涉及多个工作流、复杂依赖关系或预算高达数百万美元的企业级项目。
---
# 高级项目管理专家

## 概述

专注于企业软件、SaaS 产品以及数字化转型项目的战略项目管理。提供项目组合管理功能、定量分析工具以及适用于复杂多项目组合的高层报告框架。

### 核心专长领域

**项目组合管理与战略对齐**
- 使用先进的优先级排序模型（WSJF、RICE、ICE、MoSCoW）对多项目组合进行优化
- 制定与业务目标和市场状况相一致的战略路线图
- 在整个项目组合中进行资源容量规划和分配优化
- 通过多维度评分框架监控项目组合的健康状况

**定量风险管理**
- 使用预期货币价值（EMV）分析来量化财务风险
- 通过蒙特卡洛模拟进行进度风险建模和置信区间计算
- 实施具有企业级风险容忍度的风险偏好框架
- 分析项目组合中的风险相关性并制定多元化策略

**高层沟通与治理**
- 为董事会准备包含风险等级（RAG）状态和战略建议的报告
- 通过复杂的 RACI 矩阵和升级路径来协调利益相关者的意见
- 通过风险调整后的投资回报率（ROI）和净现值（NPV）计算来跟踪财务绩效
- 为大规模数字化转型制定变更管理策略

## 方法论与框架

### 三层分析方法

**第一层：项目组合健康状况评估**
使用 `project_health_dashboard.py` 进行全面的多维度评分：

```bash
python3 scripts/project_health_dashboard.py assets/sample_project_data.json
```

**健康状况评估维度（加权评分）：**
- **时间线表现**（25% 权重）：进度遵守情况、里程碑达成情况、关键路径分析
- **预算管理**（25% 权重）：支出偏差、预测准确性、成本效率指标
- **范围交付**（20% 权重）：功能完成率、需求满足情况、变更控制
- **质量指标**（20% 权重）：代码覆盖率、缺陷密度、技术债务、安全状况
- **风险暴露**（10% 权重）：风险评分、缓解措施的有效性、风险暴露趋势

**风险等级（RAG）状态计算：**
- 🟢 绿色：综合评分 >80，所有维度 >60
- 🟡 黄色：综合评分 60-80，或任意维度 40-60
- 🔴 红色：综合评分 <60，或任意维度 <40

**第二层：风险矩阵与缓解策略**
使用 `risk_matrix_analyzer.py` 进行定量风险评估：

```bash
python3 scripts/risk_matrix_analyzer.py assets/sample_project_data.json
```

**风险量化流程：**
1. **概率评估**（1-5 分级）：历史数据、专家判断、蒙特卡洛模拟输入
2. **影响分析**（1-5 分级）：财务、进度、质量和战略影响
3. **类别权重**：技术（1.2 倍）、资源（1.1 倍）、财务（1.4 倍）、进度（1.0 倍）
4. **EMV 计算**：

```python
# EMV and risk-adjusted budget calculation
def calculate_emv(risks):
    category_weights = {"Technical": 1.2, "Resource": 1.1, "Financial": 1.4, "Schedule": 1.0}
    total_emv = 0
    for risk in risks:
        score = risk["probability"] * risk["impact"] * category_weights[risk["category"]]
        emv = risk["probability"] * risk["financial_impact"]
        total_emv += emv
        risk["score"] = score
    return total_emv

def risk_adjusted_budget(base_budget, portfolio_risk_score, risk_tolerance_factor):
    risk_premium = portfolio_risk_score * risk_tolerance_factor
    return base_budget * (1 + risk_premium)
```

**根据风险评分划分的风险应对策略：**
- **避免**（>18）：通过调整范围或方法来消除风险
- **缓解**（12-18）：通过积极干预来降低风险概率或影响
- **转移**（8-12）：通过保险、合同、合作伙伴关系来转移风险
- **接受**（<8）：通过应急计划进行监控

**第三层：资源容量优化**
使用 `resource_capacity_planner.py` 进行项目组合资源分析：

```bash
python3 scripts/resource_capacity_planner.py assets/sample_project_data.json
```

**容量分析框架：**
- **利用率优化**：目标利用率在 70-85% 之间，以实现可持续的生产力
- **技能匹配**：基于算法的资源分配，以最大化效率
- **瓶颈识别**：识别项目组合中的关键路径资源约束
- **情景规划**：进行资源重新分配的假设分析

### 高级优先级排序模型

根据具体情况选择最合适的优先级排序模型：

**加权最短工作优先级（WSJF）** —— 适用于资源受限的敏捷项目组合，具有可量化的延迟成本
```python
def wsjf(user_value, time_criticality, risk_reduction, job_size):
    return (user_value + time_criticality + risk_reduction) / job_size
```

**RICE** —— 适用于可量化达成指标的客户导向型项目
```python
def rice(reach, impact, confidence_pct, effort_person_months):
    return (reach * impact * (confidence_pct / 100)) / effort_person_months
```

**ICE** —— 在头脑风暴或分析时间有限时快速进行优先级排序
```python
def ice(impact, confidence, ease):
    return (impact + confidence + ease) / 3
```

**模型选择决策逻辑：**
```
if resource_constrained and agile_methodology and cost_of_delay_quantifiable:
    → WSJF
elif customer_facing and reach_metrics_available:
    → RICE
elif quick_prioritization_needed or ideation_phase:
    → ICE
elif multiple_stakeholder_groups_with_differing_priorities:
    → MoSCoW
elif complex_tradeoffs_across_incommensurable_criteria:
    → Multi-Criteria Decision Analysis (MCDA)
```

参考文档：`references/portfolio-prioritization-models.md`

### 风险管理框架

参考文档：`references/risk-management-framework.md`

**步骤 1：按类别分类风险**
- 技术风险：架构、集成、性能
- 资源风险：可用性、技能、人员保留
- 进度风险：依赖关系、关键路径、外部因素
- 财务风险：预算超支、货币波动、经济因素
- 商业风险：市场变化、竞争压力、战略调整

**步骤 2：为蒙特卡洛模拟提供三点估算**
```python
def three_point_estimate(optimistic, most_likely, pessimistic):
    expected = (optimistic + 4 * most_likely + pessimistic) / 6
    std_dev = (pessimistic - optimistic) / 6
    return expected, std_dev
```

**步骤 3：项目组合风险相关性分析**
```python
import math

def portfolio_risk(individual_risks, correlations):
    # individual_risks: list of risk EMV values
    # correlations: list of (i, j, corr_coefficient) tuples
    sum_sq = sum(r**2 for r in individual_risks)
    sum_corr = sum(2 * c * individual_risks[i] * individual_risks[j]
                   for i, j, c in correlations)
    return math.sqrt(sum_sq + sum_corr)
```

**风险偏好框架：**
- **保守型**：风险评分 0-8，预留 25-30% 的应急资金
- **中等型**：风险评分 8-15，预留 15-20% 的应急资金
- **激进型**：风险评分 15+，预留 10-15% 的应急资金

## 资产与模板

### 项目章程模板
参考文档：`assets/project_charter_template.md`

**包含 12 个部分的全面项目章程：**
- 包含战略对齐的高层摘要
- 带有关键绩效指标（KPI）和质量标准的成功标准
- 明确决策权限的 RACI 矩阵
- 包含风险评估和缓解策略的文档
- 带有应急分析的预算分解
- 包含关键路径依赖关系的时间线

### 高层报告模板
参考文档：`assets/executive_report_template.md`

**董事会级别的项目组合报告包括：**
- 显示风险等级（RAG）状态和趋势分析的仪表板
- 财务绩效与战略目标的对比
- 带有缓解措施状态的风险热图
- 资源利用情况和容量分析
- 包含投资回报率（ROI）预测的前瞻性建议

### RACI 矩阵模板
参考文档：`assets/raci_matrix_template.md`

**企业级责任分配包括：**
- 详细的利益相关者名单及决策权限
- 从项目启动到部署各阶段的 RACI 分配
- 带有时间线和权限级别的升级路径
- 沟通协议和会议框架
- 冲突解决流程及治理整合

### 样本项目组合数据
参考文档：`assets/sample_project_data.json`

**包含多个项目的实际项目组合：**
- 不同阶段和优先级的 4 个项目
- 完整的财务数据（预算、实际支出、预测）
- 带有利用率指标的资源分配
- 带有概率/影响评分的风险登记册
- 质量指标和利益相关者满意度数据
- 依赖关系和里程碑跟踪

### 预期输出示例
参考文档：`assets/expected_output.json`

**展示脚本功能包括：**
- 项目组合健康状况评分和风险等级（RAG）状态
- 风险矩阵可视化及缓解措施优先级
- 资源容量分析及优化建议
- 整合示例，展示各项输出如何相互补充

## 实施工作流程

### 项目组合健康状况审查（每周）

1. **数据收集与验证**
   ```bash
   python3 scripts/project_health_dashboard.py current_portfolio.json
   ```
   ⚠️ 如果任何项目的综合评分 <60 或关键数据字段缺失，请停止操作并解决数据完整性问题后再继续。

2. **风险评估更新**
   ```bash
   python3 scripts/risk_matrix_analyzer.py current_portfolio.json
   ```
   ⚠️ 如果任何风险评分 >18（避免风险阈值），请停止操作并立即向项目发起人报告后再继续。

3. **容量分析**
   ```bash
   python3 scripts/resource_capacity_planner.py current_portfolio.json
   ```
   ⚠️ 如果任何团队的利用率 >90% 或 <60%，请标记出来，以便在步骤 4 之前立即讨论资源重新分配。

4. **高层报告生成**
   - 将各项输出整合成高层报告格式
   - 突出关键问题和建议
   - 准备与利益相关者的沟通材料

### 每月战略审查

1. **项目组合优先级评估**
   - 应用 WSJF/RICE/ICE 模型评估当前优先级
   - 评估与业务目标的战略对齐情况
   - 识别优化机会

2. **项目组合风险分析**
   - 更新风险偏好和容忍度
   - 审查项目组合中的风险相关性和集中度
   - 调整风险缓解措施

3. **资源优化规划**
   - 分析即将到来季度的资源限制
   - 规划资源重新分配和招聘策略
   - 识别技能缺口和培训需求

4. **利益相关者协调会议**
   - 展示项目组合健康状况和战略建议
   - 收集关于优先级和资源分配的反馈
   - 就即将到来季度的优先级和投资达成共识

### 季度项目组合优化

1. **战略对齐评估**
   - 评估项目组合对业务目标的贡献
   - 评估市场和竞争状况的变化
   - 更新战略优先级和成功标准

2. **财务绩效审查**
   - 分析项目组合中的风险调整后投资回报率（ROI）
   - 审查预算绩效和预测准确性
   - 优化投资分配以获得最大价值

3. **能力差距分析**
   - 识别新兴技术和技能需求
   - 规划能力建设投资
   - 评估自建与外包或合作的决策

4. **项目组合再平衡**
   - 应用三阶段模型进行创新平衡
   - 使用效率前沿优化风险回报比
   - 规划新项目和淘汰项目的决策

## 集成策略

### Atlassian 集成
- **Jira**：项目组合仪表板、跨项目指标、风险跟踪
- **Confluence**：战略文档、高层报告、知识管理
- 使用 MCP 集成自动化数据收集和报告生成

### 财务系统集成
- **预算跟踪**：实时支出数据用于偏差分析
- **资源成本核算**：每小时费用和利用率用于容量规划
- **ROI 测量**：根据预测值跟踪价值实现情况

### 利益相关者管理
- **高层仪表板**：实时项目组合健康状况可视化
- **团队看板**：单个项目的绩效指标
- **风险登记册**：协作式风险管理及自动化的风险升级流程

## 交接协议

### 与 Scrum Master 的交接
**传递以下内容：**
- 战略优先级和成功标准
- 资源分配和团队组成
- 需要在冲刺层面关注的风险因素
- 质量标准和验收标准

**持续协作：**
- 每周的速度和健康状况指标审查
- 用于项目组合学习的冲刺回顾
- 障碍物升级和解决支持
- 团队能力和利用率反馈

### 与产品经理的交接
**传递以下内容：**
- 战略背景信息：市场优先级和竞争分析
- 用户价值框架和衡量标准
- 与项目组合目标对齐的功能优先级
- 资源和时间线限制

**提供决策支持：**
- 功能投资的 ROI 分析
- 产品决策的风险评估
- 市场情报和客户反馈整合
- 战略路线图的对齐和依赖关系

### 与执行团队的交接
**传递以下内容：**
- 战略方向：业务目标更新和优先级变更
- 预算分配和资源审批决策
- 风险偏好和容忍度调整
- 市场策略和竞争响应决策

**绩效期望：**
- 项目组合健康状况和价值交付目标
- 时间线和里程碑承诺
- 质量标准和合规要求

## 成功指标与关键绩效指标（KPIs）

参考文档：`references/portfolio-kpis.md` 以获取完整定义和测量指南。

### 项目组合绩效**
- 按时交付率：在计划时间内的交付率 >80%
- 预算偏差：项目组合平均偏差 <5%
- 质量评分：综合评分 >85%
- 风险缓解覆盖率：90% 的风险有相应的缓解措施
- 资源利用率：平均利用率在 75-85% 之间

### 战略价值**
- 投资回报率（ROI）：12 个月内超过 90% 的项目达到预期
- 战略对齐度：95% 的投资与业务优先级一致
- 创新平衡：70% 的投资用于运营，20% 用于增长，10% 用于转型
- 利益相关者满意度：高层平均满意度 >8.5 分

### 风险管理**
- 风险暴露：保持在批准的风险容忍范围内
- 解决时间：中等风险 <30 天，高风险 <7 天
- 缓解成本效率：缓解措施成本低于项目组合总风险的 20%
- 风险预测准确性：风险概率评估的准确率 >70%

## 持续改进框架

### 项目组合学习整合
- 从已完成的项目中总结经验教训
- 根据历史数据更新风险概率评估
- 通过回顾性分析提高估算准确性
- 在项目团队之间分享最佳实践

### 方法论改进**
- 定期评估优先级排序模型的有效性
- 根据行业最佳实践更新风险框架
- 整合新的工具和技术以提高分析效率
- 与行业项目组合绩效标准进行对比

### 利益相关者反馈整合**
- 每季度进行利益相关者满意度调查
- 收集关于决策支持质量的执行层反馈
- 团队对流程效率和效果的反馈
- 项目组合决策对客户影响的评估

## 相关技能

- **产品策略师**（`product-team/product-strategist/`）：产品 OKR 与项目组合目标对齐
- **Scrum Master**（`project-management/scrum-master/`）：冲刺速度数据用于项目组合健康状况仪表板