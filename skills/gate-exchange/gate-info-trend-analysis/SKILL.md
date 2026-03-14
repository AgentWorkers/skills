---
name: gate-info-trendanalysis
version: "2026.3.12-1"
updated: "2026-03-12"
description: "趋势与技术分析：每当用户请求对某种加密货币进行技术分析或趋势分析时，可使用此功能。相关关键词包括：技术分析（technical analysis）、K线图（K-line）、相对强弱指数（RSI）、移动平均收敛发散指标（MACD）、趋势（trend）、支撑位（support）、阻力位（resistance）。相关工具包括：info_markettrend_get_kline、info_markettrend_getindicator_history、info_markettrend_get_technical_analysis、info_marketsnapshot_get_market_snapshot。"
---
# gate-info-trendanalysis

> 这是一项以技术分析为核心的技能。用户输入一个币种名称及分析需求，系统会同时调用4个工具（K线数据、指标历史记录、多时间框架信号、实时市场快照），随后大型语言模型（LLM）会整合这些数据生成一份多维度的技术分析报告。

**触发场景**：用户明确提及“技术分析”、“K线”、“指标”、“趋势”、“支撑/阻力”等关键词。

---

## 路由规则

| 用户需求 | 关键词 | 执行操作 |
|-------------|----------|--------|
| 技术分析 | “技术分析” “K线” “RSI” “MACD” “Bollinger” “移动平均线” “支撑” “阻力” “趋势” | 执行该技能的全部工作流程 |
| 综合分析（包含基本面） | “帮我分析BTC” | 转向 `gate-info-coinanalysis` |
| 仅查询价格 | “BTC的价格是多少” | 直接调用 `info_marketsnapshot_get_market_snapshot` |
| 仅获取原始K线数据 | “BTC 30天K线” | 直接调用 `info_markettrend_get_kline` — 无需执行完整技能 |

---

## 执行流程

### 第1步：需求识别与参数提取

从用户输入中提取以下信息：
- `symbol`：币种代码（如BTC、ETH、SOL等）
- `timeframe`：分析时间框架（例如，“daily”表示1天，“4-hour”表示4小时；默认为1天）
- `indicators`：用户关注的特定指标（如“RSI”、“MACD”；默认为所有指标）
- `period`：K线的回顾天数（默认为90天）

### 第2步：并行调用4个MCP工具

| 步骤 | MCP工具 | 参数 | 获取的数据 | 是否并行执行 |
|------|----------|------------|----------------|----------|
| 1a | `info_markettrend_get_kline` | `symbol={symbol}, timeframe={timeframe}, limit=90` | K线开盘价（OHLCV数据，默认90根K线） | 是 |
| 1b | `info_markettrend_get_indicator_history` | `symbol={symbol}, indicators=["rsi","macd","bollinger","ma"], timeframe={timeframe}` | 技术指标历史记录 | 是 |
| 1c | `info_markettrend_get_technical_analysis` | `symbol={symbol}` | 多时间框架综合信号（1小时/4小时/1天/1周） | 是 |
| 1d | `info_marketsnapshot_get_market_snapshot` | `symbol={symbol}, timeframe="1d", source="spot"` | 实时市场快照（价格、成交量、持仓量、融资利率） | 是 |

> 这4个工具会同时被调用。

### 第3步：LLM分析

LLM会对原始数据进行分析，完成以下工作：
1. 通过K线形态判断趋势（上升趋势/下降趋势/盘整区间）
2. 结合指标历史记录评估市场状态（超买/超卖/中性）
3. 分析多时间框架信号的一致性或背离情况
4. 确定关键的支撑和阻力水平

### 第4步：输出结构化报告

---

## 报告模板

