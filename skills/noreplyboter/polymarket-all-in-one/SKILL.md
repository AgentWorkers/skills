---
name: Better Polymarket
description: 查询 Polymarket 预测市场：查看赔率、热门市场、搜索事件、跟踪价格，并按交易量列出市场。
homepage: https://polymarket.com
metadata: {"clawdbot":{"emoji":"📊"}}
---

# 更强大的 Polymarket

Polymarket 提供了丰富的预测市场功能：您可以查询市场赔率、查找热门市场、搜索特定事件，或者通过市场标识符（slug）获取详细信息，还可以按交易量列出活跃市场（该功能与 PolyEdge 中的 Gamma API 相一致）。

## 命令

```bash
# Trending/active events (by 24h volume)
python3 {baseDir}/scripts/polymarket.py trending

# Search markets
python3 {baseDir}/scripts/polymarket.py search "trump"
python3 {baseDir}/scripts/polymarket.py search "bitcoin"

# Get specific event by slug (event = group of markets)
python3 {baseDir}/scripts/polymarket.py event "fed-decision-in-october"

# Get single market by slug (one binary market; polymarket.com/market/xxx)
python3 {baseDir}/scripts/polymarket.py market "will-trump-win-2024"

# List active markets (by volume; like PolyEdge FetchMarkets)
python3 {baseDir}/scripts/polymarket.py markets
python3 {baseDir}/scripts/polymarket.py markets --closed   # include closed markets
python3 {baseDir}/scripts/polymarket.py markets --order volumeNum --limit 10

# Get markets by category
python3 {baseDir}/scripts/polymarket.py category politics
python3 {baseDir}/scripts/polymarket.py category crypto
python3 {baseDir}/scripts/polymarket.py category sports
```

## 示例对话：

- “特朗普在 2028 年获胜的概率是多少？”
- “Polymarket 上目前有哪些热门市场？”
- “在 Polymarket 中搜索‘比特币’的相关信息。”
- “美联储利率决议的赔率是多少？”
- “有哪些值得关注的加密货币市场？”
- “显示与‘特朗普在 2024 年获胜’相关的市场信息。”
- “按交易量列出 Polymarket 上最活跃的市场。”

## 输出结果：

- **事件**：事件标题、总交易量、标记为“是”（Yes）的市场列表以及事件链接。
- **市场**：问题内容、标记为“是”/“否”（Yes/No）的答案、交易量、结束日期（如有的话）、结果来源以及市场链接。
- **markets** 命令：返回单个市场的详细信息，结果按交易量排序（或根据指定顺序排列）。

## API

Polymarket 使用公开的 Gamma API 进行数据查询（无需身份验证），其接口与 PolyEdge 完全兼容：
- 基本 URL：`https://gamma-api.polymarket.com`
- 端点：`/events`、`/events/slug/:slug`、`/markets`、`/markets/slug/:slug`、`/search`
- 参数：`limit`、`offset`、`order`、`ascending`、`closed`、`active`
- 文档：https://docs.polymarket.com

## 注意：

目前这些功能仅支持数据读取，进行交易操作需要使用钱包进行身份验证（该功能尚未实现）。