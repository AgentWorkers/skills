---
name: okx-dex-token
description: "此功能适用于以下场景：用户请求“查找代币”、“搜索代币”、“查询PEPE代币的信息”、“了解当前的热门代币”、“查看热门代币排行榜”、“获取代币排名”、“查询持有该代币的用户”、“分析代币的持有者分布”、“了解代币的市场资本市值”、“评估代币的流动性”、“深入研究某个代币”、“提供代币的详细信息”，或者提及通过名称或地址来搜索代币、发现热门代币、查看代币排名、检查持有者分布、分析代币的市场资本市值和流动性等。该功能支持在XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon以及20多个其他区块链平台上进行代币搜索、查询代币元数据、市场资本市值、流动性、交易量、热门代币排名以及持有者分析。**请注意：**当用户仅简单提及“代币”或“加密货币”而没有具体说明代币名称、操作或问题时，切勿使用此功能。对于简单的当前价格查询、价格图表、K线数据或交易历史信息，请使用okx-dex-market。另外，对于Meme代币的安全性分析、开发者声誉评估、欺诈行为检测，或根据创作者来查找代币等功能，也请使用okx-dex-market。"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.1"
  homepage: "https://web3.okx.com"
---
# OKX DEX Token Info CLI

提供了5个命令，用于查询token信息、元数据、详细价格、排名以及持有者分布。

## 预运行检查

在运行任何`onchainos`命令之前，请务必按照以下步骤操作。不要将常规命令的输出显示给用户；仅在安装、更新或处理失败时提供简短的状态更新。

1. **确认已安装**：运行`which onchainos`。如果未找到，请根据以下链接手动安装：https://github.com/okx/onchainos-skills
2. **检查更新**：读取`~/.onchainos/last_check`文件，并将其与当前时间戳进行比较：
   - 如果`cached_ts`不为空且`(now - cached_ts) < 43200`（12小时内），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时），运行安装程序以检查更新：
   - 如果安装了新版本，请告知用户，并建议他们从https://github.com/okx/onchainos-skills更新他们的onchainos技能以获取最新功能。
3. 如果在此过程中任何`onchainos`命令因意外错误而失败，请尝试重新安装后再进行操作。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可跳过此步骤）。

## 技能路由

- 实时价格、K线图和交易历史记录：使用`okx-dex-market`
- 交易执行：使用`okx-dex-swap`
- 交易广播：使用`okx-onchain-gateway`
- 钱包余额和投资组合：使用`okx-wallet-portfolio`
- 模因币安全（开发者声誉、欺诈行为、同一开发者的类似token）：使用`okx-dex-market`
- 智能资金、大资金持有者和KOL信号：使用`okx-dex-market`

## 快速入门

## 支持的链名

该CLI接受人类可读的链名（例如`ethereum`、`solana`、`xlayer`），并自动解析它们。

| 链名 | 对应的chainIndex |  
|---|---|
| XLayer | `196` |  
| Solana | `501` |  
| Ethereum | `1` |  
| Base | `8453` |  
| BSC | `56` |  
| Arbitrum | `42161` |  

## 命令索引

| 命令 | 描述 |  
|---|---|---|
| 1 | `onchainos token search <查询>` | 按名称、符号或地址搜索token |
| 2 | `onchainos token info <地址>` | 获取token的基本信息（名称、符号、小数位数、标志） |
| 3 | `onchainos token price-info <地址>` | 获取详细的定价信息（价格、市值、流动性、成交量、24小时变化） |
| 4 | `onchainos token trending` | 获取热门/排名靠前的token |
| 5 | `onchainos token holders <地址>` | 获取token持有者分布（前20名） |

## 功能区分

