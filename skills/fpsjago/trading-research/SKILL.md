---
name: trading-research
description: 币安（Binance）的加密货币交易研究、技术分析以及仓位管理服务。当用户提出关于加密货币价格、市场数据、交易分析、定期定额投资（DCA）计划、仓位规模调整、大户交易行为，或任何与比特币、山寨币及加密货币市场相关的问题时，这些服务便会自动启动。
---

# 交易研究技能

这是一套全面的加密货币交易研究和分析工具，专注于Binance市场。专为采用定期定额投资（DCA）策略、且风险偏好较为保守或中等的投资者设计，同时提供技术分析支持。

## 适用场景

当用户需要以下信息时，可激活此技能：
- 当前加密货币价格或市场数据
- 技术分析结果（如RSI、MACD、Bollinger Bands等）
- DCA策略规划或投资计划计算
- 基于风险管理的持仓规模确定
- 市场机会扫描
- 大额交易（“鲸鱼交易”）监控
- 交易策略建议或风险评估

## 核心理念

- **保守优先**：保护资本，最小化风险
- **以DCA为核心**：长期持有优于市场时机选择
- **风险管理**：每次交易的风险不超过1-2%
- **数据驱动**：使用技术指标进行确认，而非预测
- **透明化**：展示计算过程，解释分析逻辑

## 可用工具

### 1. 市场数据（`binance_market.py`）

获取Binance市场的实时数据。

**使用场景**：用户查询价格、成交量、订单簿、近期交易记录或资金费率。

**常用命令**：
```bash
# Current price and 24h stats (default)
python3 scripts/binance_market.py --symbol BTCUSDT

# Orderbook depth
python3 scripts/binance_market.py --symbol BTCUSDT --orderbook --depth 20

# Candlestick data
python3 scripts/binance_market.py --symbol BTCUSDT --klines 1h --limit 100

# Recent trades
python3 scripts/binance_market.py --symbol BTCUSDT --trades --limit 100

# Funding rate (futures)
python3 scripts/binance_market.py --symbol BTCUSDT --funding

# All data at once
python3 scripts/binance_market.py --symbol BTCUSDT --all

# JSON output (for piping)
python3 scripts/binance_market.py --symbol BTCUSDT --json > btc_data.json
```

**时间间隔**：1分钟、5分钟、15分钟、30分钟、1小时、4小时、1天、1周

### 2. 技术分析（`technical_analysis.py`

计算并解读技术指标。

**使用场景**：用户需要技术分析结果、指标数据、买卖信号或市场趋势分析。

**常用命令**：
```bash
# Full analysis (default: 1h timeframe, 200 candles)
python3 scripts/technical_analysis.py --symbol BTCUSDT

# Different timeframe
python3 scripts/technical_analysis.py --symbol BTCUSDT --interval 4h

# Custom RSI period
python3 scripts/technical_analysis.py --symbol BTCUSDT --rsi-period 21

# From saved klines JSON
python3 scripts/technical_analysis.py --input btc_klines.json

# JSON output
python3 scripts/technical_analysis.py --symbol BTCUSDT --json
```

**分析内容**：
- 趋势方向（SMA 20/50、EMA 12/26）
- RSI（14）：超买/超卖信号
- MACD：动量及交叉点
- Bollinger Bands：波动性及买卖信号
- 支撑/阻力位
- 成交量分析
- 交易建议

### 3. 定期定额投资计算器（`dca_calculator.py`

帮助用户规划定期定额投资策略。

**使用场景**：用户希望设置DCA计划、计算投资时间表或比较不同策略。

**常用命令**：
```bash
# Basic DCA plan
python3 scripts/dca_calculator.py --total 5000 --frequency weekly --duration 180

# With current price for projections
python3 scripts/dca_calculator.py --total 10000 --frequency monthly --duration 365 --current-price 100000

# Show scenario analysis
python3 scripts/dca_calculator.py --total 5000 --frequency weekly --duration 180 --current-price 100000 --scenarios

# Custom start date
python3 scripts/dca_calculator.py --total 5000 --frequency weekly --duration 180 --start-date 2026-03-01

# JSON output
python3 scripts/dca_calculator.py --total 5000 --frequency weekly --duration 180 --json
```

**投资频率**：每日、每周、每两周、每月

**输出内容**：
- 显示每次投资的日期和金额
- 总投资次数及每次投资金额
- 不同市场环境（牛市/熊市）下的投资效果
- 与一次性投资的对比

### 4. 持仓规模确定器（`position_sizer.py**

根据风险管理规则计算安全持仓规模。

**使用场景**：用户准备入场交易时，需要确定持仓规模、止损点或止盈点。

