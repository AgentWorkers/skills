---
name: gate-exchange-staking
version: "2026.3.12-1"
updated: "2026-03-13"
description: "Gate Exchange的链上质押查询功能：您可以使用此功能来查询质押状态、奖励信息、相关产品以及交易历史记录。相关的查询关键词包括：staking（质押）、stake（质押）、earn（赚取）、staking rewards（质押奖励）、staking positions（质押状态）、earning records（收益记录）、staking history（质押历史）、available coins（可用代币）。"
---
# Gate质押查询套件

## 通用规则

在继续操作之前，请阅读并遵守共享的运行时规则：
→ [exchange-runtime-rules.md](../exchange-runtime-rules.md)

---

本技能专门用于查询Gate Exchange的质押（链上收益）相关操作。它支持以下四个查询模块：**质押位置**、**奖励**、**产品**和**订单历史**。用户的请求会被路由到相应的参考文档和MCP工具。

## 模块概述

| 模块 | 描述 | 触发关键词 |
|--------|-------------|------------------|
| **质押位置** | 查询质押位置、余额、可用余额与锁定余额 | `position`, `balance`, `staked`, `stakingassets`, `holdings`, `redeemable` |
| **奖励** | 查询奖励历史、昨日/每月收益 | `reward`, `earning`, `profit`, `income`, `yesterday earnings`, `monthly earnings` |
| **产品** | 查看可用的质押产品、年化收益率（APY）和最低投入金额 | `products`, `available`, `APY`, `stakeable coins`, `high yield`, `flexible` |
| **订单历史** | 查询质押/赎回订单列表及分页信息 | `history`, `orders`, `transactions`, `staking records`, `redemption records` |

**注意：** 当用户打算执行质押或赎回操作时，请勿调用任何工具。应回复该操作暂时不受支持，并提供查询选项（例如显示质押位置或产品信息）。

**注意：** 当用户打算执行铸币操作时，请勿调用任何工具。应回复该操作暂时不受支持，并提供查询选项。

## 领域知识

### 产品类型

| productType | 标签 | 描述 |
|-------------|-------|-------------|
| 0 | 证书型 | 可即时赎回的灵活质押（redeemPeriod = 0） |
| 1 | 固定期限型 | 具有固定锁定期（redeemPeriod > 0）的质押 |
| 2 | 美国国债型 | 以美国国债为支撑的产品（例如GUSD）。用户质押加密货币并获取基于美国国债利率的收益，通常具有固定或半固定的年化收益率（APY），风险较低。 |

### 可赎回金额计算

质押位置的可赎回金额 **并非** `mortgage_amount − freeze_amount`。正确的计算公式为：

```
redeemable = mortgage_amount × exchangeRate
```

其中 `exchangeRate` 来自 `cex_earn_find_coin`，用于获取相同 `pid` 和匹配货币的汇率。某些产品的 `exchangeRate` 为 1（例如USDT灵活型），而其他产品的 `exchangeRate` 可能不同（例如液态质押代币）。

### 奖励分配

- `reward_delay_days = -1` 表示奖励在赎回时一次性支付，而非定期支付。
- `interest_delay_days` 表示质押后开始累积奖励的延迟时间（通常为1天/T+1）。
- 多币种奖励：一个质押位置可以产生多种货币的奖励（例如，在Compound V3中质押USDT，可以获得USDT和COMP）。

### 数字格式化规则

| 类别 | 精度 | 小数位数 | 示例 |
|----------|-----------|----------------|----------|
| 一般金额（mortgage_amount, freeze_amount, income_total等） | 8位小数 | 保留8位小数 | `1.23` 而不是 `1.23000000`；`100` 而不是 `100.00000000` |
| 利率字段（estimateApr, APY, APR, exchangeRate） | 2位小数 | 保留2位小数 | `5.20%` 而不是 `5.2%`；`8.00%` 而不是 `8%` |

## 路由规则

| 用户意图 | 示例短语 | 路由到 |
|--------|-----------------|----------|
| **质押位置** | “显示我的质押位置”，“查看我的质押资产”，“我可以解冻哪些资产？” | 查阅 `references/staking-assets.md` |
| **奖励** | “质押奖励”，“昨日收益”，“每月收益”，“收益记录” | 查阅 `references/staking-list.md`（第二部分：奖励列表） |
| **产品** | “可用的质押产品”，“可质押的货币”，“最高年化收益率”，“仅限灵活型” | 查阅 `references/staking-coins.md` |
| **订单历史** | “质押历史”，“质押记录”，“显示赎回记录”，“最近的活动” | 查阅 `references/staking-list.md`（第一部分：订单列表） |
| **质押/赎回（不支持）** | “质押1 BTC”，“质押100 USDT”，“赎回我的ETH”，“我想进行质押”，“帮我赎回” | **不要调用任何工具**。回复：此处不支持质押和赎回操作；请使用Gate网站或应用程序。我可以帮助您查询质押位置或产品信息。 |
| **铸币（不支持）** | “铸币”，“我想铸币”，“铸币GT”，“帮我铸币” | **不要调用任何工具**。回复：此处不支持铸币操作；请使用Gate网站或应用程序。我可以帮助您查询质押位置或产品信息。 |
| **意图不明确** | “关于质押的帮助”，“链上收益” | **请澄清**：是查询质押位置、奖励、产品还是订单历史，然后根据情况路由请求。 |

## 执行流程

### 1. 确定用户意图和参数

