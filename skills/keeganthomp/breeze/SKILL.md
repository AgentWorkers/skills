---
name: breeze-x402-payment-api
description: 通过 x402 支付网关的 HTTP API 与 Breeze 收益聚合器进行交互。当用户需要查看 DeFi 账户余额、存入代币、提取代币或通过 x402 微支付来管理 Solana 收益头寸时，可以使用该 API。
---
# Breeze x402 支付 API

该技能允许通过 [x402 支付协议](https://www.x402.org/) 使用 HTTP API 与 [Breeze](https://breeze.baby)（一个 Solana 收益聚合器）进行交互。每次 API 调用都会自动使用 USDC 在 Solana 上进行微支付。

## 先决条件

- 拥有一个包含 USDC 的 Solana 钱包，用于 x402 微支付
- 一个兼容 x402 协议的 API 服务器（默认：`https://x402.breeze.baby`）
- Node.js / TypeScript 开发环境

## 依赖项

```
@faremeter/fetch        — wraps fetch with automatic x402 payment handling
@faremeter/payment-solana — Solana payment handler for x402
@faremeter/wallet-solana  — local wallet abstraction
@scure/base             — base58 encoding/decoding
@solana/web3.js         — Solana transaction signing and sending
```

## 设置：带支付功能的 `fetch` 请求库

所有 API 调用都使用了一个带有支付功能的 `fetch` 请求库，该库可以自动处理 x402 协议中的挑战（例如收到 HTTP 402 错误时，会要求用户签名支付信息并重试请求）：

```typescript
import { wrap } from "@faremeter/fetch";
import { createPaymentHandler } from "@faremeter/payment-solana/exact";
import { createLocalWallet } from "@faremeter/wallet-solana";
import { Connection, Keypair, PublicKey } from "@solana/web3.js";
import { base58 } from "@scure/base";

const keypair = Keypair.fromSecretKey(base58.decode(WALLET_PRIVATE_KEY));
const connection = new Connection(SOLANA_RPC_URL);
const wallet = await createLocalWallet("mainnet-beta", keypair);
const USDC_MINT = new PublicKey("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v");
const paymentHandler = createPaymentHandler(wallet, USDC_MINT, connection);

const fetchWithPayment = wrap(fetch, { handlers: [paymentHandler] });
```

## API 端点

### 查看余额

```
GET /balance/:fund_user
```

返回一个 JSON 对象，其中包含持仓、存入金额、获得的收益以及年化收益率（APY）。所有数值均以 **基础单位** 表示；若需转换为人类可读的格式（例如 USDC 有 6 位小数），需将数值除以 `10^decimals`。

```typescript
const response = await fetchWithPayment(
  `${API_URL}/balance/${encodeURIComponent(walletPublicKey)}`,
  { method: "GET" }
);
const balances = await response.json();
```

### 存款

```
POST /deposit
Content-Type: application/json
```

创建一个未签名的存款交易。`amount` 参数必须以 **基础单位** 表示。

```typescript
const response = await fetchWithPayment(`${API_URL}/deposit`, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({
    amount: 10_000_000,        // 10 USDC (6 decimals)
    user_key: walletPublicKey,
    strategy_id: STRATEGY_ID,
    base_asset: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
  }),
});
const txString = await response.text(); // encoded unsigned transaction
```

### 提取资金

```
POST /withdraw
Content-Type: application/json
```

创建一个未签名的提取资金交易。支持可选的 WSOL 处理选项。

```typescript
const response = await fetchWithPayment(`${API_URL}/withdraw`, {
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify({
    amount: 5_000_000,
    user_key: walletPublicKey,
    strategy_id: STRATEGY_ID,
    base_asset: "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    all: false,
    exclude_fees: true,          // always recommended
    // For wrapped SOL withdrawals only:
    // unwrap_wsol_ata: true,     // unwrap WSOL to native SOL
    // create_wsol_ata: true,     // create WSOL ATA if needed
    // detect_wsol_ata: true,     // auto-detect WSOL ATA existence
  }),
});
const txString = await response.text();
```

**提取资金参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|---------|-------|--------|-----------|
| `amount` | number | 是     | 存款金额（以基础单位计） |
| `user_key` | string | 是     | 用户的 Solana 公钥 |
| `strategy_id` | string | 是     | Breeze 策略 ID |
| `base_asset` | string | 是     | 代币的发行地址 |
| `all` | boolean | 否      | 提取全部持仓 |
| `exclude_fees` | boolean | 否      | 从金额中扣除费用（推荐：`true`） |
| `unwrap_wsol_ata` | boolean | 否      | 提取资金后将其转换为原生 SOL |
| `create_wsol_ata` | boolean | 否      | 如果不存在 WSOL，则创建 WSOL ATA |
| `detect_wsol_ata` | boolean | 否      | 自动检测 WSOL ATA 并相应地设置相关参数 |

**WSOL 处理：** 在提取封装后的 SOL（格式为 `So11111111111111111111111111111111111111112`）时，设置 `unwrap_wsol_ata: true` 以接收原生 SOL。

## 签名和发送交易

存款和提取资金的操作会返回未签名的交易数据。需要对这些数据进行签名并发送到 Solana：

```typescript
import { VersionedTransaction, Transaction } from "@solana/web3.js";

function extractTransactionString(responseText: string): string {
  const trimmed = responseText.trim();
  try {
    const parsed = JSON.parse(trimmed);
    if (typeof parsed === "string") return parsed;
    throw new Error("expected transaction string");
  } catch (e) {
    if (e instanceof SyntaxError) return trimmed;
    throw e;
  }
}

async function signAndSend(txString: string) {
  const bytes = Uint8Array.from(Buffer.from(txString, "base64"));

  // Try versioned transaction first, then legacy
  try {
    const tx = VersionedTransaction.deserialize(bytes);
    tx.sign([keypair]);
    const sig = await connection.sendRawTransaction(tx.serialize());
    await connection.confirmTransaction(sig, "confirmed");
    return sig;
  } catch {
    const tx = Transaction.from(bytes);
    tx.partialSign(keypair);
    const sig = await connection.sendRawTransaction(tx.serialize());
    await connection.confirmTransaction(sig, "confirmed");
    return sig;
  }
}
```

## 支持的代币

| 代币 | 发行地址 | 小数位数 |
|-------|---------|-----------|
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6       |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | 6       |
| USDS | `USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA` | 6       |
| SOL | `So11111111111111111111111111111111111111112` | 9       |
| JitoSOL | `J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn` | 9       |
| mSOL | `mSoLzYCxHdYgdzU16g5QSh3i5K3z3KZK7ytfqcJm7So` | 9       |
| JupSOL | `jupSoLaHXQiZZTSfEWMTRRgpnyFm8f6sZdosWBjx93v` | 9       |
| JLP | `27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4` | 6       |

## 环境变量

| 变量 | 是否必填 | 默认值 | 说明         |
|---------|---------|-------------|-------------------|
| `WALLET_PRIVATE_KEY` | 是     | —         | Solana 钱包的 Base58 编码私钥 |
| `STRATEGY_ID` | 是     | —         | Breeze 策略 ID         |
| `X402_API_URL` | 否      | `https://x402.breeze.baby` | x402 支付 API 的 URL           |
| `SOLANA_RPC_URL` | 否      | `https://api.mainnet-beta.solana.com` | Solana 的 RPC 端点         |
| `BASE_ASSET` | 否      | 使用的代币发行地址（默认为 USDC） |

## 示例：完整的代理工作流程

典型的存款流程如下：

1. **查看余额** → `GET /balance/:wallet`（通过 x402 协议支付费用）
2. **创建存款交易** → `POST /deposit`（输入以基础单位表示的存款金额，费用通过 x402 协议支付）
3. 从响应文本中提取交易信息
4. 对交易数据进行签名并发送到 Solana
5. 提供交易的签名和查询链接（`https://solscan.io/tx/{sig}`）

有关使用 Claude 框架实现的完整代理流程示例，请参阅 `apps/examples/agent-using-x402-payment-api/`。