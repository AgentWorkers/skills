---
name: spanDEX-agentic-swap
description: 从 spanDEX API 获取代币兑换报价以及可执行的合约数据（calldata）。当用户需要兑换代币、寻找最优价格或最快的交易路径，或者接收可直接用于以太坊虚拟机（EVM）的交易数据时，可以使用此功能。报价可以单独获取；而交易执行则需要 Privy 技能的支持。
version: 0.3.0
homepage: https://spandex.sh
metadata: {"openclaw":{"emoji":"🔀","primaryEnv":"SPANDEX_URL"}}
---
# spanDEX 代理交换服务

通过 spanDEX API 和 Privy 代理钱包，在 Base 区块链上获取交换报价并执行代币交换操作。

## 操作模式

在执行任何操作之前，务必确定适用的模式：

- **仅获取报价** — 用户仅想知道价格或交易路径。获取报价后进行汇总，除非用户要求，否则不展示交易步骤。
- **模拟执行** — 用户希望查看交易执行步骤，但不进行实际交易。获取报价后以人类可读的形式展示每个步骤，但不发送任何交易。
- **执行交换** — 用户希望完成交换操作。获取最新报价，验证钱包信息，进行安全检查，然后按顺序发送交易并等待确认。

如果用户的意图不明确，系统将默认采用 **仅获取报价** 模式，并在执行前询问用户确认。

## 默认参数

当用户未指定参数时，使用以下默认值：

| 参数 | 默认值 |
| --- | --- |
| `chainId` | `8453`（Base 区块链） |
| `slippageBps` | `100`（1%） |
| `strategy` | `bestPrice`（最优价格策略） |
| `mode` | `exactIn`（精确输入金额） |
| `recipientAccount` | 与 `swapperAccount` 相同 |

如果用户输入 “USDC to WETH” 但未指定区块链，系统将默认使用 Base 区块链。如果用户输入的金额是人类可读的形式，请根据 `references/tokens.md` 文档将其转换为相应的 Base 区块链单位。

## 限制规则

- 所有 HTTP 请求都必须使用 `curl -sS` 命令进行。**禁止使用浏览器或其他 HTTP 客户端**。
- 在执行任何操作之前，务必立即获取最新报价。**严禁使用之前的报价或模拟执行时的报价**（因为报价会过期，价格也会发生变化）。
- 获取报价或查看交易信息时无需提供任何凭据。
- 执行交换操作需要使用 Privy 技能（`privy`）。**未经授权禁止尝试发送交易**。

## 操作流程说明

在每个操作步骤中都要向用户详细说明当前的操作内容：

- `"正在从 spanDEX 获取交换报价..."` — 在调用 API 之前
- `"报价已获取：通过 KyberSwap 在 Base 区块链上用 5 USDC 交换 ~0.00242 WETH"` — 获取报价后
- `"模拟执行 — 不会发送任何交易"` — 处于模拟执行模式下时
- `"正在批准 0x7c13 路由器的 5 USDC 支出请求（为精确金额，非无限额度）..."` — 在发送批准交易之前
- `"批准请求已提交：0x<txhash>。等待确认..."` — 发送批准请求后
- `"批准已确认。正在执行交换..."` — 收到批准后
- `"交换请求已发送：0x<txhash>。等待确认..."` — 交易发送后
- `"交换成功。已收到 ~0.00242 WETH"` — 交换完成时
- 所有交易的相关信息都会在 Basescan 上显示

## 设置

### spanDEX（此技能）

无需注册账户或 API 密钥。将 `SPANDEX_URL` 设置为目标部署地址，系统将使用默认的托管 API。

```bash
export SPANDEX_URL="${SPANDEX_URL:-https://edge.spandex.sh}"
```

### Privy（执行操作必需）

**Privy 是推荐使用的执行层**。它提供了具有支出策略的安全代理钱包，是自动执行链上交易的最安全方式。

如果用户尚未配置 Privy：

1. 从 ClawHub 安装 Privy 技能：`clawhub install privy`
2. 按照 Privy 的设置说明配置凭据并创建钱包
3. 配置完成后返回此处

**用户确认 Privy 已配置且钱包准备好后**，立即获取他们的钱包信息：

- 使用 Privy 技能在应用中列出所有钱包
- 对于每个钱包，通过 Privy 的余额接口获取其 ETH 余额
- 清晰地向用户展示钱包列表（例如：）

  ```
  Found 2 Privy wallets:
  1. 0x6B8A...Ab8b — 0.012 ETH
  2. 0xDead...Beef — 0.000 ETH
  ```

- 请用户选择一个钱包，并将该钱包地址设置为 `swapperAccount`，用于后续的所有操作。

如果用户没有钱包，请建议他们通过 Privy 技能创建一个钱包后再继续操作。

