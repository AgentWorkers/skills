---
name: metered-api-marketplace
description: 构建并运营一个计费的公共 API 端点（即“代理微服务”），用于 OpenClaw 技能/代理的调用。该 API 支持 API 密钥认证、每次请求的使用量记录与计费功能，同时支持预付费余额管理以及通过支付处理器的 Webhook 进行加密货币（BTC/ETH）充值。当您希望将某项功能作为公共 API 进行商业化、实施速率限制/防滥用机制、建立信用记录系统，或添加收入分成/平台费用逻辑时，可以使用该服务。
---
# 计费型 API 市场平台

我们提供了一个适用于以下场景的模板：**OpenClaw 技能 → 公共 API 端点 → 使用量计量 → 加密支付网关 → BTC/ETH 钱包**。

该技能包含一个可运行的参考服务器（基于 Fastify 和 SQLite 构建）：

- **接受结构化的 JSON 输入**  
- **执行高价值的业务逻辑处理**（通过可插拔的 “transformers” 实现）  
- **返回结构化的 JSON 输出**  
- **强制使用签名 API 密钥进行身份验证**  
- **检查预付费余额**，按每次调用扣费，并记录使用情况**  
- **接收支付通知（遵循 Coinbase Commerce 或 BTCPay Server 的规范）**  
- **在账本中收取 2.5% 的平台费用**（费用地址可配置）  

## 工作流程（请按顺序执行）  

### 1) 选择可商业化的功能  
从以下功能中选择一个：  
- 具有较高收益潜力（能够持续产生收入）  
- 被频繁调用  
- 具有较高的可重复使用性（逻辑清晰、可自动化）  

推荐的默认功能包括：  
- 收入/优惠优化器  
- 广告文案优化器  
- 客户潜在价值评分系统  
- 合同风险检测工具  

如果不确定该选择哪个功能，可以先使用随附的 `revenue-amplifier` 转换器，之后再根据实际需求进行替换。  

### 2) 在本地运行参考服务器  
使用 `scripts/server/` 目录下的服务器脚本：  
- `cd scripts/server`  
- `npm install`  
- `cp .env.example .env` 并编辑配置文件  
- `npm run dev`  

在 `.env` 文件中设置固定费用：  
- `COST_CENTS_PER_CALL=25`  # 每次调用 0.25 美元  

### 3) 创建 API 密钥  
使用 `scripts/server/admin/create_key_pg.js` 脚本（或相应的管理 API）来生成 API 密钥并设置初始余额。  

### 4) 从 OpenClaw 技能或代理程序集成  
调用公共 API 端点时，需要提供以下参数：  
- `x-api-key`  
- `x-timestamp`（Unix 时间戳，单位：毫秒）  
- `x-signature` = `hex(HMAC_SHA256(api_secret, `${timestamp}.${rawBody}`)`  

### 5) 实现支付功能  
将支付处理器的 Webhook 配置到 `/v1/payments/webhook/:provider` 路由上。  

支付处理器支持多种适配器：  
- 先使用 “手动” 信用额度进行支付（通过管理脚本配置）  
- 随后可以集成 Coinbase Commerce 或 BTCPay Server。  

### 6) 部署服务  
将服务部署在支持 TLS 协议的环境中（例如 Cloudflare、Fly.io、Render、AWS 或 GCP），并在客户端和应用内部实施速率限制机制。  

## 随附资源  

### scripts/server/  
- 可运行的参考实现代码：  
  - Fastify 架构的 API 服务器（支持长时间运行）  
  - Postgres 数据库（用于存储余额、使用量和信用额度信息）  
  - 基于签名 API 密钥的身份验证机制  
  - 实施速率限制和反滥用策略  
  - Webhook 接口  

### scripts/nextjs-starter/  
- 预置好的 Next.js API 实现框架（支持 Vercel 部署）：  
  - 无服务器端的 API 路由配置  
  - 使用 Supabase Transaction Pooler 管理 Postgres 数据库  
  - 保持与前面部分相同的身份验证、计费及 Webhook 功能  

### 参考文档  
仅在需要时查阅：  
- `references/api_reference.md` – API 端点的相关文档和身份验证机制  
- `references/billing_ledger.md` – 计费逻辑和幂等性处理  
- `referencesproviders.md` – 支付处理器适配器示例（包括 Coinbase 和 BTCPay 的实现方式）