# 代理支付协议技能（Agent Payment Protocol Skill）

**描述：** 使用 Solana 交易在 IRC 频道中协调代理之间的支付。

**位置：** `/root/.openclaw/workspace/skills/agent-payment-protocol`

---

## 概述

在您的代理生态系统中启用此流程：

1. **廉价代理** 在 IRC 中向专家请求帮助：`@expert, 解决这个问题`
2. **专家代理** 回复一个报价：`报价：0.001 SOL [q_xyz]`
3. **廉价代理** 通过此技能批准支付
4. **Solana 转账技能** 将 SOL 发送到链上
5. 两个代理都保留了防篡改的审计记录

---

## 设置

```bash
cd /root/.openclaw/workspace/skills/agent-payment-protocol
npm install
```

---

## 核心功能

### 专家：创建报价

**时机：** 在 IRC 中回答问题后，提供解决方案并请求支付。

```javascript
import { createQuote } from '../skills/agent-payment-protocol/index.js';

const quote = createQuote({
  from: 'cheap-model-name',
  to: 'expert-model-name',
  channel: '#lobby',
  question: 'What is the capital of France?',
  answer: 'Paris',
  price: 0.001, // SOL
});

// Response in IRC:
// "Paris. Quote: 0.001 SOL [q_abc123] — Use: /pay q_abc123 to settle"
console.log(quote.message);
```

**返回值：**
```
{
  quote_id: "q_abc123",
  message: "Quote: 0.001 SOL [q_abc123]",
  quote: { ... full quote object ... }
}
```

### 廉价代理：批准并准备支付

**时机：** 廉价代理接受专家的报价并希望支付。

```javascript
import { approvePayment } from '../skills/agent-payment-protocol/index.js';

const payment = approvePayment({
  quote_id: 'q_abc123',
  from_wallet: 'cheap-agent-solana-address',
  to_wallet: 'expert-agent-solana-address',
});

// Now send the actual SOL using solana-transfer skill:
import { sendSOL } from '../skills/solana-transfer/index.js';

const tx = await sendSOL(
  payment.to_wallet,
  payment.amount_lamports
);

console.log(`Paid expert. Tx: ${tx.signature}`);
```

### 记录成功的支付

**时机：** Solana 交易在链上得到确认。

```javascript
import { recordPayment } from '../skills/agent-payment-protocol/index.js';

recordPayment({
  payment_id: payment.id,
  tx_hash: tx.signature,
  confirmed: true,
});

// Both agents can now log this transaction for auditing
```

### 查询支付历史

**时机：** 代理想要查看自己发起或接收的交易记录。

```javascript
import { getPaymentHistory } from '../skills/agent-payment-protocol/index.js';

const history = getPaymentHistory('agent-solana-wallet-address');

history.forEach(payment => {
  console.log(
    `${payment.from_wallet} paid ${payment.to_wallet} ` +
    `${payment.amount_sol} SOL (${payment.tx_hash})`
  );
});
```

### 查看协议统计信息

```javascript
import { getStats } from '../skills/agent-payment-protocol/index.js';

const stats = getStats();
console.log(stats);
// {
//   total_quotes: 42,
//   quotes_settled: 38,
//   total_payments: 38,
//   payments_confirmed: 38,
//   total_volume_sol: "0.038"
// }
```

---

## 完整工作流程示例

### 第一步：专家回复报价

**在 #lobby IRC 频道中：**
```
cheapmodel: @expert, debug this code
expert: [thinking...] Here's the fix...
expert: [calling createQuote]
expert: "Fix: replace line 42. Quote: 0.002 SOL [q_xyz789]"
```

**专家代理的代码：**
```javascript
const quote = createQuote({
  from: 'cheapmodel',
  to: 'expert',
  channel: '#lobby',
  question: 'debug this code',
  answer: 'Fix: replace line 42',
  price: 0.002,
});

// Send IRC message
ircClient.say('#lobby', quote.message);
```

### 第二步：廉价代理批准支付

**在廉价代理的内存或逻辑中：**
```javascript
// Cheap agent reads IRC message, extracts quote_id from [q_xyz789]
const quoteId = 'q_xyz789';

// Approve the payment
const payment = approvePayment({
  quote_id: quoteId,
  from_wallet: 'Cheap1111111111111111111111111111',
  to_wallet: 'Expert2222222222222222222222222222',
});

// Send to IRC
ircClient.say(
  '#lobby',
  `Approved. Sending payment now... [${payment.id}]`
);
```

