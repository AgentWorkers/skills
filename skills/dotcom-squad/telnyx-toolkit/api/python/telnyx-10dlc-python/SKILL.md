---
name: telnyx-10dlc-python
description: >-
  Register brands and campaigns for 10DLC (10-digit long code) A2P messaging
  compliance in the US. Manage campaign assignments to phone numbers. This skill
  provides Python SDK examples.
metadata:
  author: telnyx
  product: 10dlc
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 10Dlc - Python

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出品牌

此端点用于列出与您的组织关联的所有品牌。

`GET /10dlc/brand`

```python
page = client.messaging_10dlc.brand.list()
page = page.records[0]
print(page.identity_status)
```

## 创建品牌

此端点用于创建新品牌。

`POST /10dlc/brand` — 必需参数：`entityType`、`displayName`、`country`、`email`、`vertical`

```python
telnyx_brand = client.messaging_10dlc.brand.create(
    country="US",
    display_name="ABC Mobile",
    email="email",
    entity_type="PRIVATE_PROFIT",
    vertical="TECHNOLOGY",
)
print(telnyx_brand.identity_status)
```

## 获取品牌信息

通过 `brandId` 获取品牌详情。

`GET /10dlc/brand/{brandId}`

```python
brand = client.messaging_10dlc.brand.retrieve(
    "brandId",
)
print(brand)
```

## 更新品牌信息

通过 `brandId` 更新品牌属性。

`PUT /10dlc/brand/{brandId}` — 必需参数：`entityType`、`displayName`、`country`、`email`、`vertical`

```python
telnyx_brand = client.messaging_10dlc.brand.update(
    brand_id="brandId",
    country="US",
    display_name="ABC Mobile",
    email="email",
    entity_type="PRIVATE_PROFIT",
    vertical="TECHNOLOGY",
)
print(telnyx_brand.identity_status)
```

## 删除品牌

删除品牌。

`DELETE /10dlc/brand/{brandId}`

```python
client.messaging_10dlc.brand.delete(
    "brandId",
)
```

## 重新发送品牌 2FA 邮件

`POST /10dlc/brand/{brandId}/2faEmail`

```python
client.messaging_10dlc.brand.resend_2fa_email(
    "brandId",
)
```

## 获取品牌的外部审核记录

获取指定品牌的有效外部审核记录列表。

`GET /10dlc/brand/{brandId}/externalVetting`

```python
external_vettings = client.messaging_10dlc.brand.external_vetting.list(
    "brandId",
)
print(external_vettings)
```

## 为品牌请求外部审核

为品牌请求新的外部审核。

`POST /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`、`vettingClass`

```python
response = client.messaging_10dlc.brand.external_vetting.order(
    brand_id="brandId",
    evp_id="evpId",
    vetting_class="vettingClass",
)
print(response.create_date)
```

## 导入外部审核记录

此操作可用于从 TCR 批准的审核提供商导入外部审核记录。

`PUT /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`、`vettingId`

```python
response = client.messaging_10dlc.brand.external_vetting.imports(
    brand_id="brandId",
    evp_id="evpId",
    vetting_id="vettingId",
)
print(response.create_date)
```

## 取消品牌审核

此操作允许您取消品牌的审核状态。

`PUT /10dlc/brand/{brandId}/revet`

```python
telnyx_brand = client.messaging_10dlc.brand.revet(
    "brandId",
)
print(telnyx_brand.identity_status)
```

## 通过品牌 ID 获取 SMS OTP 状态

查询使用品牌 ID 进行的 Sole Proprietor 品牌验证的 SMS OTP（一次性密码）状态。

`GET /10dlc/brand/{brandId}/smsOtp`

```python
response = client.messaging_10dlc.brand.retrieve_sms_otp_status(
    "4b20019b-043a-78f8-0657-b3be3f4b4002",
)
print(response.brand_id)
```

## 触发品牌 SMS OTP

触发或重新触发用于 Sole Proprietor 品牌验证的 SMS OTP（一次性密码）。

`POST /10dlc/brand/{brandId}/smsOtp` — 必需参数：`pinSms`、`successSms`

```python
response = client.messaging_10dlc.brand.trigger_sms_otp(
    brand_id="4b20019b-043a-78f8-0657-b3be3f4b4002",
    pin_sms="Your PIN is @OTP_PIN@",
    success_sms="Verification successful!",
)
print(response.brand_id)
```

## 验证品牌 SMS OTP

