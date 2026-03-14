---
name: crypto-treasury-ops
description: 为 OpenClaw 代理提供安全的管理 EVM（以太坊虚拟机）资金库操作及原生 Hyperliquid 交易服务，包括钱包余额查询、受保护的代币转移、跨链 USDC 桥接、Hyperliquid 存款、目标地址的Gas费用补充、交易安全性保障以及结构化的报价功能。
---
# crypto-treasury-ops

当 OpenClaw 代理需要以严格的安全控制措施检查或操作以太坊（Ethereum）、Polygon、Arbitrum 或 Base 上的 treasury 钱包，或读取 Solana 账户余额时，请使用此技能。

## 该技能的功能

- 检查原生稳定币和配置的稳定币余额
- 检查 Solana 的原生 SOL 代币以及配置的 SPL 代币余额
- 在同一链路上转移原生资产或 ERC-20 代币
- 通过可插拔的提供者层在链路上桥接代币
- 将 USDC 存入 Hyperliquid，支持 Arbitrum 直接转账以及 Polygon/Base 的路由
- 读取 Hyperliquid 永续合约的市场状态和账户状态
- 下单、保护或取消 Hyperliquid 永续合约订单
- 在执行前评估 treasury 的安全策略
- 返回结构化的 JSON 数据，以便下游代理可靠地使用

## 运行时合约

在执行构建或运行之前，需要配置环境变量。

**所需变量：**

**推荐的工作流程：**

**重要提示：**

- `TREASURY_PRIVATE_KEY` 是 `transfer_token`、`bridge_token`、`deposit_to_hyperliquid`、`place_hyperliquid_order`、`protect_hyperliquid_position` 和 `cancel_hyperliquid_order` 操作所必需的。
- `ZEROX_API_KEY` 是 `swap_token` 和交换报价所必需的。
- `HYPERLIQUID_TRADING_*` 变量可以进一步限制市场允许列表、订单名义金额、杠杆率和确认阈值。
- 该技能内置了以太坊（Ethereum）、Polygon、Arbitrum、Base 和 Solana 的 RPC URL 列表作为备用方案。
- 如 `ETHEREUM_RPC_URL` 和 `SOLANA_RPC_URL` 等 RPC 环境变量可以自定义；支持逗号分隔的列表。
- `get_balances`、`get_hyperliquid_market_state`、`get_hyperliquid_account_state`、`safety_check` 等操作无需签名者即可执行。
- 请勿在工具输入的 JSON 中传递私钥；该技能仅从环境中读取私钥。
- 在生产环境中，建议使用保管库（vault）、KMS、HSM 或委托签名者，而不是直接在 `.env` 文件中存储私钥。
- 对于会改变状态的 treasury 操作，在执行前请先运行 `quote_operation` 或设置 `dryRun=true`，以确保路由和余额是最新的。

**通过 CLI 调用工具：**

## 工具

### `get_balances`

**输入：**
- `walletAddress`
- `chain`
- 当 `chain=solana` 时，`solanaAddress` 是可选的

**返回：**
- 原生余额
- 该链路上配置的稳定币余额
- 代币符号、小数位数、原始金额和人类可读的金额

**备注：**
- 当 `chain=solana` 时，支持只读余额查询。
- 该技能不支持 Solana 的执行流程。

### `transfer_token`

**输入：**
- `chain`
- `token`
- `recipient`
- `amount`
- `approval` 是可选的
- `dryRun` 是可选的

**行为：**
- 验证接收者的格式
- 根据代币符号或地址解析接收者
- 在发送前检查钱包余额
- 估算所需的气体费用
- 执行安全策略检查
- 拒绝不安全或资金不足的转账
- 返回转账摘要和交易哈希

### `swap_token`

**输入：**
- `chain`
- `sellToken`
- `buyToken`
- `amount`
- `recipient` 是可选的
- `slippageBps` 是可选的
- `approval` 是可选的
- `dryRun` 是可选的

**行为：**
- 使用配置的交换提供者抽象层
- 首次实现使用 0x Swap API
- 仅支持 EVM ERC-20 代币的交换
- 拒绝原生气体代币（如 `ETH` 或 `POL`）的交换；请使用封装后的代币（如 `WETH`）
- 提供报价路径、最低接收金额、气体费用、允许金额和交易数据
- 在执行前检查 treasury 策略和气体储备
- 仅在批准和策略条件满足时执行

