---
name: institutional-flow-tracker
description: 使用这项技能，可以通过13F文件数据来追踪机构投资者的持股变化和资金流向。该技能会分析对冲基金、共同基金及其他机构投资者，以识别那些出现大量资金流入或流出的股票。通过追踪这些 sophisticated investors（精明投资者）的资本投向，可以帮助投资者在股票出现重大波动之前发现潜在的投资机会。
---

# 机构资金流动追踪器

## 概述

该工具通过分析13F SEC文件来追踪机构投资者的活动，以识别资金流入和流出股票的“聪明资金”（即具有专业投资能力的机构投资者）。通过分析机构投资者持股情况的季度变化，您可以发现那些在股价大幅波动前被资深投资者大量买入的股票，或者在机构投资者减少持股时识别潜在风险。

**关键洞察：** 机构投资者（对冲基金、养老基金、共同基金）管理着数万亿美元的资产，并进行广泛的研究。他们的集体买卖行为通常会在股价大幅波动前1-3个季度出现。

## 适用场景

在以下情况下使用该工具：
- 验证投资思路（检查“聪明资金”是否与您的观点一致）
- 发现新的投资机会（寻找机构投资者正在买入的股票）
- 风险评估（识别机构投资者正在卖出的股票）
- 投资组合监控（跟踪机构投资者对您所持股票的支持情况）
- 跟踪特定投资者（例如沃伦·巴菲特、凯西·伍德等）
- 行业轮动分析（识别机构投资者正在转移资金的行业）

**不适用场景：**
- 寻求实时盘中交易信号（13F数据的报告周期为45天）
- 分析市值低于1亿美元的微型股票（这类股票通常不受机构投资者关注）
- 寻找短期交易信号（投资周期少于3个月）

## 数据来源与要求

### 必需条件：FMP API密钥

该工具使用Financial Modeling Prep (FMP) API来获取13F文件数据：

**设置步骤：**
```bash
# Set environment variable (preferred)
export FMP_API_KEY=your_key_here

# Or provide when running scripts
python3 scripts/track_institutional_flow.py --api-key YOUR_KEY
```

**API层级要求：**
- **免费层级：** 每天250次请求（足以分析20-30只股票）
- **付费层级：** 提供更高的请求次数限制，适用于更广泛的筛选

**13F文件提交时间表：**
- 每季度在季度末后的45天内提交
- 第一季度（1月至3月）：5月中旬前提交
- 第二季度（4月至6月）：8月中旬前提交
- 第三季度（7月至9月）：11月中旬前提交
- 第四季度（10月至12月）：2月中旬前提交

## 分析流程

### 第一步：识别机构投资者持股变化显著的股票

执行主要筛选脚本，找出机构投资者活动显著的股票：

**快速扫描（按机构投资者持股变化排名前50的股票）：**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --top 50 \
  --min-change-percent 10
```

**行业聚焦扫描：**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --sector Technology \
  --min-institutions 20
```

**自定义筛选：**
```bash
python3 institutional-flow-tracker/scripts/track_institutional_flow.py \
  --min-market-cap 2000000000 \
  --min-change-percent 15 \
  --top 100 \
  --output institutional_flow_results.json
```

**输出内容包括：**
- 股票代码和公司名称
- 当前机构投资者持股百分比（占流通股的比例）
- 季度间的持股变化
- 持有该股票的机构投资者数量
- 机构投资者的增减数量
- 主要的机构投资者持有者
- 总持股价值的变动

### 第二步：深入分析特定股票

对特定股票的机构投资者持股情况进行分析：

```bash
python3 institutional-flow-tracker/scripts/analyze_single_stock.py AAPL
```

**分析结果包括：**
- 过去8个季度的机构投资者持股趋势
- 所有持有机构投资者的名单及持股变化
- 持有比例最高的10家机构投资者
- 新增持股、增持持股、减持持股的情况
- 季度内的净增减持股情况
- 与行业平均持股水平的对比

**关键评估指标：**
- **持股百分比：** 机构投资者持股比例较高（>70%）= 更稳定的表现，但上涨空间有限
- **持股趋势：** 持股比例上升 = 看涨信号；下降 = 看跌信号
- **集中度：** 高集中度（前10家机构投资者持有超过50%）= 如果他们卖出，可能带来风险
- **投资者质量：** 是否包含优质长期投资者（如伯克希尔·哈撒韦、富达等）或投机性基金

