---
name: portfolio-manager
description: 使用 Alpaca MCP Server 进行全面的资产组合分析：该服务器可用于获取用户的持仓和股票位置信息，进而分析资产配置、风险指标、个股表现以及投资组合的多样化程度，并生成再平衡建议。适用于用户需要查看资产组合状况、进行持仓分析、风险评估、绩效评估或为他们的经纪账户制定再平衡策略的场景。
---

# 投资组合管理器

## 概述

该技能通过与 Alpaca MCP 服务器集成来获取实时持仓数据，从而分析和管理投资组合。随后会进行全面的分析，涵盖资产配置、多元化、风险指标、个别持仓评估以及再平衡建议。生成包含可操作见解的详细投资组合报告。

该技能利用 Alpaca 的经纪 API 通过 MCP（模型上下文协议）访问实时投资组合数据，确保分析基于实际持仓情况，而非手动输入的数据。

## 适用场景

当用户请求以下内容时，可调用此技能：
- “分析我的投资组合”
- “查看我的当前持仓”
- “我的资产配置是什么？”
- “我的投资组合风险如何？”
- “我应该重新平衡投资组合吗？”
- “评估我的持仓”
- “投资组合表现评估”
- “我应该买入或卖出哪些股票？”
- 任何涉及投资组合级别分析或管理的请求

## 先决条件

### Alpaca MCP 服务器设置

使用此技能需要配置并连接 Alpaca MCP 服务器。MCP 服务器提供以下数据访问权限：
- 当前投资组合持仓
- 账户净值和买入能力
- 历史持仓和交易记录
- 持有证券的市场数据

**使用的 MCP 服务器工具：**
- `get_account_info` - 获取账户净值、买入能力和现金余额
- `get_positions` - 获取所有当前持仓的数量、成本基础和市场价值
- `get_portfolio_history` - 历史投资组合表现数据
- 市场数据工具，用于获取价格报价和基本信息

如果 Alpaca MCP 服务器未连接，请告知用户，并参考 `references/alpaca_mcp_setup.md` 中的设置说明进行配置。

## 工作流程

### 第一步：通过 Alpaca MCP 获取投资组合数据

使用 Alpaca MCP 服务器工具收集当前投资组合信息：

**1.1 获取账户信息：**
```
Use mcp__alpaca__get_account_info to fetch:
- Account equity (total portfolio value)
- Cash balance
- Buying power
- Account status
```

**1.2 获取当前持仓：**
```
Use mcp__alpaca__get_positions to fetch all holdings:
- Symbol ticker
- Quantity held
- Average entry price (cost basis)
- Current market price
- Current market value
- Unrealized P&L ($ and %)
- Position size as % of portfolio
```

**1.3 获取投资组合历史（可选）：**
```
Use mcp__alpaca__get_portfolio_history for performance analysis:
- Historical equity values
- Time-weighted return calculation
- Drawdown analysis
```

**数据验证：**
- 确认所有持仓的代码符号有效
- 核对市场价值总和是否接近账户净值
- 检查是否有过时或不活跃的持仓
- 处理特殊情况（如零股、期权、支持的加密货币）

### 第二步：丰富持仓数据

对于投资组合中的每个持仓，收集额外的市场数据和基本信息：

**2.1 当前市场数据：**
- 实时或延迟的价格报价
- 日成交量和流动性指标
- 52 周价格范围
- 市值

**2.2 基本数据：**
使用 WebSearch 或可用的市场数据 API 获取：
- 行业和领域分类
- 关键估值指标（市盈率、市净率、股息率）
- 最新收益和财务健康状况指标
- 分析师评级和价格目标
- 最新新闻和重要事件

**2.3 技术分析：**
- 价格趋势（20 日、50 日、200 日移动平均线）
- 相对强弱
- 支撑和阻力水平
- 动量指标（如 RSI、MACD）

### 第三步：投资组合级别分析

