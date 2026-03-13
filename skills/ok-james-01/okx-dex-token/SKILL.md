---
name: okx-dex-token
description: "此技能适用于以下场景：用户请求“查找代币”、“搜索代币”、“查询PEPE信息”、“了解当前的热门代币”、“查看热门代币”、“获取代币排名”、“了解代币持有者情况”、“分析代币的市场资本化”、“评估代币的流动性”、“深入研究某个代币”或提及与代币相关的操作（如搜索代币、发现热门代币、查看排名、检查持有者分布、分析市场资本化和流动性等）。该技能支持在XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon以及20多个其他区块链平台上进行代币搜索、查询代币元数据、市场资本化、流动性、交易量、热门代币排名以及持有者分析。**请注意：**仅当用户明确指定了具体的代币名称或需要执行具体操作时，才可使用此技能。对于价格图表、K线图、交易数据或交易信号的相关需求，请使用okx-dex-market；而对于与Meme代币的安全性、开发者声誉、代币欺诈行为（如“Rug Pull”）或代币捆绑销售/欺诈行为相关的分析，请同样使用okx-dex-market。"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.2"
  homepage: "https://web3.okx.com"
---
# OKX DEX Token Info CLI

提供了5个命令，用于查询token信息、元数据、详细价格、排名以及持有者分布。

## 预运行检查

在运行任何`onchainos`命令之前，请务必按照以下步骤操作。不要将常规命令的输出显示给用户；仅在安装、更新或处理错误时提供简短的状态更新。

