---
name: quickintel-scan
description: "使用 Quick Intel 的合约分析 API 来扫描任何代币，以检测其中可能存在的安全风险、蜜罐（honeypots）或诈骗行为。适用场景包括：判断代币是否适合购买、识别蜜罐、分析合约的所有权和权限、查找隐藏的代币生成（minting）或黑名单相关功能，以及在交易前评估代币的风险。触发命令包括：`is this token safe`、`scan token`、`check for honeypot`、`audit contract`、`rug pull check`、`token security`、`safe to buy`、`scam check`。该工具支持 63 种区块链网络，包括 Base、Ethereum、Solana、Sui 和 Tron。每次扫描的费用为 0.03 美元 USD，通过 x402 支付协议进行结算。该服务兼容所有支持 x402 协议的钱包。"
---
# 快速英特尔代币安全扫描器（Quick Intel Token Security Scanner）

## 常见错误

**请注意：**  
**这并非免费API。** 快速英特尔（Quick Intel）使用x402支付协议：每次扫描费用为0.03美元（USDC），无需API密钥或订阅服务。您的钱包会完成支付授权，之后扫描才会执行。  

**x402支付流程简单易懂：**  
您只需调用相应端点，系统会返回包含支付要求的402响应；您需完成支付签名后重新尝试请求，最终获取扫描结果。大多数钱包库均可自动处理这一流程。  

**支持63个区块链：**  
不仅支持EVM（以太坊），还支持Solana、Sui、Radix、Tron和Injective等区块链。如果您要扫描某个代币，快速英特尔通常也支持该区块链。  

## 概述  

| 详情 | 说明 |
|--------|-------|
| **端点** | `POST https://x402.quickintel.io/v1/scan/full` |
| **费用** | 0.03美元（USDC，相当于30000个原子单位） |
| **支持的网络** | Base、Ethereum、Arbitrum、Optimism、Polygon、Avalanche、Unichain、Linea、MegaETH、Solana |
| **支付货币** | USDC（每个区块链上使用Circle发行的原生USDC） |
| **协议** | x402 v2（需要HTTP 402响应） |
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

**注意：** 请使用官方列出的区块链名称（例如，使用“eth”而非“Ethereum”，“bsc”而非“binance”）。  

## 使用前的检查  

在调用API之前，请确认：  

### 1. 在支持的区块链上有足够的USDC余额  

您至少需要在支持的区块链上拥有0.03美元的USDC余额。建议使用Base区块链（费用最低），Solana也同样支持。  
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

- **EVM：** 以`0x`开头的42位十六进制地址  
- **Solana：** Base58编码的地址（32-44位字符）  

## x402支付流程  

x402是一种基于HTTP的支付协议。以下是完整的支付流程：  

### EVM区块链的支付流程（Base、Ethereum、Arbitrum等）  
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
│  4. RETRY      Resend request with PAYMENT-SIGNATURE header │
│                Contains base64-encoded signed payment proof  │
│                                                             │
│  5. SETTLE     Server verifies signature, settles on-chain  │
│                                                             │
│  6. RESPONSE   Server returns scan results (200 OK)         │
│                PAYMENT-RESPONSE header contains tx receipt   │
└─────────────────────────────────────────────────────────────┘
```  

### Solana（SVM）的支付流程  
```
┌─────────────────────────────────────────────────────────────┐
│  1. REQUEST    POST to endpoint with scan parameters        │
│                                                             │
│  2. 402        Server returns "Payment Required"            │
│                Solana entry includes extra.feePayer address  │
│                                                             │
│  3. BUILD      Build SPL TransferChecked transaction:       │
│                - Set feePayer to gateway's facilitator       │
│                - Transfer USDC to gateway's payTo address    │
│                - Partially sign with your wallet             │
│                                                             │
│  4. RETRY      Resend request with PAYMENT-SIGNATURE header │
│                payload: { transaction: "<base64>" }          │
│                                                             │
│  5. SETTLE     Gateway co-signs as feePayer, submits to     │
│                Solana, confirms transaction                  │
│                                                             │
│  6. RESPONSE   Server returns scan results (200 OK)         │
│                PAYMENT-RESPONSE header contains tx signature │
└─────────────────────────────────────────────────────────────┘
```  

### x402 v2请求头信息  

| 请求头 | 类型 | 说明 |
|--------|-----------|-------------|
| `PAYMENT-REQUIRED` | 响应（402状态码） | 包含支付要求和可接受网络的Base64 JSON数据 |
| `PAYMENT-SIGNATURE` | 请求（重试时使用） | 包含签名后的EIP-3009授权信息的Base64 JSON数据（EVM）或部分签名的交易信息（SVM） |
| `PAYMENT-RESPONSE` | 响应（200状态码） | 包含结算交易哈希值/签名及区块号的Base64 JSON数据 |

**注意：** 为兼容旧版本，系统也接受`X-PAYMENT`请求头，但推荐使用`PAYMENT-SIGNATURE`。  

### 支付标识符（幂等性）  

系统支持`payment-identifier`扩展。如果您的代理程序可能因网络故障或超时而重复请求，请在请求数据中添加唯一的支付ID，以避免重复支付：  
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
如果系统已处理过相同支付ID的请求，会直接返回缓存结果而不再收费。支付ID应为16-128个字符，包含字母、数字及连字符/下划线。  

## 预查询功能  

在调用API之前，请先查询系统支持的支付网络和数据格式：  
```
GET https://x402.quickintel.io/accepted
```  
该功能可获取所有可用路径、支持的网络、价格信息以及输入/输出格式，便于集成到您的代理程序中。  

## 钱包集成方式  

### 方式1：本地EVM钱包（使用私钥）  
推荐使用`@x402/fetch`：  
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

### 方式2：Solana钱包（SVM）  
```javascript
import { createSvmClient } from '@x402/svm/client';
import { toClientSvmSigner } from '@x402/svm';
import { wrapFetchWithPayment } from '@x402/fetch';
import { createKeyPairSignerFromBytes } from '@solana/kit';
import { base58 } from '@scure/base';

