---
name: okx-wallet-portfolio
description: "此技能适用于用户请求“查看我的钱包余额”、“显示我的代币持有情况”、“我拥有多少OKB？”、“我有哪些代币？”、“检查我的投资组合价值”、“查看我的资产”、“我的投资组合价值是多少？”、“我的钱包里有什么？”等情况。它支持XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon以及20多种其他区块链平台。**请勿将其用于关于余额变量或API文档的一般性编程问题**，也请勿在用户询问如何将余额功能集成到代码中时使用该技能。"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.1"
  homepage: "https://web3.okx.com"
---
# OKX钱包投资组合CLI

该CLI提供了4个命令，用于查询支持的交易链、钱包总资产价值、所有代币余额以及特定代币的余额。

## 预运行检查

在每次运行`onchainos`命令之前，请务必按照以下步骤操作。不要将常规命令的输出显示给用户，仅在安装、更新或处理错误时提供简短的状态更新：

1. **确认已安装**：运行`which onchainos`。如果未找到该命令，请按照以下链接手动安装：https://github.com/okx/onchainos-skills
2. **检查更新**：读取`~/.onchainos/last_check`文件，并将其与当前时间戳进行比较：
   - 如果`cached_ts`非空且`(now - cached_ts) < 43200`（12小时以内），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时），运行安装程序以检查更新：
     如果安装了新版本，请告知用户，并建议他们从https://github.com/okx/onchainos-skills更新他们的onchainos技能以获取最新功能。
3. 如果在本次会话中任何`onchainos`命令因意外错误而失败，请尝试重新安装后再继续操作。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可跳过此步骤）。

## 技能路由

- 代币价格/K线图查询 → 使用`okx-dex-market`
- 代币搜索/元数据查询 → 使用`okx-dex-token`
- 交易执行 → 使用`okx-dex-swap`
- 交易广播 → 使用`okx-onchain-gateway`

## 快速入门

```bash
# Get supported chains for balance queries
onchainos portfolio chains

# Get total asset value on XLayer and Solana
onchainos portfolio total-value --address 0xYourWallet --chains "xlayer,solana"

# Get all token balances
onchainos portfolio all-balances --address 0xYourWallet --chains "xlayer,solana,ethereum"

# Check specific tokens (native OKB + USDC on XLayer)
onchainos portfolio token-balances --address 0xYourWallet --tokens "196:,196:0x74b7f16337b8972027f6196a17a631ac6de26d22"
```

## 支持的交易链名称

该CLI支持人类可读的交易链名称，并能自动解析这些名称。

| 交易链 | 名称 | chainIndex |
|---|---|---|
| XLayer | `xlayer` | `196` |
| Solana | `solana` | `501` |
| Ethereum | `ethereum` | `1` |
| Base | `base` | `8453` |
| BSC | `bsc` | `56` |
| Arbitrum | `arbitrum` | `42161` |

**地址格式说明**：EVM地址（`0x...`）适用于Ethereum/BSC/Polygon/Arbitrum/Base等链；Solana地址（Base58）和Bitcoin地址（UTXO）的格式不同。请勿在不同类型的链之间混合使用地址格式。

## 命令索引

| 编号 | 命令 | 描述 |
|---|---|---|
| 1 | `onchainos portfolio chains` | 获取支持的交易链列表，用于查询余额 |
| 2 | `onchainos portfolio total-value --address ... --chains ...` | 获取钱包的总资产价值 |
| 3 | `onchainos portfolio all-balances --address ... --chains ...` | 获取钱包的所有代币余额 |
| 4 | `onchainos portfolio token-balances --address ... --tokens ...` | 获取钱包中特定代币的余额 |

## 跨技能工作流程

此技能通常用于**交易前**（验证余额是否充足）或作为**投资组合的入口点**。

### 工作流程A：交易前余额检查

> 用户：“将1个SOL兑换成BONK”

```
1. okx-dex-token    onchainos token search BONK --chains solana               → get tokenContractAddress
       ↓ tokenContractAddress
2. okx-wallet-portfolio  onchainos portfolio all-balances --address <addr> --chains solana
       → verify SOL balance >= 1
       ↓ balance field (UI units) → convert to minimal units for swap
3. okx-dex-swap     onchainos swap quote --from 11111111111111111111111111111111 --to <BONK_address> --amount 1000000000 --chain solana
4. okx-dex-swap     onchainos swap swap --from ... --to <BONK_address> --amount 1000000000 --chain solana --wallet <addr>
```

