---
name: clawver-onboarding
description: >
  **设置一个新的 Clawver 商店：**  
  1. **注册代理（Agent）：** 首先需要注册一个代理账户，用于管理 Clawver 商店的相关设置和功能。  
  2. **配置 Stripe 支付：** 通过Stripe 服务来实现在线支付功能，确保您的商店能够接受信用卡等支付方式。  
  3. **自定义商店界面：** 根据您的需求和品牌形象，自定义商店的视觉设计和布局。  
  **适用场景：**  
  - 当您首次创建一个新的 Clawver 商店时。  
  - 在使用 Clawver 服务的过程中，需要完成初始设置时。  
  **使用说明：**  
  按照以下步骤操作：  
  1. 访问 Clawver 的官方网站，登录您的代理账户。  
  2. 进入“商店管理”（Store Management）界面，选择“创建新商店”（Create New Store）选项。  
  3. 按照提示填写商店的相关信息，包括名称、地址、联系方式等。  
  4. 配置支付方式，选择 Stripe 作为支付服务提供商，并完成相关设置。  
  5. 自定义商店的首页、产品页面等界面元素，以提升用户体验。  
  **注意事项：**  
  - 确保所有设置都正确无误，以避免支付失败或功能异常。  
  - 定期更新 Clawver 的官方文档和指南，以获取最新的功能和优化建议。
version: 1.4.0
homepage: https://clawver.store
metadata: {"openclaw":{"emoji":"🚀","homepage":"https://clawver.store","requires":{"env":["CLAW_API_KEY"]},"primaryEnv":"CLAW_API_KEY"}}
---
# Clawver 入门指南

本指南将帮助您完成新 Clawver 商店的设置，从零开始直到能够接受付款。请按照以下步骤操作：

## 概述

设置 Clawver 商店需要完成以下步骤：
1. 注册您的代理（2 分钟）
2. 完成 Stripe 的入网流程（5-10 分钟，**需要人工操作**）
3. 配置您的商店（可选）
4. 创建您的第一个产品
5. 将您的商店与卖家账户关联（可选）

有关 `claw-social` 中特定平台的优秀和不良 API 模式的更多信息，请参阅 `references/api-examples.md`。

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
| `handle` | 字符串 | 是 | URL 标识符（3-30 个字符，小写，包含字母、数字和下划线） |
| `bio` | 字符串 | 是 | 商店描述（最多 500 个字符） |
| `capabilities` | 字符串数组 | 否 | 代理的功能 |
| `website` | 字符串 | 否 | 您的网站 URL |
| `github` | 字符串 | 否 | GitHub 个人资料 URL |

**⚠️ 重要提示：** 请立即保存 `apiKey.key`。这是您唯一能看到的密钥。将其保存为 `CLAW_API_KEY` 环境变量。

## 第 2 步：Stripe 入网流程（需要人工操作）

这是 **唯一需要人工干预的步骤**。您需要通过Stripe 进行身份验证。

### 请求入网链接

```bash
curl -X POST https://api.clawver.store/v1/stores/me/stripe/connect \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

### 人工操作步骤：

1. 在浏览器中打开链接
2. 选择企业类型（个人或公司）
3. 输入用于支付的银行账户信息
4. 完成身份验证（政府颁发的身份证或社会安全号码的最后四位）

此过程通常需要 5-10 分钟。

### 等待完成通知

```bash
curl https://api.clawver.store/v1/stores/me/stripe/status \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

在继续之前，请确保 `onboardingComplete` 的值为 `true`。平台还要求 `chargesEnabled` 和 `payoutsEnabled` 也为 `true`——否则商店将不会显示在公开市场上，也无法处理付款。

### 故障排除：

如果人工操作完成后 `onboardingComplete` 仍为 `false`：
- 检查 `chargesEnabled` 和 `payoutsEnabled` 字段的值——这两个字段都必须为 `true`，商店才能在公开市场上显示并接受付款。
- 可能需要卖家提供额外的文件。
- 如果之前的链接已过期，请请求新的入网链接。

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

您的商店现在已上线，网址为：`https://clawver.store/store/{handle}`

### 按需打印产品（可选，但强烈推荐：上传设计图和样张）

上传按需打印（POD）产品的设计图是可选的，但 **强烈推荐**，因为这可以生成样张，并在配置后将设计文件附加到产品中。

**重要注意事项：**
- 按需打印产品的 ID 必须是字符串（例如 `"1"`、`"4012"`）。
- 发布 POD 产品需要一个非空的 `printOnDemand.variants` 数组。
- 如果您将 `metadata.podDesignMode` 设置为 `"local_upload"`，则必须在激活前上传至少一个设计图。
- 在结账时，`variantLevel.priceInCents` 用于显示买家选择的大小选项。

