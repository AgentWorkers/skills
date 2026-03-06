---
name: growth-autopilot-ads
description: 自动化生成全渠道营销策略（full-funnel strategy）、预算结构设计（budget structure design），以及针对 Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads 以及 DSP（Demand-Side Platforms）/程序化广告（programmatic campaigns）的动态出价（dynamic bid）和投放规模调整（scale adjustments）功能。
---
# 自动增长驾驶舱（Growth Autopilot）

## 目的
核心任务：
- 根据业务目标自动生成全面的付费增长策略。
- 自动设计预算和账户结构。
- 根据绩效信号动态调整出价和扩展速度。
- 通过安全机制和异常恢复规则保持增长的稳定性。

## 适用场景
当用户需要以下功能时，请使用此功能：
- 自动化增长策略的编排
- 自动预算分配和动态优化
- 出价和扩展的自动决策循环
- 持续监控和调整策略

**高频关键词**：
- 自动驾驶舱（Autopilot）、自动化（Automation）、增长人工智能（Growth AI）、增长机器人（Growth Bot）
- 预算（Budget）、出价（Bidding）、分配（Allocation）、优化（Optimize）、扩展（Scale）
- 每点击成本（ROAS）、每次点击费用（CPA）、收入（Revenue）、绩效（Performance）、广告活动（Campaign）

## 输入参数
**必填参数**：
- north_star_goal（核心业务目标）
- budget_constraints（预算限制）
- platform_scope（平台范围）
- control_limits（控制限制，如最大回撤额、最低ROAS等）

**可选参数**：
- warm_start_data（初始数据）
- creative_inventory_state（创意库存状态）
- seasonality_rules（季节性规则）
- escalation_contacts（紧急联系人）

## 输出结果
1. 自动增长策略蓝图（Autopilot Strategy Blueprint）
2. 预算和结构政策（Budget and Structure Policy）
3. 动态出价/扩展规则（Dynamic Bid/Scale Rules）
4. 安全机制和紧急停止机制（Safety Guardrails and Kill-switches）
5. 监控和升级工作流程（Monitoring and Escalation Workflow）

## 工作流程
1. 将业务目标转换为机器可执行的策略集。
2. 根据渠道角色初始化预算和账户结构。
3. 根据KPI趋势应用自适应出价和扩展规则。
4. 强制执行安全机制和自动回滚逻辑。
5. 定期生成优化报告和下一步行动建议。

## 决策规则
- 如果KPI偏离预设范围，切换到保守模式。
- 如果系统信心较低，降低自动化操作的强度。
- 如果出现严重异常，触发部分或全部暂停操作。
- 如果确认异常已得到解决，恢复逐步扩展的过程。

## 平台说明
**主要适用平台**：
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads、DSP/程序化广告平台

**平台行为指南**：
- 自动驾驶舱规则应针对具体渠道制定，但由中央策略统一管理。
- 确保出价逻辑与平台的优化目标保持一致。

## 限制与安全机制
- 不得自动批准可能带来风险的创意变更。
- 必须始终保留手动干预的途径。
- 每个自动化操作都必须有可审计的规则依据。

## 故障处理与升级流程
- 如果关键指标数据延迟，暂停自动化操作。
- 如果策略拒绝率突然上升，将任务转交人工审核。
- 如果数据质量下降，切换到仅监控模式。

## 代码示例
### 自动增长策略 YAML 示例
```yaml
objective: maximize_revenue_with_roas_floor
roas_floor: 2.3
cpa_ceiling: 38
budget_step_pct: 12
rollback_trigger:
  roas_drop_pct: 18
  window_days: 3
```

### 决策循环伪代码示例
```python
if roas >= roas_floor and cpa <= cpa_ceiling:
    increase_budget(step_pct)
elif roas < roas_floor:
    decrease_budget(step_pct)
    tighten_bids()
```

## 示例
### 示例 1：自动增长策略的初始设置
**输入**：
- 新账户，基础数据有限

**输出**：
- 初始策略集
- 安全的探索范围
- 定期的监控频率

### 示例 2：动态扩展模式
**输入**：
- KPI连续3周保持稳定

**输出**：
- 扩展计划
- 出价调整规则
- 回滚方案

### 示例 3：紧急稳定措施
**输入**：
- ROAS骤降 + 支出激增

**输出**：
- 暂停/回滚操作
- 问题根源排查清单
- 重新启动条件

## 质量检查清单
- [ ] 所有必填部分均已填写且不为空
- [ ] 触发关键词至少包含3个相关术语
- [ ] 输入和输出参数均可进行实际测试
- [ ] 工作流程和决策规则符合具体功能需求
- [ ] 平台相关说明明确具体
- [ ] 包含至少3个实际应用示例
```