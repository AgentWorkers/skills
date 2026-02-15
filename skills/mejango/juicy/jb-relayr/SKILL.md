---
name: jb-relayr
description: **Relayr API参考：多链交易捆绑功能**  
该API支持在一条链上支付交易手续费（即“gas fee”），然后在多条链上同时执行这些交易。它适用于跨链部署、跨链操作以及元交易（meta-transactions）场景。
---

# Relayr：多链交易打包服务

Relayr 是由 0xBASED 提供的一种元交易中继服务，它能够将多个链上的交易打包在一起。用户可以为多个链签署交易，在一个链上支付手续费，然后 Relayr 会负责在其他链上执行这些交易。

## 概述

```
1. User signs ERC2771 forward requests for each target chain
2. POST to Relayr API to get quote with payment options
3. User selects which chain to pay on
4. User sends single payment transaction
5. Relayr relayers execute on all other chains
6. Poll for bundle completion status
```

## API 基本 URL

```
Production API: https://api.relayr.ba5ed.com
Dashboard: https://relayr.ba5ed.com
```

## 认证

**无需 API 密钥。** Relayr 支持无需权限的访问，任何人都可以提交交易打包请求。

---

## API 端点

### 1. 创建交易打包请求（Create Bundle Quote）

```
POST /v1/bundle/prepaid
```

该接口用于创建交易打包请求，并返回支付选项。

**请求体：**
```json
{
  "transactions": [
    {
      "chain": 1,
      "target": "0x...",
      "data": "0x...",
      "value": "0"
    }
  ],
  "virtual_nonce_mode": "Disabled"
}
```

**字段：**
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `chain` | 数字 | 目标链的 ID |
| `target` | 字符串 | 需要调用的合约（通常是 ERC2771Forwarder） |
| `data` | 字符串 | 编码后的调用数据（calldata） |
| `value` | 字符串 | 以太坊金额（单位：wei，元交易通常为 "0"） |
| `virtual_nonce_mode` | 字符串 | "Disabled" 或 "Enabled"（用于指定交易的执行顺序） |

**响应：**
```json
{
  "bundle_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "payment_info": [
    {
      "chain": 1,
      "target": "0x...",
      "amount": "1234567890",
      "calldata": "0x..."
    },
    {
      "chain": 10,
      "target": "0x...",
      "amount": "987654321",
      "calldata": "0x..."
    }
  ],
  "per_txn": [
    {
      "txn_uuid": "...",
      "chain": 1,
      "gas_cost": "500000",
      "status": "Quoted"
    }
  ],
  "txn_uuids": ["uuid1", "uuid2"]
}
```

**响应字段：**
| 字段 | 描述 |
|-------|-------------|
| `bundle_uuid` | 用于追踪的唯一标识符 |
| `payment_info` | 支付选项数组（每个支持的链对应一个选项） |
| `payment_info[].chain` | 需要支付的链的 ID |
| `payment_info[].target` | 支付目标地址 |
| `payment_info[].amount` | 需要支付的金额（单位：wei） |
| `payment_info[].calldata` | 用于支付的交易数据 |
| `per_txn` | 单个交易的详细信息 |
| `txn_uuids` | 交易 UUID 的数组 |

---

### 2. 获取交易打包请求的状态（Get Bundle Status）

```
GET /v1/bundle/{bundle_uuid}
```

通过调用此接口可以查询交易打包请求的执行状态。

**响应：**
```json
{
  "bundle_uuid": "550e8400-e29b-41d4-a716-446655440000",
  "payment_received": true,
  "payment_chain": 1,
  "transactions": [
    {
      "txn_uuid": "...",
      "chain": 1,
      "status": "Success",
      "tx_hash": "0x...",
      "block_number": 12345678
    },
    {
      "txn_uuid": "...",
      "chain": 10,
      "status": "Pending",
      "tx_hash": null,
      "block_number": null
    }
  ]
}
```

---

### 3. 获取单个交易的状态（Get Transaction Status）

```
GET /v1/transaction/{txn_uuid}
```

用于获取打包请求中某个交易的具体状态。

---

## 交易状态码及其含义

| 状态码 | 含义 |
|--------|---------|
| `Quoted` | 交易打包请求已创建，等待支付 |
| `PaymentReceived` | 支付已确认，正在排队执行 |
| `Pending` | 交易已提交，等待确认 |
| `Success` | 交易已在链上确认 |
| `Completed` | 与 "Success" 同义 |
| `Failed` | 交易被回滚 |
| `Expired` | 支付未在 48 小时内完成 |

---

## ERC2771 Forward 请求格式

Relayr 使用 ERC2771 元交易机制。Forwarder 合约会验证签名，并在执行交易时保留原始发送者的信息（通过 `_msgSender()` 方法获取）。

### TypedData 的相关内容

```javascript
const domain = {
  name: 'Juicebox',           // Or actual contract name
  version: '1',
  chainId: 1,                 // Target chain ID
  verifyingContract: '0x...'  // ERC2771Forwarder address
};
```

### TypedData 的类型

