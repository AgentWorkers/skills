---
name: growth-hub
description: 这是一个高级级的编排技能，用于管理 Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads 以及 DSP（程序化广告平台）中的广告运营活动，并协助企业做出相关增长决策。
---
# Growth Hub

## 目的
核心使命：
- 作为 Growth Hub 系统的顶层协调层。
- 解析用户意图，并将其引导至正确的执行或决策路径。
- 在一个平台上协调广告操作和企业增长工作流程。
- 确保输出结果与平台战略和运营约束保持一致。

## 何时使用
当用户需要以下内容时，请使用此功能：
- 覆盖广告执行和企业增长决策的端到端规划
- 需要一个统一的控制平面建议，而不是单一专家的任务
- 需要市场、财务和增长团队之间的跨职能协调
- 需要了解平台级别的系统行为和运营规则

**高信号关键词**：
- growth hub（增长中心）、growth（增长）、strategy（战略）、report（报告）、dashboard（仪表盘）
- ads（广告）、advertising（广告活动）、campaign（广告活动）、performance（性能）、optimize（优化）
- revenue（收入）、profit（利润）、budget（预算）、allocation（分配）、forecast（预测）

## 输入契约
**必填项**：
- business_goal_bundle：收入、利润、现金流和增长目标
- operating_scope：市场、渠道、团队和时间线
- decision_priority：速度、效率、规模或风险控制

**可选项**：
- platform_constraints（平台约束）
- capital_constraints（资金约束）
- existing_operating_playbook（现有运营方案）
- governance_policies（治理政策）

## 输出契约
1. 统一的意图映射
2. 协调计划（各辅助功能/技能的具体职责）
3. 跨职能 KPI 树
4. 执行和决策时间线
5. 治理和升级矩阵

## 工作流程
1. 将请求解析为执行部分和决策部分。
2. 将执行任务路由到广告相关的路径，将增长任务路由到决策路径。
3. 在各团队之间建立共享的 KPI 树。
4. 对动作和依赖关系进行排序。
5. 输出控制平面的指令和责任分配。

## 决策规则
- 如果请求涉及多个领域，优先考虑依赖关系安全的执行顺序。
- 如果 KPI 存在冲突，在最终建议之前明确指出权衡点。
- 如果缺少治理约束，应用保守的默认值。
- 如果决策影响较大，需要经过明确的审核流程。

## 平台说明
**主要覆盖的平台**：
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads、DSP/程序化广告

**平台行为指导**：
- 对于渠道级别的执行细节，请使用专门的技能。
- 除非用户明确要求深入分析，否则将 Growth Hub 的输出结果保持在协调层面。

## 约束和限制
- 不得为了追求速度而绕过治理流程。
- 在每个计划中明确责任归属和问责机制。
- 将政策与建议分开处理。

## 故障处理和升级
- 如果请求不明确，请仅要求提供缺失的关键信息。
- 如果跨团队依赖关系不明确，在生成执行计划之前返回依赖关系映射。
- 如果风险超出阈值，将问题升级至 Growth Strategy Hub（增长策略中心）进行决策。

## 代码示例
### 协调数据（JSON 格式）

    {
      "orchestrator": "growth-hub",
      "execution_path": ["ads-execution-hub", "shopify-ads-helper"],
      "decision_path": ["growth-strategy-hub"],
      "governance_level": "standard"
    }

### KPI 树规范（YAML 格式）

    north_star: contribution_profit
    children:
      - revenue（收入）
      - blended_roas（综合 ROAS）
      - cashflow_stability（现金流稳定性）
      - customer_ltv（客户生命周期价值）

## 示例
### 示例 1：统一的季度计划
**输入**：
- 需要一个涵盖广告和企业增长的综合计划

**输出重点**：
- 协调计划
- 责任分配矩阵
- 分阶段的时间线

### 示例 2：多团队执行冲突
**输入**：
- 市场团队希望扩大规模，财务团队希望保持现金流稳定

**输出重点**：
- 冲突解决逻辑
- KPI 权衡框架
- 分阶段执行计划

### 示例 3：平台扩展与治理
**输入**：
- 在保持控制的同时新增两个渠道

**输出重点**：
- 控制平面的路由规则
- 治理流程
- 升级路径

## 质量检查清单
- [ ] 必填项齐全且不为空
- [ ] 触发关键词至少包含 3 个相关术语
- [ ] 输入和输出契约具有可操作性
- [ ] 工作流程和决策规则与具体功能相匹配
- [ ] 平台引用明确且具体
- [ ] 包含至少 3 个实际应用示例