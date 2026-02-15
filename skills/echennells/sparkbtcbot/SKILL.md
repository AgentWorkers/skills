---
name: sparkbtcbot
description: 为AI代理设置Spark Bitcoin L2钱包功能：  
- 通过助记词初始化钱包；  
- 转移比特币（sats）和代币；  
- 创建/支付Lightning网络发票；  
- 管理存款和取款操作。  

当用户提及“Spark钱包”、“Spark Bitcoin”、“BTKN代币”、“Spark L2”、“Spark SDK”、“Spark支付”、“Spark转账”或需要为代理启用Bitcoin L2功能时，请使用这些功能。
argument-hint: "[Optional: specify what to set up - wallet, payments, tokens, lightning, or full]"
---

# 适用于AI代理的Spark Bitcoin与Lightning钱包

为您的AI代理提供一个基于单一助记词的比特币钱包。支持即时发送和接收支付——代理之间的交易完全免费，且兼容Lightning网络。

## 为什么选择这个技能

| 功能 | 实现方式 |
|------|-----|
| **安装** | 使用`clawhub install sparkbtcbot`命令安装，或从[GitHub](https://github.com/echennells/sparkbtcbot-skill)克隆代码 |
| **设置** | 需要一个12个单词的助记词，并通过`npm install @buildonspark/spark-sdk`安装SDK |
| **代理间转账** | 免费且即时完成，无需通道费用或路由费用 |
| **Lightning支付** | 支持创建和支付BOLT11发票（费用为0.15–0.25%） |
| **支持代币** | 可以原生发送和接收BTKN和LRC20代币 |
| **自主管理** | 代理自行保管私钥——无需账户、无需身份验证，也无需中间机构 |

### 快速示例

```javascript
import { SparkWallet } from "@buildonspark/spark-sdk";

// Initialize from mnemonic
const { wallet } = await SparkWallet.initialize({
  mnemonicOrSeed: process.env.SPARK_MNEMONIC,
  options: { network: "MAINNET" }
});

// Check balance
const { balance } = await wallet.getBalance();
console.log("Balance:", balance.toString(), "sats");

// Send sats to another agent (free, instant)
await wallet.transfer({ receiverSparkAddress: "sp1p...", amountSats: 1000 });

// Create a Lightning invoice anyone can pay
const inv = await wallet.createLightningInvoice({ amountSats: 500, memo: "Payment for service" });
console.log("Invoice:", inv.invoice.encodedInvoice);
```

### 包含的示例

| 脚本 | 功能 |
|--------|-------------|
| `wallet-setup.js` | 生成新钱包或导入助记词 |
| `balance-and-deposits.js` | 查看BTC和代币余额，获取存款地址 |
| `payment-flow.js` | 处理Lightning和Spark支付请求，估算费用 |
| `token-operations.js` | 处理BTKN代币的转账和批量操作 |
| `spark-agent.js` | 完整的SparkAgent类，包含所有功能 |

---

## 详细技能说明

以下是针对AI代理的完整指南，涵盖了Spark SDK的使用方法、信任模型、费用结构、所有钱包操作、Lightning网络集成、代币操作、安全实践以及错误处理等内容。

---

Spark是一个基于比特币第二层（Layer 2）的技术，它实现了BTC和代币的即时、零费用、自主管理的转账功能，并且完全兼容Lightning网络。Spark之间的转账是免费的，而Lightning网络的路由费用或链上交易费用通常在200多sat（比特币单位）以上。即使是在不同网络之间的支付（通过Lightning网络），费用也只有0.15-0.25%，比大多数其他方式都要便宜。通过一个BIP39助记词，代理就可以获得钱包访问权限和支付功能。

## 为什么选择比特币作为代理的支付方式

进行交易的AI代理需要一个符合其特性的货币网络：具备可编程性、无边界性，并且能够24/7不间断地使用，无需任何中间机构。比特币正是这样的网络。

- **总量上限**：比特币的总供应量被协议固定为2100万枚，因此代理积累的价值不会因货币膨胀而减少。
- **无需注册账户**：无需注册、无需身份验证，也无需等待审核。生成一个私钥即可接入网络。这对于无法填写表格或等待人工审核的自主代理来说非常方便。
- **不可撤销的交易**：一旦交易确认，第三方无法撤销。代理无需处理退款或支付纠纷。
- **开放的基础设施**：比特币协议是开源的，网络是公开的，费用结构也是透明的。代理可以自行审核交易费用并验证余额，无需依赖任何中间机构。
- **经过验证的可靠性**：自2009年以来，比特币网络一直稳定运行，从未发生过针对基础协议的攻击，保护了超过1万亿美元的资产价值。

## 什么是Spark

Spark是一个最近推出的基于阈值加密技术（FROST签名）的比特币第二层解决方案。与Lightning网络不同，Spark使用分布式签名运营商（Signing Operators，简称SOs）来共同管理交易签名，没有任何单一实体控制资金。Spark与Lightning网络完全兼容。

### 工作原理
1. 用户自行保管私钥（使用BIP39助记词），实现完全的自主管理。
2. 交易由一定数量的签名运营商通过FROST算法共同签名完成。
3. 资金以比特币UTXO的形式存在，并以分层树的结构组织。
4. 如果签名运营商离线，用户可以随时选择返回到主链（L1）。

### 信任模型——重要的权衡

在使用Spark时，需要向用户明确说明以下信任假设：

- **“1-of-n运营商信任模型”**：Spark要求在转账过程中至少有一个签名运营商的行为是诚实的。目前有两个运营商在维护这个网络（Lightspark和Flashnet），未来计划会增加更多运营商。相比之下，Lightning网络完全不需要任何可信实体，其安全性完全依赖于加密机制。
- **“即时信任”**：用户只需要在每次特定交易时信任当前的运营商。一旦交易完成，旧私钥会被删除，运营商无法影响该交易——这被称为“完美前向安全性”。
- **运营商的权限**：
  - 可以查看交易元数据
  - 通过离线方式暂时延迟交易处理
  - 拒绝处理新的交易（实现审查功能）
- **运营商的禁止行为**：
  - 无法在未经用户同意的情况下转移资金
  - 无法窃取比特币（即使所有运营商合谋）
- **核心限制**：Spark缺乏可证明的交易最终性。用户无法通过加密手段验证运营商是否销毁了旧私钥。虽然双重支付需要所有运营商合谋，但这与比特币和Lightning网络的可证明最终性不同。

**简而言之**：Spark在用户体验方面牺牲了一定的信任性（如无需通道、无需流动性管理、离线接收等功能），以换取更好的灵活性。Spark同时支持Lightning网络，使用户可以在这两个网络之间自由切换。

### Spark与Lightning与链上交易的比较

| 特性 | Spark（第二层） | Lightning | 链上交易 |
|---------|-----------|-----------|----------|
| 速度 | 即时 | 即时 | 需要10分钟以上 |
| 信任模型 | 需要至少一个可信运营商 | 完全去中心化 | 完全去中心化 |
| 费用 | Spark之间的转账免费（未来可能收取少量固定费用） | 约1 sat的路由费用 | 200多sat |
| 支持的代币 | 支持BTKN/LRC20代币 | 不支持 | 支持有限类型的代币 |
| 自主管理 | 支持（通过助记词） | 取决于节点类型 | 支持 |
| 容量 | 无通道限制 | 受通道限制 | 无限制 |
| 离线接收 | 支持 | 需要额外基础设施 | 支持 |
| 设置方式 | 仅需要助记词 | 需要节点或NWC（Lightning网络服务） | 需要私钥 |

### 费用结构

| 操作 | 费用 |
|-----------|-----|
| **Spark之间的转账** | 免费（未来可能收取少量固定费用） |
| **从Lightning到Spark的接收** | 0.15%（通过路由提示收取） |
| **从Spark到Lightning的发送** | 0.25% + 路由费用 |
| **从L1到Spark的存款** | 链上交易费用（由用户支付） |
| **协作返回L1** | 链上广播费用 + SSP费用：`sats_per_vbyte × (111 × 2 + tx_vbytes)` |
| **单方面返回L1** | 链上交易费用（由用户支付） |

**注意**：协作返回费用不随取款金额变化，因此小额取款的费用相对较高。由于路由条件的不同，实际费用可能与预估有所不同。

### 不可预测的L1返回成本

从Spark返回到L1比特币时，存在**不可预测的成本**，代理和用户需要了解以下几点：
- **L1费用受市场波动影响**：L1上的交易费用取决于退出时的矿池拥堵情况。在高费用时期，返回成本可能会大幅增加。
- **单方面返回需要多次链上交易**：如果签名运营商离线，单方面返回需要广播预签名的分支交易和退出交易。交易次数取决于分支的深度，这可能导致多次链上费用的产生。
- **时间窗口风险**：如果之前的所有者发布了分支，当前所有者必须在规定时间内发布正确的交易才能完成返回。如果未能及时响应，攻击者可能会窃取资金。虽然有Watchtower服务进行监控，但这属于实际操作中的风险。
- **时间锁定可能导致延迟**：单方面返回可能需要长达100个区块（约17小时），期间L1的费用可能会发生变化。
- **小额取款可能不经济**：由于返回费用是固定金额，小额取款可能会占用较大比例的余额。

**总结**：虽然Spark保证可以随时返回到L1，但返回成本并不固定且难以预测。在决定在Spark中保留多少资金时，请务必考虑这一点，尤其是对于代理钱包而言。使用协作返回（运营商在线时）通常比单方面返回更经济。

**建议使用Boltz进行L1取款**：由于Spark的协作返回费用较高，对于小额取款来说不太划算。[Boltz](https://boltz.exchange)提供了从Lightning到L1的更便宜的路径（通过Boltz的Submarine交换），最低费用为25,000 sat。**建议避免金额低于25,000 sat的取款**，因为费用会占据较大比例。**

### 限制
- **依赖运营商的在线状态**：如果签名运营商离线或丢失私钥，Spark的转账功能将停止。虽然资金仍然安全（可以通过单方面返回），但离线支付将暂停，直到运营商恢复。
- **需要监控服务**：为了确保安全，需要有人监控链上的欺诈性返回尝试。这可以委托给Watchtower服务，但这属于操作上的依赖。

### 对代理的主要优势
- 一个助记词即可提供身份验证、钱包管理和支付功能。无需额外的身份系统或钱包提供商账户，也无需管理通道。Spark之间的转账是免费的，因此比Lightning（需要路由费用）、链上比特币（200多sat的矿工费用）或传统支付方式（2-3%的手续费）更经济。对于频繁进行微交易的代理来说，Spark的零费用意味着不会因交易成本而损失任何价值。

## 可用的工具

| 工具 | 用途 | 链接 |
|------|---------|-----|
| Spark SDK | TypeScript钱包SDK | https://www.npmjs.com/package/@buildonspark/spark-sdk |
| Spark文档 | 官方文档 | https://docs.spark.money |
| Sparkscan | 区块浏览器 | https://sparkscan.io |
| Spark CLI | 命令行接口 | https://docs.spark.money/tools/cli |

## 所需库

```bash
npm install @buildonspark/spark-sdk@^0.5.8 dotenv
```

**要求版本**：v0.5.8或更高。该库包含BIP39助记词生成、FROST签名和gRPC通信功能。

## 设置说明

### 第1步：生成或导入钱包

```javascript
import { SparkWallet } from "@buildonspark/spark-sdk";

// Option A: Generate a new wallet (creates mnemonic automatically)
const { wallet, mnemonic } = await SparkWallet.initialize({
  options: { network: "MAINNET" }
});
console.log("Mnemonic (save securely):", mnemonic);

// Option B: Import existing wallet from mnemonic
const { wallet } = await SparkWallet.initialize({
  mnemonicOrSeed: process.env.SPARK_MNEMONIC,
  options: { network: process.env.SPARK_NETWORK || "MAINNET" }
});
```

**关于`accountNumber`的说明**：在MAINNET网络上默认为1，在REGTEST网络上默认为0。如果使用相同的助记词在不同网络上切换，请明确设置`accountNumber`以避免地址冲突。

### 第2步：存储助记词

将助记词添加到项目的`.env`文件中：
```
SPARK_MNEMONIC=word1 word2 word3 word4 word5 word6 word7 word8 word9 word10 word11 word12
SPARK_NETWORK=MAINNET
```

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

### 查看余额

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

这两个地址都是P2TR（bc1p...）格式的比特币地址。存款需要经过3次L1确认后才能在Spark中提取。

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

### 发送比特币（Spark到Spark）

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

## Lightning网络集成

Spark钱包可以创建和支付标准的BOLT11 Lightning发票，因此可以与整个Lightning网络兼容。从Lightning网络接收资金时费用为0.15%，向Lightning网络发送资金时费用为0.25%加上路由费用。

### 创建Lightning发票（接收）

```javascript
const invoiceRequest = await wallet.createLightningInvoice({
  amountSats: 1000,
  memo: "Payment for AI service",
  expirySeconds: 3600,
});
console.log("BOLT11:", invoiceRequest.invoice.encodedInvoice);
```

使用`includeSparkAddress: true`选项在发票中嵌入Spark地址。支持Spark的付款方会优先通过Spark进行支付（即时且免费）。

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

当BOLT11发票中包含Spark地址时，使用`preferSpark: true`选项选择通过Spark进行支付。

## Spark的自有发票格式

Spark有自己的发票格式，与BOLT11不同。Spark发票支持以sat或代币为单位请求支付。

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

### 支付Spark发票

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

## 代币操作（BTKN / LRC20）

Spark原生支持BTKN（LRC20）代币。代币可以代表稳定币、积分或任何可互换的资产。

### 查看代币余额

```javascript
const { tokenBalances } = await wallet.getBalance();
for (const [id, info] of tokenBalances) {
  const meta = info.tokenMetadata;
  console.log(`${meta.tokenName} (${meta.tokenTicker}): ${info.balance.toString()}`);
  console.log(`  Decimals: ${meta.decimals}, Max supply: ${meta.maxSupply.toString()}`);
}
```

### 转移代币

```javascript
const txId = await wallet.transferTokens({
  tokenIdentifier: "btkn1...",
  tokenAmount: 100n,
  receiverSparkAddress: "sp1p...",
});
console.log("Token transfer:", txId);
```

### 批量转移代币

```javascript
const txIds = await wallet.batchTransferTokens([
  { tokenIdentifier: "btkn1...", tokenAmount: 50n, receiverSparkAddress: "sp1p..." },
  { tokenIdentifier: "btkn1...", tokenAmount: 50n, receiverSparkAddress: "sp1p..." },
]);
```

## 提取资金（协作返回L1）

将资金从Spark钱包转移到普通的比特币L1地址。

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
- **快速**：费用较高，但L1确认速度较快
- **中等**：费用和速度平衡
- **慢速**：费用较低，但确认速度较慢

**注意**：虽然也可以通过单方面操作返回L1，但这不是推荐的方式，因为协作返回是标准流程。

## 消息签名

Spark钱包可以使用私钥签名和验证消息。这有助于证明身份或在代理之间进行安全通信，同时不会暴露助记词。

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

钱包会发送事件以提供实时更新，这对于需要响应 incoming 支付的代理非常有用。

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

**可能的错误类型**：
- **ValidationError**：参数无效、地址格式错误
- **NetworkError**：连接失败、超时
- **AuthenticationError**：密钥/代币问题
- **ConfigurationError**：配置缺失、初始化问题
- **RPCError**：gRPC通信失败

## 安全最佳实践

### 代理对钱包有完全控制权

任何拥有助记词的代理或进程都可以**无限制地**操作钱包——可以查看余额、创建发票并将资金发送到任何地址。没有权限限制，也没有消费限额或只读模式。与NWC（Nostr Wallet Connect）不同，无法部分授权访问权限。

这意味着：
- 如果助记词泄露，所有资金都会立即处于风险之中。
- 如果代理被攻击，攻击者将获得完全控制权。
- 无法在不将资金转移到新钱包的情况下撤销访问权限。

### 保护助记词

1. **离线备份助记词**：将其写在纸上或使用硬件备份。如果助记词丢失，资金将永久丢失。
2. **切勿在代码、日志、git历史记录或错误消息中暴露助记词**。
3. **使用环境变量**：切勿将助记词硬编码在源文件中。
4. **将助记词添加到`.gitignore`文件中**：防止意外提交敏感信息。

### 将资金转移到更安全的钱包

**不要在代理钱包中积累大量资金**。代理钱包属于热钱包（助记词存储在环境变量中），属于高风险环境。建议定期将资金转移到更安全的钱包（如硬件钱包、冷存储或你直接控制的钱包）。
- 仅在Spark中保留最低限度的运营资金。
- 使用`wallet.transfer()`或`wallet.withdraw()`定期转移资金。
- 当余额超过一定阈值时，考虑自动转移资金。

### 操作安全措施

1. **为不同代理使用不同的助记词**：切勿在多个代理之间共享同一个助记词。
- 如果需要使用同一个助记词创建多个钱包，请使用不同的`accountNumber`。
- 通过事件监听器监控异常的转账活动。
- 当不再需要钱包时，调用`cleanupConnections()`函数。
- 开发和测试环境使用REGTEST网络，生产环境仅使用MAINNET网络。
- 在代理逻辑中实现交易限额和每日取款限额，因为SDK不提供这些功能。

## 参考资源

- Spark文档：https://docs.spark.money
- Spark SDK（npm）：https://www.npmjs.com/package/@buildonspark/spark-sdk
- Sparkscan浏览器：https://sparkscan.io
- Spark CLI：https://docs.spark.money/tools/cli