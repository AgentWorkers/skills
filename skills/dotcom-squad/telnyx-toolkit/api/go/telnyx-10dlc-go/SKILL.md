---
name: telnyx-10dlc-go
description: >-
  Register brands and campaigns for 10DLC (10-digit long code) A2P messaging
  compliance in the US. Manage campaign assignments to phone numbers. This skill
  provides Go SDK examples.
metadata:
  author: telnyx
  product: 10dlc
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 |

# Telnyx 10Dlc - Go

## 安装

```bash
go get github.com/team-telnyx/telnyx-go
```

## 设置

```go
import (
  "context"
  "fmt"
  "os"

  "github.com/team-telnyx/telnyx-go"
  "github.com/team-telnyx/telnyx-go/option"
)

client := telnyx.NewClient(
  option.WithAPIKey(os.Getenv("TELNYX_API_KEY")),
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出品牌

此端点用于列出与您的组织关联的所有品牌。

`GET /10dlc/brand`

```go
	page, err := client.Messaging10dlc.Brand.List(context.TODO(), telnyx.Messaging10dlcBrandListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建品牌

此端点用于创建新品牌。

`POST /10dlc/brand` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```go
	telnyxBrand, err := client.Messaging10dlc.Brand.New(context.TODO(), telnyx.Messaging10dlcBrandNewParams{
		Country:     "US",
		DisplayName: "ABC Mobile",
		Email:       "email",
		EntityType:  telnyx.EntityTypePrivateProfit,
		Vertical:    telnyx.VerticalTechnology,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxBrand.IdentityStatus)
```

## 获取品牌信息

通过 `brandId` 获取品牌信息。

`GET /10dlc/brand/{brandId}`

```go
	brand, err := client.Messaging10dlc.Brand.Get(context.TODO(), "brandId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", brand)
```

## 更新品牌信息

通过 `brandId` 更新品牌属性。

`PUT /10dlc/brand/{brandId}` — 必需参数：`entityType`, `displayName`, `country`, `email`, `vertical`

```go
	telnyxBrand, err := client.Messaging10dlc.Brand.Update(
		context.TODO(),
		"brandId",
		telnyx.Messaging10dlcBrandUpdateParams{
			Country:     "US",
			DisplayName: "ABC Mobile",
			Email:       "email",
			EntityType:  telnyx.EntityTypePrivateProfit,
			Vertical:    telnyx.VerticalTechnology,
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxBrand.IdentityStatus)
```

## 删除品牌

删除品牌。

`DELETE /10dlc/brand/{brandId}`

```go
	err := client.Messaging10dlc.Brand.Delete(context.TODO(), "brandId")
	if err != nil {
		panic(err.Error())
	}
```

## 重新发送品牌 2FA 邮件

`POST /10dlc/brand/{brandId}/2faEmail`

```go
	err := client.Messaging10dlc.Brand.Resend2faEmail(context.TODO(), "brandId")
	if err != nil {
		panic(err.Error())
	}
```

## 获取品牌的外部审核记录

获取指定品牌的有效外部审核记录列表。

`GET /10dlc/brand/{brandId}/externalVetting`

```go
	externalVettings, err := client.Messaging10dlc.Brand.ExternalVetting.List(context.TODO(), "brandId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", externalVettings)
```

## 请求品牌的外部审核

为品牌请求新的外部审核。

`POST /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingClass`

```go
	response, err := client.Messaging10dlc.Brand.ExternalVetting.Order(
		context.TODO(),
		"brandId",
		telnyx.Messaging10dlcBrandExternalVettingOrderParams{
			EvpID:        "evpId",
			VettingClass: "vettingClass",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.CreateDate)
```

## 导入外部审核记录

此操作可用于从 TCR 批准的审核提供商导入外部审核记录。

`PUT /10dlc/brand/{brandId}/externalVetting` — 必需参数：`evpId`, `vettingId`

```go
	response, err := client.Messaging10dlc.Brand.ExternalVetting.Imports(
		context.TODO(),
		"brandId",
		telnyx.Messaging10dlcBrandExternalVettingImportsParams{
			EvpID:     "evpId",
			VettingID: "vettingId",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.CreateDate)
```

## 取消品牌审核

此操作允许您取消品牌审核。

`PUT /10dlc/brand/{brandId}/revet`

```go
	telnyxBrand, err := client.Messaging10dlc.Brand.Revet(context.TODO(), "brandId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxBrand.IdentityStatus)
```

## 通过品牌 ID 获取品牌 SMS OTP 状态

使用品牌 ID 查询 SMS OTP（一次性密码）的状态（用于个体经营者品牌验证）。

`GET /10dlc/brand/{brandId}/smsOtp`

```go
	response, err := client.Messaging10dlc.Brand.GetSMSOtpStatus(context.TODO(), "4b20019b-043a-78f8-0657-b3be3f4b4002")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.BrandID)
```

## 触发品牌 SMS OTP

触发或重新触发品牌验证的 SMS OTP（一次性密码）。

`POST /10dlc/brand/{brandId}/smsOtp` — 必需参数：`pinSms`, `successSms`

```go
	response, err := client.Messaging10dlc.Brand.TriggerSMSOtp(
		context.TODO(),
		"4b20019b-043a-78f8-0657-b3be3f4b4002",
		telnyx.Messaging10dlcBrandTriggerSMSOtpParams{
			PinSMS:     "Your PIN is @OTP_PIN@",
			SuccessSMS: "Verification successful!",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.BrandID)
```

## 验证品牌 SMS OTP

验证用于个体经营者品牌验证的 SMS OTP（一次性密码）。

`PUT /10dlc/brand/{brandId}/smsOtp` — 必需参数：`otpPin`

```go
	err := client.Messaging10dlc.Brand.VerifySMSOtp(
		context.TODO(),
		"4b20019b-043a-78f8-0657-b3be3f4b4002",
		telnyx.Messaging10dlcBrandVerifySMSOtpParams{
			OtpPin: "123456",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 通过 ID 获取品牌反馈

通过 ID 获取关于品牌的反馈信息。

`GET /10dlc/brand_feedback/{brandId}`

```go
	response, err := client.Messaging10dlc.Brand.GetFeedback(context.TODO(), "brandId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.BrandID)
```

## 提交活动计划

在创建活动计划之前，请使用 [按用例筛选端点](https://developers.telnyx.com/api-reference/campaign/qualify-by-usecase) 确保您想要分配新活动计划的品牌符合要求...

`POST /10dlc/campaignBuilder` — 必需参数：`brandId`, `description`, `usecase`

```go
	telnyxCampaignCsp, err := client.Messaging10dlc.CampaignBuilder.Submit(context.TODO(), telnyx.Messaging10dlcCampaignBuilderSubmitParams{
		BrandID:     "brandId",
		Description: "description",
		Usecase:     "usecase",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxCampaignCsp.BrandID)
```

## 按用例筛选

此端点用于判断提供的品牌是否适合您的活动计划用例。

`GET /10dlc/campaignBuilder/brand/{brandId}/usecase/{usecase}`

```go
	response, err := client.Messaging10dlc.CampaignBuilder.Brand.QualifyByUsecase(
		context.TODO(),
		"usecase",
		telnyx.Messaging10dlcCampaignBuilderBrandQualifyByUsecaseParams{
			BrandID: "brandId",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AnnualFee)
```

## 列出活动计划

检索与指定 `brandId` 关联的所有活动计划。

`GET /10dlc/campaign`

```go
	page, err := client.Messaging10dlc.Campaign.List(context.TODO(), telnyx.Messaging10dlcCampaignListParams{
		BrandID: "brandId",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取活动计划详情

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/campaign/{campaignId}`

```go
	telnyxCampaignCsp, err := client.Messaging10dlc.Campaign.Get(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxCampaignCsp.BrandID)
```

## 更新活动计划

通过 `campaignId` 更新活动计划的属性。

`PUT /10dlc/campaign/{campaignId}`

```go
	telnyxCampaignCsp, err := client.Messaging10dlc.Campaign.Update(
		context.TODO(),
		"campaignId",
		telnyx.Messaging10dlcCampaignUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxCampaignCsp.BrandID)
```

## 关闭活动计划

终止活动计划。

`DELETE /10dlc/campaign/{campaignId}`

```go
	response, err := client.Messaging10dlc.Campaign.Deactivate(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Time)
```

## 为被拒绝的活动计划提交申诉

为状态为 TELNYX_FAILED 或 MNO_REJECTED 的活动计划提交申诉。

`POST /10dlc/campaign/{campaignId}/appeal` — 必需参数：`appeal_reason`

```go
	response, err := client.Messaging10dlc.Campaign.SubmitAppeal(
		context.TODO(),
		"5eb13888-32b7-4cab-95e6-d834dde21d64",
		telnyx.Messaging10dlcCampaignSubmitAppealParams{
			AppealReason: "The website has been updated to include the required privacy policy and terms of service.",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.AppealedAt)
```

## 获取活动计划的 MNO 元数据

获取每个活动计划对应的 MNO（移动网络运营商）元数据。

`GET /10dlc/campaign/{campaignId}/mnoMetadata`

```go
	response, err := client.Messaging10dlc.Campaign.GetMnoMetadata(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Number10999)
```

## 获取活动计划的操作状态

检索活动计划在 MNO 级别的操作状态。

`GET /10dlc/campaign/{campaignId}/operationStatus`

```go
	response, err := client.Messaging10dlc.Campaign.GetOperationStatus(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 获取 OSR 活动计划属性

`GET /10dlc/campaign/{campaignId}/osr_attributes`

```go
	response, err := client.Messaging10dlc.Campaign.Osr.GetAttributes(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 获取共享状态

`GET /10dlc/campaign/{campaignId}/sharing`

```go
	response, err := client.Messaging10dlc.Campaign.GetSharingStatus(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.SharedByMe)
```

## 接受共享的活动计划

手动接受与 Telnyx 共享的活动计划。

`POST /10dlc/campaign/acceptSharing/{campaignId}`

```go
	response, err := client.Messaging10dlc.Campaign.AcceptSharing(context.TODO(), "C26F1KLZN")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 获取活动计划成本

`GET /10dlc/campaign/usecase_cost`

```go
	response, err := client.Messaging10dlc.Campaign.Usecase.GetCost(context.TODO(), telnyx.Messaging10dlcCampaignUsecaseGetCostParams{
		Usecase: "usecase",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.CampaignUsecase)
```

## 列出共享的活动计划

分页方式获取您与 Telnyx 共享的所有活动计划。

`GET /10dlc/partner_campaigns`

```go
	page, err := client.Messaging10dlc.PartnerCampaigns.List(context.TODO(), telnyx.Messaging10dlcPartnerCampaignListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取单个共享活动计划

通过 `campaignId` 获取活动计划详情。

`GET /10dlc/partner_campaigns/{campaignId}`

```go
	telnyxDownstreamCampaign, err := client.Messaging10dlc.PartnerCampaigns.Get(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxDownstreamCampaign.TcrBrandID)
```

## 更新单个共享活动计划

通过 `campaignId` 更新活动计划详情。

`PATCH /10dlc/partner_campaigns/{campaignId}`

```go
	telnyxDownstreamCampaign, err := client.Messaging10dlc.PartnerCampaigns.Update(
		context.TODO(),
		"campaignId",
		telnyx.Messaging10dlcPartnerCampaignUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", telnyxDownstreamCampaign.TcrBrandID)
```

## 获取共享状态

`GET /10dlc/partnerCampaign/{campaignId}/sharing`

```go
	response, err := client.Messaging10dlc.PartnerCampaigns.GetSharingStatus(context.TODO(), "campaignId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 列出共享的活动计划

分页方式获取您与 Telnyx 共享的所有活动计划

此端点目前仅返回 Telnyx 已接受的活动计划。

`GET /10dlc/partnerCampaign/sharedByMe`

```go
	page, err := client.Messaging10dlc.PartnerCampaigns.ListSharedByMe(context.TODO(), telnyx.Messaging10dlcPartnerCampaignListSharedByMeParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出电话号码活动计划

`GET /10dlc/phone_number_campaigns`

```go
	page, err := client.Messaging10dlc.PhoneNumberCampaigns.List(context.TODO(), telnyx.Messaging10dlcPhoneNumberCampaignListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的电话号码活动计划

`POST /10dlc/phone_number_campaigns` — 必需参数：`phoneNumber`, `campaignId`

```go
	phoneNumberCampaign, err := client.Messaging10dlc.PhoneNumberCampaigns.New(context.TODO(), telnyx.Messaging10dlcPhoneNumberCampaignNewParams{
		PhoneNumberCampaignCreate: telnyx.PhoneNumberCampaignCreateParam{
			CampaignID:  "4b300178-131c-d902-d54e-72d90ba1620j",
			PhoneNumber: "+18005550199",
		},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberCampaign.CampaignID)
```

## 获取单个电话号码活动计划详情

通过 `phoneNumber` 获取特定的电话号码/活动计划关联信息。

`GET /10dlc/phone_number_campaigns/{phoneNumber}`

```go
	phoneNumberCampaign, err := client.Messaging10dlc.PhoneNumberCampaigns.Get(context.TODO(), "phoneNumber")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberCampaign.CampaignID)
```

## 创建新的电话号码活动计划

`PUT /10dlc/phone_number_campaigns/{phoneNumber}` — 必需参数：`phoneNumber`, `campaignId`

```go
	phoneNumberCampaign, err := client.Messaging10dlc.PhoneNumberCampaigns.Update(
		context.TODO(),
		"phoneNumber",
		telnyx.Messaging10dlcPhoneNumberCampaignUpdateParams{
			PhoneNumberCampaignCreate: telnyx.PhoneNumberCampaignCreateParam{
				CampaignID:  "4b300178-131c-d902-d54e-72d90ba1620j",
				PhoneNumber: "+18005550199",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberCampaign.CampaignID)
```

## 删除电话号码活动计划

此端点用于删除与指定 `phoneNumber` 关联的活动计划。

`DELETE /10dlc/phone_number_campaigns/{phoneNumber}`

```go
	phoneNumberCampaign, err := client.Messaging10dlc.PhoneNumberCampaigns.Delete(context.TODO(), "phoneNumber")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberCampaign.CampaignID)
```

## 将消息配置文件分配给活动计划

此端点允许您将所有与消息配置文件关联的电话号码链接到活动计划。

`POST /10dlc/phoneNumberAssignmentByProfile` — 必需参数：`messagingProfileId`

```go
	response, err := client.Messaging10dlc.PhoneNumberAssignmentByProfile.Assign(context.TODO(), telnyx.Messaging10dlcPhoneNumberAssignmentByProfileAssignParams{
		MessagingProfileID: "4001767e-ce0f-4cae-9d5f-0d5e636e7809",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.MessagingProfileID)
```

## 获取任务状态

检查将所有电话号码分配给活动计划的任务状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}`

```go
	response, err := client.Messaging10dlc.PhoneNumberAssignmentByProfile.GetStatus(context.TODO(), "taskId")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Status)
```

## 获取电话号码状态

检查与指定 `taskId` 关联的个别电话号码/活动计划分配的状态。

`GET /10dlc/phoneNumberAssignmentByProfile/{taskId}/phoneNumbers`

```go
	response, err := client.Messaging10dlc.PhoneNumberAssignmentByProfile.ListPhoneNumberStatus(
		context.TODO(),
		"taskId",
		telnyx.Messaging10dlcPhoneNumberAssignmentByProfileListPhoneNumberStatusParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Records)
```

---

## Webhook

以下 Webhook 事件将发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `campaignStatusUpdate` | 活动计划状态更新 |
```
```