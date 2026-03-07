---
name: meme-rush
description: >
  **Meme Token快速交易助手**  
  具备两大核心功能：  
  1. **Meme Rush**：实时获取来自LaunchPads（如Pump.fun、Four.meme等平台）的Meme Token列表，涵盖新发行、待完成发行以及已迁移阶段的Token信息。  
  2. **Topic Rush**：基于人工智能技术的市场热门话题分析，系统会根据Token的净流入量对相关话题进行排名。  
  当用户询问关于新Meme Token的信息、Meme Token的发行情况、Token的绑定曲线、迁移状态、Pump.fun平台的Token、Four.meme平台的Token、快速Meme交易策略、市场热点话题或当前流行的趋势时，可使用此工具获取所需信息。
metadata:
  author: binance-web3-team
  version: "1.0"
---
# Meme Rush 技能

## 概述

### Meme Rush — 发布平台代币生命周期追踪

| 排名类型 | 阶段 | 描述 |
|----------|-------|-------------|
| 10 | 新创建 | 新生成的代币仍在绑定曲线上 |
| 20 | 完成绑定 | 代币即将迁移（绑定曲线接近完成） |
| 30 | 迁移完成 | 代币已成功迁移到去中心化交易所（DEX） |

### Topic Rush — 基于 AI 的市场热点话题发现

| 排名类型 | 阶段 | 描述 |
|----------|-------|-------------|
| 10 | 最新 | 最新的热点话题 |
| 20 | 上升中 | 流量激增的热门话题（流入量在 1,000 至 20,000 美元之间） |
| 30 | 爆火 | 流量激增的热门话题（流入量超过 20,000 美元） |

## 使用场景

1. **捕捉新发行代币**：在 Pump.fun、Four.meme 等平台查找新生成的代币。
2. **监控迁移过程**：实时关注即将迁移到 DEX 的代币，以便尽早参与交易。
3. **迁移后交易**：寻找刚迁移到 DEX 的代币，进行早期交易。
4. **按开发者行为过滤**：排除开发者的洗售行为，检查开发者卖出比例和销毁的代币数量。
5. **持有者分析**：按持有者比例（前 10%）、开发者持有比例、狙击手持有比例、内部人士持有比例等条件进行筛选。
6. **智能过滤**：结合绑定曲线进度、流动性、交易量、市值等多种因素进行综合过滤。
7. **话题发现**：查找由 AI 生成的热点话题及其相关代币。
8. **基于话题的交易策略**：根据热门话题进行交易，按净流入量排序。

## 支持的链

| 链 | chainId |
|-------|---------|
| BSC | 56 |
| Solana | CT_501 |

## 协议参考

| 协议代码 | 平台 | 链 |
|---------------|----------|-------|
| 1001 | Pump.fun | Solana |
| 1002 | Moonit | Solana |
| 1003 | Pump AMM | Solana |
| 1004 | Launch Lab | Solana |
| 1005 | Raydium V4 | Solana |
| 1006 | Raydium CPMM | Solana |
| 1007 | Raydium CLMM | Solana |
| 1008 | BONK | Solana |
| 1009 | Dynamic BC | Solana |
| 1010 | Moonshot | Solana |
| 1011 | Jup Studio | Solana |
| 1012 | Bags | Solana |
| 1013 | Believer | Solana |
| 1014 | Meteora DAMM V2 | Solana |
| 1015 | Meteora Pools | Solana |
| 1016 | Orca | Solana |
| 2001 | Four.meme | BSC |
| 2002 | Flap | BSC |

---

## API 1: Meme Rush 排名列表

### 方法：POST

**URL**：
```
https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list
```

**请求头**：
`Content-Type: application/json`, `Accept-Encoding: identity`

**请求体**

**必填参数**：
| field | 类型 | 描述 |
|-------|------|-------------|
| chainId | string | 链 ID：BSC 为 `56`，Solana 为 `CT_501` |
| rankType | integer | `10` = 新创建，`20` = 完成绑定，`30` = 迁移完成 |

**分页与关键词**：
| field | 类型 | 描述 |
|-------|------|-------------|
| limit | integer | 每次请求的最大结果数量（默认 40，最大 200） |
| keywords | string[] | 包含与关键词匹配的代币符号（最多 5 个） |
| excludes | string[] | 需要排除的代币符号（最多 5 个） |

**代币过滤条件**：
| field | 类型 | 描述 |
|--------|------|-------------|
| progressMin/Max | string | 绑定曲线进度（0-100%） |
| tokenAgeMin/Max | long | 代币年龄 |
| holdersMin/Max | long | 持有者数量 |
| liquidityMin/Max | string | 流动性（美元） |
| volumeMin/Max | string | 24 小时交易量（美元） |
| marketCapMin/Max | string | 市值（美元） |
| countMin/Max | long | 总交易次数 |
| countBuyMin/Max | long | 买入交易次数 |
| countSellMin/Max | long | 卖出交易次数 |