- 确定用户想要查询的模块（质押位置/奖励/产品/订单历史），或者用户是否打算执行质押/赎回或铸币操作。
- **质押/赎回意图**：如果用户明确表示要执行质押或赎回操作（例如：“质押1 BTC”、“质押100 USDT”、“赎回”、“我想进行质押”），**不要**调用任何MCP工具。回复“该操作暂时不受支持”，并提供查询选项（例如查询质押位置或产品信息），然后结束处理。
- **铸币意图**：如果用户明确表示要执行铸币操作（例如：“铸币”、“我想铸币”、“铸币GT”、“帮我铸币”），**不要**调用任何MCP工具。回复“该操作暂时不受支持”，并提供查询选项（例如查询质押位置或产品信息），然后结束处理。
- 提取参数：`coin`、`pid`、`page`；对于订单列表还需要 `type`（0=质押，1=赎回）。
- **参数缺失**：如果用户仅提到“我的质押”但没有指定具体内容，询问用户需要查询的具体内容，或者默认显示所有质押位置。

### 2. 选择相应的工具

| 模块 | 使用的MCP工具 | 可选参数 |
|--------|----------|-----------------|
| 质押位置 | `cex_earn_asset_list` | `coin`, `pid` |
| 奖励 | `cex_earn_award_list` | `coin`, `pid`, `page` |
| 产品 | `cex_earn_find_coin` | `cointype` |
| 订单历史 | `cex_earn_order_list` | `coin`, `pid`, `type`, `page` |

- **质押位置**：在显示可赎回金额时，调用 `cex_earn_find_coin`（可选参数 `cointype`），查找与每个质押位置相同 `pid` 和匹配货币的产品；使用该产品的 `exchangeRate`（或API中的 `exchangeRateReserve`）进行计算。可赎回金额 = `mortgage_amount × exchangeRate`。不要使用 `mortgage_amount − freeze_amount`。
- 响应结构：
  - **质押位置**：返回一个包含 `pid`, `mortgage_coin`, `mortgage_amount`, `freeze_amount`, `income_total`, `yesterday_income` 等字段的数组。
  - **可赎回金额** **不是** `mortgage_amount − freeze_amount`；正确的计算公式为 `mortgage_amount × exchangeRate`，其中 `exchangeRate` 来自 `cex_earn_find_coin`（相同 `pid` 和匹配货币的汇率）。
- **订单列表**：返回一个包含 `page`, `pageSize`, `totalCount`, `list[]` 的对象。
- **奖励列表**：返回一个包含 `page`, `pageSize`, `totalCount`, `list[]` 的对象，其中 `list` 包含 `pid`, `mortgage_coin`, `reward_coin`, `interest`, `bonus_date` 等字段。
- **产品**：返回一个包含 `pid`, `currency`, `estimateApr`, `minStakeAmount`, `protocolName`, `redeemPeriod`, `productType`, `isDefi`, `currencyRewards`, `exchangeRate` 等字段的数组。

### 3. 格式化响应

- 使用参考文档中指定的 **响应模板** 和字段名称。
- 对于质押位置：显示 `mortgage_amount`, `freeze_amount`, **可赎回金额`（`mortgage_amount × exchangeRate`，其中 `exchangeRate` 来自 `cex_earn_find_coin`），`income_total`, `yesterday_income`；可以按货币分组或按 `pid` 显示。
- 对于奖励：显示包含 `reward_coin`, `interest`, `bonus_date`, `pid`, `mortgage_coin` 的列表；必要时按 `reward_coin` 进行汇总。
- 对于产品：显示 `protocolName`, `currency`, `estimateApr`, `minStakeAmount`, `maxStakeAmount`, `redeemPeriod`, `productType`, `isDefi` 等字段；可以按 `estimateApr` 排序或按 `cointype` 过滤。
- 对于订单历史：显示包含 `coin`, `amount`, `type`（0=质押，1=赎回）的列表；使用 `totalCount`, `page`, `pageCount` 进行分页。

## 报告模板

每次查询后，输出与参考文档一致的标准化结果（例如质押位置摘要、奖励摘要、产品列表或订单列表）。使用API中提供的确切字段名称和值。

## 安全规则

### 只读功能

- 本技能仅用于查询，不执行质押、赎回或铸币操作。
- **质押/赎回意图**：当用户请求执行质押或赎回操作时，回复：“此处不支持质押和赎回操作；请使用Gate网站或应用程序。我可以帮助您查询质押位置或产品信息。” **不要**调用任何工具。可以选择性地显示当前质押位置（`cex_earn_asset_list`）或可用产品（`cex_earn_find_coin`）。
- **铸币意图**：当用户请求执行铸币操作时，回复：“此处不支持铸币操作；请使用Gate网站或应用程序。我可以帮助您查询质押位置或产品信息。” **不要**调用任何工具。可以选择性地显示质押位置或产品信息。

### 错误处理

| 错误情况 | 处理方式 |
|----------|--------|
| 无质押位置（`list` 为空或 `totalCount` 为0） | “您没有任何质押位置。请浏览可用的产品以开始收益。” 并建议用户查阅 `references/staking-coins.md`。 |
| 尚未获得奖励 | “未找到奖励。奖励通常在质押后24小时开始累积。” 可以选择性地显示 `cex_earn_asset_list` 中的质押位置信息。 |
| 产品未找到/无可用容量 | 建议用户根据 `cex_earn_find_coin()`（例如按 `estimateApr`）查找其他产品。 |
| API错误/401 | “无法获取质押数据。请稍后再试。” 或 “请登录以查看质押数据。” |