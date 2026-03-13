---
name: okx-dex-swap
description: "此技能适用于以下场景：用户请求“交换代币”、“用OKB兑换USDC”、“购买代币”、“出售代币”、“交易加密货币”、“转换代币”、“用SOL兑换USDC”、“获取交换报价”、“执行交易”、“寻找最佳交换路径”、“寻找最便宜的交换方式”、“进行最优交换”、“比较交换费率”，或提及在XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon以及20多个支持的交易链上进行代币的交换、交易、购买或出售操作。该技能会从500多个去中心化交易所（DEX）中聚合流动性信息，以帮助用户找到最优的交换路径和价格。同时支持滑点控制、价格影响保护以及跨交易所路径优化功能。**请勿将其用于与交换代码相关的一般编程问题，也不适用于关于历史交换量的分析问题。**"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.2"
  homepage: "https://web3.okx.com"
---
# OKX DEX Aggregator CLI

这是一个用于多链交易聚合的工具，提供了5个核心命令：报价、审批和执行交易。

## 预执行检查

在运行任何`onchainos`命令之前，请务必按照以下步骤操作。不要将常规命令的输出显示给用户，仅在安装、更新或处理错误时提供简短的状态更新：

1. **确认已安装**：运行`which onchainos`。如果未找到，请根据以下链接手动安装：[https://github.com/okx/onchainos-skills](https://github.com/okx/onchainos-skills)。
2. **检查更新**：读取`~/.onchainos/last_check`文件，并将其与当前时间戳进行比较：
   - 如果`cached_ts`非空且`(now - cached_ts) < 43200`（12小时），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时），运行安装程序以检查更新：
     如果安装了新版本，请告知用户并建议他们从[https://github.com/okx/onchainos-skills](https://github.com/okx/onchainos-skills)更新`onchainos`以获取最新功能。
3. 如果在此过程中任何`onchainos`命令因意外错误失败，请尝试重新安装后再继续。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可跳过此步骤）。

## 技能路由

- 查找代币信息 → 使用`okx-dex-token`
- 查看市场价格 → 使用`okx-dex-market`
- 广播交易 → 使用`okx-onchain-gateway`
- 查看钱包余额/投资组合 → 使用`okx-wallet-portfolio`

## 快速入门

### EVM交易聚合（报价 → 审批 → 执行）

### Solana交易聚合

## 支持的链名

该CLI支持人类可读的链名，并能自动解析它们：

| 链名 | 链索引 |
|---|---|
| XLayer | `196` |
| Solana | `501` |
| Ethereum | `1` |
| Base | `8453` |
| BSC | `56` |
| Arbitrum | `42161` |

## 原生代币地址

> **重要提示**：每个链都有特定的原生代币地址。使用错误的地址会导致交易失败。

| 链名 | 原生代币地址 |
|---|---|
| EVM（Ethereum、BSC、Polygon、Arbitrum、Base等） | `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee` |
| Solana | `11111111111111111111111111111111` |
| Sui | `0x2::sui::SUI` |
| Tron | `T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb` |
| Ton | `EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c` |

> **警告**：Solana的原生代币地址是`11111111111111111111111111111111`（系统程序地址），**切勿**使用`So111111111111111111111111111112`（wSOL代币地址），因为这是不同的代币，会导致交易失败。

## 命令索引

| 命令 | 描述 |
|---|---|
| 1 | `onchainos swap chains` | 获取DEX聚合器支持的链名 |
| 2 | `onchainos swap liquidity --chain <链名>` | 获取指定链上的可用流动性来源 |
| 3 | `onchainos swap approve --token ... --amount ... --chain ...` | 获取ERC-20代币的审批交易数据 |
| 4 | `onchainos swap quote --from ... --to ... --amount ... --chain ...` | 获取交易报价（仅限查看价格估算） |
| 5 | `onchainos swap swap --from ... --to ... --amount ... --chain ... --wallet ...` | 获取交易执行数据 |

## 跨技能工作流程

此技能是大多数用户交易流程的**执行端点**，几乎总是需要先从其他技能获取输入数据。

### 工作流程A：按代币名称进行完整交易（最常见）

> 用户：“在Solana上将1 SOL兑换成BONK”

### 数据传递：

- 第1步中的`tokenContractAddress` → 第2-3步中的`--to`参数
- SOL的原生地址 `11111111111111111111111111111111` → 使用`--from`参数
- 交易金额 `1 SOL` → 使用`--amount`参数（以最小单位表示）

### 工作流程B：需要审批的EVM交易

> 用户：“在XLayer上将100 USDC兑换成OKB”

### 工作流程C：先比较报价再执行

## 交易流程

### EVM链（XLayer、Ethereum、BSC、Base等）

### Solana

## 操作流程

### 第1步：确定交易意图

- 查看报价 → 使用`onchainos swap quote`
- 执行交易 → 完整的交易流程（报价 → 审批 → 执行）
- 列出可用的DEX → 使用`onchainos swap liquidity`
- 审批代币 → 使用`onchainos swap approve`

### 第2步：收集参数

- 如果缺少链名，建议使用XLayer（`--chain xlayer`，Gas费用低，确认速度快），然后询问用户偏好哪个链
- 如果缺少代币地址，使用`okx-dex-token`和`onchainos token search`来查找地址
- 如果缺少交易金额，询问用户并提醒将其转换为最小单位
- 如果缺少滑点率，建议使用1%作为默认值；对于波动性较大的代币，建议使用3-5%
- 如果缺少钱包地址，询问用户

### 第3步：执行交易

- **报价阶段**：调用`onchainos swap quote`，显示预估结果
  - 预计输出、Gas费用估算、价格影响、路由路径
  - 检查`isHoneyPot`和`taxRate`，向用户展示安全信息
- **审批阶段**：等待用户批准后再继续
- **审批阶段**（仅适用于EVM链）：在出售非原生代币时检查/执行审批
- **执行阶段**：调用`onchainos swap swap`，返回交易数据以供用户签名

### 第4步：建议后续操作

在显示结果后，建议用户进行以下操作：

| 操作 | 建议 |
|---|---|
| 交易报价（尚未确认） | 1. 在决定前查看价格图表 → 使用`okx-dex-market` 2. 继续进行交易 → 继续审批和交易 |
| 交易成功执行 | 1. 查看收到的代币价格 → 使用`okx-dex-market` 2. 交易另一种代币 → 重新开始交易流程 |
| 查询流动性 | 1. 获取交易报价 → 使用`onchainos swap quote` |

以对话式的方式与用户交流，例如：“交易已完成！您想查看更新后的余额吗？”——切勿向用户透露技能名称或端点路径。

## CLI命令参考

### 1. `onchainos swap chains`

获取DEX聚合器支持的链名。无需参数。

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `chainIndex` | 字符串 | 链名标识符（例如 `"1"`、`501"` |
| `chainName` | 字符串 | 人类可读的链名 |
| `dexTokenApproveAddress` | 字符串 | 用于该链上代币审批的DEX路由地址 |

### 2. `onchainos swap liquidity`

获取指定链上的可用流动性来源。

**参数**：

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|---|
| `--chain` | 是 | - | 链名（例如 `ethereum`、`solana`、`xlayer` |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `id` | 字符串 | 流动性来源ID |
| `name` | 字符串 | 流动性来源名称（例如 `"Uniswap V3"`、`CurveNG"` |
| `logo` | 字符串 | 流动性来源的Logo链接 |

### 3. `onchainos swap approve`

获取ERC-20代币的审批交易数据。

**参数**：

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|---|
| `--token` | 是 | - | 需要审批的代币合约地址 |
| `--amount` | 是 | - | 交易金额（以最小单位表示） |
| `--chain` | 是 | - | 链名 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `data` | 字符串 | 审批的交易数据（十六进制格式） |
| `dexContractAddress` | 字符串 | 支付方地址（已编码在`data`中）**注意**：这不是交易的目标地址 |
| `gasLimit` | 字符串 | 审批交易的预估Gas费用 |
| `gasPrice` | 字符串 | 推荐的Gas费用 |

### 4. `onchainos swap quote`

获取交易报价（仅限查看价格估算）。

**参数**：

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|
| `--from` | 是 | - | 来源代币合约地址 |
| `--to` | 是 | - | 目标代币合约地址 |
| `--amount` | 是 | - | 交易金额（以最小单位表示） |
| `--chain` | 是 | - | 链名 |
| `--swap-mode` | 可选 | `exactIn` | 表示输入金额是否精确 |
| `exactIn` | 布尔值 | 是否输入金额必须精确 |
| `exactOut` | 布尔值 | 表示输出金额是否必须精确 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| `toTokenAmount` | 字符串 | 预计的输出金额（以最小单位表示） |
| fromTokenAmount | 字符串 | 输入金额（以最小单位表示） |
| estimateGasFee | 字符串 | 预估的Gas费用（以原生代币单位计） |
| tradeFee | 字符串 | 交易费用估算（以USD表示） |
| priceImpactPercent | 字符串 | 价格影响百分比（例如 `"0.05"`） |
| router | 字符串 | 使用的路由器类型 |
| dexRouterList[]` | 数组 | DEX的路由路径详情 |
| dexRouterList[].dexName | 字符串 | 路由中使用的DEX名称 |
| dexRouterList[].percentage | 字符串 | 通过该DEX路由的金额百分比 |
| fromToken.isHoneyPot | 布尔值 | 来源代币是否为“蜜罐”（无法出售） |
| fromToken.taxRate | 字符串 | 来源代币的买卖税率 |
| fromToken.decimal | 字符串 | 来源代币的小数位数 |
| fromToken.tokenUnitPrice | 字符串 | 来源代币的单位价格（以USD表示） |
| toToken.isHoneyPot | 布尔值 | 目标代币是否为“蜜罐”（无法出售） |
| toToken.taxRate | 字符串 | 目标代币的买卖税率 |
| toToken.decimal | 字符串 | 目标代币的小数位数 |
| toToken.tokenUnitPrice | 字符串 | 目标代币的单位价格（以USD表示） |

### 5. `onchainos swap swap`

执行交易（报价 → 审批 → 广播）。

**参数**：

| 参数 | 是否必需 | 默认值 | 描述 |
|---|---|---|
| `--from` | 是 | - | 来源代币合约地址 |
| `--to` | 是 | - | 目标代币合约地址 |
| `--amount` | 是 | - | 交易金额（以最小单位表示） |
| `--chain` | 是 | - | 链名 |
| `--wallet` | 是 | - | 用户的钱包地址 |
| `--slippage` | 可选 | `"1"` | 滑点容忍度（例如 `"1"` 表示1%） |
| `--swap-mode` | 可选 | `exactIn` | 表示输入金额是否必须精确 |

**返回字段**：

| 字段 | 类型 | 描述 |
|---|---|---|
| routerResult | 对象 | 与报价阶段的返回结果相同 |
| tx.from | 字符串 | 发送方地址 |
| tx.to | 字符串 | 交易的目标地址 |
| tx.data | 字符串 | 交易的数据（EVM使用十六进制格式，Solana使用base58格式） |
| tx.gas | 字符串 | 交易的Gas费用 |
| tx.gasPrice | 字符串 | 交易的Gas费用 |
| tx.value | 字符串 | 需要发送的原生代币金额（以最小单位表示） |
| tx.minReceiveAmount | 字符串 | 滑点后的最小接收金额（以最小单位表示） |
| tx.maxSpendAmount | 字符串 | 最大可花费金额（仅适用于`exactOut`模式） |
| tx.slippagePercent | 字符串 | 应用的滑点容忍度百分比 |

## 输入/输出示例

**用户输入：**“在XLayer上将100 USDC兑换成OKB”

**用户输入：**“XLayer上有哪些可用的DEX？”

## 边缘情况

- **滑点率过高（>5%）**：警告用户，建议拆分交易或调整滑点率
- **价格影响过大（>10%）**：强烈建议用户减少交易金额
- **涉及“蜜罐”代币**：`isHoneyPot`为`true`时，阻止交易并警告用户
- **涉及征税代币**：`taxRate`非零时，向用户显示税率（例如5%）
- **余额不足**：先检查余额，显示当前余额，建议用户调整交易金额
- **不支持`exactOut`模式**：仅适用于Ethereum/Base/BSC/Arbitrum链，提示用户使用`exactIn`模式
- **Solana的原生代币地址**：必须使用`11111111111111111111111111111111`（系统地址），**切勿**使用`So1111111111111111111111111111112`（wSOL地址）
- **网络错误**：重试一次，然后提示用户稍后再试
- **地区限制（错误代码50125或80001）**：不要直接向用户显示原始错误代码，而是显示友好提示：`⚠️ 该服务在您所在的地区不可用。请切换到支持的地区后再试。`

## 注意事项

- 输入/输出金额以用户界面显示的单位为准（例如 `1.5 ETH`、`3,200 USDC`）
- CLI内部参数使用最小单位（例如 `1 USDC` 对应 `"1000000"`，`1 ETH` 对应 `"1000000000000000000"`）
- Gas费用以USD表示
- `minReceiveAmount` 以用户界面单位和USD两种格式显示
- 价格影响以百分比表示

## 其他注意事项

- 交易金额必须以**最小单位**（wei/lamport）表示
- `exactOut`模式仅适用于Ethereum（`1`）、Base（`8453`）、BSC（`56`）、Arbitrum（`42161`）
- 必须检查`isHoneyPot`和`taxRate`，并向用户展示安全信息
- EVM合约地址必须全部使用小写
- CLI会自动解析链名（例如 `ethereum` → `1`，`solana` → `501`）
- CLI通过环境变量处理身份验证——详见“预执行检查”步骤中的默认值设置