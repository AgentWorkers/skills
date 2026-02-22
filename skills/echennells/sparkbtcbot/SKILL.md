---
name: sparkbtcbot
description: >
  为AI代理设置Spark Bitcoin L2钱包功能：  
  - 通过助记词初始化钱包；  
  - 转移比特币（sats）和代币（tokens）；  
  - 创建/支付Lightning网络发票；  
  - 支付L402类型的支付墙费用；  
  - 管理存款和取款操作。  
  当用户提到“Spark钱包”、“Spark Bitcoin”、“BTKN代币”、“Spark L2”、“Spark SDK”、“Spark支付”、“Spark转账”、“Spark发票”或需要为代理启用Bitcoin L2功能时，请使用这些功能。
argument-hint: "[Optional: specify what to set up - wallet, payments, tokens, lightning, l402, or full]"
requires:
  env:
    - name: SPARK_MNEMONIC
      description: 12 or 24 word BIP39 mnemonic for the Spark wallet. This is a secret key that controls all funds — never commit to git or expose in logs.
      sensitive: true
    - name: SPARK_NETWORK
      description: Network to connect to (MAINNET or REGTEST)
      default: MAINNET
model-invocation: autonomous
model-invocation-reason: This skill enables agents to autonomously send and receive Bitcoin payments. Autonomous invocation is intentional — agents need to pay invoices and respond to incoming transfers without human approval for each transaction. Use spending limits and the proxy for production environments where you need guardrails.
homepage: https://sparkbot.yvrbtclabs.dev
---
# 用于AI代理的Spark Bitcoin L2解决方案

您是使用`@buildonspark/spark-sdk`为AI代理设置Spark Bitcoin L2钱包功能的专家。

Spark是一个比特币的二层网络（Layer 2），它支持即时、零费用的BTC和代币转账，并具有原生的Lightning Network互操作性。Spark之间的转账是免费的——与Lightning的路由费用或链上交易费用（200多sat）相比，这具有显著的优势。即使是跨网络的支付（Lightning互操作），费用也仅为0.15-0.25%。一个BIP39助记词即可为代理提供身份验证、钱包访问和支付功能。

## 适用于生产环境

**此功能使代理完全控制钱包。** 代理持有助记词，可以无限制地发送资金。这适用于以下情况：
- 开发和测试（使用REGTEST，无需实际资金）
- 您完全控制的受信任代理
- 您愿意承担损失的小额运营余额