使用参考文件中的框架进行全面的投资组合分析：

#### 3.1 资产配置分析

**阅读参考资料/asset-allocation.md** 以了解配置框架**

从多个维度分析当前的资产配置：

**按资产类别：**
- 股票 vs 固定收益 vs 现金 vs 替代投资
- 与用户风险偏好的目标配置进行比较
- 评估配置是否符合投资目标

**按行业：**
- 科技、医疗保健、金融、消费等
- 识别行业集中度风险
- 与基准行业权重（如标准普尔 500 指数）进行比较

**按市值：**
- 大盘股 vs 中盘股 vs 小盘股分布
- 在大盘股中的集中度
- 市值多元化得分

**按地区：**
- 美国 vs 国际 vs 新兴市场
- 国内集中度风险评估

**输出格式：**
```markdown
## Asset Allocation

### Current Allocation vs Target
| Asset Class | Current | Target | Variance |
|-------------|---------|--------|----------|
| US Equities | XX.X% | YY.Y% | +/- Z.Z% |
| ... |

### Sector Breakdown
[Pie chart description or table with sector percentages]

### Top 10 Holdings
| Rank | Symbol | % of Portfolio | Sector |
|------|--------|----------------|--------|
| 1 | AAPL | X.X% | Technology |
| ... |
```

#### 3.2 多元化分析**

**阅读参考资料/diversification-principles.md** 以了解多元化理论**

评估投资组合的多元化质量：

**持仓集中度：**
- 识别主要持仓及其总权重
- 标记任何单一持仓是否超过投资组合的 10-15%
- 计算赫芬达尔-赫希曼指数（HHI）以衡量集中度

**行业集中度：**
- 识别主导行业
- 标记任何行业是否超过投资组合的 30-40%
- 与基准行业多样性进行比较

**相关性分析：**
- 估计主要持仓之间的相关性
- 识别高度相关的持仓（潜在的冗余）
- 评估真正的多元化效益

**持仓数量：**
- 个人投资组合的最佳范围：15-30 只股票
- 标记是否过度分散（<10 只股票）或过度分散（>50 只股票）

**输出：**
```markdown
## Diversification Assessment

**Concentration Risk:** [Low / Medium / High]
- Top 5 holdings represent XX% of portfolio
- Largest single position: [SYMBOL] at XX%

**Sector Diversification:** [Excellent / Good / Fair / Poor]
- Dominant sector: [Sector Name] at XX%
- [Assessment of balance across sectors]

**Position Count:** [Optimal / Under-diversified / Over-diversified]
- Total positions: XX stocks
- [Recommendation]

**Correlation Concerns:**
- [List any highly correlated position pairs]
- [Diversification improvement suggestions]
```

#### 3.3 风险分析**

**阅读参考资料/portfolio-risk-metrics.md** 以了解风险衡量框架**

计算并解释关键风险指标：

**波动性指标：**
- 估计的投资组合贝塔值（持仓贝塔值的加权平均值）
- 单个持仓的波动性
- 如果有历史数据，计算投资组合的标准差

**下行风险：**
- 从投资组合历史中得出的最大回撤
- 从峰值开始的当前回撤
- 有重大未实现损失的持仓

**风险集中度：**
- 高波动性股票的比例（贝塔值 > 1.5）
- 投资于投机性/无利可图公司的比例
- 杠杆使用情况（如适用）

**尾部风险：**
- 暴发黑天鹅事件的风险敞口
- 单个股票的风险集中度
- 行业特定事件的风险

**输出：**
```markdown
## Risk Assessment

**Overall Risk Profile:** [Conservative / Moderate / Aggressive]

**Portfolio Beta:** X.XX (vs market at 1.00)
- Interpretation: Portfolio is [more/less] volatile than market

**Maximum Drawdown:** -XX.X% (from $XXX,XXX to $XXX,XXX)
- Current drawdown from peak: -XX.X%

**High-Risk Positions:**
| Symbol | % of Portfolio | Beta | Risk Factor |
|--------|----------------|------|-------------|
| [TICKER] | XX% | X.XX | [High volatility / Recent loss / etc] |

**Risk Concentrations:**
- XX% in single sector ([Sector])
- XX% in stocks with beta > 1.5
- [Other concentration risks]

**Risk Score:** XX/100 ([Low/Medium/High] risk)
```

