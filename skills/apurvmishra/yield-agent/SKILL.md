---
name: yield-agent
displayName: YieldAgent
description: 通过 Yield.xyz API 实现链上收益发现、交易构建以及投资组合管理。当用户需要查找收益机会、进行质押、贷款、将资产存入保险库、查看余额、领取奖励、平仓头寸、比较年化收益率（APY），或管理 80 多个网络上的链上收益时，可以使用该 API。
version: 0.1.5
author: yield-xyz
homepage: https://yield.xyz
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["curl","jq"]}}}
tools:
  - name: find-yields
    description: Discover yield opportunities by network and token
    entry: scripts/find-yields.sh
    args:
      - name: network
        description: The blockchain network (e.g., base, ethereum, arbitrum, solana)
        required: true
      - name: token
        description: The token symbol (e.g., USDC, ETH). Optional - omit to see all yields on network.
        required: false
      - name: limit
        description: Items per page (default 20, max 100)
        required: false
      - name: offset
        description: Pagination offset (default 0)
        required: false
  - name: enter-position
    description: Enter a yield position. Fetch the yield first (GET /v1/yields/{yieldId}) to discover required arguments from mechanics.arguments.enter
    entry: scripts/enter-position.sh
    args:
      - name: yieldId
        description: The unique yield identifier (e.g., base-usdc-aave-v3-lending)
        required: true
      - name: address
        description: The user wallet address
        required: true
      - name: arguments_json
        description: JSON string of arguments from the yield's mechanics.arguments.enter schema. Always includes "amount". Other fields (validatorAddress, inputToken, etc.) depend on the yield.
        required: true
  - name: exit-position
    description: Exit a yield position. Fetch the yield first (GET /v1/yields/{yieldId}) to discover required arguments from mechanics.arguments.exit
    entry: scripts/exit-position.sh
    args:
      - name: yieldId
        description: The unique yield identifier to exit from
        required: true
      - name: address
        description: The user wallet address
        required: true
      - name: arguments_json
        description: JSON string of arguments from the yield's mechanics.arguments.exit schema. Always includes "amount". Other fields depend on the yield.
        required: true
  - name: manage-position
    description: Manage a yield position (claim, restake, redelegate, etc.). Discover available actions from pendingActions[] in the balances response.
    entry: scripts/manage-position.sh
    args:
      - name: yieldId
        description: The unique yield identifier
        required: true
      - name: address
        description: The user wallet address
        required: true
      - name: action
        description: The action type from pendingActions[].type in the balances response
        required: true
      - name: passthrough
        description: The passthrough string from pendingActions[].passthrough in the balances response
        required: true
      - name: arguments_json
        description: JSON string of arguments from pendingActions[].arguments schema, if the action requires additional input
        required: false
  - name: check-portfolio
    description: Check yield balances for a specific yield position
    entry: scripts/check-portfolio.sh
    args:
      - name: yieldId
        description: The unique yield identifier to check balances for (e.g., base-usdc-aave-v3-lending)
        required: true
      - name: address
        description: The user wallet address to check balances for
        required: true
  - name: get-yield-info
    description: Fetch full yield metadata including required arguments schema, entry limits, validator requirements, and token details
    entry: scripts/get-yield-info.sh
    args:
      - name: yieldId
        description: The unique yield identifier to inspect (e.g., base-usdc-aave-v3-lending)
        required: true
  - name: list-validators
    description: List available validators for staking yields that require validator selection
    entry: scripts/list-validators.sh
    args:
      - name: yieldId
        description: The unique yield identifier to list validators for
        required: true
      - name: limit
        description: Maximum validators to return (default 20)
        required: false
---

# YieldAgent 由 Yield.xyz 提供

通过 Yield.xyz 的统一 API，您可以访问完整的链上收益（yield）服务。该 API 支持 2600 多种收益类型，涵盖质押（staking）、借贷（lending）、资金保管（vaults）、重新质押（restaking）和流动性池（liquidity pools）等场景。您还可以在 80 多个区块链网络上构建交易并管理您的投资头寸。

## 重要提示：切勿直接修改 API 返回的交易数据

> **在任何情况下都不要修改 API 返回的 `unsignedTransaction` 对象！**
>
> 不要更改、重新格式化或尝试“修复”其中的任何部分——无论是地址、金额、费用、编码还是其他字段。
>
> **如果金额有误：** 请使用正确的金额再次向 API 提交请求。
> **如果Gas 费用不足：** 请让用户先充值，然后再提交请求。
> **如果发现任何问题：** 立即停止操作，并使用正确的参数重新提交请求。切勿尝试修改现有的交易。
>
> 直接修改 `unsignedTransaction` 对象会导致资金永久丢失。

