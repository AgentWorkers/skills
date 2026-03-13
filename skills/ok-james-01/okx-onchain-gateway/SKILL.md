---
name: okx-onchain-gateway
description: "此技能适用于用户请求执行以下操作的情况：广播交易（broadcast transaction）、发送交易（send tx）、估算交易所需的气体费用（estimate gas）、模拟交易（simulate transaction）、检查交易状态（check tx status）、追踪自己的交易（track my transaction）、获取气体费用（get gas price）、设置气体费用上限（gas limit）、广播已签名的交易（broadcast signed tx），或涉及交易广播、链上交易发送、气体费用估算、交易模拟、交易追踪等相关操作。该技能支持在 XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon 以及 20 多个其他区块链平台上使用。请勿将其用于交换报价或交易执行相关操作（请使用 okx-dex-swap）；同时，也不适用于关于交易处理的一般性编程问题。"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.2"
  homepage: "https://web3.okx.com"
---
# OKX Onchain Gateway CLI

提供了6个命令，用于估算交易手续费（gas）、模拟交易、广播交易以及追踪交易状态。

## 预运行检查

在运行任何`onchainos`命令之前，请务必按照以下步骤操作。不要向用户显示常规命令的输出；仅在安装、更新或处理失败时提供简短的状态更新：

1. **确认已安装**：运行`which onchainos`。如果未找到该命令，请根据以下链接手动安装：https://github.com/okx/onchainos-skills
2. **检查更新**：读取`~/.onchainos/last_check`文件，并将其与当前时间戳进行比较：
   - 如果`cached_ts`非空且`(now - cached_ts) < 43200`（12小时内），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时），运行安装程序以检查更新：
     如果安装了新版本，请告知用户，并建议他们从https://github.com/okx/onchainos-skills更新他们的onchainos技能包以获取最新功能。
3. 如果在此过程中任何`onchainos`命令因意外错误而失败，请尝试重新安装后再继续。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可跳过此步骤）。

## 技能路由

- 用于交换报价和执行交易：使用`okx-dex-swap`
- 用于查询市场价格：使用`okx-dex-market`
- 用于搜索代币：使用`okx-dex-token`
- 用于查看钱包余额/投资组合：使用`okx-wallet-portfolio`
- 用于广播交易：使用`okx-onchain-gateway`

## 快速入门

（此处应包含快速入门的详细步骤或示例）

## 支持的链名称

该CLI支持人类可读的链名称，并能自动解析这些名称。

| 链名称 | 链ID | 链索引 |
|---|---|---|
| XLayer | `xlayer` | `196` |
| Solana | `solana` | `501` |
| Ethereum | `ethereum` | `1` |
| Base | `base` | `8453` |
| BSC | `bsc` | `56` |
| Arbitrum | `arbitrum` | `42161` |

## 命令索引

| 命令编号 | 命令 | 描述 |
|---|---|---|
| 1 | `onchainos gateway chains` | 获取支持的链名称 |
| 2 | `onchainos gateway gas --chain <链名称>` | 获取指定链的当前手续费价格 |
| 3 | `onchainos gateway gas-limit --from ... --to ... --chain ...` | 估算交易的手续费上限 |
| 4 | `onchainos gateway simulate --from ... --to ... --data ... --chain ...` | 模拟交易（预测试） |
| 5 | `onchainos gateway broadcast --signed-tx ... --address ... --chain ...` | 广播已签名的交易 |
| 6 | `onchainos gateway orders --address ... --chain ...` | 追踪已广播的交易状态 |

## 跨技能工作流程

此技能负责将已签名的交易发送到链上。它与`okx-dex`技能配合使用，以获取交易数据：

### 工作流程A：交换 → 广播 → 追踪

> 用户：“将1 ETH兑换成USDC并广播”

**数据传递**：
- 从`okx-dex-swap`获取`tx.data`、`tx.to`、`tx.value`、`tx.gas` → 用户构建并签名交易 → 使用`--signed-tx`进行广播
- 从广播结果中获取`orderId` → 用于在`onchainos gateway orders`中查询交易状态

### 工作流程B：模拟 → 广播 → 追踪

> 用户：“先模拟交易，确认无误后再广播”

### 工作流程C：检查手续费 → 交换 → 广播