**数据传递**：
- 从代币搜索中获取的`tokenContractAddress`用于交换命令的`--from`/`--to`参数
- 从投资组合中获取的`balance`是**用户界面单位**；交换需要**最小单位**，因此需要将其乘以`10^decimal`
- 如果余额低于所需金额 → 通知用户，不要继续进行交易

### 工作流程B：投资组合概览 + 分析

> 用户：“显示我的投资组合”

```
1. okx-wallet-portfolio  onchainos portfolio total-value --address <addr> --chains "xlayer,solana,ethereum"
       → total USD value
2. okx-wallet-portfolio  onchainos portfolio all-balances --address <addr> --chains "xlayer,solana,ethereum"
       → per-token breakdown
       ↓ top holdings by USD value
3. okx-dex-token    onchainos token price-info <address> --chain <chain>  → enrich with 24h change, market cap
4. okx-dex-market   onchainos market kline <address> --chain <chain>      → price charts for tokens of interest
```

### 工作流程C：出售表现不佳的代币

```
1. okx-wallet-portfolio  onchainos portfolio all-balances --address <addr> --chains "xlayer,solana,ethereum"
       → list all holdings
       ↓ tokenContractAddress + chainIndex for each
2. okx-dex-token    onchainos token price-info <address> --chain <chain>  → get priceChange24H per token
3. Filter by negative change → user confirms which to sell
4. okx-dex-swap     onchainos swap quote → onchainos swap swap → execute sell
```

**关键转换**：`balance`（用户界面单位）× `10^decimal` = `amount`（最小单位），用于交易。

## 操作流程

### 第1步：确定操作意图

- 查看总资产 → 使用`onchainos portfolio total-value`
- 查看所有代币持有情况 → 使用`onchainos portfolio all-balances`
- 查看特定代币的余额 → 使用`onchainos portfolio token-balances`
- 如果不确定支持哪些交易链 → 先使用`onchainos portfolio chains`查询

### 第2步：收集参数

- 如果缺少钱包地址 → 询问用户
- 如果缺少目标交易链 → 建议默认使用XLayer（`--chains xlayer`，Gas费用低，确认速度快），然后询问用户偏好哪个交易链。常见组合：`"xlayer,solana,ethereum,base,bsc"`
- 如果需要过滤风险代币 → 设置`--exclude-risk 0`（仅适用于ETH/BSC/SOL/BASE）

### 第3步：调用并显示结果

- 显示总资产价值（以美元为单位）
- 显示代币名称、数量（用户界面单位）和美元价值
- 按美元价值降序排序

### 第4步：建议下一步操作

显示结果后，建议用户进行2-3个相关的后续操作：

| 操作建议 | 建议 |
|---|---|
| `portfolio total-value` | 1. 查看代币级别的详细信息 → 使用`onchainos portfolio all-balances` |
| `portfolio all-balances` | 1. 查看代币的市场资本量和24小时价格变化 → 使用`okx-dex-token` |
| `portfolio token-balances` | 1. 查看所有代币的投资组合概览 → 使用`onchainos portfolio all-balances` |
| 2. 交换某个代币 → 使用`okx-dex-swap` |

以对话的方式与用户交流，例如：“您想查看您持有最多的代币的价格图表吗？或者想兑换这些代币中的任何一个吗？”——切勿向用户透露技能名称或端点路径。

## CLI命令参考

### 1. `onchainos portfolio chains`

获取支持的交易链列表，用于查询余额。无需参数。

```bash
onchainos portfolio chains
```

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `name` | String | 交易链名称（例如，“XLayer”） |
| `logoUrl` | String | 交易链的Logo链接 |
| `shortName` | String | 交易链的简称（例如，“OKB”） |
| `chainIndex` | String | 交易链的唯一标识符（例如，“196”） |

### 2. `onchainos portfolio total-value`

获取钱包地址的总资产价值。

