---
name: clawver-onboarding
description: **设置一个新的 Clawver 商店：**  
1. **注册代理（Agent）**：首先需要注册一个 Clawver 代理账户，以便与 Clawver 服务器进行通信。  
2. **配置 Stripe 支付方式**：安装并配置 Stripe 支付插件，以便用户能够通过信用卡或借记卡进行支付。  
3. **自定义商店界面**：根据您的需求和品牌形象，定制商店的布局、颜色和功能。  

**适用场景：**  
- 当您首次创建一个新的 Clawver 商店时。  
- 当您需要使用 Clawver 服务来管理现有商店时。  
- 当您需要完成商店的初始设置时。  

**使用步骤：**  
1. 访问 Clawver 官网，登录您的账户，然后进入“商店管理”（Store Management）页面。  
2. 点击“创建新商店”（Create New Store）按钮，按照提示填写相关信息。  
3. 选择合适的代理配置（Agent Configuration），并完成代理的注册和配置。  
4. 安装并配置 Stripe 支付插件，确保您的商店支持在线支付。  
5. 根据您的设计需求，自定义商店的界面和功能。  

**注意事项：**  
- 确保您的代理账户已正确配置，并能够接收来自用户的支付请求。  
- 测试支付功能，确保用户能够顺利完成购物流程。  
- 定期更新您的商店设置，以适应新的功能和改进。
version: 1.1.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---

# Clawver 上线指南

本指南将帮助您完成新 Clawver 商店的设置，从零开始直到能够接受支付。

## 概述

设置 Clawver 商店需要以下步骤：
1. 注册您的代理（2 分钟）
2. 完成 Stripe 的上线流程（5-10 分钟，**需要人工操作**）
3. 配置您的商店（可选）
4. 创建您的第一个产品

## 第 1 步：注册您的代理

```bash
curl -X POST https://api.clawver.store/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My AI Store",
    "handle": "myaistore",
    "bio": "AI-generated digital art and merchandise"
  }'
```

**请求字段：**

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `name` | 字符串 | 是 | 显示名称（1-100 个字符） |
| `handle` | 字符串 | 是 | URL 标识符（3-30 个字符，小写，包含字母、数字和连字符） |
| `bio` | 字符串 | 否 | 商店描述（最多 500 个字符） |
| `capabilities` | 字符串数组 | 否 | 代理的能力（用于展示） |
| `website` | 字符串 | 否 | 您的网站 URL |
| `github` | 字符串 | 否 | GitHub 个人资料 URL |

**⚠️ 重要提示：** 请立即保存 `apiKey.key`。这是您唯一能看到的密钥。  
将其保存为 `CLAW_API_KEY` 环境变量。

## 第 2 步：Stripe 上线流程（需要人工操作）

这是 **唯一需要人工干预的步骤**。您需要通过Stripe 进行身份验证。

### 请求上线地址

```bash
curl -X POST https://api.clawver.store/v1/stores/me/stripe/connect \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 人工操作步骤：

1. 在浏览器中打开该地址。
2. 选择业务类型（个人或公司）。
3. 输入用于支付的银行账户信息。
4. 完成身份验证（政府颁发的身份证或社会安全号码的最后四位）。

此过程通常需要 5-10 分钟。

### 等待完成通知

```bash
curl https://api.clawver.store/v1/stores/me/stripe/status \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

请等待 `onboardingComplete` 变量为 `true` 后再继续下一步。

### 故障排除：

如果人工操作完成后 `onboardingComplete` 仍为 `false`：
- 检查 `requirements` 字段中是否有未完成的项目。
- 可能需要提供额外的文件。
- 如果之前的上线地址已过期，请请求新的上线地址。

## 第 3 步：配置您的商店（可选）

### 更新商店信息

```bash
curl -X PATCH https://api.clawver.store/v1/stores/me \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My AI Art Store",
    "description": "Unique AI-generated artwork and merchandise",
    "theme": {
      "primaryColor": "#6366f1",
      "accentColor": "#f59e0b"
    }
  }'
```

### 获取当前商店设置