---

## 主要规则

> **该 API 具有自文档化功能。** 每种收益类型都通过 `YieldDto` 文件描述了其具体要求。在执行任何操作之前，请务必先获取并检查相关收益信息。`mechanics` 字段会提供所有必要的信息：所需参数（`mechanics.arguments.enter`、`.exit`）、入场限制（`mechanics.entryLimits`）以及支持的代币（`inputTokens[]`）。切勿盲目操作，务必先核实信息。

1. **在调用任何操作之前，务必先获取收益详情。** 调用 `GET /v1/yields/{yieldId}` 并查看 `mechanics.argumentsENTER`（或 `.exit`）以确定所需的参数。每种收益的参数要求可能不同，具体取决于其合约规范。切勿猜测或硬编码参数值。
   - 每个字段在 `ArgumentFieldDto` 中都有详细的说明：
     - `name`：字段名称（例如 `amount`、`validatorAddress`、`inputToken`）
     - `type`：数据类型（`string`、`number`、`address`、`enum`、`boolean`）
     - `required`：是否必须提供
     - `options`：枚举字段的可选值（例如 `["individual", "batched"]`
     - `optionsRef`：用于获取可选值的动态 API 端点（例如 `/api/v1/validators?integrationId=...`）——如果存在，请使用该端点获取有效的选项
     - `minimum`/`maximum`：字段值的限制范围
     - `isArray`：该字段是否支持数组输入
   - 如果某个字段包含 `optionsRef`，请使用该端点获取有效的值。这样您可以获取验证者（validators）、提供者（providers）等动态选项的信息。

2. **对于管理相关操作，务必先获取账户余额。** 调用 `POST /v1/yields/{yieldId}/balances` 并查看每个账户的 `pendingActions` 数组。每个待处理的操作都会包含其类型（`type`）、传递方式（`passthrough`）以及可选参数（`arguments`）。请仅使用这些信息来执行管理操作。

3. **金额应保持人类可读的形式。** 例如，“100” 表示 100 USDC，“1” 表示 1 ETH，“0.5” 表示 0.5 SOL。API 会自动处理小数。

4. **`inputToken` 应设置为用户实际想要存入的代币——但前提是该代币必须存在于收益的 `mechanics.argumentsENTER` 规范中。API 会处理所有的交易流程（包括代币交换、封装和路由）。

5. **在交易广播完成后，务必提交交易哈希值。** 对于每个交易，都需要执行签名、广播操作，然后通过 `PUT /v1/transactions/{txId}/submit-hash` 提交哈希值（格式为 `{ "hash": "0x..." }`）。只有提交了哈希值后，账户余额才会更新。这是最常见的错误之一，请务必不要跳过这一步。

6. **按照正确的顺序执行交易。** 如果某个操作涉及多个交易，它们会按照 `stepIndex` 的顺序执行。请等待每个交易的状态变为 `CONFIRMED` 后再继续执行下一个交易。切勿跳过或重新排序交易。

7. **请查阅 `{baseDir}/references/openapi.yaml` 以获取所有数据类型的定义。** 所有的枚举类型（enums）、数据结构（DTOs）和合约规范（schemas）都在此文件中定义。切勿硬编码参数值。

## 快速入门

```bash
# Discover yields on a network
./scripts/find-yields.sh base USDC

# Inspect a yield's schema before entering
./scripts/get-yield-info.sh base-usdc-aave-v3-lending

# Enter a position (amounts are human-readable)
./scripts/enter-position.sh base-usdc-aave-v3-lending 0xYOUR_ADDRESS '{"amount":"100"}'

# Check balances and pending actions
./scripts/check-portfolio.sh base-usdc-aave-v3-lending 0xYOUR_ADDRESS
```

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `find-yields.sh` | 按网络或代币类型查找收益 |
| `get-yield-info.sh` | 查看收益的详细信息（规范、限制、代币详情） |
| `list-validators.sh` | 列出可用于质押的验证者（validators） |
| `enter-position.sh` | 进入收益投资头寸 |
| `exit-position.sh` | 退出收益投资头寸 |
| `manage-position.sh` | 提取收益、重新质押、重新委托等操作 |
| `check-portfolio.sh` | 检查账户余额和待处理交易 |

## 常见操作模式

