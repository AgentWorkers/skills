---
name: aurex
description: 通过 Aurex API 发行虚拟的加密货币支付卡并管理相关支付操作。当用户需要创建虚拟的 Visa/Mastercard 卡、处理 SOL/USDT/USDC 类型的加密货币存款、管理用户账户、为卡片充值或查询交易历史时，可以使用该 API。您可以在 aurex.cash 的“仪表盘”（Dashboard）页面下的“API 密钥”（API Keys）区域获取 API 密钥。
primaryEnv: AUREX_API_KEY
credentials:
  - name: AUREX_API_KEY
    description: Your Aurex API key from aurex.cash dashboard. Never log or expose this value.
    required: true
---
# Aurex

使用Aurex API程序化地发行虚拟加密货币支持的卡片并管理支付。

## 设置

在 [aurex.cash](https://aurex.cash) 的“仪表板”（Dashboard）→“API密钥”（API Keys）处获取您的API密钥。

**基础URL：** `https://aurex.cash/api/dashboard`  
**认证方式：** `Authorization: Bearer $AUREX_API_KEY`  
**请求速率限制：** 每分钟60次请求

## 安全性

- 仅将 `AUREX_API_KEY` 存储在环境变量中，切勿将其硬编码或记录在日志中。  
- 卡片详细信息（卡号、CVV码、有效期、OTP码）属于敏感数据，切勿以明文形式记录或存储。  
- 仅在用户任务确实需要时才请求卡片详细信息。  
- 将CVV码和OTP码视为一次性使用的密钥，使用后立即丢弃。

## 用户

### 创建用户  
```http
POST /users
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "name": "John Doe", "email": "john@example.com" }
```

### 获取用户信息  
```http
GET /users/:userId
Authorization: Bearer $AUREX_API_KEY
```

### 获取用于存款的钱包地址  
```http
GET /users/:userId/wallet
Authorization: Bearer $AUREX_API_KEY
```  
返回一个用于存款的地址。您可以向该地址发送SOL、USDT或USDC来为钱包充值。

## 卡片

### 发行卡片  
```http
POST /cards
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "userId": "user_123", "name": "Shopping Card", "amount": 50 }
```

### 获取卡片详细信息  
```http
GET /cards/:cardId
Authorization: Bearer $AUREX_API_KEY
```  
返回卡号、CVV码、有效期和OTP码。请谨慎处理这些信息，切勿记录它们。  

### 为卡片充值  
```http
POST /cards/:cardId/topup
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "amount": 25 }
```

### 列出所有卡片  
```http
GET /cards?userId=user_123
Authorization: Bearer $AUREX_API_KEY
```

### 查看交易记录  
```http
GET /cards/:cardId/transactions
Authorization: Bearer $AUREX_API_KEY
```

## 佣金

### 设置合作伙伴佣金率  
```http
POST /partner/markup
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "markup": 5 }
```

### 获取佣金收益  
```http
GET /partner/commission
Authorization: Bearer $AUREX_API_KEY
```

## 常见工作流程

### 发行卡片的完整流程  
1. 创建用户：`POST /users`  
2. 获取存款地址：`GET /users/:id/wallet`  
3. 用户向该地址发送加密货币  
4. 发行卡片：`POST /cards`  
5. 安全地将卡片详细信息返回给用户  

### 为现有卡片充值  
1. 查看钱包余额：`GET /users/:id/wallet`  
2. 充值：`POST /cards/:id/topup`  
3. 确认余额：`GET /cards/:id`  

## 错误代码  

| 状态 | 含义 |  
|--------|---------|  
| 401 | API密钥无效或缺失 |  
| 404 | 未找到用户或卡片 |  
| 422 | 钱包余额不足 |  
| 429 | 超过请求速率限制 |  

## TypeScript SDK  
```bash
npm install @aurexcash/agent
```  
```typescript
import { createAurexTools } from '@aurexcash/agent'

const tools = createAurexTools({ apiKey: process.env.AUREX_API_KEY })
// Works with Claude, OpenAI, Vercel AI SDK
```  

## 资源  

- 官网：[aurex.cash](https://aurex.cash)  
- 文档：[docs.aurex.cash](https://docs.aurex.cash)  
- 技术支持：[support@aurex.cash](mailto:support@aurex.cash)