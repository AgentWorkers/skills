---
name: telnyx-messaging-hosted-python
description: >-
  Set up hosted SMS numbers, toll-free verification, and RCS messaging. Use when
  migrating numbers or enabling rich messaging features. This skill provides
  Python SDK examples.
metadata:
  author: telnyx
  product: messaging-hosted
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息托管服务 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出托管消息服务的号码订单

`GET /messaging_hosted_number_orders`

```python
page = client.messaging_hosted_number_orders.list()
page = page.data[0]
print(page.id)
```

## 创建托管消息服务的号码订单

`POST /messaging_hosted_number_orders`

```python
messaging_hosted_number_order = client.messaging_hosted_number_orders.create()
print(messaging_hosted_number_order.data)
```

## 获取托管消息服务的号码订单信息

`GET /messaging_hosted_number_orders/{id}`

```python
messaging_hosted_number_order = client.messaging_hosted_number_orders.retrieve(
    "id",
)
print(messaging_hosted_number_order.data)
```

## 删除托管消息服务的号码订单

删除托管消息服务的号码订单及其所有关联的电话号码。

`DELETE /messaging_hosted_number_orders/{id}`

```python
messaging_hosted_number_order = client.messaging_hosted_number_orders.delete(
    "id",
)
print(messaging_hosted_number_order.data)
```

## 上传托管号码文档

`POST /messaging_hosted_number_orders/{id}/actions/file_upload`

```python
response = client.messaging_hosted_number_orders.actions.upload_file(
    id="id",
)
print(response.data)
```

## 验证托管号码的验证码

验证发送到托管号码的验证码。

`POST /messaging_hosted_number_orders/{id}/validation_codes` — 必需参数：`verification_codes`

```python
response = client.messaging_hosted_number_orders.validate_codes(
    id="id",
    verification_codes=[{
        "code": "code",
        "phone_number": "phone_number",
    }],
)
print(response.data)
```

## 生成托管号码的验证码

为托管号码生成验证码。

`POST /messaging_hosted_number_orders/{id}/verification_codes` — 必需参数：`phone_numbers`, `verification_method`

```python
response = client.messaging_hosted_number_orders.create_verification_codes(
    id="id",
    phone_numbers=["string"],
    verification_method="sms",
)
print(response.data)
```

## 检查托管号码的适用性

`POST /messaging_hosted_number_orders/eligibility_numbers_check` — 必需参数：`phone_numbers`

```python
response = client.messaging_hosted_number_orders.check_eligibility(
    phone_numbers=["string"],
)
print(response.phone_numbers)
```

## 删除托管消息服务的号码

`DELETE /messaging_hosted_numbers/{id}`

```python
messaging_hosted_number = client.messaging_hosted_numbers.delete(
    "id",
)
print(messaging_hosted_number.data)
```

## 发送 RCS 消息

`POST /messages/rcs` — 必需参数：`agent_id`, `to`, `messaging_profile_id`, `agent_message`

```python
response = client.messages.rcs.send(
    agent_id="Agent007",
    agent_message={},
    messaging_profile_id="messaging_profile_id",
    to="+13125551234",
)
print(response.data)
```

## 列出所有 RCS 代理

`GET /messaging/rcs/agents`

```python
page = client.messaging.rcs.agents.list()
page = page.data[0]
print(page.agent_id)
```

## 获取 RCS 代理信息

`GET /messaging/rcs/agents/{id}`

```python
rcs_agent_response = client.messaging.rcs.agents.retrieve(
    "id",
)
print(rcs_agent_response.data)
```

## 修改 RCS 代理信息

`PATCH /messaging/rcs/agents/{id}`

```python
rcs_agent_response = client.messaging.rcs.agents.update(
    id="id",
)
print(rcs_agent_response.data)
```

## 检查 RCS 功能（批量）

`POST /messaging/rcs/bulk_capabilities` — 必需参数：`agent_id`, `phone_numbers`

