---
name: okx-onchain-gateway
description: "当用户请求“广播交易”、“发送交易”、“估算交易费用”、“模拟交易”、“检查交易状态”、“追踪我的交易”、“获取交易费用”、“设置交易费用上限”、“广播已签名的交易”，或涉及交易广播、链上交易发送、交易费用估算、交易模拟、交易订单追踪或交易状态检查等操作时，应使用此技能。该技能支持在 XLayer、Solana、Ethereum、Base、BSC、Arbitrum、Polygon 以及 20 多个其他区块链平台上进行交易费用估算、交易模拟、交易广播和订单追踪。请勿将其用于交换报价或执行操作（请使用 okx-dex-swap）；同时，也不适用于关于交易处理的一般性编程问题。"
license: Apache-2.0
metadata:
  author: okx
  version: "1.0.1"
  homepage: "https://web3.okx.com"
---
# OKX Onchain Gateway CLI

该CLI提供了6个命令，用于估算交易手续费（gas）、模拟交易、广播交易以及追踪交易状态。

## 前置检查

在运行任何`onchainos`命令之前，请务必按照以下步骤进行操作。不要将常规命令的输出显示给用户，仅在安装、更新或处理错误时提供简短的状态更新：

1. **确认已安装**：运行`which onchainos`。如果未找到该命令，请根据以下链接手动安装：https://github.com/okx/onchainos-skills
2. **检查更新**：读取`~/.onchainos/last_check`文件，并将其与当前时间戳进行比较：
   - 如果`cached_ts`非空且`(now - cached_ts) < 43200`（12小时内），则跳过更新并继续执行。
   - 否则（文件缺失或超过12小时），运行安装程序以检查更新：
   - 如果安装了新版本，请告知用户并建议他们从https://github.com/okx/onchainos-skills更新他们的onchainos技能，以获取最新功能。
3. 如果在此过程中任何`onchainos`命令因意外错误失败，请尝试重新安装后再继续操作。
4. 在项目根目录下创建一个`.env`文件以覆盖默认的API凭据（可选——快速启动时可以跳过此步骤）。

## 技能路由

- 用于查询和执行交易对价：使用`okx-dex-swap`
- 用于查询市场价格：使用`okx-dex-market`
- 用于查询代币信息：使用`okx-dex-token`
- 用于查询钱包余额/投资组合：使用`okx-wallet-portfolio`
- 用于广播交易：使用`okx-onchain-gateway`

## 快速入门

（此处应包含快速入门的详细步骤或示例）

## 支持的链名称

该CLI支持人类可读的链名称，并能自动解析这些名称：

| 链名称 | 链索引 |
|---|---|
| XLayer | `196` |
| Solana | `501` |
| Ethereum | `1` |
| Base | `8453` |
| BSC | `56` |
| Arbitrum | `42161` |

## 命令索引

| 命令 | 描述 |
|---|---|
| `onchainos gateway chains` | 获取支持的链名称 |
| `onchainos gateway gas --chain <链名称>` | 获取指定链的当前手续费价格 |
| `onchainos gateway gas-limit --from ... --to ... --chain ...` | 估算交易的手续费上限 |
| `onchainos gateway simulate --from ... --to ... --data ... --chain ...` | 模拟交易（预测试） |
| `onchainos gateway broadcast --signed-tx ... --address ... --chain ...` | 广播已签名的交易 |
| `onchainos gateway orders --address ... --chain ...` | 追踪已广播的交易状态 |

## 跨技能工作流程

该CLI负责将已签名的交易发送到链上。它与`okx-dex`技能配合使用，以获取交易数据：

### 工作流程A：交易对价 → 广播 → 追踪

> 用户：“将1 ETH兑换成USDC并广播”

**数据传递**：
- 从`okx-dex-swap`获取`tx.data`、`tx.to`、`tx.value`、`tx.gas` → 用户构建并签名交易 → 使用`--signed-tx`进行广播
- 从广播结果中获取`orderId` → 用于在`okx-onchain-gateway`中查询交易状态

