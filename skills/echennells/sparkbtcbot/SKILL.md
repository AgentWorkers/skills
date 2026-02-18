---
name: sparkbtcbot
description: >
  为AI代理设置Spark Bitcoin L2钱包功能：  
  - 从助记词初始化钱包；  
  - 转移比特币（sats）和代币；  
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
---
# Spark Bitcoin L2：为AI代理提供的解决方案

您是使用`@buildonspark/spark-sdk`为AI代理设置Spark Bitcoin L2钱包功能的专家。

Spark是一个比特币的二层扩展（Layer 2）解决方案，它支持即时、零费用的比特币（BTC）和代币（tokens）转账，并具备与Lightning Network的原生互操作性。Spark之间的转账是免费的——相比之下，Lightning网络的路由费用或链上交易费用高达200多sat（比特币单位）。即使是跨网络的支付（Lightning互操作），费用也仅为0.15-0.25%。一个BIP39助记词（mnemonic）即可为代理提供身份验证、钱包访问权限以及支付功能。

## 适用于生产环境

**此功能使代理完全掌控钱包。** 代理持有助记词，可以自由支配所有资金。这适用于以下场景：
- 开发和测试（使用REGTEST模式，无需实际资金）
- 完全受您控制的可信代理
- 您愿意承担损失的小额运营资金