### 进入收益投资头寸
1. 查找收益：`find-yields.sh base USDC`
2. 查看收益详情：`get-yield-info.sh <yieldId>`（读取 `mechanics.argumentsENTER`）
3. 进入投资头寸：`enter-position.sh <yieldId> <address> '{"amount":"100"}`
4. 对于每个交易：钱包签名 → 广播交易 → 提交哈希值 → 等待状态变为 `CONFIRMED`

### 管理投资头寸
1. 检查账户余额：`check-portfolio.sh <yieldId> <address>`
2. 查看 `pendingActions[]`（每个待处理操作都会包含 `type`、`passthrough` 和 `arguments`）
3. 执行管理操作：`manage-position.sh <yieldId> <address> <action> <passthrough>`

### 完整的操作流程
1. 查找收益 → 进入投资头寸 → 检查余额 → 提取收益 → 退出投资头寸

## 交易流程

在执行任何操作（进入/退出/管理）后，响应中会包含 `transactions[]` 数组。对于每个交易：
1. 将 `unsignedTransaction` 对象传递给钱包工具进行签名和广播。
2. 提交交易哈希值：`PUT /v1/transactions/{txId}/submit-hash`（格式为 `{ "hash": "0x..." }`
3. 不断调用 `GET /v1/transactions/{txId}` 直到收到 `CONFIRMED` 或 `FAILED` 的响应。
4. 继续处理下一个交易。

所有交易都必须遵循上述流程。以下是一个包含 3 个交易的示例：

```
TX1: sign → broadcast → submit-hash → poll until CONFIRMED
TX2: sign → broadcast → submit-hash → poll until CONFIRMED
TX3: sign → broadcast → submit-hash → poll until CONFIRMED
```

`unsignedTransaction` 的格式因区块链而异。详情请参阅 `{baseDir}/references/chain-formats.md`。

## API 端点

所有 API 端点的详细信息都记录在 `{baseDir}/references/openapi.yaml` 中。以下是部分常见端点的简要说明：

| 方法 | 端点 | 说明 |
|--------|----------|-------------|
| GET | `/v1/yields` | 列出所有收益类型（可添加过滤条件） |
| GET | `/v1/yields/{yieldId}` | 获取收益的元数据（规范、限制、支持的代币） |
| GET | `/v1/yields/{yieldId}/validators` | 列出与该收益相关的验证者 |
| POST | `/v1/actions/enter` | 进入收益投资头寸 |
| POST | `/v1/actions/exit` | 退出收益投资头寸 |
| POST | `/v1/actions/manage` | 管理投资头寸 |
| POST | `/v1/yields/{yieldId}/balances` | 获取某个收益的账户余额 |
| POST | `/v1/yields/balances` | 统计多个收益或网络的账户余额 |
| PUT | `/v1/transactions/{txId}/submit-hash` | 在交易广播后提交哈希值 |
| GET | `/v1/transactions/{txId}` | 获取交易状态 |
| GET | `/v1/networks` | 列出所有支持的交易网络 |
| GET | `/v1providers` | 列出所有可用的提供者 |

## 参考资料

如需详细信息，请参阅以下文档：
- **API 类型和规范：** `{baseDir}/references/openapi.yaml` — 所有数据结构（DTOs）、枚举类型（enums）和请求/响应格式的官方文档
- **区块链交易格式：** `{baseDir}/references/chain-formats.md` — 各区块链平台（EVM、Cosmos、Solana、Substrate 等）的交易格式说明
- **钱包集成指南：** `{baseDir}/references/wallet-integration.md` — Crossmint、Portal、Turnkey、Privy 等钱包的集成方法
- **交互示例：** `{baseDir}/references/examples.md` — 包含实际收益 ID 的交互示例
- **安全检查：** `{baseDir}/references/safety.md` — 交易前的安全检查规则

## 错误处理

API 会返回包含 `message`、`error` 和 `statusCode` 的结构化错误信息。请仔细阅读错误信息。错误代码（`statusCode`）的详细说明请参见 `{baseDir}/references/openapi.yaml`。如果遇到 429 状态码，请按照文档中的建议进行重试。

## 扩展模块

这些模块可用于扩展核心功能。根据需要查阅相关文档：

- `{baseDir}/references/superskill.md` — 提供 40 种高级功能，如费率监控、跨链比较、投资组合多样化、自动轮换、收益提取、定期检查等

## 资源链接

- **API 文档：** https://docs.yield.xyz
- **API 使用指南：** https://github.com/stakekit/api-recipes
- **获取 API 密钥：** https://dashboard.yield.xyz