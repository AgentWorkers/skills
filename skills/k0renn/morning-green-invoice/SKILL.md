---
name: morning
description: 用于与 Morning (GreenInvoice) 服务进行身份验证，以及创建/管理客户、商品信息以及会计文档（发票/收据/报价单/订单/信用记录）。
---

# Morning (GreenInvoice)

## 使用场景
当您需要与 **Morning / GreenInvoice** 工具进行交互时，请使用此技能：
- 使用 API 密钥凭据获取认证令牌（JWT）
- 创建/更新 **客户端**（clients）
- 创建/更新 **商品**（items）
- 创建 **文档**（发票、收据、报价单、订单、贷项通知单、借项通知单）
- 如果工具支持，检索文档输出信息（如文档 ID 或链接）

## 用户需要提供的信息
仅收集执行相应操作所需的信息：

### 认证
- `apiKeyId`
- `apiKeySecret`

### 客户端（创建或查询时）
- `name`
- 可选：`taxId`, `email`, `phone`, `address`, `city`, `country`

### 商品（创建时）
- `name`
- `price`
- 可选：`description`, `currency`

### 文档（创建时）
- `documentType`（发票、收据、报价单、订单、贷项通知单、借项通知单）
- `clientId`（或用于创建客户端的足够信息）
- `lines[]`（每行包含：商品描述、商品 ID、数量、单价）
- 可选：`currency`, `language`, `description`, `discount`

## 工具使用规范
使用 `morning` 工具，并指定相应的 `action` 参数。

### 支持的操作
- `getToken`
- `createClient`
- `createItem`
- `createDocument`
- （如果您的工具支持）`findClient`, `findItem`, `getDocument`, `listDocuments`

## 安全规范
- 绝不要将 `apiKeySecret` 或 JWT 信息反馈给用户。
- 在可能的情况下，优先使用现有的 `clientId`/`itemId`。
- 验证文档信息：
  - `quantity` 必须大于 0
  - `unitPrice` 必须大于等于 0
- 货币默认设置为 “ILS”，除非用户另有指定
- 语言默认设置为 “Hebrew”，除非用户另有指定

## 示例

### 1) 获取认证令牌（JWT）
```json
{
  "action": "getToken",
  "apiKeyId": "YOUR_API_KEY_ID",
  "apiKeySecret": "YOUR_API_KEY_SECRET"
}
```

### 2) 创建客户端
```json
{
  "action": "createClient",
  "jwt": "JWT_FROM_getToken",
  "client": {
    "name": "Acme Ltd",
    "taxId": "515555555",
    "email": "billing@acme.com",
    "phone": "+972-50-000-0000",
    "address": "1 Rothschild Blvd",
    "city": "Tel Aviv",
    "country": "Israel"
  }
}
```

### 3) 创建商品
```json
{
  "action": "createItem",
  "jwt": "JWT_FROM_getToken",
  "item": {
    "name": "Consulting hour",
    "description": "Senior engineering consulting",
    "price": 500,
    "currency": "ILS"
  }
}
```

### 4) 创建发票文档
```json
{
  "action": "createDocument",
  "jwt": "JWT_FROM_getToken",
  "document": {
    "documentType": "Invoice",
    "language": "English",
    "currency": "ILS",
    "clientId": "CLIENT_ID",
    "description": "Invoice for January services",
    "lines": [
      {
        "description": "Consulting hour",
        "quantity": 10,
        "unitPrice": 500
      }
    ]
  }
}
```

### 5) 使用商品 ID 创建收据文档
```json
{
  "action": "createDocument",
  "jwt": "JWT_FROM_getToken",
  "document": {
    "documentType": "Receipt",
    "language": "Hebrew",
    "currency": "ILS",
    "clientId": "CLIENT_ID",
    "lines": [
      {
        "itemId": "ITEM_ID",
        "quantity": 1,
        "unitPrice": 1200
      }
    ]
  }
}
```

## 错误处理
- 如果令牌验证失败（401/403 错误），请重新调用 `getToken` 并重试请求。
- 如果客户端或商品已存在：
  - 如果工具支持查询，优先返回现有 ID；
  - 否则，显示明确提示：“客户端已存在；请提供 clientId 或唯一标识符。”
- 如果验证失败，仅提示缺失或无效的字段（例如：“数量必须大于 0”）。

## 输出结果
返回以下信息：
- 创建的资源 ID（`clientId`, `itemId`, `documentId`）
- 如果 API 或工具提供相关内容，还包括相关 URL（PDF 文件链接或查看链接）