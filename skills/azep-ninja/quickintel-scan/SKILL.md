---
name: quickintel-scan
description: "使用 Quick Intel 的合约分析 API 来扫描任何代币，以检测其中可能存在的安全风险、蜜罐（honeypots）和诈骗行为。适用场景包括：判断代币是否安全购买、检测蜜罐、分析合约的所有权和权限、查找隐藏的代币生成（minting）或黑名单相关功能，以及在交易前评估代币的风险。触发命令包括：“is this token safe”、“scan token”、“check for honeypot”、“audit contract”、“rug pull check”、“token security”、“safe to buy”、“scam check”。该工具支持 63 种区块链网络，包括 Base、Ethereum、Solana、Sui 和 Tron。每次扫描的费用为 0.03 美元（USDC），通过 x402 支付协议进行结算。适用于所有兼容 x402 协议的钱包。"
---
# 快速英特尔代币安全扫描器（Quick Intel Token Security Scanner）

## 常见错误

**请注意：** 这不是一个免费API。Quick Intel使用x402支付协议——每次扫描费用为0.03美元（USDC），无需API密钥或订阅服务。您的钱包会完成支付授权，之后扫描才会执行。

**x402支付流程很简单：** 您调用相应的API端点，收到包含支付要求的402响应；接着签署EIP-3009授权文件；再次尝试请求时需包含支付头部信息；最后获取扫描结果。大多数钱包库都能自动处理这些步骤。

**支持63个区块链：** 不仅支持EVM，还支持Solana、Sui、Radix、Tron和Injective等区块链。如果您要检查某个代币，Quick Intel很可能支持该区块链。

## 概述

| 详细信息 | 说明 |
|--------|-------|
| **API端点** | `POST https://x402.quickintel.io/v1/scan/full` |
| **费用** | 0.03美元（30000原子单位） |
| **支持的支付网络** | Base、Ethereum、Arbitrum、Optimism、Polygon、Avalanche、Unichain、Linea、MegaETH |
| **支付货币** | USDC（每个区块链上使用的原生Circle USDC） |
| **协议版本** | x402 v2（需要支付请求） |
| **幂等性** | 通过`payment-identifier`扩展支持 |

## 支持的区块链（共63个）

| 区块链 | 区块链 | 区块链 | 区块链 |
|-------|-------|-------|-------|
| eth | arbitrum | bsc | opbnb |
| base | core | linea | pulse |
| zksync | shibarium | maxx | polygon |
| scroll | polygonzkevm | fantom | avalanche |
| bitrock | loop | besc | kava |
| metis | astar | oasis | iotex |
| conflux | canto | energi | velas |
| grove | mantle | lightlink | optimism |
| klaytn | solana | radix | sui |
| injective | manta | zeta | blast |
| zora | inevm | degen | mode |
| viction | nahmii | real | xlayer |
| tron | worldchain | apechain | morph |
| ink | sonic | soneium | abstract |
| berachain | unichain | hyperevm | plasma |
| monad | megaeth | | |

**注意：** 请使用准确的区块链名称（例如使用“eth”而非“Ethereum”，“bsc”而非“binance”）。

## 使用前的检查

在调用API之前，请确认以下内容：

### 1. 在支持的支付链上有足够的USDC余额

您至少需要在某个支持的支付链上拥有0.03美元的USDC余额。建议使用Base区块链（费用最低）。

**检查余额（使用viem）：**
```javascript
const balance = await publicClient.readContract({
  address: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC on Base
  abi: erc20Abi,
  functionName: "balanceOf",
  args: [walletAddress],
});
const hasEnough = balance >= 30000n; // $0.03 with 6 decimals
```

**检查余额（使用ethers.js）：**
```javascript
const USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const balance = await usdcContract.balanceOf(walletAddress);
const hasEnough = balance >= 30000n; // $0.03 with 6 decimals
```

### 2. 有效的代币地址

- EVM：以`0x`开头的42位十六进制地址
- Solana：Base58编码的地址（32-44位）

## x402支付流程

x402是一个基于HTTP的支付协议。以下是完整的支付流程：

