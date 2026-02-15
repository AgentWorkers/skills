---
name: pair-trade-screener
description: **统计套利工具：用于识别和分析配对交易机会**  
该工具专门用于发现和分析股票配对交易中的套利机会。它能识别同一行业内的共整关系（即股票价格之间存在长期稳定的联动关系），分析价差波动行为，计算相关指标的z分数，并为市场中性策略提供买入/卖出建议。适用于用户需要寻找配对交易机会、进行统计套利筛选、实施均值回归策略或构建市场中性投资组合的场景。工具支持相关性分析、共整性检验以及价差回测功能。
---

# 对冲交易筛选器

## 概述

该技能通过对冲交易识别并分析统计套利机会。对冲交易是一种市场中性策略，它从两只相关证券的相对价格变动中获利，而不受整体市场方向的影响。该技能使用包括相关性分析和协整性测试在内的严格统计方法来寻找可靠的交易对。

**核心方法论：**
- 识别具有高相关性和相似行业/领域敞口的股票对
- 测试协整性（长期统计关系）
- 计算价差z分数以识别均值回归机会
- 根据统计阈值生成买入/卖出信号
- 提供市场中性敞口的头寸规模建议

**主要优势：**
- 市场中性：无论市场上涨、下跌还是盘整，都能获利
- 风险管理：对市场整体波动的敞口有限
- 基于数据：以数据为驱动，而非主观判断
- 分散化：与传统仅做多策略不同

## 何时使用此技能

在以下情况下使用此技能：
- 用户请求“对冲交易机会”
- 用户希望使用“市场中性策略”
- 用户请求“统计套利筛选”
- 用户询问“哪些股票会一起波动”
- 用户希望对冲行业敞口
- 用户询问均值回归交易策略

示例用户请求：
- “在科技行业中寻找对冲交易机会”
- “哪些股票是协整的？”
- “筛选统计套利机会”
- “找到均值回归对”
- “目前哪些是对冲交易的好选择？”

## 分析工作流程

### 第1步：定义股票池

**目标：**确定用于分析股票对关系的股票池。

**选项A：基于行业的筛选（推荐）**

选择特定行业进行筛选：
- 科技
- 金融
- 医疗保健
- 消费品
- 工业
- 能源
- 材料
- 消费必需品
- 公用事业
- 房地产
- 通信服务

**选项B：自定义股票列表**

用户提供具体的股票代码进行分析：
```
Example: ["AAPL", "MSFT", "GOOGL", "META", "NVDA"]
```

**选项C：特定行业**

在行业内进一步聚焦于特定行业：
- 例如：科技行业中的“软件”
- 例如：金融行业中的“地区性银行”

**筛选标准：**
- 最小市值：20亿美元（中盘及以上）
- 最小日均成交量：100万股（流动性要求）
- 活跃交易：无退市或不活跃的股票
- 同一交易所：避免跨交易所的复杂性

### 第2步：获取历史价格数据

**目标：**获取用于相关性和协整性分析的价格历史数据。

**数据要求：**
- 时间范围：2年（至少252个交易日）
- 频率：每日收盘价
- 调整：考虑股票分割和股息
- 数据清洗：无缺失值

**FMP API端点：**
```
GET /v3/historical-price-full/{symbol}?apikey=YOUR_API_KEY
```

**数据验证：**
- 确保所有股票的时间范围一致
- 删除缺失数据超过10%的股票
- 用前向填充方法填补小范围的数据缺失
- 记录数据质量问题

**脚本执行：**
```bash
python scripts/fetch_price_data.py --sector Technology --lookback 730
```

### 第3步：计算相关性和贝塔系数

**目标：**识别具有强线性关系的候选股票对。

**相关性分析：**

对于股票池中的每对股票（i, j）：
1. 计算皮尔逊相关系数（ρ）
2. 计算90天窗口的滚动相关性（稳定性检查）
3. 筛选ρ ≥ 0.70的对（强正相关）

**相关性解释：**
- ρ ≥ 0.90：非常强相关（最佳候选）
- ρ 0.70-0.90：强相关（良好候选）
- ρ 0.50-0.70：中等相关（边缘相关）
- ρ < 0.50：弱相关（排除）

**贝塔系数计算：**

对于每对候选股票（股票A，股票B）：
```
Beta = Covariance(A, B) / Variance(B)
```

贝塔系数表示对冲比率：
- Beta = 1.0：等额投资
- Beta = 1.5：每投资1美元股票A，就投资1.5美元股票B
- Beta = 0.8：每投资1美元股票A，就投资0.8美元股票B

**相关性稳定性检查：**
- 在多个时期（6个月、1年、2年）计算相关性
- 要求相关性保持稳定（不恶化）
- 标记近期相关性比历史相关性低超过0.15的对

