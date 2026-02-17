---
name: agenthc-market-intelligence
description: 实时股票市场数据与交易智能API，包含47个模块：股票、债券、加密货币（包括比特币）、宏观经济、美联储政策、国债收益率、VIX指数、期权交易动态、行业轮动以及技术分析功能。该API为AI代理提供金融数据支持，并支持比特币闪电网络（Bitcoin Lightning Network）的微支付功能。
homepage: https://x.com/traderhc
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: ["AGENTHC_API_KEY"]
      bins: ["curl", "jq"]
    primaryEnv: "AGENTHC_API_KEY"
---
# 股票市场情报

这是一个面向人工智能代理的机构级市场情报API，提供47个模块，涵盖股票、债券、加密货币、宏观经济、美联储政策、市场流动性、市场状态检测、阿尔法信号、期权交易流量等多个领域。同时支持比特币Lightning微支付功能，由@traderhc开发。

## 设置

### 快速启动（一个命令）

```bash
bash scripts/setup.sh
```

注册一个免费的API密钥，并将其保存到您的shell配置文件中。无需进行任何身份验证（KYC）或支付信用卡费用。

### 手动设置

```bash
# 1. Register
curl -s -X POST "https://api.traderhc.com/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "MyAgent", "description": "AI agent using Stock Market Intelligence"}' | jq '.'

# 2. Set your key
export AGENTHC_API_KEY=your_api_key_here
```

## 免费模块（无需支付）

### 市场情报
- 实时市场快照：标准普尔500指数（S&P 500）、VIX指数、国债收益率、美元指数（DXY）、大宗商品价格、行业表现、市场恐慌情绪（Fear & Greed指数）以及市场状态。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 教育内容
- 交易概念、历史经验以及市场心理学框架。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/educational_content" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 多市场情报
- 美联储/联邦公开市场委员会（FOMC）预测市场、经济衰退概率、加密货币价格预测、政治/监管政策变化。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/polymarket_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 高级模块（每条查询费用100个Lightning代币）

这些模块需要高级账户才能使用。您可以使用Lightning微支付进行升级，或者每次查询时支付402个Lightning代币。

### 技术分析
- 为任意股票代码提供RSI、MACD、Bollinger Bands等技术指标，以及成交量分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=AAPL" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 债券情报
- 国债收益率、收益率曲线动态、信用利差、久期风险分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/bond_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 美联储情报
- 美联储资产负债表、FOMC会议日程、ISM采购经理指数（ISM PMI）、收益率曲线分析、回购利率（RRP）以及市场流动性趋势。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/fed_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 宏观经济情报
- 消费者价格指数（CPI）、个人消费支出（PCE）、非农就业数据（NFP）、货币供应量（M2）、信用利差、ISM服务业指数（ISM Services）、消费者情绪指数以及房地产市场状况。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/macro_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 相关性追踪
- 支持18种以上的跨市场相关性分析，并具备异常检测和市场状态分类功能。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/correlation_tracker" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析
- VIX指数市场状态分类、期限结构分析、VVIX指数、隐含波动率与实际波动率的对比。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_analyzer" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析工具
- VIX指数生态系统（包括VIX、VIX9D、VIX3M、VIX6M等指标）、期限结构分析以及波动性市场状态检测。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_surface" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 加密货币情报
- 比特币（Bitcoin）、以太坊（Ethereum）的价格走势、比特币的市场主导地位、减半周期预测以及加密货币市场的恐慌情绪分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/crypto_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 期权情报
- 根据美国期权清算公司（OCC）的公开数据，提供期权的未平仓合约数量（open interest）、成交量以及Gamma值。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/options_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### CME FedWatch
- 通过CME FedWatch代理服务获取美联储利率的预测概率。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/cme_fedwatch" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 机构级模块（每条查询费用500个Lightning代币）

### 阿尔法信号
- 综合多因子信号：包括动量（momentum）、均值回归（mean reversion）、价值（value）、波动性（volatility）、市场流量（flow）以及宏观经济因素。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/alpha_signals" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 市场状态检测引擎
- 识别12种市场状态及其转换概率，提供领先指标和历史参考数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/regime_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 尾部风险引擎
- 能够检测12种类型的危机，提供早期预警信号以及综合尾部风险评分。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/tail_risk_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 流动性情报
- 美联储的净流动性数据（资产负债表 - TGA - RRP）、市场流动性状态以及银行压力信号。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/liquidity_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 信用周期分析
- 高收益债券（HY）、投资级债券（IG）、BBB级债券（BBB）、CCC级债券的信用利差、贷款标准、违约指标以及信用周期阶段。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/credit_cycle" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 机构持仓分析
- 美国商品期货交易委员会（CFTC）的COT数据、投资者情绪指数（AAII）、NAAIM指数、看跌/看涨期权比率以及市场拥挤程度分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/institutional_positioning" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 优化后的数据格式（适用于AI代理）

