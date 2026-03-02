---
name: iauotpay-api
description: >
  **从 iAutoPay Fact API 购买 API 密钥（使用 Base 链上的 USDC）**  
  在以下情况下可以使用此功能：  
  - 为 AI 代理支付服务购买 API 密钥  
  - 管理 API 密钥的订阅（1 天、7 天、30 天有效期）  
  - 查看用户账户信息和使用统计  
  - 查看服务器信息及定价  
  - 集成加密支付以访问 API  
  **注意：**  
  - API 密钥的购买和订阅需要使用 Base 链上的 USDC 进行支付。  
  - 请确保您已拥有足够的 USDC 账户余额以完成购买操作。
---
# iAutoPay 事实 API (Fact API)

## 基础 URL  
- **fact-api**: `https://apipaymcp.okart.fun`（支付 API）  
- **napi-ser**: `http://ipaynapi.gpuart.cn`（用户管理及 API 密钥）  

## 网络配置  
- **链（Chain）**: Base Sepolia（测试网）  
- **链 ID（Chain ID）**: eip155:84532  
- **资产（Asset）**: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`（USDC）  
- **收款人（Payee）**: `0x1a85156c2943b63febeee7883bd84a7d1cf0da0c`  

## 价格（Pricing）  
| 时长（Duration） | 价格（USDC） |  
|------------|-------------|  
| 1 天       | 0.09         |  
| 7 天       | 0.49         |  
| 30 天       | 0.99         |  

## 端点（Endpoints）  

### fact-api（支付服务）（Payment Service）  

#### GET /info - 服务器信息（Server Information）  
获取当前服务器状态、价格和配置信息。  

**响应（Response）**:  
```json
{
  "name": "iAutoPay Fact API",
  "version": "0.1.0",
  "environment": "dev",
  "network": "eip155:84532",
  "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
  "prices": {
    "1day": "90000",
    "1dayUsdc": 0.09,
    "7days": "490000",
    "7daysUsdc": 0.49,
    "30days": "990000",
    "30daysUsdc": 0.99
  },
  "payee": "0x1a85156c2943b63febeee7883bd84a7d1cf0da0c",
  "bypassPayment": false,
  "paymentScheme": "exact"
}
```  

#### POST /v1/buy-apikey - 购买 API 密钥（Buy API Key）  
购买指定期限的 API 密钥。支付通过请求头中的 EIP-3009 签名完成。  

**请求体（Request Body）**:  
```json
{
  "duration": 7
}
```  

**请求头（Headers）**:  
| 头部字段（Header Field） | 类型（Type） | 是否必需（Required） | 描述（Description） |  
|-----------------|-----------|-----------------|-----------------|  
| Content-Type | string | Yes | "application/json"       |          |  
| PAYMENT-SIGNATURE | string | Yes | EIP-3009 签名的支付数据（JSON 字符串） |  

**PAYMENT-SIGNATURE 数据格式（PAYMENT-SIGNATURE Format）**:  
```json
{
  "from": "0x1234567890abcdef1234567890abcdef12345678",
  "to": "0x1a85156c2943b63febeee7883bd84a7d1cf0da0c",
  "value": "490000",
  "validAfter": "0",
  "validBefore": "1738368000",
  "nonce": "0xabc123...",
  "v": 27,
  "r": "0x...",
  "s": "0x..."
}
```  

**时长选项（Duration Options）**:  
| 值（Value） | 时长（Duration） | 价格（Price） |  
|---------|-----------|-------------|-----------------|  
| 1       | 1 天       | 0.09 USDC         |          |  
| 7       | 7 天       | 0.49 USDC         |          |  
| 30       | 30 天       | 0.99 USDC         |          |  

**响应（Response）**:  
```json
{
  "apiKey": "sk-7ac3d7c8fed74b0a8ae8f949e017e9f5",
  "txHash": "0x1f62f45e5ae6e8cd637048d0f099d324f749f61d35906ffe481e36e92689769b",
  "payState": "paid",
  "durationDays": 7,
  "transactionId": "ed66d250-7353-473d-bc73-0bd7541f40c0"
}
```  

**响应字段（Response Fields）**:  
| 字段（Field） | 类型（Type） | 描述（Description） |  
|---------|-----------|-----------------|-----------------|  
| apiKey     | string | 你的 API 密钥（用于身份验证） |          |  
| txHash    | string | 区块链交易哈希值       |          |  
| payState   | string | 支付状态（"paid"）       |          |  
| durationDays | number | API 密钥有效期（天数）    |          |  
| transactionId | string | 唯一交易 ID       |          |  

#### POST /v1/transfer - 支付稳定币（Pay Stablecoin）  
使用 EIP-3009 离线签名将 USDC 支付到任意地址。  

#### GET /user/me - 获取用户信息（Get User Information）  
获取用户账户信息、API 密钥和使用统计信息。**需要使用 API 密钥进行身份验证**。  

**响应（Response）**:  
```bash
curl "http://ipaynapi.gpuart.cn/user/me" \
  -H "Authorization: Bearer YOUR_API_KEY"
