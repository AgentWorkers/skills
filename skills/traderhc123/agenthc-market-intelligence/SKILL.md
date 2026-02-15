---
name: agenthc-market-intelligence
description: 获取用于交易和宏观分析的实时市场情报。可以查询46个模块的数据，包括市场状态检测、波动性分析、国债收益率、加密货币指标、美联储/流动性跟踪、相关性异常、阿尔法信号（alpha signals）、信用周期、机构持仓情况以及行业轮动（sector rotation）。当用户询问有关市场、股票、加密货币、债券、经济、美联储政策、交易信号或金融状况的问题时，可以使用这些数据。
homepage: https://github.com/traderhc123/main
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: ["AGENTHC_API_KEY"]
      bins: ["curl", "jq"]
    primaryEnv: "AGENTHC_API_KEY"
---

# AgentHC 市场情报

这是一个面向 AI 代理的机构级市场情报 API，提供 46 个模块，涵盖股票、债券、加密货币、宏观经济、美联储政策、流动性、市场趋势检测、阿尔法信号等多个领域。由 @traderhc 开发。

## 设置

### 1. 注册（免费，无需进行客户身份验证）

```bash
curl -s -X POST "https://api.traderhc.com/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{"name": "MyOpenClawAgent", "description": "OpenClaw agent using AgentHC intelligence"}' | jq '.'
```

请保存响应中的 `api_key`。

### 2. 设置环境变量

```bash
export AGENTHC_API_KEY=your_api_key_here
```

## 免费模块（无需支付）

### 市场概览
获取市场快照：标准普尔 500 指数、VIX 指数、国债收益率、美元指数（DXY）、大宗商品价格、行业表现以及市场情绪。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 新闻情绪分析
提供带有情绪评分、类别分类和事件提取功能的突发新闻。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/news_sentiment" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 加密货币情报
涵盖比特币、以太坊的价格信息、BTC 的主导地位、减半周期检测以及加密货币市场的情绪分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/crypto_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 经济日历
展示即将发布和已经发布的经济数据（如非农就业数据（NFP）、CPI、美联储利率会议（FOMC）等，并提供数据是否符合预期的检测结果。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/economic_calendar" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 高级模块（每次查询费用 100 萨特）

这些模块需要高级会员资格。可以通过 Lightning Network 支付费用，或者每次请求支付 402 萨特。

### 技术分析
为任意股票代码提供相对强弱指数（RSI）、移动平均线差（MACD）、布林带（Bollinger Bands）等技术分析指标。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=AAPL" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 债券情报
包括国债收益率、收益率曲线动态、信用利差以及久期风险分析。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/bond_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 美联储情报
提供美联储的资产负债表、FOMC 会议日程、ISM 制造业指数（ISM）等数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/fed_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 宏观经济情报
涵盖 CPI、个人消费支出（PCE）、非农就业数据（NFP）、失业率、M2 货币供应量、信用利差以及消费者情绪等指标。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/macro_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 相关性追踪
分析 18 个以上市场之间的相关性，并检测异常情况以及市场趋势。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/correlation_tracker" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 波动性分析
分析 VIX 指数的市场趋势、期限结构（term structure）、隐含波动率（implied vol）与实际波动率（realized vol）。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/volatility_analyzer" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 行业轮动
预测行业周期的轮动趋势、行业领导地位以及资金流向的变化。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/sector_rotation" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### ETF 流动性
分析比特币 ETF（如 IBIT、FBTC、GBTC）和股票 ETF 的资金流动情况。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/etf_flows" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 多市场情报
提供关于美联储政策（FOMC）的预测市场数据、经济衰退的概率以及加密货币价格预测。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/polymarket_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 机构级模块（每次查询费用 500 萨特）

### 阿尔法信号
系统化的多因子信号组合：动量（momentum）、均值回归（mean reversion）、价值（value）、波动性（volatility）等因素。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/alpha_signals" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 市场趋势检测引擎
识别 12 种市场趋势，并提供转换概率、领先指标以及历史参考数据。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/regime_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 尾部风险引擎
检测 12 种类型的危机，并提供早期预警指标和综合尾部风险评分。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/tail_risk_engine" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 流动性情报
分析美联储的净流动性（资产负债表数据）、流动性趋势以及银行压力信号。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/liquidity_intelligence" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 信贷周期
涵盖高收益债券（HY）、中等收益债券（IG）、低收益债券（BBB）、CCC 等的利差、贷款标准、违约指标以及信贷周期的各个阶段。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/credit_cycle" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

### 机构持仓分析
提供 CFTC 的持仓数据（COT data）、投资者情绪指数（AAII sentiment）、NAAIM 指数、看跌/看涨期权比率以及市场拥挤情况。

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/institutional_positioning" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.data'
```

## 为 AI 代理优化的格式

如需获取包含方向、置信度、紧迫性和变化量的可操作信号，请使用 `format=agent` 格式：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.signals'
```

响应内容包括：
- `signals.direction` — 多头/空头/中性/混合
- `signals.confidence` — 0.0 到 1.0
- `signals.urgency` — 低/中/高/紧急
- `signals.actionable` — 如果建议采取行动，则为 `true`
- `suggested_actions` — 下一步应查询的相关模块
- `delta` — 自上次查询以来的变化内容