### 第4步：协整性测试

**目标：**统计验证长期均衡关系。

**为什么协整性很重要：**
- 相关性衡量短期共动性
- 协整性证明长期均衡关系
- 协整的对具有可预测的均值回归特性
- 非协整的对可能会永久分离

**增强型迪基-富勒（ADF）测试：**

对于每对相关股票：
1. 计算价差：`价差 = 股票A价格 - （贝塔 × 股票B价格）`
2. 对价差序列运行ADF测试
3. 检查p值：p < 0.05表示协整（拒绝单位根的零假设）
4. 提取ADF统计量以进行强度排名

**协整性解释：**
- p值 < 0.01：非常强协整（★★★）
- p值 0.01-0.05：中等协整（★★）
- p值 > 0.05：无协整（排除）

**半衰期计算：**

估计均值回归速度：
```
Half-Life = -log(2) / log(mean_reversion_coefficient)
```

- 半衰期 < 30天：快速均值回归（适合短期交易）
- 半衰期 30-60天：中等速度（标准）
- 半衰期 > 60天：缓慢均值回归（适合长期持有）

**Python实现：**
```python
from statsmodels.tsa.stattools import adfuller

# Calculate spread
spread = price_a - (beta * price_b)

# ADF test
result = adfuller(spread)
adf_stat = result[0]
p_value = result[1]

# Interpret
is_cointegrated = p_value < 0.05
```

### 第5步：价差分析和Z分数计算

**目标：**量化当前价差与均衡状态的偏差。

**价差计算：**

两种常见方法：

**方法1：价格差（加法）**
```
Spread = Price_A - (Beta × Price_B)
```
适用于：价格水平相似的股票

**方法2：价格比率（乘法）**
```
Spread = Price_A / Price_B
```
适用于：价格水平不同的股票，解释更简单

**Z分数计算：**

衡量价差与其均值的偏离程度（以标准差为单位）：
```
Z-Score = (Current_Spread - Mean_Spread) / Std_Dev_Spread
```

**Z分数解释：**
- Z > +2.0：股票A相对于股票B价格过高（做空股票A，买入股票B）
- Z > +1.5：价格适中（考虑买入）
- Z -1.5至+1.5：正常范围（不进行交易）
- Z < -1.5：股票A相对于股票B价格过低（买入股票A，卖出股票B）

**历史价差分析：**
- 计算90天滚动窗口内的平均值和标准差
- 绘制历史Z分数分布图
- 识别最大的历史Z分数偏差
- 检查结构性的变化（价差模式的变化）

### 第6步：生成买入/卖出建议

**目标：**提供具有明确规则的可行交易信号。

**买入条件：**

**保守方法（Z ≥ ±2.0）：**
```
LONG Signal:
- Z-score < -2.0 (spread 2+ std devs below mean)
- Spread is mean-reverting (cointegration p < 0.05)
- Half-life < 60 days
→ Action: Buy Stock A, Short Stock B (hedge ratio = beta)

SHORT Signal:
- Z-score > +2.0 (spread 2+ std devs above mean)
- Spread is mean-reverting (cointegration p < 0.05)
- Half-life < 60 days
→ Action: Short Stock A, Buy Stock B (hedge ratio = beta)
```

**激进方法（Z ≥ ±1.5）：**
- 较低的阈值，交易频率更高
- 胜率较高，但每次交易的平均利润较低
- 需要更严格的风险管理

**卖出条件：**

**主要卖出条件：均值回归（Z = 0）**
```
Exit when spread returns to mean (z-score crosses 0)
→ Close both legs simultaneously
```

**次要卖出条件：部分获利**  
```
Exit 50% when z-score reaches ±1.0
Exit remaining 50% at z-score = 0
```

**止损：**  
```
Exit if z-score extends beyond ±3.0 (extreme divergence)
Risk: Possible structural break in relationship
```

**基于时间的卖出：**  
```
Exit after 90 days if no mean-reversion
Prevents holding broken pairs indefinitely
```

### 第7步：头寸规模和风险管理

**目标：**确定市场中性敞口的金额。

**市场中性头寸规模：**

对于一对股票（股票A，股票B），其贝塔系数为β：

**等额投资：**
```
If portfolio size = $10,000 allocated to this pair:
- Long $5,000 of Stock A
- Short $5,000 × β of Stock B

Example (β = 1.2):
- Long $5,000 Stock A
- Short $6,000 Stock B
→ Market neutral, beta = 0
```

**头寸规模考虑因素：**
- 每对股票的总配置：投资组合的10-20%
- 最多活跃股票对：5-8对（以实现分散化）
- 避免高度相关的股票对

