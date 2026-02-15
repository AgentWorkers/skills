---
name: openclaw-commerce-shopify
description: 通过 OpenClaw Commerce API 管理 Shopify 商店
metadata: {"openclaw": {"requires": {"env": ["OPENCLAW_COMMERCE_API_KEY"]}, "primaryEnv": "OPENCLAW_COMMERCE_API_KEY"}}
---
# OpenClaw Commerce 与 Shopify 的集成

通过 OpenClaw Commerce API 使用直接的 HTTP 请求来管理您的 Shopify 商店。

## 先决条件

**重要提示**：在使用此功能之前，您需要在您的 Shopify 商店中安装 OpenClaw Commerce 应用程序。该应用程序充当 OpenClaw 与您的 Shopify 商店之间的桥梁，实现安全的 API 访问和操作执行。

**安装要求**：请访问 [openclawcommerce.com](https://openclawcommerce.com) 以在您的 Shopify 商店中安装 OpenClaw Commerce 应用程序。该应用程序提供了此功能所需的 API 端点及身份验证机制。

如果未安装 OpenClaw Commerce 应用程序，此功能将无法正常使用，因为需要该应用程序的 API 基础设施来与您的 Shopify 商店进行通信。

## 设置

将您的 API 密钥设置到 `~/.openclaw/openclaw.json` 文件中：

```json5
{
  "skills": {
    "entries": {
      "openclaw-commerce-shopify": {
        "enabled": true,
        "env": {
          "OPENCLAW_COMMERCE_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## 基本 API URL

`https://shopify.openclawcommerce.com/api/v1`

**注意**：在以下示例中，`$API_BASE` 表示上述 URL。

## 可用的操作

### 1. 测试连接
- **目的**：验证 API 连接性和身份验证
- **端点**：`/test`
- **方法**：GET

#### 测试连接
```bash
curl "$API_BASE/test" \
  -H "X-OpenClaw-Commerce-Token: $OPENCLAW_COMMERCE_API_KEY"
```

### 2. 统一操作
- **目的**：通过单一端点执行所有 Shopify 操作
- **端点**：`/operation`
- **方法**：POST

#### 商店信息
- **$QUERY**：参考文档：queries/shop.md

#### 订单操作
- **$QUERY**：参考文档：queries/getOrders.md

#### 创建订单
- **$QUERY**：参考文档：queries/createOrder.md

#### 更新订单
- **$QUERY**：参考文档：queries/updateOrder.md

#### 删除订单
- **$QUERY**：参考文档：queries/deleteOrder.md

#### 客户操作
- **$QUERY**：参考文档：queries/getCustomers.md

#### 创建客户
- **$QUERY**：参考文档：queries/createCustomer.md

#### 更新客户
- **$QUERY**：参考文档：queries/updateCustomer.md

#### 删除客户
- **$QUERY**：参考文档：queries/deleteCustomer.md

#### 产品操作
- **$QUERY**：参考文档：queries/getProducts.md

#### 创建产品
- **$QUERY**：参考文档：queries/createProduct.md

#### 更新产品
- **$QUERY**：参考文档：queries/updateProduct.md

#### 删除产品
- **$QUERY**：参考文档：queries/deleteProduct.md

#### 集合操作
- **$QUERY**：参考文档：queries/getCollections.md

#### 创建集合
- **$QUERY**：参考文档：queries/createCollection.md

#### 更新集合
- **$QUERY**：参考文档：queries/updateCollection.md

#### 删除集合
- **$QUERY**：参考文档：queries/deleteCollection.md

#### 目录操作
- **$QUERY**：参考文档：queries/getCatalogs.md

#### 创建目录
- **$QUERY**：参考文档：queries/createCatalog.md

#### 更新目录
- **$QUERY**：参考文档：queries/updateCatalog.md

#### 删除目录
- **$QUERY**：参考文档：queries/deleteCatalog.md

#### 优惠券操作
- **$QUERY**：参考文档：queries/getDiscounts.md

#### 代码优惠券操作
- **$QUERY**：参考文档：queries/getCodeDiscounts.md

#### 创建代码优惠券
- **$QUERY**：参考文档：queries/createCodeDiscount.md

#### 更新代码优惠券
- **$QUERY**：参考文档：queries/updateCodeDiscount.md

#### 删除代码优惠券
- **$QUERY**：参考文档：queries/deleteCodeDiscount.md

#### 自动优惠券操作
- **$QUERY**：参考文档：queries/getAutomaticDiscounts.md

#### 创建自动优惠券
- **$QUERY**：参考文档：queries/createAutomaticDiscount.md

#### 更新自动优惠券
- **$QUERY**：参考文档：queries/updateAutomaticDiscount.md

#### 删除自动优惠券
- **$QUERY**：参考文档：queries/deleteAutomaticDiscount.md

```bash
curl -X POST $API_BASE/operation \
  -H 'Content-Type: application/json' \
  -H 'X-OpenClaw-Commerce-Token: {$OPENCLAW_COMMERCE_API_KEY}' \
  -d '{"query": "$QUERY"}'
```

## 响应指南

OpenClaw 服务于 Shopify 商店的所有者，而非技术开发者。在与用户沟通时，请遵循以下原则：

- **使用简单的语言**：用商业术语解释问题，避免使用技术术语。
- **明确问题**：清楚地说明问题所在以及这对他们的业务意味着什么。
- **提供可行的解决方案**：告诉他们下一步需要做什么。
- **避免技术细节**：不要提及 API 错误、数据库问题或系统内部机制。
- **关注业务影响**：解释问题如何影响他们的店铺运营。

**示例沟通方式**：
- ❌ “数据库连接失败：Prisma 客户端未定义”
- ✅ “我目前无法连接到您的店铺数据，请稍后再试。”

**错误响应格式**：
始终提供清晰、易于理解的错误信息，帮助商家了解问题发生的原因及应对措施。

### 错误响应
```json
{
  "error": "Error message here"
}
```

## 错误代码

- `400` - 字段配置无效或缺少参数
- `401` - API 密钥无效或缺失
- `500` - 服务器错误或 GraphQL 执行失败

## 提示

1. **对于复杂的查询，请使用 POST 方法**——比 URL 编码更简单。
2. **仅请求所需的字段**——可以提高性能。
3. **检查生成的查询**——查询结果会包含在响应中，便于调试。
4. **使用分页**：初次请求时使用较小的 `first` 值。
5. **始终添加 `X-OpenClaw-Commerce-Token` 标头**以进行身份验证。