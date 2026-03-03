---
name: olo-deal-screening
version: 1.0.0
description: 针对私募股权（PE）投资者和战略买家的目标公司评估与交易资格审核
author: ololand.ai
author_url: https://ololand.ai
license: MIT
triggers:
  - deal screening
  - target evaluation
  - investment criteria
  - acquisition criteria
  - deal qualification
  - deal fit
  - buyer criteria
  - deal scoring
tags:
  - finance
  - screening
  - m-and-a
  - due-diligence
  - private-equity
---
# 并购中的交易筛选

根据买方的投资标准对收购目标进行评分和评估。

## 筛选框架

从五个维度对目标进行评估，每个维度的评分范围为0-100：

### 1. 战略契合度（25%权重）
- 行业/领域与买方投资组合的匹配度
- 地理位置的契合度（市场、运营、客户群）
- 产品/服务的互补性
- 技术或能力的补缺作用
- 品牌和市场地位的价值

### 2. 财务状况（25%权重）
- 收入规模（最低门槛检查）
- 收入增长趋势（三年趋势）
- EBITDA利润率与行业基准的对比
- 收入质量（经常性收入与一次性收入、客户集中度）
- 流动资本效率

### 3. 估值吸引力（20%权重）
- EV/EBITDA与可比交易的对比
- EV/收入与行业中位数的对比
- 在预估购买价格下的内部收益率（IRR）
- 多元化投资潜力（低价买入，高价卖出）

### 4. 风险状况（15%权重）
- 客户集中度（前10大客户占收入的百分比）
- 对关键人员的依赖性
- 监管风险
- 技术过时的风险
- 诉讼或合规问题

### 5. 执行可行性（15%权重）
- 管理团队的素质及留任可能性
- 整合的复杂性评估
- 竞争性拍卖的动态
- 卖方的动机和时间表
- 融资的可用性

## 评分结果

```
Overall Fit Score: 78/100 — PROCEED TO DD

Strategic Fit:     85/100 ████████░░
Financial Profile: 72/100 ███████░░░
Valuation:         80/100 ████████░░
Risk Profile:      68/100 ██████░░░░
Execution:         82/100 ████████░░

Recommendation: PROCEED TO DD
Key Strengths: [top 3]
Key Concerns: [top 3]
Suggested Next Steps: [prioritized actions]
```

## 阈值

| 评分范围 | 建议 |
|-------------|----------------|
| 80-100 | 战略契合度强 — 优先进行深入评估 |
| 65-79 | 战略契合度良好 — 谨慎推进 |
| 50-64 | 战略契合度一般 — 需要进一步论证 |
| 低于50 | 战略契合度差 — 除非有充分的理由，否则不予考虑 |

## 绝对否决条件（自动触发）

在评分之前，需检查以下绝对否决条件：
- 收入低于买方的最低门槛
- EBITDA为负（除非处于成长阶段）
- 活跃的诉讼导致EV损失超过20%
- 交易方所属实体受到制裁
- 该行业被买方明确排除在投资范围之外

## 私募股权（PE）特定标准

对于财务投资者买家，还需额外评估：
- **杠杆收购（LBO）可行性**：该交易能否实现3-5倍的EBITDA杠杆？
- **价值创造潜力**：收入增长、利润率提升、附加业务、多元化发展
- **退出途径**：IPO的可行性、潜在的收购方群体、不同投资者之间的合作可能性
- **持有期回报**：目标公司在3-5年内的总IRR达到20-25%
- **基金匹配度**：检查基金规模、投资期限、行业专注度、地理投资范围

## 输出格式

提供符合JSON格式的结构化输出，包括：
- `overall_score`：0-100的总体评分
- `recommendation`：`proceed_to_dd` | `proceed_with_caution` | `pass`
- `dimension_scores`：包含每个维度的评分结果
- `deal_breakers`：触发自动否决条件的列表
- `strengths`：最重要的三个正面因素
- `concerns`：最重要的三个风险因素
- `next_steps`：优先处理的行动事项