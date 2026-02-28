---
name: crinkl
version: 1.0.0
description: 将电子邮件收据提交给 Crinkl，验证 DKIM 签名，并通过 Lightning Network 赚取 BTC。
homepage: https://crinkl.xyz
metadata: {"openclaw":{"emoji":"🧾","requires":{"env":["CRINKL_API_KEY"]},"primaryEnv":"CRINKL_API_KEY"}}
---
# Crinkl — 电子邮件收据提交服务

将您的员工收到的、经过 DKIM 签名的账单邮件提交给 Crinkl，从而通过 Lightning Network 赚取比特币。每条经过验证的收据都会生成一个无身份信息的消费令牌（spend token），并将相应的比特币（sats）发送到员工的钱包中。

## 功能概述

您的员工可能收到来自 SaaS 供应商（如 Cursor、Vercel、OpenAI、Anthropic、Stripe 等）的账单邮件，这些邮件都带有供应商邮件服务器生成的 DKIM 签名——这是一种证明邮件真实性和未被篡改的加密机制。通过使用此功能，您可以将这些邮件提交给 Crinkl 的验证 API。服务器会验证 DKIM 签名，提取发票信息，并生成相应的消费令牌。按照当前的比特币价格计算，每条经过验证的收据可为钱包赚取约 147 个比特币单位（sats）。

## 设置步骤

### 1. 员工获取 Crinkl API 密钥

在 [app.crinkl.xyz](https://app.crinkl.xyz) 注册账户（这是一个 PWA 应用，支持所有浏览器）。注册完成后，进入“设置” → “代理 API 密钥” → “生成”选项，即可获得一个与员工钱包关联的 API 密钥（格式为 `crk_...`）。将该密钥设置为环境变量 `CRINKL_API_KEY`。

### 2. （可选）运行自动扫描工具

如果员工需要一个能够自动扫描 Gmail 中邮件的独立 CLI 工具，可以参考以下代码示例：  
```bash
npx crinkl-agent
```

或者克隆该项目：[github.com/crinkl-protocol/crinkl-agent](https://github.com/crinkl-protocol/crinkl-agent)

## API 参考

基础 URL：`https://api.crinkl.xyz`

### 检查支持的供应商列表（无需身份验证）

```
GET /api/agent/allowed-vendors
```

该接口会返回所有被支持的供应商域名列表。所有供应商都必须发送经过 DKIM 签名的账单邮件。

### 提交电子邮件收据

```
POST /api/agent/submit-email-receipt
Header: x-api-key: <CRINKL_API_KEY>
Body: { "eml": "<base64-encoded .eml file>" }
```

**响应代码说明：**
- `201`：消费令牌已生成，比特币已排队等待发送。
- `202`：供应商尚未通过审核，提交内容正在排队等待审核（未被拒绝，如通过审核将会被处理）。
- `409`：邮件重复提交。
- `422`：验证失败（DKIM 签名无效、无法提取数据或邮件过于陈旧）。
- `429`：达到每日提交上限。

### 预览邮件内容（不进行实际提交）

```
POST /api/agent/verify-email-receipt
Header: x-api-key: <CRINKL_API_KEY>
Body: { "eml": "<base64-encoded .eml file>" }
```

该接口会返回包含提取信息的 200 状态码响应，但不会生成消费令牌。

### 获取消费令牌

```
GET /api/agent/spends/:spendId/token/latest
Header: x-api-key: <CRINKL_API_KEY>
```

该接口用于获取已签名的消费令牌。

## 提交流程

1. 员工提供原始的 `.eml` 邮件文件（可通过电子邮件客户端导出，或使用授权的 Gmail/IMAP 工具获取）。请注意：切勿自动访问员工的邮箱账户，必须由员工本人提供或授权访问权限。
2. 将 `.eml` 文件内容进行 Base64 编码。
3. 使用 API 密钥通过 `/api/agent/submit-email-receipt` 路由请求进行提交。
4. 根据返回的响应代码处理相应的操作。

所有验证和数据提取工作均由服务器完成。您只需作为数据传输的中间环节即可，无需提供邮箱账户凭据，只需提供 `.eml` 文件和 `CRINKL_API_KEY`。

## 不支持的供应商

如果您提交的邮件来自未在支持列表中的供应商，系统会将其**排队等待审核**（返回状态码 202），但不会直接拒绝。如果该供应商的域名具有有效的 DKIM 签名，系统会后续批准该邮件并生成相应的消费令牌。

**如何添加新的供应商？**  
只需提交该供应商发送的一封账单邮件即可。

## 赚取比特币的规则

以下类型的账单邮件均可赚取比特币：
- 来自支持供应商的 SaaS 订阅服务（如 Cursor、Vercel、OpenAI、Anthropic、GitHub 等）的邮件。
- 通过 Stripe、Paddle、Gumroad 等平台生成的账单邮件。
- 任何发送经过 DKIM 签名收据的供应商的邮件。

实体收据需要通过 [PWA 应用中的摄像头功能](https://app.crinkl.xyz) 进行提交，而非通过此 API。

## 隐私政策

- 只有原始的 `.eml` 邮件文件会被传输到服务器，不会共享任何邮箱账户信息。
- 消费令牌不包含任何个人身份信息（如电子邮件地址、姓名或账户 ID）。
- API 密钥仅用于将收据与员工钱包关联，而非与具体个人关联。