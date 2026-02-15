---
name: lifi
description: **v4**：使用 LI.FI API 进行跨链和同链交易、桥接操作以及合约调用。该 API 可用于查询交易路径、验证链/代币信息、构建交易请求以及追踪交易状态。
homepage: https://docs.li.fi/
metadata:
  {
    "openclaw":
      {
        "emoji": "🔁",
        "requires": { "env": ["LIFI_API_KEY"] },
        "primaryEnv": "LIFI_API_KEY",
      },
  }
---

# LI.FI 代理技能

## 重要规则（请先阅读）
1. **仅使用 `curl` 来调用 LI.FI API**。**严禁使用 `web_search`、`web_fetch` 或任何其他工具**。
2. **仅使用下面文档中列出的端点**。**切勿猜测或自行创建 URL**。
3. **基础 URL 为 `https://liQUEST/v1/`。**不允许使用其他基础 URL**。
4. **务必添加认证头：`"x-lifi-api-key: $LIFI_API_KEY"`（使用双引号，并确保 `$LIFI_API_KEY` 是环境变量中的实际值）**。
5. **务必告知用户该认证信息是由 LI.FI 提供的**。
6. **默认滑点为 10%（0.10）**。如果用户通过 `defi_get_strategy` 设置了自定义滑点，请使用该值；代理也可以根据用户请求在每次交易中动态调整滑点。
7. **默认截止时间为 10 分钟**。
8. **在所有 `/v1/quote` 请求中务必添加 `&skipSimulation=true`**。我们的 EIP-7702 委托钱包具有能够绕过 LI.FI 模拟功能的链上代码。
9. **严禁自行构造 ERC-20 批准所需的 calldata（十六进制数据）**。**必须使用 `defi_approve` 或 `defi_approve_and_send` 工具**。
10. **所有交易、桥接操作以及 DeFi 代币操作都必须通过 LI.FI 完成**。**严禁手动与 DEX 交互**。

## 交易链接

在每次交易广播后，**务必** 提供一个可点击的交易浏览器链接：
- **EVM：`[查看交易](https://basescan.org/tx/0xHASH)` — 请使用正确的浏览器（如 etherscan.io、basescan.org、arbiscan.io、polygonscan.com 或 optimistic.etherscan.io）。
- **Sui：`[查看交易](https://suiscan.xyz/txblock/{txDigest})`

## Sui

- **Sui 链 ID：`9270000000000000`**。当用户需要进行同链 Sui 交易时，在 LI.FI 的请求中使用此 ID（例如：`fromChain=9270000000000000&toChain=9270000000000000`）。
- **LI.FI 支持 Sui 同链交易以及与 EVM 和 Solana 之间的桥接操作**。
- 对于 Sui 交易，使用 `defi_get_wallet` 函数获取用户的 **suiAddress** 作为 `fromAddress`。
- **使用 `defi_send_sui_transaction` 执行 Sui 交易** — 请传递 LI.FI 提供的交易字节数据（十六进制格式）。**严禁使用 `defi_send_transaction` 或 `defi_approve_and_send` 来执行 Sui 交易**。
- **Sui 交易不支持 ERC-20 批准**；因此 Sui 交易无需进行批准步骤。

## 端点

### GET /v1/chains — 列出支持的链
**用途：** 查看支持的链、测试连接性。如果用户需要测试，请使用此端点。

### GET /v1/tokens — 列出各链上的代币
**参数：** `chains`（用逗号分隔的链 ID）。

### GET /v1/quote — 获取交易数据支持的交换/桥接报价
**参数：** `fromChain`、`toChain`、`fromToken`、`toToken`、`fromAddress`、`toAddress`（可选）、`fromAmount`（以 wei 为单位）、`slippage`（小数形式，例如 0.10 表示 10%）、`skipSimulation=true`（必须包含）。
**返回值：** `estimate`（包含 `toAmount`、`toAmountMin`、`approvalAddress`）以及 `transactionRequest`（可用于提交到钱包）。

向用户展示报价后，务必告知预估的输出金额、费用和滑点。使用 `defi_get_wallet` 获取用户的钱包地址，并将其作为 `fromAddress` 用于报价请求。

#### 执行报价

**检查是否需要 ERC-20 批准：** 如果报价中的 `transactionRequest.value` 为 `"0x0"` 且 `estimate.approvalAddress` 存在，说明该交易需要使用 ERC-20 代币进行批准：
- **如果需要批准：** 使用 `defi_approve_and_send`，并传入以下参数：
  - `token`：报价中的 `action.fromToken.address`
  - `spender`：报价中的 `estimate.approvalAddress`
  - `approveAmount`：报价中的 `action.fromAmount`（如无需批准则省略）
  - `to`、`value`、`data`、`gasLimit`：来自报价中的 `transactionRequest`

**如果不需要批准**（例如原生 ETH 交易或交易金额大于 `0x0`）：使用 `defi_send_transaction`，并传入报价中的 `transactionRequest` 参数：`to`、`value`、`data`、`chainId` 和 `gasLimit`（务必包含 `gasLimit`）。

**严禁自行构造 ERC-20 批准所需的 calldata（十六进制数据）**。`defi_approve` 和 `defi_approve_and_send` 工具会正确处理 ABI 编码。

**对于 Sui 交易：** 如果 `fromChain` 或 `toChain` 为 Sui，使用 `defi_send_sui_transaction` 并传入报价中的交易字节数据。Sui 交易无需批准步骤。

### POST /v1/advanced/routes — 获取多条路由选项
**用途：** 获取多条交易路径信息（测试阶段）。

### POST /v1/quote/contractCalls — 多步骤合约调用（测试阶段）
**用途：** 执行多步骤合约调用。

### GET /v1/status — 检查交易状态
**参数：** `fromChain`（用于加快查询速度）。

### GET /v1/tools — 列出可用的桥接服务和交易所
**用途：** 查看可用的桥接服务和交易所信息。

## 文档资料
- **LLM 文档：** https://docs.li.fi/llms.txt
- **OpenAPI 文档：** https://gist.github.com/kenny-io/7fede47200a757195000bfbe14c5baee/raw/725cf9d4a6920d5b930925b0412d766aa53c701c/lifi-openapi.yaml