#### 3.4 表现分析**

使用可用数据评估投资组合表现：

**绝对回报：**
- 整体投资组合的未实现利润和亏损（金额和百分比）
- 表现最好的持仓（按收益百分比排名前 5）
- 表现最差的持仓（按亏损百分比排名后 5）

**时间加权回报（如果有历史数据）：**
- 年度回报
- 1 年、3 年、5 年的年化回报
- 与基准（标准普尔 500 指数）进行比较

**持仓级别表现：**
- 获胜持仓与亏损持仓的比例
- 获胜持仓的平均收益
- 失败持仓的平均损失
- 接近 52 周高点的持仓

**输出：**
```markdown
## Performance Review

**Total Portfolio Value:** $XXX,XXX
**Total Unrealized P&L:** $XX,XXX (+XX.X%)
**Cash Balance:** $XX,XXX (XX% of portfolio)

**Best Performers:**
| Symbol | Gain | Position Value |
|--------|------|----------------|
| [TICKER] | +XX.X% | $XX,XXX |
| ... |

**Worst Performers:**
| Symbol | Loss | Position Value |
|--------|------|----------------|
| [TICKER] | -XX.X% | $XX,XXX |
| ... |

**Performance vs Benchmark (if available):**
- Portfolio return: +X.X%
- S&P 500 return: +Y.Y%
- Alpha: +/- Z.Z%
```

### 第四步：个别持仓分析

对于投资组合中权重较高的前 10-15 只关键持仓，进行详细分析：

**阅读参考资料/position-evaluation.md** 以了解持仓分析框架

对于每个重要持仓：

**4.1 当前投资逻辑验证：**
- 为什么持有该持仓？（如果用户提供了背景信息）
- 投资逻辑是否成立或已失效？
- 公司的最新发展和新闻

**4.2 估值评估：**
- 当前的估值指标（市盈率、市净率等）
- 与历史估值范围进行比较
- 与行业同行进行比较
- 估值过高/合理/过低

**4.3 技术状况：**
- 价格趋势（上升趋势、下降趋势、横盘）
- 持仓相对于移动平均线的位置
- 支撑和阻力水平
- 动量状态

**4.4 持仓规模：**
- 在投资组合中的当前权重
- 鉴于信念和风险，规模是否合适？
- 是过度配置还是配置不足？

**4.5 行动建议：**
- **持有** - 持仓规模合适且投资逻辑成立
- **增加** - 如果有机会且投资逻辑得到加强
- **减少** - 如果过度配置或估值过高
- **卖出** - 如果投资逻辑失效或有其他更好的机会

**每个持仓的输出：**
```markdown
### [SYMBOL] - [Company Name] (XX.X% of portfolio)

**Position Details:**
- Shares: XXX
- Avg Cost: $XX.XX
- Current Price: $XX.XX
- Market Value: $XX,XXX
- Unrealized P/L: $X,XXX (+XX.X%)

**Fundamental Snapshot:**
- Sector: [Sector]
- Market Cap: $XX.XB
- P/E: XX.X | Dividend Yield: X.X%
- Recent developments: [Key news or earnings]

**Technical Status:**
- Trend: [Uptrend / Downtrend / Sideways]
- Price vs 50-day MA: [Above/Below by XX%]
- Support: $XX.XX | Resistance: $XX.XX

**Position Assessment:**
- **Thesis Status:** [Intact / Weakening / Broken / Strengthening]
- **Valuation:** [Undervalued / Fair / Overvalued]
- **Position Sizing:** [Optimal / Overweight / Underweight]

**Recommendation:** [HOLD / ADD / TRIM / SELL]
**Rationale:** [1-2 sentence explanation]
```

