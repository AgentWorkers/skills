---
name: agenthc-market-intelligence
description: 实时股票市场数据与交易智能API。提供85个智能模块、40种编码化的智能分析工具以及7种定制化的警报服务，涵盖股票、债券、加密货币（包括比特币）、宏观经济、美联储货币政策、国债收益率、VIX指数、期权交易动态、行业轮动趋势、市场格局分析以及技术分析等领域。该API专为金融AI应用设计，支持比特币闪电网络（Lightning Network）下的微支付功能。
homepage: https://api.traderhc.com/docs
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: ["AGENTHC_API_KEY"]
      bins: ["curl", "jq", "python3"]
    primaryEnv: "AGENTHC_API_KEY"
---
# 股市情报服务

专为人工智能代理设计的机构级市场情报API。提供85个情报模块、40项编码智能技能以及7个定制化的警报服务，涵盖股票、债券、加密货币、宏观经济、美联储政策、市场流动性、市场趋势检测、阿尔法信号等多个领域。免费版本包含市场趋势检测功能及相应的转换概率分析。支持通过Webhook和Discord实时发送警报，同时支持比特币Lightning网络进行微支付。该服务由@traderhc开发。

## 设置

### 适用于人工智能代理（无需任何操作）

```bash
export AGENTHC_API_KEY=$(curl -s -X POST "https://api.traderhc.com/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "MyAgent"}' | jq -r '.api_key')
```

只需执行一条命令即可使用全部功能。完全免费，无需进行客户身份验证（KYC）或支付信用卡费用。现在可以查询任何免费模块：

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

## 免费模块（无需付费）

### 市场情报
提供机构级别的实时市场概览及市场趋势检测功能，包括标准普尔500指数（S&P 500）、VIX指数、国债收益率、美元指数（DXY）、大宗商品价格、市场情绪指数（Fear & Greed），以及当前所处的12种市场趋势类型、市场信心评分、未来可能的市场趋势以及转换概率。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '{regime: .data.regime, confidence: .data.regime_confidence, signals: .data.regime_signals, next_likely: .data.regime_next_most_likely, transition_gap: .data.regime_transition_gap, implications: .data.regime_implications, vix: .data.vix, fear_greed: .data.fear_greed_index}'
```

示例响应：
```json
{
  "regime": "goldilocks",
  "confidence": 0.473,
  "signals": ["Tight HY spreads", "ISM at 51.0 - moderate expansion"],
  "next_likely": "recovery",
  "transition_gap": 2.8,
  "implications": ["Reflation (25% probability)", "Melt Up (20% probability)", "Growth Scare (15% probability)"],
  "vix": 19.09,
  "fear_greed": 69
}
```

### 教育内容
涵盖交易理念、历史经验和市场心理学相关知识。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/educational_content" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 多市场情报
提供关于美联储（Fed）/联邦公开市场委员会（FOMC）政策预测的市场数据、经济衰退概率、加密货币价格预测以及政治/监管政策的相关信息。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/polymarket_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### VIX指数趋势情报
基于历史数据对VIX指数进行趋势分类（7个等级：极低 → 危机），并预测未来30天内标准普尔500指数的回报情况，同时提供均值回归概率及市场波动性交易机会分析。数据基于1990年至2024年的CBOE市场数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/vix_regime_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 高级模块（每次查询费用100个比特币）

这些高级模块需要订阅高级版本。您可以使用Lightning网络进行支付，或按每次请求支付L402个比特币。

### 技术分析
提供RSI、MACD、Bollinger Bands等技术指标，以及适用于任何股票代码的技术分析工具。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=AAPL" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 债券情报
提供国债收益率、收益率曲线动态、信用利差及债券期限风险等相关数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/bond_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 美联储情报
包含美联储的资产负债表、FOMC会议日程、ISM采购经理人指数（ISM PMI）数据、收益率曲线分析以及回购市场（RRP/repo）的流动性趋势。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/fed_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 宏观经济情报
提供CPI、PCE指数、非农就业数据（NFP）、失业率、M2货币供应量、信用利差以及消费者情绪等相关宏观经济指标。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/macro_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 相关性追踪
提供18个以上市场之间的相关性数据，并能检测异常现象及市场趋势变化。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/correlation_tracker" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析
提供VIX指数趋势分类、期限结构分析、VVIX指数（VIX的衍生指标）以及隐含波动性与实际波动性的对比分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_analyzer" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析工具
提供VIX指数生态系统的相关数据，包括VIX、VIX9D、VIX3M、VIX6M等指标的期限结构及偏度分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_surface" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 加密货币情报
提供比特币、以太坊等加密货币的相关信息，包括比特币的市场主导地位、减半周期预测以及市场情绪指数（Fear & Greed）。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/crypto_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 期权情报
提供期权未平仓量（Options Open Interest）、期权交易量以及来自OCC公共数据的Gamma值（次日数据）。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/options_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### CME FedWatch
提供基于CME FedWatch的数据，预测美联储的利率变化概率。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/cme_fedwatch" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 机构级模块（每次查询费用500个比特币）

### 阿尔法信号
提供系统化的多因子信号组合，包括动量、均值回归、价值、波动性、市场趋势等多维度信号。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/alpha_signals" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 市场趋势检测引擎
提供12种市场趋势类型及其转换概率，以及相关的领先指标和历史参考数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/regime_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 尾部风险检测引擎
提供危机检测功能，包括12种危机类型、早期预警指标及综合尾部风险评分。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/tail_risk_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 流动性情报
提供美联储的净流动性数据（资产负债表）、流动性趋势以及银行压力信号。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/liquidity_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 信用周期分析
提供高收益债券（HY）、投资级债券（IG）、 BBB级债券（BBB）、CCC级债券（CCC）的信用利差、贷款标准、违约指标以及信用周期阶段等相关信息。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/credit_cycle" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 机构投资策略分析
提供CFTC的COT数据、投资者情绪指数（AAII）数据、NAAIM指数数据以及买入/卖出比率等机构投资策略相关指标。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/institutional_positioning" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 优化后的数据格式

对于人工智能代理，使用`format=agent`格式可获取包含方向、信心程度、紧急程度及变化量的可操作信号：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.signals'
```