```  

**注意（Note）**: 首次购买会自动创建用户账户，无需单独注册！  

#### GET /user/my-keys - 列出用户 API 密钥（List User API Keys）  
获取用户账户的所有 API 密钥。**需要使用 API 密钥进行身份验证**。  

**响应（Response）**:  
```bash
curl "http://ipaynapi.gpuart.cn/user/my-keys" \
  -H "Authorization: Bearer YOUR_API_KEY"
```  

#### POST /v1/transfer - 支付稳定币（Pay Stablecoin）  
使用 EIP-3009 离线签名将 USDC 支付到任意地址。  

**请求体（Request Body）**:  
```json
{
  "to": "0x1234567890abcdef1234567890abcdef12345678",
  "amount": "10000",
  "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
}
```  

**参数（Parameters）**:  
| 参数（Parameter） | 类型（Type） | 是否必需（Required） | 描述（Description） |  
|------------|-----------|-----------------|-----------------|  
| to       | string | 是（Yes）      | 收款人钱包地址       |  
| amount     | string | 是（Yes）      | 金额（最小单位：10000 = 0.01 USDC） |  
| asset     | string | 是（Yes）      | 代币合约地址（Base Sepolia 上的 USDC） |  

**请求头（Headers）**:  
| 头部字段（Header Field） | 类型（Type） | 是否必需（Required） | 描述（Description） |  
|-----------------|-----------|-----------------|-----------------|  
| Content-Type | string | 是（Yes）      | "application/json"       |          |  
| PAYMENT-SIGNATURE | string | 是（Yes）      | EIP-3009 签名的支付数据（JSON 字符串） |          |  

**响应（Response）**:  
```json
{
  "success": true,
  "transactionHash": "0x1234567890abcdef...",
  "from": "0xabcdef1234567890abcdef1234567890abcdef12",
  "to": "0x1234567890abcdef1234567890abcdef12345678",
  "amount": "0.010000",
  "deductedAmount": "0.010000 USDC",
  "currentBalance": "9.990000 USDC"
}
```  

## 用户管理（New Feature）  
iAutoPay 系统现在支持**自动用户注册**。首次购买 API 密钥时，会自动创建用户账户并将其关联到用户的钱包地址。  

### 自动注册流程（Auto-Registration Process）  
1. **首次购买（First Purchase）**: 使用已签名的支付请求调用 `/v1/buy-apikey`  
2. **自动创建用户（Auto-Create User）**: 系统自动创建用户账户  
3. **分配 API 密钥（Assign API Key）**: API 密钥与用户账户关联  
4. **查看用户信息（View User Info）**: 使用 `/user/me` 查看账户详情  

无需单独注册！  

### 用户端点（User Endpoints）  

#### GET /user/me - 获取用户信息（Get User Information）  
获取用户账户信息、API 密钥和使用统计信息。  

**响应（Response）**:  
```bash
curl "http://ipaynapi.gpuart.cn/user/me" \
  -H "Authorization: Bearer YOUR_API_KEY"