```
┌─────────────────────────────────────────────────────────────┐
│  1. REQUEST    POST to endpoint with scan parameters        │
│                                                             │
│  2. 402        Server returns "Payment Required"            │
│                PAYMENT-REQUIRED header contains payment info │
│                                                             │
│  3. SIGN       Your wallet signs EIP-3009 authorization     │
│                (transferWithAuthorization for USDC)          │
│                                                             │
│  4. RETRY      Resend request with PAYMENT-SIGNATURE header  │
│                Contains base64-encoded signed payment proof  │
│                                                             │
│  5. SETTLE     Server verifies signature, settles on-chain  │
│                                                             │
│  6. RESPONSE   Server returns scan results (200 OK)         │
│                PAYMENT-RESPONSE header contains tx receipt   │
└─────────────────────────────────────────────────────────────┘
```

## x402 v2请求头信息

| 请求头 | 作用 | 说明 |
|--------|-----------|-------------|
| `PAYMENT-REQUIRED` | 响应头（402状态码） | 包含支付要求和支持的支付网络的信息（Base64编码的JSON） |
| `PAYMENT-SIGNATURE` | 请求头（重试时使用） | 包含已签署的EIP-3009授权信息的Base64编码JSON |
| `PAYMENT-RESPONSE` | 响应头（200状态码） | 包含结算交易哈希和区块编号的Base64编码JSON |

**注意：** 为了兼容旧版本，也支持`X-PAYMENT`请求头，但推荐使用`PAYMENT-SIGNATURE`。

## 支付标识符（确保请求的幂等性）

该服务支持`payment-identifier`扩展。如果您的代理程序可能因网络故障或超时而重复请求，请在请求数据中包含唯一的支付ID，以避免重复支付：

```javascript
const paymentPayload = {
  // ... standard payment fields ...
  extensions: {
    'payment-identifier': {
      paymentId: 'pay_' + crypto.randomUUID().replace(/-/g, '')
    }
  }
};
```

如果系统已经处理过带有相同支付ID的请求，它会返回缓存的结果而不会再次收费。支付ID应为16-128个字符，包含字母、数字以及连字符和下划线。

## 查询支持的信息

在调用API之前，请先查询系统支持的支付网络和数据格式：

```
GET https://x402.quickintel.io/accepted
```

该接口会返回所有可用路径、支持的支付网络、价格信息以及输入/输出格式，以便集成到您的代理程序中。

## 钱包集成方式

### 方式1：本地钱包（使用私钥）

推荐使用`@x402/fetch`函数：

```javascript
import { x402Fetch } from '@x402/fetch';
import { createWallet } from '@x402/evm';

const wallet = createWallet(process.env.PRIVATE_KEY);

const response = await x402Fetch('https://x402.quickintel.io/v1/scan/full', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    chain: 'base',
    tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
  }),
  wallet,
  preferredNetwork: 'eip155:8453'
});

const scanResult = await response.json();
```

### 方式2：AgentWallet（frames.ag）

AgentWallet可以一次性完成整个x402请求流程：

```javascript
const response = await fetch('https://frames.ag/api/wallets/{username}/actions/x402/fetch', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${AGENTWALLET_API_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    url: 'https://x402.quickintel.io/v1/scan/full',
    method: 'POST',
    body: {
      chain: 'base',
      tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
    }
  })
});

const scanResult = await response.json();
```

### 方式3：Vincent Wallet（heyvincent.ai）

```javascript
// Vincent handles x402 via its transaction signing API
const paymentAuth = await vincent.signPayment({
  network: 'eip155:8453',
  amount: '30000',
  token: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  recipient: recipientFromHeader
});

// Then retry with the signed payment
const response = await fetch('https://x402.quickintel.io/v1/scan/full', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'PAYMENT-SIGNATURE': paymentAuth.encoded
  },
  body: JSON.stringify({ chain: 'base', tokenAddress: '0x...' })
});
```

### 方式4：任何支持EIP-3009协议的钱包

如果您的钱包支持签署EIP-712格式的数据，也可以使用相应的接口：

