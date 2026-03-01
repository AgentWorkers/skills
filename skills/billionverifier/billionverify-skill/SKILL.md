---
name: billionverify
description: 使用 BillionVerify API 验证电子邮件地址。适用于用户需要验证单个电子邮件地址、批量验证电子邮件列表、上传文件进行批量验证、检查信用余额或管理 Webhook 的场景。
version: 1.0.0
allowed-tools: Bash
---
# BillionVerify API 功能说明

您可以使用 [BillionVerify](https://billionverify.com/) API 来验证电子邮件地址，支持单次验证、批量验证或通过文件批量验证。

## 设置

API 密钥需要设置为环境变量 `BILLIONVERIFY_API_KEY`。您可以在以下链接获取 API 密钥：  
https://billionverify.com/auth/sign-in?next=/home/api-keys

## 基本 URL  
```
https://api.billionverify.com
```

## 认证

所有请求都必须包含 API 密钥头部信息：  
```bash
-H "BV-API-KEY: $BILLIONVERIFY_API_KEY"
```

## 端点说明

### 单个电子邮件验证  
```bash
curl -X POST "https://api.billionverify.com/v1/verify/single" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "check_smtp": true
  }'
```

响应内容包括：`status`（有效/无效/未知/风险/一次性使用/通用）、`score`（0-1）、`is_deliverable`、`is_disposable`、`is_catchall`、`is_role`、`is_free`、`domain`、`domain_age`、`mx_records`、`domain_reputation`、`smtp_check`、`reason`、`suggestion`、`response_time`、`credits_used`。

### 批量验证（最多 50 封电子邮件）  
```bash
curl -X POST "https://api.billionverify.com/v1/verify/bulk" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "emails": ["user1@example.com", "user2@example.com"],
    "check_smtp": true
  }'
```

### 上传文件进行批量验证  
支持上传 CSV、Excel（.xlsx/.xls）或 TXT 格式的文件（文件大小不超过 20MB，最多包含 100,000 封电子邮件）：  
```bash
curl -X POST "https://api.billionverify.com/v1/verify/file" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY" \
  -F "file=@/path/to/emails.csv" \
  -F "check_smtp=true" \
  -F "email_column=email" \
  -F "preserve_original=true"
```

系统会返回一个 `task_id`，用于追踪异步任务的进度。

### 获取文件验证状态  
支持使用 `timeout` 参数（0-300 秒）进行长轮询：  
```bash
curl -X GET "https://api.billionverify.com/v1/verify/file/{task_id}?timeout=30" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY"
```

状态值：`pending`（待处理）、`processing`（处理中）、`completed`（已完成）、`failed`（失败）。

### 下载验证结果  
- 无需过滤条件时，系统会直接返回所有验证结果；  
- 使用过滤条件时（过滤条件采用 OR 逻辑组合），系统会返回匹配的电子邮件列表（格式为 CSV）：  
```bash
curl -X GET "https://api.billionverify.com/v1/verify/file/{task_id}/results?valid=true&invalid=true" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY" \
  -L -o results.csv
```

过滤参数：`valid`（有效）、`invalid`（无效）、`catchall`（通用邮箱）、`role`（特定角色）、`unknown`（未知状态）、`disposable`（一次性使用）、`risky`（高风险）。

### 获取剩余信用额度  
```bash
curl -X GET "https://api.billionverify.com/v1/credits" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY"
```

### 创建 Webhook  
创建 Webhook 时系统会返回一个 `secret` 参数，请妥善保管：  
```bash
curl -X POST "https://api.billionverify.com/v1/webhooks" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-app.com/webhooks/billionverify",
    "events": ["file.completed", "file.failed"]
  }'
```

### 列出已创建的 Webhook  
```bash
curl -X GET "https://api.billionverify.com/v1/webhooks" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY"
```

### 删除 Webhook  
```bash
curl -X DELETE "https://api.billionverify.com/v1/webhooks/{webhook_id}" \
  -H "BV-API-KEY: $BILLIONVERIFY_API_KEY"
```

### 健康检查（无需认证）  
```bash
curl -X GET "https://api.billionverify.com/health"
```

## 信用额度与计费规则  

- **无效**/**未知** 状态：0 信用额度（免费）  
- 其他所有状态（有效、风险、一次性使用、通用、特定角色）：每封电子邮件消耗 1 信用额度。

## 速率限制  

| 端点        | 限制      |
|------------|---------|
| 单个电子邮件验证 | 每分钟 6,000 次 |
| 批量验证     | 每分钟 1,500 次 |
| 文件上传     | 每分钟 300 次 |
| 其他端点     | 每分钟 200 次 |

## 用户请求参数  
$ARGUMENTS