```  

#### GET /user/my-keys - 列出用户 API 密钥（List User API Keys）  
获取用户账户的所有 API 密钥。  

**响应（Response）**:  
```bash
curl "http://ipaynapi.gpuart.cn/user/my-keys" \
  -H "Authorization: Bearer YOUR_API_KEY"
```  

#### GET /refresh_pricing - 刷新价格信息（Refresh Pricing）  
从服务器刷新价格信息（缓存数据）。  

**响应（Response）**:  
```bash
curl "https://apipaymcp.okart.fun/refresh_pricing"
```  

## napi-ser（用户管理）（User Management）  
#### GET /user/me - 获取用户信息（Get User Information）  
获取用户账户信息、API 密钥和使用统计信息。**需要使用 API 密钥进行身份验证**。  

**响应（Response）**:  
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "user_xxx",
      "walletAddress": "0x1234567890abcdef1234567890abcdef12345678",
      "createdAt": 1772072451317,
      "lastPurchasedAt": 1772072457962,
      "status": "active",
      "totalPurchases": 2
    },
    "activeApiKeys": 2,
    "totalSpent": 1480000,
    "apiKeys": [
      {
        "apiKey": "sk-xxx",
        "durationDays": 7,
        "createdAt": "2026-02-26T02:01:12.904Z",
        "expiresAt": "2026-03-05T02:01:12.904Z",
        "status": "active"
      }
    ],
    "recentTransactions": [...]
  }
}
```  

**注意（Note）**: 首次购买会自动创建用户账户，无需单独注册！  

#### GET /user/my-keys - 列出用户 API 密钥（List User API Keys）  
获取用户账户的所有 API 密钥。**需要使用 API 密钥进行身份验证**。  

**响应（Response）**:  
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "apiKey": "sk-xxx",
      "durationDays": 7,
      "createdAt": "2026-02-26T02:01:12.904Z",
      "expiresAt": "2026-03-05T02:01:12.904Z",
      "status": "active"
    }
  ]
}
```  

## 支付流程（Payment Process）  
Fact API 使用 **EIP-3009（TransferWithAuthorization）** 进行离线支付签名。这意味着你无需先发送链上交易——只需签名支付授权信息并将其包含在 API 请求中。  

**步骤（Steps）**:  
1. **获取支付信息（Get Payment Info）**: 调用 `/info` 获取收款人地址和 USDC 合约地址  
2. **签名支付（Sign Payment）**: 使用钱包的私钥创建 EIP-3009 签名  
3. **购买 API 密钥（Buy API Key）**: 使用包含 `PAYMENT-SIGNATURE` 的请求头调用 `/v1/buy-apikey`  
4. **自动注册（Auto-Registration）**: 首次购买会自动创建用户账户  
5. **查看用户信息（View User Info）**: 使用 `/user/me` 和 API 密钥查看账户详情  

**重要提示（Important Notes）**:  
- 无需单独注册  
- 首次购买会自动创建用户账户  
- 用户账户与钱包地址关联  
- 未来的所有购买操作都将关联到同一用户账户  

## 用户管理端点（napi-ser）（User Management Endpoints）  
- `GET /user/me` - 获取用户信息、API 密钥和使用统计信息  
- `GET /user/my-keys` - 列出用户账户的所有 API 密钥  

**EIP-3009 签名要求（EIP-3009 Signature Requirements）**:  
- **域名（Domain）**: 代币名称、版本（USDC 为 2）、链 ID（chainId）、验证合约（verifyingContract，USDC 地址）  
- **类型（Type）**: TransferWithAuthorization（from, to, value, validAfter, validBefore, nonce）  
- **有效期（Valid Before）**: 当前时间戳 + 8 小时（28800 秒）  

**USDC 合约（USDC Contract）**: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`（Base Sepolia）  
**收款人（Payee）**: `0x1a85156c2943b63febeee7883bd84a7d1cf0da0c`  

