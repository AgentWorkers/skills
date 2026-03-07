---
name: crypto-market-rank
description: 加密货币市场排名与排行榜：可查询热门代币、搜索量最高的代币、Binance Alpha平台上的代币、被证券化的股票、社交媒体的热度排名、智能资金流入的代币排名、来自Pulse Launchpad的顶级模因代币排名，以及顶尖交易者的盈利排行榜。当用户询问代币排名、市场趋势、社交媒体热度、模因代币排名或顶尖交易者的表现时，可使用此功能。
metadata:
  author: binance-web3-team
  version: "2.0"
---
# 加密市场排名技能

## 概述

以下是提供的一些关键加密市场排名API，用于分析市场趋势和用户行为：

| API | 功能 | 使用场景 |
|-----|----------|----------|
| Social Hype Leaderboard | 社交热度排行榜 | 显示具有高社交关注度和情绪分析的代币 |
| Unified Token Rank | 统一代币排名 | 支持多种类型的代币排名，包括热门趋势代币、搜索量最高的代币等 |
| Smart Money Inflow Rank | 智能资金流入排名 | 显示智能资金买入最多的代币 |
| Meme Rank | 模因代币排名 | 从Pulse平台推出的热门模因代币 |

## 使用场景

1. **社交热度分析**：发现具有最高社交关注度和情绪的代币。
2. **热门代币**：查看当前最热门的代币（`rankType=10`）。
3. **搜索量最高的代币**：查看用户搜索最多的代币（`rankType=11`）。
4. **Binance Alpha精选**：浏览Binance Alpha推荐的代币（`rankType=20`）。
5. **股票代币**：查看被代币化的股票（`rankType=40`）。
6. **智能资金流入**：发现智能资金买入最多的代币。
7. **模因排名**：找到最有可能走红的模因代币。
8. **交易者收益排行榜**：查看表现最佳的交易者及其收益情况。

## 支持的链

| 链 | chainId |
|-------|---------|
| BSC | 56 |
| Base | 8453 |
| Solana | CT_501 |

---

## API 1: Social Hype Leaderboard

### 方法：GET

**URL**：
[此处应插入API的完整URL]

**请求参数**：

| 参数 | 类型 | 是否必填 | 描述 |
| chainId | string | 是 | 链ID |
| sentiment | string | 否 | 过滤条件：`All`、`Positive`、`Negative`、`Neutral` |
| targetLanguage | string | 是 | 翻译目标语言（例如`en`、`zh`） |
| timeRange | number | 是 | 时间范围（`1`表示24小时） |
| socialLanguage | string | 否 | 内容语言（`ALL`表示所有语言） |

**响应头**：`Accept-Encoding: identity`

**示例请求**：
[此处应插入示例请求]

**响应**（`data.leaderBoardList[]`）：

| 字段路径 | 类型 | 描述 |
|------------|------|-------------|
| metaInfo.logo | string | 图标URL路径（前缀为`https://bin.bnbstatic.com`） |
| metaInfo.symbol | string | 代币符号 |
| metaInfo.chainId | string | 链ID |
| metaInfo.contractAddress | string | 合同地址 |
| metaInfo.tokenAge | number | 创建时间戳（毫秒） |
| marketInfo.marketCap | number | 市值（美元） |
| marketInfo.priceChange | number | 价格变化百分比 |
| socialHypeInfo.socialHype | number | 总社交热度指数 |
| socialHypeInfo.sentiment | string | 情绪（正面/负面/中性） |
| socialHypeInfo.socialSummaryBrief | string | 简短的社会摘要 |
| socialHypeInfo.socialSummaryDetail | string | 详细的社会摘要 |
| socialHypeInfo.socialSummaryBriefTranslated | string | 翻译后的简要摘要 |
| socialHypeInfo.socialSummaryDetailTranslated | string | 翻译后的详细摘要 |

---

## API 2: Unified Token Rank

### 方法：POST（推荐）/GET

**URL**：
[此处应插入API的完整URL]

**请求头**：`Content-Type: application/json`, `Accept-Encoding: identity`

**排名类型**：

| rankType | 名称 | 描述 |
|----------|------|-------------|
| 10 | Trending | 热门趋势代币 |
| 11 | Top Search | 搜索量最高的代币 |
| 20 | Alpha | Binance Alpha推荐的代币 |
| 40 | Stock | 被代币化的股票代币 |

**请求体（所有字段均为可选）**：

| 字段 | 类型 | 默认值 | 描述 |
| rankType | integer | 10 | 排名类型：`10`表示热门趋势，`11`表示搜索量最高，`20`表示Binance Alpha推荐的代币，`40`表示股票代币 |
| chainId | string | - | 链ID（例如`1`、`56`、`8453`、`CT_501`） |
| period | integer | 50 | 时间周期（`10`表示1分钟，`20`表示5分钟，`30`表示1小时，`40`表示4小时，`50`表示24小时） |
| sortBy | integer | 0 | 排序字段 |
| orderAsc | boolean | 如果为`true`，则按升序排序 |
| page | integer | 1 | 页码（最小值1） |
| size | integer | 每页显示的数量（最大值200） |

