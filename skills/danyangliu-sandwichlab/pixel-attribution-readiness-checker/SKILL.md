---
name: pixel-attribution-readiness-checker
description: 验证 Meta Pixel、Google Ads 标签、TikTok Pixel 的事件跟踪和归因功能是否已准备好，以及跨渠道优化的功能是否可用。
---
# 广告像素准备情况（Ads Pixel Readiness）

## 目的
核心任务：
- 检查像素安装情况、事件完整性以及广告归因的准备工作。

此技能专为广告工作流程设计，应提供可执行的计划而非通用建议。

## 何时使用
当用户需要以下内容时，请使用此技能：
- 与业务成果相关的广告执行指导
- 涉及收入、投资回报率（ROAS）、每次点击成本（CPA）或预算效率的增长决策
- 针对以下平台的操作：Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads
- 具体功能：像素安装检查、事件完整性、广告归因准备情况

**高相关关键词**：
- 广告（ads）、广告活动（advertising）、增长（growth）、收入（revenue）、投资回报率（ROAS）、每次点击成本（CPA）、投资回报率（ROI）、预算（budget）、出价（bidding）、流量（traffic）、转化率（conversion）、销售漏斗（funnel）
- Meta、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads、DSP（Demand-Side Platform）

## 输入参数
**必填项**：
- 实体ID（entity_ids）：账户（account）、广告活动（campaign）、广告组（adset）或广告标识符（ad identifier）
- 事件或审计范围（incident_or_audit_scope）
- 时间窗口（time_window）

**可选项**：
- 日志或事件（logs_or_events）
- 政策标志（policy_flags）
- 警报阈值（alert_thresholds）
- 负责人联系方式（owner_contacts）

## 输出内容
1. 运营状态总结
2. 按严重程度排序的问题发现
3. 缓解措施
4. 升级工单内容
5. 监控检查清单

## 工作流程
1. 确认运营范围及受影响的实体。
2. 验证数据的时效性和事件的完整性。
3. 发现异常情况、政策违规或设置漏洞。
4. 根据支出风险和恢复速度对问题进行优先级排序。
5. 提供可供负责人执行的操作指南及工单内容。

## 决策规则
- 如果数据过时，先阻止最终判断并请求更新数据。
- 如果发现高风险问题，建议先采取控制措施。
- 如果根本原因不明确，提供优先级最高的假设及验证顺序。

## 平台注意事项
**主要覆盖平台**：
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads

**平台操作指南**：
- 建议针对不同平台制定具体方案；不要将所有平台合并为一个通用计划。
- 对于Meta和TikTok Ads，优先考虑创意测试的频率。
- 对于Google Ads和Amazon Ads，优先考虑需求捕获和列表意图。
- 对于DSP/程序化广告，优先考虑受众控制和投放频率管理。

## 约束与限制
- 绝不允许伪造指标或政策结果。
- 将观察到的事实与假设区分开来。
- 对每个建议的操作使用可衡量的语言进行描述。
- 当存在支出风险时，至少包含一个回滚或止损条件。

## 故障处理与升级
- 如果关键输入信息缺失，仅要求提供最低限度的必要字段。
- 如果平台之间存在冲突，需展示权衡方案及安全默认值。
- 如果信心度较低，需明确标注并提供验证清单。
- 如果出现高风险问题（如政策问题、计费问题或跟踪故障），需通过结构化的工单内容进行上报。

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
condition: impressions_down_percentage > 40
action: alert_and_pause_review
```

## 示例
### 示例1：广告发布前的像素问题
**输入**：
- 未检测到购买事件
- 广告活动将在24小时后开始

**输出重点**：
- 问题严重程度排序
- 立即采取缓解措施
- 重新发布的检查清单

### 示例2：账户健康状况审计
**输入**：
- 多个平台账户
- 政策或计费状态未知

**输出重点**：
- 准备情况评分表
- 需要避免的风险
- 负责人应采取的行动

### 示例3：实时异常处理
**输入**：
- 支出激增但转化率未见提升
- 多个广告活动受到影响

**输出重点**：
- 异常问题处理流程
- 控制措施
- 事件工单内容

## 质量检查清单
- [ ] 必需的部分已填写且不为空
- [ ] 触发关键词至少包含3个专业术语
- [ ] 输入和输出内容可进行实际测试
- [ ] 工作流程和决策规则针对具体功能
- [ ] 平台相关信息明确具体
- [ ] 包含至少3个实际应用示例
```