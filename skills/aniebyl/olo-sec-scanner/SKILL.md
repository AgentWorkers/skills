---
name: olo-sec-scanner
version: 1.0.0
description: SEC EDGAR 文件分析用于并购尽职调查——从 10-K、10-Q 和 8-K 文件中提取财务数据、识别风险并跟踪公司事件
author: ololand.ai
author_url: https://ololand.ai
license: MIT
triggers:
  - sec filing
  - edgar
  - 10-k analysis
  - 10-q analysis
  - 8-k filing
  - annual report
  - quarterly report
  - sec extraction
  - xbrl
tags:
  - finance
  - sec
  - m-and-a
  - due-diligence
  - regulatory
---
# 用于并购的SEC文件扫描工具

该工具用于提取并分析美国证券交易委员会（SEC）EDGAR系统中的相关文件，以协助并购尽职调查。

## 数据来源

SEC EDGAR API（免费使用，无需API密钥，每秒请求次数限制为10次）：
- 公司信息：`https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`
- 提交文件：`https://data.sec.gov/submissions/CIK{cik}.json`
- 全文搜索：`https://efts.sec.gov/LATEST/search-index?q=...`

## 文件类型与并购相关性

| 文件类型 | 用途 |
|--------|----------|
| 10-K | 年度财务报表、风险因素、业务板块数据、法律诉讼信息 |
| 10-Q | 季度财务数据、中期变动、持续经营能力评估 |
| 8-K | 重要事件：收购、资产处置、管理层变动、财务报表重述 |
| DEF 14A | 高管薪酬、关联方交易、公司治理信息 |
| SC 13D/G | 激进投资者持股情况、持股比例超过5%的变动 |
| Form 4 | 内部人士买卖行为（可能预示市场动向） |
| Form D | 私募活动相关文件（IPO前的目标公司） |

## 数据提取框架

### 1. 财务数据提取（来自XBRL格式文件）
- 收入（过去3-5年的趋势数据，可从`Revenues`或`RevenueFromContractWithCustomerExcludingAssessedTax`字段获取）
- EBITDA（计算方法：`OperatingIncome` + `DepreciationAndAmortization`）
- 净利润、每股收益（EPS）、稀释后的股份数
- 总资产、总负债、股东权益
- 经营现金流、资本支出（CapEx）、自由现金流
- 如果公司业务分为多个板块，则需提取各板块的收入数据

### 2. 风险因素分析（来自10-K文件的第1A项）
- 对风险因素进行分类：市场风险、运营风险、监管风险、财务风险、法律风险、技术风险
- 标记出涉及诉讼、监管调查、重大经营缺陷或持续经营能力问题的风险
- 对风险因素进行年度对比，以发现新的风险信息
- 评估整体风险等级（低风险 / 中等风险 / 高风险）

### 3. 重要事件检测（来自8-K文件）
- 第1.01项：签订重要协议
- 第2.01项：收购或资产处置完成
- 第2.05项：重组相关费用
- 第4.01项：会计师变更（可能预示公司问题）
- 第5.02项：董事/高管离职
- 第8.01项：其他重大事件

### 4. 持股结构与治理结构分析（来自DEF 14A和SC 13D/G文件）
- 主要机构投资者持股情况及其集中度
- 内部人士持股比例
- 最近的内部人士交易记录（买入/卖出行为）
- 激进投资者的参与情况

## 输出格式

```
SEC Filing Analysis: [Company Name] (CIK: XXXXXXXXXX)

Filings Scanned: 12 (3x 10-K, 8x 10-Q, 1x 8-K)
Date Range: 2023-01-01 to 2025-12-31

Financial Summary (from XBRL):
  Revenue TTM:     $164.5M (↑ 12% YoY)
  EBITDA TTM:      $28.3M  (17.2% margin)
  FCF TTM:         $22.1M
  Net Debt:        $45.0M  (1.6x EBITDA)

Risk Flags:
  ⚠ New risk factor: "concentration of revenue" (added FY2025)
  ⚠ Material weakness in internal controls (10-K Item 9A)
  ✓ No going concern language
  ✓ No change in auditor

Material Events (8-K):
  2025-09-15: Entered into $50M credit facility (Item 1.01)
  2025-06-01: CFO departure (Item 5.02)

Insider Activity (Last 12 months):
  Net Selling: $2.3M (3 insiders sold, 0 bought)
```

## 与并购相关的特定检查内容

- **控制权变更条款**：在10-K文件中搜索“change of control”、“golden parachute”（金色降落伞条款）、“poison pill”（毒丸计划）等关键词
- **重要合同**：识别包含控制权变更触发条件的合同
- **客户集中度**：从风险因素或业务板块数据中提取相关信息
- **待决诉讼**：从文件脚注中统计或有负债的金额
- **税务资产递延**：提取与税收相关的资产价值（并购中的第382条法规相关风险）
- **租赁义务**：使用权资产及总租赁承诺金额