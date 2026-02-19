---
name: talkspresso
description: 使用 Talkspresso REST API 管理 Talkspresso 业务（服务、预约、产品、客户、收入、日历）。当用户需要查看预订信息、创建服务、管理数字产品、查看收入、更新个人资料、安排会议或执行与 Talkspresso 账户相关的任何操作时，可以使用此 API。需要设置 `TALKSPRESSO_API_KEY` 环境变量。
metadata:
  {
    "openclaw":
      {
        "emoji": "☕",
        "requires": { "env": ["TALKSPRESSO_API_KEY"] },
      },
  }
---
# Talkspresso

您可以使用 `curl` 和 `jq` 通过 REST API 管理 Talkspresso 业务。

## 设置

用户需要一个 `TALKSPRESSO_API_KEY`。如果该密钥缺失：

1. 引导他们访问 [https://app.talkspresso.com/settings/api-keys](https://app.talkspresso.com/settings/api-keys) 以生成一个密钥。
2. 如果他们没有 Talkspresso 账户，请引导他们访问 [https://talkspresso.com/signup](https://talkspresso.com/signup) 注册。
3. 设置 `TALKSPRESSO_API_KEY`：`export TALKSPRESSO_API_KEY="tsp_..."`

如果用户是 Talkspresso 的新用户，请帮助他们完成以下设置：个人资料、时区、可用时间以及首次服务安排。

## API 格式

所有 API 请求都遵循以下格式：

```bash
# GET
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/ENDPOINT" | jq .data

# POST
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}' \
  "https://api.talkspresso.com/ENDPOINT" | jq .data

# PUT
curl -s -X PUT -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}' \
  "https://api.talkspresso.com/ENDPOINT" | jq .data

# DELETE
curl -s -X DELETE -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/ENDPOINT" | jq .data
```

对于每个响应，使用 `jq .data` 来提取数据。API 会将所有响应封装在 `{ "data": ... }` 中。

## 快速参考

### 个人资料

```bash
# Get profile
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/profile/me" | jq .data

# Update profile
curl -s -X PUT -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"expert_title":"Executive Coach","about":"Short bio","bio":"Full bio","categories":["coaching"]}' \
  "https://api.talkspresso.com/profile" | jq .data
```

关键字段：`expert_title`（专家头衔）、`about`（简介）、`bio`（个人简介）、`categories`（类别数组）、`handle`（URL 标识符）、`profile_photo`（个人资料图片）。

### 服务（视频通话、研讨会）

```bash
# List services
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/service/me" | jq .data

# Create service
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Strategy Call",
    "short_description":"1-on-1 strategy session",
    "long_description":"",
    "price":100,
    "duration":30,
    "logistics":{"session_type":"single","capacity_type":"single","capacity":1}
  }' \
  "https://api.talkspresso.com/service" | jq .data

# Update service
curl -s -X PUT -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title":"New Title","price":150}' \
  "https://api.talkspresso.com/service/SERVICE_ID" | jq .data

# Delete service
curl -s -X DELETE -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/service/SERVICE_ID" | jq .data
```

服务类型（通过 `logistics` 字段区分）：
- **一对一通话**：`{"capacity_type":"single","capacity":1}`  
- **小组会议**：`{"capacity_type":"group","capacity":10}`  
- **网络研讨会**：`{"capacity_type":"group","capacity":50,"is_webinar":true}`

### 产品（数字下载）

```bash
# List products
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/product/me" | jq .data

# Create product
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Leadership Guide",
    "slug":"leadership-guide",
    "short_description":"Comprehensive guide for emerging leaders",
    "long_description":"Full description here...",
    "price":29,
    "product_type":"download",
    "status":"active"
  }' \
  "https://api.talkspresso.com/product" | jq .data

# AI-generate product details from description
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"description":"A guide about leadership for new managers","productType":"download"}' \
  "https://api.talkspresso.com/product/generate-details" | jq .data

# Update product
curl -s -X PUT -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"price":39,"status":"active"}' \
  "https://api.talkspresso.com/product/PRODUCT_ID" | jq .data

# Delete product
curl -s -X DELETE -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/product/PRODUCT_ID" | jq .data

# Product analytics
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/product/analytics" | jq .data

# List purchases
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/product/purchases" | jq .data
```

产品类型：`download`（下载）、`video`（视频）、`bundle`（捆绑包）。状态：`draft`（草稿）、`active`（激活）、`archived`（已归档）。

### 预约与日程安排

```bash
# List appointments (upcoming by default)
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/appointments/me?status=upcoming" | jq .data

# Get specific appointment
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/appointments/APT_ID" | jq .data

# Check available time slots
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"date":"2026-02-20","interval":30,"provider_id":"PROVIDER_ID"}' \
  "https://api.talkspresso.com/appointments/slots" | jq .data

# Create appointment (does NOT send email)
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name":"Jane Smith",
    "client_email":"jane@example.com",
    "service_id":"SERVICE_ID",
    "scheduled_date":"2026-02-20",
    "scheduled_time":"10:00",
    "is_complimentary":true,
    "skip_email":true
  }' \
  "https://api.talkspresso.com/appointments/invite" | jq .data

# Send the invitation email (after reviewing)
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}' \
  "https://api.talkspresso.com/appointments/APT_ID/resend-invite" | jq .data

# Approve pending booking
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/appointments/APT_ID/approve" | jq .data

# Cancel appointment
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/appointments/APT_ID/cancel" | jq .data
```

**重要提示：** 在创建预约时，务必先设置 `skip_email: true`。在用户确认后，再发送邀请邮件。

### 客户

```bash
# List clients (optional search)
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/client/my?search=jane" | jq .data

# Get client details + booking history
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/client/CLIENT_ID/appointments" | jq .data

# Get session history (summaries, action items)
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/client/CLIENT_ID/session-history" | jq .data
```

### 收入

```bash
# Get transactions
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/transaction/my?limit=50" | jq .data
```

### 日历与可用时间

```bash
# Get calendar settings (timezone, availability windows)
curl -s -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  "https://api.talkspresso.com/calendar/me" | jq .data

# Update timezone
curl -s -X PUT -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"timezone":"America/New_York"}' \
  "https://api.talkspresso.com/calendar" | jq .data

# Update availability windows
curl -s -X PUT -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"availability":{"Monday":{"is_selected":true,"start_time":"09:00","end_time":"17:00"}}}' \
  "https://api.talkspresso.com/calendar" | jq .data
```

### 文件上传

```bash
# Upload image
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -F "file=@/path/to/image.jpg" \
  "https://api.talkspresso.com/file/upload/image" | jq .data

# Upload video
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -F "file=@/path/to/video.mp4" \
  "https://api.talkspresso.com/file/upload/video" | jq .data

# Upload file (PDF, doc, etc)
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -F "file=@/path/to/document.pdf" \
  "https://api.talkspresso.com/file/upload/file" | jq .data

# Set profile photo (upload, then update profile)
CDN_URL=$(curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -F "file=@/path/to/photo.jpg" \
  "https://api.talkspresso.com/file/upload/image" | jq -r .data)
curl -s -X PUT -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"profile_photo\":\"$CDN_URL\"}" \
  "https://api.talkspresso.com/profile" | jq .data

# Attach file to product
curl -s -X POST -H "Authorization: Bearer $TALKSPRESSO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_type":"pdf","file_name":"Guide.pdf","file_url":"CDN_URL","file_size":12345}' \
  "https://api.talkspresso.com/product/PRODUCT_ID/files" | jq .data
```

产品支持的文件类型：`pdf`（PDF）、`video`（视频）、`audio`（音频）、`image`（图片）、`zip`（压缩文件）、`presentation`（演示文稿）、`other`（其他格式）。

### 预约链接

公共预约页面的 URL 是：`https://talkspresso.com/HANDLE`  
特定服务的预约链接格式为：`https://talkspresso.com/HANDLE/SERVICE_SLUG`  
您可以通过个人资料的 `handle` 字段获取服务的具体 URL 标识符。

## 工作流程

### 新用户设置

1. 查看用户的当前个人资料信息。
2. 更新用户的个人资料：`expert_title`（专家头衔）、`about`（简介）、`bio`（个人简介）。
3. 设置用户的时区。
4. 设置用户的可用时间窗口。
5. 为用户创建首次服务（从免费的 15 分钟试听通话开始）。
6. 分享预约链接：`https://talkspresso.com/HANDLE`。

### 从头开始创建产品

1. 询问用户产品的具体内容。
2. 使用人工智能生成产品详细信息：`POST /product/generate-details`。
3. 根据生成的信息创建产品。
4. 如果用户有相关文件，可以上传文件并将其附加到产品中。
5. 分享产品的链接。

### 预约会议

1. 通过 `GET /client/my?search=name` 查找目标客户。
2. 列出可用的服务选项。
3. 检查用户所在日期的可用时间。
4. 创建预约时设置 `skip_email: true`。
5. 向用户展示预约详情以获取确认。
6. 确认后，再发送邀请邮件。

### 收入统计

1. 通过 `GET /transaction/my` 获取用户的交易记录。
2. 计算当月的总收入。
3. 显示即将进行的预约数量。
4. 提供预约链接供用户分享。

## 规则

- **未经用户确认，切勿发送邀请邮件。** 必须先设置 `skip_email: true`，再展示预约详情后发送邀请。
- **付费服务需要使用 Stripe 支付平台。** 如果用户尚未关联 Stripe 账户，他们只能创建免费服务和免费产品。
- 在需要检查可用时间时，从用户个人资料的 `id` 字段获取 `provider_id`。
- 如果用户未提供服务名称，系统会自动生成服务标识符（`slug`）。标识符应为小写、使用连字符，且不能包含特殊字符。
- 时区信息来自用户的日历设置（请通过 `GET /calendar/me` 获取）。

## 其他 API 端点

有关完整的 API 参考信息（包括通知、用户评价、录制内容、促销代码、文件库、消息功能、Google 日历同步以及组织管理功能），请参阅 [references/api.md](references/api.md)。