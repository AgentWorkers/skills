---
name: telnyx-10dlc-java
description: >-
  Register brands and campaigns for 10DLC (10-digit long code) A2P messaging
  compliance in the US. Manage campaign assignments to phone numbers. This skill
  provides Java SDK examples.
metadata:
  author: telnyx
  product: 10dlc
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 10Dlc - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出品牌

此端点用于列出与您的组织关联的所有品牌。

`GET /10dlc/brand`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandListPage;
import com.telnyx.sdk.models.messaging10dlc.brand.BrandListParams;

BrandListPage page = client.messaging10dlc().brand().list();
```

## 创建品牌

此端点用于创建新品牌。

`POST /10dlc/brand` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandCreateParams;
import com.telnyx.sdk.models.messaging10dlc.brand.EntityType;
import com.telnyx.sdk.models.messaging10dlc.brand.TelnyxBrand;
import com.telnyx.sdk.models.messaging10dlc.brand.Vertical;

BrandCreateParams params = BrandCreateParams.builder()
    .country("US")
    .displayName("ABC Mobile")
    .email("email")
    .entityType(EntityType.PRIVATE_PROFIT)
    .vertical(Vertical.TECHNOLOGY)
    .build();
TelnyxBrand telnyxBrand = client.messaging10dlc().brand().create(params);
```

## 获取品牌信息

通过 `brandId` 获取品牌详细信息。

`GET /10dlc/brand/{brandId}`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandRetrieveParams;
import com.telnyx.sdk.models.messaging10dlc.brand.BrandRetrieveResponse;

BrandRetrieveResponse brand = client.messaging10dlc().brand().retrieve("brandId");
```

## 更新品牌信息

通过 `brandId` 更新品牌属性。

`PUT /10dlc/brand/{brandId}` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandUpdateParams;
import com.telnyx.sdk.models.messaging10dlc.brand.EntityType;
import com.telnyx.sdk.models.messaging10dlc.brand.TelnyxBrand;
import com.telnyx.sdk.models.messaging10dlc.brand.Vertical;

BrandUpdateParams params = BrandUpdateParams.builder()
    .brandId("brandId")
    .country("US")
    .displayName("ABC Mobile")
    .email("email")
    .entityType(EntityType.PRIVATE_PROFIT)
    .vertical(Vertical.TECHNOLOGY)
    .build();
TelnyxBrand telnyxBrand = client.messaging10dlc().brand().update(params);
```

## 删除品牌

删除品牌。

`DELETE /10dlc/brand/{brandId}`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandDeleteParams;

client.messaging10dlc().brand().delete("brandId");
```

## 重新发送品牌 2FA 邮件

`POST /10dlc/brand/{brandId}/2faEmail`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandResend2faEmailParams;

client.messaging10dlc().brand().resend2faEmail("brandId");
```

## 获取品牌的外部审核记录

获取指定品牌的所有有效外部审核记录。

`GET /10dlc/brand/{brandId}/externalVetting`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.externalvetting.ExternalVettingListParams;
import com.telnyx.sdk.models.messaging10dlc.brand.externalvetting.ExternalVettingListResponse;

List<ExternalVettingListResponse> externalVettings = client.messaging10dlc().brand().externalVetting().list("brandId");
```

## 请求品牌的外部审核

为品牌请求新的外部审核。

`POST /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingClass`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.externalvetting.ExternalVettingOrderParams;
import com.telnyx.sdk.models.messaging10dlc.brand.externalvetting.ExternalVettingOrderResponse;

ExternalVettingOrderParams params = ExternalVettingOrderParams.builder()
    .brandId("brandId")
    .evpId("evpId")
    .vettingClass("vettingClass")
    .build();
ExternalVettingOrderResponse response = client.messaging10dlc().brand().externalVetting().order(params);
```

## 导入外部审核记录

此操作可用于从 TCR（Telnyx 认证的）审核提供商导入外部审核记录。

`PUT /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingId`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.externalvetting.ExternalVettingImportsParams;
import com.telnyx.sdk.models.messaging10dlc.brand.externalvetting.ExternalVettingImportsResponse;

ExternalVettingImportsParams params = ExternalVettingImportsParams.builder()
    .brandId("brandId")
    .evpId("evpId")
    .vettingId("vettingId")
    .build();
ExternalVettingImportsResponse response = client.messaging10dlc().brand().externalVetting().imports(params);
```

## 取消品牌审核

此操作允许您取消品牌的审核状态。

`PUT /10dlc/brand/{brandId}/revet`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandRevetParams;
import com.telnyx.sdk.models.messaging10dlc.brand.TelnyxBrand;

TelnyxBrand telnyxBrand = client.messaging10dlc().brand().revet("brandId");
```

## 通过品牌 ID 查询 SMS OTP 状态