```javascript
const types = {
  ForwardRequest: [
    { name: 'from', type: 'address' },
    { name: 'to', type: 'address' },
    { name: 'value', type: 'uint256' },
    { name: 'gas', type: 'uint256' },
    { name: 'nonce', type: 'uint256' },
    { name: 'deadline', type: 'uint48' },
    { name: 'data', type: 'bytes' }
  ]
};
```

### 消息字段

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `from` | 地址 | 原始签名者的地址 |
| `to` | 地址 | 需要调用的目标合约 |
| `value` | uint256 | 需要转发的以太币数量 |
| `gas` | uint256 | 交易执行的 gas 限制 |
| `nonce` | uint256 | 用户提供的 nonce 值（从合约中获取） |
| `deadline` | uint48 | 交易执行的截止时间（从现在起最多 48 小时） |
| `data` | bytes | 编码后的函数调用数据 |

### 获取用户的 nonce 值

可以通过调用 Forwarder 合约来获取用户的当前 nonce 值：

```javascript
const forwarder = new ethers.Contract(forwarderAddress, [
  'function nonces(address) view returns (uint256)'
], provider);

const nonce = await forwarder.nonces(userAddress);
```

---

## 完整的 JavaScript 示例

```javascript
import { ethers } from 'ethers';

const RELAYR_API = 'https://api.relayr.ba5ed.com';

// ERC2771Forwarder addresses (same on all chains - deterministic deployment)
const FORWARDER = {
  1: '0x...', // Ethereum mainnet
  10: '0x...', // Optimism
  8453: '0x...', // Base
  42161: '0x...' // Arbitrum
};

/**
 * Deploy or execute across multiple chains with single payment
 */
async function executeOmnichain(signer, targetChains, targetContract, calldata) {
  const address = await signer.getAddress();
  const signedRequests = [];

  // Step 1: Sign forward request for each chain
  for (const chainId of targetChains) {
    // Get nonce from forwarder contract
    const nonce = await getNonce(chainId, address);

    const domain = {
      name: 'Juicebox',
      version: '1',
      chainId: chainId,
      verifyingContract: FORWARDER[chainId]
    };

    const types = {
      ForwardRequest: [
        { name: 'from', type: 'address' },
        { name: 'to', type: 'address' },
        { name: 'value', type: 'uint256' },
        { name: 'gas', type: 'uint256' },
        { name: 'nonce', type: 'uint256' },
        { name: 'deadline', type: 'uint48' },
        { name: 'data', type: 'bytes' }
      ]
    };

    // 48-hour deadline (maximum allowed)
    const deadline = Math.floor(Date.now() / 1000) + 48 * 60 * 60;

    const message = {
      from: address,
      to: targetContract,
      value: '0',
      gas: '1000000',
      nonce: nonce,
      deadline: deadline,
      data: calldata
    };

    // Sign the typed data
    const signature = await signer.signTypedData(domain, types, message);

    // Encode for forwarder.execute()
    const forwarderAbi = [
      'function execute((address from, address to, uint256 value, uint256 gas, uint256 nonce, uint48 deadline, bytes data) request, bytes signature)'
    ];
    const iface = new ethers.Interface(forwarderAbi);
    const encodedData = iface.encodeFunctionData('execute', [
      [message.from, message.to, message.value, message.gas, message.nonce, message.deadline, message.data],
      signature
    ]);

    signedRequests.push({
      chain: chainId,
      target: FORWARDER[chainId],
      data: encodedData,
      value: '0'
    });
  }

  // Step 2: Get quote from Relayr
  const quoteResponse = await fetch(`${RELAYR_API}/v1/bundle/prepaid`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      transactions: signedRequests,
      virtual_nonce_mode: 'Disabled'
    })
  });

  if (!quoteResponse.ok) {
    throw new Error(`Quote failed: ${quoteResponse.statusText}`);
  }

  const quote = await quoteResponse.json();
  console.log('Bundle UUID:', quote.bundle_uuid);
  console.log('Payment options:', quote.payment_info.map(p =>
    `Chain ${p.chain}: ${ethers.formatEther(p.amount)} ETH`
  ));

  return quote;
}

/**
 * Execute payment on chosen chain
 */
async function payForBundle(signer, paymentInfo) {
  const tx = await signer.sendTransaction({
    to: paymentInfo.target,
    value: paymentInfo.amount,
    data: paymentInfo.calldata
  });

  console.log('Payment tx:', tx.hash);
  await tx.wait();
  console.log('Payment confirmed');

  return tx;
}

/**
 * Poll until all transactions complete
 */
async function waitForCompletion(bundleUuid, onUpdate) {
  while (true) {
    const response = await fetch(`${RELAYR_API}/v1/bundle/${bundleUuid}`);
    const status = await response.json();

    if (onUpdate) onUpdate(status);

    const allDone = status.transactions.every(
      tx => ['Success', 'Completed', 'Failed'].includes(tx.status)
    );

    if (allDone) {
      const anyFailed = status.transactions.some(tx => tx.status === 'Failed');
      if (anyFailed) {
        const failed = status.transactions.filter(tx => tx.status === 'Failed');
        throw new Error(`Transactions failed on chains: ${failed.map(t => t.chain).join(', ')}`);
      }
      return status;
    }

    console.log('Status:', status.transactions.map(t => `Chain ${t.chain}: ${t.status}`).join(', '));
    await new Promise(r => setTimeout(r, 3000));
  }
}

/**
 * Helper: Get nonce from forwarder on specific chain
 */
async function getNonce(chainId, address) {
  const rpcUrls = {
    1: 'https://eth.llamarpc.com',
    10: 'https://mainnet.optimism.io',
    8453: 'https://mainnet.base.org',
    42161: 'https://arb1.arbitrum.io/rpc'
  };

  const provider = new ethers.JsonRpcProvider(rpcUrls[chainId]);
  const forwarder = new ethers.Contract(
    FORWARDER[chainId],
    ['function nonces(address) view returns (uint256)'],
    provider
  );

  return await forwarder.nonces(address);
}

/**
 * Complete flow example
 */
async function main() {
  const provider = new ethers.BrowserProvider(window.ethereum);
  const signer = await provider.getSigner();

  // Example: Deploy to Ethereum, Optimism, and Base
  const targetChains = [1, 10, 8453];
  const targetContract = '0x...'; // JBController
  const calldata = '0x...'; // launchProjectFor encoded

  // Get quote
  const quote = await executeOmnichain(signer, targetChains, targetContract, calldata);

  // Find cheapest payment option
  const cheapest = quote.payment_info.reduce((min, p) =>
    BigInt(p.amount) < BigInt(min.amount) ? p : min
  );

  console.log(`Paying ${ethers.formatEther(cheapest.amount)} ETH on chain ${cheapest.chain}`);

  // Switch chain if needed and pay
  // ... chain switching logic ...
  await payForBundle(signer, cheapest);

  // Wait for all chains to complete
  const result = await waitForCompletion(quote.bundle_uuid, (status) => {
    console.log('Update:', status.transactions.map(t => t.status));
  });

  console.log('All transactions complete!');
  console.log('Tx hashes:', result.transactions.map(t => `${t.chain}: ${t.tx_hash}`));
}
```

