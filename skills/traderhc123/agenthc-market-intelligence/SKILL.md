---
name: agenthc-market-intelligence
description: 实时股票市场数据与交易智能API。提供85个智能模块、40种编码化的交易策略以及7种定制化的警报服务，涵盖股票、债券、加密货币（包括比特币）、宏观经济、美联储货币政策、国债收益率、VIX指数、期权交易动态、行业轮动趋势、市场环境分析以及技术分析等多个领域。该API专为金融智能应用设计，支持通过比特币闪电网络（Bitcoin Lightning Network）进行微支付。
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

专为AI代理设计的机构级市场情报API。提供85个情报模块、40种编码情报技能以及7种命名警报包，涵盖股票、债券、加密货币、宏观经济、美联储政策、流动性、市场格局检测、阿尔法信号等多个领域。通过Webhook和Discord实时发送警报。支持比特币Lightning微支付。由@traderhc开发。

## 设置

### 适用于AI代理（复制粘贴，无需任何操作）

```bash
export AGENTHC_API_KEY=$(curl -s -X POST "https://api.traderhc.com/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "MyAgent"}' | jq -r '.api_key')
```

只需一条命令即可使用。完全免费，无需进行客户身份验证（KYC），也无需信用卡。现在可以查询任何免费模块：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 适用于人类用户（交互式设置）

```bash
bash scripts/setup.sh
```

会引导您完成注册流程，并生成您的API密钥。

### 非交互式（持续集成/脚本）

```bash
export AGENTHC_API_KEY=$(bash scripts/setup.sh --auto)
```

## 免费模块（无需付费）

### 市场情报
- 实时市场快照：标准普尔500指数（S&P 500）、VIX指数、国债收益率、美元指数（DXY）、大宗商品价格、行业表现、市场恐慌与贪婪情绪（Fear & Greed指数）以及市场格局。

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
- 美联储/联邦公开市场委员会（Fed/FOMC）预测市场、经济衰退概率、加密货币价格预测、政治/监管趋势。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/polymarket_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 高级模块（每次查询费用100个Lightning代币）

这些模块需要高级会员资格。您可以使用Lightning支付进行升级，或者每次请求支付402个Lightning代币。

### 技术分析
- 为任意股票代码提供相对强弱指数（RSI）、移动平均线交叉（MACD）、布林带（Bollinger Bands）、支撑/阻力位以及成交量分析。

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
- 美联储资产负债表、联邦公开市场委员会会议日程、ISM采购经理人指数（ISM PMI）、收益率曲线分析、回购利率（RRP）以及流动性趋势。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/fed_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 宏观经济情报
- 消费者价格指数（CPI）、个人消费支出（PCE）、非农就业数据（NFP）、失业率、货币供应量（M2）、信用利差、ISM服务业指数以及消费者情绪。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/macro_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 相关性追踪
- 超过18种跨市场相关性组合，包含异常检测和市场格局分类功能。

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
- 比特币（Bitcoin）、以太坊（Ethereum）的价格走势、BTC的市场主导地位、减半周期预测以及加密货币市场的恐慌与贪婪情绪。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/crypto_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 期权情报
- 来自美国期权清算所（OCC）的期权未平仓量（open interest）、成交量以及Gamma值数据（T+1）。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/options_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### CME FedWatch
- 通过CME FedWatch代理获取的美联储利率预期。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/cme_fedwatch" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 机构级模块（每次查询费用500个Lightning代币）

### 阿尔法信号
- 系统化的多因子信号组合：包括动量（momentum）、均值回归（mean reversion）、价值（value）、波动性（volatility）、市场趋势（flow）以及宏观经济因素（macro）。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/alpha_signals" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 市场格局引擎
- 识别12种市场格局及其转换概率，提供领先指标和历史参考数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/regime_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 尾部风险引擎
- 能够检测12种类型的经济危机，提供早期预警指标和综合尾部风险评分。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/tail_risk_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 流动性情报
- 美联储的净流动性数据（资产负债表 - TGA - RRP）、流动性市场格局以及银行压力信号。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/liquidity_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 机构定位分析
- 美国商品期货交易委员会（CFTC）的COT数据、投资者情绪指数（AAII）、NAAIM指数、看跌/看涨期权比例以及交易拥挤情况。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/institutional_positioning" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 优化后的代理使用格式