使用品牌 ID 查询 SMS OTP（一次性密码）的状态，用于唯一所有者的品牌验证。

`GET /10dlc/brand/{brandId}/smsOtp`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandRetrieveSmsOtpStatusParams;
import com.telnyx.sdk.models.messaging10dlc.brand.BrandRetrieveSmsOtpStatusResponse;

BrandRetrieveSmsOtpStatusResponse response = client.messaging10dlc().brand().retrieveSmsOtpStatus("4b20019b-043a-78f8-0657-b3be3f4b4002");
```

## 触发品牌 SMS OTP

触发或重新触发 SMS OTP（一次性密码），用于唯一所有者的品牌验证。

`POST /10dlc/brand/{brandId}/smsOtp` — 必需参数：`pinSms`, `successSms`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandTriggerSmsOtpParams;
import com.telnyx.sdk.models.messaging10dlc.brand.BrandTriggerSmsOtpResponse;

BrandTriggerSmsOtpParams params = BrandTriggerSmsOtpParams.builder()
    .brandId("4b20019b-043a-78f8-0657-b3be3f4b4002")
    .pinSms("Your PIN is @OTP_PIN@")
    .successSms("Verification successful!")
    .build();
BrandTriggerSmsOtpResponse response = client.messaging10dlc().brand().triggerSmsOtp(params);
```

## 验证品牌 SMS OTP

验证 SMS OTP（一次性密码），用于唯一所有者的品牌验证。

`PUT /10dlc/brand/{brandId}/smsOtp` — 必需参数：`otpPin`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandVerifySmsOtpParams;

BrandVerifySmsOtpParams params = BrandVerifySmsOtpParams.builder()
    .brandId("4b20019b-043a-78f8-0657-b3be3f4b4002")
    .otpPin("123456")
    .build();
client.messaging10dlc().brand().verifySmsOtp(params);
```

## 通过 ID 获取品牌反馈

通过 ID 获取关于品牌的反馈信息。

`GET /10dlc/brand_feedback/{brandId}`

```java
import com.telnyx.sdk.models.messaging10dlc.brand.BrandGetFeedbackParams;
import com.telnyx.sdk.models.messaging10dlc.brand.BrandGetFeedbackResponse;

BrandGetFeedbackResponse response = client.messaging10dlc().brand().getFeedback("brandId");
```

## 提交活动计划

在创建活动计划之前，请使用 [按用例筛选端点](https://developers.telnyx.com/api-reference/campaign/qualify-by-usecase) 确保您想要分配新活动计划的品牌符合要求...

`POST /10dlc/campaignBuilder` — 必需参数：`brandId`, `description`, `usecase`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.TelnyxCampaignCsp;
import com.telnyx.sdk.models.messaging10dlc.campaignbuilder.CampaignBuilderSubmitParams;

CampaignBuilderSubmitParams params = CampaignBuilderSubmitParams.builder()
    .brandId("brandId")
    .description("description")
    .usecase("usecase")
    .build();
TelnyxCampaignCsp telnyxCampaignCsp = client.messaging10dlc().campaignBuilder().submit(params);
```

## 按用例筛选

此端点用于判断提供的品牌是否适合您的活动计划用例。

`GET /10dlc/campaignBuilder/brand/{brandId}/usecase/{usecase}`

```java
import com.telnyx.sdk.models.messaging10dlc.campaignbuilder.brand.BrandQualifyByUsecaseParams;
import com.telnyx.sdk.models.messaging10dlc.campaignbuilder.brand.BrandQualifyByUsecaseResponse;

BrandQualifyByUsecaseParams params = BrandQualifyByUsecaseParams.builder()
    .brandId("brandId")
    .usecase("usecase")
    .build();
BrandQualifyByUsecaseResponse response = client.messaging10dlc().campaignBuilder().brand().qualifyByUsecase(params);
```

## 列出活动计划

检索与指定 `brandId` 关联的所有活动计划。

`GET /10dlc/campaign`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignListPage;
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignListParams;

CampaignListParams params = CampaignListParams.builder()
    .brandId("brandId")
    .build();
CampaignListPage page = client.messaging10dlc().campaign().list(params);
```

## 获取活动计划详情

通过 `campaignId` 获取活动计划详细信息。

`GET /10dlc/campaign/{campaignId}`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignRetrieveParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.TelnyxCampaignCsp;

TelnyxCampaignCsp telnyxCampaignCsp = client.messaging10dlc().campaign().retrieve("campaignId");
```

## 更新活动计划

通过 `campaignId` 更新活动计划的属性。

`PUT /10dlc/campaign/{campaignId}`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignUpdateParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.TelnyxCampaignCsp;

