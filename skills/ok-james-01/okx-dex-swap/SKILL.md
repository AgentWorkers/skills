---
name: okx-dex-swap
description: "此技能应在用户提出以下请求时使用：  
- “交换代币”  
- “用OKB兑换USDC”  
- “购买代币”  
- “出售代币”  
- “交易加密货币”  
- “转换代币”  
- “用SOL兑换USDC”  
- “获取交换报价”  
- “执行交易”  
- “寻找最佳交换路径”  
- “最便宜的交换方式”  
- “最优交换方案”  
- “比较交换费率”  
- 或者提及在XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon以及20多个支持的交易链上进行代币的交换、交易、购买或出售操作。  
该技能会从500多个去中心化交易所（DEX）中聚合流动性数据，以提供最优的交换路径和价格。同时支持滑点控制、价格影响保护以及跨交易所路径优化功能。  
**注意：**  
- 请勿将此技能用于与交换代码相关的一般编程问题，也不适用于关于历史交换量的分析性查询。"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.1"
  homepage: "https://web3.okx.com"
---
# OKX DEX Aggregator CLI

这是一个用于多链交易聚合的工具，提供了5个核心命令：报价（quote）、批准（approve）和执行（execute）。

## 预运行检查

在运行任何`onchainos`命令之前，请务必按照以下步骤操作。不要将常规命令的输出显示给用户，仅在安装、更新或处理错误时提供简短的状态更新：

