---
name: landing-page-auditor
description: 审核来自 Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads 和 Shopify Ads 的付费流量质量的相关登录页面。
---
# 广告 landing page 审计

## 目的
核心任务：
- 检查广告的可达性（reachability），诊断用户转化过程中的障碍（friction），并找出影响转化效率的因素。

此技能专为广告相关工作流程设计，其输出应包含可执行的计划，而不仅仅是泛泛的建议。

## 适用场景
当用户提出以下需求时，可使用此技能：
- 需要与业务成果相关的广告执行指导
- 需要制定涉及收入（revenue）、投资回报率（ROAS）、每次点击成本（CPA）或预算效率（budget efficiency）的增长策略
- 需要对 Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads 等平台进行操作

相关关键词：
- 广告（ads）、广告活动（advertising）、增长策略（growth strategy）、收入（revenue）、投资回报率（ROAS）、每次点击成本（CPA）、预算（budget）、流量（traffic）、转化率（conversion rate）、转化漏斗（conversion funnel）

## 输入参数
必填参数：
- 实体标识符（entity_ids）：账户（account）、广告活动（campaign）、广告组（adset）或广告 ID（ad identifier）
- 事件或审计范围（incident_or_audit_scope）
- 时间范围（time_window）

可选参数：
- 日志或事件记录（logs_or_events）
- 政策相关标志（policy_flags）
- 警报阈值（alert_thresholds）
- 负责人联系方式（owner_contacts）

## 输出内容
1. 运营状态总结
2. 按严重程度排序的问题发现
3. 缓解措施（mitigation actions）
4. 升级处理工单（escalation ticket payload）
5. 监控检查清单（monitoring checklist）

## 工作流程
1. 确认审计范围及受影响的实体。
2. 验证数据的时效性和事件的完整性。
3. 发现异常情况、政策相关问题或设置上的漏洞。
4. 根据风险程度和修复速度对问题进行排序。
5. 提供可供负责人执行的操作方案及相应的工单内容。

## 决策规则
- 如果数据过时，暂缓最终判断并请求更新数据。
- 如果发现高风险问题，建议先采取控制措施。
- 如果根本原因不明确，提供多个假设及验证顺序。

## 平台注意事项
主要审计平台包括：
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads

平台操作建议：
- 建议针对不同平台制定具体的优化方案，不要将所有平台的建议合并为一个通用计划。
- 对于 Meta 和 TikTok Ads，优先考虑创意内容的测试频率。
- 对于 Google Ads 和 Amazon Ads，重点关注需求捕获和商品展示的准确性。
- 对于 DSP（程序化广告平台），重点关注受众控制及投放频率的管理。

## 约束与限制
- 禁止伪造任何指标或政策结果。
- 将观察到的事实与假设区分开来。
- 对于每项建议措施，使用可量化的表述。
- 当存在支出风险时，必须包含至少一种回滚或止损策略。

## 故障处理与升级流程
- 如果关键输入信息缺失，仅要求提供最低限度的必要字段。
- 如果平台存在限制，需说明权衡方案及安全默认值。
- 如果对问题的确定性较低，需明确标注并提供验证清单。
- 如果出现高风险问题（如政策问题、计费问题或跟踪数据异常），需通过结构化的方式上报问题。

## 代码示例
### 事件工单示例
```
ticket_id: INC-ads-001
severity: high
impact: spend_waste_risk
owner: media-ops
next_check_at: 2026-03-03T10:00:00Z
```

### 健康检查规则示例
```
rule: delivery_drop
condition: impressions_down_pct > 40
action: alert_and_pause_review
```

## 示例
### 示例 1：广告素材在发布前损坏
输入：
- 未记录购买事件（Purchase event missing）
- 广告活动将在 24 小时后开始（Campaign start in 24h）

输出重点：
- 问题的严重程度排名
- 立即采取的缓解措施
- 重新发布的检查清单

### 示例 2：账户健康状况审计
输入：
- 涉及多个平台账户（Multiple platform accounts）
- 政策或计费状态未知（Unknown policy or billing status）

输出重点：
- 账户健康状况评分卡（Account health scorecard）
- 需要避免的风险
- 负责人应采取的行动

### 示例 3：实时异常处理
输入：
- 支出激增但转化率未见提升（Spending spikes with no conversion lift）
- 多个广告活动受到影响（Multiple campaigns impacted）

输出重点：
- 异常问题的处理流程
- 应采取的缓解措施
- 事件工单内容

## 质量检查清单
- [ ] 所有必填部分均已填写且内容不为空
- [ ] 触发关键词中包含至少 3 个专业术语
- [ ] 输入和输出内容均经过实际测试验证
- [ ] 工作流程和决策规则与具体功能相匹配
- [ ] 平台相关说明清晰明确
- [ ] 包含至少 3 个实际应用案例
```