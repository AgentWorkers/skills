---
name: telnyx-10dlc-ruby
description: >-
  Register brands and campaigns for 10DLC (10-digit long code) A2P messaging
  compliance in the US. Manage campaign assignments to phone numbers. This skill
  provides Ruby SDK examples.
metadata:
  author: telnyx
  product: 10dlc
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 10Dlc - Ruby

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

## 列出品牌

此端点用于列出与您的组织关联的所有品牌。

`GET /10dlc/brand`

```ruby
page = client.messaging_10dlc.brand.list

puts(page)
```

## 创建品牌

此端点用于创建新的品牌。

`POST /10dlc/brand` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```ruby
telnyx_brand = client.messaging_10dlc.brand.create(
  country: "US",
  display_name: "ABC Mobile",
  email: "email",
  entity_type: :PRIVATE_PROFIT,
  vertical: :TECHNOLOGY
)

puts(telnyx_brand)
```

## 获取品牌信息

通过 `brandId` 获取品牌详情。

`GET /10dlc/brand/{brandId}`

```ruby
brand = client.messaging_10dlc.brand.retrieve("brandId")

puts(brand)
```

## 更新品牌信息

通过 `brandId` 更新品牌属性。

`PUT /10dlc/brand/{brandId}` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```ruby
telnyx_brand = client.messaging_10dlc.brand.update(
  "brandId",
  country: "US",
  display_name: "ABC Mobile",
  email: "email",
  entity_type: :PRIVATE_PROFIT,
  vertical: :TECHNOLOGY
)

puts(telnyx_brand)
```

## 删除品牌

删除品牌。

`DELETE /10dlc/brand/{brandId}`

```ruby
result = client.messaging_10dlc.brand.delete("brandId")

puts(result)
```

## 重新发送品牌 2FA 邮件

`POST /10dlc/brand/{brandId}/2faEmail`

```ruby
result = client.messaging_10dlc.brand.resend_2fa_email("brandId")

puts(result)
```

## 获取品牌的外部审核记录

获取指定品牌的所有有效外部审核记录。

`GET /10dlc/brand/{brandId}/externalVetting`

```ruby
external_vettings = client.messaging_10dlc.brand.external_vetting.list("brandId")

puts(external_vettings)
```

## 请求品牌的外部审核

为品牌请求新的外部审核。

`POST /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingClass`

```ruby
response = client.messaging_10dlc.brand.external_vetting.order(
  "brandId",
  evp_id: "evpId",
  vetting_class: "vettingClass"
)

puts(response)
```

## 导入外部审核记录

此操作可用于从 TCR 批准的审核提供商导入外部审核记录。

`PUT /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingId`

```ruby
response = client.messaging_10dlc.brand.external_vetting.imports("brandId", evp_id: "evpId", vetting_id: "vettingId")

puts(response)
```

## 取消品牌认证

此操作允许您取消品牌的认证。

`PUT /10dlc/brand/{brandId}/revet`

```ruby
telnyx_brand = client.messaging_10dlc.brand.revet("brandId")

puts(telnyx_brand)
```

## 通过品牌 ID 查询 SMS OTP 状态

使用品牌 ID 查询 SMS OTP（一次性密码）的状态，用于个人独资企业的品牌验证。

`GET /10dlc/brand/{brandId}/smsOtp`

```ruby
response = client.messaging_10dlc.brand.retrieve_sms_otp_status("4b20019b-043a-78f8-0657-b3be3f4b4002")

puts(response)
```

## 触发品牌 SMS OTP

触发或重新触发 SMS OTP（一次性密码），用于个人独资企业的品牌验证。

`POST /10dlc/brand/{brandId}/smsOtp` — 必需参数：`pinSms`, `successSms`

```ruby
response = client.messaging_10dlc.brand.trigger_sms_otp(
  "4b20019b-043a-78f8-0657-b3be3f4b4002",
  pin_sms: "Your PIN is @OTP_PIN@",
  success_sms: "Verification successful!"
)

puts(response)
```

## 验证品牌 SMS OTP

验证 SMS OTP（一次性密码），用于个人独资企业的品牌验证。

