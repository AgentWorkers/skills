---
name: purch-api
description: |
  AI-powered shopping API for product search and crypto checkout. Use this skill when:
  - Searching for products from Amazon and Shopify
  - Building shopping assistants or product recommendation features
  - Creating purchase orders with crypto (USDC on Solana or Base)
  - Integrating e-commerce checkout into applications
  - Signing and submitting blockchain transactions for purchases
---

# 购物公共API

基础URL：`https://api.purch.xyz`

## 速率限制

每个IP每分钟允许60次请求。每个响应中包含以下头部信息：
- `X-RateLimit-Limit`：当前时间窗口内的最大请求次数
- `X-RateLimit-Remaining`：剩余的请求次数
- `X-RateLimit-Reset`：距离重置还有多少秒

## 端点

### GET /search - 结构化产品搜索

通过过滤器查询产品。

```bash
curl "https://api.purch.xyz/search?q=headphones&priceMax=100"
```

**参数：**
| 参数 | 类型 | 是否必填 | 描述 |
|-------|------|----------|-------------|
| q | 字符串 | 是 | 搜索查询 |
| priceMin | 数字 | 否 | 最低价格 |
| priceMax | 数字 | 否 | 最高价格 |
| brand | 字符串 | 否 | 按品牌过滤 |
| page | 数字 | 否 | 页码（默认：1） |

**响应：**
```json
{
  "products": [
    {
      "id": "B0CXYZ1234",
      "title": "Sony WH-1000XM5",
      "price": 348.00,
      "currency": "USD",
      "rating": 4.8,
      "reviewCount": 15420,
      "imageUrl": "https://...",
      "productUrl": "https://amazon.com/dp/B0CXYZ1234",
      "source": "amazon"
    }
  ],
  "totalResults": 20,
  "page": 1,
  "hasMore": true
}
```

### POST /shop - 人工智能购物助手

使用自然语言搜索产品。返回来自Amazon和Shopify的20多个产品。

```bash
curl -X POST "https://api.purch.xyz/shop" \
  -H "Content-Type: application/json" \
  -d '{"message": "comfortable running shoes under $100"}'
```

**请求体：**
```json
{
  "message": "comfortable running shoes under $100",
  "context": {
    "priceRange": { "min": 0, "max": 100 },
    "preferences": ["comfortable", "breathable"]
  }
}
```

**响应：**
```json
{
  "reply": "Found 22 running shoes. Top pick: Nike Revolution 6 at $65...",
  "products": [
    {
      "asin": "B09XYZ123",
      "title": "Nike Revolution 6",
      "price": 65.00,
      "currency": "USD",
      "rating": 4.5,
      "reviewCount": 8420,
      "imageUrl": "https://...",
      "productUrl": "https://amazon.com/dp/B09XYZ123",
      "source": "amazon"
    },
    {
      "asin": "gid://shopify/p/abc123",
      "title": "Allbirds Tree Runners",
      "price": 98.00,
      "source": "shopify",
      "productUrl": "https://allbirds.com/products/tree-runners",
      "vendor": "Allbirds"
    }
  ]
}
```

### POST /buy - 创建购买订单

创建订单并获取待签名的交易信息。**交易链信息会自动从钱包格式中检测出来：**
- Solana钱包（base58格式）：`7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU`
- Base/EVM钱包（0x格式）：`0x1234567890abcdef1234567890abcdef12345678`

**Solana平台上的Amazon产品：**
```bash
curl -X POST "https://api.purch.xyz/buy" \
  -H "Content-Type: application/json" \
  -d '{
    "asin": "B0CXYZ1234",
    "email": "buyer@example.com",
    "walletAddress": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
    "shippingAddress": {
      "name": "John Doe",
      "line1": "123 Main St",
      "line2": "Apt 4B",
      "city": "New York",
      "state": "NY",
      "postalCode": "10001",
      "country": "US",
      "phone": "+1-555-123-4567"
    }
  }'
```

**Base平台上的Amazon产品：**
```bash
curl -X POST "https://api.purch.xyz/buy" \
  -H "Content-Type: application/json" \
  -d '{
    "asin": "B0CXYZ1234",
    "email": "buyer@example.com",
    "walletAddress": "0x1234567890abcdef1234567890abcdef12345678",
    "shippingAddress": {
      "name": "John Doe",
      "line1": "123 Main St",
      "city": "New York",
      "state": "NY",
      "postalCode": "10001",
      "country": "US"
    }
  }'
```

**Shopify平台上的产品**：需要使用`productUrl`和`variantId`：
```bash
curl -X POST "https://api.purch.xyz/buy" \
  -H "Content-Type: application/json" \
  -d '{
    "productUrl": "https://store.com/products/item-name",
    "variantId": "41913945718867",
    "email": "buyer@example.com",
    "walletAddress": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
    "shippingAddress": {
      "name": "John Doe",
      "line1": "123 Main St",
      "city": "New York",
      "state": "NY",
      "postalCode": "10001",
      "country": "US"
    }
  }'
```

