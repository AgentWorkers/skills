---
name: telnyx-messaging-hosted-ruby
description: >-
  Set up hosted SMS numbers, toll-free verification, and RCS messaging. Use when
  migrating numbers or enabling rich messaging features. This skill provides
  Ruby SDK examples.
metadata:
  author: telnyx
  product: messaging-hosted
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息托管服务 - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出托管消息服务的号码订单

`GET /messaging_hosted_number_orders`

```ruby
page = client.messaging_hosted_number_orders.list

puts(page)
```

## 创建托管消息服务的号码订单

`POST /messaging_hosted_number_orders`

```ruby
messaging_hosted_number_order = client.messaging_hosted_number_orders.create

puts(messaging_hosted_number_order)
```

## 获取托管消息服务的号码订单信息

`GET /messaging_hosted_number_orders/{id}`

```ruby
messaging_hosted_number_order = client.messaging_hosted_number_orders.retrieve("id")

puts(messaging_hosted_number_order)
```

## 删除托管消息服务的号码订单

删除托管消息服务的号码订单及其所有关联的电话号码。

`DELETE /messaging_hosted_number_orders/{id}`

```ruby
messaging_hosted_number_order = client.messaging_hosted_number_orders.delete("id")

puts(messaging_hosted_number_order)
```

## 上传托管号码相关文档

`POST /messaging_hosted_number_orders/{id}/actions/file_upload`

```ruby
response = client.messaging_hosted_number_orders.actions.upload_file("id")

puts(response)
```

## 验证托管号码的验证码

验证发送到托管号码的验证码。

`POST /messaging_hosted_number_orders/{id}/validation_codes` — 必需参数：`verification_codes`

```ruby
response = client.messaging_hosted_number_orders.validate_codes(
  "id",
  verification_codes: [{code: "code", phone_number: "phone_number"}]
)

puts(response)
```

## 为托管号码生成验证码

为托管号码生成验证码。

`POST /messaging_hosted_number_orders/{id}/verification_codes` — 必需参数：`phone_numbers`, `verification_method`

```ruby
response = client.messaging_hosted_number_orders.create_verification_codes(
  "id",
  phone_numbers: ["string"],
  verification_method: :sms
)

puts(response)
```

## 检查托管号码的适用性

`POST /messaging_hosted_number_orders/eligibility_numbers_check` — 必需参数：`phone_numbers`

```ruby
response = client.messaging_hosted_number_orders.check_eligibility(phone_numbers: ["string"])

puts(response)
```

## 删除托管消息服务的号码

`DELETE /messaging_hosted_numbers/{id}`

```ruby
messaging_hosted_number = client.messaging_hosted_numbers.delete("id")

puts(messaging_hosted_number)
```

## 发送 RCS 消息

`POST /messages/rcs` — 必需参数：`agent_id`, `to`, `messaging_profile_id`, `agent_message`

```ruby
response = client.messages.rcs.send_(
  agent_id: "Agent007",
  agent_message: {},
  messaging_profile_id: "messaging_profile_id",
  to: "+13125551234"
)

puts(response)
```

## 列出所有 RCS 代理

`GET /messaging/rcs/agents`

```ruby
page = client.messaging.rcs.agents.list

puts(page)
```

## 获取单个 RCS 代理的信息

`GET /messaging/rcs/agents/{id}`

```ruby
rcs_agent_response = client.messaging.rcs.agents.retrieve("id")

puts(rcs_agent_response)
```

## 修改 RCS 代理

`PATCH /messaging/rcs/agents/{id}`

```ruby
rcs_agent_response = client.messaging.rcs.agents.update("id")

puts(rcs_agent_response)
```

## 检查 RCS 功能（批量）

`POST /messaging/rcs/bulk_capabilities` — 必需参数：`agent_id`, `phone_numbers`