**持有者分布过滤条件**：
| field | 类型 | 描述 |
|--------|------|-------------|
| holdersTop10PercentMin/Max | string | 前 10% 持有者比例 |
| holdersDevPercentMin/Max | string | 开发者持有者比例 |
| holdersSniperPercentMin/Max | string | 狙击手持有者比例 |
| holdersInsiderPercentMin/Max | string | 内部人士持有者比例 |
| bundlerHoldingPercentMin/Max | string | 聚合器持有者比例 |
| newWalletHoldingPercentMin/Max | string | 新钱包持有者比例 |
| bnHoldingPercentMin/Max | string | Binance 钱包持有者比例 |
| bnHoldersMin/Max | long | Binance 钱包持有者数量 |
| kolHoldersMin/Max | long | KOL 持有者数量 |
| proHoldingMin/Max | long | 专业投资者持有者数量 |

**开发者与发行相关过滤条件**：
| field | 类型 | 描述 |
|-------|------|-------------|
| devMigrateCountMin/Max | long | 开发者的历史迁移次数 |
| devPosition | integer | 开发者的持有情况：`2` = 开发者已售出所有代币 |
| devBurnedToken | integer | 开发者销毁的代币数量：`1` = 是 |
| excludeDevWashTrading | integer | 排除开发者洗售行为：`1` = 是 |
| excludeInsiderWashTrading | integer | 排除内部人士洗售行为：`1` = 是 |

**其他过滤条件**：
| field | 类型 | 描述 |
|-------|------|-------------|
| protocol | integer[] | 发布平台协议代码（参见协议参考） |
| exclusive | integer | 是否为 Binance 独家代币：`0` = 否，`1` = 是 |
| paidOnDexScreener | integer | 是否在 DexScreener 中显示 |
| pumpfunLiving | integer | 是否在 Pump.fun 直播中：`1` = 是 |
| cmcBoost | integer | 是否获得了 CMC 的推广支持：`1` = 是 |
| globalFeeMin/Max | string | 交易手续费（仅限 Solana） |
| pairAnchorAddress | string[] | 相关代币的地址 |

### 示例请求

```bash
curl -X POST 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/pulse/rank/list' \
-H 'Content-Type: application/json' \
-H 'Accept-Encoding: identity' \
-d '{"chainId":"CT_501","rankType":10,"limit":20}'
```

### 响应（`data.tokens[]`）

**核心字段**：
| field | 类型 | 描述 |
|-------|------|-------------|
| chainId | string | 链 ID |
| contractAddress | string | 合同地址 |
| symbol | string | 代币符号 |
| name | string | 代币名称 |
| decimals | integer | 代币小数位数 |
| icon | string | 徽标 URL（前缀为 `https://bin.bnbstatic.com`） |
| price | string | 当前价格（美元） |
| priceChange | string | 24 小时价格变化百分比 |
| marketCap | string | 市值（美元） |
| liquidity | string | 流动性（美元） |
| volume | string | 24 小时交易量（美元） |
| holders | long | 持有者数量 |
| progress | string | 绑定曲线进度（百分比，直接添加 `%`） |
| protocol | integer | 发布平台协议代码 |
| exclusive | integer | 是否为 Binance 独家代币：0/1 |

**交易统计**：
| field | 类型 | 描述 |
|-------|------|-------------|
| count | long | 24 小时总交易次数 |
| countBuy | long | 24 小时买入交易次数 |
| countSell | long | 24 小时卖出交易次数 |

**持有者分布**（所有字段均为百分比形式，直接添加 `%`）：
| field | 描述 |
|-------|-------------|
| holdersTop10Percent | 前 10% 持有者比例 |
| holdersDevPercent | 开发者持有者比例 |
| holdersSniperPercent | 狙击手持有者比例 |
| holdersInsiderPercent | 内部人士持有者比例 |
| bnHoldingPercent | Binance 钱包持有者比例 |
| kolHoldingPercent | KOL 持有者比例 |
| proHoldingPercent | 专业投资者持有者比例 |
| newWalletHoldingPercent | 新钱包持有者比例 |
| bundlerHoldingPercent | 聚合器持有者比例 |

**开发者与迁移信息**：
| field | 类型 | 描述 |
|-------|------|-------------|
| devAddress | string | 开发者钱包地址 |
| devSellPercent | 开发者卖出比例 |
| devMigrateCount | long | 开发者的历史迁移次数 |
| devPosition | integer | 开发者的持有情况：`2` = 开发者已售出所有代币 |
| migrateStatus | integer | `0` = 未迁移，`1` = 已迁移 |
| migrateTime | long | 迁移时间（毫秒） |
| createTime | long | 代币创建时间（毫秒） |

**标签与标志**：
| field | 类型 | 描述 |
|-------|------|-------------|
| tagDevWashTrading | integer | 开发者洗售行为：1 = 是 |
| tagInsiderWashTrading | integer | 内部人士洗售行为：1 = 是 |
| tagDevBurnedToken | integer | 开发者销毁的代币数量：1 = 是 |
| tagPumpfunLiving | integer | 是否在 Pump.fun 直播中：1 = 是 |
| tagCmcBoost | integer | 是否获得了 CMC 的推广支持：1 = 是 |
| paidOnDexScreener | integer | 是否在 DexScreener 中显示：1 = 是 |
| launchTaxEnable | integer | 是否包含发行税：1 = 是 |
| taxRate | string | 交易手续费（百分比） |
| globalFee | string | 交易手续费（仅限 Solana） |