## CLI 脚本（CLI Scripts）  
该技能包含适用于所有端点的现成 CLI 脚本。  

**依赖项（Dependencies）**:  
```bash
# TypeScript/Bun
bun add viem dotenv

# Python
pip install web3 requests python-dotenv
```  

### 获取服务器信息（Get Server Info）  
```bash
# Python
python scripts/info.py

# TypeScript/Bun
bun run scripts/info.ts
```  

### 获取钱包地址（Get Wallet Address）  
```bash
# Python
python scripts/get_address.py

# TypeScript/Bun
bun run scripts/get_address.ts
```  

### 购买 API 密钥（Buy API Key）  
```bash
# Python
python scripts/buy_apikey.py --duration 7

# TypeScript/Bun
bun run scripts/buy_apikey.ts --duration 7
```  

### 刷新价格信息（Refresh Pricing）  
```bash
# Python
python scripts/refresh_pricing.py

# TypeScript/Bun
bun run scripts/refresh_pricing.ts
```  

## Python 实现（Python Implementation）  
### info.py  
```python
import requests

def get_info():
    response = requests.get("https://apipaymcp.okart.fun/info")
    return response.json()

if __name__ == "__main__":
    info = get_info()
    print(f"Environment: {info['environment']}")
    print(f"Network: {info['network']}")
    print(f"Payee: {info['payee']}")
    print(f"Asset: {info['asset']}")
    print(f"Pricing:")
    for key, value in info['prices'].items():
        print(f"  {key}: {value}")
```  

### get_address.py  
```python
from web3 import Web3
import os

def get_address(private_key: str = None):
    if private_key is None:
        private_key = os.environ.get('AUTOPAY_PKEY')
        if not private_key:
            raise ValueError("AUTOPAY_PKEY environment variable not set")
    
    w3 = Web3()
    account = w3.eth.account.from_key(private_key)
    return account.address

if __name__ == "__main__":
    address = get_address()
    print(f"Your Wallet Address: {address}")
```  

### buy_apikey.py  
```python
import requests
from web3 import Web3
import json
import time
import os

def buy_apikey(duration: int, private_key: str = None):
    if private_key is None:
        private_key = os.environ.get('AUTOPAY_PKEY')
        if not private_key:
            raise ValueError("AUTOPAY_PKEY environment variable not set")
    
    w3 = Web3(Web3.HTTPProvider("https://sepolia.base.org"))
    account = w3.eth.account.from_key(private_key)
    
    # Step 1: Get payment quote
    info_response = requests.get("https://apipaymcp.okart.fun/info")
    info = info_response.json()
    
    payee_address = info['payee']
    usdc_address = info['asset']
    price_in_usdc = info['prices'][f'{duration}daysUsdc']
    
    # USDC uses 6 decimals
    amount = int(price_in_usdc * 10 ** 6)
    
    # Step 2: Create EIP-3009 signature
    # For Base Sepolia USDC: name="USDC", version="2"
    domain = {
        "name": "USDC",
        "version": "2",
        "chainId": 84532,
        "verifyingContract": usdc_address
    }
    
    message_types = {
        "TransferWithAuthorization": [
            {"name": "from", "type": "address"},
            {"name": "to", "type": "address"},
            {"name": "value", "type": "uint256"},
            {"name": "validAfter", "type": "uint256"},
            {"name": "validBefore", "type": "uint256"},
            {"name": "nonce", "type": "bytes32"}
        ]
    }
    
    nonce = os.urandom(32).hex()
    now = int(time.time())
    valid_after = 0
    valid_before = now + 28800  # 8 hours
    
    message = {
        "from": account.address,
        "to": payee_address,
        "value": amount,
        "validAfter": valid_after,
        "validBefore": valid_before,
        "nonce": f"0x{nonce}"
    }
    
    # Sign typed data
    signed_message = w3.eth.account.sign_typed_data(
        private_key=private_key,
        domain=domain,
        message_types=message_types,
        message=message
    )
    
    signature_payload = {
        "from": account.address,
        "to": payee_address,
        "value": str(amount),
        "validAfter": str(valid_after),
        "validBefore": str(valid_before),
        "nonce": f"0x{nonce}",
        "v": signed_message.v,
        "r": signed_message.r.hex(),
        "s": signed_message.s.hex()
    }
    
    # Step 3: Call buy-apikey with EIP-3009 signature
    buy_response = requests.post(
        "https://apipaymcp.okart.fun/v1/buy-apikey",
        headers={
            "Content-Type": "application/json",
            "PAYMENT-SIGNATURE": json.dumps(signature_payload)
        },
        json={"duration": duration}
    )
    
    if buy_response.status_code != 200:
        raise Exception(f"Buy API key failed: {buy_response.text}")
    
    return {
        "apiKey": buy_response.json()['apiKey'],
        "txHash": buy_response.json()['txHash'],
        "payState": buy_response.json()['payState'],
        "durationDays": buy_response.json()['durationDays'],
        "transactionId": buy_response.json()['transactionId']
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=int, choices=[1, 7, 30], required=True)
    args = parser.parse_args()
    
    result = buy_apikey(args.duration)
    print(json.dumps(result, indent=2))
```  