响应内容包括：
- `signals.direction`：牛市/熊市/中性/混合趋势
- `signals.confidence`：0.0至1.0的信心评分
- `signals.urgency`：低/中/高/极端紧急程度
- `signals.actionable`：是否建议采取行动
- `suggested_actions`：建议下一步查询的模块
- `delta`：自上次查询以来的变化情况

## 紧凑格式（节省Token使用）

使用`format=compact`格式可减少上下文窗口中的Token使用量（节省约60%）：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=compact" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 批量查询（高级版本）

支持在一次请求中查询多个模块：

```bash
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["market_intelligence", "bond_intelligence", "fed_intelligence"]}' | jq '.'
```

## 警报服务

提供定制化的警报产品，通过Webhook（适用于人工智能代理）或Discord（适用于人类交易者）实时推送市场情报。每个警报包含信号数据、市场趋势背景、投资策略影响、受影响的股票代码以及下一步需要关注的市场指标。所有7个警报服务均处于实时运行状态，每120秒自动更新一次。

### 可用警报服务列表

```bash
curl -s "https://api.traderhc.com/api/v1/alert-packages" | jq '.packages'
```

### 订阅警报服务

```bash
# Webhook delivery (for AI agents)
curl -s -X POST "https://api.traderhc.com/api/v1/alert-packages/regime_shift/subscribe" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"delivery_channels": ["webhook"], "callback_url": "https://mybot.example.com/alerts"}' | jq '.'

# Discord delivery (for human traders)
curl -s -X POST "https://api.traderhc.com/api/v1/alert-packages/volatility/subscribe" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"delivery_channels": ["discord"], "discord_webhook_url": "https://discord.com/api/webhooks/..."}' | jq '.'
```

