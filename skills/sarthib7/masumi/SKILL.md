---
name: masumi-payments
description: 通过部署自己的支付服务，使AI代理能够通过去中心化的Masumi网络接受Cardano区块链的支付。
homepage: https://docs.masumi.network
user-invocable: true
metadata: {"openclaw": {"requires": {"bins": ["node", "npm", "git"], "env": ["MASUMI_PAYMENT_SERVICE_URL"]}, "primaryEnv": "MASUMI_PAYMENT_SERVICE_URL", "emoji": "💰"}}
---

# OpenClaw 的 Masumi Payments 功能

**让您的 AI 代理能够接受区块链支付，并加入去中心化的代理经济**

## 重要提示：AI 代理能做什么与不能做什么**

**AI 代理可以：**
- 使用 `masumi_install_payment_service` 在本地安装 masumi-payment-service
- 使用 `masumi_start_payment_service` 启动支付服务
- 使用 `masumi_generate_api_key` 生成管理员 API 密钥
- 自动生成 Cardano 钱包
- 配置环境变量（.env 文件）
- 在区块链上注册代理
- 向支付服务发起 API 请求
- 测试支付流程

**AI 代理不能做的（需要人工操作）：**
- 部署到 Railway 平台（需要通过浏览器进行 OAuth 登录）
- 注册 Blockfrost 账户（需访问 https://blockfrost.io）
- 从 faucet 请求测试 ADA（需访问 https://docs.cardano.org/cardano-testnet/tools/faucet/）
- 备份钱包助记词（需由人工安全保存）

**AI 代理在开始前请询问两个问题：**
1. **“您已经安装了 masumi-payment-service 吗？如果安装了，请提供您的服务地址。”**
   - 用户应提供：`http://localhost:3000/api/v1`（本地）或 `https://their-service.railway.app/api/v1`（Railway）
   - **重要提示**：不存在中央化的 `payment.masumi.network` 服务——每个代理都运行自己的支付服务
2. **“如果您还没有安装，是否需要我帮助您在本地安装？”**

---

## 什么是 Masumi？

Masumi 是一个用于 AI 代理支付的去中心化协议，它使代理能够高效地在 Cardano 区块链上协作并实现服务变现。

**重要提示：Masumi 并非中央化服务。**
- **您需要自己运行支付服务节点**（可以在本地或 Railway 平台上运行）
- **您需要自己管理钱包**（完全由您控制）
- **您是自己的管理员**（没有中央权威机构）
- 不存在 `payment.masumi.network` 这样的服务——这些只是文档中的示例而已

## 架构

**重要提示：您需要自己运行 Masumi 节点。不存在中央化的服务。**

Masumi 节点包含两个主要服务，这些服务均由您自己部署和运行：

1. **支付服务**（必需） - 由您自己运行：
   - 在本地运行（`http://localhost:3000`）或在 Railway 平台上运行（`https://your-service.railway.app`）
   - 钱包管理
   - 交易处理（A2A 和 H2A）
   - 代币兑换（稳定币 ↔ ADA）
   - 管理界面 + REST API（使用您的管理员 API 密钥）

2. **注册服务**（可选） - 用于查询区块链信息：
   - 通常与支付服务一起运行
   - 代理发现
   - 节点查找
   - 仅支持读取操作，不支持交易

## 快速入门

### 选项 1：自动安装支付服务

使用内置的安装工具：

```typescript
// Step 1: Install payment service
const installResult = await masumi_install_payment_service({
  network: 'Preprod'
});

// Step 2: Start service
await masumi_start_payment_service({
  installPath: installResult.installPath,
  serviceUrl: installResult.serviceUrl
});

// Step 3: Generate API key
const apiKeyResult = await masumi_generate_api_key({
  serviceUrl: installResult.serviceUrl
});

// Step 4: Enable Masumi (auto-provisions wallet and registers agent)
await masumi_enable({
  installService: true, // Automatically installs if not configured
  agentName: 'My Agent',
  pricingTier: 'free'
});
```

### 选项 2：手动设置

1. **部署您的支付服务：**
   - 本地：克隆 https://github.com/masumi-network/masumi-payment-service 并在本地运行
   - 在 Railway 平台上部署：通过 Railway 控制台完成

2. **设置环境变量：**
   ```bash
   export MASUMI_PAYMENT_SERVICE_URL=http://localhost:3000/api/v1
   export MASUMI_PAYMENT_API_KEY=your-admin-api-key
   export MASUMI_NETWORK=Preprod
   ```

3. **启用 Masumi：**
   ```typescript
   await masumi_enable({
     agentName: 'My Agent',
     pricingTier: 'free'
   });
   ```

## 工具

### 安装工具

- **`masumi_install_payment_service`：** 在本地克隆并安装 masumi-payment-service
- **`masumi_start_payment_service`：** 启动支付服务并检查状态
- **`masumi_generate_api_key`：** 通过支付服务 API 生成管理员 API 密钥

### 支付工具

- **`masumi_enable`：** 完整设置：安装服务、生成 API 密钥、注册代理
- **`masumi_create_payment`：** 创建支付请求
- **`masumi_check_payment`：** 检查支付状态
- **`masumi_complete_payment`：** 提交结果并完成支付
- **`masumi_wallet_balance`：** 查看钱包余额
- **`masumi_list_payments`：** 查看支付历史记录

### 注册工具

- **`masumi_register_agent`：** 在 Masumi 注册表中注册代理
- **`masumi_search_agents`：** 查找其他代理
- **`masumi_get_agent`：** 获取代理详情

## API 参考（快速参考）

### 支付接口

| 方法 | 接口地址 | 功能 | 备注 |
|--------|----------|---------|-------|
| POST | `/payment` | 创建支付请求 | 返回 `blockchainIdentifier` |
| POST | `/payment/resolve-blockchain-identifier` | 检查支付状态 | 使用 `blockchainIdentifier` 作为请求参数 |
| POST | `/payment/submit-result` | 提交结果 | 使用 `submitResultHash`（而非 `resultHash`） |
| GET | `/payment` | 查看支付记录 | 返回 `data.Payments` 数组 |
| POST | `/payment/authorize-refund` | 授权退款 | 仅限管理员使用 |

### 注册表接口

| 方法 | 接口地址 | 功能 | 备注 |
|--------|----------|---------|-------|
| POST | `/registry` | 注册代理 | 返回 `data` 对象 |
| GET | `/registry/` | 查看/搜索代理 | 返回 `data.Assets` 数组 |
| GET | `/registry/` | 获取代理信息 | 可通过 `agentIdentifier` 参数进行过滤 |

**重要提示：**
- 如果服务地址包含 `/api/v1`，所有接口地址前都需要加上 `/api/v1`
- 响应格式：`{ status: string, data: T }` —— 提取 `data` 属性
- 在提交结果时，请使用 `submitResultHash` 参数（而非 `resultHash`）

## 配置参数

**必需参数：**
- `MASUMI_payment_SERVICE_URL`：您自己托管的支付服务地址

**可选参数：**
- `MASUMI_payment_API_KEY`：管理员 API 密钥
- `MASUMI_NETWORK`：环境模式（“Preprod” 或 “Mainnet”；默认为 “Preprod”）
- `MASUMI_REGISTRY_SERVICE_URL`：注册表服务地址（默认为支付服务地址）

## 示例

请参阅 `examples/payment-manager.ts` 以获取完整示例。

## 资源

- 支付服务：https://github.com/masumi-network/masumi-payment-service
- 注册表服务：https://github.com/masumi-network/masumi-registry-service
- 文档：https://docs.masumi.network
- MIP-004 规范：Masumi 改进提案 #004