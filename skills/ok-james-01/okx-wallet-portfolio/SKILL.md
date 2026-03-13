---
name: okx-wallet-portfolio
description: "此技能适用于用户请求“查看我的钱包余额”、“显示我的代币持有情况”、“我拥有多少OKB代币”、“我有哪些代币”、“检查我的投资组合价值”、“查看我的资产”、“我的投资组合价值是多少”、“我的钱包里有什么”等情况。该技能支持XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon以及20多种其他区块链平台。请勿将其用于关于余额变量或API文档的一般性编程问题；也不适用于用户询问如何将余额功能集成到代码中的情况。"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.2"
  homepage: "https://web3.okx.com"
---
# OKX钱包投资组合CLI

该CLI提供了4个命令，用于查询不同链路的资产信息、钱包总价值、所有代币的余额以及特定代币的余额。

## 预运行检查

在运行任何`onchainos`命令之前，请务必按照以下步骤操作。不要将常规命令的输出显示给用户，仅在安装、更新或处理错误时提供简短的状态更新：

1. **确认已安装**：运行`which onchainos`。如果未找到该命令，请根据以下链接手动安装：https://github.com/okx/onchainos-skills
2. **检查更新**：读取`~/.onchainos/last_check`文件，并将其与当前时间戳进行比较：
   - 如果`cached_ts`非空且`(now - cached_ts) < 43200`（12小时内），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时），运行安装程序以检查更新：
     如果安装了新版本，请告知用户，并建议他们从https://github.com/okx/onchainos-skills更新他们的onchainos技能以获取最新功能。
3. 如果在此过程中任何`onchainos`命令因意外错误失败，请尝试重新安装后再继续。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可跳过此步骤）。

## 技能路由

- 代币价格/K-line信息：使用`okx-dex-market`
- 代币搜索/元数据：使用`okx-dex-token`
- 交易执行：使用`okx-dex-swap`
- 交易广播：使用`okx-onchain-gateway`

## 快速入门

## 支持的链路名称

该CLI支持用户可读的链路名称，并能自动解析这些名称。

| 链路 | 名称 | chainIndex |
|---|---|---|
| XLayer | `xlayer` | `196` |
| Solana | `solana` | `501` |
| Ethereum | `ethereum` | `1` |
| Base | `base` | `8453` |
| BSC | `bsc` | `56` |
| Arbitrum | `arbitrum` | `42161` |

**地址格式说明**：EVM地址（`0x...`）适用于Ethereum/BSC/Polygon/Arbitrum/Base等链路；Solana地址（Base58）和Bitcoin地址（UTXO）的格式不同。请勿在不同链路类型之间混用地址格式。

## 命令索引

| 编号 | 命令 | 描述 |
|---|---|---|
| 1 | `onchainos portfolio chains` | 获取可用于余额查询的链路列表 |
| 2 | `onchainos portfolio total-value --address ... --chains ...` | 获取钱包的总资产价值 |
| 3 | `onchainos portfolio all-balances --address ... --chains ...` | 获取钱包中所有代币的余额 |
| 4 | `onchainos portfolio token-balances --address ... --tokens ...` | 获取钱包中特定代币的余额 |

## 跨技能工作流程

此技能通常用于**交易前**（验证余额是否充足）或作为**投资组合的入口点**。

### 工作流程A：交易前余额检查

> 用户：“将1个SOL兑换成BONK”

**数据传递**：
- 从代币搜索中获取的`tokenContractAddress`用于交易命令的`--from`/`--to`参数
- 从投资组合中获取的余额是**UI单位**；交易需要**最小单位**，因此需要将其乘以`10^decimal`
- 如果余额低于所需金额，则通知用户，不要继续进行交易

### 工作流程B：投资组合概览与分析

> 用户：“显示我的投资组合”

### 工作流程C：出售表现不佳的代币

**关键转换**：`balance`（UI单位）× `10^decimal` = `amount`（交易所需的最小单位）

## 操作流程

### 第1步：确定操作意图

- 查看总资产：`onchainos portfolio total-value`
- 查看所有代币持有情况：`onchainos portfolio all-balances`
- 查看特定代币的余额：`onchainos portfolio token-balances`
- 如果不确定支持哪些链路，先使用`onchainos portfolio chains`查询

### 第2步：收集参数

- 如果缺少钱包地址，请询问用户
- 如果缺少目标链路，建议默认使用XLayer（`--chains xlayer`，Gas费用低，确认速度快），然后询问用户偏好哪个链路。常见选项：`"xlayer,solana,ethereum,base,bsc"`
- 如果需要过滤风险代币，设置`--exclude-risk 0`（仅适用于ETH/BSC/SOL/BASE）

### 第3步：调用并显示结果

- 显示总价值（以USD为单位）
- 显示代币名称、数量（UI单位）和USD价值
- 按USD价值降序排序

### 第4步：建议下一步操作

在显示结果后，建议用户进行2-3个相关的后续操作：