TelnyxCampaignCsp telnyxCampaignCsp = client.messaging10dlc().campaign().update("campaignId");
```

## 关闭活动计划

终止活动计划。

`DELETE /10dlc/campaign/{campaignId}`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignDeactivateParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignDeactivateResponse;

CampaignDeactivateResponse response = client.messaging10dlc().campaign().deactivate("campaignId");
```

## 为被拒绝的活动计划提交申诉

为状态为 TELNYX_FAILED 或 MNO_REJECTED 的活动计划提交申诉。

`POST /10dlc/campaign/{campaignId}/appeal` — 必需参数：`appeal_reason`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignSubmitAppealParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignSubmitAppealResponse;

CampaignSubmitAppealParams params = CampaignSubmitAppealParams.builder()
    .campaignId("5eb13888-32b7-4cab-95e6-d834dde21d64")
    .appealReason("The website has been updated to include the required privacy policy and terms of service.")
    .build();
CampaignSubmitAppealResponse response = client.messaging10dlc().campaign().submitAppeal(params);
```

## 获取活动计划的 MNO 元数据

获取每个 MNO（移动网络运营商）的活动计划元数据。

`GET /10dlc/campaign/{campaignId}/mnoMetadata`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignGetMnoMetadataParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignGetMnoMetadataResponse;

CampaignGetMnoMetadataResponse response = client.messaging10dlc().campaign().getMnoMetadata("campaignId");
```

## 获取活动计划操作状态

检索活动计划在 MNO（移动网络运营商）层面的操作状态。

`GET /10dlc/campaign/{campaignId}/operationStatus`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignGetOperationStatusParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignGetOperationStatusResponse;

CampaignGetOperationStatusResponse response = client.messaging10dlc().campaign().getOperationStatus("campaignId");
```

## 获取 OSR 活动计划属性

`GET /10dlc/campaign/{campaignId}/osr_attributes`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.osr.OsrGetAttributesParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.osr.OsrGetAttributesResponse;

OsrGetAttributesResponse response = client.messaging10dlc().campaign().osr().getAttributes("campaignId");
```

## 获取共享状态

`GET /10dlc/campaign/{campaignId}/sharing`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignGetSharingStatusParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignGetSharingStatusResponse;

CampaignGetSharingStatusResponse response = client.messaging10dlc().campaign().getSharingStatus("campaignId");
```

## 接受共享的活动计划

手动接受与 Telnyx 共享的活动计划。

`POST /10dlc/campaign/acceptSharing/{campaignId}`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignAcceptSharingParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.CampaignAcceptSharingResponse;

CampaignAcceptSharingResponse response = client.messaging10dlc().campaign().acceptSharing("C26F1KLZN");
```

## 获取活动计划成本

`GET /10dlc/campaign/usecase_cost`

```java
import com.telnyx.sdk.models.messaging10dlc.campaign.usecase.UsecaseGetCostParams;
import com.telnyx.sdk.models.messaging10dlc.campaign.usecase.UsecaseGetCostResponse;

UsecaseGetCostParams params = UsecaseGetCostParams.builder()
    .usecase("usecase")
    .build();
UsecaseGetCostResponse response = client.messaging10dlc().campaign().usecase().getCost(params);
```

## 列出共享活动计划

分页方式检索您与 Telnyx 共享的所有活动计划。

`GET /10dlc/partner_campaigns`

```java
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignListPage;
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignListParams;

PartnerCampaignListPage page = client.messaging10dlc().partnerCampaigns().list();
```

## 获取单个共享活动计划

通过 `campaignId` 获取活动计划详细信息。

`GET /10dlc/partner_campaigns/{campaignId}`

```java
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignRetrieveParams;
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.TelnyxDownstreamCampaign;

TelnyxDownstreamCampaign telnyxDownstreamCampaign = client.messaging10dlc().partnerCampaigns().retrieve("campaignId");
```

## 更新单个共享活动计划

通过 `campaignId` 更新活动计划详细信息。

`PATCH /10dlc/partner_campaigns/{campaignId}`

```java
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignUpdateParams;
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.TelnyxDownstreamCampaign;

TelnyxDownstreamCampaign telnyxDownstreamCampaign = client.messaging10dlc().partnerCampaigns().update("campaignId");
```

## 获取共享状态

`GET /10dlc/partnerCampaign/{campaignId}/sharing`

```java
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignRetrieveSharingStatusParams;
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignRetrieveSharingStatusResponse;

PartnerCampaignRetrieveSharingStatusResponse response = client.messaging10dlc().partnerCampaigns().retrieveSharingStatus("campaignId");
```

## 列出共享的活动计划

分页方式获取您与 Telnyx 共享的所有活动计划

当前此端点仅返回 Telnyx 已接受的活动计划。

`GET /10dlc/partnerCampaign/sharedByMe`

