---
name: lanbow-ads
description: Lanbow Ads 控制技能用于管理及优化 Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads 以及 DSP（程序化广告）平台上的广告活动。
---
# Lanbow 广告

## 目的
Lanbow 广告的核心功能包括：
- 作为专用的广告运营和优化接口；
- 管理广告渠道的规划、投放、监控和扩展；
- 标准化出价、预算和性能恢复的决策流程；
- 为媒体团队提供明确的操作指导。

## 使用场景
当用户需要以下服务时，请使用此功能：
- 在一个或多个渠道中设置、优化或扩展广告活动；
- 在有性能限制的情况下提供预算和出价决策支持；
- 对正在进行的广告活动进行异常诊断并采取恢复措施；
- 制定跨渠道的广告运营方案。

## 关键关键词
- lanbow ads（Lanbow 广告）
- run ads（投放广告）
- campaign（广告活动）
- media buyer（媒体买家）
- bidding（出价）
- budget（预算）
- allocation（分配）
- optimize（优化）
- scale（扩展）
- cpa（每点击成本）
- roas（投资回报率）
- performance（性能）
- monitor（监控）
- abtest（A/B 测试）

## 输入参数
**必填参数：**
- campaign_objective（广告活动目标）
- channel_scope（广告渠道范围）
- budget_constraints（预算限制）
- recent_performance_snapshot（最近的性能数据）

**可选参数：**
- creative_state（创意状态）
- audience_state（受众状态）
- tracking_health（跟踪健康状况）
- policy_or_account_flags（策略/账户标志）

## 输出结果
- 广告活动行动计划
- 出价和预算策略
- A/B 测试与扩展模型
- 监控与警报计划
- 操作员交接清单

## 工作流程
1. 标准化广告活动目标和关键绩效指标（KPI）的限制条件；
2. 评估广告渠道的适用性和结构质量；
3. 制定出价和资源分配方案；
4. 附加测试和扩展规则；
5. 返回监控触发条件及操作员交接清单。

## 决策规则
- 如果数据测量结果的可靠性较低，应先限制扩展规模并改进跟踪机制；
- 如果投资回报率（ROAS）稳定在阈值以上，可逐步增加预算；
- 如果每点击成本（CPA）不稳定，应减少实验的并发数量；
- 如果存在异常风险，应优先采取控制措施。

## 平台说明
主要支持的广告平台包括：
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads 以及 DSP/程序化购买平台。

平台使用建议：
- 确保广告推荐的执行具有可追溯性，并符合各平台的优化规则。

## 限制与约束
- 任何不可逆的更改都必须有回滚机制；
- 所有推荐方案都必须与关键绩效指标（KPI）的影响相关联；
- 遵守相关的政策和账户使用限制。

## 故障处理与升级流程
- 如果所需平台数据缺失，返回最低限度的数据请求列表；
- 如果出现政策或账户使用限制，引导用户联系合规部门或账户支持人员；
- 如果支出风险较高，触发紧急控制模式。

## 代码示例
### 广告活动控制配置示例
```json
{
  "objective": "提高投资回报率（improve_roas)",
  "channels": ["Meta", "GoogleAds", "TikTokAds"],
  "budget_mode": "staged_scale",
  "cpa_ceiling": 42,
  "roas_floor": 2.5
}
```

### 警报触发规则示例
```json
{
  "if": "roas_drop pct > 20 and spend_up pct > 25",
  "severity": "high",
  "action": "cap_budget_and_notify"
}
```

## 示例
### 示例 1：启动并稳定广告活动
**输入：**
- 在 Meta 和 TikTok 广告平台上启动新的广告活动

**输出内容：**
- 广告活动启动清单
- 第一周的监控要点
- 备用方案

### 示例 2：在验证后扩展广告活动
**输入：**
- 广告活动的投资回报率（ROAS）已稳定 10 天

**输出内容：**
- 扩展方案
- 出价策略更新
- 监控检查点

### 示例 3：跨渠道出现异常情况
**输入：**
- 支出激增，转化效果不稳定

**输出内容：**
- 异常情况分析
- 控制措施
- 下一步的验证步骤

## 质量检查清单
- [ ] 必填内容已完整且不为空
- [ ] 触发关键词至少包含 3 个相关术语
- [ ] 输入和输出参数均经过实际测试验证
- [ ] 工作流程和决策规则符合具体业务需求
- [ ] 平台相关信息明确具体
- [ ] 包含至少 3 个实际应用案例
```