### 可用警报服务列表

| 服务名称 | 服务等级 | 价格 | 触发条件 |
|---------|------|-------|-------------|
| **市场趋势变化警报** | 高级 | 每月25,000个比特币 | 市场趋势转换（12种状态） |
| **尾部风险警报** | 机构级 | 每月100,000个比特币 | 危机检测（0-100分，12种危机类型） |
| **波动性警报** | 高级 | 每月25,000个比特币 | VIX指数飙升、市场趋势变化、期限结构变化 |
| **信用周期警报** | 高级 | 每月25,000个比特币 | 信用利差激增、周期阶段变化、市场压力 |
| **流动性警报** | 机构级 | 每月100,000个比特币 | 美联储净流动性变化 |
| **跨市场警报** | 高级 | 每月25,000个比特币 | 相关市场相关性突破、阿尔法信号反转 |
| **聪明资金与愚蠢资金对比警报** | 机构级 | 每月100,000个比特币 | “聪明资金”与“愚蠢资金”的投资策略差异 |

### 警报推送方式

所有警报均包含以下详细信息：
- **信号数据**：原始触发值（如VIX指数水平、市场趋势名称等）
- **市场趋势背景**：当前市场趋势的详细解释
- **投资策略建议**：3-4条可操作的投资建议
- **受影响股票代码**：相关股票代码（如$SPY、$VIX、$TLT等）
- **下一步关注点**：需要密切关注的关键市场指标和事件
- **相关信号**：来自编码智能技能的深度分析

推送渠道：
- **Webhook**：通过HMAC-SHA256签名的JSON格式数据发送到您的回调URL
- **Discord**：带有颜色编码的实时警报信息（红色/橙色/黄色/蓝色）
- **SSE**：服务器推送的事件流

### Discord频道

加入**#agenthc-market-alerts**频道，观看实时警报演示。

## 实时事件（通过Webhook接收）

通过HMAC-SHA256签名订阅20多种市场事件：
- 市场趋势变化、VIX指数飙升、市场暴跌
- 相关性突破、信用市场压力加剧
- 阿尔法信号反转、尾部风险警报
- 重要新闻、异常期权交易活动
- 美联储利率变化概率

## Lightning网络支付（L402）

支持无需注册的按请求付费方式：
1. 请求高级版本的服务端点
2. 收到包含BOLT11 Lightning发票的响应
3. 使用任何Lightning钱包支付发票金额
4. 重新请求时添加`Authorization: L402 <macaroon>:<preimage>`参数
5. 令牌有效期为24小时，可重复使用于多次请求

## MCP集成

支持通过Model Context Protocol（streamable-http传输协议）进行数据集成：

```
Endpoint: https://api.traderhc.com/mcp
Protocol: 2025-03-26
Tools: 73
```

## 所有85个模块

### 基础情报模块（45个）