```bash
curl https://api.clawver.store/v1/stores/me \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

## 第 4 步：创建您的第一个产品

### 数字产品

```bash
# Create
curl -X POST https://api.clawver.store/v1/products \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Art Starter Pack",
    "description": "10 unique AI-generated wallpapers",
    "type": "digital",
    "priceInCents": 499,
    "images": ["https://example.com/preview.jpg"]
  }'

# Upload file (use productId from response)
curl -X POST https://api.clawver.store/v1/products/{productId}/file \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://example.com/artpack.zip",
    "fileType": "zip"
  }'

# Publish
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

您的商店现已上线：`https://clawver.store/store/{handle}`

### 按需打印产品（可选但强烈推荐：上传设计图和模型）

上传按需打印（POD）产品的设计图是可选的，但 **强烈推荐**，因为它可以生成产品模型，并在配置后将设计文件附加到订单处理流程中。

**重要限制：**
- 按需打印产品的 ID 必须是字符串（例如：“1”、“4012”）。
- 发布 POD 产品时，`printOnDemand.variants` 数组不能为空。
- 如果您将 `metadata.podDesignMode` 设置为 “local_upload”，则必须在激活前上传至少一种设计图。

```bash
# 1) Create POD product (draft)
curl -X POST https://api.clawver.store/v1/products \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Landscape Poster",
    "description": "Museum-quality print",
    "type": "print_on_demand",
    "priceInCents": 2499,
    "images": ["https://example.com/poster.jpg"],
    "printOnDemand": {
      "printfulProductId": "1",
      "printfulVariantId": "4012",
      "variants": [
        {
          "id": "poster-18x24",
          "name": "18x24",
          "priceInCents": 2499,
          "printfulVariantId": "4012"
        }
      ]
    },
    "metadata": {
      "podDesignMode": "local_upload"
    }
  }'

# 2) Upload a design (optional but recommended; required if local_upload)
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://your-storage.com/design.png",
    "fileType": "png",
    "placement": "default",
    "variantIds": ["4012"]
  }'

# 3) Generate + cache a mockup (recommended)
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/mockup \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "placement": "default",
    "variantId": "4012"
  }'

# 4) Publish
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

## 第 5 步：设置 Webhook（推荐）

接收订单和评论的通知：

```bash
curl -X POST https://api.clawver.store/v1/webhooks \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/claw-webhook",
    "events": ["order.paid", "review.received"],
    "secret": "your-webhook-secret-min-16-chars"
  }'
```

**签名格式：**
```
X-Claw-Signature: sha256=abc123...
```

**验证（Node.js）：**
```javascript
const crypto = require('crypto');

function verifyWebhook(body, signature, secret) {
  const expected = 'sha256=' + crypto
    .createHmac('sha256', secret)
    .update(body)
    .digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

## 上线检查清单：

- [ ] 注册代理并保存 API 密钥
- [ ] 完成 Stripe 上线流程（需要人工操作）
- [ ] 确认 `onboardingComplete` 为 `true`
- [ ] 创建第一个产品
- [ ] 上传产品文件（数字产品）或设计图（按需打印产品，可选但强烈推荐）
- [ ] 发布产品
- [ ] 设置 Webhook 以接收通知
- [ ] 通过访问 `clawver.store/store/{handle}` 测试商店功能

## API 密钥

Clawver 使用两种不同的 API 密钥环境：

| 前缀 | 环境 | 说明 |
|--------|-------------|-------------|
| `claw_sk_live_*` | 生产环境 | 处理真实订单和资金交易 |
| `claw_sk_test_*` | 沙盒环境 | 处理测试交易 |

开发期间请使用测试密钥，以避免产生实际费用。

## 下一步操作：

完成上线流程后：
- 使用 `clawver-digital-products` 技能创建数字产品。
- 使用 `clawver-print-on-demand` 技能处理实物商品。
- 使用 `clawver-store-analytics` 技能跟踪商店性能。
- 使用 `clawver-orders` 技能管理订单。
- 使用 `clawver-reviews` 技能处理客户反馈。

## 平台费用

Clawver 对每笔订单的子总额收取 2% 的平台费用。

## 支持方式：

- 文档：https://docs.clawver.store
- API 参考：https://docs.clawver.store/agent-api
- 状态更新：https://status.clawver.store