1. **确认已安装**：运行`which onchainos`。如果未找到，请根据以下链接手动安装：[https://github.com/okx/onchainos-skills](https://github.com/okx/onchainos-skills)。
2. **检查更新**：读取`~/.onchainos/last_check`文件，并与当前时间戳进行比较：
   - 如果`cached_ts`非空且`(now - cached_ts) < 43200`（12小时内），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时旧），运行安装程序以检查更新：
     如果安装了新版本，请告知用户，并建议他们从[https://github.com/okx/onchainos-skills](https://github.com/okx/onchainos-skills)更新`onchainos`工具以获取最新功能。
3. 如果在此过程中任何`onchainos`命令因意外错误失败，请尝试重新安装后再继续操作。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可跳过此步骤）。

## 技能路由

- 要获取实时价格、K线图和交易历史记录，请使用`okx-dex-market`。
- 要执行交换操作，请使用`okx-dex-swap`。
- 要广播交易，请使用`okx-onchain-gateway`。
- 要查看钱包余额和投资组合，请使用`okx-wallet-portfolio`。
- 要了解meme token的安全性（开发者声誉、欺诈行为、捆绑器以及同一开发者发布的类似token），请使用`okx-dex-market`。
- 要获取智能资金、大客户或KOL的交易信号，请使用`okx-dex-market`。

## 快速入门

```bash
# Search token
onchainos token search xETH --chains "ethereum,solana"

# Get detailed price info
onchainos token price-info 0xe7b000003a45145decf8a28fc755ad5ec5ea025a --chain xlayer

# What's trending on Solana by volume?
onchainos token trending --chains solana --sort-by 5 --time-frame 4

# Check holder distribution
onchainos token holders 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee --chain xlayer
```

## 支持的链名

该CLI接受人类可读的链名（例如`ethereum`、`solana`、`xlayer`），并自动解析它们。

| 链名 | 对应的`chainIndex` |
|---|---|
| XLayer | `196` |
| Solana | `501` |
| Ethereum | `1` |
| Base | `8453` |
| BSC | `56` |
| Arbitrum | `42161` |

## 命令索引

| 命令编号 | 命令 | 描述 |
|---|---|---|
| 1 | `onchainos token search <查询>` | 按名称、符号或地址搜索token |
| 2 | `onchainos token info <地址>` | 获取token的基本信息（名称、符号、小数位数、标志） |
| 3 | `onchainos token price-info <地址>` | 获取详细的定价信息（价格、市值、流动性、成交量、24小时价格变化） |
| 4 | `onchainos token trending` | 获取热门/排名靠前的token |
| 5 | `onchainos token holders <地址>` | 获取token持有者分布（前20名） |

## 功能区分

| 功能需求 | 使用`okx-dex-token` | 使用`okx-dex-market` |
|---|---|---|
| 按名称/符号搜索token | `onchainos token search` | - |
| Token元数据（小数位数、标志） | `onchainos token info` | - |
| 价格 + 市值 + 流动性 + 多时间帧价格变化 | `onchainos token price-info` | - |
| Token排名（热门） | `onchainos token trending` | - |
| 持有者分布 | `onchainos token holders` | - |
| 原始实时价格（单一值） | - | `onchainos market price` |
| K线图/蜡烛图 | - | `onchainos market kline` |
| 交易历史记录（买入/卖出日志） | - | `onchainos market trades` |
| 指数价格（多源聚合） | - | `onchainos market index` |
| Meme token开发者声誉/欺诈行为 | - | `onchainos market memepump-token-dev-info` |
| 捆绑器/恶意行为检测 | - | `onchainos market memepump-token-bundle-info` |
| 同一开发者发布的类似token | - | `onchainos market memepump-similar-tokens` |

**使用建议**：`okx-dex-token`用于token的发现和深入分析（搜索、热门趋势、持有者信息、市值统计）。`okx-dex-market`用于获取原始价格数据、图表、智能资金交易信号以及meme token的欺诈行为检测。

## 跨功能工作流程

该工具通常是用户开始使用的**入口点**——用户通常会先搜索/发现token，然后进行交易。

### 工作流程A：搜索 → 研究 → 购买

> 用户：“查找BONK token，分析后购买一些”

```
1. okx-dex-token    onchainos token search BONK --chains solana              → get tokenContractAddress, chain, price
       ↓ tokenContractAddress
2. okx-dex-token    onchainos token price-info <address> --chain solana      → market cap, liquidity, volume24H, priceChange24H
3. okx-dex-token    onchainos token holders <address> --chain solana         → top 20 holders distribution
4. okx-dex-market   onchainos market kline <address> --chain solana --bar 1H → hourly price chart
       ↓ user decides to buy
5. okx-dex-swap     onchainos swap quote --from ... --to <address> --amount ... --chain solana
6. okx-dex-swap     onchainos swap swap --from ... --to <address> --amount ... --chain solana --wallet <addr>
```

**数据传递**：
- 第1步中的`tokenContractAddress`将在后续步骤中重复使用。
- 第1步中的`chain`将在后续步骤中重复使用。
- 第1步中的`decimal`或`onchainos token info`中的小数位数用于交换操作中的单位转换。

### 工作流程B：发现热门token → 调查 → 交易

> 用户：“Solana上有哪些热门token？”

```
1. okx-dex-token    onchainos token trending --chains solana --sort-by 5 --time-frame 4  → top tokens by 24h volume
       ↓ user picks a token
2. okx-dex-token    onchainos token price-info <address> --chain solana                   → detailed analytics
3. okx-dex-token    onchainos token holders <address> --chain solana                      → check if whale-dominated
4. okx-dex-market   onchainos market kline <address> --chain solana                       → K-line for visual trend
       ↓ user decides to trade
5. okx-dex-swap     onchainos swap swap --from ... --to ... --amount ... --chain solana --wallet <addr>
```

### 交换前的Token验证

在交换未知token之前，请务必进行验证：

```
1. okx-dex-token    onchainos token search <name>                            → find token
2. Check communityRecognized:
   - true → proceed with normal caution
   - false → warn user about risk
3. okx-dex-token    onchainos token price-info <address> → check liquidity:
   - liquidity < $10K → warn about high slippage risk
   - liquidity < $1K → strongly discourage trade
4. okx-dex-swap     onchainos swap quote ... → check isHoneyPot and taxRate
5. If all checks pass → proceed to swap
```

## 操作流程

### 第1步：确定需求

- 搜索token → `onchainos token search`
- 获取token元数据 → `onchainos token info`
- 获取价格、市值和流动性 → `onchainos token price-info`
- 查看排名 → `onchainos token trending`
- 查看持有者分布 → `onchainos token holders`

### 第2步：收集参数

- 如果不知道链名，建议默认使用XLayer（`--chain xlayer`，gas费用低，确认速度快），然后询问用户偏好哪个链。
- 如果只有token名称而没有地址，先使用`onchainos token search`。
- 搜索时，`--chains`的默认值为`"1,501"`（Ethereum + Solana）。
- 查看热门token时，`--sort-by`的默认值为`5`（成交量），`--time-frame`的默认值为`4`（24小时）。

### 第3步：调用并显示结果

- 显示搜索结果：名称、符号、链名、价格、24小时价格变化。
- 显示`communityRecognized`状态以表示可信度。
- 价格信息：同时显示市值、流动性和成交量。

### 第4步：建议下一步操作

根据用户执行的命令，建议2-3个相关的后续操作：

| 命令 | 建议 |
|---|---|
| `token search` | 1. 查看详细分析（市值、流动性） → `onchainos token price-info` |
| `token info` | 1. 查看价格和市场数据 → `onchainos token price-info` |
| `token price-info` | 1. 查看K线图 → `okx-dex-market` |
| `token trending` | 1. 查看特定token的详细信息 → `onchainos token price-info` |
| `token holders` | 1. 查看价格趋势 → `okx-dex-market` |
| `token holders` | 1. 查看价格趋势 → `okx-dex-market` |

以对话式的方式与用户交流，例如：“您想查看价格图表还是检查持有者分布？”——切勿直接向用户展示技能名称或端点路径。

## CLI命令参考

### 1. `onchainos token search`

按名称、符号或合约地址搜索token。

```bash
onchainos token search <query> [--chains <chains>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
|---|---|---|
| `<查询>` | 是 | - | 关键词：token名称、符号或合约地址 |
| `--chains` | 否 | `"1,501"` | 链名或ID，用逗号分隔（例如`"ethereum,solana"`或`"196,501"` |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `tokenContractAddress` | 字符串 | Token合约地址 |
| `tokenSymbol` | 字符串 | Token符号（例如`"ETH"`） |
| `tokenName` | 字符串 | Token全称 |
| `tokenLogoUrl` | 字符串 | Token标志图片URL |
| `chainIndex` | 字符串 | 链名标识符 |
| `decimal` | 字符串 | Token的小数位数（例如`"18"`） |
| `price` | 字符串 | 当前价格（美元） |
| `change` | 字符串 | 24小时价格变化百分比 |
| `marketCap` | 字符串 | 市值（美元） |
| `liquidity` | 字符串 | 流动性（美元） |
| `holders` | 字符串 | Token持有者数量 |
| `explorerUrl` | 字符串 | Token的区块浏览器URL |
| `tagList.communityRecognized` | 布尔值 | `true` = 在Top 10 CEX上列出或经过社区验证 |

### 2. `onchainos token info`

获取token的基本信息（名称、符号、小数位数、标志）。

```bash
onchainos token info <address> [--chain <chain>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
| `<地址>` | 是 | - | Token合约地址 |
| `--chain` | 否 | `ethereum` | 链名 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `tokenName` | 字符串 | Token全称 |
| `tokenSymbol` | 字符串 | Token符号（例如`"ETH"`） |
| `tokenLogoUrl` | 字符串 | Token标志图片URL |
| `decimal` | 字符串 | Token的小数位数（例如`"18"` |
| `tokenContractAddress` | 字符串 | Token合约地址 |
| `tagList.communityRecognized` | 布尔值 | `true` = 在Top 10 CEX上列出或经过社区验证 |

### 3. `onchainos token price-info`

获取详细的定价信息，包括市值、流动性、成交量和多时间帧的价格变化。

```bash
onchainos token price-info <address> [--chain <chain>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
| `<地址>` | 是 | - | Token合约地址 |
| `--chain` | 否 | `ethereum` | 链名 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `price` | 字符串 | 当前价格（美元） |
| `time` | 字符串 | 时间戳（Unix毫秒） |
| `marketCap` | 字符串 | 市值（美元） |
| `liquidity` | 字符串 | 流动性（美元） |
| `circSupply` | 字符串 | 流通量（美元） |
| `holders` | 字符串 | Token持有者数量 |
| `tradeNum` | 字符串 | 24小时交易数量 |
| `priceChange5M` | 字符串 | 过去5分钟的价格变化百分比 |
| `priceChange1H` | 字符串 | 过去1小时的价格变化百分比 |
| `priceChange4H` | 字符串 | 过去4小时的价格变化百分比 |
| `priceChange24H` | 字符串 | 过去24小时的价格变化百分比 |
| `volume5M` | 字符串 | 过去5分钟的成交量（美元） |
| `volume1H` | 字符串 | 过去1小时的成交量（美元） |
| `volume4H` | 字符串 | 过去4小时的成交量（美元） |
| `volume24H` | 字符串 | 过去24小时的成交量（美元） |
| `txs5M` | 字符串 | 过去5分钟的交易数量 |
| `txs1H` | 字符串 | 过去1小时的交易数量 |
| `txs4H` | 字符串 | 过去4小时的交易数量 |
| `txs24H` | 字符串 | 过去24小时的交易数量 |
| `maxPrice` | 字符串 | 24小时最高价格 |
| `minPrice` | 字符串 | 24小时最低价格 |

### 4. `onchainos token trending`

根据不同标准获取热门/排名靠前的token。

```bash
onchainos token trending [--chains <chains>] [--sort-by <sort>] [--time-frame <frame>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
|---|---|---|
| `--chains` | 否 | `"1,501"` | 链名或ID，用逗号分隔 |
| `--sort-by` | 否 | `"5"` | 排序方式：`2`=价格变化，`5`=成交量，`6`=市值 |
| `--time-frame` | 否 | `"4"` | 时间窗口：`1`=5分钟，`2`=1小时，`3`=4小时，`4`=24小时 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `tokenSymbol` | 字符串 | Token符号 |
| `tokenContractAddress` | 字符串 | Token合约地址 |
| `tokenLogoUrl` | 字符串 | Token标志图片URL |
| `chainIndex` | 字符串 | 链名标识符 |
| `price` | 字符串 | 当前价格（美元） |
| `change` | 字符串 | 选定时段的价格变化百分比 |
| `volume` | 字符串 | 选定时段的成交量（美元） |
| `marketCap` | 字符串 | 市值（美元） |
| `liquidity` | 字符串 | 总流动性（美元） |
| `holders` | 字符串 | Token持有者数量 |
| `uniqueTraders` | 字符串 | 选定时段的唯一交易者数量 |
| `txsBuy` | 字符串 | 选定时段的买入交易数量 |
| `txsSell` | 字符串 | 选定时段的卖出交易数量 |
| `txs` | 字符串 | 选定时段的总交易数量 |
| `firstTradeTime` | 字符串 | 第一笔交易的时间戳（Unix毫秒） |

### 5. `onchainos token holders`

获取token持有者分布（前20名）。

```bash
onchainos token holders <address> [--chain <chain>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
| `<地址>` | 是 | - | Token合约地址 |
| `--chain` | 否 | `ethereum` | 链名 |

**返回字段**（前20名持有者）：

| 字段 | 类型 | 描述 |
|---|---|---|
| `data[].holdAmount` | 字符串 | 持有的Token数量 |
| `data[].holderWalletAddress` | 字符串 | 持有者的钱包地址 |

## 输入/输出示例

**用户输入：**“在XLayer上搜索xETH token”

```bash
onchainos token search xETH --chains xlayer
# → Display:
#   xETH (0xe7b0...) - XLayer
#   Price: $X,XXX.XX | 24h: +X% | Market Cap: $XXM | Liquidity: $XXM
#   Community Recognized: Yes
```

**用户输入：**“Solana上成交量最高的token是什么？”

```bash
onchainos token trending --chains solana --sort-by 5 --time-frame 4
# → Display top tokens sorted by 24h volume:
#   #1 SOL  - Vol: $1.2B | Change: +3.5% | MC: $80B
#   #2 BONK - Vol: $450M | Change: +12.8% | MC: $1.5B
#   ...
```

**用户输入：**“这个token的顶级持有者是谁？”

```bash
onchainos token holders 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee --chain xlayer
# → Display top 20 holders with amounts and addresses
```

## 边缘情况

- **未找到Token**：建议验证合约地址（符号可能重复）。
- **同一符号存在于多个链上**：显示所有匹配的链名。
- **未验证的Token**：`communityRecognized`设置为`false`——提醒用户注意风险。
- **结果过多**：名称/符号的搜索结果限制为100条——建议使用确切的合约地址。
- **网络错误**：重试一次。
- **地区限制（错误代码50125或80001）**：不要向用户显示原始错误代码，而是显示友好提示：`⚠️ 该服务在您的地区不可用。请切换到支持的地区后再试。`

## 数字显示规则

- 对于高价值Token，使用2位小数；对于低价值Token，使用足够的位数显示。
- 市值/流动性使用简写格式（例如$1.2B、$45M）。
- 24小时价格变化用符号和颜色表示（+X% / -X%）。

## 全局注意事项

- 使用合约地址作为**主要识别依据**——不同Token的符号可能相同。
- `communityRecognized = true`表示在Top 10 CEX上列出或经过社区验证。
- CLI会自动解析链名（例如`ethereum` → `1`，`solana` → `501`）。
- EVM地址必须全部小写。
- CLI通过环境变量内部处理身份验证——详见“先决条件”步骤中的默认值。