---
name: ads-execution-hub
description: **Ads Execution Hub 控制技能：用于跨 Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads 以及 DSP/程序化广告平台的广告活动管理和优化。**
---
# 广告执行中心（Ads Execution Hub）

## 目的  
核心使命：  
- 作为专用的广告运营和优化接口；  
- 管理跨广告渠道的规划、投放、监控和扩展；  
- 标准化出价、预算和性能恢复的决策流程；  
- 为媒体团队提供明确的操作指南。  

## 适用场景  
在用户需要以下服务时使用该功能：  
- 在一个或多个渠道中设置、优化或扩展广告活动；  
- 在有性能限制的情况下提供预算和出价决策支持；  
- 对实时广告活动进行异常诊断并采取恢复措施；  
- 制定跨渠道的媒体运营方案。  

## 关键术语  
- 广告执行中心（Ads Execution Hub）  
- 运营广告（Run Ads）  
- 广告活动（Campaign）  
- 媒体购买者（Media Buyer）  
- 出价（Bidding）  
- 预算（Budget）  
- 分配（Allocation）  
- 优化（Optimize）  
- 扩展（Scale）  
- 每点击成本（CPA）  
- 每投资回报率（ROAS）  
- 性能监控（Performance Monitoring）  
- A/B测试（AB Test）  

## 输入参数  
**必填参数：**  
- 广告活动目标（Campaign Objective）  
- 渠道范围（Channel Scope）  
- 预算限制（Budget Constraints）  
- 最新性能数据（Recent Performance Snapshot）  

**可选参数：**  
- 创意内容状态（Creative State）  
- 目标受众状态（Audience State）  
- 跟踪系统健康状况（Tracking Health）  
- 政策或账户相关标志（Policy/Account Flags）  

## 输出结果  
1. 广告活动行动计划（Campaign Action Plan）  
2. 出价与预算策略（Bidding and Budget Policy）  
3. A/B测试与扩展模型（AB Test and Scale Model）  
4. 监控与警报计划（Monitoring and Alert Plan）  
5. 操作员交接清单（Operator Handoff Checklist）  

## 工作流程  
1. 标准化广告活动目标及关键绩效指标（KPI）；  
2. 评估各渠道的适用性和数据质量；  
3. 制定出价与资源分配方案；  
4. 规定测试与扩展规则；  
5. 提供监控触发条件及操作员操作指南。  

## 决策规则  
- 如果数据测量精度较低，先限制扩展规模并改进跟踪机制；  
- 如果ROAS稳定且高于阈值，可逐步增加预算；  
- 如果CPA波动较大，减少实验的并发数量；  
- 如果存在异常风险，优先采取控制措施。  

## 平台注意事项  
**主要支持的平台：**  
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads、DSP/程序化购买平台（DSP/Programmatic Buying）  
**平台使用建议：**  
- 确保推荐策略针对具体平台进行优化，并可进行审计；  
- 使出价逻辑与各平台的优化机制保持一致。  

## 限制与约束  
- 任何不可逆的更改都必须具备回滚机制；  
- 所有推荐方案都必须与关键绩效指标（KPI）相关联；  
- 遵守相关政策和账户使用限制。  

## 故障处理与升级流程  
- 如果所需平台数据缺失，返回最低限度的数据请求列表；  
- 如果出现政策或账户使用限制，引导用户联系合规部门或账户支持团队；  
- 如果支出风险过高，触发紧急控制模式。  

## 代码示例  
### 广告活动控制参数  
```json
{
  "objective": "提高ROAS",
  "channels": ["Meta", "GoogleAds", "TikTokAds"],
  "budget_mode": "staged_scale",
  "cpa_ceiling": 42,
  "roas_floor": 2.5
}
```

### 警报触发规则  
```json
{
  "if": "roas_drop pct > 20 AND spend_up pct > 25",
  "severity": "high",
  "action": "cap_budget_and_notify"
}
```

## 示例  
### 示例1：启动并稳定广告活动  
**输入：**  
- 在Meta和TikTok Ads平台上启动新的广告活动  

**输出内容：**  
- 广告活动启动 checklist  
- 首周监控要点  
- 备用方案  

### 示例2：验证后扩展广告活动  
**输入：**  
- 广告活动ROAS连续10天保持稳定  

**输出内容：**  
- 扩展计划  
- 出价策略更新  
- 监控节点  

### 示例3：跨渠道异常情况  
**输入：**  
- 支出激增，转化数据不稳定  

**输出内容：**  
- 异常情况分析  
- 应急处理措施  
- 下一步验证步骤  

## 质量检查清单  
- 必填内容完整且不为空  
- 触发关键词包含至少3个相关术语  
- 输入与输出数据可进行实际测试  
- 工作流程和决策规则符合平台特性  
- 提供至少3个实际应用案例