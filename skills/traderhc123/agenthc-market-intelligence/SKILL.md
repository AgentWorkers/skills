---
name: agenthc-market-intelligence
description: 实时股票市场数据与交易智能API，包含47个模块：股票、债券、加密货币、比特币、宏观经济、美联储政策、国债收益率、VIX指数、期权交易动态、行业轮动以及技术分析功能。该API为AI代理提供金融数据支持，并支持比特币闪电网络（Bitcoin Lightning Network）的微支付功能。
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

专为AI代理设计的机构级市场情报API，包含47个模块，涵盖股票、债券、加密货币、宏观经济、美联储政策、流动性、市场趋势检测、阿尔法信号、期权交易等多个领域。支持比特币闪电网络（Lightning Network）微支付功能，由@traderhc开发。

## 设置

### 适用于AI代理（复制粘贴，无需任何额外操作）

```bash
export AGENTHC_API_KEY=$(curl -s -X POST "https://api.traderhc.com/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "MyAgent"}' | jq -r '.api_key')
```

只需一条命令即可使用，完全免费，无需进行任何身份验证或信用卡支付。现在可以查询任意免费模块：

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
- 实时市场概览：标准普尔500指数（S&P 500）、VIX指数、国债收益率、美元指数（DXY）、大宗商品价格、行业表现、市场情绪（Fear & Greed指数）等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 教育内容
- 交易概念、历史案例分析以及市场心理学相关知识。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/educational_content" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 多市场情报
- 美联储/联邦公开市场委员会（Fed/FOMC）预测市场、经济衰退概率、加密货币价格预测等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/polymarket_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 高级模块（每次查询费用100个比特币）

这些高级模块需要订阅高级套餐。您可以使用闪电网络支付（Lightning Network）进行支付，或者每次请求支付402个比特币。

### 技术分析
- 为任意股票代码提供RSI、MACD、布林带（Bollinger Bands）、支撑/阻力位（support/resistance）、成交量分析等功能。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=AAPL" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 债券情报
- 国债收益率、收益率曲线动态、信用利差（credit spreads）、久期风险（duration risk）等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/bond_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 美联储情报
- 美联储资产负债表、FOMC会议日程、ISM制造业指数（ISM PMI）、收益率曲线分析、回购利率（RRP/repo）以及流动性趋势等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/fed_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 宏观经济情报
- 消费者价格指数（CPI）、个人消费支出（PCE）、非农就业数据（NFP）、失业率、M2货币供应量、信用利差（credit spreads）、ISM服务业指数（ISM Services）、消费者情绪等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/macro_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 相关性追踪
- 超过18种跨市场相关性指标，具备异常检测和市场趋势分类功能。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/correlation_tracker" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析
- VIX指数市场趋势分类、期限结构分析、隐含波动率（implied vol）与实际波动率（realized vol）的对比。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_analyzer" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析工具
- VIX指数生态系统（包括VIX、VIX9D、VIX3M、VIX6M等指标）、期限结构分析以及波动性趋势检测。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_surface" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 加密货币情报
- 比特币（Bitcoin）、以太坊（Ethereum）的价格走势、比特币主导地位分析、减半周期预测、加密货币市场情绪（Fear & Greed指数）等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/crypto_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 期权情报
- 来自美国期权清算所（OCC）的公开数据，包括期权未平仓合约量（options open interest）、成交量以及Gamma值。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/options_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### CME FedWatch
- 通过CME FedWatch提供的美联储利率预测数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/cme_fedwatch" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 机构级模块（每次查询费用500个比特币）

### 阿尔法信号
- 综合多因子交易信号：动量（momentum）、均值回归（mean reversion）、价值（value）、波动性（volatility）、市场趋势（flow）等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/alpha_signals" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 市场趋势检测引擎
- 识别12种市场趋势，提供转换概率及历史参考数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/regime_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 尾部风险检测引擎
- 能够检测12种类型的经济危机，提供早期预警信号及综合尾部风险评分。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/tail_risk_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 流动性情报
- 美联储净流动性数据（基于资产负债表和回购利率）、流动性市场趋势、银行压力指标等。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/liquidity_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 机构投资策略分析
- CFTC持仓报告（CFTC COT数据）、投资者情绪指数（AAII）、NAAIM指数、看涨/看跌期权比例以及市场拥挤度分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/institutional_positioning" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 优化后的数据格式（适用于AI代理）