**响应：**
```json
{
  "orderId": "550e8400-e29b-41d4-a716-446655440000",
  "status": "awaiting-payment",
  "serializedTransaction": "NwbtPCP62oXk5fmSrgT...",
  "product": {
    "title": "Sony WH-1000XM5",
    "imageUrl": "https://...",
    "price": { "amount": "348.00", "currency": "usdc" }
  },
  "totalPrice": { "amount": "348.00", "currency": "usdc" },
  "checkoutUrl": "https://www.crossmint.com/checkout/550e8400..."
}
```

## CLI脚本

该技能提供了适用于所有端点的现成CLI脚本，支持Python和TypeScript/Bun语言。

**Solana平台的依赖项：**
```bash
# Python
pip install solana solders base58

# TypeScript/Bun
bun add @solana/web3.js bs58
```

**Base/EVM平台的依赖项：**
```bash
# TypeScript/Bun
bun add viem
```

### 搜索产品

```bash
# Python
python scripts/search.py "wireless headphones" --price-max 100
python scripts/search.py "running shoes" --brand Nike --page 2

# TypeScript
bun run scripts/search.ts "wireless headphones" --price-max 100
```

### 人工智能购物助手

```bash
# Python
python scripts/shop.py "comfortable running shoes under $100"

# TypeScript
bun run scripts/shop.ts "wireless headphones with good noise cancellation"
```

### 创建订单（不进行签名）

```bash
# Amazon by ASIN
python scripts/buy.py --asin B0CXYZ1234 --email buyer@example.com \
  --wallet 7xKXtg... --address "John Doe,123 Main St,New York,NY,10001,US"

# Shopify product
bun run scripts/buy.ts --url "https://store.com/products/item" --variant 41913945718867 \
  --email buyer@example.com --wallet 7xKXtg... --address "John Doe,123 Main St,NYC,NY,10001,US"
```

地址格式：`姓名,街道1号,城市,州,邮政编码,国家[,街道2号][,电话]`

### 创建订单并签名交易（Solana平台）

端到端的购买流程：创建订单并签名/提交Solana交易：

```bash
# Python
python scripts/buy_and_sign.py --asin B0CXYZ1234 --email buyer@example.com \
  --wallet 7xKXtg... --private-key 5abc123... \
  --address "John Doe,123 Main St,New York,NY,10001,US"

# TypeScript
bun run scripts/buy_and_sign.ts --url "https://store.com/products/item" --variant 41913945718867 \
  --email buyer@example.com --wallet 7xKXtg... --private-key 5abc123... \
  --address "John Doe,123 Main St,NYC,NY,10001,US"
```

### 创建订单并签名交易（Base平台）

使用Base/EVM钱包的端到端购买流程：

```bash
bun run scripts/buy_and_sign_base.ts --asin B0CXYZ1234 --email buyer@example.com \
  --wallet 0x1234567890abcdef1234567890abcdef12345678 \
  --private-key 0xabc123... \
  --address "John Doe,123 Main St,New York,NY,10001,US"
```

### 仅签名交易（Solana平台）

如果您已经从 `/buy` 端点获得了 `serializedTransaction`：

```bash
# Python
python scripts/sign_transaction.py "<serialized_tx>" "<private_key_base58>"

# TypeScript
bun run scripts/sign_transaction.ts "<serialized_tx>" "<private_key_base58>"
```

### 仅签名交易（Base平台）

```bash
bun run scripts/sign_transaction_base.ts "<serialized_tx_hex>" "<private_key_hex>"
```

**输出（Solana平台）：**
```
✅ Transaction successful!
   Signature: 5UfgJ3vN...
   Explorer:  https://solscan.io/tx/5UfgJ3vN...
```

**输出（Base平台）：**
```
✅ Transaction successful!
   Hash:     0x1234...
   Explorer: https://basescan.org/tx/0x1234...
```

## 程序化签名交易

对于不使用捆绑脚本的自定义集成：

### JavaScript/TypeScript

```typescript
import { Connection, Transaction, clusterApiUrl } from "@solana/web3.js";
import bs58 from "bs58";

async function signAndSendTransaction(
  serializedTransaction: string,
  wallet: { signTransaction: (tx: Transaction) => Promise<Transaction> }
) {
  // Decode the base58 transaction
  const transactionBuffer = bs58.decode(serializedTransaction);
  const transaction = Transaction.from(transactionBuffer);

  // Sign with user's wallet (e.g., Phantom, Solflare)
  const signedTransaction = await wallet.signTransaction(transaction);

  // Send to Solana network
  const connection = new Connection(clusterApiUrl("mainnet-beta"));
  const signature = await connection.sendRawTransaction(
    signedTransaction.serialize()
  );

  // Confirm transaction
  await connection.confirmTransaction(signature, "confirmed");

  return signature;
}
```

### 使用钱包适配器的React应用