```markdown
## {symbol} Technical Analysis Report

> Analysis time: {timestamp} | Primary timeframe: {timeframe}

### 1. Current Market Snapshot

| Metric | Value |
|--------|-------|
| Price | ${price} |
| 24h Change | {change_24h}% |
| 24h Volume | ${volume_24h} |
| 24h High | ${high_24h} |
| 24h Low | ${low_24h} |
| Open Interest | ${oi} (if available) |
| Funding Rate | {funding_rate}% (if available) |

### 2. Trend Assessment

**Overall Trend**: {Uptrend / Downtrend / Sideways / Trend Reversal}

{Trend analysis based on candlestick patterns and MA alignment:}
- MA7 / MA25 / MA99 alignment: {Bullish / Bearish / Tangled}
- Recent candlestick patterns: {Bullish Engulfing / Doji / Hammer / etc.} (if notable)
- Volume confirmation: {Rising volume + price up (healthy) / Declining volume + price up (weak momentum) / Rising volume + price down (accelerated selling)}

### 3. Technical Indicator Details

#### RSI (14)
| Timeframe | Value | Status |
|-----------|-------|--------|
| 1h | {rsi_1h} | {Overbought/Oversold/Neutral} |
| 4h | {rsi_4h} | {Overbought/Oversold/Neutral} |
| 1d | {rsi_1d} | {Overbought/Oversold/Neutral} |

{RSI divergence analysis: any bullish/bearish divergence present?}

#### MACD
| Timeframe | DIF | DEA | Histogram | Status |
|-----------|-----|-----|-----------|--------|
| 1h | {dif} | {dea} | {histogram} | {Golden Cross/Death Cross/Above Zero/Below Zero} |
| 4h | ... | ... | ... | ... |
| 1d | ... | ... | ... | ... |

#### Bollinger Bands (20, 2)
| Metric | Value |
|--------|-------|
| Upper Band | ${upper} |
| Middle Band | ${middle} |
| Lower Band | ${lower} |
| Bandwidth | {bandwidth}% |
| Current Position | {price relative to bands + percentile} |

{Narrowing bands → breakout imminent; price touching upper band → potential pullback to middle; touching lower band → potential bounce}

### 4. Key Price Levels

| Type | Price | Basis |
|------|-------|-------|
| Strong Resistance | ${resistance_1} | {Previous high / MA99 / Upper Bollinger / Round number} |
| Weak Resistance | ${resistance_2} | ... |
| Weak Support | ${support_1} | ... |
| Strong Support | ${support_2} | {Previous low / MA99 / Lower Bollinger / Volume profile cluster} |

### 5. Multi-Timeframe Signal Summary

| Timeframe | Composite Signal | Bullish Indicators | Bearish Indicators |
|-----------|-----------------|--------------------|--------------------|
| 1h | {Strong Buy/Buy/Neutral/Sell/Strong Sell} | {count} | {count} |
| 4h | ... | ... | ... |
| 1d | ... | ... | ... |
| 1w | ... | ... | ... |

**Signal Consistency**: {Are multi-timeframe signals aligned? e.g., "Short-term bearish but medium/long-term bullish — divergence present"}

### 6. Overall Technical Assessment

{LLM generates a comprehensive assessment:}
- Current trend strength evaluation
- Short-term (1-3 day) likely direction
- Medium-term (1-2 week) likely direction
- Key observation: a break above ${resistance_1} opens upside; a break below ${support_2} signals trend weakening

### Risk Warnings

{Data-driven risk alerts}

> Technical analysis is based on historical data and cannot predict future price movements. This does not constitute investment advice.
```

---

## 决策逻辑

| 条件 | 分析结果 |
|-----------|------------|
| 多时间框架RSI均大于70 | “多时间框架RSI处于超买状态 — 可能出现大幅回调” |
| 多时间框架RSI均小于30 | “多时间框架RSI处于超卖状态 — 可能出现大幅反弹” |
| 日线MACD金叉 + 4小时MACD金叉 | “MACD多时间框架金叉确认 — 买入信号” |
| 日线MACD死叉 + 4小时MACD死叉 | “MACD多时间框架死叉确认 — 卖出信号” |
| Bollinger带宽小于5% | “Bollinger带宽度极度收窄 — 即将出现突破” |
| 价格突破上轨Bollinger带 | “短期市场过度扩张 — 可能回调至中间带” |
| MA7 > MA25 > MA99 | “多头MA排列” |
| MA7 < MA25 < MA99 | “空头MA排列” |
| 连续3天成交量上升且价格上涨 | “成交量上升表明趋势健康” |
| 成交量下降但价格上升 | “成交量低迷表明趋势可能减弱” |
| 短期信号与中长期信号出现背离 | 标记为“多头/空头背离 — 待进一步确认方向” |
| 融资利率大于0.1% | “期货市场多头拥挤严重 — 存在逼空风险” |
| 任何工具返回空数据或错误 | 跳过该指标的分析；标注“数据不可用” |

---

## 错误处理

| 错误类型 | 处理方式 |
|------------|----------|
| 币种不存在 | 提示用户核实币种名称 |
| `info_markettrend_get_kline` 数据不足 | 减少回顾天数或更换时间框架；标注数据有限 |
| `info_markettrend_get_technical_analysis` 失败 | 从K线和指标历史记录中手动分析信号；标注“综合信号手动生成” |
| `info_markettrend_get_indicator_history` 部分指标缺失 | 显示可用的指标；标注缺失的指标为“暂时不可用” |
| 所有工具均失败 | 返回错误信息；建议用户稍后再试 |

---

## 跨技能路由

| 用户后续需求 | 转向服务 | -----------------------|
| “关于基本面的分析呢？” / “进行全面分析” | `gate-info-coinanalysis` |
| “为什么价格波动如此剧烈？” | `gate-news-eventexplain` |
| “链上芯片分析” | `gate-info-tokenonchain` |
| “比较XX和YY” | `gate-info-coincompare` |
| “最近有什么新闻？” | `gate-news-briefing` |

---

## 安全规则

1. **禁止交易建议**：不提供“建议买入/卖出”或“价格将达到XX”的建议 |
2. **不进行具体价格预测**：不预测“价格明天会升至XX”或“目标价格为XX” |
3. **明确说明局限性**：明确指出技术分析基于历史数据，可能存在误差 |
4. **数据透明度**：标注K线数据范围和指标参数设置 |
5. **标记数据缺失情况**：当指标数据不可用时，必须如实说明 — 绝不伪造数据