### 工作流程B：模拟 → 广播 → 追踪

> 用户：“先模拟交易，确认无误后再广播”

### 工作流程C：检查手续费 → 交易对价 → 广播

> 用户：“先检查手续费，然后进行交易对价”

## 操作流程

### 第1步：确定操作意图

- 估算链的手续费：`onchainos gateway gas`
- 估算交易的手续费上限：`onchainos gateway gas-limit`
- 测试交易是否可行：`onchainos gateway simulate`
- 广播已签名的交易：`onchainos gateway broadcast`
- 追踪已广播的交易：`onchainos gateway orders`
- 查看支持的链名称：`onchainos gateway chains`

### 第2步：收集参数

- 如果缺少链名称，建议使用XLayer（手续费较低，确认速度较快），然后询问用户选择的链名称
- 如果缺少`--signed-tx`参数，提醒用户先签名交易（该CLI不负责签名交易）
- 如果缺少钱包地址，询问用户提供地址
- 对于估算手续费或模拟交易，需要`--from`、`--to`参数（以及可选的`--data`参数）
- 对于查询交易状态，需要`--address`和`--chain`参数（以及可选的`--order-id`参数）

### 第3步：执行操作

- **估算手续费**：调用`onchainos gateway gas`或`gas-limit`，显示结果
- **模拟交易**：调用`onchainos gateway simulate`，检查是否成功
- **广播交易**：调用`onchainos gateway broadcast`并传入已签名的交易，返回`orderId`
- **追踪交易状态**：调用`onchainos gateway orders`，显示交易状态

### 第4步：建议后续操作

根据显示的结果，建议用户进行以下操作：

| 操作 | 建议 |
|---|---|
| 估算手续费 | 1. 估算特定交易的手续费上限 → `onchainos gateway gas-limit` |
| 获取交易对价 | 2. 查询交易对价 → `okx-dex-swap` |
| 模拟交易 | 1. 模拟交易 → `onchainos gateway simulate` |
| 广播交易 | 1. 广播交易 → `onchainos gateway broadcast` |
| 追踪交易状态 | 1. 查看交易状态 → `onchainos gateway orders` |

**提示方式**：以对话的形式与用户交流，避免直接展示技能名称或API端点路径。

## CLI命令参考

### 1. `onchainos gateway chains`

获取支持的链名称。无需参数。

**返回字段**：
- `chainIndex`：链的标识符（例如`"196"`、`"501"`）
- `name`：人类可读的链名称（例如`"Ethereum"`）
- `logoUrl`：链的Logo图片URL
- `shortName`：链的简称（例如`"ETH"`）

### 2. `onchainos gateway gas`

获取指定链的当前手续费价格。

**参数**：
- `--chain`：链名称（例如`"Ethereum"`、`"solana"`）

**返回字段**：
- `normal`：常规手续费价格
- `min`：最低手续费价格
- `max`：最高手续费价格
- `supporteip1559`：是否支持EIP-1559协议
- `eip1559Protocol.suggestBaseFee`：建议的基费
- `eip1559Protocol.baseFee`：当前基费
- `eip1559Protocol.proposePriorityFee`：建议的优先费
- `eip1559Protocol.safePriorityFee`：安全的优先费
- `eip1559Protocol.fastPriorityFee`：快速的优先费

### 3. `onchainos gateway gas-limit`

估算交易的手续费上限。

**参数**：
- `--from`：发送者地址
- `--to`：接收者/合约地址
- `--chain`：链名称
- `--amount`：转账金额（以最小单位表示）
- `--data`：合约交互所需的编码数据（hex格式）

**返回字段**：
- `gasLimit`：估算的手续费上限

### 4. `onchainos gateway simulate`

模拟交易（预测试）。