```typescript
import { useWallet, useConnection } from "@solana/wallet-adapter-react";
import { Transaction } from "@solana/web3.js";
import bs58 from "bs58";

function CheckoutButton({ serializedTransaction }: { serializedTransaction: string }) {
  const { signTransaction, publicKey } = useWallet();
  const { connection } = useConnection();

  const handlePayment = async () => {
    if (!signTransaction || !publicKey) {
      throw new Error("Wallet not connected");
    }

    // Decode and sign
    const tx = Transaction.from(bs58.decode(serializedTransaction));
    const signed = await signTransaction(tx);

    // Send and confirm
    const sig = await connection.sendRawTransaction(signed.serialize());
    await connection.confirmTransaction(sig, "confirmed");

    console.log("Payment complete:", sig);
  };

  return <button onClick={handlePayment}>Pay with USDC</button>;
}
```

### 使用`solana-py`的Python应用

```python
import base58
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.keypair import Keypair

def sign_and_send(serialized_tx: str, keypair: Keypair) -> str:
    # Decode base58 transaction
    tx_bytes = base58.b58decode(serialized_tx)
    transaction = Transaction.deserialize(tx_bytes)

    # Sign
    transaction.sign(keypair)

    # Send
    client = Client("https://api.mainnet-beta.solana.com")
    result = client.send_transaction(transaction)

    return result.value  # transaction signature
```

## 签名Base/EVM平台上的交易

对于Base链上的订单，`serializedTransaction`是一个需要使用EVM钱包进行签名的EVM交易。

### 使用`viem`的TypeScript应用

```typescript
import { createWalletClient, http, parseTransaction } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

async function signAndSendBaseTransaction(
  serializedTransaction: string,
  privateKey: `0x${string}`
) {
  const account = privateKeyToAccount(privateKey);

  const client = createWalletClient({
    account,
    chain: base,
    transport: http(),
  });

  // Parse and send the serialized transaction
  const tx = parseTransaction(serializedTransaction as `0x${string}`);
  const hash = await client.sendTransaction(tx);

  console.log("Transaction hash:", hash);
  console.log("Explorer: https://basescan.org/tx/" + hash);

  return hash;
}
```

### 使用`wagmi`的React应用

```typescript
import { useSendTransaction } from "wagmi";
import { parseTransaction } from "viem";

function CheckoutButton({ serializedTransaction }: { serializedTransaction: string }) {
  const { sendTransaction } = useSendTransaction();

  const handlePayment = async () => {
    const tx = parseTransaction(serializedTransaction as `0x${string}`);
    sendTransaction(tx);
  };

  return <button onClick={handlePayment}>Pay with USDC on Base</button>;
}
```

## 完整的结账流程（Solana平台）

```typescript
// 1. Search for products
const searchResponse = await fetch("https://api.purch.xyz/shop", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "wireless headphones under $100" })
});
const { products, reply } = await searchResponse.json();

// 2. User selects a product, create order (Solana wallet)
const orderResponse = await fetch("https://api.purch.xyz/buy", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    asin: products[0].asin,
    email: "buyer@example.com",
    walletAddress: wallet.publicKey.toBase58(), // Solana address
    shippingAddress: {
      name: "John Doe",
      line1: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US"
    }
  })
});
const { orderId, serializedTransaction, checkoutUrl } = await orderResponse.json();

// 3. Sign and send Solana transaction
const tx = Transaction.from(bs58.decode(serializedTransaction));
const signed = await wallet.signTransaction(tx);
const signature = await connection.sendRawTransaction(signed.serialize());
await connection.confirmTransaction(signature, "confirmed");

console.log(`Order ${orderId} paid. Tx: ${signature}`);
```

## 完整的结账流程（Base平台）

```typescript
import { parseTransaction } from "viem";

// 1. Search for products
const searchResponse = await fetch("https://api.purch.xyz/shop", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ message: "wireless headphones under $100" })
});
const { products } = await searchResponse.json();

// 2. User selects a product, create order (EVM wallet)
const orderResponse = await fetch("https://api.purch.xyz/buy", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    asin: products[0].asin,
    email: "buyer@example.com",
    walletAddress: "0x1234...", // Base/EVM address - chain auto-detected
    shippingAddress: {
      name: "John Doe",
      line1: "123 Main St",
      city: "New York",
      state: "NY",
      postalCode: "10001",
      country: "US"
    }
  })
});
const { orderId, serializedTransaction } = await orderResponse.json();

// 3. Sign and send Base transaction
const tx = parseTransaction(serializedTransaction as `0x${string}`);
const hash = await walletClient.sendTransaction(tx);

console.log(`Order ${orderId} paid. Tx: ${hash}`);
```

## 备用方案：浏览器结账

如果钱包签名失败或不可用，会重定向到 `checkoutUrl` 以进行浏览器支付：

```typescript
if (!wallet.connected) {
  window.open(checkoutUrl, "_blank");
}
```

## 错误处理

所有端点都会返回错误信息，错误代码如下：
- `VALIDATION_ERROR` (400) - 请求参数无效
- `NOT_FOUND` (404) - 产品未找到
- `RATE_LIMITED` (429) - 请求次数过多
- `INTERNAL_ERROR` (500) - 服务器错误