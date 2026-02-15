---
name: aisp
version: 1.0.2
description: 该功能允许AI代理与AISP（Agent Inference Sharing Protocol）进行交互，以便租用或提供DIEM API的计算资源。适用于使用diem-marketplace、Venice API密钥、USDC托管服务、进行资源租赁的场景，或者当用户希望租用计算资源或发布API密钥时使用。
metadata: {"openclaw":{"homepage":"https://github.com/DaveO280/Diem-Marketplace-V2-","emoji":"⚡","requires":{"env":["BACKEND_URL"]}}}
---

# AISP代理技能

Agent Inference Sharing Protocol（AISP）允许代理通过USDC托管服务租赁闲置的DIEM/Venice API容量。提供商会列出可租赁的API密钥；代理完成付款后即可自动获取这些密钥。

## 架构

```
Agent: fund() → Backend sees Funded event → Key released → Agent uses Venice API
Provider: list() → Agent funds → Term expires → settle() → Provider paid (99%, 1% fee)
```

## 代理工作流程（租赁流程）

1. 从后端获取可租赁的API列表：`GET /api/listings`
2. 如有需要，批准USDC付款（通过`fund`合约进行支付）
3. 在链上完成付款：`contract.fund(listingId, termDays, diemAmount)` → 返回`rentalId`
4. 获取API密钥：`POST /api/key/{rentalId}`，并附上签名消息`diem-marketplace:get-key:{rentalId}:{timestamp}`
5. 在`expiresAt`（Unix时间戳）之前使用该API密钥访问Venice API

### 代理SDK

```typescript
import { DiemAgent } from "diem-marketplace-sdk";

const agent = new DiemAgent({
  signer: wallet,
  contractAddress: "0x...",
  backendUrl: "https://diem-marketplace-backend.fly.dev",
  usdcAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
});

const listings = await agent.getListings();
const { apiKey, expiresAt } = await agent.rent(
  listings[0].listingId,
  termDays,
  ethers.parseUnits(diemAmount, 6)
);
```

## 提供商工作流程（发布租赁信息）

1. 在链上创建租赁信息：`contract.list(pricePerDay, termDays, diemMin, diemMax)` → 生成`listingId`
2. 将API密钥存储在后端：`POST /api/keys`，包含`{listingId, apiKey, signature, timestamp}`信息
   - 发送的消息格式：`diem-marketplace:store-key:{listingId}:{timestamp}`
3. 租赁到期时进行结算：`contract.settle(rentalId)` → 提供商获得99%的租金，1%作为协议费用

### 提供商SDK

```typescript
import { DiemProvider } from "diem-marketplace-sdk";

const provider = new DiemProvider({
  signer: wallet,
  contractAddress: "0x...",
  backendUrl: "https://diem-marketplace-backend.fly.dev",
  usdcAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
});

const listingId = await provider.createListing({
  pricePerDay: ethers.parseUnits("0.80", 6),
  termDays: 30,
  diemMin: ethers.parseUnits("1000", 6),
  diemMax: ethers.parseUnits("4000", 6),
  apiKey: "vn-scoped-...",
});
```

## 关键文件路径

| 文件路径 | 功能 |
|------|---------|
| `sdk/src/agent.ts` | DiemAgent模块：处理获取租赁信息、租赁操作、获取自己的租赁记录等功能 |
| `sdk/src/provider.ts` | DiemProvider模块：处理创建租赁信息、结算、撤销租赁及退款等功能 |
| `backend/src/routes.ts` | 后端API路由：/api/listings、/api/keys、/api/key/:id |
| `contracts/DiemMarketplace.sol` | 负责链上托管服务及收取1%的协议费用 |

## 后端API

| API端点 | 方法 | 功能 |
|----------|--------|---------|
| `/api/listings` | GET | 获取所有可租赁的API信息 |
| `/api/listings/:id` | GET | 查看特定租赁信息的详情 |
| `/api/keys` | POST | 提供商存储API密钥 |
| `/api/key/:rentalId` | POST | 代理获取API密钥（需要提供签名） |
| `/api/balance` | POST | 检查代理的DIEM余额（用于支付API密钥费用） |
| `/api/requests` | POST | 创建租赁请求 |

## 签名方式

所有需要身份验证的后端请求均使用EIP-191签名方式：
- `getKey`：`diem-marketplace:get-key:{rentalId}:{timestamp}`  
- `storeKey`：`diem-marketplace:store-key:{listingId}:{timestamp}`  
- `balance`：请求体中包含`apiKey`（无需签名）

## 合同信息

- **链上合约版本**：Base（8453）
- **主网地址**：`0xeeDa7657f2018b3b71B444b7ca2D8dE91b3B08f3`
- **USDC地址**：`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

## 安全性与签名要求

- 必须使用外部签名工具或硬件钱包进行密钥管理；严禁直接粘贴原始私钥。
- 在进行资金转移或使用凭证之前，必须获得用户的明确授权。
- Venice API密钥仅限用于推理用途，具有可撤销性，并且为了托管服务的安全需要使用最小权限。

## 注意事项

- Venice API密钥仅限用于推理操作（不具备管理权限）。
- 结算时将扣除1%的协议费用。