```java
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignListSharedByMePage;
import com.telnyx.sdk.models.messaging10dlc.partnercampaigns.PartnerCampaignListSharedByMeParams;

PartnerCampaignListSharedByMePage page = client.messaging10dlc().partnerCampaigns().listSharedByMe();
```

## 列出电话号码活动计划

`GET /10dlc/phone_number_campaigns`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignListPage;
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignListParams;

PhoneNumberCampaignListPage page = client.messaging10dlc().phoneNumberCampaigns().list();
```

## 创建新的电话号码活动计划

`POST /10dlc/phone_number_campaigns` — 必需参数：`phoneNumber`, `campaignId`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaign;
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignCreate;
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignCreateParams;

PhoneNumberCampaignCreate params = PhoneNumberCampaignCreate.builder()
    .campaignId("4b300178-131c-d902-d54e-72d90ba1620j")
    .phoneNumber("+18005550199")
    .build();
PhoneNumberCampaign phoneNumberCampaign = client.messaging10dlc().phoneNumberCampaigns().create(params);
```

## 获取单个电话号码活动计划

通过 `phoneNumber` 获取特定的电话号码/活动计划关联信息。

`GET /10dlc/phone_number_campaigns/{phoneNumber}`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaign;
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignRetrieveParams;

PhoneNumberCampaign phoneNumberCampaign = client.messaging10dlc().phoneNumberCampaigns().retrieve("phoneNumber");
```

## 创建新的电话号码活动计划

`PUT /10dlc/phone_number_campaigns/{phoneNumber}` — 必需参数：`phoneNumber`, `campaignId`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaign;
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignCreate;
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignUpdateParams;

PhoneNumberCampaignUpdateParams params = PhoneNumberCampaignUpdateParams.builder()
    .campaignPhoneNumber("phoneNumber")
    .phoneNumberCampaignCreate(PhoneNumberCampaignCreate.builder()
        .campaignId("4b300178-131c-d902-d54e-72d90ba1620j")
        .phoneNumber("+18005550199")
        .build())
    .build();
PhoneNumberCampaign phoneNumberCampaign = client.messaging10dlc().phoneNumberCampaigns().update(params);
```

## 删除电话号码活动计划

此端点用于删除与指定 `phoneNumber` 关联的活动计划。

`DELETE /10dlc/phone_number_campaigns/{phoneNumber}`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaign;
import com.telnyx.sdk.models.messaging10dlc.phonenumbercampaigns.PhoneNumberCampaignDeleteParams;

PhoneNumberCampaign phoneNumberCampaign = client.messaging10dlc().phoneNumberCampaigns().delete("phoneNumber");
```

## 将消息配置文件分配给活动计划

此端点允许您将所有与消息配置文件关联的电话号码链接到活动计划。

`POST /10dlc/phoneNumberAssignmentByProfile` — 必需参数：`messagingProfileId`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumberassignmentbyprofile.PhoneNumberAssignmentByProfileAssignParams;
import com.telnyx.sdk.models.messaging10dlc.phonenumberassignmentbyprofile.PhoneNumberAssignmentByProfileAssignResponse;

PhoneNumberAssignmentByProfileAssignParams params = PhoneNumberAssignmentByProfileAssignParams.builder()
    .messagingProfileId("4001767e-ce0f-4cae-9d5f-0d5e636e7809")
    .build();
PhoneNumberAssignmentByProfileAssignResponse response = client.messaging10dlc().phoneNumberAssignmentByProfile().assign(params);
```

## 获取任务状态

检查将所有电话号码分配给活动计划的任务状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumberassignmentbyprofile.PhoneNumberAssignmentByProfileRetrieveStatusParams;
import com.telnyx.sdk.models.messaging10dlc.phonenumberassignmentbyprofile.PhoneNumberAssignmentByProfileRetrieveStatusResponse;

PhoneNumberAssignmentByProfileRetrieveStatusResponse response = client.messaging10dlc().phoneNumberAssignmentByProfile().retrieveStatus("taskId");
```

## 获取电话号码状态

检查与指定 `taskId` 关联的个别电话号码/活动计划分配的状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}/phoneNumbers`

```java
import com.telnyx.sdk.models.messaging10dlc.phonenumberassignmentbyprofile.PhoneNumberAssignmentByProfileListPhoneNumberStatusParams;
import com.telnyx.sdk.models.messaging10dlc.phonenumberassignmentbyprofile.PhoneNumberAssignmentByProfileListPhoneNumberStatusResponse;

PhoneNumberAssignmentByProfileListPhoneNumberStatusResponse response = client.messaging10dlc().phoneNumberAssignmentByProfile().listPhoneNumberStatus("taskId");
```

---

## Webhook

以下 Webhook 事件将发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `campaignStatusUpdate` | 活动计划状态更新 |
```
```