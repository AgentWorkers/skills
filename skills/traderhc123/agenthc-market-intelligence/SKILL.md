---
name: agenthc-market-intelligence
description: 实时股票市场数据与交易智能API。提供85个智能模块，涵盖40种编码化的分析工具，适用于股票、债券、加密货币（包括比特币）、宏观经济、美联储政策、国债收益率、VIX指数、期权交易动态、行业轮动趋势、市场趋势识别以及技术分析等领域。该API专为金融AI应用设计，支持比特币闪电网络（Lightning Network）微支付功能。
homepage: https://api.traderhc.com/docs
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: ["AGENTHC_API_KEY"]
      bins: ["curl", "jq", "python3"]
    primaryEnv: "AGENTHC_API_KEY"
---
# 股票市场情报

专为人工智能代理设计的机构级市场情报API。提供85个情报模块（包括40个经过历史校准的编码情报技能），涵盖股票、债券、加密货币、宏观经济、美联储政策、流动性、市场格局检测、阿尔法信号、期权交易流量等多个领域。支持比特币闪电网络微支付功能。由@traderhc开发。

## 设置

### 适用于人工智能代理（复制粘贴，无需任何操作）

```bash
export AGENTHC_API_KEY=$(curl -s -X POST "https://api.traderhc.com/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "MyAgent"}' | jq -r '.api_key')
```

只需一条命令即可使用。完全免费，无需进行客户身份验证（KYC）或使用信用卡。现在可以查询任何免费模块：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 适用于人类用户（交互式设置）

```bash
bash scripts/setup.sh
```

系统会引导您完成注册流程，并生成您的API密钥。

### 非交互式使用（持续集成/脚本）

```bash
export AGENTHC_API_KEY=$(bash scripts/setup.sh --auto)
```

## 免费模块（无需支付）

### 市场情报
- 实时市场快照：标准普尔500指数（S&P 500）、VIX指数、国债收益率、美元指数（DXY）、大宗商品价格、行业表现、市场情绪（Fear & Greed指数）以及市场格局。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 教育内容
- 交易概念、历史案例分析以及市场心理学框架。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/educational_content" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 多市场情报
- 美联储/联邦公开市场委员会（Fed/FOMC）预测市场、经济衰退概率、加密货币价格预测。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/polymarket_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 高级模块（每次查询费用100个闪电网络代币（L402）

这些高级模块需要订阅高级服务。您可以使用闪电网络支付进行升级，或者每次请求支付402个闪电网络代币。

### 技术分析
- 为任意股票代码提供相对强弱指数（RSI）、移动平均线差（MACD）、布林带（Bollinger Bands）、支撑/阻力位以及成交量分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=AAPL" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 债券情报
- 国债收益率、收益率曲线动态、信用利差、久期风险。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/bond_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 美联储情报
- 美联储资产负债表、联邦公开市场委员会会议日程、工业生产指数（ISM PMI）、收益率曲线分析、回购利率（RRP）以及流动性趋势。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/fed_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 宏观经济情报
- 消费者价格指数（CPI）、个人消费支出（PCE）、非农就业数据（NFP）、失业率、广义货币供应量（M2）、信用利差、ISM服务业指数以及消费者情绪。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/macro_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 相关性追踪
- 提供18个以上跨市场的相关性指标，并具备异常检测和市场格局分类功能。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/correlation_tracker" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析
- VIX指数市场格局分类、期限结构分析、隐含波动率与实际波动率对比。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_analyzer" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析工具
- VIX指数生态系统（包括VIX、VIX9D、VIX3M、VIX6M等指标）、期限结构分析以及波动性市场格局检测。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_surface" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 加密货币情报
- 比特币（Bitcoin）、以太坊（Ethereum）的市场状况、比特币主导地位分析、减半周期预测以及加密货币市场情绪（Fear & Greed指数）。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/crypto_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 期权情报
- 来自美国期权清算公司（OCC）的期权未平仓量（open interest）、成交量以及Gamma值数据（T+1）。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/options_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### CME FedWatch
- 通过CME FedWatch代理获取的美联储利率预测概率。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/cme_fedwatch" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 机构级模块（每次查询费用500个闪电网络代币）