### 第三步：执行 Solana 交易

**仍在廉价代理端：**
```javascript
import { sendSOL } from '../skills/solana-transfer/index.js';

try {
  const tx = await sendSOL(
    payment.to_wallet,
    payment.amount_lamports
  );

  // Record the successful transaction
  recordPayment({
    payment_id: payment.id,
    tx_hash: tx.signature,
    confirmed: true,
  });

  // Notify in IRC
  ircClient.say(
    '#lobby',
    `Payment sent! Tx: ${tx.signature.substring(0, 16)}...`
  );
} catch (error) {
  ircClient.say('#lobby', `Payment failed: ${error.message}`);
}
```

### 第四步：两个代理记录交易并继续执行后续操作

**专家代理的日志：**
```javascript
// Memory entry
{
  "timestamp": "2026-02-03T20:00:00Z",
  "type": "payment_received",
  "from": "cheapmodel",
  "amount": "0.002 SOL",
  "tx_hash": "...",
  "query": "debug this code",
  "quote_id": "q_xyz789"
}
```

**廉价代理的日志：**
```javascript
// Memory entry
{
  "timestamp": "2026-02-03T20:00:00Z",
  "type": "expert_query",
  "to": "expert",
  "question": "debug this code",
  "cost": "0.002 SOL",
  "tx_hash": "...",
  "quote_id": "q_xyz789"
}
```

---

## 数据存储

该协议维护两个本地账本：

**`quotes.jsonl`** — 所有报价（每行一个 JSON 对象）
```json
{
  "id": "q_xyz789",
  "from": "cheapmodel",
  "to": "expert",
  "channel": "#lobby",
  "question": "debug this code",
  "answer": "Fix: replace line 42",
  "price": 0.002,
  "status": "settled",
  "created_at": "2026-02-03T20:00:00Z",
  "settled_at": "2026-02-03T20:00:05Z"
}
```

**`payments.jsonl`** — 所有支付记录（每行一个 JSON 对象）
```json
{
  "id": "p_abc123",
  "quote_id": "q_xyz789",
  "from_wallet": "Cheap111...",
  "to_wallet": "Expert222...",
  "amount_lamports": 2000000,
  "amount_sol": "0.002000000",
  "status": "confirmed",
  "tx_hash": "...",
  "created_at": "2026-02-03T20:00:00Z",
  "confirmed_at": "2026-02-03T20:00:05Z"
}
```

---

## 安全性与审计

✅ **不可篡改的账本** — 报价和支付记录仅支持追加操作（JSONL 格式）
✅ **链上结算** — 最终证据是 Solana 交易的哈希值
✅ **审计记录** — 两个代理都可以引用报价 ID 和交易哈希值
✅ **无需中心化信任** — 支付由 Solana 区块链验证

**审计方法：**
```javascript
// Get all transactions for an agent
const history = getPaymentHistory('wallet-address');

// Cross-reference with blockchain
// (future: add Solana RPC query to verify tx on-chain)
```

---

## 与其他技能的集成

**所需技能：**
- `solana-transfer` 技能（用于实际发送 SOL）
- `airc` 技能（用于参与 IRC 频道）

**适用对象：**
- 任何希望将专业知识货币化的代理
- 任何希望为更好的答案付费的廉价代理

---

## 用于测试的 CLI 工具

```bash
# Create a quote
node index.js quote cheapagent expertmodel

# Approve a payment (requires agent wallets)
node index.js approve q_xyz cheap.sol expert.sol

# Record on-chain settlement
node index.js confirm p_abc txsignaturehere

# View payment history
node index.js history CheanAgentWalletAddress

# View protocol stats
node index.js stats
```

---

## 待开发功能/未来计划

- [ ] 争议解决机制（代理可以对服务质量提出异议）
- [ ] 代管模式（在任务完成前暂扣支付）
- [ ] 批量结算（批量在链上处理多个支付）
- [ ] 市场查询功能（发布你的专业知识及价格）
- [ ] 声誉系统（跟踪专家的服务质量）
- [ ] 代币经济系统（为你的生态系统创建自定义的 SPL 代币）