**过滤参数**：

| Filter | 类型 | 描述 |
|--------|------|-------------|
| percentChangeMin/Max | decimal | 价格变化范围（百分比） |
| marketCapMin/Max | decimal | 市值范围（美元） |
| volumeMin/Max | decimal | 成交量范围（美元） |
| liquidityMin/Max | decimal | 流动性范围（美元） |
| holdersMin/Max | long | 持有者数量范围 |
| holdersTop10PercentMin/Max | decimal | 前10大持有者的百分比范围 |
| kycHoldersMin/Max | long | 完成KYC验证的持有者数量（仅限Alpha代币） |
| countMin/Max | long | 交易数量范围 |
| uniqueTraderMin/Max | long | 唯一交易者数量范围 |
| launchTimeMin/Max | long | 代币发布时间范围（毫秒） |

**高级过滤参数**：

| Field | 类型 | 描述 |
|-------|------|-------------|
| keywords | string[] | 包含与这些关键词匹配的代币 |
| excludes | string[] | 排除这些代币 |
| socials | integer[] | 社交媒体来源：`0`表示至少一种，`1`表示Telegram，`2`表示Website |
| alphaTagFilter | string[] | Alpha标签 |
| auditFilter | integer[] | 审计状态：`0`表示未拒绝，`1`表示可冻结，`2`表示可铸造 |
| tagFilter | integer[] | 标签过滤：`0`表示隐藏Alpha信息，`23`表示dex_paid，`29`表示alpha_points等 |

**排序选项**：

| sortBy | 字段 | 描述 |
|--------|-------|
| 0 | 默认排序 |
| 1 | 搜索量 |
| 10 | 发布时间 |
| 20 | 流动性 |
| 30 | 持有者数量 |
| 40 | 市值 |
| 50 | 价格变化 |
| 60 | 交易数量 |
| 70 | 成交量 |
| 80 | 完成KYC验证的持有者数量 |
| 90 | 价格 |
| 100 | 唯一交易者 |

**示例请求**：
[此处应插入示例请求]

**响应**（`data.tokens[]`）：

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| chainId | string | 链ID |
| contractAddress | string | 合同地址 |
| symbol | string | 代币符号 |
| icon | string | 图标URL路径（前缀为`https://bin.bnbstatic.com`） |
| price | string | 当前价格（美元） |
| marketCap | string | 市值 |
| liquidity | string | 流动性 |
| holders | string | 持有者数量 |
| launchTime | string | 发布时间戳（毫秒） |
| decimals | integer | 代币的小数位数 |
| links | string | 社交媒体链接（JSON格式） |
| percentChange{1m,5m,1h,4h,24h} | 各时间段的价格变化百分比 |
| volume{1m,5m,1h,4h,24h} | 各时间段的成交量（美元） |
| volume{1m,5m,1h,4h,24h}Buy/Sell | 各时间段的买卖成交量（美元） |
| count{1m,5m,1h,4h,24h} | 各时间段的交易数量 |
| count{1m,5m,1h,4h,24h}Buy/Sell | 各时间段的买卖交易数量 |
| uniqueTrader{1m,5m,1h,4h,24h} | 各时间段的唯一交易者数量 |
| alphaInfo | object | Alpha信息（标签列表、描述） |
| auditInfo | object | 审计信息（风险等级、风险数量） |
| tokenTag | object | 代币标签信息 |
| kycHolders | string | 完成KYC验证的持有者数量 |
| holdersTop10Percent | string | 前10大持有者的百分比 |

---

## API 3: Smart Money Inflow Rank

### 方法：POST

**URL**：
[此处应插入API的完整URL]

**请求头**：`Content-Type: application/json`, `Accept-Encoding: identity`

**请求体**：

| 字段 | 类型 | 是否必填 | 描述 |
| chainId | string | 是 | 链ID（例如`56`（BSC）或`CT_501`（Solana） |
| period | string | 统计时间窗口（例如`5m`、`1h`、`4h`、`24h`） |
| tagType | integer | 地址标签类型（例如`2`） |

**示例请求**：
[此处应插入示例请求]

**响应**（`data[]`）：

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| tokenName | string | 代币名称 |
| tokenIconUrl | string | 图标URL路径（前缀为`https://bin.bnbstatic.com`） |
| ca | string | 合同地址 |
| price | string | 当前价格（美元） |
| marketCap | string | 市值（美元） |
| volume | string | 该时间段内的交易量（美元） |
| priceChangeRate | string | 价格变化百分比 |
| liquidity | string | 流动性（美元） |
| holders | string | 总持有者数量 |
| kycHolders | string | 完成KYC验证的持有者数量 |
| holdersTop10Percent | string | 前10大持有者的百分比 |
| count | string | 该时间段内的交易数量 |
| countBuy / countSell | string | 买卖交易数量 |
| inflow | number | 智能资金的净流入金额（美元） |
| traders | integer | 交易该代币的智能资金地址数量 |
| launchTime | number | 代币发布时间戳（毫秒） |
| tokenDecimals | integer | 代币的小数位数 |
| tokenRiskLevel | integer | 风险等级（-1=未知，1=低，2=中等，3=高） |
| link | array | 社交媒体链接（格式：`[{label, link}]` |
| tokenTag | object | 代币标签信息 |

