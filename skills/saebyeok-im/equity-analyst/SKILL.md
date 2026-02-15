---
name: equity-analyst
description: 作为专业的投资分析人工智能，我们能够分析韩国股票的财务报表、新闻和图表，从而给出投资吸引力评分（0-100分）以及“买入”/“持有”/“避免”的投资建议。我们使用的是Naver金融数据，并严格遵循预设的优先级规则（财务数据 > 新闻 > 图表），同时依据相应的权重进行评估。
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"📈"}}
---

# 股票分析师技能

该技能提供针对在KRX上市的韩国股票的专业级股票分析服务。分析过程遵循严格的评估框架，重点考虑财务基本面（50%）、新闻与市场展望（25%）和技术图表（25%）三个方面。

## 适用场景

- 用户请求对特定股票代码或公司名称进行股票分析（例如：“分析一下三星电子”或“告诉我SK海力士的投资吸引力”）
- 用户要求提供带有理由的投资建议（买入/持有/避免投资）
- 需要基于财务指标的系统性、保守性、逻辑性的评估

**不适用场景**：
- 非韩国股票；
- 加密货币；
- 用户仅寻求非基于严格框架的随意性或主观性建议。

## 快速入门

1. 确定股票代码（例如：三星电子的代码为005930，SK海力士的代码为000660）；
2. 使用浏览器工具访问Naver Finance页面：`https://finance.naver.com/item/main.naver?code={ticker}`；
3. 提取所需数据（详见下方数据要求）；
4. 应用评估框架；
5. 生成指定格式的结构化报告。

## 数据要求

从Naver Finance主页面收集以下数据：

### 财务指标
- 市盈率（PER）
- 市净率（PBR）
- 净资产收益率（ROE，仅计算归属于母公司股东的收益）
- 营业利润率
- 负债比率
- 收入增长率（近几年的趋势，用于2024年至2025年的预测）

### 新闻与市场展望（摘要）
- 最近的重大新闻标题
- 盈利预期
- 行业利好/利空因素
- 分析师情绪变化

### 技术/图表状况（摘要）
- 股价走势（上涨/盘整/下跌）
- 当前价格相对于52周高点的位置
- 成交量特征（增加/减少/正常）
- 任何显著的图表形态（支撑位/阻力位等）

**注意**：无需使用布林带等复杂指标。图表描述应简洁明了，重点关注股价趋势和当前状态。

## 评估框架

严格按照以下步骤进行评估：

### 第一步：财务评分（50%）

对每个子类别评分0-100分：

**A. 估值（PER、PBR） - 权重30%**
- 低市盈率（低于行业平均水平）和低市净率（低于1）为正面因素
- 极高的市盈率（超过40）除非有出色的增长表现，否则为负面因素
- 评分结果：ValuationScore

**B. 盈利能力（ROE、营业利润率） - 权重30%**
- 净资产收益率低于5%：表现极差
- 净资产收益率在10%以上：表现良好
- 营业利润率稳定且高于行业平均水平：正面因素
- 评分结果：ProfitabilityScore

**C. 增长能力（收入增长率） - 权重25%**
- 持续增长（超过10%）为正面因素
- 增长停滞（低于3%）或下降：负面因素
- 评分结果：GrowthScore

**D. 稳定性（负债比率） - 权重15%**
- 低负债率（低于50%）为正面因素
- 高杠杆率（超过100%）为负面因素
- 评分结果：StabilityScore

**FinancialScore = Valuation×0.30 + Profitability×0.30 + Growth×0.25 + Stability×0.15**

**特别规则**：如果ProfitabilityScore和GrowthScore均低于30分，则将FinancialScore上限设定为50分（不受其他评分影响）。

### 第二步：新闻与市场展望评分（25%）

评估定性因素：
- 盈利预期的强度
- 产品/服务的市场表现
- 分析师的情绪倾向
- 行业的利好/利空因素

**评分规则**：
- 强有力的正面因素（新合同、监管批准、市场扩张）会提高评分
- 中立或“观望”态度：评分40-55分
- 无财务支撑的炒作行为：评分不应过高（最高60分）
- 负面因素（诉讼、客户流失、行业衰退）会降低评分
- 评分结果：NewsScore（0-100分）