1. **确认已安装**：运行`which onchainos`。如果未找到该命令，请根据以下链接手动安装：[https://github.com/okx/onchainos-skills](https://github.com/okx/onchainos-skills)。
2. **检查更新**：读取`~/.onchainos/last_check`文件，并将其与当前时间戳进行比较：
   - 如果`cached_ts`非空且`(now - cached_ts) < 43200`（12小时内），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时），运行安装程序以检查更新：
     如果安装了新版本，请告知用户，并建议他们从[https://github.com/okx/onchainos-skills](https://github.com/okx/onchainos-skills)更新`onchainos`以获取最新功能。
3. 如果在此过程中任何`onchainos`命令因意外错误失败，请尝试重新安装后再继续。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可以跳过此步骤）。

## 技能路由

- 要搜索代币，请使用`okx-dex-token`。
- 要查询市场价格，请使用`okx-dex-market`。
- 要广播交易，请使用`okx-onchain-gateway`。
- 要查看钱包余额/投资组合，请使用`okx-wallet-portfolio`。

## 快速入门

### EVM交易聚合（报价 → 批准 → 执行）

### Solana交易聚合

## 支持的链名称

该CLI支持人类可读的链名称，并能自动解析这些名称：

| 链名称 | 链索引 |
| --- | --- |
| XLayer | `196` |
| Solana | `501` |
| Ethereum | `1` |
| Base | `8453` |
| BSC | `56` |
| Arbitrum | `42161` |

## 原生代币地址

> **重要提示**：每个链都有特定的原生代币地址。使用错误的地址会导致交易失败。

| 链名称 | 原生代币地址 |
| --- | --- |
| EVM（Ethereum、BSC、Polygon、Arbitrum、Base等） | `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee` |
| Solana | `11111111111111111111111111111111` |
| Sui | `0x2::sui::SUI` |
| Tron | `T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb` |
| Ton | `EQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM9c` |

> **警告**：Solana的原生代币地址是`11111111111111111111111111111111`（系统程序地址），**切勿**使用`So11111111111111111111111111112`（wSOL代币地址），因为这是不同的代币，会导致交易失败。

## 命令索引

| 命令编号 | 命令 | 描述 |
| --- | --- |
| 1 | `onchainos swap chains` | 获取DEX聚合器支持的链列表 |
| 2 | `onchainos swap liquidity --chain <链名称>` | 获取指定链上的可用流动性来源 |
| 3 | `onchainos swap approve --token ... --amount ... --chain ...` | 获取ERC-20代币的批准交易数据 |
| 4 | `onchainos swap quote --from ... --to ... --amount ... --chain ...` | 获取交易报价（仅限查看价格预估） |
| 5 | `onchainos swap swap --from ... --to ... --amount ... --chain ... --wallet ...` | 获取交易执行数据 |

## 跨技能工作流程

此技能是大多数用户交易流程的**执行端点**，几乎总是需要先从其他技能获取输入数据。

### 工作流程A：按代币名称进行完整交易（最常见）

> 用户：在Solana上将1个SOL兑换成BONK

**数据传递**：
- 第1步中的`tokenContractAddress` → 第2-3步中的`--to`参数
- SOL的原生地址 `11111111111111111111111111111111` → `--from`参数
- 交易金额 `1 SOL` → `--amount`参数（单位为最小单位）

### 工作流程B：需要批准的EVM交易

> 用户：在XLayer上将100个USDC兑换成OKB

**注意**：EVM代币（非原生OKB）需要执行批准操作。如果用户出售的是原生代币，则可以跳过此步骤。

### 先报价再执行

## 交易流程

### EVM链（XLayer、Ethereum、BSC、Base等）

### Solana

## 操作流程

### 第1步：确定交易意图

- 查看报价 → 使用`onchainos swap quote`
- 执行交易 → 完整的交易流程（报价 → 批准 → 执行）
- 列出可用的DEX → 使用`onchainos swap liquidity`
- 批准代币 → 使用`onchainos swap approve`

### 第2步：收集参数

- 如果缺少链名称，建议使用XLayer（`--chain xlayer`，Gas费用较低，确认速度快），然后询问用户偏好使用哪个链。
- 如果缺少代币地址，使用`okx-dex-token`和`onchainos token search`来获取地址。
- 如果缺少交易金额，询问用户并提醒其转换为最小单位。
- 如果缺少滑点设置，建议使用1%作为默认值；对于波动性较大的代币，建议使用3-5%。
- 如果缺少钱包地址，询问用户。

### 第3步：执行交易

- **报价阶段**：调用`onchainos swap quote`，显示预估结果：
  - 预计输出、Gas费用估算、价格影响、路由路径
  - 检查`isHoneyPot`和`taxRate`，向用户展示安全信息
- **确认阶段**：等待用户批准后再继续
- **批准阶段**（仅适用于EVM链）：检查/执行批准操作（如果出售的是非原生代币）
- **执行阶段**：调用`onchainos swap swap`，返回交易数据以供用户签名

### 第4步：建议后续操作

在显示结果后，建议用户采取以下2-3个操作：

| 操作 | 建议 |
| --- | --- |
| 交易报价（尚未确认） | 1. 在确认前查看价格图表 → 使用`okx-dex-market` | 2. 继续执行交易 → 使用`onchainos swap` |
| 交易成功执行 | 1. 查看收到的代币价格 → 使用`okx-dex-market` | 2. 进行下一次交易 → 使用`onchainos swap` |
| 查询流动性 | 1. 获取交易报价 → 使用`onchainos swap quote` |

以对话式的方式与用户交流，例如：“交易已完成！您是否想查看更新后的余额？”——切勿直接向用户透露技能名称或端点路径。

## CLI命令参考

### 1. `onchainos swap chains`

获取DEX聚合器支持的链列表。无需参数。

**返回字段**：
- `chainIndex`：字符串 | 链名称的标识符（例如 `"1"`、`501`）
- `chainName`：字符串 | 人类可读的链名称
- `dexTokenApproveAddress`：字符串 | 用于该链上代币批准的DEX路由地址

### 2. `onchainos swap liquidity`

获取指定链上的可用流动性来源。

**参数**：
- `--chain`：必填 | - | 链名称（例如 `ethereum`、`solana`、`xlayer`）

**返回字段**：
- `id`：字符串 | 流动性来源的ID
- `name`：字符串 | 流动性来源的名称（例如 `"Uniswap V3"`、`CurveNG`）
- `logo`：字符串 | 流动性来源的Logo链接

### 3. `onchainos swap approve`

获取ERC-20代币的批准交易数据。

**参数**：
- `--token`：必填 | - | 需要批准的代币合约地址
- `--amount`：必填 | 交易金额（单位为最小单位）
- `--chain`：必填 | 链名称

**返回字段**：
- `data`：字符串 | 批准交易的Calldata（十六进制格式）
- `dexContractAddress`：字符串 | 支付方地址（已编码在`data`中，**不是`tx.to`字段**）
- `gasLimit`：字符串 | 批准交易的预估Gas费用上限
- `gasPrice`：字符串 | 推荐的Gas费用

### 4. `onchainos swap quote`

获取交易报价（仅限查看价格预估）。

**参数**：
- `--from`：必填 | - | 来源代币合约地址
- `--to`：必填 | 目标代币合约地址
- `--amount`：必填 | 交易金额（单位为最小单位）
- `--chain`：必填 | 链名称
- `--swap-mode`：可选 | `exactIn` 或 `exactOut`（指定交易方式）

**返回字段**：
- `toTokenAmount`：字符串 | 预计的输出金额（单位为最小单位）
- `fromTokenAmount`：输入金额（单位为最小单位）
- `estimateGasFee`：字符串 | 预估的Gas费用（以原生代币单位计）
- `tradeFee`：字符串 | 交易费用估算（以USD计）
- `priceImpactPercent`：字符串 | 价格影响百分比（例如 `"0.05"`）
- `router`：字符串 | 使用的路由器类型
- `dexRouterList[]`：数组 | 交易路由路径详情
- `dexRouterList[].dexName`：数组中的DEX名称
- `dexRouterList[].percentage`：通过该DEX路由的金额百分比
- `fromToken.isHoneyPot`：布尔值 | 来源代币是否为“蜜罐”（无法出售）
- `fromToken.taxRate`：字符串 | 来源代币的买卖税率
- `fromToken.decimal`：字符串 | 来源代币的小数位数
- `fromToken.tokenUnitPrice`：字符串 | 来源代币的单位价格（以USD计）
- `toToken.isHoneyPot`：布尔值 | 目标代币是否为“蜜罐”（无法出售）
- `toToken.taxRate`：字符串 | 目标代币的买卖税率
- `toToken.decimal`：字符串 | 目标代币的小数位数
- `toToken.tokenUnitPrice`：字符串 | 目标代币的单位价格（以USD计）

### 5. `onchainos swap swap`

执行交易（包括报价、签名和广播）。

**参数**：
- `--from`：必填 | 来源代币合约地址
- `--to`：必填 | 目标代币合约地址
- `--amount`：交易金额（单位为最小单位）
- `--chain`：必填 | 链名称
- `--wallet`：必填 | 用户的钱包地址
- `--slippage`：可选 | 滑点容忍度（百分比，例如 `1` 表示1%）
- `--swap-mode`：可选 | `exactIn` 或 `exactOut`（指定交易方式）

**返回字段**：
- `routerResult`：对象 | 与报价阶段返回的字段结构相同
- `tx.from`：字符串 | 发送交易的发送方地址
- `tx.to`：字符串 | 交易的目标合约地址
- `tx.data`：交易的数据（EVM链使用十六进制格式，Solana链使用Base58格式）
- `tx.gas`：交易的Gas费用上限
- `tx.gasPrice`：交易的Gas费用
- `tx.value`：要发送的原生代币金额（单位为最小单位）
- `tx.minReceiveAmount`：交易完成后可能收到的最小金额（单位为最小单位）
- `tx.maxSpendAmount`：`exactOut`模式下允许的最大支出金额
- `tx.slippagePercent`：应用的滑点容忍度百分比

## 输入/输出示例

**用户输入**：“在XLayer上将100个USDC兑换成OKB。”

**用户输入**：“XLayer上有哪些可用 的DEX？”

## 边缘情况处理**

- **滑点过高（>5%）**：警告用户，建议分次交易或调整滑点设置。
- **价格影响过大（>10%）**：强烈建议用户减少交易金额。
- **代币为“蜜罐”（`isHoneyPot = true`）**：阻止交易并向用户发出警告。
- **涉及税收的代币**：显示税率（例如5%的买入税）。
- **余额不足**：先检查余额，再提示用户调整交易金额。
- **不支持`exactOut`模式**：仅适用于Ethereum、Base、BSC、Arbitrum链，此时提示用户使用`exactIn`模式。
- **Solana的原生代币地址**：必须使用`11111111111111111111111111111111`，**切勿**使用`So11111111111111111111111111112`（wSOL代币地址）。
- **网络错误**：尝试一次后提示用户稍后再试。
- **地区限制（错误代码50125或80001）**：不要直接向用户显示原始错误代码，而是显示友好提示：“⚠️ 该服务在您所在的地区不可用。请切换到支持的地区后再试。”

## 金额显示规则

- 用户界面中的金额以特定单位显示（例如 `1.5 ETH`、`3,200 USDC`）。
- CLI内部参数使用最小单位（例如 `1 USDC` 表示 `1000000`，`1 ETH` 表示 `1000000000000000000`）。
- Gas费用以USD为单位显示。
- `minReceiveAmount` 既以用户界面单位显示，也以USD显示。
- 价格影响以百分比形式显示。

## 其他注意事项

- 交易金额必须以**最小单位**表示（例如wei或lamports）。
- `exactOut`模式仅适用于Ethereum（`1`）、Base（`8453`）、BSC（`56`）、Arbitrum（`42161`）链。
- 必须检查`isHoneyPot`和`taxRate`，并向用户展示相关安全信息。
- EVM链的合约地址必须全部使用小写。
- CLI会自动解析链名称（例如 `Ethereum` 显示为 `1`，`Solana` 显示为 `501`）。
- CLI通过环境变量处理身份验证——详情请参见“先决条件”部分。