对于AI代理，使用`format=agent`格式可以获取包含方向、置信度、紧迫性和变化量的可操作信号：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.signals'
```

响应内容包括：
- `signals.direction`：牛市/熊市/中性/混合
- `signals.confidence`：0.0到1.0之间的置信度值
- `signals.urgency`：低/中/高/临界
- `signals.actionable`：如果建议采取行动，则设置为true
- `suggested_actions`：建议下次查询的相关模块
- `delta`：自上次查询以来的变化情况

## 紧凑格式（节省Token使用）

使用`format=compact`格式可以减少上下文窗口中显示的Token数量：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=compact" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 批量查询（高级用户）

一次请求可以查询多个模块：

```bash
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["market_intelligence", "bond_intelligence", "fed_intelligence"]}' | jq '.'
```

## 实时事件（通过Webhook）

通过HMAC-SHA256签名订阅20多种市场事件：

- 市场状态变化、VIX指数骤升/骤降
- 相关性破裂、信用市场压力骤增
- 阿尔法信号反转、尾部风险警报
- 重大新闻、异常期权交易活动
- 美联储利率预测变化

## Lightning支付（L402）

对于无需注册的按请求付费的情况：

1. 请求高级接口（无需认证）
2. 收到包含BOLT11 Lightning发票的响应
3. 使用任何Lightning钱包支付发票金额
4. 重新请求时添加`Authorization: L402 <macaroon>:<preimage>`参数
5. 该Token在24小时内有效，可重复用于多次请求

## MCP集成

通过Model Context Protocol（流式HTTP传输协议）进行集成：

```
Endpoint: https://api.traderhc.com/mcp
Protocol: 2025-03-26
Tools: 28
```

## 所有47个模块

| 模块 | 级别 | 描述 |
|--------|------|-------------|
| market_intelligence | 免费 | 市场快照、市场状态、恐慌情绪指数 |
| educational_content | 免费 | 交易概念、历史经验 |
| polymarket_intelligence | 免费 | 预测市场概率 |
| technical_analysis | 高级 | 任意股票代码的技术分析（RSI、MACD等） |
| economic_calendar | 高级 | 经济事件、业绩表现 |
| fed_intelligence | 高级 | 美联储资产负债表、FOMC会议信息 |
| macro_intelligence | 高级 | 通货膨胀、就业数据、货币供应量 |
| bond_intelligence | 高级 | 国债收益率、收益率曲线、信用利差 |
| correlation_tracker | 高级 | 跨市场相关性异常检测 |
| volatility_analyzer | 高级 | VIX指数市场状态、期限结构分析 |
| volatility_surface | 高级 | VIX指数生态系统、偏度分析 |
| crypto_intelligence | 高级 | 比特币/以太坊价格走势、市场主导地位 |
| credit_cycle | 高级 | 信用周期阶段、信用利差、金融市场状况 |
| sector_rotation | 高级 | 行业周期变化 |
| intermarket_analysis | 高级 | 股票/债券/美元/大宗商品市场信号 |
| earnings_calendar | 高级 | 即将发布的财报及市场反应 |
| news_sentiment | 高级 | 带有情绪评分的重大新闻 |
| smart_money_tracker | 高级 | 智能资金与传统资金的对比分析 |
| divergence_detection | 高级 | 价格/成交量/情绪的背离情况 |
| market_structure | 高级 | 市场广度、市场趋势分析 |
| exchange_stats | 高级 | 市场广度、涨跌幅度 |
| cme_fedwatch | 高级 | 美联储利率预测概率 |
| options_intelligence | 高级 | 期权未平仓合约数量、成交量、Gamma值 |
| alpha_signals | 机构级 | 多因子信号组合 |
| regime_engine | 机构级 | 12种市场状态及其转换概率 |
| tail_risk_engine | 机构级 | 危机检测、早期预警 |
| liquidity_intelligence | 机构级 | 美联储净流动性数据 |
| hedge_fund_playbooks | 机构级 | 20多种机构投资策略 |
| institutional_positioning | 机构级 | CFTC持仓数据、投资者情绪指数 |
| currency_intelligence | 机构级 | 美元指数、套利交易、外汇市场 |
| factor_analysis | 机构级 | 因子轮动、市场拥挤程度 |
| trend_exhaustion_scanner | 机构级 | 趋势衰竭信号 |
| advanced_risk | 机构级 | 凯利系数（Kelly）、VaR风险模型 |
| valuation_intelligence | 机构级 | 市值比率（CAPE）、巴菲特指标 |
| global_flows | 机构级 | 美元周期、资本流动 |
| geopolitical_risk | 机构级 | 地缘政治风险评估 |
| central_bank_dashboard | 机构级 | 主要中央银行的实时数据 |
| market_microstructure | 机构级 | 市场微观结构分析 |
| narrative_tracker | 机构级 | 市场舆论动态 |
| wealth_knowledge | 机构级 | 杰出投资者的投资智慧 |
| institutional_content | 机构级 | 热门金融行业资讯 |
| market_knowledge | 机构级 | 深度市场知识库 |
| sentiment_engine | 机构级 | 多源情绪分析 |
| sec_edgar | 机构级 | 美国证券交易委员会（SEC）内部文件 |
| intelligence_service | 机构级 | 人工智能综合分析服务 |
| historical_parallels | 机构级 | 历史事件对比分析 |
| agent_consensus | 机构级 | 代理行为分析工具 |

## 定价

- **免费**：3个模块，每分钟10次查询，每天100次查询
- **高级**：23个模块，每分钟60次查询，每天5,000次查询，每次查询费用100个Lightning代币（约0.10美元）
- **机构级**：所有47个模块，每分钟120次查询，每天50,000次查询，每次查询费用500个Lightning代币（约0.50美元）

支付方式：通过比特币Lightning网络。支持即时结算，无需进行任何身份验证（KYC）。

## 示例使用流程

- **晨间市场简报**
- **风险评估**
- **股票代码深度分析**

## 免责声明

所有数据和分析内容仅用于教育和信息交流目的，不构成投资建议。请自行进行充分研究。