> 用户：“先检查手续费，然后进行兑换”

## 操作流程

### 第一步：确定操作意图

- 估算链的手续费：`onchainos gateway gas`
- 估算交易的手续费上限：`onchainos gateway gas-limit`
- 测试交易是否可行：`onchainos gateway simulate`
- 广播已签名的交易：`onchainos gateway broadcast`
- 追踪已广播的交易：`onchainos gateway orders`
- 查看支持的链：`onchainos gateway chains`

### 第二步：收集参数

- 如果缺少链名称，建议使用XLayer（`--chain xlayer`，手续费较低，确认速度快），然后询问用户偏好哪个链
- 如果缺少`--signed-tx`参数，提醒用户先签名交易（此CLI不负责签名交易）
- 如果缺少钱包地址，询问用户提供地址
- 对于估算手续费或模拟交易，需要`--from`、`--to`参数（以及可选的`--data`参数）
- 对于查询交易状态，需要`--address`和`--chain`参数

### 第三步：执行操作

- **估算手续费**：调用`onchainos gateway gas`或`gas-limit`，显示结果
- **模拟交易**：调用`onchainos gateway simulate`，检查是否成功
- **广播交易**：调用`onchainos gateway broadcast`并传入已签名的交易，返回`orderId`
- **追踪交易状态**：调用`onchainos gateway orders`，显示交易状态

### 第四步：建议下一步操作

根据显示的结果，建议用户进行以下操作：

| 操作 | 建议 |
|---|---|
| 估算手续费 | 1. 估算特定交易的手续费上限 → `onchainos gateway gas-limit` |
| 获取交换报价 | 2. 使用`okx-dex-swap`进行交易 |
| 模拟交易 | 1. 模拟交易 → `onchainos gateway simulate` |
| 广播交易 | 2. 广播交易 → `onchainos gateway broadcast` |
| 追踪交易状态 | 1. 查看交易状态 → `onchainos gateway orders` |

**交互式提示**：
- 以对话的方式与用户交流，例如：“交易已广播！您是否需要追踪订单状态？”
- 绝不要直接向用户展示技能名称或API端点路径。

## CLI命令参考

### 1. `onchainos gateway chains`

获取支持的链名称。无需参数。

**返回字段**：
- `chainIndex`：字符串类型，表示链的标识符（例如`"196"`、`"501"`等）
- `name`：字符串类型，表示人类可读的链名称（例如`"Ethereum"`）
- `logoUrl`：字符串类型，表示链的Logo图片URL
- `shortName`：字符串类型，表示链的简称（例如`"ETH"`）

### 2. `onchainos gateway gas`

获取指定链的当前手续费价格。

**参数**：
- `--chain`：必选参数，表示链名称（例如`"ethereum"`、`"solana"`等）

**返回字段**：
- `normal`：字符串类型，表示常规手续费价格
- `min`：字符串类型，表示最低手续费价格
- `max`：字符串类型，表示最高手续费价格
- `supporteip1559`：布尔值，表示是否支持EIP-1559协议
- `eip1559Protocol.suggestBaseFee`：字符串类型，表示建议的基础费用
- `eip1559Protocol.baseFee`：字符串类型，表示当前的基础费用
- `eip1559Protocol.proposePriorityFee`：字符串类型，表示建议的优先费用
- `eip1559Protocol.safePriorityFee`：字符串类型，表示安全的（较慢的）优先费用
- `eip1559Protocol.fastPriorityFee`：字符串类型，表示快速的优先费用

### 3. `onchainos gateway gas-limit`

估算交易的手续费上限。

**参数**：
- `--from`：必选参数，表示发送者地址
- `--to`：必选参数，表示接收者/合约地址
- `--chain`：必选参数，表示链名称
- `--amount`：可选参数，表示转账金额（以最小单位计）
- `--data`：可选参数，表示编码后的合约数据（十六进制格式）

**返回字段**：
- `gasLimit`：字符串类型，表示交易的预估手续费上限

### 4. `onchainos gateway simulate`

模拟交易（预测试）。

**参数**：
- `--from`：必选参数，表示发送者地址
- `--to`：必选参数，表示接收者/合约地址
- `--data`：必选参数，表示编码后的合约数据（十六进制格式）
- `--chain`：必选参数，表示链名称
- `--amount`：可选参数，表示转账金额（以最小单位计）