| 功能需求 | 使用哪个技能（`okx-dex-token`） | 使用`okx-dex-market` |
|---|---|---|
| 按名称/符号搜索token | `onchainos token search` | - |
| Token元数据（小数位数、标志） | `onchainos token info` | - |
| 价格 + 市值 + 流动性 + 多时间框架变化 | `onchainos token price-info` | - |
| Token排名（热门） | `onchainos token trending` | - |
| 持有者分布 | `onchainos token holders` | - |
| 原始实时价格（单一值） | - | `onchainos market price` |
| K线图/蜡烛图 | - | `onchainos market kline` |
| 交易历史记录（买卖记录） | - | `onchainos market trades` |
| 指数价格（多源汇总） | - | `onchainos market index` |
| 模因币开发者声誉/欺诈行为 | - | `onchainos market memepump-token-dev-info` |
| 模因币捆绑/检测 | - | `onchainos market memepump-token-bundle-info` |
| 同一开发者的类似token | - | `onchainos market memepump-similar-tokens` |

**经验法则**：`okx-dex-token`用于token发现和丰富分析（搜索、热门趋势、持有者信息、市值）。`okx-dex-market`用于获取原始价格数据、图表、智能资金信号以及模因币的欺诈行为检测。

## 跨技能工作流程

这个技能是典型的**入口点**——用户通常会先搜索/发现token，然后进行交易。

### 工作流程A：搜索 → 研究 → 购买

> 用户：“查找BONK token，分析后购买一些”

### 数据传递：
- 第1步中的`tokenContractAddress`会在后续步骤中重复使用
- 第1步中的`chain`也会在后续步骤中重复使用
- 第1步中的`decimal`或`onchainos token info`中的数据用于交易时的单位转换

### 工作流程B：发现热门token → 调查 → 交易

> 用户：“Solana上有哪些热门token？”

### 工作流程C：交易前验证token

在交易未知token之前，请务必进行验证：

### 操作流程

### 第1步：确定需求

- 搜索token → `onchainos token search`
- 获取token元数据 → `onchainos token info`
- 获取价格、市值和流动性 → `onchainos token price-info`
- 查看排名 → `onchainos token trending`
- 查看持有者分布 → `onchainos token holders`

### 第2步：收集参数

- 如果缺少链名，建议使用XLayer（`--chain xlayer`，gas费用低，确认速度快）作为默认选项，然后询问用户偏好哪个链名
- 如果只有token名称而没有地址，先使用`onchainos token search`
- 搜索时，`--chains`的默认值为`"1,501"`（Ethereum + Solana）
- 查看热门token时，`--sort-by`的默认值为`5`（成交量），`--time-frame`的默认值为`4`（24小时）

### 第3步：调用并显示结果

- 显示搜索结果：名称、符号、链名、价格、24小时变化
- 显示`communityRecognized`状态以表示可信度
- 价格信息：同时显示市值、流动性和成交量

### 第4步：建议下一步操作

根据用户执行的命令，建议2-3个相关的后续操作：

| 命令 | 建议 |
|---|---|
| `token search` | 1. 查看详细分析（市值、流动性） → `onchainos token price-info` | 2. 查看价格图表 → `okx-dex-market` | 3. 购买/交易该token → `okx-dex-swap` |
| `token info` | 1. 查看价格和市场数据 → `onchainos token price-info` | 2. 查看持有者分布 → `onchainos token holders` |  |
| `token price-info` | 1. 查看K线图 → `okx-dex-market` | 2. 查看持有者分布 → `onchainos token holders` |  |
| `token trending` | 1. 查看特定token的详细信息 → `onchainos token price-info` | 2. 查看价格图表 → `okx-dex-market` | 3. 购买热门token → `okx-dex-swap` | |
| `token holders` | 1. 查看价格趋势 → `okx-dex-market` | 2. 购买/交易该token → `okx-dex-swap` | |

以对话的方式与用户交流，例如：“您想查看价格图表还是检查持有者分布？”——切勿向用户透露技能名称或端点路径。

## CLI命令参考

### 1. `onchainos token search`