若您使用AI代理，可使用`format=agent`格式，获取包含方向、置信度、紧急程度及变化信息的可操作信号：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.signals'
```

响应内容包括：
- `signals.direction`：牛市/熊市/中性/混合趋势
- `signals.confidence`：0.0至1.0的置信度评分
- `signals.urgency`：低/中/高/紧急程度
- `signals.actionable`：是否建议采取行动
- `suggested_actions`：建议下次查询的模块
- `delta`：自上次查询以来的变化内容

## 紧凑格式（节省Token使用量）

使用`format=compact`格式，可在上下文窗口中节省60%的Token使用量：

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

## 实时事件（通过Webhook接收）

通过HMAC-SHA256签名订阅20多种市场事件：
- 市场趋势变化、VIX指数骤升/骤降
- 相关性异常、信用市场压力骤增
- 阿尔法信号反转、尾部风险警报
- 重大新闻、异常期权交易活动
- 美联储利率预测变化

## 闪电网络支付（L402）

若您选择按请求付费，无需注册：
1. 请求高级接口（无需认证）
2. 收到包含BOLT11闪电网络发票的响应
3. 使用任意闪电网络钱包支付发票金额
4. 重新请求时添加`Authorization: L402 <macaroon>:<preimage>`参数
5. 该发票有效期为24小时，可重复使用

## MCP集成

支持通过Model Context Protocol（streamable-http协议）进行数据传输：

```
Endpoint: https://api.traderhc.com/mcp
Protocol: 2025-03-26
Tools: 28
```

## 所有47个模块一览

| 模块            | 级别            | 描述                                                                                                                         |
|-----------------|-----------------|---------------------------------------------------------------------------------------------------------------------------|
| market_intelligence | 免费            | 实时市场概览、市场趋势、市场情绪分析                                                                                         |
| educational_content | 免费            | 交易概念、历史案例                                                                                                      |
| polymarket_intelligence | 免费            | 多市场预测概率                                                                                                      |
| technical_analysis | 高级            | 为任意股票代码提供技术分析工具（RSI、MACD等）                                                                                   |
| economic_calendar | 高级            | 经济事件、业绩预测                                                                                                      |
| fed_intelligence | 高级            | 美联储资产负债表、FOMC会议信息                                                                                         |
| macro_intelligence | 高级            | 宏观经济指标（CPI、PCE、NFP等）                                                                                         |
| bond_intelligence | 高级            | 国债收益率、收益率曲线                                                                                                   |
| correlation_tracker | 高级            | 跨市场相关性分析                                                                                                   |
| volatility_analyzer | 高级            | VIX指数趋势分析                                                                                                   |
| volatility_surface | 高级            | VIX指数生态系统分析                                                                                                   |
| crypto_intelligence | 高级            | 加密货币价格走势分析                                                                                                   |
| credit_cycle | 高级            | 信用周期分析                                                                                                   |
| sector_rotation | 高级            | 行业周期变化                                                                                                   |
| intermarket_analysis | 高级            | 股票/债券/美元/大宗商品市场分析                                                                                         |
| earnings_calendar | 高级            | 即将发布的财报及市场反应                                                                                         |
| news_sentiment | 高级            | 带有情绪评分的重大新闻                                                                                                 |
| smart_money_tracker | 高级            | “聪明资金”与“愚蠢资金”的对比分析                                                                                         |
| divergence_detection | 高级            | 价格/成交量/波动率差异分析                                                                                         |
| market_structure | 高级            | 市场广度分析                                                                                                   |
| exchange_stats | 高级            | 市场交易量统计                                                                                                   |
| cme_fedwatch | 高级            | 美联储利率预测                                                                                                   |
| options_intelligence | 高级            | 期权未平仓合约量、成交量、Gamma值                                                                                         |
| alpha_signals | 机构级            | 多因子交易信号复合指标                                                                                             |
| regime_engine | 机构级            | 12种市场趋势检测                                                                                                 |
| tail_risk_engine | 机构级            | 经济危机检测及早期预警                                                                                                 |
| liquidity_intelligence | 机构级            | 美联储净流动性分析                                                                                                 |
| hedge_fund_playbooks | 机构级            | 20多种机构投资策略                                                                                                 |
| institutional_positioning | 机构级            | CFTC持仓报告、投资者情绪分析                                                                                         |
| currency_intelligence | 机构级            | 美元指数（DXY）及相关交易策略                                                                                         |
| factor_analysis | 机构级            | 因子轮动及市场拥挤度分析                                                                                         |
| trend_exhaustion_scanner | 机构级            | 趋势衰竭信号                                                                                                   |
| advanced_risk | 机构级            | 风险评估工具（Kelly比率、VaR模型）                                                                                         |
| valuation_intelligence | 机构级            | 企业估值指标（CAPE、Buffett指数）                                                                                         |
| global_flows | 机构级            | 全球资本流动分析                                                                                                 |
| geopolitical_risk | 机构级            | 地缘政治风险评估                                                                                                 |
| central_bank_dashboard | 机构级            | 主要中央银行信息                                                                                                 |
| market_microstructure | 机构级            | 市场微观结构分析                                                                                                 |
| narrative_tracker | 机构级            | 市场舆论动态追踪                                                                                                 |
| wealth_knowledge | 机构级            | 杰出投资者的投资智慧                                                                                                 |
| institutional_content | 机构级            | 精选金融行业内容                                                                                                 |
| market_knowledge | 机构级            | 深度市场知识库                                                                                                 |
| sentiment_engine | 机构级            | 多源市场情绪分析                                                                                                 |
| sec_edgar | 机构级            | 美国证券交易委员会（SEC）内部文件                                                                                         |
| intelligence_service | 机构级            | 人工智能辅助分析服务                                                                                                 |
| historical_parallels | 机构级            | 历史数据对比分析                                                                                                 |
| agent_consensus | 机构级            | 代理用户行为分析                                                                                                 |

## 价格政策

- **免费套餐**：3个模块，每分钟10次查询，每天100次查询
- **高级套餐**：23个模块，每分钟60次查询，每天5,000次查询，每次查询费用100个比特币（约0.10美元）
- **机构级套餐**：所有47个模块，每分钟120次查询，每天50,000次查询，每次查询费用500个比特币（约0.50美元）

支持通过比特币闪电网络支付，即时结算，无需进行任何身份验证。

## 示例使用场景

- **晨间市场简报**：```bash
# Get market overview + bonds + macro + crypto in one batch
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["market_intelligence", "bond_intelligence", "macro_intelligence", "crypto_intelligence"]}' | jq '.results'
```
- **风险评估**：```bash
# Check tail risk + volatility + correlations
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["tail_risk_engine", "volatility_analyzer", "correlation_tracker"]}' | jq '.results'
```
- **股票代码深度分析**：```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=NVDA&format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 免责声明

所有数据和分析内容仅用于教育和信息提供目的，不构成投资建议。请自行进行充分研究。