| 模块名称 | 服务等级 | 描述 |
|--------|------|-------------|
| market_intelligence | 免费 | 市场概览、市场趋势检测（12种状态）、信心评分、转换概率、市场情绪指数 |
| educational_content | 免费 | 交易理念、历史经验 |
| polymarket_intelligence | 免费 | 市场预测数据 |
| technical_analysis | 高级 | 适用于任何股票代码的技术分析指标（如RSI、MACD等） |
| economic_calendar | 高级 | 经济事件、业绩预测 |
| fed_intelligence | 高级 | 美联储资产负债表、FOMC会议数据 |
| macro_intelligence | 高级 | 通货膨胀、就业数据、M2货币供应量 |
| bond_intelligence | 高级 | 国债收益率、收益率曲线、信用利差 |
| correlation_tracker | 高级 | 市场相关性异常检测 |
| volatility_analyzer | 高级 | VIX指数趋势、期限结构分析 |
| volatility_surface | 高级 | VIX指数生态系统分析 |
| crypto_intelligence | 高级 | 比特币、以太坊等加密货币的相关信息 |
| credit_cycle | 高级 | 信用周期阶段、信用利差、金融市场状况 |
| sector_rotation | 高级 | 行业周期轮动分析 |
| intermarket_analysis | 高级 | 股票/债券/美元/大宗商品之间的市场相关性 |
| earnings_calendar | 高级 | 即将发布的财报及市场反应 |
| news_sentiment | 高级 | 带有情绪评分的重要新闻 |
| smart_money_tracker | 高级 | “聪明资金”与“愚蠢资金”的投资策略差异 |
| divergence_detection | 高级 | 价格/成交量/市场广度的相关性分析 |
| market_structure | 高级 | 市场广度、市场活跃度分析 |
| cme_fedwatch | 高级 | 美联储利率预测 |
| options_intelligence | 高级 | OCC机构的期权未平仓量、交易量、Gamma值 |
| alpha_signals | 机构级 | 多因子信号组合 |
| regime_engine | 机构级 | 12种市场趋势及其转换概率 |
| tail_risk_engine | 机构级 | 危机检测、早期预警 |
| liquidity_intelligence | 机构级 | 美联储净流动性数据 |
| hedge_fund_playbooks | 机构级 | 20多种机构投资策略 |
| institutional_positioning | 机构级 | CFTC交易数据、投资者情绪指数 |
| currency_intelligence | 机构级 | 美元指数（DXY）及相关金融指标 |
| factor_analysis | 机构级 | 因子轮动、市场拥挤情况 |
| trend_exhaustion_scanner | 机构级 | 市场趋势衰竭信号 |
| advanced_risk | 机构级 | 凯利比率（Kelly Ratio）、VaR风险模型 |
| valuation_intelligence | 机构级 | 市场估值指标（CAPE）、巴菲特估值指标 |
| global_flows | 机构级 | 美元周期、资本流动分析 |
| geopolitical_risk | 机构级 | 地缘政治风险评估 |
| central_bank_dashboard | 机构级 | 主要中央银行的货币政策 |
| market_microstructure | 机构级 | 市场微观结构分析 |
| narrative_tracker | 机构级 | 市场舆论生命周期分析 |
| wealth_knowledge | 机构级 | 杰出投资者的投资智慧 |
| institutional_content | 机构级 | 精选金融行业资讯 |
| market_knowledge | 机构级 | 深度市场知识库 |
| sentiment_engine | 机构级 | 多源市场情绪分析 |
| sec_edgar | 机构级 | 美国证券交易委员会（SEC）的内部文件 |
| intelligence_service | 机构级 | 人工智能合成服务 |
| historical_parallels | 机构级 | 历史数据对比分析 |
| agent_consensus | 机构级 | 代理机构的关注信号 |

### 编码智能技能（40项）

这些技能经过预处理和历史数据校准，能够提供结构化的数据，包括评分、标签、概率、历史参考数据以及未来回报预测（而非原始数据）。

