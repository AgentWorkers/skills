---
name: growth-strategy-hub
description: 基于真实市场信号构建的企业增长决策系统，用于管理Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads以及DSP/程序化广告平台上的资本分配。
---
# 成长战略中心（Growth Strategy Hub）

## 目的
核心使命：
- 运营一个企业增长决策系统。
- 该系统基于真实的市场信号进行运作。
- 通过明确的风险控制机制来管理资本分配。
- 将企业目标转化为可执行的投资政策。

## 使用时机
当用户需要以下内容时，请使用此功能：
- 企业层面的增长投资决策
- 跨渠道和市场的资本分配管理
- 季度或年度增长投资组合策略
- 风险预警及高管决策支持

**高相关关键词**：
- 企业增长（Enterprise Growth）、决策系统（Decision System）、资本分配（Capital Allocation）
- 收入（Revenue）、利润（Profit）、现金流（Cashflow）、投资回报率（ROI）、投资回报率（ROAS）、贷款价值（LTV）
- 预测（Forecast）、模型（Model）、策略（Strategy）、风险（Risk）、预算（Budget）

## 输入合同（Input Contract）
**必填项**：
- 企业目标（Enterprise Targets）：收入/利润/现金流目标
- 资本池（Capital Pool）：可使用的预算及限制条件
- 市场信号输入（Market Signal Inputs）：成本（Cost）、需求（Demand）、竞争情况（Competition）、转化率信号（Conversion Signals）
- 管理规则（Governance Rules）：风险限额及审批阈值

**可选项**：
- 场景定义（Scenario Definitions）
- 财务报表约束（Balance Sheet Constraints）
- 董事会偏好（Board Preferences）
- 下降容忍度（Downside Tolerance）

## 输出合同（Output Contract）
1. 市场信号决策简报（Market-Signal Decision Brief）
2. 资本分配投资组合计划（Capital Allocation Portfolio Plan）
3. 场景预测（Base/Upside/Downside）
4. 风险预警系统及阈值（Risk Warning System and Thresholds）
5. 高管决策备忘录（Executive Decision Memo）

## 工作流程（Workflow）
1. 标准化企业目标及资本限制。
2. 整合并分析真实的市场信号。
3. 按不同场景模拟资本分配结果。
4. 评估风险及触发条件。
5. 输出经过管理的资本分配决策。

## 决策规则（Decision Rules）
- 如果市场信号的可靠性较低，减少资本集中程度。
- 如果下行风险超过管理限制，切换至防御性分配模式。
- 如果上行前景良好但波动性较高，按阶段逐步释放资金。
- 如果现金流保护与增长速度冲突，优先考虑偿付能力保障措施。

## 平台说明（Platform Notes）
**主要应用领域**：
- Meta（Facebook/Instagram）、Google Ads、TikTok Ads、YouTube Ads、Amazon Ads、Shopify Ads、DSP/程序化广告（DSP/Programmatic Advertising）

**平台使用指南**：
- 将平台输出作为市场信号使用，而非孤立的关键绩效指标（KPIs）。
- 最终决策应在投资组合层面做出。

## 约束与限制（Constraints and Guardrails）
- 绝不要将推测性结果作为确定性结论呈现。
- 确保资本管理过程透明且可审计。
- 将战略建议与执行细节分开。

## 故障处理与升级流程（Failure Handling and Escalation）
- 如果信号质量不稳定，提供置信区间及数据修复需求。
- 如果缺少管理规则，严格执行默认的风险政策。
- 对于高风险且置信度较低的决策，需经过高管审批。

## 代码示例（Code Examples）
### 资本分配场景（YAML格式）
```yaml
decision_system: growth_strategy_hub
horizon: Q4-2026
capital_pool: 1800000
allocations:
  Meta: 0.28
  GoogleAds: 0.26
  TikTokAds: 0.14
  AmazonAds: 0.12
  DSP: 0.20
risk_mode: balanced
```

### 风险预警规则（JSON格式）
```json
{
  "trigger": "blended_roas_below_floor",
  "floor": 2.1,
  "window_days": 7,
  "action": "freeze_incremental_capital"
}
```

## 实例说明（Examples）
### 示例1：资本投资组合重置
**输入**：
- 需要根据更严格的风险政策重新平衡各渠道的支出

**输出重点**：
- 新的投资组合分配方案
- 不同场景下的影响分析
- 相关的管理决策流程

### 示例2：高增长与现金流冲突
**输入**：
- 设定激进的增长目标，但现金流缓冲有限

**输出重点**：
- 权衡方案
- 分阶段释放资本的策略
- 风险预警阈值

### 示例3：董事会决策支持
**输入**：
- 季度企业增长评估报告

**输出重点**：
- 决策备忘录
- 基于市场信号的推荐方案
- 应急预案

## 质量检查清单（Quality Checklist）
- [ ] 所有必填项均已填写且内容完整
- [ ] 关键触发词至少包含3个专业术语
- [ ] 输入和输出内容均经过实际测试
- [ ] 工作流程及决策规则符合具体功能需求
- [ ] 平台相关信息明确具体
- [ ] 包含至少3个实际应用案例
```