```javascript
// 1. Call endpoint, get 402 response
// 2. Parse PAYMENT-REQUIRED header
// 3. Sign EIP-3009 transferWithAuthorization
const signature = await wallet.signTypedData({
  domain: {
    name: 'USD Coin',
    version: '2',
    chainId: 8453,
    verifyingContract: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
  },
  types: {
    TransferWithAuthorization: [
      { name: 'from', type: 'address' },
      { name: 'to', type: 'address' },
      { name: 'value', type: 'uint256' },
      { name: 'validAfter', type: 'uint256' },
      { name: 'validBefore', type: 'uint256' },
      { name: 'nonce', type: 'bytes32' }
    ]
  },
  primaryType: 'TransferWithAuthorization',
  message: { from, to, value: 30000n, validAfter: 0, validBefore, nonce }
});
// 4. Retry with PAYMENT-SIGNATURE header (base64-encoded payload)
```

## API请求格式

```http
POST https://x402.quickintel.io/v1/scan/full
Content-Type: application/json

{
  "chain": "base",
  "tokenAddress": "0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00"
}
```

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `chain` | string | 是 | 区块链名称（小写，参见支持的区块链列表） |
| `tokenAddress` | string | 是 | 代币合约地址 |

## API响应

扫描结果会提供详细的代币安全分析：

```json
{
  "tokenDetails": {
    "tokenName": "Ribbita by Virtuals",
    "tokenSymbol": "TIBBIR",
    "tokenDecimals": 18,
    "tokenSupply": 1000000000,
    "tokenCreatedDate": 1736641803000
  },
  "tokenDynamicDetails": {
    "is_Honeypot": false,
    "buy_Tax": "0.0",
    "sell_Tax": "0.0",
    "transfer_Tax": "0.0",
    "has_Trading_Cooldown": false,
    "liquidity": false
  },
  "isScam": null,
  "isAirdropPhishingScam": false,
  "contractVerified": true,
  "quickiAudit": {
    "contract_Renounced": true,
    "hidden_Owner": false,
    "is_Proxy": false,
    "can_Mint": false,
    "can_Blacklist": false,
    "can_Update_Fees": false,
    "can_Pause_Trading": false,
    "has_Suspicious_Functions": false,
    "has_Scams": false
  }
}
```

### 需重点关注的字段

#### 即刻避免购买的代币

| 字段 | 不良状态 | 含义 |
|-------|-----------|---------|
| `is_Honeypot` | `true` | 该代币可能是“蜜罐”，资金可能无法取出 |
| `isScam` | `true` | 该代币属于已知诈骗合约 |
| `isAirdropPhishingScam` | `true` | 该代币涉及钓鱼攻击 |
| `has_Scams` | `true` | 该代币包含诈骗特征 |
| `can_Potentially_Steal_Funds` | `true` | 该代币存在资金被盗的风险 |

#### 高风险警告

| 字段 | 高风险状态 | 含义 |
|-------|-------------|---------|
| `buy_Tax` / `sell_Tax` | `> 10` | 高额税费会降低收益 |
| `can_Mint` | `true` | 合约所有者可以增加代币供应量 |
| `can_Blacklist` | `true` | 合约所有者可以屏蔽您的钱包 |
| `can_Pause_Trading` | `true` | 合约所有者可以暂停交易 |
| `hidden_Owner` | `true` | 所有者信息被隐藏 |
| `contract_Renounced` | `false` | 合约所有者仍保留控制权 |

#### 正面信号

| 字段 | 正面状态 | 含义 |
|-------|------------|---------|
| `contract_Renounced` | `true` | 合约所有者已放弃控制权 |
| `contractVerified` | `true` | 合约源代码已公开 |
| `is_Launchpad_Contract` | `true` | 来自知名发行平台 |
| `can_Mint` | `false` | 代币供应量固定 |
| `can_Blacklist` | `false` | 合约所有者无屏蔽他人钱包的能力 |

### 解释结果

**安全交易的条件：** 所有相关字段都必须为以下状态：
- `is_Honeypot` = `false`
- `isScam` = `null` 或 `false`
- `has_Scams` = `false`
- `buy_Tax` 和 `sell_Tax` 的值 < 10%
- 无 `has_Suspicious Functions`（表示代币没有可疑功能）

**交易时需谨慎：**
- `contract_Renounced` = `false`（表示所有者已放弃控制权）
- `can_Update_Fees` = `true`（表示费用可能随时调整）
- `is_Proxy` = `true`（表示代码可能随时更新）