| 技能名称 | 服务等级 | 描述 |
|-------|------|-------------|
| liquidity_fair_value | 机构级 | 美联储净流动性与标准普尔500指数公允价值之间的偏差分析 |
| regime_duration | 机构级 | 当前市场趋势的持续时间与历史平均值的对比 |
| momentum_contagion | 机构级 | 资产间动量溢出效应检测 |
| cross_asset_momentum | 机构级 | 多资产动量综合评分 |
| credit_impulse_sequence | 机构级 | 信用周期阶段及3-6个月的股票市场领先指标 |
| vol_regime_premium | 机构级 | 不同市场趋势下的隐含波动性与实际波动性对比 |
| sector_cycle_position | 机构级 | 基于ISM指数的行业轮动分析 |
| institutional_conviction | 机构级 | 来自COT/AAII/NAAIM的数据分析得出的“聪明资金”投资倾向 |
| tail_risk_phase | 机构级 | 危机生命周期阶段（早期预警） |
| carry_unwind_cascade | 机构级 | 日元套利交易的压力及概率分析 |
| macro_inflection | 机构级 | 经济意外事件指数及趋势变化检测 |
| stress_propagation | 机构级 | 市场压力传播效应分析 |
| valuation_mean_reversion | 机构级 | 市场估值指标及未来回报预测 |
| sentiment_exhaustion | 机构级 | 多源市场情绪疲劳度检测 |
| regime_transition_probability | 机构级 | 12种市场趋势的马尔可夫转换矩阵 |
| signal_confluence_strength | 机构级 | 多因子信号一致性评分（命中率超过82%） |
| signal_flip_velocity | 机构级 | 信号反转的快速检测 |
| opex_gamma_mechanics | 机构级 | 交易成本（OpEx）对市场的影响分析 |
| microstructure_flow_composite | 机构级 | CTA/vol-target/pension/buyback市场的流量分析 |
| central_bank_divergence_index | 机构级 | 全球中央银行的货币政策差异及其影响 |
| narrative_lifecycle_exhaustion | 机构级 | 市场舆论的衰竭情况及反向趋势分析 |
| narrative_conflict_tension | 机构级 | 竞争性舆论的紧张关系及解决概率 |
| factor_crowding_composite | 机构级 | 因子轮动的系统性风险检测 |
| factor_leadership_momentum | 机构级 | 因子轮动的速度及周期对齐分析 |
| crypto_leverage_cycle | 机构级 | 衍生品杠杆率的周期检测 |
| onchain_miner_capitulation | 机构级 | 比特币减半周期的预测 |
| onchain_network_health | 机构级 | 网络活动及采用趋势分析 |
| crypto_halving_cycle_phase | 机构级 | 比特币减半周期的阶段划分 |
| breadth_regimeconfirmation | 机构级 | 价格与市场广度的对比分析 |
| etf_flow_regime_shift | 机构级 | ETF市场流动性的变化检测 |
| risk_drawdown_expectation | 机构级 | 经过凯利比率（Kelly Ratio）调整后的风险预测 |
| bond_yield_regime | 机构级 | 国债收益率与市场趋势的关联分析 |
| geopolitical_risk_premium | 机构级 | 综合地缘政治风险溢价 |
| vix_regime_intelligence | 免费 | VIX指数趋势（7个等级）及未来30天的标准普尔500指数回报预测 |
| yield_curve_stress_signal | 机构级 | 经济衰退概率预测（2秒至10秒周期） |
| commodity_macro_signal | 机构级 | 黄金/石油/铜等大宗商品的宏观市场趋势 |
| dxy_impact_matrix | 机构级 | 美元指数与大宗商品之间的市场影响 |
| cross_asset_momentum_regime | 机构级 | 多资产动量的同步或分化分析 |
| sector_dispersion_signal | 机构级 | 宏观市场趋势与股票市场趋势的对比分析 |
| fear_greed_extreme_signal | 机构级 | 反向市场信号及未来回报预测 |

## 价格政策

- **免费版本**：4个基础模块（包含市场趋势检测及转换概率），每分钟1次更新，每天100次查询，每月费用100个比特币
- **高级版本**：23个模块，每分钟60次更新，每天5,000次查询，每月费用约50美元（50,000个比特币）
- **机构级版本**：所有85个模块（包含40项编码智能技能），每分钟120次更新，每天50,000次查询，每月费用约500美元（500,000个比特币）

支付方式：比特币Lightning网络。支持即时结算，无需进行客户身份验证（KYC）。

## 示例使用场景

### 早晨市场简报

```bash
# Get market overview + bonds + macro + crypto in one batch
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["market_intelligence", "bond_intelligence", "macro_intelligence", "crypto_intelligence"]}' | jq '.results'
```

### 风险评估

```bash
# Check tail risk + volatility + correlations
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["tail_risk_engine", "volatility_analyzer", "correlation_tracker"]}' | jq '.results'
```

### 深度股票分析

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=NVDA&format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 免责声明

所有数据和分析内容仅用于教育和信息交流目的，不构成投资建议。请自行进行充分研究。