```python
response = client.messaging.rcs.list_bulk_capabilities(
    agent_id="TestAgent",
    phone_numbers=["+13125551234"],
)
print(response.data)
```

## 检查 RCS 功能

`GET /messaging/rcs/capabilities/{agent_id}/{phone_number}`

```python
response = client.messaging.rcs.retrieve_capabilities(
    phone_number="phone_number",
    agent_id="agent_id",
)
print(response.data)
```

## 添加 RCS 测试号码

为 RCS 代理添加测试电话号码以供测试使用。

`PUT /messages/rcs/test_number_invite/{id}/{phone_number}`

```python
response = client.messaging.rcs.invite_test_number(
    phone_number="phone_number",
    id="id",
)
print(response.data)
```

## 生成 RCS 深链接

生成用于与特定代理发起 RCS 对话的深链接。

`GET /messages/rcs_deeplinks/{agent_id}`

```python
response = client.messages.rcs.generate_deeplink(
    agent_id="agent_id",
)
print(response.data)
```

## 列出验证请求

获取之前提交的免费电话验证请求列表

`GET /messaging_tollfree/verification/requests`

```python
page = client.messaging_tollfree.verification.requests.list(
    page=1,
    page_size=1,
)
page = page.records[0]
print(page.id)
```

## 提交验证请求

提交新的免费电话验证请求

`POST /messaging_tollfree/verification/requests` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```python
verification_request_egress = client.messaging_tollfree.verification.requests.create(
    additional_information="additionalInformation",
    business_addr1="600 Congress Avenue",
    business_city="Austin",
    business_contact_email="email@example.com",
    business_contact_first_name="John",
    business_contact_last_name="Doe",
    business_contact_phone="+18005550100",
    business_name="Telnyx LLC",
    business_state="Texas",
    business_zip="78701",
    corporate_website="http://example.com",
    isv_reseller="isvReseller",
    message_volume="100,000",
    opt_in_workflow="User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
    opt_in_workflow_image_urls=[{
        "url": "https://telnyx.com/sign-up"
    }, {
        "url": "https://telnyx.com/company/data-privacy"
    }],
    phone_numbers=[{
        "phone_number": "+18773554398"
    }, {
        "phone_number": "+18773554399"
    }],
    production_message_content="Your Telnyx OTP is XXXX",
    use_case="2FA",
    use_case_summary="This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal",
)
print(verification_request_egress.id)
```

## 获取验证请求信息

通过 ID 获取单个验证请求的详细信息。

`GET /messaging_tollfree/verification/requests/{id}`

```python
verification_request_status = client.messaging_tollfree.verification.requests.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(verification_request_status.id)
```

## 更新验证请求

更新现有的免费电话验证请求。

`PATCH /messaging_tollfree/verification/requests/{id}` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```python
verification_request_egress = client.messaging_tollfree.verification.requests.update(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    additional_information="additionalInformation",
    business_addr1="600 Congress Avenue",
    business_city="Austin",
    business_contact_email="email@example.com",
    business_contact_first_name="John",
    business_contact_last_name="Doe",
    business_contact_phone="+18005550100",
    business_name="Telnyx LLC",
    business_state="Texas",
    business_zip="78701",
    corporate_website="http://example.com",
    isv_reseller="isvReseller",
    message_volume="100,000",
    opt_in_workflow="User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset",
    opt_in_workflow_image_urls=[{
        "url": "https://telnyx.com/sign-up"
    }, {
        "url": "https://telnyx.com/company/data-privacy"
    }],
    phone_numbers=[{
        "phone_number": "+18773554398"
    }, {
        "phone_number": "+18773554399"
    }],
    production_message_content="Your Telnyx OTP is XXXX",
    use_case="2FA",
    use_case_summary="This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal",
)
print(verification_request_egress.id)
```

## 删除验证请求

只有当验证请求处于“已拒绝”状态时，才能删除该请求。

`DELETE /messaging_tollfree/verification/requests/{id}`

```python
client.messaging_tollfree.verification.requests.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```