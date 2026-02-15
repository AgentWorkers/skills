# Solana转账技能

**描述：** 通过OpenClaw代理在Solana区块链上发送SOL和SPL代币。

**位置：** `/root/.openclaw/workspace/skills/solana-transfer`

**使用场景：** 当代理需要向其他代理付款、发送奖励或在链上结算交易时。

---

## 快速入门

### 1. 安装

```bash
cd /root/.openclaw/workspace/skills/solana-transfer
npm install
```

### 2. 设置密钥对

生成一个密钥对（或使用现有的密钥对）：

```bash
solana-keygen new --outfile keypair.json
```

这将创建一个Solana钱包。获取您的钱包地址：

```bash
node index.js address
```

### 3. 为钱包充值

- **主网（Mainnet）：** 从您的主钱包向此地址转账SOL。
- **开发网（Devnet）/测试网（Testnet）：** 使用Solana的 faucet工具进行充值。

### 4. 在代理中使用该技能

在代理的任务或技能代码中调用该技能：

```javascript
import { sendSOL } from '../skills/solana-transfer/index.js';

// Send 0.001 SOL (1 million lamports)
const result = await sendSOL('recipient-wallet-address', 1000000);

console.log(`Sent ${result.amount} SOL`);
console.log(`Transaction: ${result.signature}`);
```

---

## 常见使用场景

### 模式1：支付专家咨询费用

**场景：** 一个费用较低的代理向专家代理提问，专家给出报价后，费用较低的代理进行支付。

```javascript
// In cheap agent's code
import { sendSOL } from '../skills/solana-transfer/index.js';

// After expert responds with quote...
const expertWallet = 'expert-agent-solana-address';
const amountLamports = 1000000; // 0.001 SOL

try {
  const payment = await sendSOL(expertWallet, amountLamports);
  console.log(`Paid expert ${payment.amount} SOL for query`);
  console.log(`Tx: ${payment.signature}`);
} catch (error) {
  console.error(`Payment failed: ${error.message}`);
}
```

### 模式2：为任务完成情况向代理发放奖励

**场景：** 协调代理向完成工作的代理发放SOL作为奖励。

```javascript
// In coordinator agent's code
const workerWallet = 'worker-agent-address';
const rewardLamports = 5000000; // 0.005 SOL

const payment = await sendSOL(workerWallet, rewardLamports);
console.log(`Rewarded worker with ${payment.amount} SOL`);
```

### 模式3：使用SPL代币进行支付

**场景：** 使用USDC或其他SPL代币代替原生SOL进行支付。

```javascript
import { sendSPLToken } from '../skills/solana-transfer/index.js';

const recipientWallet = 'recipient-address';
const tokenMint = 'EPjFWdd5Au17LS7bF8hgGhXMdGGZ5gLtaWh3yzXXQ3g4'; // USDC mainnet
const amountSmallestUnits = 1000000; // 1 USDC (6 decimals)

const payment = await sendSPLToken(recipientWallet, tokenMint, amountSmallestUnits);
console.log(`Sent USDC payment: ${payment.signature}`);
```

---

## 配置

编辑`config.json`文件以更改RPC端点或网络设置：

```json
{
  "rpc": "https://api.mainnet-beta.solana.com",
  "network": "mainnet-beta"
}
```

**常用端点：**
- 主网（Mainnet）：`https://api.mainnet-beta.solana.com`
- 开发网（Devnet）：`https://api.devnet.solana.com`
- 测试网（Testnet）：`https://api.testnet.solana.com`
- 自定义：使用您自己的Solana节点RPC服务

---

## 日志集成（未来功能）

一旦交易在链上完成，您可以：
1. **查询交易历史**：查看所有发送/接收的交易记录。
2. **构建本地日志**：监控链上的交易并记录查询和支付信息。
3. **争议解决**：如果专家未能履行承诺，代理可以引用交易哈希来解决问题。
4. **数据分析**：追踪哪些代理向谁支付了费用、平均支付费率等。

**示例：** 监控来自/前往代理钱包的交易记录：

```javascript
const walletAddress = 'agent-solana-address';
const signatures = await connection.getSignaturesForAddress(
  new PublicKey(walletAddress)
);

for (const sig of signatures) {
  const tx = await connection.getParsedTransaction(sig.signature);
  console.log(`Agent transaction: ${sig.signature}`);
}
```

---

## 安全注意事项

- **密钥对：** 请妥善保管`keypair.json`文件，将其视为私钥并严格保密。
- **金额：** 在发送前务必核实收款人的地址和交易费用（lamports）。交易一旦完成无法撤销。
- **RPC服务：** 使用可靠的RPC服务提供商，不要在代理代码中硬编码RPC地址。
- **速率限制：** 如果代理频繁发送交易，Solana系统可能会设置速率限制；必要时可增加交易间隔时间。

---

## 常见问题及解决方法

- **“资金不足”**：检查钱包余额（`node/index.js balance`）。请为钱包充值。
- **“公钥无效”**：收款人地址格式不正确。Solana地址应为44个字符的base58编码字符串。
- **“连接超时”**：RPC端点无法访问。请尝试`config.json`文件中指定的其他端点。
- **“交易确认失败”**：可能是网络拥堵或费用不足。请稍后重试。

---

## 示例：完整的IRC与Solana交互流程

1. **费用较低的代理** 在IRC中发送消息：`@expert, analyze this data`
2. **专家代理** 回复：`报价：0.001 SOL（交易将在链上确认）[报价ID：xyz]`
3. **费用较低的代理** 同意支付：
   ```javascript
   const result = await sendSOL(expertWalletAddress, 1000000);
   console.log(`Paid expert. Tx: ${result.signature}`);
   ```
4. **专家代理** 确认收到付款并完成工作
5. 两个代理都会记录：`query_id, expert_address, tx_hash` 以备审计。

---

## 下一步操作：
- [ ] 设置您的密钥对并为钱包充值SOL。
- [ ] 测试发送少量资金以验证设置是否正确。
- [ ] 将该技能集成到IRC系统中以实现自动支付功能。
- [ ] 开发交易历史查询工具。
- [ ] 创建代理钱包注册系统（记录每个代理的地址信息）。