### 第三步：追踪特定机构投资者的投资组合

跟踪特定对冲基金或投资公司的投资组合变动：

```bash
# Track Warren Buffett's Berkshire Hathaway
python3 institutional-flow-tracker/scripts/track_institution_portfolio.py \
  --cik 0001067983 \
  --name "Berkshire Hathaway"

# Track Cathie Wood's ARK Investment Management
python3 institutional-flow-tracker/scripts/track_institution_portfolio.py \
  --cik 0001579982 \
  --name "ARK Investment Management"
```

**CIK（中央索引键）查询：**
- 在以下网址查询：https://www.sec.gov/cgi-bin/browse-edgar
- 或使用FMP API进行机构投资者查询

**分析结果包括：**
- 当前投资组合持仓（前50只股票）
- 本季度新增的持仓
- 完全卖出的持仓
- 持有量最大的增减情况
- 投资组合的集中度及行业分配变化
- 他们精选股票的历史表现

### 第四步：解读与行动

请参考以下文档以获取解读指南：
- `references/13f_filings_guide.md` - 了解13F数据及其局限性
- `references/institutional_investor_types.md` - 不同类型机构投资者及其策略
- `references/interpretation_framework.md` - 如何解读机构投资者资金流动信号

**信号强度框架：**

**强烈看涨（考虑买入）：**
- 机构投资者持股比例环比增加超过15%
- 持有机构投资者数量增加超过10%
- 优质长期投资者增持持股
- 当前持股比例较低（<40%），且有增长空间
- 多个季度持续出现增持行为

**中性：**
- 持股比例变化较小（<5%）
- 买卖双方数量相当
- 机构投资者基础稳定

**适度看跌：**
- 机构投资者持股比例环比下降5-15%
- 卖方数量多于买方
- 持股比例较高（>80%），限制新买家进入

**强烈看跌（考虑卖出/避免买入）：**
- 机构投资者持股比例环比下降超过15%
- 持有机构投资者数量减少超过10%
- 优质投资者开始卖出持股
- 多个季度持续出现减持行为
- 高集中度（主要持有者卖出大量持股）

### 第五步：投资组合应用

**对于新股票：**
1. 对您的投资标的进行机构投资者分析
2. 查看是否有机构投资者也在买入的确认信号
3. 如果出现强烈看跌信号，重新考虑投资策略或减少持股规模
4. 如果出现强烈看涨信号，增强投资信心

**对于现有股票：**
1. 在13F文件提交截止日期后进行季度回顾
2. 监控机构投资者的减持情况（作为早期预警信号）
3. 如果机构投资者开始减持，重新评估投资策略
4. 如果普遍出现机构投资者减持，考虑减少持股

**筛选流程整合：**
1. 使用价值股息筛选器或其他筛选工具找到候选股票
2. 对候选股票运行机构资金流动追踪器
3. 优先选择机构投资者持续增持的股票
4. 避免机构投资者持续减持的股票

## 输出格式

所有分析结果将以结构化的Markdown格式保存在仓库根目录下：

**文件命名规则：`institutional_flow_analysis_<股票代码/主题>_<日期>.md`

**报告内容：**
1. 执行摘要（主要发现）
2. 机构投资者持股趋势（当前与历史对比）
3. 主要持有者及持股变化
4. 新买家与卖家情况
5. 集中度分析
6. 解读与建议
7. 数据来源与时间戳

## 限制与注意事项

**数据延迟：**
- 13F文件的报告周期为45天
- 提交日期后股票持仓情况可能发生变化
- 该工具仅作为确认信号使用，而非预测工具

**覆盖范围：**
- 仅要求管理资产超过1亿美元的机构投资者提交文件
- 不包括个人投资者和小型基金
- 国际机构投资者可能不提交13F文件

**报告规则：**
- 仅报告长期股票持仓（不包括空头头寸、期权、债券）
- 数据基于季度末的持股情况
- 部分持仓可能属于保密信息（报告延迟）

**解读注意事项：**
- 相关性≠因果关系（即使机构投资者买入，股票价格也可能下跌）
- 需结合整体市场环境和基本面进行分析
- 结合技术分析和其他工具使用

## 高级应用场景**

**内部人士与机构投资者联合分析：**
- 寻找同时受到内部人士和机构投资者买入的股票
- 当两者观点一致时，该信号更为可靠