**禁止交易的代币：**
- `is_Honeypot` = `true`
- `isScam` = `true`
- `can_Potentially_Steal_Funds` = `true`
- `buy_Tax` 或 `sell_Tax` > 50%

## 完整示例

```javascript
import { x402Fetch } from '@x402/fetch';
import { createWallet } from '@x402/evm';

async function scanToken(chain, tokenAddress) {
  const wallet = createWallet(process.env.PRIVATE_KEY);

  // Pre-flight: Check USDC balance
  const balance = await checkUSDCBalance(wallet.address);
  if (balance < 30000n) {
    throw new Error('Insufficient USDC on Base. Need at least $0.03');
  }

  // Scan token (x402 payment handled automatically by x402Fetch)
  const response = await x402Fetch('https://x402.quickintel.io/v1/scan/full', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chain, tokenAddress }),
    wallet,
    preferredNetwork: 'eip155:8453'
  });

  if (!response.ok) {
    throw new Error(`Scan failed: ${response.status}`);
  }

  const result = await response.json();

  // Analyze results
  const analysis = {
    token: result.tokenDetails.tokenName,
    symbol: result.tokenDetails.tokenSymbol,
    safe: !result.tokenDynamicDetails.is_Honeypot &&
          !result.isScam &&
          !result.quickiAudit.has_Scams,
    risks: []
  };

  if (result.tokenDynamicDetails.is_Honeypot) {
    analysis.risks.push('HONEYPOT - Cannot sell');
  }
  if (result.quickiAudit.can_Mint) {
    analysis.risks.push('Owner can mint new tokens');
  }
  if (result.quickiAudit.can_Blacklist) {
    analysis.risks.push('Owner can blacklist wallets');
  }
  if (!result.quickiAudit.contract_Renounced) {
    analysis.risks.push('Contract not renounced');
  }
  if (parseFloat(result.tokenDynamicDetails.buy_Tax) > 5) {
    analysis.risks.push(`High buy tax: ${result.tokenDynamicDetails.buy_Tax}%`);
  }
  if (parseFloat(result.tokenDynamicDetails.sell_Tax) > 5) {
    analysis.risks.push(`High sell tax: ${result.tokenDynamicDetails.sell_Tax}%`);
  }

  return analysis;
}

// Usage
const result = await scanToken('base', '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00');
console.log(result);
// {
//   token: "Ribbita by Virtuals",
//   symbol: "TIBBIR",
//   safe: true,
//   risks: ["Contract not renounced"]
// }
```

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|-------|-------|----------|
| `402 Payment Required` | 未提供支付头部信息 | 请签署请求并添加`PAYMENT-SIGNATURE`头部 |
| `402 Payment verification failed` | 签名无效或USDC余额不足 | 请检查余额和签名 |
| `402 Nonce already used` | 请求被重复发送或未包含支付标识符 | 请使用`payment-identifier`进行安全重试 |
| `400 Invalid Chain` | 未知的区块链名称 | 请查看支持的区块链列表 |
| `400 Invalid Address` | 地址格式错误 | 请检查地址格式 |
| `404 Token Not Found` | 代币不存在 | 请检查地址和区块链名称 |
| `500 Scan Failed` | 合约分析失败 | 请重试或联系客服 |

## 重要提示

- **无论扫描结果如何，费用都会被收取。** 即使扫描返回的信息有限（例如合约未经过验证或代币是新发行的），您仍需支付0.03美元。使用`payment-identifier`可以避免重复支付。
- **扫描结果为实时数据。** 今天安全的代币明天可能不再安全（例如合约所有者可能放弃控制权）。
- **本文档仅提供数据，不提供交易建议。**
- **Solana代币的分析方式与EVM不同，某些字段可能为空。**
- **多区块链支付：** 您可以在任何支持的支付链（Base、Ethereum、Arbitrum等）上进行支付。402响应会列出所有支持的支付网络。

## 相关资源

- **Quick Intel文档：** https://docs.quickintel.io
- **x402协议文档：** https://www.x402.org
- **支付网关信息：** https://x402.quickintel.io/accepted
- **技术支持：** https://t.me/quicki