---
name: gate-news-listing
version: "2026.3.13-1"
updated: "2026-03-13"
description: "**交易所挂牌追踪功能**  
当用户询问关于交易所的挂牌、摘牌或维护公告时，请使用此功能。相关触发语句包括：  
- “最近有哪些新币种被挂牌？”  
- “Binance 上新增了哪些币种？”  
- “哪些币种已被摘牌？”  
**使用的 MCP 工具**：  
- `news_feed_get_exchange_announcements`  
- `info_coin_get_coin_info`  
- `info_marketsnapshot_get_market_snapshot`"
---
# gate-news-listing

> 该技能用于查询加密货币的上市/退市/维护公告。用户查询相关信息时，系统会首先调用交易所公告工具，然后为热门加密货币补充基本信息和市场数据。大型语言模型（LLM）会将所有这些信息整合成一份结构化的交易所活动报告。

**触发场景**：用户提及交易所名称并加上“上市/退市”等关键词，或者询问“最近有哪些新币上市”或“有哪些新项目”。

---

## 路由规则

| 用户意图 | 关键词/模式 | 执行操作 |
|-------------|-----------------|--------|
| 查询交易所上市信息 | “Binance 上市了什么币？” “Gate 上最近有什么新币上市？” | 执行该技能的全部工作流程 |
| 查询特定加密货币的上市信息 | “SOL 在哪里上市？” “PEPE 什么时候在 Binance 上市的？” | 执行该技能（按加密货币筛选） |
| 查询退市/维护公告 | “有哪些币即将退市？” “交易所维护公告” | 执行该技能（按公告类型筛选） |
| 新闻简报 | “最近发生了什么？” | 路由到 `gate-news-briefing` |
| 加密货币分析 | “这种新币表现如何？” | 路由到 `gate-info-coinanalysis` |
| 合同安全性检查 | “这种新币安全吗？” | 路由到 `gate-info-riskcheck` |

---

## 执行流程

### 第一步：意图识别与参数提取

从用户输入中提取以下信息：
- `exchange`（可选）：交易所名称（例如 Binance、Gate、OKX、Bybit、Coinbase）
- `coin`（可选）：特定加密货币的符号
- `announcement_type`（可选）：公告类型（上市/退市/维护）
- `limit`：结果数量，默认为 10

**默认逻辑**：
- 如果未指定交易所，则查询所有交易所
- 如果未指定公告类型，则默认查询上市信息
- 如果用户提到“退市”或“维护”，则设置相应的 `announcement_type`

### 第二步：调用交易所公告工具

| 步骤 | 使用的工具 | 参数 | 获取的数据 | 并行处理 |
|------|----------|------------|----------------|----------|
| 1 | `news_feed_get_exchange_announcements` | `exchange={exchange}, coin={coin}, announcement_type={type}, limit={limit}` | 公告列表：交易所、加密货币、公告类型、时间、详细信息 | — |

### 第三步：为热门加密货币补充数据（并行处理）

从第二步的结果中提取最近上市的 3-5 种加密货币，并同时补充以下数据：

| 步骤 | 使用的工具 | 参数 | 获取的数据 | 并行处理 |
|------|----------|------------|----------------|----------|
| 2a | `info_coin_get_coin_info` | `query={coin_symbol}` | 加密货币的基本信息：行业、资金情况、描述 | 是 |
| 2b | `info_marketsnapshot_get_market_snapshot` | `symbol={coin_symbol}, timeframe="1d", source="spot"` | 市场数据：价格、涨跌幅度、市值、成交量 | 是 |

> 仅对上市类型的公告补充市场数据。退市/维护公告不需要市场数据。

### 第四步：利用大型语言模型生成报告

将公告数据和补充信息传递给大型语言模型（LLM），使用以下模板生成交易所活动报告。

---

## 报告模板