**参数**：
- `--from`：发送者地址
- `--to`：接收者/合约地址
- `--data`：合约交互所需的编码数据（hex格式）
- `--chain`：链名称
- `--amount`：转账金额（以最小单位表示）

**返回字段**：
- `intention`：交易意图
- `assetChange`：交易涉及的资产变动
- `assetChange[]`：资产变动的详细信息
- `gasUsed`：模拟过程中消耗的手续费
- `failReason`：失败原因（为空表示成功）
- `risks`：交易风险信息

### 5. `onchainos gateway broadcast`

广播已签名的交易。

**参数**：
- `--signed-tx`：已签名的交易数据（EVM格式为hex，Solana格式为base58）
- `--address`：发送者钱包地址
- `--chain`：链名称

**返回字段**：
- `orderId`：OKX的交易追踪ID
- `txHash`：链上的交易哈希

### 6. `onchainos gateway orders`

追踪已广播的交易状态。

**参数**：
- `--address`：钱包地址
- `--chain`：链名称
- `--order-id`：特定交易的ID

**返回字段**：
- `cursor`：下一页的页码
- `orders`：交易对象列表
- `orders[]`：交易对象
- `orders[].orderId`：OKX的交易追踪ID
- `orders[].txHash`：链上的交易哈希
- `orders[].chainIndex`：链的标识符
- `orders[].address`：钱包地址
- `orders[].txStatus`：交易状态（`1`表示待处理，`2`表示成功，`3`表示失败）
- `orders[].failReason`：失败原因（成功时为空）

## 输入/输出示例

**用户输入：**“XLayer链的当前手续费是多少？”
**输出：**“XLayer链的当前手续费价格为18.5 Gwei。”

**用户输入：**“在发送交易之前，先模拟一下这个交易对价。”
**输出：**“已成功模拟交易对价。”

**用户输入：**“广播我的已签名交易。”
**输出：**“交易已成功广播。”

**用户输入：**“查看我的交易状态。”
**输出：**“您的交易已成功广播，您可以查看其状态。”

## 边缘情况**

- **MEV保护**：通过OKX节点广播交易可能在支持的链上提供MEV保护。
- **Solana的特殊处理**：Solana链上的已签名交易使用`base58`编码格式（而非hex格式），请确保`--signed-tx`参数正确。
- **链不支持**：首先调用`onchainos gateway chains`确认链是否支持。
- **节点返回错误**：可能是由于手续费不足、nonce值过低或合约回滚等原因导致交易失败。请使用正确的参数重试。
- **钱包地址格式不匹配**：地址格式可能与链不兼容（例如，在Solana链上使用EVM地址）。
- **网络错误**：尝试一次后提示用户稍后再试。
- **地区限制（错误代码50125或80001）**：不要直接向用户显示原始错误代码，而是显示友好提示：“⚠️ 该服务在您的地区不可用。请切换到支持的地区后再试。”
- **交易已广播**：如果相同的`--signed-tx`被多次广播，API可能会返回错误或相同的`txHash`，此时应忽略重复请求。

## 显示规则

- EVM链的手续费以Gwei为单位（例如18.5 Gwei），不显示原始wei值。
- 手续费上限以整数形式显示（例如21000、145000）。
- 尽可能以USD为单位显示手续费成本。
- 交易金额在用户界面中以相应单位显示（例如1.5 ETH）。

## 其他注意事项

- 该CLI不负责签名交易，仅负责广播已签名的交易。
- 参数中的金额以最小单位（wei/lamports）表示。
- 对于支持EIP-1559协议的链，手续费字段使用`eip1559Protocol.suggestBaseFee`和`proposePriorityFee`；对于传统链，使用`normal`字段。
- EVM合约地址必须全部使用小写。
- CLI会自动解析链名称（例如`Ethereum`显示为`1`，`Solana`显示为`501`）。
- CLI通过环境变量处理认证信息——具体设置请参见“前置检查”部分。