### refresh_pricing.py  
```python
import requests

def refresh_pricing():
    response = requests.get("https://apipaymcp.okart.fun/refresh_pricing")
    return response.json()

if __name__ == "__main__":
    pricing = refresh_pricing()
    print(f"Pricing updated at: {pricing.get('updatedAt', 'N/A')}")
    if 'prices' in pricing:
        print(f"1 day: ${pricing['prices']['1dayUsdc']} USDC")
        print(f"7 days: ${pricing['prices']['7daysUsdc']} USDC")
        print(f"30 days: ${pricing['prices']['30daysUsdc']} USDC")
```  

## TypeScript 实现（TypeScript Implementation）  
### info.ts  
```typescript
async function getInfo() {
  const response = await fetch("https://apipaymcp.okart.fun/info");
  return response.json();
}

const info = await getInfo();
console.log(`Environment: ${info.environment}`);
console.log(`Network: ${info.network}`);
console.log(`Payee: ${info.payee}`);
console.log(`Asset: ${info.asset}`);
console.log("Pricing:");
Object.entries(info.prices).forEach(([key, value]) => {
  console.log(`  ${key}: ${value}`);
});
```  

### get_address.ts  
```typescript
import { privateKeyToAccount } from "viem/accounts";

function getAddress(privateKey?: `0x${string}`): string {
  const key = privateKey || (process.env.AUTOPAY_PKEY as `0x${string}`);
  if (!key) {
    throw new Error("AUTOPAY_PKEY environment variable not set");
  }
  
  const account = privateKeyToAccount(key);
  return account.address;
}

const address = getAddress();
console.log(`Your Wallet Address: ${address}`);
```  