**常用命令**：
```bash
# Basic position sizing (2% risk recommended)
python3 scripts/position_sizer.py --balance 10000 --risk 2 --entry 100000 --stop-loss 95000

# Conservative 1% risk
python3 scripts/position_sizer.py --balance 10000 --risk 1 --entry 100000 --stop-loss 97000

# Custom take-profit ratios
python3 scripts/position_sizer.py --balance 10000 --risk 2 --entry 100000 --stop-loss 95000 --take-profit 2 3 5

# Ladder strategy (scaling in)
python3 scripts/position_sizer.py --balance 10000 --risk 2 --entry 100000 --stop-loss 95000 --ladder 3

# JSON output
python3 scripts/position_sizer.py --balance 10000 --risk 2 --entry 100000 --stop-loss 95000 --json
```

**输出内容**：
- 持仓规模（单位及美元金额）
- 风险金额（美元）
- 多个止盈比例下的止盈点
- 持仓比例（占账户资金的百分比）
- 如果持仓过大时的警告提示

**规则**：
- 保守策略：每次交易风险不超过1%
- 中等风险策略：每次交易风险不超过2%
- 总风险不超过3%
- 持仓比例应低于账户资金的50%

### 5. 市场扫描器（`market_scanner.py**

扫描Binance所有USDT交易对，寻找交易机会。

**使用场景**：用户希望发现价格波动较大的交易对或新的投资机会。

**常用命令**：
```bash
# Full market scan (default)
python3 scripts/market_scanner.py

# Top gainers only
python3 scripts/market_scanner.py --gainers --limit 20

# High volume pairs
python3 scripts/market_scanner.py --volume

# Most volatile pairs
python3 scripts/market_scanner.py --volatile

# Breakout candidates (near 24h high with volume)
python3 scripts/market_scanner.py --breakout

# Filter by minimum volume
python3 scripts/market_scanner.py --min-volume 500000

# JSON output
python3 scripts/market_scanner.py --json
```

**扫描类别**：
- 24小时内涨幅最大的交易对
- 24小时内跌幅最大的交易对
- 成交量最大的交易对
- 波动性最高的交易对
- 可能的突破点（接近24小时高点且成交量大的交易对）

### 6. 大额交易监控器（`whale_tracker.py**

监控大额交易和订单簿不平衡情况。

**使用场景**：用户关注大额交易或订单簿的异常情况。

**常用命令**：
```bash
# Full whale analysis (default)
python3 scripts/whale_tracker.py --symbol BTCUSDT

# Large trades only
python3 scripts/whale_tracker.py --symbol BTCUSDT --trades

# Orderbook imbalances only
python3 scripts/whale_tracker.py --symbol BTCUSDT --orderbook

# Custom orderbook depth
python3 scripts/whale_tracker.py --symbol BTCUSDT --orderbook --depth 50

# Adjust threshold (default 90th percentile)
python3 scripts/whale_tracker.py --symbol BTCUSDT --threshold 95

# JSON output
python3 scripts/whale_tracker.py --symbol BTCUSDT --json
```

**输出内容**：
- 按金额排名前十的大额交易
- 大额交易的买卖压力
- 订单簿的买卖不平衡情况
- 市场情绪（看涨/看跌/中性）

## 快速操作流程

- **查询BTC价格**：```bash
# Get overview
python3 scripts/binance_market.py --symbol BTCUSDT --ticker

# Technical analysis
python3 scripts/technical_analysis.py --symbol BTCUSDT --interval 1h
```
- **是否现在买入？**：```bash
# Check technicals first
python3 scripts/technical_analysis.py --symbol BTCUSDT

# Check whale activity
python3 scripts/whale_tracker.py --symbol BTCUSDT

# If signals look good, calculate position size
python3 scripts/position_sizer.py --balance 10000 --risk 2 --entry <CURRENT_PRICE> --stop-loss <SUPPORT_LEVEL>
```
- **设置DCA计划**：```bash
# Plan the strategy
python3 scripts/dca_calculator.py --total 5000 --frequency weekly --duration 180 --current-price <CURRENT_PRICE> --scenarios

# Show them the schedule and explain
```
- **寻找投资机会**：```bash
# Scan market
python3 scripts/market_scanner.py

# For interesting pairs, do deeper analysis
python3 scripts/technical_analysis.py --symbol <PAIR>
python3 scripts/whale_tracker.py --symbol <PAIR>
```
- **市场情绪如何？**：```bash
# Check whale activity
python3 scripts/whale_tracker.py --symbol BTCUSDT

# Check volume and volatility
python3 scripts/market_scanner.py --volume --volatile
```

## 参考资料

相关资料位于`references/`目录下：

### `binance-api.md`
- API接口及参数
- 请求速率限制
- 认证流程
- 订单类型及有效期
- 错误代码
- Python代码示例

**使用场景**：需要API详细信息、构建自定义查询或解决技术问题