### 第五步：再平衡建议**

**阅读参考资料/rebalancing-strategies.md** 以了解再平衡方法**

生成具体的再平衡建议：

**5.1 识别再平衡触发因素：**
- 与目标权重偏离较大的持仓
- 需要调整的行业/资产类别配置
- 需要减少的过度配置持仓
- 需要增加的不足配置领域
- 税务考虑（资本利得影响）

**5.2 制定再平衡计划：**

**需要减少的持仓：**
- 过度配置的持仓（偏离目标超过阈值）
- 价格大幅上涨的持仓（存在估值问题）
- 集中度过高的持仓（超过投资组合的 15-20%）
- 投资逻辑失效的持仓

**需要增加的持仓：**
- 配置不足的行业或资产类别
- 目前配置不足但信心较高的持仓
- 有助于提高多样化的新机会

**现金分配：**
- 如果有超额现金（超过投资组合的 10%），建议如何分配
- 根据机会和配置缺口确定优先级

**5.3 优先级排序：**
按优先级排序再平衡行动：
1. **立即** - 降低风险（减少集中持仓）
2. **高优先级** - 主要配置偏离（偏离目标超过 10%）
3. **中等优先级** - 中等偏离（偏离目标 5-10%）
4. **低优先级** - 微调和机会性调整

**输出：**
```markdown
## Rebalancing Recommendations

### Summary
- **Rebalancing Needed:** [Yes / No / Optional]
- **Primary Reason:** [Concentration risk / Sector drift / Cash deployment / etc]
- **Estimated Trades:** X sell orders, Y buy orders

### Recommended Actions

#### HIGH PRIORITY: Risk Reduction
**TRIM [SYMBOL]** from XX% to YY% of portfolio
- **Shares to Sell:** XX shares (~$XX,XXX)
- **Rationale:** [Overweight / Valuation extended / etc]
- **Tax Impact:** $X,XXX capital gain (est)

#### MEDIUM PRIORITY: Asset Allocation
**ADD [Sector/Asset Class]** exposure
- **Target:** Increase from XX% to YY%
- **Suggested Stocks:** [SYMBOL1, SYMBOL2, SYMBOL3]
- **Amount to Invest:** ~$XX,XXX

#### CASH DEPLOYMENT
**Current Cash:** $XX,XXX (XX% of portfolio)
- **Recommendation:** [Deploy / Keep for opportunities / Reduce to X%]
- **Suggested Allocation:** [Distribution across sectors/stocks]

### Implementation Plan
1. [First action - highest priority]
2. [Second action]
3. [Third action]
...

**Timing Considerations:**
- [Tax year-end planning / Earnings season / Market conditions]
- [Suggested phasing if applicable]
```

### 第六步：生成投资组合报告

创建一个保存在仓库根目录下的综合 markdown 报告：

**文件名：** `portfolio_analysis_YYYY-MM-DD.md`

**报告结构：**
```markdown
# Portfolio Analysis Report

**Account:** [Account type if available]
**Report Date:** YYYY-MM-DD
**Portfolio Value:** $XXX,XXX
**Total P&L:** $XX,XXX (+XX.X%)

---

## Executive Summary

[3-5 bullet points summarizing key findings]
- Overall portfolio health assessment
- Major strengths
- Key risks or concerns
- Primary recommendations

---

## Holdings Overview

[Summary table of all positions]

---

## Asset Allocation
[Section from Step 3.1]

---

## Diversification Analysis
[Section from Step 3.2]

---

## Risk Assessment
[Section from Step 3.3]

---

## Performance Review
[Section from Step 3.4]

---

## Position Analysis
[Detailed analysis of top 10-15 positions from Step 4]

---

## Rebalancing Recommendations
[Section from Step 5]

---

## Action Items

**Immediate Actions:**
- [ ] [Action 1]
- [ ] [Action 2]

**Medium-Term Actions:**
- [ ] [Action 3]
- [ ] [Action 4]

**Monitoring Priorities:**
- [ ] [Watch list item 1]
- [ ] [Watch list item 2]

---

## Appendix: Full Holdings

[Complete table with all positions and metrics]
```

