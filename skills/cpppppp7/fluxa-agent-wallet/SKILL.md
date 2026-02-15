---
name: fluxa-agent-wallet
description: >-
  FluxA Agent Wallet integration via CLI. Enables agents to make x402 payments
  for paid APIs, send USDC payouts to any wallet, and create payment links to receive
  payments. Use when the user asks about crypto payments, x402, USDC transfers,
  payment links, or interacting with the FluxA Agent Wallet.
---

# FluxA 代理钱包

FluxA 代理钱包允许 AI 代理执行链上金融操作（如支付、收款以及生成支付链接），而无需管理私钥。所有操作均通过 **命令行界面（CLI）**（`scripts/fluxa-cli.bundle.js`）来完成。

## 设置

CLI 工具包位于本技能目录下的 `scripts/fluxa-cli.bundle.js` 文件中。该工具包需要 Node.js v18 或更高版本的支持。

```bash
node scripts/fluxa-cli.bundle.js <command> [options]
```

所有命令的输出都会以 JSON 格式显示到标准输出（stdout）：

```json
{ "success": true, "data": { ... } }
```

如果发生错误，输出内容如下：

```json
{ "success": false, "error": "Error message" }
```

退出代码的含义：
- `0`：操作成功
- `1`：操作失败

## 功能

| 功能        | 功能描述                | 使用场景                |
|------------|------------------|----------------------|
| **x402 支付 (v3)** | 使用 x402 协议进行 API 支付，并需要提供授权信息 | 当代理收到 HTTP 402 错误码、需要支付 API 访问费用时使用 |
| **收款**     | 将 USDC 转账到任意钱包地址       | 代理需要将资金转移给收款人             |
| **生成支付链接**   | 创建可共享的支付链接           | 代理需要向用户收费、创建发票或出售内容         |

## 先决条件 — 注册代理 ID

在进行任何操作之前，代理必须拥有一个代理 ID。可以通过以下方式注册代理 ID：

```bash
node scripts/fluxa-cli.bundle.js init \
  --email "agent@example.com" \
  --name "My AI Agent" \
  --client "Agent v1.0"
```

或者通过环境变量预先配置代理 ID：

```bash
export AGENT_ID="ag_xxxxxxxxxxxx"
export AGENT_TOKEN="tok_xxxxxxxxxxxx"
export AGENT_JWT="eyJhbGciOiJ..."
```

验证代理 ID 的状态：

```bash
node scripts/fluxa-cli.bundle.js status
```

CLI 会自动刷新过期的 JWT（JSON Web Tokens）。

## 打开授权链接（用户交互流程）

许多操作需要用户通过链接进行授权（例如授权签名、收款审批、代理注册）。当需要用户打开链接时，请按照以下步骤操作：

1. **首先询问用户**，使用 `AskUserQuestion` 工具并提供选项：
   - “是的，打开链接”
   - “不，直接显示链接”

2. **如果用户选择“是”**：使用 `open` 命令在用户的默认浏览器中打开链接：
   ```bash
   open "<URL>"
   ```

3. **如果用户选择“否”**：显示链接，并询问用户下一步的操作方式。

**示例交互流程：**

```
Agent: I need to open the authorization URL to sign the mandate.
       [Yes, open the link] [No, show me the URL]

User: [Yes, open the link]

Agent: *runs* open "https://agentwallet.fluxapay.xyz/onboard/intent?oid=..."
Agent: I've opened the authorization page in your browser. Please sign the mandate, then let me know when you're done.
```

此流程适用于以下场景：
- 授权签名（来自 `mandate-create` 的 `authorizationUrl`）
- 收款审批（来自 `payout` 的 `approvalUrl`）
- 代理注册（如果需要手动注册）

## 快速决策指南

| 我想... | 相关文档                |
|--------------|----------------------|
| **为返回 HTTP 402 错误的 API 支付** | [X402-PAYMENT.md](X402-PAYMENT.md) |
| **向支付链接付款**（代理之间） | [PAYMENT-LINK.md](PAYMENT-LINK.md) — “向支付链接付款”部分 |
| **向钱包地址转账 USDC** | [PAYOUT.md](PAYOUT.md) |
| **创建支付链接**以接收付款 | [PAYMENT-LINK.md](PAYMENT-LINK.md) — “创建支付链接”部分 |