```ruby
response = client.messaging.rcs.list_bulk_capabilities(agent_id: "TestAgent", phone_numbers: ["+13125551234"])

puts(response)
```

## 检查单个 RCS 代理的功能

`GET /messaging/rcs/capabilities/{agent_id}/{phone_number}`

```ruby
response = client.messaging.rcs.retrieve_capabilities("phone_number", agent_id: "agent_id")

puts(response)
```

## 为 RCS 代理添加测试号码

为测试目的向 RCS 代理添加测试电话号码。

`PUT /messages/rcs/test_number_invite/{id}/{phone_number}`

```ruby
response = client.messaging.rcs.invite_test_number("phone_number", id: "id")

puts(response)
```

## 生成 RCS 深链接

生成可用于与特定代理发起 RCS 对话的深链接。

`GET /messages/rcs_deeplinks/{agent_id}`

```ruby
response = client.messages.rcs.generate_deeplink("agent_id")

puts(response)
```

## 列出验证请求

获取之前提交的免费电话验证请求列表

`GET /messaging_tollfree/verification/requests`

```ruby
page = client.messaging_tollfree.verification.requests.list(page: 1, page_size: 1)

puts(page)
```

## 提交验证请求

提交新的免费电话验证请求

`POST /messaging_tollfree/verification/requests` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```ruby
verification_request_egress = client.messaging_tollfree.verification.requests.create(
  additional_information: "additionalInformation",
  business_addr1: "600 Congress Avenue",
  business_city: "Austin",
  business_contact_email: "email@example.com",
  business_contact_first_name: "John",
  business_contact_last_name: "Doe",
  business_contact_phone: "+18005550100",
  business_name: "Telnyx LLC",
  business_state: "Texas",
  business_zip: "78701",
  corporate_website: "http://example.com",
  isv_reseller: "isvReseller",
  message_volume: :"100,000",
  opt_in_workflow: "User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
  opt_in_workflow_image_urls: [{url: "https://client.com/sign-up"}, {url: "https://client.com/company/data-privacy"}],
  phone_numbers: [{phoneNumber: "+18773554398"}, {phoneNumber: "+18773554399"}],
  production_message_content: "Your Telnyx OTP is XXXX",
  use_case: :"2FA",
  use_case_summary: "This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal"
)

puts(verification_request_egress)
```

## 获取验证请求信息

通过 ID 获取单个验证请求的详细信息。

`GET /messaging_tollfree/verification/requests/{id}`

```ruby
verification_request_status = client.messaging_tollfree.verification.requests.retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(verification_request_status)
```

## 更新验证请求

更新现有的免费电话验证请求。

`PATCH /messaging_tollfree/verification/requests/{id}` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```ruby
verification_request_egress = client.messaging_tollfree.verification.requests.update(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  additional_information: "additionalInformation",
  business_addr1: "600 Congress Avenue",
  business_city: "Austin",
  business_contact_email: "email@example.com",
  business_contact_first_name: "John",
  business_contact_last_name: "Doe",
  business_contact_phone: "+18005550100",
  business_name: "Telnyx LLC",
  business_state: "Texas",
  business_zip: "78701",
  corporate_website: "http://example.com",
  isv_reseller: "isvReseller",
  message_volume: :"100,000",
  opt_in_workflow: "User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
  opt_in_workflow_image_urls: [{url: "https://client.com/sign-up"}, {url: "https://client.com/company/data-privacy"}],
  phone_numbers: [{phoneNumber: "+18773554398"}, {phoneNumber: "+18773554399"}],
  production_message_content: "Your Telnyx OTP is XXXX",
  use_case: :"2FA",
  use_case_summary: "This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal"
)

puts(verification_request_egress)
```

## 删除验证请求

仅当验证请求处于“被拒绝”状态时，才能将其删除。

`DELETE /messaging_tollfree/verification/requests/{id}`

```ruby
result = client.messaging_tollfree.verification.requests.delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")

puts(result)
```