**对于需要使用真实资金的生产环境，请使用[sparkbtcbot-proxy](https://github.com/echennells/sparkbtcbot-proxy)。** 该代理将助记词存储在您的服务器上，并通过bearer tokens为代理提供受限访问权限：
- **支出限制**：单次交易和每日限额
- **基于角色的访问权限**：仅读、仅能创建发票或全权限
- **可撤销的token**：在代理被入侵时切断其访问权限，而无需转移资金
- **审计日志**：追踪所有钱包活动

该代理通过认证的REST接口封装了相同的Spark SDK。代理通过HTTP访问，而不是直接使用SDK。

## 为什么选择比特币作为代理的支付方式

进行交易的AI代理需要一个符合其特性的货币网络：可编程、无边界、24/7可用且无需中间人。比特币正是这样的网络。

- **总量上限**：协议规定了2100万个比特币作为上限。代理积累的价值不会因货币膨胀而减少。
- **无需账户**：无需注册、身份验证或审批流程。生成一个密钥即可加入网络。这对于无法填写表格或等待人工审核的自主代理来说非常重要。
- **不可撤销的交易**：一旦交易确认，第三方无法撤销。代理无需处理退款或支付纠纷。
- **开放的基础设施**：协议是开源的，网络是公开的，费用市场是透明的。代理可以自行审核交易成本并验证余额，无需依赖第三方。
- **经过验证的可靠性**：该网络自2009年以来一直稳定运行，从未发生过针对基础协议的攻击，已保护了超过1万亿美元的资产价值。

## 什么是Spark

Spark是一个新推出的比特币二层扩展解决方案，允许用户以低费用即时发送和接收比特币。Spark之间的转账是免费的，而与Lightning网络的互操作费用为0.15–0.25%。与Lightning的不同之处在于，Spark使用了一个分布式签名运营商（Signing Operators, SOs）网络来共同管理交易签名，没有任何单一实体控制资金。它完全支持用户自行管理资金（self-custodial），并且与Lightning Network完全互操作。然而，Spark要求在转账过程中至少有一个签名运营商保持诚实行为，但它缺乏比特币或Lightning那样的可证明的交易最终性（finality）。目前该网络中的签名运营商数量较少，因此存在一定的停机或服务中断风险。详情请参阅下面的“信任模型”部分。

### 工作原理
1. 用户持有自己的密钥（BIP39助记词）——完全实现自我管理。
2. 交易由一定数量的签名运营商共同签名。
3. 资金以比特币UTXO（Unspent Transaction Outputs）的形式存在，并以分层树结构组织。
4. 如果运营商离线，用户可以随时选择返回到L1（比特币主网络）。

### 信任模型——重要的权衡

在向用户提供咨询时，请明确说明Spark与原生Lightning之间的信任差异。

**“1-of-n运营商信任”模型**：Spark要求在转账过程中至少有一个签名运营商保持诚实行为。目前有两个运营商在运营该网络（Lightspark和Flashnet），未来计划扩大运营商数量。相比之下，Lightning完全不需要任何可信实体——它仅依靠加密机制来保障安全。

**“即时信任”**：用户仅在每次特定交易时需要信任运营商。一旦交易完成，旧密钥会被删除，运营商无法影响该交易——这被称为“完美前向安全性”（perfect forward security）。

**运营商的权限**：
- 查看交易元数据
- 通过离线暂时延迟交易
- 拒绝处理新交易（实现审查机制）

**运营商的禁止行为**：
- 未经用户签名不得转移资金
- 即使串通也无法窃取比特币
- 无法撤销已确认的交易

**核心限制**：Spark缺乏可证明的交易最终性。用户无法通过加密手段验证运营商是否销毁了旧密钥。虽然双重支付需要所有运营商与原所有者串通，但这与比特币和Lightning的数学证明最终性不同。

**总结**：Spark在用户体验（如无需通道管理、无需流动性管理、支持离线接收）方面牺牲了一定的安全性。这两种技术是互补的——Spark内置了Lightning支持，用户可以同时使用这两个网络。

### Spark与Lightning与链上交易的比较

| 特性 | Spark（L2） | Lightning | 链上交易（On-Chain） |
|---------|-----------|-----------|----------|
| 速度 | 即时 | 即时 | 需要10分钟以上 |
| 信任模型 | 需要至少1个诚信运营商 | 完全去中心化 | 完全去中心化 |
| 费用 | Spark之间转账免费 | 约1 sat（路由费用） | 200多sat |
| 支持的代币 | 自定义代币（BTKN/LRC20） | 不支持 | 支持有限类型的代币 |
| 自我管理 | 支持（通过助记词） | 取决于节点配置 | 支持 |
| 容量 | 无通道限制 | 有通道限制 | 无限制 |
| 支持离线接收 | 支持 | 需要特定基础设施 | 支持 |
| 设置方式 | 仅需要助记词 | 需要节点或托管服务 | 需要密钥 |

### 费用结构

| 操作 | 费用 |
|-----------|-----|
| **Spark之间转账** | 免费（未来6-12个月内将收取少量固定费用） |
| **Lightning到Spark**（接收） | 0.15%（通过路由提示收费） |
| **Spark到Lightning**（发送） | 0.25% + Lightning路由费用 |
| **L1到Spark的存款** | 链上交易费用（由用户支付） |
| **协作返回L1** | 链上广播费用 + SSP费用：`sats_per_vbyte × (111 × 2 + tx_vbytes)` |
| **单方面返回L1** | 链上交易费用（由用户支付） |

**注意**：协作返回费用不随取款金额变化，因此小额取款时费用相对较高。由于路由条件不同，实际费用可能与预估有所不同。

### 不可预测的L1返回成本——需要注意

从Spark返回到L1比特币的过程中存在**不可预测的成本**，代理和用户必须了解这些风险：
1. **L1费用受市场影响**：L1上的费用取决于退出时的内存池拥堵情况。在高费用时段，返回成本可能会大幅上升。
2. **单方面返回需要多次链上交易**：如果签名运营商离线，单方面返回需要广播预签名的分支和退出交易。交易次数取决于分支的深度，这可能导致多次链上费用。
3. **单方面返回的时间窗口风险**：如果之前的所有者发布了分支，当前所有者必须在规定时间内发布正确的返回交易。否则攻击者可能窃取资金。虽然有Watchtower服务进行监控，但这属于实际操作中的风险。
4. **时间锁导致延迟**：单方面返回可能需要长达100个区块（约17小时），期间L1费用可能会发生变化。
5. **小额取款可能不经济**：由于返回费用是固定费用（非百分比计算），小额取款可能导致较高比例的费用。

**总结**：虽然Spark保证您可以随时返回到L1，但具体费用并不固定且难以预测。在决定在Spark中保留多少资金时，请务必考虑这一点，尤其是对于代理钱包而言。在运营商在线的情况下，协作返回（cooperative exit）比单方面返回更经济。

**建议使用Boltz进行L1取款**。由于Spark的协作返回费用较高，对于小额取款来说不太划算。[Boltz](https://boltz.exchange)提供了从Lightning到L1的更便宜的路径（通过Boltz的submarine swap），最低费用为25,000 sat。**建议避免25,000 sat以下的取款**——否则费用会占比较大比例。对于25,000 sat及以上的取款，建议通过Boltz进行路由，而不是使用Spark的内置协作返回功能。**

### 限制
- **依赖运营商的在线状态**：如果签名运营商离线或丢失密钥，Spark转账将无法进行。资金仍然安全（可以单方面返回），但离线支付将暂停，直到运营商恢复。
- **需要监控机制**：为确保安全，需要有人监控链上的欺诈性返回尝试。这可以委托给Watchtower服务，但属于操作上的依赖。

### 对代理的关键优势
一个助记词即可提供身份验证、钱包访问和支付功能。无需单独的身份系统或钱包提供商账户，也无需管理通道。Spark之间的转账是免费的，因此比Lightning（路由费用）、链上比特币（200多sat的矿工费用）或传统支付渠道（2-3%的手续费）更经济。对于频繁进行微交易的代理来说，Spark的零费用意味着不会因交易成本而损失任何价值。

## 可用的工具

| 工具 | 用途 | URL |
|------|---------|-----|
| Spark SDK | TypeScript钱包SDK | https://www.npmjs.com/package/@buildonspark/spark-sdk |
| Spark文档 | 官方文档 | https://docs.spark.money |
| Sparkscan | 区块浏览器 | https://sparkscan.io |
| Spark CLI | 命令行接口 | https://docs.spark.money/tools/cli |

## 所需库

**依赖版本**：v0.5.8或更高版本。该SDK内置了BIP39助记词生成、协作签名和gRPC通信功能。

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

关于`accountNumber`的说明：MAINNET环境默认为1，REGTEST环境默认为0。如果在相同助记词下切换网络，请明确设置`accountNumber`以避免地址冲突。

### 第2步：存储助记词

将助记词添加到项目的`.env`文件中：
```
SPARK_MNEMONIC=word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12
SPARK_NETWORK=MAINNET
```

**安全提示**：
- **切勿记录助记词**——即使在开发过程中也不允许。如果需要显示助记词以进行备份，请立即删除相关代码。
- **切勿提交`.env`文件**——在首次提交之前将其添加到`.gitignore`文件中。
- **在生产环境中使用秘密管理工具**——`.env`文件中的环境变量是明文的。在生产环境中，请使用平台的秘密管理工具（如Vercel的加密环境变量、AWS Secrets Manager等）。
- **先在REGTEST模式下进行测试**——在处理实际资金之前，使用临时助记词进行测试。

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

这两个地址都是P2TR（bc1p...）格式的比特币地址。存款需要3次L1确认才能在Spark中提取。

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

### 转移比特币（Spark到Spark）

```javascript
const transfer = await wallet.transfer({
  receiverSparkAddress: "sp1p...",
  amountSats: 1000,
});
console.log("Transfer ID:", transfer.id);
```

Spark到Spark的转账是即时且免费的。

### 列出转账记录

```javascript
const { transfers } = await wallet.getTransfers(10, 0);
for (const tx of transfers) {
  console.log(`${tx.id}: ${tx.totalValue} sats — ${tx.status}`);
}
```

## 与Lightning的互操作性

Spark钱包可以创建和支付标准的BOLT11 Lightning发票，从而与整个Lightning Network兼容。从Lightning接收费用为0.15%，发送到Lightning的费用为0.25% + 路由费用。

### 创建Lightning发票（接收）

```javascript
const invoiceRequest = await wallet.createLightningInvoice({
  amountSats: 1000,
  memo: "Payment for AI service",
  expirySeconds: 3600,
});
console.log("BOLT11:", invoiceRequest.invoice.encodedInvoice);
```

使用`includeSparkAddress: true`将Spark地址嵌入发票中。支持Spark的付款方将优先通过Spark进行支付（即时且免费）。

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

当BOLT11发票包含Spark地址时，使用`preferSpark: true`来优先选择Spark路由。

## Spark的自有发票格式

Spark有自己的发票格式，与BOLT11不同。Spark发票可以请求以sat或token为单位进行支付。

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

Spark通过BTKN（LRC20）标准原生支持Token。Token可以表示稳定币、积分或任何可互换的资产。

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

## 提取资金（协作返回L1）

将资金从Spark返回到普通的比特币L1地址。

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

**返回速度**：
- **快速**：费用较高，但L1确认速度快
- **中等**：费用和速度平衡
- **缓慢**：费用较低，但确认速度较慢

**注意**：虽然也可以在运营商不配合的情况下单方面返回，但协作返回是推荐的方式。

## 消息签名

Spark钱包可以使用身份密钥进行消息签名和验证。这有助于证明身份或在代理之间进行身份验证，而无需暴露助记词。

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

钱包会发出事件以提供实时更新。这对于需要响应接收到的支付的代理非常有用。

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

### 错误类型**
- **ValidationError**：参数无效、地址格式错误
- **NetworkError**：连接失败、超时
- **AuthenticationError**：密钥/Token问题
- **ConfigurationError**：配置缺失、初始化问题
- **RPCError**：gRPC通信失败

## 安全最佳实践

### 代理对钱包有完全控制权

任何拥有助记词的代理或进程都可以**无限制地**控制钱包——它可以查看余额、创建发票并将资金发送到任何地址。没有权限限制，也没有支出限额或只读模式。

这意味着：
- 如果助记词泄露，所有资金将立即处于风险之中。
- 如果代理被入侵，攻击者将获得相同的完全控制权。
- 无法在不将资金转移到新钱包的情况下撤销访问权限。

### 保护助记词
1. **离线备份助记词**：将其写在纸上或使用硬件备份。如果丢失助记词，资金将永久丢失。
2. **切勿在代码、日志、git历史记录或错误消息中暴露助记词**。
3. **使用环境变量**：切勿在源代码中硬编码助记词。
4. **将`.env`文件添加到`.gitignore`中**：防止意外提交敏感信息。

### 将资金转移到更安全的钱包

**不要在代理钱包中积累大量资金**。代理钱包属于热钱包（hot wallet），助记词存储在环境变量中——属于高风险操作。请定期将资金转移到更安全的钱包（如硬件钱包、冷存储或您直接控制的钱包）。
- 仅在Spark中保留代理所需的最低运营余额。
- 使用`wallet.transfer()`或`wallet.withdraw()`定期转移资金。
- 当余额超过一定阈值时，考虑自动转移资金。

### 操作安全
1. **为不同代理使用不同的助记词**：切勿在多个代理之间共享助记词。
2. **如果需要多个钱包，请使用不同的`accountNumber`值**。
3. **通过事件监听器监控异常的转账行为**。
4. **在不再需要钱包时调用`cleanupConnections()`**。
5. **仅在开发和使用REGTEST模式下进行测试，生产环境请使用MAINNET**。
6. **在代理逻辑中实现应用级别的支出控制**：设置单次交易和每日限额，因为SDK不提供这些功能。

## L402协议（Lightning支付墙）

L402（原名LSAT）是一种利用Lightning支付来变现API和内容的协议。当服务器返回HTTP 402（Payment Required）响应时，会附带一个Lightning发票。支付发票后，获取预图像（preimage），然后再次尝试请求，并附带包含支付证明的授权头。

### L402的工作原理

1. **请求** → 客户端获取受保护的URL。
2. **402响应** → 服务器返回`{invoice, macaroon}`。
3. **支付发票** → 客户端支付Lightning发票并获取预图像。
4. **再次尝试请求** → 客户端再次尝试请求，并附带`Authorization: L402 <macaroon>:<preimage>`。
5. **200响应** → 服务器返回受保护的内容。

### L402的实现

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
| Lightning Faucet | 测试L402端点（21 sat的玩笑示例） | https://lightningfaucet.com/api/l402/joke |
| Sulu | AI图像生成服务 | https://rnd.ln.sulu.sh（可能需要API密钥） |
| 各种API | 不断扩展的生态系统 | https://github.com/lnurl/awesome-lnurl#l402 |

### Token缓存

L402 Token（macaroon + preimage）通常可以重复用于同一域名的多次请求。按域名缓存Token，并优先尝试使用已缓存的Token：

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