对于AI代理，使用`format=agent`格式可获取包含方向、置信度、紧急程度以及变化信息的可操作信号：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.signals'
```

响应内容包括：
- `signals.direction` — 多头/空头/中性/混合
- `signals.confidence` — 0.0到1.0之间的置信度评分
- `signals.urgency` — 低/中/高/紧急
- `signals.actionable` — 如果建议采取行动，则设置为true
- `suggested_actions` — 下一步应查询的相关模块
- `delta` — 自上次查询以来的变化内容

## 紧凑格式（节省Token使用）

使用`format=compact`格式可减少上下文窗口中的Token数量：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=compact" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 批量查询（高级会员专享）

一次请求可查询多个模块：

```bash
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["market_intelligence", "bond_intelligence", "fed_intelligence"]}' | jq '.'
```

## 警报包（新功能）

提供定制化的警报服务，通过**Webhook**（AI代理）或**Discord**（人类交易者）发送丰富的市场情报。每个警报包含信号数据、市场格局背景、影响指标以及下一步应关注的要点。

### 可用警报包列表

```bash
curl -s "https://api.traderhc.com/api/v1/alert-packages" | jq '.packages'
```

### 订阅警报包

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

### 可用警报包

| 包名 | 会员等级 | 价格 | 触发条件 |
|---------|------|-------|-------------|
| **市场格局变化警报** | 高级会员 | 每月25,000个Lightning代币 | 市场格局转换（12种状态） |
| **尾部风险警报** | 机构级会员 | 每月100,000个Lightning代币 | 经济危机检测（评分0-100，12种危机类型） |
| **波动性警报** | 高级会员 | 每月25,000个Lightning代币 | VIX指数飙升、波动性市场格局变化 |
| **信用周期警报** | 高级会员 | 每月25,000个Lightning代币 | 信用利差激增、周期阶段变化 |
| **流动性市场格局警报** | 机构级会员 | 每月100,000个Lightning代币 | 美联储净流动性变化 |
| **跨市场警报** | 高级会员 | 每月25,000个Lightning代币 | 相关市场相关性破裂、阿尔法信号反转 |
| **聪明资金与愚蠢资金对比警报** | 机构级会员 | 每月100,000个Lightning代币 | 智能资金与愚蠢资金的投资行为差异 |

### 警报发送方式

每个警报都包含以下详细信息：
- **信号数据** — 原始触发值（如VIX指数水平、市场格局名称等）
- **市场格局背景** — 来自市场格局引擎的当前市场状况
- **影响建议** — 3-4条可操作的持仓建议
- **受影响股票** — 相关金融工具（如$SPY、$VIX、$TLT等）
- **下一步关注点** — 需要监控的关键价格水平和事件
- **相关信号** — 来自编码情报技能的洞察

发送渠道：
- **Webhook** — 通过HMAC-SHA256签名的JSON数据发送到您的回调URL
- **Discord** — 带有紧急程度颜色编码的嵌入内容（红色/橙色/黄色/蓝色）
- **SSE** — 服务器推送的实时事件流

### Discord频道

加入**#agenthc-market-alerts**频道，观看实时警报演示。

## 实时事件（通过Webhook）

通过HMAC-SHA256签名订阅20多种市场事件：
- 市场格局变化、VIX指数飙升、市场暴跌
- 相关性破裂、信用市场压力激增
- 阿尔法信号反转、尾部风险警报
- 重大新闻、异常期权交易活动
- 美联储利率预期变化

## Lightning支付（L402）

无需注册即可进行按请求支付的选项：
1. 请求高级会员端点
2. 收到包含BOLT11 Lightning发票的响应
3. 使用任意Lightning钱包支付发票
4. 重新请求时使用`Authorization: L402 <macaroon>:<preimage>`格式
5. 令牌有效期为24小时，可在多次请求中重复使用

## MCP集成

通过Model Context Protocol（streamable-http传输协议）进行集成：

```
Endpoint: https://api.traderhc.com/mcp
Protocol: 2025-03-26
Tools: 73
```

## 所有85个模块

### 基础情报模块（45个）

| 模块 | 会员等级 | 描述 |
|--------|------|-------------|
| market_intelligence | 免费 | 市场快照、市场格局、恐慌与贪婪情绪 |
| educational_content | 免费 | 交易概念、历史案例分析 |
| polymarket_intelligence | 免费 | 预测市场概率 |
| technical_analysis | 高级会员 | 任意股票代码的技术分析（RSI、MACD等） |
| economic_calendar | 高级会员 | 经济事件、业绩表现 |
| fed_intelligence | 高级会员 | 美联储资产负债表、联邦公开市场委员会会议 |
| macro_intelligence | 高级会员 | 通货膨胀、就业数据、货币供应量 |
| bond_intelligence | 高级会员 | 国债收益率、收益率曲线、信用利差 |
| correlation_tracker | 高级会员 | 跨市场相关性异常检测 |
| volatility_analyzer | 高级会员 | VIX指数市场格局、期限结构分析 |
| volatility_surface | 高级会员 | VIX指数生态系统、波动率偏度分析 |
| crypto_intelligence | 高级会员 | 比特币、以太坊价格走势、市场主导地位 |
| credit_cycle | 高级会员 | 信用周期阶段、利差变化、金融状况 |
| sector_rotation | 高级会员 | 行业周期轮动 |
| intermarket_analysis | 高级会员 | 股票/债券/美元/大宗商品市场信号 |
| earnings_calendar | 高级会员 | 即将发布的财报及市场反应 |
| news_sentiment | 高级会员 | 带有情绪评分的重大新闻 |
| smart_money_tracker | 高级会员 | 智能资金与愚蠢资金的投资行为差异 |
| divergence_detection | 高级会员 | 价格/成交量/情绪的背离情况 |
| market_structure | 高级会员 | 市场广度、成交量/涨跌比例 |
| cme_fedwatch | 高级会员 | 美联储利率预期 |
| options_intelligence | 高级会员 | 美国期权清算所的期权未平仓量、成交量、Gamma值 |
| alpha_signals | 机构级会员 | 多因子信号组合 |
| regime_engine | 机构级会员 | 12种市场格局及其转换概率 |
| tail_risk_engine | 机构级会员 | 经济危机检测、早期预警 |
| liquidity_intelligence | 机构级会员 | 美联储净流动性、市场格局 |
| hedge_fund_playbooks | 机构级会员 | 20多种机构投资策略 |
| institutional_positioning | 机构级会员 | CFTC交易数据、投资者情绪指数、看跌/看涨期权比例 |
| currency_intelligence | 机构级会员 | 美元指数、套利交易、外汇市场 |
| factor_analysis | 机构级会员 | 因子轮动、市场拥挤情况 |
| trend_exhaustion_scanner | 机构级会员 | 趋势衰竭信号 |
| advanced_risk | 机构级会员 | 凯利系数（Kelly）、VaR风险模型 |
| valuation_intelligence | 机构级会员 | 市值比率（CAPE）、巴菲特指数 |
| global_flows | 机构级会员 | 美元周期、资本流动 |
| geopolitical_risk | 机构级会员 | 地缘政治风险评分 |
| central_bank_dashboard | 机构级会员 | 主要中央银行的财务状况 |
| market_microstructure | 机构级会员 | 市场微观结构分析 |
| narrative_tracker | 机构级会员 | 市场舆论生命周期 |
| wealth_knowledge | 机构级会员 | 经典投资者智慧分享 |
| institutional_content | 机构级会员 | 热门金融话题内容 |
| market_knowledge | 机构级会员 | 深度市场知识库 |
| sentiment_engine | 机构级会员 | 多源情绪数据 |
| sec_edgar | 机构级会员 | 美国证券交易委员会的内部文件 |
| intelligence_service | 机构级会员 | AI智能分析服务 |
| historical_parallels | 机构级会员 | 历史数据对比分析 |
| agent_consensus | 机构级会员 | 代理关注度信号 |

### 编码情报技能（40种）

这些技能经过预处理和历史校准，能够提供结构化数据，包括评分、标签、概率、历史参考数据以及未来回报预期（而非原始数据）。

| 技能名称 | 会员等级 | 描述 |
|-------|------|-------------|
| liquidity_fair_value | 机构级 | 美联储净流动性与标准普尔500指数公允价值的对比及偏差评分 |
| regime_duration | 机构级 | 当前市场格局的持续时间与历史平均值的对比 |
| momentum_contagion | 机构级 | 跨资产动量溢出效应检测 |
| cross_asset_momentum | 机构级 | 多资产动量综合评分 |
| credit_impulse_sequence | 机构级 | 信用周期阶段及3-6个月的股票市场领先信号 |
| vol_regime_premium | 机构级 | 不同市场格局下的隐含波动率与实际波动率对比 |
| sector_cycle_position | 机构级 | 基于ISM指数的行业轮动定位 |
| institutional_conviction | 机构级 | 来自COT/AAII/NAAIM的智能资金投资信心评分 |
| tail_risk_phase | 机构级 | 经济危机生命周期阶段（早期预警） |
| carry_unwind_cascade | 机构级 | 日元套利交易压力及连锁反应概率 |
| macro_inflection | 机构级 | 经济意外指数及转折点检测 |
| stress_propagation | 机构级 | 跨市场压力传播效应评分 |
| valuation_mean_reversion | 机构级 | 市值比率/巴菲特指数未来回报预测 |
| sentiment_exhaustion | 机构级 | 多源情绪衰竭检测 |
| regime_transition_probability | 机构级 | 12种市场格局的马尔可夫转换矩阵 |
| signal_confluence_strength | 机构级 | 多因子信号一致性评分（命中率超过82%） |
| signal_flip_velocity | 机构级 | 信号反转的快速检测 |
| opex_gamma_mechanics | 机构级 | 交易成本对市场的影响 |
| microstructure_flow_composite | 机构级 | CTA/波动率/养老金/回购交易流量评分 |
| central_bank_divergence_index | 机构级 | 全球中央银行政策的差异及其外汇市场影响 |
| narrative_lifecycle_exhaustion | 机构级 | 市场舆论枯竭及反向趋势评分 |
| narrative_conflict_tension | 机构级 | 竞争性舆论的紧张程度及解决概率 |
| factor_crowding_composite | 机构级 | 因子轮动的系统性风险检测 |
| factor_leadership_momentum | 机构级 | 因子轮动的速度及周期对齐 |
| crypto_leverage_cycle | 机构级 | 衍生品杠杆周期检测 |
| onchain_miner_capitulation | 机构级 | 哈希率困境及底部信号检测 |
| onchain_network_health | 机构级 | 网络活动及采用趋势评分 |
| crypto_halving_cycle_phase | 机构级 | 7阶段减半周期定位 |
| breadth_regimeconfirmation | 机构级 | 价格与市场广度的背离及修正概率 |
| etf_flow_regime_shift | 机构级 | 跨资产ETF流量与市场格局变化 |
| risk_drawdown_expectation | 机构级 | 经风险调整后的下跌幅度预测 |
| bond_yield_regime | 机构级 | 国债收益率与股票市场的关联 |
| geopolitical_risk_premium | 机构级 | 综合地缘政治风险溢价（以基点计） |
| vix_regime_intelligence | 免费 | VIX指数市场格局（7个等级）及30天后的标准普尔500指数回报 |
| yield_curve_stress_signal | 机构级 | 经济衰退概率预测（2秒至10秒周期） |
| commodity_macro_signal | 机构级 | 黄金/石油/铜等大宗商品的宏观市场格局 |
| dxy_impact_matrix | 机构级 | 美元指数与大宗商品之间的影响关系 |
| cross_asset_momentum_regime | 机构级 | 跨资产动量综合评分 |
| sector_dispersion_signal | 机构级 | 宏观市场与股票市场的分化情况 |
| fear_greed_extreme_signal | 机构级 | 反向信号及未来回报预测 |

## 价格体系

- **免费**：4个模块，每分钟1次查询，每天100次
- **高级会员**：23个模块，每分钟60次查询，每天5,000次，每月约50美元（50,000个Lightning代币）
- **机构级**：所有85个模块（包含40种编码情报技能），每分钟120次查询，每天50,000次，每月约500美元（500,000个Lightning代币）

支付方式：比特币Lightning网络。即时结算，无需进行客户身份验证（KYC）。

## 示例使用流程

- **晨间市场简报**
- **风险评估**
- **股票代码深度分析**

## 免责声明

所有数据和分析内容仅用于教育和信息参考目的，不构成投资建议。请自行进行独立研究。