### 第七步：互动跟进

准备好回答后续问题：

**常见问题：**

**“我为什么应该卖出 [SYMBOL]？”**
- 解释具体原因（估值、投资逻辑失效、集中度）
- 提供支持数据
- 如果适用，提供替代持仓建议

**“我应该买入什么？”**
- 建议具体的股票以改善配置
- 解释它们如何解决投资组合的不足
- 提供简要的投资逻辑

**“我的最大风险是什么？”**
- 识别主要风险因素（集中度、行业敞口、波动性）
- 量化风险
- 建议缓解策略

**“我的投资组合与 [基准] 相比如何？”**
- 比较配置、行业权重、风险指标
- 强调关键差异
- 评估差异是否合理

**“我现在应该再平衡吗？还是等待？”**
- 考虑市场状况、税务影响、交易成本
- 提供带有理由的时间建议

**“你能更详细地分析 [特定持仓] 吗？”**
- 如有需要，使用 us-stock-analysis 技能进行深入分析
- 将分析结果整合回投资组合背景中

## 分析框架

### 目标配置模板

该技能包括针对不同投资者偏好的参考配置模型：

**阅读参考资料/target-allocations.md** 以了解详细模型：

- **保守型**（注重资本保值、收入）
- **平衡型**（平衡增长和收入）
- **成长型**（长期资本增值）
- **激进型**（追求最大增长、高风险承受能力）

每个模型包括：
- 资产类别目标（股票/债券/现金/替代投资）
- 行业指南
- 市值分布
- 地区配置
- 持仓规模规则

当用户未指定配置策略时，可以使用这些模型作为比较基准。

### 风险偏好评估

如果用户的目标配置未知，根据以下因素评估适当的风险偏好：
- 年龄（如果提及）
- 投资时间线（如果提及）
- 当前配置（反映偏好）
- 持仓类型（保守型 vs 投机型股票）

**阅读参考资料/risk-profile-questionnaire.md** 以了解评估框架

## 输出指南

**语气和风格：**
- 客观和分析性
- 提出具有明确理由的可操作建议
- 承认市场预测的不确定性
- 在乐观与风险意识之间保持平衡
- 尽可能量化数据

**数据呈现：**
- 用于比较和指标的表格
- 配置和回报的百分比
- 绝对值的美元金额
- 报告中的格式保持一致

**建议的清晰度：**
- 明确的行动动词（减少、增加、持有、卖出）
- 具体的数量（卖出 XX 股票、增加 $X,XXX）
- 优先级级别（立即、高、中、低）
- 每项建议的支持理由

**视觉描述：**
- 以饼图的形式描述配置分布
- 用条形图表示行业权重
- 使用方向指示符表示表现趋势（↑ ↓ →）

## 参考文件

在分析过程中根据需要加载这些参考文件：

**references/alpaca-mcp-setup.md**
- 适用场景：用户需要帮助设置 Alpaca MCP 服务器时
- 内容：安装说明、API 密钥配置、MCP 服务器连接步骤、故障排除

**references/asset-allocation.md**
- 适用场景：分析投资组合配置或制定再平衡计划时
- 内容：资产配置理论、根据风险偏好的最佳配置、行业配置指南、再平衡触发因素

**references/diversification-principles.md**
- 适用场景：评估投资组合的多元化质量时
- 内容：现代投资组合理论基础、相关性概念、最佳持仓数量、集中度风险阈值、多元化指标

**references/portfolio-risk-metrics.md**
- 适用场景：计算风险分数或解释波动性时
- 内容：贝塔值计算、标准差、夏普比率、最大回撤、风险调整后回报指标