**社交链接**：
| field | 类型 | 描述 |
|-------|------|-------------|
| socials.website | string | 社交媒体网站 URL |
| socials.twitter | string | Twitter URL |
| socialsTelegram | string | Telegram URL |

**AI 生成的热点话题描述**：
| field | 类型 | 描述 |
|-------|------|-------------|
| narrativeText.en | string | AI 生成的热点话题英文描述 |
| narrativeText.cn | string | AI 生成的热点话题中文描述 |

---

## API 2: Topic Rush 排名列表

### 方法：GET

**URL**：
```
https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list
```

**请求头**：
`Accept-Encoding: identity`

**请求参数**：
| field | 类型 | 描述 |
|-------|------|-------------|
| chainId | string | 链 ID：`56` 或 `CT_501` |
| rankType | integer | `10` = 最新，`20` = 上升中，`30` = 爆火 |
| sort | integer | 排序方式：`10` = 创建时间，`20` = 净流入量，`30` = 爆火时间 |

> **排序规则**：用户未指定排序方式时，`sort=10` 表示按创建时间排序（最新/上升中），`sort=30` 表示按爆火时间排序。

**可选参数**：
| field | 类型 | 描述 |
|-------|------|-------------|
| asc | boolean | `true` = 升序，`false` = 降序 |
| keywords | string | 关键词过滤（不区分大小写，包含匹配） |
| topicType | string | 话题类型过滤（多个类型用逗号分隔） |
| tokenSizeMin/Max | integer | 相关代币数量范围 |
| netInflowMin/Max | string | 话题净流入量范围（美元） |

### 示例请求

```bash
curl 'https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/market/token/social-rush/rank/list?chainId=CT_501&rankType=30&sort=30&asc=false' \
-H 'Accept-Encoding: identity'
```

### 响应（`data[]`）

**话题字段**：
| field | 类型 | 描述 |
|-------|------|-------------|
| topicId | string | 话题唯一 ID |
| chainId | string | 链 ID |
| name | object | 多语言话题名称（如 `topicNameEn`、`topicNameCn` 等） |
| type | string | 话题类型/类别 |
| close | integer | 话题是否关闭：`0` = 未关闭，`1` = 已关闭 |
| topicLink | string | 相关推文/帖子链接 |
| createTime | long | 话题创建时间（毫秒） |
| progress | string | 话题进度（百分比形式，直接添加 `%`） |
| aiSummary | object | AI 生成的热点话题描述 |
| topicNetInflow | string | 总净流入量（美元） |
| topicNetInflow1h | string | 1 小时净流入量（美元） |
| topicNetInflowAth | string | 历史最高净流入量（美元） |
| tokenSize | integer | 相关代币数量 |
| deepAnalysisFlag | integer | 是否提供深度分析：`1` = 是 |

**代币列表**（每个话题下包含 `tokenList[]`）：
| field | 类型 | 描述 |
|-------|------|-------------|
| chainId | string | 链 ID |
| contractAddress | string | 合同地址 |
| symbol | string | 代币符号 |
| icon | string | 徽标 URL（前缀为 `https://bin.bnbstatic.com`） |
| decimals | integer | 代币小数位数 |
| createTime | long | 代币创建时间（毫秒） |
| marketCap | string | 市值（美元） |
| liquidity | string | 流动性（美元） |
| priceChange24h | string | 24 小时价格变化百分比（直接添加 `%`） |
| netInflow | string | 话题创建以来的净流入量（美元） |
| netInflow1h | string | 1 小时净流入量（美元） |
| volumeBuy / volumeSell | string | 话题创建以来的买入/卖出量（美元） |
| volume1hBuy / volume1hSell | string | 1 小时内的买入/卖出量（美元） |
| uniqueTrader{5m,1h,4h,24h} | long | 不同时间段的唯一交易者数量 |
| count{5m,1h,4h,24h} | 不同时间段的交易数量 |
| holders | long | 持有者数量 |
| kolHolders | long | KOL 持有者数量 |
| smartMoneyHolders | long | 智能资金持有者数量 |
| protocol | integer | 发布平台协议代码（`0`/null = DEX 代币） |
| internal | integer | 是否在绑定曲线上：`0` = 未在，`1` = 是 |
| migrateStatus | integer | 是否已迁移：`0` = 未迁移，`1` = 已迁移 |

---

## 注意事项

1. 仅需要提供 `chainId` 和 `rankType`；其他参数均为可选的过滤条件。
2. 百分比字段（如进度、持有者比例、开发者卖出比例、税率）已预先格式化为百分比形式，直接添加 `%`。
3. 当协议为 `2001`（Four.meme）时，`taxRate` 仅显示在迁移完成列表中；当协议为 `2002`（Flap）时，该字段会显示在所有列表中。
4. 徽标 URL 需要加上前缀 `https://bin.bnbstatic.com` 和路径。