### `bridge_token`

**输入：**
- `sourceChain`
- `destinationChain`
- `token`
- `amount`
- `approval` 是可选的
- `dryRun` 是可选的

**行为：**
- 使用配置的桥接提供者抽象层
- 提供报价路径、费用、最低接收金额和交易数据
- 在执行前检查 treasury 策略、费用阈值和气体储备
- 仅在批准和策略条件满足时执行
- 返回路径摘要、交易状态和浏览器链接（如果可用）

### `deposit_to_hyperliquid`

**输入：**
- `sourceChain`
- `token`
- `amount`
- `destination`
- `approval` 是可选的
- `dryRun` 是可选的

**行为：**
- 仅支持 `USDC`
- 支持通过 Arbitrum 的直接转账，以及从 Polygon/Base 到 Arbitrum 再到 Hyperliquid 的转账
- 如果 Arbitrum 的气体费用不足，可以先储备源端的 USDC 然后桥接到 Arbitrum
- 这是一个多阶段流程：可以选择性地补充气体费用，先桥接到 Arbitrum，再将 Arbitrum 的 USDC 存入 Hyperliquid
- 如果桥接状态 API 不可靠但资金已经到账，该工具会尝试基于余额进行恢复
- 拒绝向与 treasury 签名者不同的 Hyperliquid 钱包进行转账
- 不支持来自 Solana 的转账或 `SOL` 代币
- Hyperliquid 可能支持通过 Unit 管理的流程进行 Solana 转账，但这些不在该技能的范围内
- 如果未满足最低存款或气体储备要求，将拒绝转账
- 返回桥接阶段、存款阶段和最终执行摘要

**推荐的代理工作流程：**
- 先调用 `quote_operation`
- 如果报价可行，再调用 `deposit_to_hyperliquid` 并设置 `dryRun=true`
- 之后再调用 `deposit_to_hyperliquid` 并设置 `dryRun=false`
- 如果部分桥接或补充后执行失败，请不要盲目重试原始金额
- 重新检查 `base/polygon` 和 `arbitrum` 的余额；如果需要重试，请再次运行 `quote_operation` 并使用剩余的源余额

### `get_hyperliquid_market_state`

**输入：**
- `market` 是可选的

**行为：**
- 返回 Hyperliquid 永续合约的实时元数据和上下文
- 如果省略了 `market`，则返回所有支持的永久合约列表
- 如果提供了 `market`，还会返回实时 L2 快照中的最佳买价/卖价
- 支持 `dex:COIN` 格式的 HIP-3 / builder dex 市场，例如 `xyz:GOLD`

### `get_hyperliquid_account_state`

**输入：**
- `user` 是可选的
- `dex` 是可选的

**行为：**
- 返回 Hyperliquid 永续合约账户的摘要信息
- 返回持仓和未平仓订单
- 如果省略了 `user`，该技能将使用 treasury 签名者的地址
- 如果提供了 `dex`，工具将查询特定的 HIP-3 builder dex
- 还会返回 `abstractionState` 和 `dexAbstractionEnabled`

### `place_hyperliquid_order`

**输入：**
- `accountAddress` 是可选的（仅用于只读预览/报价）
- `market`
- `side`
- `size`
- `orderType`（限价单必需）
- `price`（限价单必需）
- `slippageBps`（市价单可选）
- `reduceOnly` 是可选的
- `leverage` 是可选的
- `marginMode` 是可选的（限价单必需）
- `timeInForce`（限价单可选）
- `enableDexAbstraction` 是可选的
- `approval` 是可选的
- `dryRun` 是可选的

**行为：**
- 仅支持 Hyperliquid 永续合约
- 支持 `dex:COIN` 格式的 builder dex 永续合约，例如 `xyz:GOLD`
- 第一个版本支持 `market` 和 `limit` 订单
- 市价单会被转换为带有可配置价格上限的受保护的 IOC 订单
- 可以在下单前更新杠杆率
- 执行时会检查市场允许列表、最大单笔订单名义金额、最大每日订单名义金额、最大杠杆率和确认阈值
- `quote_operation` 支持此操作
- 如果提供了 `accountAddress`，则可以使用它进行只读的账户上下文预览
- 只有当签名者与目标 Hyperliquid 账户匹配时才会执行实际操作
- HIP-3 builder-dex 的执行需要启用 `dexAbstraction`
- 如果希望在执行前将账户切换到 `dexAbstraction`，请设置 `enableDexAbstraction=true`

