---
name: consortium-ai-create-account
displayName: Consortium AI Create Account
description: 在 Consortium AI 上创建一个托管钱包账户。
requirements: TRADING_ANALYSIS_API_KEY
author: Consortium AI
authorUrl: https://consortiumai.org/
keywords: ["crypto", "wallet", "create", "account", "custodial", "API"]
category: trading
---

## 使用说明

此技能提供了在 Consortium AI 上创建账户的功能。

它会调用一个外部 API，在 Consortium AI 上创建一个托管钱包账户。

### 运行方式（实现方式）

在技能目录中，您可以通过发送 HTTP 请求（请参阅 API 参考）或运行捆绑的脚本来调用该 API：

- **创建账户：**
  `node scripts/create-account.js <WALLET_ADDRESS>`
  或 `npm run create-account -- <WALLET_ADDRESS>`
  例如：`node scripts/create-account.js 5h4...3k1`

该脚本需要设置 `TRADING_ANALYSIS_API_KEY`。如果操作成功，它会将 API 响应以 JSON 格式输出到标准输出（stdout）；如果失败，则会将错误信息以 JSON 格式输出到标准错误输出（stderr），并退出（退出状态码非零）。

---

## 设置

在使用此技能之前，请将 API 密钥设置为环境变量：

```bash
export TRADING_ANALYSIS_API_KEY=your-secret-api-key
```

如需获取 API 密钥，请联系 [Consortium AI（在 X 平台上）](https://x.com/Consortium.AI)。

---

## API 参考

**后端 API 基本地址：** `https://api.consortiumai.org`

**端点：** `POST https://api.consortiumai.org/api/custodial-wallet/create-with-api-key`
用于创建一个新的托管钱包账户。

### 认证

仅需要 API 密钥（不支持 JWT）。可以通过以下方式之一发送密钥：
- **请求头：** `x-api-key: <TRADING_ANALYSIS_API_KEY>`
- **请求头：** `Authorization: Bearer <TRADING_ANALYSIS_API_KEY>`

### 请求体

```json
{
  "walletAddress": "5h4...YourWalletAddress...3k1"
}
```

### 成功响应（状态码 201）

```json
{
  "message": "Custodial wallet created successfully",
  "data": {
    "id": "wallet_uuid",
    "wallet_address": "GeneratedCustodialWalletAddress",
    "user_id": "user_uuid",
    "created_at": "2024-03-20T10:00:00.000Z",
    "updated_at": "2024-03-20T10:00:00.000Z"
  }
}
```

### 错误响应

| 状态码 | 错误原因 | 响应内容（示例） |
|--------|------------|-------------------|
| **400** | 缺少 walletAddress | `{ "error": "Missing walletAddress" }` |
| **401** | API 密钥缺失或错误 | `{ "success": false, "message": "Invalid or missing API key" }` |
| **404** | 未找到对应的钱包地址的用户 | `{ "error": "User not found for the provided wallet address" }` |

---

## 可用的功能

### createCustodialWallet(walletAddress)

**功能：** 在 Consortium AI 上创建一个新的托管钱包账户。

**参数：**
- `walletAddress`（字符串）：用户的钱包地址。

**预期行为：**
- 向 `https://api.consortiumai.org/api/custodial-wallet/create-with-api-key` 发送 POST 请求。
- 使用 `TRADING_ANALYSIS_API_KEY` 进行身份验证。
- 返回创建的钱包详细信息。

**返回值：**
- 钱包 ID
- 生成的托管钱包地址
- 用户 ID
- 创建时间戳