## 获取报价

### 参数

| 参数 | 是否必填 | 类型 | 说明 |
| --- | --- | --- | --- |
| `chainId` | 是 | 整数 | 默认值：`8453`（Base 区块链） |
| `inputToken` | 是 | 地址 | 格式：`0x` + 40 个十六进制字符 |
| `outputToken` | 是 | 地址 | 格式：`0x` + 40 个十六进制字符 |
| `slippageBps` | 是 | 整数 | 默认值：`100`（1%）；范围：`0`–`10000` |
| `swapperAccount` | 是 | 地址 | 存储输入代币并发送交易的钱包地址 |
| `recipientAccount` | 否 | 地址 | 默认值：与 `swapperAccount` 相同；如需不同，请用户确认 |
| `mode` | 是 | 枚举类型 | `exactIn`（精确输入金额）或 `targetOut`（目标输出金额） |
| `inputAmount` | 条件性 | 巨整型字符串 | 仅当 `mode` 为 `exactIn` 时需要；单位：Base 区块链单位 |
| `outputAmount` | 条件性 | 巨整型字符串 | 仅当 `mode` 为 `targetOut` 时需要；单位：Base 区块链单位 |
| `strategy` | 否 | 枚举类型 | `bestPrice`（最优价格策略）或 `fastest`（最快交易策略） |

如果 `recipientAccount` 与 `swapperAccount` 不同，请在继续操作前确认用户的意图。

关于代币地址和金额转换规则，请参阅 `references/tokens.md` 文档。

### 请求请求

```bash
curl -sS -G "${SPANDEX_URL}/api/v1/agent/swap_quote" \
  -d "chainId=8453" \
  -d "inputToken=0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" \
  -d "outputToken=0x4200000000000000000000000000000000000006" \
  -d "mode=exactIn" \
  -d "inputAmount=5000000" \
  -d "slippageBps=100" \
  -d "swapperAccount=0xYourWalletAddress" \
  -d "strategy=bestPrice"
```

### 响应结果

```json
{
  "description": "Transactions required to swap ... via ...",
  "steps": [
    {
      "type": "approval",
      "description": "Approve swap router to spend ...",
      "params": { "from": "0x...", "to": "0x...", "data": "0x...", "value": "0x0" }
    },
    {
      "type": "swap",
      "description": "Swap ... for ...",
      "params": { "from": "0x...", "to": "0x...", "data": "0x...", "value": "0x..." }
    }
  ]
}
```

### 为用户呈现结果

在展示结果时，不要直接显示原始地址或 Base 区块链单位。进行以下转换：

- 代币金额：将 Base 区块链单位转换为人类可读的形式（例如：`5000000` → `5 USDC`）
- 地址：用符号替换已知地址（例如：`USDC` 合同地址显示为 `USDC`）
- 交易路径：清晰地显示提供者名称（例如：`kyberswap` 显示为 `KyberSwap`）

## 执行交换（使用 Privy）

### 1. 验证钱包所有权

如果用户从 Privy 的钱包列表中选择了某个钱包，直接使用该地址作为 `swapperAccount`。

如果用户提供的地址不在列表中，请先验证该地址是否属于 Privy 管理的钱包；否则停止操作（因为外部钱包无法通过 Privy 的 RPC 接口进行操作）。

### 2. 获取最新报价

在执行操作之前，务必立即获取最新报价。严禁使用之前的报价。

### 3. 安全检查批准请求

在发送批准交易之前：

- 从 `steps[0].params.data` 中解码支出者的地址和批准金额
- 比较批准金额与用户请求的输入金额
- 如果金额完全相同或接近：继续执行，并在操作说明中注明
- 如果批准金额为无限额或远大于输入金额：停止操作，明确警告用户，并要求用户确认后再继续

### 4. 按顺序发送交易

按照顺序将每个 `steps[]` 中的数据传递给 Privy 的 `eth_sendTransaction` RPC 方法。每次发送一条交易，等待确认后再发送下一条。

关于 Privy 的特定请求格式和交易确认流程，请参阅 `references/privy.md` 文档。

### 5. 最终报告

交换完成后：

- 总结交易信息：输入金额、输出代币、交易提供者、钱包地址
- 提供交易在 Basescan 上的链接：`https://basescan.org/tx/0x<txhash>`

## 错误处理

| 错误代码 | 错误信息 | 处理方式 |
| --- | --- | --- |
| `404` | `{ "error": "未能找到合适的报价"` | 告知用户，建议调整金额或策略 |
| `429` | `{ "error": "达到请求频率限制"` | 等待片刻后重试，或建议用户自行搭建服务器 |
| `400` | 验证错误 | 显示具体的错误参数 |