验证用于 Sole Proprietor 品牌验证的 SMS OTP（一次性密码）。

`PUT /10dlc/brand/{brandId}/smsOtp` — 必需参数：`otpPin`

```python
client.messaging_10dlc.brand.verify_sms_otp(
    brand_id="4b20019b-043a-78f8-0657-b3be3f4b4002",
    otp_pin="123456",
)
```

## 通过 ID 获取品牌反馈

通过 ID 获取关于品牌的反馈信息。

`GET /10dlc/brand_feedback/{brandId}`

```python
response = client.messaging_10dlc.brand.get_feedback(
    "brandId",
)
print(response.brand_id)
```

## 提交活动计划

在创建活动计划之前，请使用 [Qualify By Usecase 端点](https://developers.telnyx.com/api-reference/campaign/qualify-by-usecase) 确保您想要分配新活动计划的品牌符合要求...

`POST /10dlc/campaignBuilder` — 必需参数：`brandId`、`description`、`usecase`

```python
telnyx_campaign_csp = client.messaging_10dlc.campaign_builder.submit(
    brand_id="brandId",
    description="description",
    usecase="usecase",
)
print(telnyx_campaign_csp.brand_id)
```

## 根据用例验证品牌

此端点用于检查提供的品牌是否适合您的活动计划用例。

`GET /10dlc/campaignBuilder/brand/{brandId}/usecase/{usecase}`

```python
response = client.messaging_10dlc.campaign_builder.brand.qualify_by_usecase(
    usecase="usecase",
    brand_id="brandId",
)
print(response.annual_fee)
```

## 列出活动计划

检索与指定 `brandId` 关联的所有活动计划。

`GET /10dlc/campaign`

```python
page = client.messaging_10dlc.campaign.list(
    brand_id="brandId",
)
page = page.records[0]
print(page.age_gated)
```

## 获取活动计划详情

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/campaign/{campaignId}`

```python
telnyx_campaign_csp = client.messaging_10dlc.campaign.retrieve(
    "campaignId",
)
print(telnyx_campaign_csp.brand_id)
```

## 更新活动计划

通过 `campaignId` 更新活动计划的属性。

`PUT /10dlc/campaign/{campaignId}`

```python
telnyx_campaign_csp = client.messaging_10dlc.campaign.update(
    campaign_id="campaignId",
)
print(telnyx_campaign_csp.brand_id)
```

## 关闭活动计划

终止活动计划。

`DELETE /10dlc/campaign/{campaignId}`

```python
response = client.messaging_10dlc.campaign.deactivate(
    "campaignId",
)
print(response.time)
```

## 为被拒绝的活动计划提交申诉

为状态为 TELNYX_FAILED 或 MNO_REJECTED 的活动计划提交申诉。

`POST /10dlc/campaign/{campaignId}/appeal` — 必需参数：`appeal_reason`

```python
response = client.messaging_10dlc.campaign.submit_appeal(
    campaign_id="5eb13888-32b7-4cab-95e6-d834dde21d64",
    appeal_reason="The website has been updated to include the required privacy policy and terms of service.",
)
print(response.appealed_at)
```

## 获取活动计划的 MNO 元数据

获取每个 MNO 的活动计划元数据。

`GET /10dlc/campaign/{campaignId}/mnoMetadata`

```python
response = client.messaging_10dlc.campaign.get_mno_metadata(
    "campaignId",
)
print(response._10999)
```

## 获取活动计划的操作状态

检索活动计划在 MNO 级别的操作状态。

`GET /10dlc/campaign/{campaignId}/operationStatus`

```python
response = client.messaging_10dlc.campaign.get_operation_status(
    "campaignId",
)
print(response)
```

## 获取 OSR 活动计划属性

`GET /10dlc/campaign/{campaignId}/osr_attributes`

```python
response = client.messaging_10dlc.campaign.osr.get_attributes(
    "campaignId",
)
print(response)
```

## 获取共享状态

`GET /10dlc/campaign/{campaignId}/sharing`

```python
response = client.messaging_10dlc.campaign.get_sharing_status(
    "campaignId",
)
print(response.shared_by_me)
```

## 接受共享的活动计划

手动接受与 Telnyx 共享的活动计划。

`POST /10dlc/campaign/acceptSharing/{campaignId}`

```python
response = client.messaging_10dlc.campaign.accept_sharing(
    "C26F1KLZN",
)
print(response)
```

## 获取活动计划成本

`GET /10dlc/campaign/usecase_cost`

```python
response = client.messaging_10dlc.campaign.usecase.get_cost(
    usecase="usecase",
)
print(response.campaign_usecase)
```

## 列出共享的活动计划

分页方式获取您与 Telnyx 共享的所有合作伙伴活动计划。

`GET /10dlc/partner_campaigns`

```python
page = client.messaging_10dlc.partner_campaigns.list()
page = page.records[0]
print(page.tcr_brand_id)
```

## 获取单个共享活动计划

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/partner_campaigns/{campaignId}`

```python
telnyx_downstream_campaign = client.messaging_10dlc.partner_campaigns.retrieve(
    "campaignId",
)
print(telnyx_downstream_campaign.tcr_brand_id)
```

## 更新单个共享活动计划

通过 `campaignId` 更新活动计划详情。

`PATCH /10dlc/partner_campaigns/{campaignId}`

```python
telnyx_downstream_campaign = client.messaging_10dlc.partner_campaigns.update(
    campaign_id="campaignId",
)
print(telnyx_downstream_campaign.tcr_brand_id)
```

## 获取共享状态

`GET /10dlc/partnerCampaign/{campaignId}/sharing`

```python
response = client.messaging_10dlc.partner_campaigns.retrieve_sharing_status(
    "campaignId",
)
print(response)
```

## 列出共享的合作伙伴活动计划

分页方式获取您与 Telnyx 共享的所有合作伙伴活动计划

此端点目前仅返回 Telnyx 已接受的活动计划。

`GET /10dlc/partnerCampaign/sharedByMe`

```python
page = client.messaging_10dlc.partner_campaigns.list_shared_by_me()
page = page.records[0]
print(page.brand_id)
```

## 列出电话号码活动计划

`GET /10dlc/phone_number_campaigns`

```python
page = client.messaging_10dlc.phone_number_campaigns.list()
page = page.records[0]
print(page.campaign_id)
```

## 创建新的电话号码活动计划

`POST /10dlc/phone_number_campaigns` — 必需参数：`phoneNumber`、`campaignId`

```python
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.create(
    campaign_id="4b300178-131c-d902-d54e-72d90ba1620j",
    phone_number="+18005550199",
)
print(phone_number_campaign.campaign_id)
```

## 获取单个电话号码活动计划

通过 `phoneNumber` 获取特定的电话号码/活动计划分配信息。

`GET /10dlc/phone_number_campaigns/{phoneNumber}`

```python
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.retrieve(
    "phoneNumber",
)
print(phone_number_campaign.campaign_id)
```

## 创建新的电话号码活动计划

`PUT /10dlc/phone_number_campaigns/{phoneNumber}` — 必需参数：`phoneNumber`、`campaignId`

```python
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.update(
    campaign_phone_number="phoneNumber",
    campaign_id="4b300178-131c-d902-d54e-72d90ba1620j",
    phone_number="+18005550199",
)
print(phone_number_campaign.campaign_id)
```

## 删除电话号码活动计划

此端点用于删除与指定 `phoneNumber` 关联的活动计划。

`DELETE /10dlc/phone_number_campaigns/{phoneNumber}`

```python
phone_number_campaign = client.messaging_10dlc.phone_number_campaigns.delete(
    "phoneNumber",
)
print(phone_number_campaign.campaign_id)
```

## 将通信配置文件分配给活动计划

此端点允许您将所有与通信配置文件关联的电话号码链接到活动计划。

`POST /10dlc/phoneNumberAssignmentByProfile` — 必需参数：`messagingProfileId`

```python
response = client.messaging_10dlc.phone_number_assignment_by_profile.assign(
    messaging_profile_id="4001767e-ce0f-4cae-9d5f-0d5e636e7809",
)
print(response.messaging_profile_id)
```

## 获取分配任务状态

检查通过 `taskId` 将所有电话号码分配给活动计划的任务状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}`

```python
response = client.messaging_10dlc.phone_number_assignment_by_profile.retrieve_status(
    "taskId",
)
print(response.status)
```

## 获取电话号码状态

检查与指定 `taskId` 关联的个别电话号码/活动计划分配的状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}/phoneNumbers`

```python
response = client.messaging_10dlc.phone_number_assignment_by_profile.list_phone_number_status(
    task_id="taskId",
)
print(response.records)
```

---

## Webhook

以下 Webhook 事件将发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `campaignStatusUpdate` | 活动计划状态更新 |
```
```