### 阿尔法信号
- 综合多因子信号：包括动量（momentum）、均值回归（mean reversion）、价值（value）、波动性（volatility）、市场流量（flow）以及宏观经济因素（macro）等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/alpha_signals" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 市场格局引擎
- 提供12种市场格局及其转换概率、领先指标以及历史对应情况。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/regime_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 尾部风险引擎
- 能够检测12种类型的经济危机，并提供早期预警指标及综合尾部风险评分。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/tail_risk_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 流动性情报
- 美联储净流动性数据（资产负债表 - TGA - 回购利率（RRP）以及流动性市场格局。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/liquidity_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 信用周期分析
- 高收益债券（HY）、投资级债券（IG）、 BBB级债券（BBB）、CCC级债券（CCC）的利差、贷款标准、违约指标以及信用周期阶段。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/credit_cycle" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 机构定位分析
- 美国商品期货交易委员会（CFTC）的持仓报告（COT数据）、投资者情绪指数（AAII）、NAAIM指数、看跌/看涨期权比率以及市场拥挤程度。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/institutional_positioning" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 优化后的代理使用格式

对于人工智能代理，使用`format=agent`格式可获取包含方向、置信度、紧急程度以及变化量的可操作信号：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.signals'
```

响应内容包括：
- `signals.direction` — 坚挺/看跌/中性/混合
- `signals.confidence` — 0.0到1.0之间的置信度值
- `signals.urgency` — 低/中/高/临界紧急程度
- `signals.actionable` — 如果建议采取行动，则设置为true
- `suggested_actions` — 推荐下一步查询的相关模块
- `delta` — 自上次查询以来的变化内容

## 紧凑格式（节省代币）

使用`format=compact`格式可以在上下文窗口中减少60%的代币使用量：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=compact" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 批量查询（高级用户）

支持一次性查询多个模块：

```bash
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["market_intelligence", "bond_intelligence", "fed_intelligence"]}' | jq '.'
```

## 实时事件（通过Webhook）

通过HMAC-SHA256签名订阅20多种市场事件：
- 市场格局变化、VIX指数骤升/骤降
- 相关性破裂、信用市场压力骤增
- 阿尔法信号反转、尾部风险警报
- 重大新闻、异常期权交易活动
- 美联储利率预测概率变化

## 闪电网络支付（L402）

对于无需注册的按请求付费情况：
1. 请求高级服务端点
2. 收到包含BOLT11闪电网络发票的响应
3. 使用任意闪电网络钱包支付发票金额
4. 重新请求时添加`Authorization: L402 <macaroon>:<preimage>`
5. 代币有效期为24小时，可在多次请求中重复使用

## MCP集成

支持通过Model Context Protocol（流式HTTP传输）进行数据集成：

```
Endpoint: https://api.traderhc.com/mcp
Protocol: 2025-03-26
Tools: 73
```

## 所有85个模块

### 基础情报模块（45个）

| 模块 | 级别 | 描述 |
|--------|------|-------------|
| market_intelligence | 免费 | 市场快照、市场格局、市场情绪分析 |
| educational_content | 免费 | 交易概念、历史案例 |
| polymarket_intelligence | 免费 | 预测市场概率 |
| technical_analysis | 高级 | 任意股票代码的技术分析（RSI、MACD等） |
| economic_calendar | 高级 | 经济事件、业绩超预期/未达预期 |
| fed_intelligence | 高级 | 美联储资产负债表、联邦公开市场委员会会议 |
| macro_intelligence | 高级 | 通货膨胀、就业数据、广义货币供应量 |
| bond_intelligence | 高级 | 国债收益率、收益率曲线、信用利差 |
| correlation_tracker | 高级 | 跨市场相关性异常检测 |
| volatility_analyzer | 高级 | VIX指数市场格局、期限结构分析 |
| volatility_surface | 高级 | VIX指数生态系统分析 |
| crypto_intelligence | 高级 | 比特币、以太坊市场状况 |
| credit_cycle | 高级 | 信用周期阶段、利差、金融条件 |
| sector_rotation | 高级 | 行业周期轮动分析 |
| intermarket_analysis | 高级 | 股票/债券/美元/大宗商品市场信号 |
| earnings_calendar | 高级 | 即将发布的财报及市场反应 |
| news_sentiment | 高级 | 带有情绪评分的重大新闻 |
| smart_money_tracker | 高级 | 智能资金与普通资金的对比分析 |
| divergence_detection | 高级 | 价格/成交量/波动率的分歧分析 |
| market_structure | 高级 | 市场广度、相对强弱指数（A/D）、McClellan指标 |
| exchange_stats | 高级 | 市场广度、涨跌趋势 |
| cme_fedwatch | 高级 | 美联储利率预测概率 |
| options_intelligence | 高级 | 美国期权清算公司的期权数据 |
| alpha_signals | 机构级 | 多因子信号综合 |
| regime_engine | 机构级 | 12种市场格局及其转换概率 |
| tail_risk_engine | 机构级 | 经济危机检测与早期预警 |
| liquidity_intelligence | 机构级 | 美联储净流动性数据 |
| hedge_fund_playbooks | 机构级 | 20多种机构投资策略 |
| institutional_positioning | 机构级 | CFTC持仓报告、投资者情绪指数 |
| currency_intelligence | 机构级 | 美元指数（DXY）、套利交易 |
| factor_analysis | 机构级 | 因子轮动、市场拥挤情况 |
| trend_exhaustion_scanner | 机构级 | 趋势衰竭信号检测 |
| advanced_risk | 机构级 | 凯利系数（Kelly）、风险价值（VaR）评估 |
| valuation_intelligence | 机构级 | 市值比率（CAPE）、巴菲特指标（Buffett Indicator） |
| global_flows | 机构级 | 美元周期、资本流动分析 |
| geopolitical_risk | 机构级 | 地缘政治风险评分与对冲策略 |
| central_bank_dashboard | 机构级 | 主要中央银行的实时数据 |
| market_microstructure | 机构级 | 市场微观结构分析 |
| narrative_tracker | 机构级 | 市场舆论生命周期追踪 |
| wealth_knowledge | 机构级 | 杰出投资者的投资智慧 |
| institutional_content | 机构级 | 热门金融推特内容 |
| market_knowledge | 机构级 | 深度市场知识库 |
| sentiment_engine | 机构级 | 多源情绪分析 |
| sec_edgar | 机构级 | 美国证券交易委员会的内部文件 |
| intelligence_service | 机构级 | 人工智能综合服务/查询端点 |
| historical_parallels | 机构级 | 历史类比分析工具 |
| agent_consensus | 机构级 | 代理关注度信号 |

### 编码情报技能（40个）

这些技能经过预处理和历史校准，能够返回包含分数、标签、概率、历史对应情况以及未来回报预期的结构化数据（而非原始数据）。

| 技能 | 级别 | 描述 |
|-------|------|-------------|
| liquidity_fair_value | 机构级 | 美联储净流动性与标准普尔500指数公允价值之间的偏差评分 |
| regime_duration | 机构级 | 当前市场格局的持续时间与历史平均值的对比 |
| momentum_contagion | 机构级 | 跨资产动量溢出效应检测 |
| cross_asset_momentum | 机构级 | 多资产动量综合评分 |
| credit_impulse_sequence | 机构级 | 基于信用周期的阶段划分及3-6个月的股票市场领先信号 |
| vol_regime_premium | 机构级 | 不同市场格局下的隐含波动率与实际波动率对比 |
| sector_cycle_position | 机构级 | 基于ISM指数的行业轮动定位 |
| institutional_conviction | 机构级 | 来自CFTC持仓报告/投资者情绪指数/NAAIM的智能资金信心评分 |
| tail_risk_phase | 机构级 | 经济危机生命周期阶段（早期预警至市场崩溃） |
| carry_unwind_cascade | 机构级 | 日元套利交易压力及其概率 |
| macro_inflection | 机构级 | 经济意外指数及转折点检测 |
| stress_propagation | 机构级 | 跨市场压力传播评分 |
| valuation_mean_reversion | 机构级 | 市值比率/巴菲特指标的未来回报预测 |
| sentiment_exhaustion | 机构级 | 多源情绪衰竭检测 |
| regime_transition_probability | 机构级 | 12种市场格局的马尔可夫转换矩阵 |
| signal_confluence_strength | 机构级 | 多因子信号对齐评分（命中率超过82%） |
| signal_flip_velocity | 机构级 | 信号反转的快速检测 |
| opex_gamma_mechanics | 机构级 | 交易成本对市场的影响及对冲策略 |
| microstructure_flow_composite | 机构级 | 市场流量、目标价格、养老金投资组合的综合评分 |
| central_bank_divergence_index | 机构级 | 全球中央银行政策的差异及其对外汇市场的影响 |
| narrative_lifecycle_exhaustion | 机构级 | 市场舆论的衰竭情况及反向趋势分析 |
| narrative_conflict_tension | 机构级 | 竞争性舆论的紧张程度及解决概率 |
| factor_crowding_composite | 机构级 | 因子轮动的系统性风险检测 |
| factor_leadership_momentum | 机构级 | 因子轮动的速度与周期对齐 |
| crypto_leverage_cycle | 机构级 | 衍生品杠杆周期的检测 |
| onchain_miner_capitulation | 机构级 | 哈希率低迷时的市场信号 |
| onchain_network_health | 机构级 | 网络活动与采用趋势分析 |
| crypto_halving_cycle_phase | 机构级 | 比特币减半周期的阶段划分 |
| breadth_regimeconfirmation | 机构级 | 价格与市场广度的差异及其修正概率 |
| etf_flow_regime_shift | 机构级 | 跨资产ETF流量与市场格局的转换 |
| risk_drawdown_expectation | 机构级 | 经风险调整后的跌幅预测 |
| bond_yield_regime | 机构级 | 国债收益率与股票市场的关联分析 |
| geopolitical_risk_premium | 机构级 | 综合地缘政治风险溢价（以基点计） |
| vix_regime_intelligence | 机构级 | VIX指数市场格局（7个级别）及30天后的标准普尔500指数回报 |
| yield_curve_stress_signal | 机构级 | 经济衰退概率预测（2秒至10秒周期） |
| commodity_macro_signal | 机构级 | 黄金/石油/铜等大宗商品的市场格局 |
| dxy_impact_matrix | 机构级 | 美元指数与大宗商品之间的市场影响 |
| cross_asset_momentum_regime | 机构级 | 跨资产动量的综合评分 |
| sector_dispersion_signal | 机构级 | 宏观因素驱动的市场分类 |
| fear_greed_extreme_signal | 机构级 | 反向趋势信号及未来回报预测 |

## 定价

- **免费**：4个模块，每分钟1次查询，每天100次查询
- **高级**：23个模块，每分钟60次查询，每天5000次查询，每月约50美元（50,000个闪电网络代币）
- **机构级**：所有85个模块（包括40个编码情报技能），每分钟120次查询，每天50,000次查询，每月约500美元（500,000个闪电网络代币）

支付方式：比特币闪电网络。支持即时结算，无需进行客户身份验证（KYC）。

## 示例使用场景

- **晨间市场简报**
- **风险评估**
- **股票代码深度分析**

## 免责声明

所有数据和分析内容仅用于教育和信息提供目的，不构成投资建议。请自行进行独立研究。