```markdown
## Exchange Activity Report

> Data range: {start_time} — {end_time} | Exchange: {exchange / "All"} | Type: {type / "Listings"}

### 1. Latest Listing Announcements

| # | Exchange | Coin | Type | Listing Time | Trading Pairs |
|---|---------|------|------|-------------|---------------|
| 1 | {exchange_1} | {coin_1} | Listed | {time_1} | {pairs_1} |
| 2 | {exchange_2} | {coin_2} | Listed | {time_2} | {pairs_2} |
| ... | ... | ... | ... | ... | ... |

### 2. Featured New Coins

{Quick analysis of the top 3-5 newly listed coins}

#### {coin_1}

| Metric | Value |
|--------|-------|
| Project Description | {description} |
| Sector | {category} |
| Funding Background | {funding} |
| Current Price | ${price} |
| Post-Listing Change | {change}% |
| 24h Volume | ${volume} |
| Market Cap | ${market_cap} |

{LLM one-liner: highlights and risks to watch for this project}

#### {coin_2}
...

### 3. Delisting / Maintenance Notices (if any)

| # | Exchange | Coin | Type | Effective Date | Notes |
|---|---------|------|------|---------------|-------|
| 1 | ... | ... | Delisted | ... | ... |

### 4. Activity Summary

{LLM generates a 2-3 sentence summary based on all announcement data:}
- Most active exchange for new listings recently
- Trending listing sectors (Meme / AI / DePIN / L2, etc.)
- Notable projects and why they stand out
- Delisting/maintenance reminders (if any)

### ⚠️ Risk Warnings

- Newly listed coins experience extreme volatility — the price discovery phase carries very high risk
- Some newly listed tokens may have insufficient liquidity — watch for slippage on large trades
- It is recommended to use the "Risk Assessment" feature to check contract security before trading

> The above information is compiled from public announcements and on-chain data and does not constitute investment advice.
```

---

## 决策逻辑

| 条件 | 评估结果 |
|-----------|------------|
| 新币上市 24 小时内的涨跌幅度超过 100% | 标记为“异常波动——追涨存在极大风险” |
| 新币上市 24 小时内的涨跌幅度低于 -50% | 标记为“上市时处于亏损状态——现在买入需谨慎” |
| 24 小时成交量低于 10 万美元 | 标记为“成交量极低——流动性严重不足” |
| 多个交易所同时上市同一加密货币 | 标记为“多交易所同时上市——市场关注度高” |
| 公告类型为退市 | 标记为“即将退市——请及时处理持仓” |
| 公告类型为维护 | 标记为“正在进行存款/提款维护——暂时无法进行交易” |
| 加密货币的基本信息中缺少资金信息 | 标记为“未找到资金信息——需要进一步核实” |
| 没有找到相关公告 | 通知用户“该时间段内没有相关公告” |
| 补充工具返回空结果或错误 | 跳过对该加密货币的详细分析；标记为“数据不可用” |

---

## 错误处理

| 错误类型 | 处理方式 |
|------------|----------|
| 交易所名称拼写错误 | 尝试模糊匹配，例如：“Binance” → Binance, “OKX” → OKX |
| 未找到匹配的公告 | 通知用户“该交易所/时间段内没有 {type} 类型的公告”。建议扩大时间范围或更换交易所 |
| `news_feed_get_exchange_announcements` 超时 | 返回错误信息；建议稍后再试 |
| 加密货币补充信息（`coin_info`/`market_snapshot`）失败 | 跳过对该加密货币的详细分析；仅显示公告信息 |
| 用户询问加密货币的上市时间（未来事件） | 通知用户“目前只能查询已发布的公告——无法预测未来的上市计划” |
| 结果过多 | 默认显示最新的 10 条；告知用户可以指定交易所或时间范围来缩小结果范围 |

---

## 跨技能路由

| 用户后续操作意图 | 路由目标 |
|-----------------------|----------|
| “帮我分析这种新币” | `gate-info-coinanalysis` |
| “这种新币的合约安全吗？” | `gate-info-riskcheck` |
| “比较这些新上市的加密货币” | `gate-info-coincompare` |
| “这种新币为什么会在这个交易所上市？” | `gate-news-eventexplain` |
| “当前市场整体情况如何？” | `gate-info-marketoverview` |
| “这种新币的链上数据” | `gate-info-tokenonchain` |

---

## 可用的工具及降级说明

| PRD 中定义的工具 | 实际可用的工具 | 状态 | 降级策略 |
|-----------------|----------------------|--------|---------------------|
| `news_feed_get_exchange_announcements` | `news_feed_get_exchange_announcements` | ✅ 可用 | — |
| `info_coin_get_coin_rankings` | — | ❌ 尚未准备好 | 无法按排名列出最近上市的加密货币——需从公告中提取信息并单独查询 |
| `info_coin_get_coin_info` | `info_coin_get_coin_info` | ✅ 可用 | — |
| `info_marketsnapshot_get_market_snapshot` | `info_marketsnapshot_get_market_snapshot` | ✅ 可用 | — |

---

## 安全规则

1. **禁止投资建议**：公告分析基于公开信息，必须包含“本分析不构成投资建议”的免责声明
2. **禁止预测上市情况**：不得预测加密货币是否会在特定交易所上市
3. **新币风险提示**：所有关于新上市加密货币的报告都必须包含“上市初期波动性极大”的风险提示
4. **数据透明度**：标注公告来源和更新时间
5. **标记数据缺失**：当某个维度的数据缺失时，必须明确告知用户——切勿伪造数据
6. **退市提醒**：对于退市公告，必须醒目地提醒用户及时管理持仓