---
name: x402
description: **x402 HTTP原生支付协议：适用于Celo平台上的AI代理**  
该协议专为Celo平台上的AI代理设计，适用于实现按使用量计费的API、代理微支付功能，以及基于稳定币的HTTP 402“Payment Required”（需要支付）流程。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# x402：基于HTTP的原生代理支付系统

x402是一种开放协议，它利用HTTP 402“需要支付”状态码来实现人工智能代理和应用无需许可即可即时进行微支付的功能，这些支付使用的是稳定币（stablecoins）。

## 使用场景

- 实现按使用次数计费的API端点
- 构建能够自主支付服务费用的人工智能代理
- 为内容或数据访问创建微支付流程
- 在没有传统支付基础设施的情况下接受稳定币支付

## 主要优势

| 特点 | 传统支付方式 | x402 |
|---------|---------------------|------|
| 设置时间 | 几天到几周 | 几分钟 |
| 结算时间 | 2-7天 | 在Celo网络中仅需几毫秒 |
| 费用 | 2-3% + 0.30美元 | 约0.001美元（gas费用） |
| 最小支付金额 | 0.50美元以上 | 0.001美元 |
| 对人工智能代理的支持 | 不支持 | 原生支持 |

## 安装

```bash
npm install thirdweb
```

## 客户端（React）

使用`useFetchWithPayment`钩子来实现自动支付处理：

```typescript
import { useFetchWithPayment } from "thirdweb/react";
import { createThirdwebClient } from "thirdweb";

const client = createThirdwebClient({ clientId: "your-client-id" });

function PaidAPIComponent() {
  const { fetchWithPayment, isPending } = useFetchWithPayment(client);

  const handleApiCall = async () => {
    // Automatically handles:
    // - Wallet connection prompts
    // - Payment signing
    // - Insufficient funds UI
    // - Retry logic
    const data = await fetchWithPayment(
      "https://api.example.com/paid-endpoint"
    );
    console.log(data);
  };

  return (
    <button onClick={handleApiCall} disabled={isPending}>
      {isPending ? "Processing..." : "Access Premium Content"}
    </button>
  );
}
```

## 客户端（TypeScript）

对于非React应用程序，可以使用`wrapFetchWithPayment`：

```typescript
import { wrapFetchWithPayment } from "thirdweb/x402";
import { createThirdwebClient } from "thirdweb";
import { privateKeyToAccount } from "thirdweb/wallets";

const client = createThirdwebClient({ clientId: "your-client-id" });
const account = privateKeyToAccount({ client, privateKey: "0x..." });

const fetchWithPayment = wrapFetchWithPayment({
  client,
  account,
  paymentOptions: {
    maxValue: "1000000", // Max payment in base units
  },
});

// Use like regular fetch - payments handled automatically
const response = await fetchWithPayment("https://api.example.com/premium");
const data = await response.json();
```

## 服务器端（Next.js）

在API端点中接受x402支付：

```typescript
// app/api/premium-content/route.ts
import { settlePayment, facilitator } from "thirdweb/x402";
import { createThirdwebClient } from "thirdweb";
import { celo } from "thirdweb/chains";

const client = createThirdwebClient({
  secretKey: process.env.THIRDWEB_SECRET_KEY,
});

const thirdwebFacilitator = facilitator({
  client,
  serverWalletAddress: "0xYourServerWalletAddress",
});

export async function GET(request: Request) {
  const paymentData =
    request.headers.get("PAYMENT-SIGNATURE") ||
    request.headers.get("X-PAYMENT");

  const result = await settlePayment({
    resourceUrl: "https://your-api.com/premium-content",
    method: "GET",
    paymentData,
    payTo: "0xYourWalletAddress",
    network: celo, // Use Celo chain
    price: "$0.01", // Price in USD
    facilitator: thirdwebFacilitator,
    routeConfig: {
      description: "Access to premium API content",
      mimeType: "application/json",
    },
  });

  if (result.status === 200) {
    return Response.json({ data: "premium content" });
  } else {
    return Response.json(result.responseBody, {
      status: result.status,
      headers: result.responseHeaders,
    });
  }
}
```

## 服务器端（Express）

