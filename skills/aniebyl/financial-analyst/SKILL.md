---
name: financial-analyst
description: 财务分析及研究工作流程，适用于市场研究、股票研究、可比公司分析、历史交易案例研究以及DCF（Discounted Cash Flow，折现现金流）估值。当需要构建或评估DCF模型、编制可比公司分析表、进行竞争对手或战略分析、市场规模估算时，均可使用该流程。最终输出结果可格式化为Excel、PowerPoint文件，或直接以Markdown格式呈现，数据来源包括CSV、Excel、SQL、API或网络数据。
---
# 财务分析师

## 概述

提供符合行业标准的市场研究、股票研究、可比公司分析（comps）、 precedent（过往交易案例分析）以及DCF（Discounted Cash Flow，折现现金流）估值报告。所有报告均需包含明确的假设、数据来源引用，并以Excel、PowerPoint或Markdown格式呈现。

## 快速了解需求

- 确认公司名称、股票代码、所属行业、地理位置、货币单位（例如：以百万美元计）。
- 明确研究范围（DCF估值、可比公司分析、过往交易案例分析、市场规模分析、竞争策略研究）及输出格式。
- 收集数据来源（CSV/Excel/SQL/API/网络数据），并索取访问权限或相关文件信息。
- 如用户要求继续进行，需列出所有必要的假设信息。

## 核心工作流程

### DCF模型

- 参考`references/dcf.md`文件，确保模型结构的规范性和准确性。
- 制定5年预测计划，使用CAPM模型计算加权平均资本成本（WACC），并利用Gordon Growth模型计算终值。
- 生成估值总结报告、敏感性分析表及假设信息表。
- 如需要模板，可使用`assets/templates/dcf-model-template.md`作为基础模板。

### 可比公司分析

- 参考`references/comps.md`文件，选择合适的可比公司并确定表格字段。
- 编制包含关键运营指标和交易倍数的可比公司分析表。
- 对异常数据进行处理，并说明调整或排除的理由。
- 使用`assets/templates/comps-template.csv`作为表格的模板。

### 过往交易案例分析

- 参考`references/precedents.md`文件，设置交易案例筛选条件及表格字段。
- 制作包含交易金额、溢价及交易倍数的表格。
- 说明交易背景（如收购方类型、控制权溢价、交易时机等）。
- 使用`assets/templates/precedents-template.csv`作为表格的模板。

### 市场研究

- 参考`references/market-research.md`文件，了解市场规模分析的方法和结构。
- 尽可能采用自上而下和自下而上的方法来确定总市场容量（TAM）、服务市场容量（SAM）及可服务市场容量（SOM）。
- 引用数据来源，并说明任何转换或估算的方法。
- 使用`assets/templates/market-research-template.md`作为报告的模板。

### 竞争策略与主要竞争对手分析

- 参考`references/competitive-strategy.md`文件，了解竞争策略分析的框架和报告结构。
- 识别直接竞争对手、潜在替代竞争对手，并简要说明原因。
- 评估各公司的差异化优势、护城河、定价能力及市场分销优势。
- 使用`assets/templates/competitive-strategy-template.md`作为报告的模板。

### 股票研究报告

- 参考`references/equity-research.md`文件，确定报告的结构。
- 明确研究结论、估值结果、潜在驱动因素及风险点。
- 确保结论与数据及可比公司分析/DCF估值结果保持一致。
- 使用`assets/templates/er-memo-template.md`作为报告的模板。

## 输出标准

- 每个模型或估值报告均需附带假设信息表。
- 所有表格均需标注货币单位和数据截止日期。
- Excel输出文件中的公式需保持透明性，关键驱动因素需用Markdown文档进行说明。
- 如用户要求使用PowerPoint格式，需提供`assets/templates/ppt-outline.md`作为幻灯片大纲。

## 资源目录

- 参考资料：`references/dcf.md`、`references/comps.md`、`references/precedents.md`、`references/market-research.md`、`references/competitive-strategy.md`、`references/equity-research.md`
- 工具模板：`assets/templates/dcf-model-template.md`、`assets/templates/comps-template.csv`、`assets/templates/precedents-template.csv`、`assets/templates/market-research-template.md`、`assets/templates/competitive-strategy-template.md`、`assets/templates/er-memo-template.md`、`assets/templates/ppt-outline.md`