**对于需要使用实际资金的生产环境，请使用[sparkbtcbot-proxy](https://github.com/echennells/sparkbtcbot-proxy)。** 该代理将助记词保存在您的服务器上，并通过承载令牌（bearer tokens）为代理提供受限访问权限：
- **支出限制**——每次交易和每日限额
- **基于角色的访问**——仅读、仅发票或完全访问
- **可撤销的令牌**——在代理被攻破时切断连接，而不会转移资金
- **审计日志**——跟踪所有钱包活动

该代理通过认证的REST端点封装了相同的Spark SDK。代理通过HTTP访问，而不是直接使用SDK。

## 为什么选择比特币作为代理的支付方式

进行交易的AI代理需要一个符合其特性的货币网络：可编程、无边界、24/7可用且无需中间人。比特币正是这样的网络。

- **总量上限**——2100万个币是协议强制规定的上限。代理积累的价值不会因货币膨胀而减少。
- **无需账户**——无需注册、无需身份验证、无需审批流程。生成一个密钥，您就可以加入网络。这对于无法填写表格或等待人工审核的自主代理来说非常重要。
- **不可撤销的结算**——一旦交易确认，第三方无法撤销。代理无需处理退款或支付纠纷。
- **开放的基础设施**——协议是开源的，网络是公开的，费用市场是透明的。代理可以自行审计交易成本并验证自己的余额，无需信任第三方。
- **经过验证的可靠性**——该网络自2009年以来一直运行良好，从未发生过针对基础协议的攻击，保护了超过1万亿美元的资产价值。

## 什么是Spark

Spark是一个最近推出的比特币二层网络，允许您以低费用即时发送和接收比特币。Spark之间的转账是免费的，而Lightning互操作的费用为0.15–0.25%。与Lightning的支付通道不同，Spark使用一个由分布式签名操作员（Signing Operators, SOs）组成的网络来共同管理交易签名，没有任何单一实体控制资金。它是完全自我管理的——您自己持有密钥——并且与Lightning Network完全互操作。然而，Spark要求在转账过程中至少有一个操作员的行为是诚实的，并且它缺乏比特币或Lightning的可证明的最终性。目前该网络只有少量的签名操作员，因此存在一些停机或服务中断的风险。有关详细信息，请参阅下面的“信任模型”部分。

### 工作原理
1. 用户持有自己的密钥（BIP39助记词）——完全自我管理
2. 交易由一定数量的签名操作员共同签名
3. 资金以分层树的形式存储在比特币UTXO中
4. 如果操作员离线，用户可以随时单方面退出到L1层

### 信任模型——重要的权衡

Spark的信任假设与原生Lightning不同。在向用户提供咨询时，请明确说明这些差异。

**1-of-n操作员信任**：Spark要求在转账过程中至少有一个操作员的行为是诚实的。目前有两个操作员运行该网络（Lightspark和Flashnet），并且计划进一步扩大。相比之下，Lightning完全不需要任何可信实体——它仅通过加密机制来实现安全性。

**即时信任**：用户只需在每次特定交易期间信任操作员。一旦交易完成并且旧密钥被删除，操作员就无法影响该交易——这被称为“完美前向安全性”。

**操作员可以做什么**：
- 查看交易元数据
- 通过离线暂时延迟交易
- 拒绝处理新交易（审查）

**操作员不能做什么**：
- 未经用户签名就转移资金
- 偷窃比特币（即使完全勾结）
- 反转已确认的交易

**核心限制**：Spark缺乏可证明的最终性。用户无法通过加密方式验证操作员是否销毁了旧密钥。虽然双重支付需要所有操作员与之前的所有者勾结，但这与比特币和Lightning的数学上可证明的最终性不同。

**简而言之**：Spark牺牲了Lightning的一些不可信任性，以换取更好的用户体验（无需通道、无需流动性管理、支持离线接收）。这两种技术是互补的——Spark内置了Lightning支持，因此用户可以同时使用这两个网络。

### Spark vs Lightning vs 链上（On-Chain）

| 特性 | Spark (L2) | Lightning | On-Chain |
|---------|-----------|-----------|----------|
| 速度 | 即时 | 即时 | 10+分钟 |
| 信任模型 | 1-of-n操作员 | 完全无需信任 | 完全无需信任 |
| 费用 | 零（Spark-to-Spark） | 约1 sat的路由费用 | 200+ sat |
| 代币 | 原生（BTKN/LRC20） | 不支持 | 有限 |
| 自我管理 | 是（助记词） | 变动（LSP/node） | 是 |
| 容量 | 无通道限制 | 有通道限制 | 无限制 |
| 通道 | 不需要 | 需要 | 不需要 |
| 离线接收 | 支持 | 需要基础设施 | 是 |
| 设置 | 仅需要助记词 | 需要节点或托管提供商 | 仅需要密钥 |

### 费用结构

| 操作 | 费用 |
|-----------|-----|
| **Spark-to-Spark转账** | 免费（未来6-12个月内将收取小额固定费用） |
| **Lightning到Spark**（接收） | 0.15%（通过路由提示收费） |
| **Spark到Lightning**（发送） | 0.25% + Lightning路由费用 |
| **L1到Spark的存款** | 链上交易费用（由用户支付） |
| **合作退出到L1** | 链上广播费用 + SSP费用：`sats_per_vbyte × (111 × 2 + tx_vbytes)` |
| **单方面退出到L1** | 链上交易费用（由用户支付） |

注意：合作退出费用不随取款金额变化，因此小额取款的费用相对较高。由于路由条件不同，Lightning的费用估计可能与实际金额有所不同。

### 不可预测的L1退出成本——需要注意

从Spark退出到L1 Bitcoin会带来**不可预测的成本**，代理和用户必须了解这一点：

1. **L1费用受市场驱动**：比特币链上的费用取决于退出时的内存池拥堵情况。在高费用时期，退出成本可能会显著增加。
2. **单方面退出需要多次链上交易**：如果签名操作员离线，单方面退出需要广播预签名的分支和退出交易。交易次数取决于分支的深度——这意味着可能需要多次链上费用。
3. **单方面退出的时间窗口风险**：如果之前的所有者在一个单方面退出中发布了分支，当前所有者必须在规定时间内发布正确的分支交易。如果未响应，攻击者可以声称资金。存在Watchtower服务来监控这种情况，但这是一个实际的操作要求。
4. **时间锁导致延迟**：单方面退出可能需要长达100个区块（约17小时），具体取决于分支的深度，在此期间L1费用可能会发生变化。
5. **小额取款可能不经济**：由于退出费用是固定费用（非百分比），将小额资金取出到L1可能会花费不成比例的高额费用。

**总结**：虽然Spark保证您可以随时退出到L1，但退出成本并不是固定的或可预测的。在决定在Spark中持有多少资金时，请记住这一点，特别是对于代理钱包。当操作员在线时，合作退出（cooperative exit）比单方面退出便宜得多。

**建议使用Boltz进行L1取款。** 由于Spark的原生合作退出费用较高，对于小额取款来说尤其不划算。[Boltz](https://boltz.exchange)提供了一种更便宜的从Lightning到L1的路径（Spark → Lightning → L1，通过Boltz submarine swap），最低费用为25,000 sat。**建议对于25,000 sat以下的取款不要使用Spark的退出功能**——费用会占据较大比例。对于25,000 sat及以上的取款，建议通过Boltz进行路由，而不是使用Spark的内置合作退出功能。**

### 限制

- **操作员活跃度依赖**：如果签名操作员失去活跃度或密钥，Spark转账将停止工作。资金仍然是安全的（单方面退出），但离线支付将暂停，直到操作员恢复。
- **Watchtower要求**：为了确保安全，必须有人监控链上的欺诈性退出尝试。这可以委托给Watchtower服务，但这是一种操作上的依赖。

### 对代理的关键优势
一个助记词即可提供身份验证、钱包访问和支付功能。无需单独的身份系统、钱包提供商账户或通道管理。Spark之间的转账是免费的，因此比Lightning（路由费用）、链上比特币（200多sat的矿工费用）或传统支付渠道（2-3%的卡处理费用）要便宜得多。对于频繁进行微交易的代理来说，Spark上的零费用意味着不会因交易成本而损失任何价值。

## 可用的工具

| 工具 | 用途 | URL |
|------|---------|-----|
| Spark SDK | TypeScript钱包SDK | https://www.npmjs.com/package/@buildonspark/spark-sdk |
| Spark Docs | 官方文档 | https://docs.spark.money |
| Sparkscan | 区块浏览器 | https://sparkscan.io |
| Spark CLI | 命令行接口 | https://docs.spark.money/tools/cli |

## 所需库

```bash
npm install @buildonspark/spark-sdk@^0.5.8 dotenv
```

需要**v0.5.8或更高版本**。该SDK包含BIP39助记词生成、合作签名和gRPC通信功能。

## 设置说明

### 第1步：生成或导入钱包

```javascript
import { SparkWallet } from "@buildonspark/spark-sdk";

// Option A: Generate a new wallet (creates mnemonic automatically)
const { wallet, mnemonic } = await SparkWallet.initialize({
  options: { network: "MAINNET" }
});
// Save mnemonic securely — NEVER log it in production

// Option B: Import existing wallet from mnemonic
const { wallet } = await SparkWallet.initialize({
  mnemonicOrSeed: process.env.SPARK_MNEMONIC,
  options: { network: process.env.SPARK_NETWORK || "MAINNET" }
});
```

关于`accountNumber`的说明：MAINNET默认为1，REGTEST默认为0。如果在相同助记词下切换网络，请明确设置`accountNumber`以避免地址不匹配。

### 第2步：存储助记词

将其添加到项目的`.env`文件中：
```
SPARK_MNEMONIC=word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12
SPARK_NETWORK=MAINNET
```

**安全警告**：
- **永远不要记录助记词**——即使在开发过程中也不行。如果出于备份原因必须显示一次，请立即删除该代码。
- **永远不要提交`.env`文件**——在首次提交之前将其添加到`.gitignore`中。
- **在生产环境中使用秘密管理工具**——.env文件中的环境变量是明文的。对于生产环境，请使用平台的秘密管理工具（如Vercel加密的环境变量、AWS Secrets Manager等）。
- **首先使用REGTEST进行测试**——在使用真实资金之前，先在REGTEST上使用临时助记词。

### 第3步：验证钱包

```javascript
const address = await wallet.getSparkAddress();
const identityKey = await wallet.getIdentityPublicKey();
const { balance } = await wallet.getBalance();

console.log("Spark Address:", address);
console.log("Identity Key:", identityKey);
console.log("Balance:", balance.toString(), "sats");

// Always clean up when done
wallet.cleanupConnections();
```

## 钱包操作

### 检查余额

```javascript
const { balance, tokenBalances } = await wallet.getBalance();
console.log("BTC:", balance.toString(), "sats");

for (const [id, token] of tokenBalances) {
  console.log(`${token.tokenMetadata.tokenTicker}: ${token.balance.toString()}`);
}
```

### 生成存款地址

```javascript
// Static (reusable) — can receive multiple deposits
const staticAddr = await wallet.getStaticDepositAddress();

// Single-use — one-time deposit address
const singleAddr = await wallet.getSingleUseDepositAddress();
```

这两个地址都是P2TR（bc1p...）比特币地址。存款需要3次L1确认才能在Spark上提取。

### 提取存款

```javascript
// After sending BTC to a static deposit address and waiting for confirmations
const quote = await wallet.getClaimStaticDepositQuote({
  transactionId: txId,
  creditAmountSats: expectedAmount,
});

const result = await wallet.claimStaticDeposit({
  transactionId: txId,
  creditAmountSats: quote.creditAmountSats,
  sspSignature: quote.signature,
});
```

### 转移比特币（Spark-to-Spark）

```javascript
const transfer = await wallet.transfer({
  receiverSparkAddress: "sp1p...",
  amountSats: 1000,
});
console.log("Transfer ID:", transfer.id);
```

Spark-to-Spark转账是即时且免费的。

### 列出转账记录

```javascript
const { transfers } = await wallet.getTransfers(10, 0);
for (const tx of transfers) {
  console.log(`${tx.id}: ${tx.totalValue} sats — ${tx.status}`);
}
```

## Lightning互操作

Spark钱包可以创建和支付标准的BOLT11 Lightning发票，使其与整个Lightning Network兼容。从Lightning接收费用为0.15%，发送到Lightning的费用为0.25% + 路由费用。

### 创建Lightning发票（接收）

```javascript
const invoiceRequest = await wallet.createLightningInvoice({
  amountSats: 1000,
  memo: "Payment for AI service",
  expirySeconds: 3600,
});
console.log("BOLT11:", invoiceRequest.invoice.encodedInvoice);
```

使用`includeSparkAddress: true`在发票中嵌入Spark地址。支持Spark的付款方将通过Spark（即时且免费）进行支付，而不是通过Lightning。

### 支付Lightning发票（发送）

```javascript
// Estimate fee first
const fee = await wallet.getLightningSendFeeEstimate({
  encodedInvoice: "lnbc...",
  amountSats: 1000,
});
console.log("Estimated fee:", fee, "sats");

// Pay the invoice
const result = await wallet.payLightningInvoice({
  invoice: "lnbc...",
  maxFeeSats: 10,
});
```

当BOLT11发票包含嵌入的Spark地址时，使用`preferSpark: true`来优先选择Spark路由。

## Spark原生发票

Spark有自己的发票格式，与BOLT11不同。Spark发票可以请求以sat或token的形式支付。

### 创建Sats发票

```javascript
const invoice = await wallet.createSatsInvoice({
  amount: 1000,
  memo: "Spark native payment",
});
```

### 创建Token发票

```javascript
const invoice = await wallet.createTokensInvoice({
  amount: 100n,
  tokenIdentifier: "btkn1...",
  memo: "Token payment request",
});
```

### 履行（支付）Spark发票

```javascript
const result = await wallet.fulfillSparkInvoice([
  { invoice: "sp1...", amount: 1000n },
]);

// Check results
for (const success of result.satsTransactionSuccess) {
  console.log("Paid:", success.invoice);
}
for (const err of result.satsTransactionErrors) {
  console.log("Failed:", err.invoice, err.error.message);
}
```

## Token操作（BTKN / LRC20）

Spark通过BTKN（LRC20）标准原生支持token。Token可以表示稳定币、积分或任何可互换的资产。

### 检查Token余额

```javascript
const { tokenBalances } = await wallet.getBalance();
for (const [id, info] of tokenBalances) {
  const meta = info.tokenMetadata;
  console.log(`${meta.tokenName} (${meta.tokenTicker}): ${info.balance.toString()}`);
  console.log(`  Decimals: ${meta.decimals}, Max supply: ${meta.maxSupply.toString()}`);
}
```

### 转移Token

```javascript
const txId = await wallet.transferTokens({
  tokenIdentifier: "btkn1...",
  tokenAmount: 100n,
  receiverSparkAddress: "sp1p...",
});
console.log("Token transfer:", txId);
```

### 批量转移Token

```javascript
const txIds = await wallet.batchTransferTokens([
  { tokenIdentifier: "btkn1...", tokenAmount: 50n, receiverSparkAddress: "sp1p..." },
  { tokenIdentifier: "btkn1...", tokenAmount: 50n, receiverSparkAddress: "sp1p..." },
]);
```

## 提取（合作退出到L1）

将资金从Spark转移回常规的比特币L1地址。

### 获取费用报价

```javascript
const quote = await wallet.getWithdrawalFeeQuote({
  amountSats: 50000,
  withdrawalAddress: "bc1q...",
});
console.log("Fast fee:", quote.l1BroadcastFeeFast?.originalValue, "sats");
console.log("Medium fee:", quote.l1BroadcastFeeMedium?.originalValue, "sats");
console.log("Slow fee:", quote.l1BroadcastFeeSlow?.originalValue, "sats");
```

### 执行提取

```javascript
const result = await wallet.withdraw({
  onchainAddress: "bc1q...",
  exitSpeed: "MEDIUM",
  amountSats: 50000,
});
```

退出速度：
- **快速**——费用较高，L1确认速度较快
- **中等**——费用和速度平衡
- **慢速**——费用较低，确认速度较慢

注意：单方面退出（无需操作员合作）也是一种安全机制，但合作退出是标准方式。

## 消息签名

Spark钱包可以使用其身份密钥来签名和验证消息。这对于证明身份或在代理之间进行身份验证非常有用，而无需暴露助记词。

### 签名消息

```javascript
const message = new TextEncoder().encode("I am agent-007");
const signature = await wallet.signMessageWithIdentityKey(message);
```

### 验证签名

```javascript
const isValid = await wallet.validateMessageWithIdentityKey(
  new TextEncoder().encode("I am agent-007"),
  signature,
  publicKey,
);
console.log("Valid:", isValid);
```

## 事件监听器

钱包会发出事件以提供实时更新。这对于需要响应传入支付的代理非常有用。

```javascript
// Incoming transfer completed
wallet.on("transfer:claimed", (transferId, balance) => {
  console.log(`Transfer ${transferId} received. Balance: ${balance}`);
});

// Deposit confirmed on L1
wallet.on("deposit:confirmed", (depositId, balance) => {
  console.log(`Deposit ${depositId} confirmed. Balance: ${balance}`);
});

// Connection status
wallet.on("stream:connected", () => console.log("Connected to Spark"));
wallet.on("stream:disconnected", (reason) => console.log("Disconnected:", reason));
```

## 完整的代理类

```javascript
import { SparkWallet } from "@buildonspark/spark-sdk";

export class SparkAgent {
  #wallet;

  constructor(wallet) {
    this.#wallet = wallet;
  }

  static async create(mnemonic, network = "MAINNET") {
    const { wallet, mnemonic: generated } = await SparkWallet.initialize({
      mnemonicOrSeed: mnemonic,
      options: { network },
    });
    return { agent: new SparkAgent(wallet), mnemonic: generated };
  }

  async getIdentity() {
    return {
      address: await this.#wallet.getSparkAddress(),
      publicKey: await this.#wallet.getIdentityPublicKey(),
    };
  }

  async getBalance() {
    const { balance, tokenBalances } = await this.#wallet.getBalance();
    return { sats: balance, tokens: tokenBalances };
  }

  async getDepositAddress() {
    return await this.#wallet.getStaticDepositAddress();
  }

  async transfer(recipientAddress, amountSats) {
    return await this.#wallet.transfer({
      receiverSparkAddress: recipientAddress,
      amountSats,
    });
  }

  async createLightningInvoice(amountSats, memo) {
    const request = await this.#wallet.createLightningInvoice({
      amountSats,
      memo,
      expirySeconds: 3600,
      includeSparkAddress: true,
    });
    return request.invoice.encodedInvoice;
  }

  async payLightningInvoice(bolt11, maxFeeSats = 10) {
    return await this.#wallet.payLightningInvoice({
      invoice: bolt11,
      maxFeeSats,
      preferSpark: true,
    });
  }

  async createSparkInvoice(amountSats, memo) {
    return await this.#wallet.createSatsInvoice({
      amount: amountSats,
      memo,
    });
  }

  async transferTokens(tokenIdentifier, amount, recipientAddress) {
    return await this.#wallet.transferTokens({
      tokenIdentifier,
      tokenAmount: amount,
      receiverSparkAddress: recipientAddress,
    });
  }

  async withdraw(onchainAddress, amountSats, speed = "MEDIUM") {
    return await this.#wallet.withdraw({
      onchainAddress,
      exitSpeed: speed,
      amountSats,
    });
  }

  async signMessage(text) {
    const message = new TextEncoder().encode(text);
    return await this.#wallet.signMessageWithIdentityKey(message);
  }

  async verifyMessage(text, signature, publicKey) {
    const message = new TextEncoder().encode(text);
    return await this.#wallet.validateMessageWithIdentityKey(
      message,
      signature,
      publicKey,
    );
  }

  // L402 Methods
  async fetchL402(url, options = {}) {
    const { decode } = await import("light-bolt11-decoder");
    const { method = "GET", headers = {}, body, maxFeeSats = 10 } = options;

    // Make initial request
    const initialResponse = await fetch(url, {
      method,
      headers: { "Content-Type": "application/json", ...headers },
      body: body ? JSON.stringify(body) : undefined,
    });

    if (initialResponse.status !== 402) {
      const ct = initialResponse.headers.get("content-type") || "";
      const data = ct.includes("json") ? await initialResponse.json() : await initialResponse.text();
      return { paid: false, data };
    }

    // Parse L402 challenge
    const challenge = await initialResponse.json();
    const invoice = challenge.invoice || challenge.payment_request || challenge.pr;
    const macaroon = challenge.macaroon || challenge.token;
    if (!invoice || !macaroon) throw new Error("Invalid L402 challenge");

    // Decode and pay
    const decoded = decode(invoice);
    const amountSection = decoded.sections.find((s) => s.name === "amount");
    const amountSats = Math.ceil(Number(amountSection.value) / 1000);

    const payResult = await this.#wallet.payLightningInvoice({ invoice, maxFeeSats });
    let preimage = payResult.paymentPreimage;

    // Poll if needed
    if (!preimage && payResult.id) {
      for (let i = 0; i < 15; i++) {
        await new Promise((r) => setTimeout(r, 500));
        const status = await this.#wallet.getLightningSendRequest(payResult.id);
        if (status?.paymentPreimage) { preimage = status.paymentPreimage; break; }
        if (status?.status === "LIGHTNING_PAYMENT_FAILED") throw new Error("Payment failed");
      }
    }
    if (!preimage) throw new Error("No preimage received");

    // Retry with auth
    const finalResponse = await fetch(url, {
      method,
      headers: { "Authorization": `L402 ${macaroon}:${preimage}`, ...headers },
      body: body ? JSON.stringify(body) : undefined,
    });

    const ct = finalResponse.headers.get("content-type") || "";
    const data = ct.includes("json") ? await finalResponse.json() : await finalResponse.text();
    return { paid: true, amountSats, preimage, data };
  }

  async previewL402(url) {
    const response = await fetch(url);
    if (response.status !== 402) return { requiresPayment: false };

    const { decode } = await import("light-bolt11-decoder");
    const challenge = await response.json();
    const invoice = challenge.invoice || challenge.payment_request;
    const decoded = decode(invoice);
    const amountSection = decoded.sections.find((s) => s.name === "amount");

    return {
      requiresPayment: true,
      amountSats: Math.ceil(Number(amountSection.value) / 1000),
      invoice,
      macaroon: challenge.macaroon,
    };
  }

  onTransferReceived(callback) {
    this.#wallet.on("transfer:claimed", callback);
  }

  onDepositConfirmed(callback) {
    this.#wallet.on("deposit:confirmed", callback);
  }

  cleanup() {
    this.#wallet.cleanupConnections();
  }
}

// Usage
const { agent } = await SparkAgent.create(process.env.SPARK_MNEMONIC);
const identity = await agent.getIdentity();
console.log("Address:", identity.address);

const { sats } = await agent.getBalance();
console.log("Balance:", sats.toString(), "sats");

agent.cleanup();
```

## 错误处理

```javascript
try {
  await wallet.transfer({
    receiverSparkAddress: "sp1p...",
    amountSats: 1000,
  });
} catch (error) {
  switch (error.constructor.name) {
    case "ValidationError":
      console.log("Invalid input:", error.message);
      break;
    case "NetworkError":
      console.log("Network issue:", error.message);
      break;
    case "AuthenticationError":
      console.log("Auth failed:", error.message);
      break;
    case "ConfigurationError":
      console.log("Config problem:", error.message);
      break;
    case "RPCError":
      console.log("RPC error:", error.message);
      break;
    default:
      console.log("Error:", error.message);
  }
}
```

错误类型：
- **ValidationError**——参数无效、地址格式错误
- **NetworkError**——连接失败、超时
- **AuthenticationError**——密钥/Token问题
- **ConfigurationError**——配置缺失、初始化问题
- **RPCError**——gRPC通信失败

## 安全最佳实践

### 代理拥有完全的钱包访问权限

任何拥有助记词的代理或进程都可以**无限制地控制**钱包——它可以检查余额、创建发票并将资金发送到任何地址。没有权限限制，没有支出限制，也没有只读模式。

这意味着：
- 如果助记词泄露，所有资金都会立即处于风险之中
- 如果代理被攻破，攻击者将拥有相同的完全访问权限
- 没有办法在不将资金转移到新钱包的情况下撤销访问权限

### 保护助记词

1. **离线备份助记词**——将其写在纸上或使用硬件备份。如果丢失了助记词，资金将永久丢失。
2. **永远不要在代码、日志、git历史记录或错误消息中暴露助记词**
3. **使用环境变量**——永远不要在源代码中硬编码助记词
4. **将`.env`添加到`.gitignore`中**——防止意外提交秘密

### 将资金转移到更安全的钱包

**不要在代理钱包中积累大量资金。** 代理钱包是一个热钱包，助记词存储在环境变量中——这属于高风险操作。
- 定期将赚取的资金转移到更安全的钱包（硬件钱包、冷存储或您直接控制的独立钱包）
- 仅在Spark上保留代理所需的最低运营余额
- 使用`wallet.transfer()`或`wallet.withdraw()`定期转移资金
- 当余额超过一定阈值时，考虑自动转移资金

### 操作安全

1. **为不同的代理使用不同的助记词**——永远不要在多个代理之间共享助记词
2. **如果需要使用同一个助记词创建多个钱包，请使用不同的`accountNumber`值**
3. **通过事件监听器监控转账**以检测异常的支出活动
4. **在不再需要钱包时调用`cleanupConnections()`**
5. **在开发和使用REGTEST时仅用于测试，在生产环境中仅使用MAINNET**
6. **在代理逻辑中实现应用级别的支出控制**——设置每次交易和每天的金额限制，因为SDK不会自动执行这些操作

## L402协议（Lightning支付墙）

L402（以前称为LSAT）是一种利用Lightning支付来货币化API和内容的协议。当服务器返回HTTP 402（Payment Required）时，它会包含一个Lightning发票。支付发票后，获取预图像，然后再次尝试请求，并附带包含支付证明的授权头。

### L402的工作原理

1. **请求** → 客户端获取受保护的URL
2. **402响应** → 服务器返回 `{invoice, macaroon}`
3. **支付发票** → 客户端支付Lightning发票，接收预图像
4. **再次尝试并附带授权** → 客户端再次尝试，附带`Authorization: L402 <macaroon>:<preimage>`
5. **200响应** → 服务器返回受保护的内容

### L402实现

```javascript
import { decode } from "light-bolt11-decoder";

async function fetchWithL402(wallet, url, options = {}) {
  const { method = "GET", headers = {}, body, maxFeeSats = 10 } = options;

  // Step 1: Make initial request
  const initialResponse = await fetch(url, {
    method,
    headers: { "Content-Type": "application/json", ...headers },
    body: body ? JSON.stringify(body) : undefined,
  });

  // If not 402, return response directly
  if (initialResponse.status !== 402) {
    const contentType = initialResponse.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      return { paid: false, data: await initialResponse.json() };
    }
    return { paid: false, data: await initialResponse.text() };
  }

  // Step 2: Parse 402 challenge
  const challenge = await initialResponse.json();
  const invoice = challenge.invoice || challenge.payment_request || challenge.pr;
  const macaroon = challenge.macaroon || challenge.token;

  if (!invoice || !macaroon) {
    throw new Error("Invalid L402 response: missing invoice or macaroon");
  }

  // Step 3: Decode invoice to get amount
  const decoded = decode(invoice);
  const amountSection = decoded.sections.find((s) => s.name === "amount");
  if (!amountSection?.value) {
    throw new Error("L402 invoice has no amount");
  }
  const amountSats = Math.ceil(Number(amountSection.value) / 1000);

  // Step 4: Pay the invoice
  const payResult = await wallet.payLightningInvoice({
    invoice,
    maxFeeSats,
  });

  // Get preimage (may need to poll if payment is async)
  let preimage = payResult.paymentPreimage;
  if (!preimage && payResult.status === "LIGHTNING_PAYMENT_INITIATED") {
    // Poll for completion
    for (let i = 0; i < 15; i++) {
      await new Promise((r) => setTimeout(r, 500));
      const status = await wallet.getLightningSendRequest(payResult.id);
      if (status?.paymentPreimage) {
        preimage = status.paymentPreimage;
        break;
      }
      if (status?.status === "LIGHTNING_PAYMENT_FAILED") {
        throw new Error("L402 payment failed");
      }
    }
  }

  if (!preimage) {
    throw new Error("L402 payment succeeded but no preimage available");
  }

  // Step 5: Retry with L402 authorization
  const finalResponse = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `L402 ${macaroon}:${preimage}`,
      ...headers,
    },
    body: body ? JSON.stringify(body) : undefined,
  });

  const contentType = finalResponse.headers.get("content-type") || "";
  let data;
  if (contentType.includes("application/json")) {
    data = await finalResponse.json();
  } else {
    data = await finalResponse.text();
  }

  return {
    paid: true,
    amountSats,
    preimage,
    data,
  };
}
```

### 预览L402费用（无需支付）

```javascript
async function previewL402(url) {
  const response = await fetch(url);

  if (response.status !== 402) {
    return { requiresPayment: false };
  }

  const challenge = await response.json();
  const invoice = challenge.invoice || challenge.payment_request;

  const decoded = decode(invoice);
  const amountSection = decoded.sections.find((s) => s.name === "amount");
  const amountSats = Math.ceil(Number(amountSection.value) / 1000);

  return {
    requiresPayment: true,
    amountSats,
    invoice,
    macaroon: challenge.macaroon,
  };
}
```

### 添加到SparkAgent类

```javascript
// Add to the SparkAgent class
async fetchL402(url, options = {}) {
  return await fetchWithL402(this.#wallet, url, options);
}

async previewL402(url) {
  return await previewL402(url);
}
```

### 使用示例

```javascript
const { agent } = await SparkAgent.create(process.env.SPARK_MNEMONIC);

// Check cost first
const preview = await agent.previewL402("https://api.example.com/paid-endpoint");
console.log("Cost:", preview.amountSats, "sats");

// Pay and fetch
const result = await agent.fetchL402("https://api.example.com/paid-endpoint", {
  maxFeeSats: 10,
});
console.log("Paid:", result.paid, "Data:", result.data);

agent.cleanup();
```

### 所需依赖项

```bash
npm install light-bolt11-decoder
```

### L402提供商

| 提供商 | 描述 | URL |
|----------|-------------|-----|
| Lightning Faucet | 测试L402端点（21 sat的笑话） | https://lightningfaucet.com/api/l402/joke |
| Sulu | AI图像生成 | https://rnd.ln.sulu.sh（可能需要API密钥） |
| 各种API | 不断增长的生态系统 | https://github.com/lnurl/awesome-lnurl#l402 |

### Token缓存

L402 token（macaroon + preimage）通常可以多次用于同一域的请求。按域名缓存token，并优先尝试缓存的token：

```javascript
const tokenCache = new Map();

async function fetchWithL402Cached(wallet, url, options = {}) {
  const domain = new URL(url).host;
  const cached = tokenCache.get(domain);

  if (cached) {
    // Try cached token first
    const response = await fetch(url, {
      method: options.method || "GET",
      headers: {
        "Authorization": `L402 ${cached.macaroon}:${cached.preimage}`,
        ...options.headers,
      },
    });

    if (response.status !== 402 && response.status !== 401) {
      return { paid: false, cached: true, data: await response.json() };
    }
    // Token expired, delete and pay again
    tokenCache.delete(domain);
  }

  // Pay for new token
  const result = await fetchWithL402(wallet, url, options);

  // Cache the token
  if (result.paid) {
    tokenCache.set(domain, {
      macaroon: result.macaroon,
      preimage: result.preimage,
    });
  }

  return result;
}
```

## 资源

- Spark文档：https://docs.spark.money
- Spark SDK（npm）：https://www.npmjs.com/package/@buildonspark/spark-sdk
- Sparkscan浏览器：https://sparkscan.io
- Spark CLI：https://docs.spark.money/tools/cli
- L402规范：https://docs.lightning.engineering/the-lightning-network/l402