```typescript
import express from "express";
import { settlePayment, facilitator } from "thirdweb/x402";
import { createThirdwebClient } from "thirdweb";
import { celo } from "thirdweb/chains";

const app = express();

const client = createThirdwebClient({
  secretKey: process.env.THIRDWEB_SECRET_KEY,
});

const thirdwebFacilitator = facilitator({
  client,
  serverWalletAddress: "0xYourServerWalletAddress",
});

app.get("/api/premium", async (req, res) => {
  const paymentData = req.headers["payment-signature"] || req.headers["x-payment"];

  const result = await settlePayment({
    resourceUrl: `${req.protocol}://${req.get("host")}${req.originalUrl}`,
    method: "GET",
    paymentData,
    payTo: "0xYourWalletAddress",
    network: celo,
    price: "$0.05",
    facilitator: thirdwebFacilitator,
  });

  if (result.status === 200) {
    res.json({ data: "premium content" });
  } else {
    res.status(result.status).set(result.responseHeaders).json(result.responseBody);
  }
});
```

## 支付流程

1. **客户端请求资源** - 人工智能代理或应用程序发送HTTP请求
2. **服务器返回402状态码** - 如果未支付，返回`HTTP 402 Payment Required`状态码并附带支付详情
3. **客户端签署支付授权** - 客户端完成支付授权
4. **客户端重新发送请求并添加`X-PAYMENT`头部** - 重新发送请求时包含支付信息
5. **服务器验证并结算** - 在区块链上验证并完成支付
6. **服务器提供资源** - 返回资源的同时附上支付收据

## Celo网络支持的支付代币

| 代币 | 地址 | 小数位数 |
|-------|---------|----------|
| USDC | `0xcebA9300f2b948710d2653dD7B07f33A8B32118C` | 6 |
| USDT | `0x48065fbbe25f71c9282ddf5e1cd6d6a887483d5e` | 6 |
| USDm | `0x765DE816845861e75A25fCA122bb6898B8B1282a` | 18 |

## Celo网络配置

```typescript
import { celo, celoSepolia } from "thirdweb/chains";

// Mainnet
const mainnetConfig = {
  network: celo,
  price: "$0.01",
};

// Testnet (Sepolia)
const testnetConfig = {
  network: celoSepolia,
  price: "$0.01",
};
```

## 人工智能代理的使用

### 自主API支付

```typescript
// AI agent paying for API calls autonomously
const agent = {
  wallet: agentWallet,
  fetchWithPayment: wrapFetchWithPayment({
    client,
    account: agentWallet
  }),
};

// Agent pays per API call - no API keys needed
const marketData = await agent.fetchWithPayment("https://api.market.com/prices");
const analysis = await agent.fetchWithPayment("https://api.ai.com/analyze");
```

### 按使用次数计费的AI推理服务

```typescript
// Server: Charge based on actual token usage with "upto" scheme
const result = await settlePayment({
  resourceUrl: request.url,
  method: "POST",
  paymentData,
  payTo: "0xYourWallet",
  network: celo,
  scheme: "upto",           // Dynamic pricing
  price: "$1.00",           // Maximum amount
  minPrice: "$0.01",        // Minimum amount
  facilitator: thirdwebFacilitator,
});

// Verify first, then charge based on actual usage
const { tokens } = await runAIInference(prompt);
const actualPrice = tokens * 0.0001; // $0.0001 per token

await settlePayment({
  ...paymentArgs,
  price: actualPrice,
});
```

### 用于内容的微支付

```typescript
// Pay-per-article instead of subscriptions
app.get("/articles/:id", async (req, res) => {
  const result = await settlePayment({
    resourceUrl: req.url,
    method: "GET",
    paymentData: req.headers["x-payment"],
    payTo: publisherWallet,
    network: celo,
    price: "$0.10",
    facilitator: thirdwebFacilitator,
    routeConfig: {
      description: "Premium article access",
    },
  });
  // ...
});
```

## 与ERC-8004的集成

将信任验证与支付功能结合使用：

```typescript
import { ReputationRegistry } from '@chaoschain/sdk';
import { wrapFetchWithPayment } from 'thirdweb/x402';

async function payTrustedService(agentId, serviceUrl) {
  // 1. Check reputation first
  const summary = await reputationRegistry.getSummary(agentId);
  if (summary.averageScore < 80) {
    throw new Error('Service reputation too low');
  }

  // 2. Make payment
  const response = await fetchWithPayment(serviceUrl);

  // 3. Submit feedback
  await reputationRegistry.giveFeedback(agentId, 90, 0, 'starred', ...);

  return response.json();
}
```

## 环境变量

```bash
# Client-side
NEXT_PUBLIC_THIRDWEB_CLIENT_ID=your_client_id

# Server-side
THIRDWEB_SECRET_KEY=your_secret_key
```

## Celo网络信息

| 网络 | 链路ID | RPC端点 |
|---------|----------|--------------|
| Celo主网 | 42220 | https://forno.celo.org |
| Celo Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org |

## 为什么选择Celo来实现x402？

- **低费用**：每次交易的gas费用低于0.001美元
- **快速结算**：区块确认时间约为1秒
- **支持稳定币**：原生支持USDC、USDT、USDm等稳定币
- **费用抽象**：用户可以使用稳定币来支付gas费用

## 额外资源

- [x402官方网站](https://www.x402.org)
- [thirdweb x402文档](https://portal.thirdweb.com/x402)
- [thirdweb测试平台](https://playground.thirdweb.com/x402)
- [x402白皮书](https://www.x402.org/x402-whitepaper.pdf)
- [GitHub仓库](https://github.com/coinbase/x402)

## 相关技能

- [8004](../8004/SKILL.md) - 用于人工智能代理的信任层技术
- [thirdweb](../thirdweb/SKILL.md) - 全栈Web3开发技术
- [fee-abstraction](../fee-abstraction/SKILL.md) - 使用稳定币支付gas费用的技术