**风险指标：**
- 每对股票的最大损失：投资组合总风险的2-3%
- 止损触发条件：Z分数 > ±3.0或价差损失超过5%
- 投资组合层面的风险：所有股票对风险之和 ≤ 10%

### 第8步：生成股票对分析报告

**目标：**创建包含发现和建议的结构化Markdown报告。

**报告章节：**

1. **执行摘要**
   - 分析的股票对总数
   - 找到的协整股票对数量
   - 按统计强度排名的前5个机会

2. **协整股票对表格**
   - 股票对名称（股票A / 股票B）
   - 相关系数
   - 协整性p值
   - 当前Z分数
   - 交易信号（买入/卖出/无）
   - 半衰期

3. **详细分析（前10对）**
   - 股票对描述
   - 统计指标
   - 当前价差状况
   - 买入/卖出建议
   - 头寸规模
   - 风险评估

4. **价差图表（文本形式）**
   - 历史Z分数图表（ASCII艺术）
   - 买入/卖出水平标记
   - 当前头寸指示器

5. **风险警告**
   - 相关性下降的股票对
   - 检测到的结构变化
   - 流动性低警告

**文件命名 convention：**
```
pair_trade_analysis_[SECTOR]_[YYYY-MM-DD].md
```

示例：`pair_trade_analysis_Technology_2025-11-08.md`

## 质量标准

### 统计严谨性

**有效股票对的最低要求：**
- ✓ 在2年期间相关性 ≥ 0.70
- ✓ 协整性p值 < 0.05（ADF测试）
- ✓ 价差稳定性得到确认
- ✓ 半衰期 < 90天
- ✓ 近6个月内无结构性变化

**排除标准：**
- 近6个月内相关性下降超过0.20
- 协整性p值 > 0.05
- 半衰期随时间增加（均值回归减弱）
- 重大公司事件（合并、分拆、破产风险）
- 流动性问题（日均成交量 < 50万股）

### 实际考虑

**交易成本：**
- 假设每笔交易的往返费用为0.1%
- 每对股票的总成本 = 0.4%（买入 + 卖出）
- 最小Z分数阈值应高于交易成本

**卖空：**
- 确认股票可卖空（不易借入）
- 考虑卖空利息成本
- 监控卖空挤压风险

**执行：**
- 同时买入/卖出两只股票（避免单只股票的风险）
- 使用限价单控制滑点
- 在买入前预先定位卖空头寸

## 可用脚本

### scripts/find_pairs.py

**用途：**在特定行业或自定义列表中筛选协整股票对。

**用法：**
```bash
# Sector-based screening
python scripts/find_pairs.py --sector Technology --min-correlation 0.70

# Custom stock list
python scripts/find_pairs.py --symbols AAPL,MSFT,GOOGL,META --min-correlation 0.75

# Full options
python scripts/find_pairs.py \
  --sector Financials \
  --min-correlation 0.70 \
  --min-market-cap 2000000000 \
  --lookback-days 730 \
  --output pairs_analysis.json
```

**参数：**
- `--sector`：行业名称（科技、金融等）
- `--symbols`：用逗号分隔的股票代码列表（替代行业）
- `--min-correlation`：最小相关性阈值（默认：0.70）
- `--min-market-cap`：最小市值过滤器（默认：20亿美元）
- `--lookback-days`：历史数据周期（默认：730天）
- `--output`：输出JSON文件（默认：标准输出）
- `--api-key`：FMP API密钥（或设置FMP_API_KEY环境变量）

**输出：**
```json
[
  {
    "pair": "AAPL/MSFT",
    "stock_a": "AAPL",
    "stock_b": "MSFT",
    "correlation": 0.87,
    "beta": 1.15,
    "cointegration_pvalue": 0.012,
    "adf_statistic": -3.45,
    "half_life_days": 42,
    "current_zscore": -2.3,
    "signal": "LONG",
    "strength": "Strong"
  }
]
```

### scripts/analyze_spread.py

**用途：**分析特定股票对的价差行为并生成交易信号。

**用法：**
```bash
# Analyze specific pair
python scripts/analyze_spread.py --stock-a AAPL --stock-b MSFT

# Custom lookback period
python scripts/analyze_spread.py \
  --stock-a JPM \
  --stock-b BAC \
  --lookback-days 365 \
  --entry-zscore 2.0 \
  --exit-zscore 0.5
```

**参数：**
- `--stock-a`：第一只股票代码
- `--stock-b`：第二只股票代码
- `--lookback-days`：分析周期（默认：365天）
- `--entry-zscore`：买入的Z分数阈值（默认：2.0）
- `--exit-zscore`：卖出的Z分数阈值（默认：0.0）
- `--api-key`：FMP API密钥

**输出：**
- 当前价差分析
- Z分数计算
- 买入/卖出建议
- 头寸规模
- 历史Z分数图表（文本）

