---
name: clawpay
version: 1.1.0
description: AI代理的私人支付：发送方与接收方之间没有链上的直接关联（即没有在区块链上记录的交易信息）。
author: clawpay
homepage: https://clawpay.dev
tags: [privacy, payments, railgun, usdt, agents, tips]
metadata:
  emoji: 🦞
  category: payments
  api_base: https://clawpay.dev
---

# ClawPay 🦞

**私密转账服务。收款人会看到资金来自 Railgun，无法追踪到您的账户。**

## 使用方法

**前提条件：** 您需要一个在 BSC 上拥有 USDT 的钱包私钥。

将以下代码保存为 `send-private.mjs`，并通过 `node send-private.mjs` 命令运行它：

```javascript
// send-private.mjs - Copy this entire file and run it
import { Wallet, JsonRpcProvider, Contract, parseUnits } from 'ethers';

// ============ CONFIGURE THESE ============
const PRIVATE_KEY = process.env.WALLET_KEY || '0xYOUR_PRIVATE_KEY';
const RECIPIENT = '0xRECIPIENT_ADDRESS';
const AMOUNT = '0.10';  // USDT amount
// =========================================

const API = 'https://clawpay.dev';
const BSC_RPC = 'https://bsc-dataseed.binance.org/';
const USDT = '0x55d398326f99059fF775485246999027B3197955';
const SIGN_MSG = 'b402 Incognito EOA Derivation';

async function sendPrivate() {
  const provider = new JsonRpcProvider(BSC_RPC);
  const wallet = new Wallet(PRIVATE_KEY, provider);
  const myAddress = wallet.address;

  console.log('Sending', AMOUNT, 'USDT privately to', RECIPIENT);
  console.log('From wallet:', myAddress, '\n');

  // 1. Sign message
  console.log('1. Signing...');
  const signature = await wallet.signMessage(SIGN_MSG);

  // 2. Get invoice address
  console.log('2. Getting invoice...');
  const invoiceRes = await fetch(
    API + '/invoice?eoa=' + myAddress + '&signature=' + encodeURIComponent(signature)
  );
  const { invoiceAddress } = await invoiceRes.json();
  console.log('   Invoice:', invoiceAddress);

  // 3. Transfer USDT to invoice
  console.log('3. Transferring USDT to invoice...');
  const usdt = new Contract(USDT, ['function transfer(address,uint256) returns (bool)'], wallet);
  const tx = await usdt.transfer(invoiceAddress, parseUnits(AMOUNT, 18));
  console.log('   TX:', tx.hash);
  await tx.wait();

  // 4. Execute private transfer
  console.log('4. Executing private transfer...');
  const transferRes = await fetch(API + '/transfer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      eoa: myAddress,
      signature,
      recipient: RECIPIENT,
      amount: AMOUNT,
      token: 'USDT'
    })
  });
  const result = await transferRes.json();

  if (result.transferId) {
    console.log('\n✓ SUCCESS!');
    console.log('Transfer ID:', result.transferId);
    console.log('Status:', result.status);
    console.log('\nRecipient gets funds from Railgun in ~60 seconds.');
    console.log('They CANNOT see your wallet address.');
    console.log('\nCheck status: curl ' + API + '/status/' + result.transferId);
  } else {
    console.log('Error:', result.error);
  }
}

sendPrivate().catch(console.error);
```

**运行方式：**
```bash
npm install ethers
WALLET_KEY=0xYourPrivateKey node send-private.mjs
```

---

## 工作原理

```
YOU                    CLAWPAY API                 RECIPIENT
 │                          │                          │
 ├── USDT to invoice ──────►│                          │
 │                          │                          │
 ├── Sign message ─────────►│                          │
 │                          │                          │
 ├── POST /transfer ───────►│                          │
 │                          ├── Shield (Railgun) ─────►│
 │                          ├── ZK Proof (~60s) ──────►│
 │                          ├── Unshield ─────────────►│
 │                          │                          │
 │                          │    Funds from "Railgun"  │
 │                          │    NO LINK TO YOU        │
```

---

## API 参考

**基础 URL：** `https://clawpay.dev`

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/health` | GET | API 状态 |
| `/invoice?eoa=...&signature=...` | GET | 获取您的发票地址 |
| `/transfer` | POST | 进行私密转账 |
| `/status/:id` | GET | 查看转账状态 |
| `/balance?eoa=...&signature=...&token=USDT` | GET | 查看受保护的余额 |
| `/faucet` | POST | 获取用于支付 gas 的 BNB（测试网） |

### POST /transfer

```json
{
  "eoa": "0xYourAddress",
  "signature": "0xSignedMessage...",
  "recipient": "0xRecipientAddress",
  "amount": "1.00",
  "token": "USDT"
}
```

响应：
```json
{
  "transferId": "tx_123...",
  "status": "pending",
  "message": "Transfer initiated"
}
```

转账状态：`pending` → `shielding` → `proving` → `complete`

---

## 没有私钥？使用 Bankr 钱包

如果您没有直接访问钱包的权限，可以使用 Bankr：

```javascript
// 1. Get your wallet from Bankr
const bankrWallet = await bankr.getWallet();

// 2. Sign the ClawPay message
const signature = await bankr.signMessage('b402 Incognito EOA Derivation');

// 3. Use signature with ClawPay API
// (same flow as above)
```

---

## 支持的代币（BSC）

| 代币 | 地址 |
|-------|---------|
| USDT | `0x55d398326f99059fF775485246999027B3197955` |
| USDC | `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d` |

---

## 需要 gas 吗？

```bash
curl -X POST https://clawpay.dev/faucet \
  -H "Content-Type: application/json" \
  -d '{"address": "0xYourAddress"}'
```

---

## 常见问题及解决方法

| 错误 | 解决方案 |
|-------|-----|
| “余额不足” | 先向发票地址转账 USDT |
| “签名不匹配” | 确保签名内容为：`b402 Incognito EOA Derivation` |
| “没有可花费的 UTXO” | 资金转入发票地址后等待 2 分钟 |

---

**为代理经济提供隐私保护** | 基于 Railgun 构建 | https://clawpay.dev