### buy_apikey.ts  
```typescript
import { createWalletClient, http, parseUnits } from "viem";
import { baseSepolia } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";
import crypto from "crypto";

const transferWithAuthorizationTypes = {
  TransferWithAuthorization: [
    { name: "from", type: "address" },
    { name: "to", type: "address" },
    { name: "value", type: "uint256" },
    { name: "validAfter", type: "uint256" },
    { name: "validBefore", type: "uint256" },
    { name: "nonce", type: "bytes32" },
  ],
} as const;

async function buyApikey(duration: number, privateKey: `0x${string}` | undefined = undefined) {
  const key = privateKey || (process.env.AUTOPAY_PKEY as `0x${string}`)
  if (!key) {
    throw new Error("AUTOPAY_PKEY environment variable not set")
  }
  
  const account = privateKeyToAccount(key);
  const client = createWalletClient({
    account,
    chain: baseSepolia,
    transport: http()
  });
  
  // Step 1: Get payment quote
  const infoResponse = await fetch("https://apipaymcp.okart.fun/info");
  const info = await infoResponse.json();
  
  const payeeAddress = info.payee as `0x${string}`;
  const usdcAddress = info.asset as `0x${string}`;
  const priceInUsdc = info.prices[`${duration}daysUsdc`];
  
  // USDC uses 6 decimals
  const amount = parseUnits(priceInUsdc.toString(), 6);
  
  // Step 2: Create EIP-3009 signature
  // For Base Sepolia USDC: name="USDC", version="2"
  const nonce = `0x${crypto.randomBytes(32).toString("hex")}` as `0x${string}`;
  const now = Math.floor(Date.now() / 1000);
  const validAfter = BigInt(0);
  const validBefore = BigInt(now + 28800); // 8 hours
  
  const signature = await client.signTypedData({
    domain: {
      name: "USDC",
      version: "2",
      chainId: 84532,
      verifyingContract: usdcAddress,
    },
    types: transferWithAuthorizationTypes,
    primaryType: "TransferWithAuthorization",
    message: {
      from: account.address,
      to: payeeAddress,
      value: amount,
      validAfter,
      validBefore,
      nonce,
    },
  });
  
  const signaturePayload = {
    from: account.address,
    to: payeeAddress,
    value: amount.toString(),
    validAfter: validAfter.toString(),
    validBefore: validBefore.toString(),
    nonce,
    v: Number((signature.slice(-2) as `0x${string}`)),
    r: signature.slice(0, 66) as `0x${string}`,
    s: `0x${signature.slice(66, 130)}` as `0x${string}`
  };
  
  // Step 3: Call buy-apikey with EIP-3009 signature
  const buyResponse = await fetch("https://apipaymcp.okart.fun/v1/buy-apikey", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "PAYMENT-SIGNATURE": JSON.stringify(signaturePayload)
    },
    body: JSON.stringify({ duration })
  });
  
  if (buyResponse.status !== 200) {
    throw new Error(`Buy API key failed: ${await buyResponse.text()}`);
  }
  
  const buyData = await buyResponse.json();
  
  return {
    apiKey: buyData.apiKey,
    txHash: buyData.txHash,
    payState: buyData.payState,
    durationDays: buyData.durationDays,
    transactionId: buyData.transactionId
  };
}
```  

### refresh_pricing.ts  
```typescript
async function refreshPricing() {
  const response = await fetch("https://apipaymcp.okart.fun/refresh_pricing");
  return response.json();
}

const pricing = await refreshPricing();
console.log(`Updated: ${pricing.updatedAt}`);
if (pricing.prices) {
  console.log(`1 day: $${pricing.prices['1dayUsdc']} USDC`);
  console.log(`7 days: $${pricing.prices['7daysUsdc']} USDC`);
  console.log(`30 days: $${pricing.prices['30daysUsdc']} USDC`);
}
```  

