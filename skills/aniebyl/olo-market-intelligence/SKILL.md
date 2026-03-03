---
name: olo-market-intelligence
version: 1.0.0
description: 并购尽职调查中的竞争格局与市场情报分析：目标市场（TAM）、潜在客户（SAM）和现有客户（SOM）的识别，竞争对手画像，以及行业趋势分析
author: ololand.ai
author_url: https://ololand.ai
license: MIT
triggers:
  - market intelligence
  - competitive landscape
  - tam sam som
  - market sizing
  - industry analysis
  - competitor mapping
  - market research
  - commercial due diligence
tags:
  - finance
  - market-research
  - m-and-a
  - due-diligence
  - competitive-intelligence
---
# 并购市场情报

为并购尽职调查提供竞争格局分析和市场规模数据。

## 研究框架

### 1. 市场规模（TAM/SAM/SOM）
- **TAM**（总可寻址市场）：产品/服务类别的全球市场规模
- **SAM**（可服务可寻址市场）：根据地理位置和细分市场筛选后的子市场
- **SOM**（可服务可获得市场）：基于竞争地位得出的实际市场份额
- 数据来源：行业报告（Gartner、IDC、Statista），并结合自下而上的估算进行验证
- 以范围（低/基准/高）的形式呈现，并附上方法论说明
- 包括TAM的5年复合年增长率（CAGR）预测

### 2. 竞争格局
- 识别5-10家直接竞争对手和3-5家相关行业企业
- 对每家竞争对手，收集以下信息：
  - 收入估算及增长率
  - 融资历史和估值（如为私营企业）
  - 市场份额估算
  - 关键差异化优势及市场定位
  - 最近的战略举措（收购、合作、产品发布）
- 使用2x2矩阵（例如：广度 vs. 深度、价格 vs. 能力）来展示竞争定位

### 3. 行业动态
- **增长驱动因素**：监管政策支持、技术变革、需求趋势
- **阻碍因素**：产品同质化、监管风险、替代品威胁
- **波特五力模型**评估：
  - 供应商议价能力（低/中/高）
  - 买方议价能力（低/中/高）
  - 竞争激烈程度（低/中/高）
  - 替代品威胁（低/中/高）
  - 新进入者威胁（低/中/高）
- **行业生命周期阶段**：新兴期、增长期、成熟期、衰退期

### 4. 客户与渠道分析
- 客户细分（企业客户/中端市场/小型企业，按行业领域划分）
- 买家画像及购买决策因素
- 销售渠道组合（直销、渠道销售、市场平台、OEM）
- 行业的净收入留存率和客户流失率基准
- 客户转换成本评估

### 5. 行业内的并购活动
- 近三年内的类似并购交易
- 并购交易的平均市盈率（EV/Revenue）和平均市净率（EV/EBITDA）
- 买家类型（战略投资者 vs. 财务投资者）
- 并购交易量趋势（增长、稳定、下降）
- 失败的并购案例及其原因

## 输出格式

```
Market Intelligence Report: [Industry/Sector]
Target: [Company Name]

Market Size:
  TAM: $12.4B (2025) → $18.7B (2030), 8.5% CAGR
  SAM: $4.2B (North America + Europe)
  SOM: $180M (target's realistic capture)

Competitive Position:
  Market Share: ~4.3% of SAM
  Rank: #5 of 12 tracked competitors
  Moat: [proprietary data / switching costs / network effects / none]

Top Competitors:
  1. CompetitorA — $520M rev, 12% share, well-funded
  2. CompetitorB — $310M rev, 7% share, PE-backed
  3. CompetitorC — $190M rev, 4.5% share, recently acquired

Industry Health:
  Growth Stage: Growth → Early Maturity
  Consolidation Trend: Accelerating (12 deals in last 18 months)
  Regulatory Climate: Favorable (no pending restrictive legislation)

Comparable Transactions:
  Median EV/Revenue: 3.2x
  Median EV/EBITDA: 14.5x
  Premium to Public Comps: +25-35% (control premium)
```

## 质量标准
- 所有市场规模估算均需注明数据来源
- 区分已确认的数据和估算数据（用“~”标记）
- 所有市场情报数据均需标注日期；过时的数据可能具有误导性
- 对信心度较低的评估结果需明确标注
- 市场规模数据至少需引用两个来源进行交叉验证