**行业轮动检测：**
- 跟踪各行业的机构投资者资金流动情况
- 在价格变动之前发现行业轮动趋势

**逆势投资策略：**
- 寻找机构投资者正在卖出的优质股票（可能具有投资价值）
- 需要具备强烈的基本面判断力

**聪明资金验证：**
- 在进行重大投资决策前，确认“聪明资金”的看法
- 增强投资信心或发现被忽视的风险

## 参考资料**

`references/`文件夹包含以下详细指南：
- **13f_filings_guide.md** - 13F SEC文件的全面指南，包括文件内容、报告要求及数据质量注意事项
- **institutional_investor_types.md** - 不同类型的机构投资者（对冲基金、共同基金、养老基金等）及其投资策略
- **interpretation_framework.md** - 机构投资者持股变化的详细解读框架、信号质量评估方法及与其他分析方法的结合方式

## 脚本参数

### track_institutional_flow.py

用于查找机构投资者持股变化显著股票的主要筛选脚本。

**必需参数：**
- `--api-key`：FMP API密钥（或设置环境变量FMP_API_KEY）

**可选参数：**
- `--top N`：按机构投资者持股变化排名前N的股票（默认：50只）
- `--min-change-percent X`：机构投资者持股变化的最低百分比（默认：10%）
- `--min-market-cap X`：最低市值（以美元计，默认：10亿美元）
- `--sector NAME`：按特定行业筛选
- `--min-institutions N`：最低持有机构投资者数量（默认：10家）
- `--output FILE`：输出JSON文件路径（默认：institutional_flow_results.json）
- `--sort-by FIELD`：按“ownership_change”、“institution_count_change”、“dollar_value_change”排序

### analyze_single_stock.py

用于深入分析特定股票的机构投资者持股情况。

**必需参数：**
- 股票代码（用于指定分析的股票）
- `--api-key`：FMP API密钥（或设置环境变量FMP_API_KEY）

**可选参数：**
- `--quarters N`：分析的季度数量（默认：8个季度，即2年）
- `--output FILE`：输出Markdown报告路径
- `--compare-to TICKER`：与另一只股票的机构投资者持股情况进行对比

### track_institution_portfolio.py

用于追踪特定机构投资者的投资组合变动。

**必需参数：**
- `--cik CIK`：该机构的中央索引键
- `--name NAME`：报告中的机构名称
- `--api-key`：FMP API密钥（或设置环境变量FMP_API_KEY`

**可选参数：**
- `--top N`：显示前N只股票
- `--min-position-value X`：包含的最低持股价值（默认：1000万美元）
- `--output FILE`：输出Markdown报告路径

## 与其他工具的整合**

- **价值股息筛选器 + 机构资金流动追踪：**
```
1. Run Value Dividend Screener to find candidates
2. For each candidate, check institutional flow
3. Prioritize stocks with rising institutional ownership
```

- **美国股票分析 + 机构资金流动追踪：**
```
1. Run comprehensive fundamental analysis
2. Validate with institutional ownership trends
3. If institutions are selling, investigate why
```

- **投资组合管理器 + 机构资金流动追踪：**
```
1. Fetch current portfolio via Alpaca
2. Run institutional analysis on each holding
3. Flag positions with deteriorating institutional support
4. Consider rebalancing away from distribution
```

- **技术分析师 + 机构资金流动追踪：**
```
1. Identify technical setup (e.g., breakout)
2. Check if institutional buying confirms
3. Higher conviction if both align
```

## 最佳实践**

1. **定期回顾：** 设置提醒，确保在13F文件提交截止日期前进行回顾
2. **多季度趋势分析：** 关注持续的趋势（3个及以上季度），而非一次性变化
3. **质量优先于数量：** 伯克希尔·哈撒韦增持的股票数量超过100只小型基金增持的股票
4. **考虑背景：** 在股价下跌时机构投资者增持可能是价值投资者在逢低买入
5. **综合分析信号：** 不要单独依赖机构资金流动信号
6. **更新数据：** 每季度重新运行分析，以获取最新的13F文件数据

## 支持与资源**

- FMP API文档：https://financialmodelingprep.com/developer/docs
- SEC 13F文件数据库：https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F
- 机构投资者数据库：https://whalewisdom.com（提供免费访问）

---

**注意：** 该工具适用于长期投资者（投资周期为3-12个月）。对于短期交易，建议结合技术分析和其他 momentum 指标使用。