---

## API 4: Meme Rank

### 方法：GET

**URL**：
[此处应插入API的完整URL]

**请求参数**：

| 参数 | 类型 | 是否必填 | 描述 |
| chainId | string | 是 | 链ID（例如`56`（BSC） |

**响应**（`data.tokens[]`）：

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| chainId | string | 链ID |
| contractAddress | string | 合同地址 |
| symbol | string | 代币符号 |
| rank | integer | 排名位置 |
| score | string | 算法评分（分数越高，越有可能走红） |
| alphaStatus | integer | Alpha列表状态 |
| price | string | 当前价格（美元） |
| percentChange | string | 价格变化百分比 |
| percentChange7d | string | 7天价格变化百分比 |
| marketCap | string | 市值（美元） |
| liquidity | string | 流动性（美元） |
| volume | string | 总成交量（美元） |
| volumeBnTotal | string | Binance用户的总成交量 |
| volumeBn7d | string | Binance用户7天内的成交量 |
| holders | string | 总持有者数量 |
| kycHolders | string | 完成KYC验证的持有者数量 |
| holdersTop10Percent | string | 前10大持有者的百分比 |
| count | integer | 总交易数量 |
| countBnTotal | integer | Binance用户的总交易数量 |
| countBn7d | integer | Binance用户7天内的交易数量 |
| uniqueTraderBn | integer | Binance用户的唯一交易者数量 |
| uniqueTraderBn7d | integer | Binance用户7天内的唯一交易者数量 |
| impression | integer | 浏览量 |
| createTime | number | 代币创建时间戳（毫秒） |
| migrateTime | number | 迁移时间戳（毫秒） |
| metaInfo'icon | string | 图标URL路径（前缀为`https://bin.bnbstatic.com`） |
| metaInfo.name | string | 代币全名 |
| metaInfo.decimals | integer | 代币的小数位数 |
| metaInfo.aiNarrativeFlag | integer | AI描述标志（1=是） |
| previewLink | object | 社交媒体链接（格式：`[{website[], x[], telegram[]}`） |
| tokenTag | object | 代币标签信息 |

---

## API 5: Address Pnl Rank

### 方法：GET

**URL**：
[此处应插入API的完整URL]

**请求参数**：

| 参数 | 类型 | 是否必填 | 描述 |
| chainId | string | 是 | 链ID（例如`56`（BSC）或`CT_501`（Solana） |
| period | string | 时间周期（例如`7d`、`30d`、`90d`） |
| tag | string | 地址标签过滤条件（例如`ALL`、`KOL`） |
| sortBy | integer | 排序字段 |
| orderBy | integer | 排序方向 |
| pageNo | integer | 页码（最小值1） |
| pageSize | integer | 每页显示的数量（最大值25） |

**过滤参数**：

| Filter | 类型 | 描述 |
| PNLMin/Max | decimal | 实现的利润范围（美元） |
| winRateMin/Max | decimal | 胜率范围（百分比，例如`1`表示1%） |
| txMin/Max | long | 交易数量范围 |
| volumeMin/Max | decimal | 成交量范围（美元） |

**示例请求**：
[此处应插入示例请求]

**响应**（`data.data[]`）：

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| address | string | 地址 |
| addressLogo | string | 地址头像URL |
| addressLabel | string | 地址显示名称 |
| balance | string | 在链上的余额（原生代币，例如SOL/BNB） |
| tags | array | 地址标签（例如KOL） |
| realizedPnl | string | 该时间段内的实现利润（美元） |
| realizedPnlPercent | string | 实现利润百分比 |
| dailyPNL | array | 每日利润列表（格式：`[{realizedPnl, dt}]` |
| winRate | string | 该时间段内的胜率 |
| totalVolume | string | 总交易量（美元） |
| buyVolume / sellVolume | string | 买入/卖出成交量 |
| avgBuyVolume | string | 平均买入金额 |
| totalTxCnt | integer | 总交易数量 |
| buyTxCnt / sellTxCnt | integer | 买入/卖出交易数量 |
| totalTradedTokens | integer | 交易的总代币数量 |
| topEarningTokens | array | 最盈利的代币：`[{tokenAddress, tokenSymbol, tokenUrl, realizedPnl, profitRate}]` |
| tokenDistribution | object | 利润分布：`{gt500Cnt, between0And500Cnt, between0AndNegative50Cnt, ltNegative50Cnt}` |
| lastActivity | number | 最后活动时间戳（毫秒） |
| genericAddressTagList | array | 详细标签信息（标签名称、图标URL、额外信息） |

---

**注意事项**：

1. 图标/Logo的URL需要使用前缀`https://bin.bnbstatic.com`加上路径。
2. `Unified Token Rank`支持GET和POST请求；建议使用POST请求。
3. 响应中的所有数值字段均为字符串格式，使用时需进行解析。
4. 时间周期字段使用缩写形式，例如`{1m,5m,1h,4h,24h`表示`percentChange1m`、`percentChange5m`等单独的字段。