```bash
onchainos portfolio total-value --address <address> --chains <chains> [--asset-type <type>] [--exclude-risk <bool>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
|---|---|---|---|
| `--address` | 是 | - | 钱包地址 |
| `--chains` | 是 | - | 交易链名称或ID，用逗号分隔（例如，“xlayer,solana”或“196,501”） |
| `--asset-type` | 否 | `0` | `0` = 所有资产；`1` = 仅代币；`2` = 仅DeFi资产 |
| `--exclude-risk` | 否 | `true` | `true` = 过滤风险代币；`false` = 包含所有代币 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `totalValue` | String | 总资产价值（以美元为单位） |

### 3. `onchainos portfolio all-balances`

获取钱包地址的所有代币余额。

```bash
onchainos portfolio all-balances --address <address> --chains <chains> [--exclude-risk <value>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
|---|---|---|---|
| `--address` | 是 | - | 钱包地址 |
| `--chains` | 是 | - | 交易链名称或ID，用逗号分隔，最多50个 |
| `--exclude-risk` | 否 | `0` | `0` = 过滤风险代币（默认）；`1` = 包含所有代币 |

**返回字段**（每个代币在`tokenAssets[]`中）：

| 字段 | 类型 | 描述 |
|---|---|---|
| `chainIndex` | String | 交易链标识符 |
| `tokenContractAddress` | String | 代币合约地址 |
| `symbol` | String | 代币符号（例如，“OKB”） |
| `balance` | String | 代币余额（用户界面单位，例如，“10.5”） |
| `rawBalance` | String | 代币的原始余额（基础单位，例如，“10500000000000000000”） |
| `tokenPrice` | String | 代币价格（以美元为单位） |
| `isRiskToken` | Boolean | 如果标记为风险代币，则为`true` |

### 4. `onchainos portfolio token-balances`

获取钱包地址中特定代币的余额。

```bash
onchainos portfolio token-balances --address <address> --tokens <tokens> [--exclude-risk <value>]
```

| 参数 | 是否必填 | 默认值 | 描述 |
|---|---|---|
| `--address` | 是 | - | 钱包地址 |
| `--tokens` | 是 | - | 代币列表：`chainIndex:tokenAddress`对，用逗号分隔。对于原生代币（例如OKB），可以使用空地址（例如，“196:”）。最多20个条目。 |
| `--exclude-risk` | 否 | `0` | `0` = 过滤掉风险代币（默认）；`1` = 包含风险代币 |

**返回字段**：与`all-balances`相同。

## 输入/输出示例

**用户输入：“查看我在XLayer和Solana上的钱包总资产”**

```bash
onchainos portfolio total-value --address 0xYourWallet --chains "xlayer,solana"
# → Display: Total assets $12,345.67
```

**用户输入：“显示我钱包中的所有代币”**

```bash
onchainos portfolio all-balances --address 0xYourWallet --chains "xlayer,solana,ethereum"
# → Display:
#   OKB:  10.5 ($509.25)
#   USDC: 2,000 ($2,000.00)
#   USDT: 1,500 ($1,500.00)
#   ...
```

**用户输入：“仅查看XLayer上的USDC和原生OKB的余额”**

```bash
onchainos portfolio token-balances --address 0xYourWallet --tokens "196:,196:0x74b7f16337b8972027f6196a17a631ac6de26d22"
# → Display: OKB: 10.5 ($509.25), USDC: 2,000 ($2,000.00)
```

## 边缘情况

- **余额为零**：显示`$0.00`，视为正常状态，不是错误
- **不支持的交易链**：首先使用`onchainos portfolio chains`进行确认
- 如果支持的交易链超过50个，则分批处理，每次请求最多显示50个
- 如果`--exclude-risk`参数无效：仅适用于ETH/BSC/SOL/BASE
- **DeFi资产**：使用`--asset-type 2`单独查询DeFi资产
- **地址格式不匹配**：Solana链上的EVM地址将返回空数据——请勿混合使用不同格式的地址
- **网络错误**：重试一次，然后提示用户稍后再试
- **地区限制（错误代码50125或80001）**：不要向用户显示原始错误代码，而是显示友好的提示信息：`⚠️ 该服务在您的地区不可用。请切换到支持的地区后再试。`

## 金额显示规则

- 代币金额以用户界面单位显示（例如“1.5 ETH”），而不是基础单位（例如“1500000000000000000”）
- 美元价值保留2位小数
- 大额金额使用简写形式（例如“$1.2M”）
- 按美元价值降序排序

## 全局说明

- `--chains`支持最多50个交易链ID（用逗号分隔，可以是名称或数字）
- `--asset-type`：`0` = 所有资产；`1` = 仅代币；`2` = 仅DeFi资产（仅适用于`total-value`命令）
- `--exclude-risk`仅适用于ETH（`1`）、BSC（`56`）、Solana（`501`）和Base（`8453`）
- `token-balances`最多支持20个代币条目
- CLI会自动解析交易链名称（例如，`ethereum` → `1`，`solana` → `501`）
- CLI通过环境变量处理身份验证——请参阅“先决条件”步骤以获取默认值