## 紧凑格式（节省令牌使用）

使用 `format=compact` 可在上下文窗口中节省 60% 的令牌数量：

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/market_intelligence?format=compact" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 批量查询（高级会员）

一次请求可查询多个模块：

```bash
curl -s -X POST "https://api.traderhc.com/api/v1/intelligence/batch" \
  -H "X-API-Key: $AGENTHC_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"modules": ["market_intelligence", "bond_intelligence", "fed_intelligence"]}' | jq '.'
```

## 实时事件（SSE 流式传输）

通过服务器发送的事件实时接收市场动态：

```bash
curl -N "https://api.traderhc.com/api/v1/events/stream?types=market.regime_change,market.vix_spike,market.flash_crash" \
  -H "X-API-Key: $AGENTHC_API_KEY"
```

事件包括：市场趋势变化、VIX 指数飙升、价格暴跌、相关性突破、尾部风险警报以及阿尔法信号的转变。

## Lightning Network 支付（L402）

对于无需注册的按请求付费的情况，该 API 支持 L402 协议。请求高级接口时无需认证，会收到包含 Lightning 发票的响应。支付后可以重试。

## 所有 46 个模块

| 模块 | 级别 | 描述 |
|--------|------|-------------|
| market_intelligence | 免费 | 市场快照、市场趋势、市场情绪分析 |
| news_sentiment | 免费 | 带有情绪评分的突发新闻 |
| crypto_intelligence | 免费 | 比特币、以太坊价格信息及主导地位分析 |
| economic_calendar | 免费 | 经济数据及预测结果 |
| technical_analysis | 高级 | 任意股票代码的技术分析指标 |
| bond_intelligence | 高级 | 国债收益率、收益率曲线分析 |
| fed_intelligence | 高级 | 美联储数据 |
| macro_intelligence | 高级 | 宏观经济指标 |
| correlation_tracker | 高级 | 市场相关性分析 |
| volatility_analyzer | 高级 | 波动性分析 |
| sector_rotation | 高级 | 行业轮动预测 |
| etf_flows | 高级 | ETF 流动性分析 |
| intermarket_analysis | 高级 | 股票/债券/美元/大宗商品市场信号 |
| earnings_calendar | 高级 | 即将发布的财报及市场反应 |
| crypto_derivatives | 高级 | 加密货币衍生品信息 |
| onchain_metrics | 高级 | 区块链指标 |
| finnhub_intelligence | 高级 | 公司财报、内部消息、分析师评级 |
| reddit_sentiment | 高级 | 社交媒体上的投资者情绪 |
| market_structure | 高级 | 市场结构分析 |
| polymarket_intelligence | 高级 | 预测市场概率 |
| alpha_signals | 机构级 | 多因子信号组合 |
| regime_engine | 机构级 | 市场趋势检测 |
| tail_risk_engine | 机构级 | 危机检测与预警 |
| hedge_fund_playbooks | 机构级 | 20 多种机构投资策略 |
| liquidity_intelligence | 机构级 | 流动性分析 |
| credit_cycle | 机构级 | 信贷周期分析 |
| institutional_positioning | 机构级 | 机构持仓数据 |
| smart_money_tracker | 机构级 | 智能资金与普通资金的对比 |
| market_microstructure | 机构级 | 市场微观结构分析 |
| volatility_surface | 机构级 | VIX 指数生态系统分析 |
| currency_intelligence | 机构级 | 美元指数及外汇交易 |
| valuation_intelligence | 机构级 | 估值指标 |
| geopolitical_risk | 机构级 | 地缘政治风险评估 |
| central_bank_dashboard | 机构级 | 主要中央银行信息 |
| factor_analysis | 机构级 | 因子轮动与市场拥挤情况 |
| narrative_tracker | 机构级 | 市场舆论动态 |
| advanced_risk | 机构级 | 风险评估与资金管理策略 |
| global_flows | 机构级 | 美元周期与资本流动 |
| wealth_knowledge | 机构级 | 经验丰富的投资者建议 |
| institutional_content | 机构级 | 专业金融内容 |
| market_knowledge | 机构级 | 深度市场知识库 |
| sentiment_engine | 机构级 | 多源情绪分析 |

## 价格

- **免费**：4 个模块，每天 100 次查询
- **高级**：24 个模块，每天 5,000 次查询，每次查询 100 萨特（约 0.10 美元）
- **机构级**：46 个模块，每天 50,000 次查询，每次查询 500 萨特（约 0.50 美元）

支付方式：比特币 Lightning Network。即时结算，无需进行客户身份验证。

## 示例工作流程

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

### 个股深度分析

```bash
curl -s "https://api.traderhc.com/api/v1/intelligence/technical_analysis?ticker=NVDA&format=agent" \
  -H "X-API-Key: $AGENTHC_API_KEY" | jq '.'
```

## 免责声明

所有数据和分析内容仅用于教育和信息交流目的，不构成投资建议。请自行进行独立研究。