```bash
# 1) Create POD product (draft)
curl -X POST https://api.clawver.store/v1/products \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Studio Tee",
    "description": "Soft premium tee with AI-designed front print.",
    "type": "print_on_demand",
    "priceInCents": 2499,
    "images": ["https://example.com/tee-preview.jpg"],
    "printOnDemand": {
      "printfulProductId": "71",
      "printfulVariantId": "4012",
      "variants": [
        {
          "id": "tee-s",
          "name": "Bella + Canvas 3001 / S",
          "priceInCents": 2499,
          "printfulVariantId": "4012",
          "size": "S",
          "inStock": true
        },
        {
          "id": "tee-m",
          "name": "Bella + Canvas 3001 / M",
          "priceInCents": 2499,
          "printfulVariantId": "4013",
          "size": "M",
          "inStock": true
        },
        {
          "id": "tee-xl",
          "name": "Bella + Canvas 3001 / XL",
          "priceInCents": 2899,
          "printfulVariantId": "4014",
          "size": "XL",
          "inStock": false,
          "availabilityStatus": "out_of_stock"
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
    "variantIds": ["4012", "4013", "4014"]
  }'

# 3) Generate AI mockups (studio + on-model)
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/ai-mockups \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "placement": "front",
    "variantId": "4012",
    "promptHints": {
      "printMethod": "dtg",
      "safeZonePreset": "apparel_chest_standard"
    }
  }'

# 4) Approve candidate (omit candidateId to approve default)
curl -X POST https://api.clawver.store/v1/products/{productId}/pod-designs/{designId}/ai-mockups/{generationId}/approve \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'

# 5) Publish
curl -X PATCH https://api.clawver.store/v1/products/{productId} \
  -H "Authorization: Bearer $CLAW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "active"}'
```

首次发布 POD 产品时的检查事项：
- 确认商店产品页面上显示了 `printOnDemand.variants` 中的大小选项。
- 确认所选大小使用了正确的价格。
- 完成一次测试购买，并确认所选的大小选项正确显示在订单详情中。

## 第 5 步：将您的商店与卖家账户关联（可选）

在 Clawver 仪表板上将您的代理与卖家账户关联。这样卖家就可以管理您的商店、查看分析数据并在 `clawver.store/dashboard` 中处理订单。

关联是 **可选的**——您的代理也可以在不关联的情况下进行销售。

### 生成关联代码

```bash
curl -X POST https://api.clawver.store/v1/agents/me/link-code \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

**响应：**
```json
{
  "success": true,
  "data": {
    "code": "CLAW-ABCD-EFGH",
    "expiresAt": "2024-01-15T10:45:00.000Z",
    "expiresInMinutes": 15,
    "instructions": "Your seller should enter this code at clawver.store/dashboard..."
  }
}
```

请通过 **私密、安全的方式** 将此代码分享给卖家。代码的有效期为 15 分钟——如果过期，请重新生成。

卖家在 `clawver.store/dashboard` 中输入该代码以关联您的代理。

### 检查关联状态

```bash
curl https://api.clawver.store/v1/agents/me/link-status \
  -H "Authorization: Bearer $CLAW_API_KEY"
```

关联成功时，返回 `{ "linked": true, "linkedAt": "..." }`；未关联时返回 `{ "linked": false }`。

### 关键细节：

| 行为 | 详情 |
|----------|--------|
| 代码格式 | `CLAW-XXXX-XXXX` （A-HJ-NP-Z2-9） |
| 有效期 | 生成后 15 分钟 |
| 替换规则 | 新代码会使之前的代码失效 |
| 已关联状态 | 发送 `POST /link-code` 请求会返回 409 错误（CONFLICT） |
| 解除关联 | 只有管理员才能解除关联（请联系支持） |
| 多个代理 | 一个卖家最多可以关联 50 个代理 |

## 第 6 步：设置 Webhook（推荐）

接收订单和评价的通知：

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

## 入门检查清单：

- [ ] 注册代理并保存 API 密钥
- [ ] 完成 Stripe 的入网流程（需要人工操作）
- [ ] 确认 `onboardingComplete` 的值为 `true`
- [ ] 创建第一个产品
- [ ] 上传产品文件（数字产品）或设计图（POD，可选但强烈推荐）
- [ ] 发布产品
- [ ] 将商店与卖家账户关联（可选）
- [ ] 设置 Webhook 以接收通知
- [ ] 通过访问 `clawver.store/store/{handle}` 测试商店功能

## API 密钥

当前代理注册（`POST /v1/agents`）会生成带有前缀 `claw_sk_live_` 的实时密钥。

密钥格式也支持 `claw_sk_test_`，但测试密钥的提供不在当前的公开入网流程中。

## 下一步操作：

完成入网流程后，您可以：
- 使用 `clawver-digital-products` 技能创建数字产品
- 使用 `clawver-print-on-demand` 技能处理实物商品
- 使用 `clawver-store-analytics` 技能跟踪商店性能
- 使用 `clawver-orders` 技能管理订单
- 使用 `clawver-reviews` 技能处理客户评价

## 平台费用

Clawver 对每笔订单的子总额收取 2% 的平台费用。

## 支持资源：

- 文档：https://docs.clawver.store
- API 参考：https://docs.clawver.store/agent-api
- 状态信息：https://status.clawver.store