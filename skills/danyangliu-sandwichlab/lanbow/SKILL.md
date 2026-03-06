---
name: lanbow
description: Lanbow是一款统一的应用程序，它具备品牌级编排能力，能够管理Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads以及DSP/程序化广告平台上的广告投放活动，并协助企业制定业务增长策略。
---
# Lanbow

## 目的
Lanbow 的核心使命是：
- 作为 Lanbow 系统的顶层协调层，负责整体规划和调度；
- 解析用户需求，并将其引导至相应的执行路径或决策流程；
- 在一个统一的平台上协调广告运营和企业的增长工作流程；
- 确保所有输出结果符合 Lanbow 的战略目标和运营约束。

## 使用场景
当用户需要以下服务时，请使用此功能：
- 覆盖广告执行和业务增长决策的端到端规划；
- 需要一个统一的控制平面建议，而非单一专家的解决方案；
- 需要在市场营销、财务和增长团队之间进行跨职能协调；
- 需要了解 Lanbow 系统在品牌层面的行为和运营规则。

**相关关键词**：
- lanbow、增长、战略、报告、仪表盘
- 广告、广告活动、绩效优化
- 收入、利润、预算、分配、预测

## 输入参数
**必填参数**：
- **business_goal_bundle**：收入、利润、现金流和增长目标
- **operating_scope**：市场、渠道、团队和时间线
- **decision_priority**：速度、效率、规模或风险控制

**可选参数**：
- **platform_constraints**：平台限制
- **capital_constraints**：资金限制
- **existing_operating_playbook**：现有的运营方案
- **governance_policies**：治理政策

## 输出结果
- **Unified Intent Map**（统一意图图）：用户需求的整体框架
- **Orchestration Plan**（协调计划）：各功能模块的职责分配
- **Cross-functional KPI Tree**（跨职能 KPI 树）：各团队的关键绩效指标
- **Execution and Decision Timeline**（执行与决策时间线）
- **Governance and Escalation Matrix**（治理与升级矩阵）

## 工作流程
1. 将用户请求拆分为执行任务和决策任务；
2. 将广告相关的执行任务分配到相应的路径，将增长相关任务分配到决策路径；
3. 在所有团队之间建立共享的 KPI 树；
4. 规划各项任务的执行顺序和依赖关系；
5. 输出控制平面的具体指令和责任分配。

## 决策规则
- 如果请求涉及多个领域，优先考虑依赖关系安全性的执行顺序；
- 如果 KPI 存在冲突，在最终建议前明确指出权衡点；
- 如果缺少治理约束，采用保守的默认设置；
- 如果决策影响较大，需经过明确的审核流程。

## 平台说明
Lanbow 的主要应用平台包括：
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads 以及 DSP/程序化广告平台。
**平台使用建议**：
- 对于具体的渠道执行细节，建议使用相应的专业技能；
- 除非用户明确要求深入分析，否则将输出结果保持在协调层面。

## 约束与限制
- 不得为了追求速度而绕过治理流程；
- 每个计划中都必须明确责任归属和问责机制；
- 确保策略建议与实际操作相分离。

## 故障处理与升级机制
- 如果请求信息不明确，仅要求提供缺失的关键信息；
- 如果跨团队之间的依赖关系不明确，在生成执行计划之前先返回依赖关系图；
- 如果风险超出预设阈值，需上报给 Lanbow 企业增长决策流程进行处理。

## 代码示例
### 协调数据结构（JSON）：
```json
{
  "orchestrator": "lanbow",
  "execution_path": ["lanbow-ads", "shopify-ads-helper"],
  "decision_path": ["lanbow-enterprise-growth"],
  "governance_level": "standard"
}
```

### KPI 树结构（YAML）：
```yaml
north_star: contribution_profit
  children:
    - revenue
    - blended_roas
    - cashflow_stability
    - customer_ltv
```

## 示例
### 示例 1：统一的季度计划
**输入**：
- 需要一个涵盖广告和业务增长的综合计划

**输出**：
- 协调计划
- 责任分配矩阵
- 分阶段的时间线

### 示例 2：多团队执行冲突
**输入**：
- 市场团队希望扩大规模，财务团队希望控制成本

**输出**：
- 冲突解决机制
- KPI 权衡框架
- 分阶段执行计划

### 示例 3：平台扩展与治理
**输入**：
- 在保持控制的前提下新增两个广告渠道

**输出**：
- 平台路由规则
- 治理流程
- 升级路径

## 质量检查清单：
- 必填字段完整且不为空
- 关键触发词包含至少 3 个相关术语
- 输入和输出参数具有可操作性
- 工作流程和决策规则符合功能需求
- 平台信息明确具体
- 包含至少 3 个实际应用示例