// Create Solana signer
const keypair = await createKeyPairSignerFromBytes(
  base58.decode(process.env.SOLANA_PRIVATE_KEY)
);
const signer = toClientSvmSigner(keypair);
const client = createSvmClient({ signer });
const paidFetch = wrapFetchWithPayment(fetch, client);

// Call scan API (x402 payment via Solana USDC)
const response = await paidFetch('https://x402.quickintel.io/v1/scan/full', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    chain: 'base',
    tokenAddress: '0xa4a2e2ca3fbfe21aed83471d28b6f65a233c6e00'
  })
});

const scanResult = await response.json();
```  

### 方式3：AgentWallet（frames.ag）  
AgentWallet可一次性完成整个x402请求流程：  
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

### 方式4：Vincent钱包（heyvincent.ai）  
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

### 方式5：任何支持EIP-3009协议的钱包  
如果您的钱包支持签名EIP-712格式的数据，也可使用此方式：  
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
| `chain` | 字符串 | 是 | 区块链名称（小写，参见支持列表） |
| `tokenAddress` | 字符串 | 是 | 代币合约地址 |

## API响应内容  

扫描结果包含详细的代币安全分析：  
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

#### 即刻避免购买的代币：  
- `is_Honeypot`：`true` 表示代币为“陷阱”，无法购买  
- `isScam`：`true` 表示代币为诈骗合约  
- `isAirdropPhishingScam`：`true` 表示存在钓鱼行为  
- `has_Scams`：`true` 表示代币包含诈骗特征  
- `can_Potentially_Steal_Funds`：`true` 表示存在资金被盗风险  

#### 高风险提示：  
- `buy_Tax` / `sell_Tax`：数值大于10% 表示交易税费较高，可能影响利润  
- `can_Mint`：`true` 表示代币所有者可增加供应量  
- `can_Blacklist`：`true` 表示所有者可阻止交易  
- `can_Pause_Trading`：`true` 表示所有者可冻结交易  
- `hidden_Owner`：`true` 表示所有者信息被隐藏  
- `contract_Renounced`：`false` 表示所有者仍保留控制权  

#### 正面信号：  
- `contract_Renounced`：`true` 表示代币所有者已放弃控制权  
- `contractVerified`：`true` 表示代币源代码已公开  
- `is_Launchpad_Contract`：`true` 表示代币来自知名发行平台  
- `can_Mint`：`false` 表示代币供应量固定  
- `can_Blacklist`：`false` 表示所有者无权限阻止交易  

### 结果解读：  

**可安全交易的代币（所有条件均需满足）：**  
- `is_Honeypot` = `false`  
- `isScam` = `null` 或 `false`  
- `has_Scams` = `false`  
- `buy_Tax` 和 `sell_Tax` 均小于10%  

**需谨慎的交易情况：**  
- `contract_Renounced` = `false`（所有者仍可能控制代币）  
- `can_Update_Fees` = `true`（费用可能随时调整）  
- `is_Proxy` = `true`（代码可能随时更改）  

**禁止交易的代币：**  
- `is_Honeypot` = `true`  
- `isScam` = `true`  
- `can_Potentially_Steal_Funds` = `true`  
- `buy_Tax` 或 `sell_Tax` 大于10%  

## 完整示例代码  
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

## 错误处理：  
| 错误代码 | 原因 | 解决方案 |
|-------|-------|----------|
| `402 Payment Required` | 未提供支付信息 | 请添加`PAYMENT-SIGNATURE`请求头 |
| `402 Payment verification failed` | 签名无效或USDC余额不足 | 请检查余额和签名信息 |
| `402 Nonce already used` | 请求被重复或未包含支付标识符 | 请使用`payment-identifier`重试 |
| `400 Invalid Chain` | 未知的区块链名称 | 请查看支持列表 |
| `400 Invalid Address` | 地址格式错误 | 请检查地址格式 |
| `404 Token Not Found` | 代币不存在 | 请检查地址和区块链 |
| `500 Scan Failed` | 代币合约分析失败 | 请重试或联系客服  

## 重要提示：**  
- **无论扫描结果如何，费用均需支付。** 即使扫描返回的信息有限（如未验证的合约或新发行的代币），您仍需支付0.03美元。使用`payment-identifier`可避免重复支付。  
- **扫描结果为实时数据**：今日安全的代币明天可能不再安全（例如，如果代币所有者放弃控制权）。  
- **本文档仅提供数据，不提供交易建议。**  
- **Solana代币的分析方式与EVM不同，部分字段可能为空。**  
- **多链支付**：您可以在任何支持的区块链上支付（EVM区块链：Base、Ethereum、Arbitrum、Optimism、Polygon、Avalanche、Unichain、Linea、MegaETH；Solana）。x402响应会列出所有可接受的网络。  
- **Solana支付**：在Solana上使用SVM支付流程，并提供`extra.feePayer`地址以完成交易。  

## 相关资源：  
- **快速英特尔文档**：https://docs.quickintel.io  
- **x402协议文档**：https://www.x402.org  
- **支付网关信息**：https://x402.quickintel.io/accepted  
- **技术支持**：https://t.me/quicki