### 第三步：技术/图表评分（25%）

评估市场时机和走势：
- 股价走势（上涨/盘整/下跌）
- 成交量变化
- 积累或分配的迹象
- 当前价格位置（接近支撑位/阻力位）

**评分规则**：
- 图表用于判断买入/卖出的时机，而非股票价值
- 即使基本面良好，如果技术图表表现不佳，评分仍可能较低
- 仅根据图表判断是否为合适的买入/卖出时机

**评分结果：ChartScore（0-100分）**

### 最终评分

FinalScore = (FinancialScore × 0.50) + (NewsScore × 0.25) + (ChartScore × 0.25)

### 投资建议类别

- **买入**：80–100分（强烈推荐）
- **谨慎买入**：65–79分（谨慎买入）
- **持有**：45–64分（等待时机或逢低买入）
- **避免投资**：低于45分（风险过高或吸引力不足）

## 输出格式

输出内容必须严格遵循以下结构：

```
1. Financial Breakdown
- ValuationScore: [0-100]
- ProfitabilityScore: [0-100]
- GrowthScore: [0-100]
- StabilityScore: [0-100]
- FinancialScore: [0-100]

2. NewsScore: [0-100]

3. ChartScore: [0-100]

4. Final Investment Attractiveness Score: XX / 100

5. Verdict: [BUY|BUY_LEAN|HOLD|AVOID]

6. Reasoning Summary:
[One paragraph explaining why the score was assigned, respecting priority order: Financial > News > Chart. Be conservative, logic-driven. Do NOT give investment advice.]
```

## 示例

### 示例1：SK海力士（基于真实数据）
```
1. Financial Breakdown
- ValuationScore: 70
- ProfitabilityScore: 95
- GrowthScore: 95
- StabilityScore: 75
- FinancialScore: 84.5

2. NewsScore: 70

3. ChartScore: 55

4. Final Investment Attractiveness Score: 73.5 / 100

5. Verdict: BUY_LEAN

6. Reasoning Summary:
SK하이닉스는 재무제표가 매우 강력합니다. ROE 43.20%, 영업이익률 46.67%, 43.7%의 매출 성장률은 업계 최상위 수준이며, PER 17.11배는 상대적으로 저평가되어 있습니다. 부채비율 64.12%는 반도체 업체로서 적정범위 내에 있습니다. 뉴스 측면에서는 HBM4 공급과 AI memory 수요 증가가 주가에 긍정적이나, 외국인 매도세가 일부 부정적 영향을 미치고 있습니다. 기술적 측면에서는 장기 상승추세는 유지되고 있으나, 단기적으로 조정 국면에 있어 매수 타이밍에 신중을 기할 필요가 있습니다. 재무적 우수성과 성장성에도 불구, 단기 차트의 불확실성으로 인해 "buy with caution" 상태로 평가됩니다.
```

### 示例2：财务指标不佳的情况
```
... (similar structure) ...
ValuationScore: 25 (PER 150, PBR 8.5 - extremely overvalued)
ProfitabilityScore: 20 (ROE 2%, margin negative)
...
Verdict: AVOID
...
```

## 脚本

该技能包含以下脚本：
- `scripts/analyze.py`：主要分析工具，用于处理提取的数据并计算评分
- `scripts/scrape_naver.py`：可选脚本，用于从Naver Finance页面提取数据

可以使用这些脚本来自动化重复性任务。

## 参考资料

详细的评估标准和示例：`references/framework.md`

## 注意事项

- 该技能仅适用于KRX上市的韩国股票
- 数据来源：Naver Finance（实时数据）
- 评分结果仅针对KRX范围内的股票
- 该评估框架较为保守：缺乏盈利支持的炒作行为不会获得高分
- 技术评分仅反映市场时机，不涉及股票质量

## 故障排除

**数据缺失**：如果某些指标无法获取，将其视为中性（评分50分），并在分析中说明原因。

**信号冲突**：按照优先级顺序进行评估：财务指标 > 新闻 > 图表。即使财务指标不佳，也无法通过良好的新闻或图表来弥补。

**极端估值**：市盈率（PER）或市净率（PBR）超过50时，除非有显著的增长表现，否则应给予较低评分。