### `indicators.md`
- 技术指标公式及解读方法
- 不同时间段的常用设置
- 指标组合使用方法
- 指标可靠性评估
- 常见错误及避免方法

**使用场景**：向用户解释技术指标、解读交易信号或提供培训

### `strategies.md`
- 各种DCA策略（固定金额、基于价值的策略、基于RSI的策略等）
- 风险管理方法（每次交易风险不超过1-2%）
- 跟踪趋势的策略
- 入场/出场策略示例
- 持仓规模计算方法
- 绩效跟踪方法

**使用场景**：制定交易计划、解释交易策略或解答风险管理相关问题

## 交易指导

### 适合保守型投资者的策略

- **定期定额投资（DCA）**：
- 从每周或每月一次的投资开始
- 每次投资金额固定（50-200美元）
- 投资期限至少6-12个月
- 不要试图预测市场时机
- 长期持有

- **风险管理**：
- 不使用杠杆
- 账户资金中至少50%用于现金或稳定币
- 每次交易风险不超过1%
- 只在有多个技术确认信号时才进行交易
- 始终设置止损

### 适合中等风险投资者的策略

- **优化后的DCA**：
- 根据RSI调整投资金额（超卖时增加投资）
- 结合技术分析优化入场时机
- 60-70%的资金用于DCA，30-40%用于主动交易
- 活动中的持仓每次交易风险不超过2%

- **趋势交易**：
- 等待多个指标一致发出买入/卖出信号
- 使用`position_sizer.py`确定每次交易的持仓规模
- 风险回报比至少为2:1
- 随着利润增长调整止损点

### 需避免的交易信号

- RSI超过70且持续上升（超买信号）
- 低成交量下的价格突破（可能为假信号）
- 逆势交易（在牛市中不要做空）
- 多个指标出现矛盾信号
- 没有明确的止损支撑位
- 风险回报比低于1.5:1
- 在极端恐惧或贪婪的情绪下不要交易

## 回答格式

当用户请求分析时，提供以下信息：
- **当前市场状况**：价格、趋势及关键技术指标
- **技术分析结果**：指标数值及其含义
- **市场情绪**：大额交易活动、成交量及市场压力
- **交易建议**：包括买入/等待/卖出的理由及依据
- **风险管理建议**：持仓规模、止损点及止盈点
- **注意事项**：可能出现的风险及替代方案

**必包含内容**：
- 具体数据（例如“RSI为28”）
- 对交易的风险提示
- 明确的下一步操作建议
- 适用的交易时间范围（日内交易、波段交易或长期投资）

## 重要说明

- **API访问**：
  所有脚本均使用Binance的公共API（无需额外认证）
  脚本中已设置请求速率限制
  如果因地理位置限制导致API无法访问，脚本会友好地提示错误

**限制事项**：
- **仅用于研究**：这些工具不支持实际交易执行
- **非实时数据**：数据基于快照（REST API）
- **不支持期货交易**：主要针对现货市场（资金费率除外）
- **无回测功能**：策略评估需手动完成

**需要认证的操作**：
- 下单
- 查看账户余额
- 查看未成交订单
- 访问交易历史记录

**提示**：建议用户参考Binance的API文档（`references/binance-api.md`）以了解认证流程。

## 错误处理

如果脚本执行失败，请检查：
- 网络连接是否正常
- 确认输入的符号格式正确（例如，使用大写形式，如BTCUSDT）
- 确认用户所在地区是否可以访问Binance API
- 检查脚本路径及Python环境的安装情况
- 检查参数是否输入正确

**常见错误**：
- **HTTP 451**：所在地区被限制访问API（建议使用VPN）
- 输入的符号不存在于Binance平台
- 请求速率达到限制（等待60秒后重试）
- 连接超时（可能是网络问题或API暂时不可用）

**最佳实践**：
- **展示操作过程**：显示用户执行的命令
- **解释结果**：不仅仅是展示数据，还要解释其含义
- **区分交易类型**：针对日内交易和长期投资提供不同建议
- **强调风险**：在给出交易建议前先说明风险管理措施
- **诚实沟通**：如果指标结果矛盾，要如实告知
- **及时更新**：如果市场情况发生变化，及时调整建议
- **避免预测**：仅说明“如果满足条件则……”，而非“一定会发生……”
- **提供多种方案**：提供看涨/看跌的多种可能性

## 技能维护

- **定期测试**：每月运行所有脚本，确保其与Binance API的兼容性。

**更新说明**：
- 如果Binance修改API接口
- 用户提出新的技术指标需求
- 需要额外的风险管理工具
- 根据用户反馈进行功能改进

---

**提醒**：此技能旨在帮助用户做出明智的交易决策，但不能替代用户的判断。始终强调个人责任和风险披露的重要性。