**references/position-evaluation.md**
- 适用场景：分析个别持仓以做出买入/持有/卖出决策时
- 内容：持仓分析框架、投资逻辑验证清单、持仓规模指南、卖出纪律标准

**references/rebalancing-strategies.md**
- 适用场景：制定再平衡建议时
- 内容：再平衡方法（基于日历、基于阈值的策略）、税务优化策略、交易成本考虑、实施时机

**references/target-allocations.md**
- 适用场景：需要基准配置进行比较时
- 内容：为保守型/平衡型/成长型/激进型投资者准备的模型投资组合、行业目标范围、市值分布

**references/risk-profile-questionnaire.md**
- 适用场景：用户未指定风险承受能力或目标配置时
- 内容：风险评估问题、评分方法、风险偏好分类

## 错误处理

**如果 Alpaca MCP 服务器未连接：**
1. 告知用户需要集成 Alpaca
2. 提供来自 references/alpaca-mcp-setup.md 的设置说明
3. 提供替代方案：手动输入数据（不太理想，用户提供持仓的 CSV 文件）

**如果 API 返回的数据不完整：**
- 使用可用数据继续分析
- 在报告中注明数据限制
- 建议手动验证缺失的持仓

**如果持仓数据似乎过时：**
- 标记问题
- 建议刷新连接或检查 Alpaca 的状态
- 继续分析，但需对结果有所了解

**如果用户没有持仓：**
- 承认投资组合为空
- 提供投资组合构建指导，而不是进行分析
- 建议使用 value-dividend-screener 或 us-stock-analysis 来寻找投资机会

## 高级功能

### 税务损失收割机会

识别适合进行税务损失收割的持仓：
- 损失超过 5% 的持仓
- 考虑持有期（避免洗售规则）
- 建议替换证券（类似但不完全相同的股票）

### 股息收入分析

对于持有分红股票的投资组合：
- 估计年度股息收入
- 股息增长率趋势
- 股息覆盖率和可持续性
- 长期持有的股息收益率

### 相关性矩阵

对于拥有 5-20 只持仓的投资组合：
- 估计主要持仓之间的相关性
- 识别冗余持仓（相关性 >0.8）
- 建议改进多元化

### 情景分析

模拟不同情景下的投资组合表现：
- **牛市**（股票价格上涨 20%）
- **熊市**（股票价格下跌 20%）
- **行业轮动**（科技行业疲软、价值行业强劲）
- **利率上升**（对成长股和债券的影响）

## 示例查询**

**基本投资组合审查：**
- “分析我的投资组合”
- “查看我的持仓”
- “我的投资组合表现如何？”

**配置分析：**
- “我的资产配置是什么？”
- “我在科技行业的配置是否过于集中？”
- “展示我的行业分布”

**风险评估：**
- “我的投资组合风险是否过高？”
- “我的投资组合贝塔值是多少？”
- “我的最大风险是什么？”

**再平衡：**
- “我应该再平衡吗？”
- “我应该买入或卖出什么？”
- “如何提高多元化？”

**表现分析：**
- “我的最佳和最差持仓是什么？”
- “我的表现与市场相比如何？”
- “哪些股票表现好，哪些表现差？”

**个别持仓：**
- “我应该卖出 [SYMBOL] 吗？”
- “[SYMBOL] 在我的投资组合中的权重是否过高？”
- “我应该如何处理 [SYMBOL]？”

## 限制和免责声明**

**在所有报告中包含以下内容：**

*本分析仅用于信息目的，不构成财务建议。投资决策应基于个人情况、风险承受能力和财务目标。过去的表现不能保证未来的结果。在做出投资决策前，请咨询合格的财务顾问。*

*数据准确性取决于 Alpaca API 和第三方市场数据源。请独立验证关键信息。税务影响仅为估计值；请咨询税务专业人士以获取具体指导。*