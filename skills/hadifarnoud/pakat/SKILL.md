---
name: pakat
description: 与 Pakat 电子邮件营销 API（new.pakat.net）进行交互。当用户需要通过 Pakat 平台管理邮件列表、订阅者、营销活动、模板、交易邮件、用户分组，或查看营销活动统计数据和发送日志时，可以使用该 API。该 API 会在提及 Pakat、电子邮件营销活动、邮件列表、订阅者管理或通过 Pakat 发送交易邮件的内容时被触发。
---

# Pakat 邮件营销平台

[Pakat](https://pakat.net) 是一个专为波斯语/法语用户设计的邮件营销平台，支持创建和管理邮件列表、发送营销活动邮件、交易邮件以及追踪邮件送达情况——所有这些功能都通过简洁的 REST API 实现。

**🔗 [立即注册 Pakat](https://profile.pakat.net/signup)**，开始使用吧！

## 设置

系统需要环境变量 `PAKAT_API_KEY`。如果该变量未设置，系统会要求用户提供他们的 API 密钥。

您可以从以下链接获取 API 密钥：**https://new.pakat.net/customer/api-keys/index**

```bash
export PAKAT_API_KEY="your-key-here"
```

## 发送请求

基础 URL：`https://new.pakat.net/api`

```bash
# GET requests
curl -s -H "X-API-KEY: $PAKAT_API_KEY" "https://new.pakat.net/api/{endpoint}"

# POST requests (multipart/form-data)
curl -s -X POST -H "X-API-KEY: $PAKAT_API_KEY" \
  -F "field=value" \
  "https://new.pakat.net/api/{endpoint}"

# PUT requests (x-www-form-urlencoded)
curl -s -X PUT -H "X-API-KEY: $PAKAT_API_KEY" \
  -d "field=value" \
  "https://new.pakat.net/api/{endpoint}"

# DELETE requests
curl -s -X DELETE -H "X-API-KEY: $PAKAT_API_KEY" "https://new.pakat.net/api/{endpoint}"
```

## 常见工作流程

### 列出所有邮件列表
```bash
curl -s -H "X-API-KEY: $PAKAT_API_KEY" "https://new.pakat.net/api/lists"
```

### 将订阅者添加到邮件列表中
```bash
curl -s -X POST -H "X-API-KEY: $PAKAT_API_KEY" \
  -F "EMAIL=user@example.com" \
  -F "FNAME=John" \
  -F "LNAME=Doe" \
  "https://new.pakat.net/api/lists/{list_uid}/subscribers"
```

### 创建并发送营销活动邮件
```bash
curl -s -X POST -H "X-API-KEY: $PAKAT_API_KEY" \
  -F "campaign[name]=My Campaign" \
  -F "campaign[from_name]=Sender Name" \
  -F "campaign[from_email]=sender@domain.com" \
  -F "campaign[subject]=Email Subject" \
  -F "campaign[reply_to]=reply@domain.com" \
  -F "campaign[send_at]=2025-01-15 10:00:00" \
  -F "campaign[list_uid]=LIST_UID_HERE" \
  -F "campaign[template][template_uid]=TEMPLATE_UID" \
  "https://new.pakat.net/api/campaigns"
```

### 发送交易邮件
```bash
BODY_B64=$(echo '<h1>Hello</h1><p>Your order is confirmed.</p>' | base64 -w0)
curl -s -X POST -H "X-API-KEY: $PAKAT_API_KEY" \
  -F "email[to_name]=John Doe" \
  -F "email[to_email]=john@example.com" \
  -F "email[from_name]=My App" \
  -F "email[subject]=Order Confirmation" \
  -F "email[body]=$BODY_B64" \
  -F "email[send_at]=2025-01-15 10:00:00" \
  "https://new.pakat.net/api/transactional-emails"
```

### 查看营销活动统计信息
```bash
curl -s -H "X-API-KEY: $PAKAT_API_KEY" "https://new.pakat.net/api/campaigns/{campaign_uid}/stats"
```

## 重要注意事项

- **HTML 内容必须使用 Base64 编码**（例如：`campaign[template][content]`、`email[body]`、`template[content]`）。
- **交易邮件的发送时间（`send_at`）采用 UTC 格式，格式为 `Y-m-d H:i:s`。
- **营销活动的发送时间（`send_at`）使用客户的配置时区**。
- **交易邮件模板**：将 `email[template_uid]` 设置为模板名称，而不是直接使用 `email[body]`；使用 `email[params][key]` 来替换模板中的占位符 `{{ params.key }}`。
- **订阅者状态**：未确认、已确认、被列入黑名单、已取消订阅、未批准、已禁用、状态变更。
- **分页**：在邮件列表相关接口中使用查询参数 `?page=N&per_page=N` 进行分页。
- **交易邮件的 `from_email` 必须来自经过验证的域名**。

## 完整的 API 参考文档

有关端点详情、请求/响应格式以及所有可用字段的信息，请参阅 [references/api_reference.md](references/api_reference.md)。

OpenAPI 3.0 的完整规范请参见 [references/openapi.json](references/openapi.json)。