**返回字段**：
- `intention`：字符串类型，表示交易意图
- `assetChange[]`：数组类型，表示交易中的资产变动
- `assetChange[].symbol`：字符串类型，表示变动的代币符号
- `assetChange[].rawValue`：字符串类型，表示变动的代币数量
- `gasUsed`：字符串类型，表示模拟过程中消耗的手续费
- `failReason`：字符串类型，表示失败原因（空表示成功）
- `risks[]`：数组类型，表示交易风险信息

### 5. `onchainos gateway broadcast`

广播已签名的交易。

**参数**：
- `--signed-tx`：必选参数，表示已签名的交易数据（EVM格式为十六进制，Solana格式为base58）
- `--address`：必选参数，表示发送者钱包地址
- `--chain`：必选参数，表示链名称

**返回字段**：
- `orderId`：字符串类型，表示OKX的交易追踪ID（用于查询交易状态）
- `txHash`：字符串类型，表示链上的交易哈希值

### 6. `onchainos gateway orders`

追踪已广播的交易状态。

**参数**：
- `--address`：必选参数，表示钱包地址
- `--chain`：必选参数，表示链名称
- `--order-id`：可选参数，表示具体的交易ID（来自广播响应）

**返回字段**：
- `cursor`：字符串类型，表示下一页的页码
- `orders[]`：数组类型，表示交易对象列表
- `orders[].orderId`：字符串类型，表示OKX的交易追踪ID
- `orders[].txHash`：字符串类型，表示链上的交易哈希值
- `orders[].chainIndex`：字符串类型，表示链的标识符
- `orders[].address`：字符串类型，表示钱包地址
- `orders[].txStatus`：字符串类型，表示交易状态（`1`表示待处理，`2`表示成功，`3`表示失败）
- `orders[].failReason`：字符串类型，表示失败原因（成功时为空）

## 输入/输出示例

**用户输入：**“XLayer链的当前手续费是多少？”
**输出：**“XLayer链的当前手续费价格为18.5 Gwei。”

**用户输入：**“在发送交易之前，先模拟一下这个交易。”
**输出：**“已成功模拟交易。”

**用户输入：**“广播我的已签名交易。”
**输出：**“交易已成功广播。”

**用户输入：**“查看我的交易状态。”
**输出：**“您的交易状态为：待处理。”

## 边缘情况处理**

- **MEV保护**：通过OKX节点广播交易可能在支持的链上提供MEV保护。
- **Solana的特殊处理**：Solana链上的已签名交易使用`base58`编码格式（而非十六进制格式）。请确保`--signed-tx`参数的格式正确。
- **链不支持**：首先调用`onchainos gateway chains`进行验证。
- **节点返回失败**：可能是由于手续费不足、nonce值过低或合约回滚等原因导致的。请使用正确的参数重新尝试。
- **钱包地址格式不匹配**：地址格式可能与链不兼容（例如，在Solana链上使用EVM地址）。
- **网络错误**：尝试一次后，提示用户稍后再试。
- **地区限制（错误代码50125或80001）**：不要直接向用户显示原始错误代码，而是显示友好提示：“⚠️ 该服务在您的地区不可用。请切换到支持的地区后再试。”
- **交易已广播**：如果相同的`--signed-tx`被多次广播，API可能会返回错误或相同的`txHash`，请忽略重复的请求。

## 显示规则

- EVM链的手续费以Gwei为单位（例如18.5 Gwei），不显示原始的wei单位
- 手续费上限以整数形式显示（例如21000、145000）
- 尽可能以USD为单位显示手续费成本
- 交易金额以UI可读的单位显示（例如1.5 ETH）

## 全局注意事项

- 该CLI不负责签名交易，仅负责广播已签名的交易
- 参数中的金额以最小单位（wei或lamports）表示
- 对于支持EIP-1559协议的链，手续费字段使用`eip1559Protocol.suggestBaseFee`和`proposePriorityFee`；对于传统链，使用`normal`字段
- EVM合约地址必须全部使用小写
- CLI会自动解析链名称（例如`ethereum`显示为`1`，`solana`显示为`501`）
- CLI通过环境变量处理身份验证（详见“先决条件”部分）