`PUT /10dlc/brand/{brandId}/smsOtp` — 必需参数：`otpPin`

```ruby
result = client.messaging_10dlc.brand.verify_sms_otp("4b20019b-043a-78f8-0657-b3be3f4b4002", otp_pin: "123456")

puts(result)
```

## 通过 ID 获取品牌反馈

通过 ID 获取关于品牌的反馈信息。

`GET /10dlc/brand_feedback/{brandId}`

```ruby
response = client.messaging_10dlc.brand.get_feedback("brandId")

puts(response)
```

## 提交活动计划

在创建活动计划之前，请使用 [Qualify By Usecase 端点](https://developers.telnyx.com/api-reference/campaign/qualify-by-usecase) 确保您想要分配新活动计划的品牌符合要求...

`POST /10dlc/campaignBuilder` — 必需参数：`brandId`, `description`, `usecase`

```ruby
telnyx_campaign_csp = client.messaging_10dlc.campaign_builder.submit(
  brand_id: "brandId",
  description: "description",
  usecase: "usecase"
)

puts(telnyx_campaign_csp)
```

## 根据用例验证品牌

此端点用于检查提供的品牌是否适合您所需的活动计划用例。

`GET /10dlc/campaignBuilder/brand/{brandId}/usecase/{usecase}`

```ruby
response = client.messaging_10dlc.campaign_builder.brand.qualify_by_usecase("usecase", brand_id: "brandId")

puts(response)
```

## 列出活动计划

检索与指定 `brandId` 关联的所有活动计划。

`GET /10dlc/campaign`

```ruby
page = client.messaging_10dlc.campaign.list(brand_id: "brandId")

puts(page)
```

## 获取活动计划详情

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/campaign/{campaignId}`

```ruby
telnyx_campaign_csp = client.messaging_10dlc.campaign.retrieve("campaignId")

puts(telnyx_campaign_csp)
```

## 更新活动计划

通过 `campaignId` 更新活动计划的属性。

`PUT /10dlc/campaign/{campaignId}`

```ruby
telnyx_campaign_csp = client.messaging_10dlc.campaign.update("campaignId")

puts(telnyx_campaign_csp)
```

## 关闭活动计划

终止活动计划。

`DELETE /10dlc/campaign/{campaignId}`

```ruby
response = client.messaging_10dlc.campaign.deactivate("campaignId")

puts(response)
```

## 为被拒绝的活动计划提交申诉

为状态为 TELNYX_FAILED 或 MNO_REJECTED 的活动计划提交申诉。

`POST /10dlc/campaign/{campaignId}/appeal` — 必需参数：`appeal_reason`

```ruby
response = client.messaging_10dlc.campaign.submit_appeal(
  "5eb13888-32b7-4cab-95e6-d834dde21d64",
  appeal_reason: "The website has been updated to include the required privacy policy and terms of service."
)

puts(response)
```

## 获取活动计划的 MNO 元数据

获取每个 MNO 的活动计划元数据。

`GET /10dlc/campaign/{campaignId}/mnoMetadata`

```ruby
response = client.messaging_10dlc.campaign.get_mno_metadata("campaignId")

puts(response)
```

## 获取活动计划的操作状态

检索活动计划在 MNO 级别的操作状态。

`GET /10dlc/campaign/{campaignId}/operationStatus`

```ruby
response = client.messaging_10dlc.campaign.get_operation_status("campaignId")

puts(response)
```

## 获取 OSR 活动计划属性

`GET /10dlc/campaign/{campaignId}/osr_attributes`

```ruby
response = client.messaging_10dlc.campaign.osr.get_attributes("campaignId")

puts(response)
```

## 获取共享状态

`GET /10dlc/campaign/{campaignId}/sharing`

```ruby
response = client.messaging_10dlc.campaign.get_sharing_status("campaignId")

puts(response)
```

## 接受共享的活动计划

手动接受与 Telnyx 共享的活动计划。

`POST /10dlc/campaign/acceptSharing/{campaignId}`

```ruby
response = client.messaging_10dlc.campaign.accept_sharing("C26F1KLZN")

puts(response)
```

## 获取活动计划成本

`GET /10dlc/campaign/usecase_cost`

```ruby
response = client.messaging_10dlc.campaign.usecase.get_cost(usecase: "usecase")

puts(response)
```

## 列出共享的活动计划

分页方式检索您与 Telnyx 共享的所有活动计划。

`GET /10dlc/partner_campaigns`

```ruby
page = client.messaging_10dlc.partner_campaigns.list

puts(page)
```

## 获取单个共享活动计划

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/partner_campaigns/{campaignId}`

```ruby
telnyx_downstream_campaign = client.messaging_10dlc.partner_campaigns.retrieve("campaignId")

puts(telnyx_downstream_campaign)
```

## 更新单个共享活动计划

通过 `campaignId` 更新活动计划详情。

`PATCH /10dlc/partner_campaigns/{campaignId}`

```ruby
telnyx_downstream_campaign = client.messaging_10dlc.partner_campaigns.update("campaignId")

puts(telnyx_downstream_campaign)
```

## 获取共享状态

`GET /10dlc/partnerCampaign/{campaignId}/sharing`

```ruby
response = client.messaging_10dlc.partner_campaigns.retrieve_sharing_status("campaignId")

puts(response)
```

## 列出共享的活动计划

分页方式检索您与 Telnyx 共享的所有活动计划。

此端点目前仅返回 Telnyx 已接受的活动计划。

`GET /10dlc/partnerCampaign/sharedByMe`

```ruby
page = client.messaging_10dlc.partner_campaigns.list_shared_by_me

puts(page)
```

## 列出电话号码活动计划

`GET /10dlc/phone_number_campaigns`

```ruby
page = client.messaging_10dlc.phone_number_campaigns.list

puts(page)
```

## 创建新的电话号码活动计划

`POST /10dlc/phone_number_campaigns` — 必需参数：`phoneNumber`, `campaignId`

```ruby
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.create(
  campaign_id: "4b300178-131c-d902-d54e-72d90ba1620j",
  phone_number: "+18005550199"
)

puts(phone_number_campaign)
```

## 获取单个电话号码活动计划

通过 `phoneNumber` 获取特定的电话号码/活动计划关联信息。

`GET /10dlc/phone_number_campaigns/{phoneNumber}`

```ruby
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.retrieve("phoneNumber")

puts(phone_number_campaign)
```

## 创建新的电话号码活动计划

`PUT /10dlc/phone_number_campaigns/{phoneNumber}` — 必需参数：`phoneNumber`, `campaignId`

```ruby
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.update(
  "phoneNumber",
  campaign_id: "4b300178-131c-d902-d54e-72d90ba1620j",
  phone_number: "+18005550199"
)

puts(phone_number_campaign)
```

## 删除电话号码活动计划

此端点用于删除与指定 `phoneNumber` 关联的活动计划。

`DELETE /10dlc/phone_number_campaigns/{phoneNumber}`

```ruby
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.delete("phoneNumber")

puts(phone_number_campaign)
```

## 将消息配置文件分配给活动计划

此端点允许您将所有与消息配置文件关联的电话号码链接到活动计划。

`POST /10dlc/phoneNumberAssignmentByProfile` — 必需参数：`messagingProfileId`

```ruby
response = client.messaging_10dlc.phone_number_assignment_by_profile.assign(
  messaging_profile_id: "4001767e-ce0f-4cae-9d5f-0d5e636e7809"
)

puts(response)
```

## 获取任务状态

检查将所有电话号码分配给活动计划的任务状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}`

```ruby
response = client.messaging_10dlc.phone_number_assignment_by_profile.retrieve_status("taskId")

puts(response)
```

## 获取电话号码状态

检查与指定 `taskId` 关联的个别电话号码/活动计划分配的状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}/phoneNumbers`

```ruby
response = client.messaging_10dlc.phone_number_assignment_by_profile.list_phone_number_status("taskId")

puts(response)
```

---

## Webhook

以下 Webhook 事件将发送到您配置的 webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `campaignStatusUpdate` | 活动计划状态更新 |
```