**推荐的代理工作流程：**
- 先调用 `quote_operation` 并设置 `operationType=place_hyperliquid_order`
- 查看返回的 `safety` 块和 `notionalUsd`
- 然后调用 `place_hyperliquid_order` 并设置 `dryRun=true`
- 之后再调用 `place_hyperliquid_order` 并设置 `dryRun=false`

### `protect_hyperliquid_position`

**输入：**
- `accountAddress` 是可选的（仅用于只读预览/报价）
- `market`
- `takeProfitRoePercent` 是可选的，默认为 `100`
- `stopLossRoePercent` 是可选的，默认为 `50`
- `replaceExisting` 是可选的
- `liquidationBufferBps` 是可选的，默认为 `25`
- `enableDexAbstraction` 是可选的
- `approval` 是可选的
- `dryRun` 是可选的

**行为：**
- 读取请求市场的实时 Hyperliquid 持仓情况
- 根据入场价格和杠杆率计算全额的止盈触发点和止损触发点
- 如果请求的止损幅度超出可清算范围，工具会使用 `liquidationBufferBps` 进行调整并发出警告
- 使用 Hyperliquid 的原生触发订单（仅限减少操作）
- `quote_operation` 支持此操作
- 只有当签名者与目标 Hyperliquid 账户匹配时才会执行实际操作
- 对于 HIP-3 builder-dex 持仓，如果需要将账户切换到 `dexAbstraction`，请设置 `enableDexAbstraction=true`

**推荐的代理工作流程：**
- 先调用 `quote_operation` 并设置 `operationType=protect_hyperliquid_position`
- 查看返回的 `safety` 块和 `notionalUsd`
- 然后调用 `protect_hyperliquid_position` 并设置 `dryRun=true`
- 之后再调用 `protect_hyperliquid_position` 并设置 `dryRun=false`

### `cancel_hyperliquid_order`

**输入：**
- `market`
- `orderId`
- `dryRun` 是可选的

**行为：**
- 首先查找匹配的未平仓订单
- 如果订单当前未打开，则拒绝执行

### `safety_check`

**输入：**
- `operationType`
- `chain`
- `token`
- `amount`
- `destination` 是可选的
- `approval` 是可选的
- `feeBps` 是可选的
- `slippageBps` 是可选的

**行为：**
- 执行允许列表检查
- 确保单次转账金额不超过最大限制
- 确保转账金额不超过每日最大限额
- 需要高于配置阈值的批准
- 拒绝气体储备不足的桥接和存款操作
- 拒绝过高估计的费用或滑点

### `quote_operation`

**输入：**
- `operationType`
- 操作特定的字段

**行为：**
- 估算转账对余额的影响、所需气体费用、路由费用和最低接收金额
- 估算 `place_hyperliquid_order` 的 Hyperliquid 订单名义金额、提交价格和模拟成交价格
- 估算 `protect_hyperliquid_position` 的衍生止盈/止损触发价格和安全结果
- 返回结构化的报价信息（不执行实际操作）

## 示例**

（示例代码块在此处省略）

## 安全默认设置

- 不要绕过 `safety_check` 的检查；执行工具会在内部再次进行验证。
- 对于所有新的目的地或较大的转账，建议先设置 `dryRun=true`。
- 在下达任何新的 Hyperliquid 订单之前，建议先执行 `quote_operation` 并设置 `dryRun=true`。
- 在保护现有的 Hyperliquid 持仓时，建议使用 `protect_hyperliquid_position` 而不是手动计算止盈/止损。
- 对于超过配置阈值的金额，必须明确设置 `approval=true`。
- 永远不要假设未列入允许列表的目的地是安全的。
- 对于多阶段流程（如 Hyperliquid 存款），在部分执行后不要重复使用旧的报价金额；请根据当前余额重新报价。