---

## RelayrClient 类

```javascript
class RelayrClient {
  constructor(apiUrl = 'https://api.relayr.ba5ed.com') {
    this.api = apiUrl;
  }

  async createBundle(transactions) {
    const response = await fetch(`${this.api}/v1/bundle/prepaid`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transactions,
        virtual_nonce_mode: 'Disabled'
      })
    });

    if (!response.ok) {
      throw new Error(`Relayr quote failed: ${response.statusText}`);
    }

    return await response.json();
  }

  async getBundleStatus(bundleUuid) {
    const response = await fetch(`${this.api}/v1/bundle/${bundleUuid}`);
    return await response.json();
  }

  async getTransactionStatus(txnUuid) {
    const response = await fetch(`${this.api}/v1/transaction/${txnUuid}`);
    return await response.json();
  }

  async waitForCompletion(bundleUuid, options = {}) {
    const { pollInterval = 3000, timeout = 600000, onUpdate } = options;
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      const status = await this.getBundleStatus(bundleUuid);

      if (onUpdate) onUpdate(status);

      const allDone = status.transactions.every(
        tx => ['Success', 'Completed', 'Failed'].includes(tx.status)
      );

      if (allDone) {
        return status;
      }

      await new Promise(r => setTimeout(r, pollInterval));
    }

    throw new Error('Bundle completion timeout');
  }
}
```

---

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `Quote failed` | 交易数据无效 | 检查编码是否正确 |
| `Nonce too low` | nonce 值已被使用 | 从 Forwarder 合约中重新获取 nonce 值 |
| `Deadline expired` | 签名失效 | 重新签名并设置新的截止时间 |
| `Insufficient payment` | 支付金额不足 | 重新请求报价 |
| `Transaction reverted` | 交易执行失败 | 在目标链上调试问题 |

---

## 最佳实践

1. **始终获取最新报价**：Gas 价格会波动，因此在支付前请立即获取最新的报价。
2. **设置合理的 gas 限制**：过低的 gas 限制可能导致交易回滚，过高的限制则会增加成本。
3. **使用 48 小时的截止时间**：这是允许的最大时间范围，确保有足够的时间完成交易执行。
4. **处理链切换**：用户可能需要更换钱包以便在不同的链上支付。
5. **采用延迟请求机制**：初始请求间隔为 2-3 秒，30 秒后间隔增加到 10 秒。
6. **验证 nonce 值**：始终从 Forwarder 合约中获取最新的 nonce 值。
7. **处理部分失败的情况**：某些链可能成功执行，而其他链可能失败。

---

## 使用场景

- **多链项目部署**：一次性将 Juicebox 项目部署到多个链上。
- **跨链配置**：同时更新所有链上的设置。
- **多链代币操作**：协调不同链上的代币操作。
- **批量交易**：使用一次支付来执行多个交易。

---

## 相关技能

- `/jb-bendystraw`：用于部署后查询跨链数据。
- `/jb-omnichain-ui`：使用 Relayr 构建用户界面。
- `/jb-project`：项目部署的相关配置。