## 完整购买流程（Complete Purchase Flow）  
```typescript
// 1. Check server info and pricing
const info = await fetch("https://apipaymcp.okart.fun/info").then(r => r.json());
console.log(`Current pricing: ${JSON.stringify(info.prices)}`);
console.log(`Payee address: ${info.payee}`);
console.log(`USDC contract: ${info.asset}`);

// 2. Create EIP-3009 signature
const privateKey = process.env.AUTOPAY_PKEY as `0x${string}`
const account = privateKeyToAccount(privateKey);
const client = createWalletClient({
  account,
  chain: baseSepolia,
  transport: http()
});

const nonce = `0x${crypto.randomBytes(32).toString("hex")}`;
const now = Math.floor(Date.now() / 1000);
const validAfter = BigInt(0);
const validBefore = BigInt(now + 28800); // 8 hours
const amount = parseUnits("0.49", 6); // for 7-day key

const signature = await client.signTypedData({
  domain: {
    name: "USDC",
    version: "2",
    chainId: 84532,
    verifyingContract: info.asset,
  },
  types: transferWithAuthorizationTypes,
  primaryType: "TransferWithAuthorization",
  message: {
    from: account.address,
    to: info.payee,
    value: amount,
    validAfter,
    validBefore,
    nonce,
  },
});

const signaturePayload = {
  from: account.address,
  to: info.payee,
  value: amount.toString(),
  validAfter: validAfter.toString(),
  validBefore: validBefore.toString(),
  nonce,
  v: Number((signature.slice(-2) as `0x${string}`)),
  r: signature.slice(0, 66) as `0x${string}`,
  s: `0x${signature.slice(66, 130)}` as `0x${string}`
};

// 3. Buy API key with EIP-3009 signature
const purchase = await fetch("https://apipaymcp.okart.fun/v1/buy-apikey", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "PAYMENT-SIGNATURE": JSON.stringify(signaturePayload)
  },
  body: JSON.stringify({
    duration: 7
  })
}).then(r => r.json());

console.log(`   API Key: ${result.apiKey}`);
console.log(`   TX Hash: ${result.txHash}`);
console.log(`   Pay State: ${result.payState}`);
console.log(`   Duration: ${result.durationDays} days`);
console.log(`   Transaction ID: ${result.transactionId}`);
```  

## 错误处理（Error Handling）  
所有端点返回的错误代码如下：  
```json
{
  "code": "PAYMENT_FAILED",
  "message": "Insufficient USDC balance",
  "details": { "required": "0.49", "available": "0.25" }
}
```  

**常见错误代码（Common Error Codes）**:  
- `INVALID_DURATION`（400） - 时长必须为 1、7 或 30  
- `PAYMENT_FAILED`（402） - 支付交易失败  
- `INSUFFICIENT_BALANCE`（402） - 钱包余额不足  
- `RATE_LIMITED`（429） - 请求次数过多  
- `INTERNAL_ERROR`（500） - 服务器错误  

## 安全注意事项（Security Notes）  
### 私钥管理（Private Key Management）  
**切勿将私钥提交到版本控制系统中！**  

**自动注册安全机制（Auto-Registration Security）**:  
- 首次购买时自动创建用户账户  
- 无需单独的注册端点  
- 用户账户与钱包地址关联  
- 未来的所有购买操作都关联到同一用户账户  
- 可通过 `/user/me` 和 API 密钥访问用户信息  

**推荐方法（Recommended Approaches）**:  
1. **环境变量（Environment Variables）**（推荐）  
    ```bash
    # Set in shell
    export AUTOPAY_PKEY="0x..."
    
    # Or in .env file
    echo "AUTOPAY_PKEY=0x..." > .env
    ```  

2. **CLI 参数（CLI Arguments）**（用于测试）  
    ```bash
    # Use AUTOPAY_PKEY environment variable
    export AUTOPAY_PKEY="0x..."
    python scripts/buy_apikey.py --duration 7
    bun run scripts/buy_apikey.ts --duration 7
    ```  

3. **技能实现（Skill Implementation）**:  
   - 通过环境变量传递私钥  
   - 不要在代码中硬编码私钥  
   - 使用 `.env` 文件通过 `dotenv` 加载私钥  

**最佳实践（Best Practices）**:  
- 使用专用钱包进行 API 支付（非主钱包）  
- 在主网之前在 Base Sepolia（链 ID：84532）上进行测试  
- 安全存储 API 密钥（环境变量或密钥管理工具）  
- 在使用 API 密钥前在 Base Sepolia 探索器中验证交易  
- 定期轮换 API 密钥