### 常见操作流程：向支付链接付款

这是一个使用 CLI 完成的六步流程：

```
1. PAYLOAD=$(curl -s <payment_link_url>)                    → Get full 402 payload JSON
2. mandate-create --desc "..." --amount <amount>            → Create mandate (BOTH flags required)
3. User signs at authorizationUrl                           → Mandate becomes "signed"
4. mandate-status --id <mandate_id>                         → Verify signed (use --id, NOT --mandate)
5. x402-v3 --mandate <id> --payload "$PAYLOAD"              → Get xPaymentB64 (pass FULL 402 JSON)
6. curl -H "X-Payment: <token>" <url>                       → Submit payment
```

**重要提示：**`x402-v3` 命令中的 `--payload` 参数必须包含完整的 402 响应 JSON 数据，而不仅仅是提取的部分字段。

详情请参阅 [PAYMENT-LINK.md](PAYMENT-LINK.md) 中的示例和详细说明。

## 金额格式

所有金额均以 **最小单位**（atomic units）表示。以 USDC 为例（保留 6 位小数）：

| 人类可读格式 | 原子单位（atomic units） |
|---------------|----------------------|
| 0.01 USDC     | `10000`                |
| 0.10 USDC     | `100000`                |
| 1.00 USDC     | `1000000`                |
| 10.00 USDC     | `10000000`                |

## CLI 命令快速参考

| 命令        | 必需的参数                | 功能描述                          |
|------------|------------------|--------------------------------------|
| `status`     | （无）                | 检查代理配置                        |
| `init`      | `--email`, `--name`         | 注册代理 ID                         |
| `mandate-create` | `--desc`, `--amount`         | 创建授权请求                         |
| `mandate-status` | `--id`             | 查询授权请求的状态                   |
| `x402-v3`     | `--mandate`, `--payload`       | 执行 x402 v3 支付请求                   |
| `payout`     | `--to`, `--amount`, `--id`       | 创建收款请求                         |
| `payout-status` | `--id`             | 查询收款请求的状态                   |
| `paymentlink-create` | `--amount`           | 创建支付链接                         |
| `paymentlink-list` | （无）                | 列出所有支付链接                         |
| `paymentlink-get` | `--id`             | 获取支付链接的详细信息                     |
| `paymentlink-update` | `--id`             | 更新支付链接                         |
| `paymentlink-delete` | `--id`             | 删除支付链接                         |
| `paymentlink-payments` | `--id`             | 获取指定链接的付款记录                     |

**常见错误及修正方式：**

| 错误表达       | 正确表达               |
|---------------|---------------------------|
| `mandate-create --amount 100000` | `mandate-create --desc "..." --amount 100000` |
| `mandate-status --mandate mand_xxx` | `mandate-status --id mand_xxx`         |
| `x402-v3 --payload '{"maxAmountRequired":"100000"}'` | `x402-v3 --payload '<完整的 402 响应 JSON，包含 accepts 数组>'` |

## 环境变量

| 变量          | 描述                        |
|---------------|-----------------------------------------|
| `AGENT_ID`     | 预先配置的代理 ID                   |
| `AGENT_TOKEN`     | 预先配置的代理令牌                   |
| `AGENT_JWT`     | 预先配置的代理 JWT                   |
| `AGENT_EMAIL`     | 用于自动注册的代理邮箱                 |
| `AGENT_NAME`     | 用于自动注册的代理名称                 |
| `CLIENT_INFO`    | 用于自动注册的客户端信息                 |
| `FLUXA_DATA_DIR`   | 自定义数据目录（默认：`~/.fluxa-ai-wallet-mcp`）     |
| `WALLET_API`     | 钱包 API 的基础 URL                   |
| `AGENT_ID_API`     | 代理 ID 相关 API 的基础 URL               |