按名称、符号或合约地址搜索token。

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|---|
| `<查询>` | 是 | - | 关键词：token名称、符号或合约地址 |
| `--chains` | 否 | `"1,501"` | 链名或ID，用逗号分隔（例如，`"ethereum,solana"`或`"196,501"` |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `tokenContractAddress` | 字符串 | Token合约地址 |
| `tokenSymbol` | 字符串 | Token符号（例如，`"ETH"`） |
| `tokenName` | 字符串 | Token全名 |
| `tokenLogoUrl` | 字符串 | Token标志图片URL |
| `chainIndex` | 字符串 | 链名标识符 |
| `decimal` | 字符串 | Token的小数位数（例如，`"18"`） |
| `price` | 字符串 | 当前价格（美元） |
| `change` | 字符串 | 24小时价格变化百分比 |
| `marketCap` | 字符串 | 市值（美元） |
| `liquidity` | 字符串 | 流动性（美元） |
| `holders` | 字符串 | Token持有者数量 |
| `explorerUrl` | 字符串 | Token的区块浏览器URL |
| `tagList.communityRecognized` | 布尔值 | `true` = 在Top 10 CEX上列出或经过社区验证 |

### 2. `onchainos token info`

获取token的基本信息（名称、符号、小数位数、标志）。

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|
| `<地址>` | 是 | - | Token合约地址 |
| `--chain` | 否 | `ethereum` | 链名 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `tokenName` | 字符串 | Token全名 |
| `tokenSymbol` | 字符串 | Token符号（例如，`"ETH"`） |
| `tokenLogoUrl` | 字符串 | Token标志图片URL |
| `decimal` | 字符串 | Token的小数位数（例如，`"18"` |
| `tokenContractAddress` | 字符串 | Token合约地址 |
| `tagList.communityRecognized` | 布尔值 | `true` = 在Top 10 CEX上列出或经过社区验证 |

### 3. `onchainos token price-info`

获取详细的定价信息，包括市值、流动性、成交量和多时间框架的价格变化。

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|
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

根据各种标准获取热门/排名靠前的token。

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|
| `--chains` | 否 | `"1,501"` | 链名或ID，用逗号分隔 |
| `--sort-by` | 否 | `"5"` | 排序方式：`2`=价格变化，`5`=成交量，`6`=市值 |
| `--time-frame` | 否 | `"4"` | 时间范围：`1`=5分钟，`2`=1小时，`3`=4小时，`4`=24小时 |

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

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|
| `<地址>` | 是 | - | Token合约地址 |
| `--chain` | 否 | `ethereum` | 链名 |

**返回字段**（前20名持有者）：

| 字段 | 类型 | 描述 |
|---|---|---|
| `data[].holdAmount` | 字符串 | 持有的Token数量 |
| `data[].holderWalletAddress` | 字符串 | 持有者的钱包地址 |

## 输入/输出示例

**用户输入：“在XLayer上搜索xETH token”**

**用户输入：“Solana上按成交量排名靠前的token是什么？”**

**用户输入：“这个token的顶级持有者是谁？”**

## 边缘情况

- **Token未找到**：建议验证合约地址（符号可能重复）
- **同一符号存在于多个链上**：显示所有匹配的链名
- **未验证的token**：`communityRecognized = false` —— 警告用户存在风险
- **结果太多**：名称/符号的搜索结果限制为100条 —— 建议使用确切的合约地址
- **网络错误**：重试一次
- **地区限制（错误代码50125或80001）**：不要向用户显示原始错误代码，而是显示友好提示：`⚠️ 该服务在您的地区不可用。请切换到支持的地区后再试。`

## 数字显示规则

- 对于高价值token，使用2位小数；对于低价值token，使用足够的数字显示精度
- 市值/流动性使用简写格式（例如：$1.2B, $45M）
- 24小时变化使用带符号和颜色提示（+X% / -X%）

## 全局说明

- 使用合约地址作为**主要识别依据** —— 不同token的符号可能相同
- `communityRecognized = true`表示在Top 10 CEX上列出或经过社区验证
- CLI会自动解析链名（例如，`ethereum` → `1`，`solana` → `501`）
- EVM地址必须全部小写
- CLI通过环境变量内部处理身份验证——详见前提条件第4步中的默认值