## 参考文档

### references/methodology.md

关于统计套利和对冲交易的全面指南：
- **股票对选择标准**：如何识别好的股票对候选者
- **统计测试**：相关性、协整性、稳定性
- **价差构建**：价格差方法与价格比率方法
- **均值回归**：半衰期计算和解释
- **风险管理**：头寸规模、止损、分散化
- **常见陷阱**：生存偏差、前瞻偏差、过拟合

### references/cointegration_guide.md

深入探讨协整性测试：
- **什么是协整？**：直观解释
- **ADF测试**：逐步说明
- **P值解释**：统计显著性阈值
- **半衰期估计**：AR(1)模型方法
- **结构变化检测**：检测模式变化
- **实际案例**：使用真实股票对的案例研究

## 与其他技能的集成

**行业分析师集成：**
- 使用行业分析师识别轮动的行业
- 在表现优异的行业中筛选股票对
- 行业领先的对可能具有更强的趋势

**技术分析师集成：**
- 使用技术分析确认股票对的买入/卖出时机
- 在买入前检查支撑/阻力水平
- 确认趋势方向与价差信号一致

**回测专家集成：**
- 将股票对候选者输入回测专家进行验证
- 测试历史Z分数的买入/卖出规则
- 优化阈值参数（买入Z分数、止损）
- 进行前瞻性分析以验证稳健性

**市场环境分析集成：**
- 在极端波动期间（VIX > 30）避免对冲交易
- 在危机时期相关性可能崩溃
- 偏好在盘整/区间市场中进行对冲交易

**投资组合经理集成：**
- 跟踪多个股票对的头寸
- 监控整体市场中性敞口
- 计算投资组合层面的对冲交易利润率
- 定期重新平衡对冲比率

## 重要说明

- **所有分析和输出均为英文**
- **基于统计数据**：无主观解释
- **市场中性策略**：最小化方向性贝塔敞口
- **数据质量至关重要**：数据质量直接影响结果
- **需要FMP API密钥**：免费 tier足以进行基本筛选
- **Python依赖库**：pandas、numpy、scipy、statsmodels

## 常见用例

**用例1：科技行业股票对**
```
User: "Find pair trading opportunities in tech stocks"

Workflow:
1. Screen Technology sector for stocks with market cap > $10B
2. Calculate all pairwise correlations
3. Filter pairs with correlation ≥ 0.75
4. Run cointegration tests
5. Identify current z-score extremes (|z| > 2.0)
6. Generate top 10 pairs report
```

**用例2：特定股票对分析**
```
User: "Analyze AAPL and MSFT as a pair trade"

Workflow:
1. Fetch 2-year price history for AAPL and MSFT
2. Calculate correlation and beta
3. Test for cointegration
4. Calculate current spread and z-score
5. Generate entry/exit recommendation
6. Provide position sizing guidance
```

**用例3：地区性银行股票对**
```
User: "Screen for pairs among regional banks"

Workflow:
1. Filter Financials sector for industry = "Regional Banks"
2. Exclude banks with <$5B market cap
3. Calculate pairwise statistics
4. Rank by cointegration strength
5. Focus on pairs with half-life < 45 days
6. Report top 5 mean-reverting pairs
```

## 故障排除

**问题：未找到协整股票对**

解决方案：
- 扩大股票池（降低市值阈值）
- 将协整性p值放宽至0.10
- 尝试不同的行业（公用事业行业通常具有较好的协整性）
- 将回顾周期延长至3年

**问题：所有Z分数接近零（无交易信号）**

解决方案：
- 市场处于正常状态（股票对处于均衡状态）
- 稍后重新检查或扩大股票池
- 将买入阈值降低至±1.5而不是±2.0

**问题：股票对的相关性下降**

解决方案：
- 检查公司事件（收益、指导方针变化）
- 确认没有并购活动或重组
- 如果确认结构变化，从观察名单中移除股票对
- 重新进入前观察30天

## API要求

- **必需**：FMP API密钥（免费 tier足够）
- **流量限制**：免费 tier每天约250次请求
- **数据使用**：每个股票约2次请求，用于2年的历史数据
- **升级**：建议使用专业计划（每月29美元）以进行频繁筛选

## 资源

- **FMP历史价格API**：https://site.financialmodelingprep.com/developer/docs/historical-price-full
- **股票筛选API**：https://site.financialmodelingprep.com/developer/docs/stock-screener-api
- **statsmodels文档**：https://www.statsmodels.org/stable/index.html
- **协整性论文**：Engle & Granger (1987) - “Co-Integration and Error Correction”

---

**版本**：1.0
**最后更新时间**：2025-11-08
**依赖库**：Python 3.8+、pandas、numpy、scipy、statsmodels、requests