| 操作 | 建议 |
|---|---|
| `portfolio total-value` | 1. 查看代币级别的详细信息 → `onchainos portfolio all-balances` |
| `portfolio all-balances` | 1. 查看代币的详细分析（市值、24小时变化） → `okx-dex-token` |
| `portfolio token-balances` | 1. 查看整个投资组合中的所有代币 → `onchainos portfolio all-balances` |
| `portfolio token-balances` | 1. 交易这些代币 → `okx-dex-swap` |

以对话的方式与用户交流，例如：“您想查看您持有最多的代币的价格图表吗？或者想要交易其中某个代币吗？”——切勿向用户透露技能名称或端点路径。

## CLI命令参考

### 1. `onchainos portfolio chains`

获取可用于余额查询的链路列表。无需参数。

**返回字段**：
| 字段 | 类型 | 描述 |
|---|---|---|
| `name` | String | 链路名称（例如，“XLayer”） |
| `logoUrl` | String | 链路Logo的URL |
| `shortName` | String | 链路的简称（例如，“OKB”） |
| `chainIndex` | String | 链路的唯一标识符（例如，“196”） |

### 2. `onchainos portfolio total-value`

获取钱包地址的总资产价值。

**参数**：
- `--address` | 是 | - | 钱包地址 |
- `--chains` | 是 | - | 链路名称或ID（用逗号分隔，例如，“xlayer,solana”或“196,501”） |
- `--asset-type` | 否 | `0` | `0` = 所有资产；`1` = 仅代币；`2` = 仅DeFi资产 |
- `--exclude-risk` | 否 | `true` | `true` = 过滤风险代币；`false` = 包含所有资产 |

**返回字段**：
| 字段 | 类型 | 描述 |
|---|---|---|
| `totalValue` | String | 总资产价值（以USD为单位） |

### 3. `onchainos portfolio all-balances`

获取钱包地址的所有代币余额。

**参数**：
- `--address` | 是 | - | 钱包地址 |
- `--chains` | 是 | - | 链路名称或ID（用逗号分隔，最多50个） |
- `--exclude-risk` | 否 | `0` | `0` = 过滤风险代币（默认）；`1` = 包含所有代币 |

**返回字段**（每个代币在`tokenAssets[]`中）：
| 字段 | 类型 | 描述 |
|---|---|---|
| `chainIndex` | String | 链路标识符 |
| `tokenContractAddress` | String | 代币合约地址 |
| `symbol` | String | 代币符号（例如，“OKB”） |
| `balance` | String | 代币余额（以UI单位表示，例如，“10.5”） |
| `rawBalance` | String | 代币的原始余额（以基础单位表示，例如，“10500000000000000000”） |
| `tokenPrice` | String | 代币价格（以USD表示） |
| `isRiskToken` | Boolean | 如果标记为风险代币，则为`true` |

### 4. `onchainos portfolio token-balances`

获取钱包地址的特定代币余额。

**参数**：
- `--address` | 是 | - | 钱包地址 |
- `--tokens` | 是 | - | 代币列表（格式为`chainIndex:tokenAddress`），用逗号分隔。对于原生代币（如OKB），可以使用空地址（例如，“196:”）。最多20个条目。 |
- `--exclude-risk` | 否 | `0` | `0` = 过滤风险代币（默认）；`1` = 包含风险代币 |

**返回字段**：与`all-balances`相同。

## 输入/输出示例

**用户输入：“查看我在XLayer和Solana上的钱包总资产”**

**用户输入：“显示我钱包中的所有代币”**

**用户输入：“仅查看我在XLayer上的USDC和原生OKB的余额”**

## 边缘情况

- **余额为零**：显示`$0.00`，视为正常状态，不是错误
- **不支持的链路**：首先调用`onchainos portfolio chains`进行确认
- **支持的链路超过50个**：分批处理，每次请求最多50个链路
- `--exclude-risk`无效：仅适用于ETH/BSC/SOL/BASE链路
- **DeFi资产**：使用`--asset-type 2`单独查询DeFi资产
- **地址格式不匹配**：EVM地址（`0x…`）和Solana/UTXO地址的格式不兼容。使用错误的地址会导致整个请求失败——不会返回部分结果。请分别为EVM链路和Solana链路分别发送请求
- **网络错误**：重试一次，然后提示用户稍后再试
- **地区限制（错误代码50125或80001）**：不要向用户显示原始错误代码，而是显示友好提示：`⚠️ 该服务在您所在地区不可用。请切换到支持的地区后再试。`

## 金额显示规则

- 代币数量以UI单位显示（例如，“1.5 ETH”）， never 以基础单位显示（例如，“1500000000000000000”）
- USD价值保留2位小数
- 大额金额使用简写形式（例如，“$1.2M”）
- 按USD价值降序排序

## 全局说明

- `--chains`支持最多50个链路ID（用逗号分隔，可以是名称或数字）
- `--asset-type`：`0` = 所有资产；`1` = 仅代币；`2` = 仅DeFi资产（仅适用于`total-value`）
- `--exclude-risk`仅适用于ETH（`1`）、BSC（`56`）、Solana（`501`）和Base（`8453`）
- `token-balances`最多支持20个代币条目
- CLI会自动解析链路名称（例如，`ethereum` → `1`，`solana` → `501`）
- CLI通过环境变量处理身份验证——详见前提条件中的设置