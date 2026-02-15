---
name: telnyx-numbers-compliance-go
description: >-
  Manage regulatory requirements, number bundles, supporting documents, and
  verified numbers for compliance. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: numbers-compliance
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字合规性 - Go

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

## 获取套餐信息

获取所有允许使用的套餐信息。

`GET /bundle_pricing/billing_bundles`

```go
	page, err := client.BundlePricing.BillingBundles.List(context.TODO(), telnyx.BundlePricingBillingBundleListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 根据 ID 获取套餐

根据 ID 获取单个套餐。

`GET /bundle_pricing/billing_bundles/{bundle_id}`

```go
	billingBundle, err := client.BundlePricing.BillingBundles.Get(
		context.TODO(),
		"8661948c-a386-4385-837f-af00f40f111a",
		telnyx.BundlePricingBillingBundleGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", billingBundle.Data)
```

## 获取用户套餐

获取用户套餐的分页列表。

`GET /bundle_pricing/user_bundles`

```go
	page, err := client.BundlePricing.UserBundles.List(context.TODO(), telnyx.BundlePricingUserBundleListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建用户套餐

为用户创建多个套餐。

`POST /bundle_pricing/user_bundles/bulk`

```go
	userBundle, err := client.BundlePricing.UserBundles.New(context.TODO(), telnyx.BundlePricingUserBundleNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", userBundle.Data)
```

## 获取未使用的用户套餐

返回所有未使用的用户套餐。

`GET /bundle_pricing/user_bundles/unused`

```go
	response, err := client.BundlePricing.UserBundles.ListUnused(context.TODO(), telnyx.BundlePricingUserBundleListUnusedParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 根据 ID 获取用户套餐

根据 ID 获取用户套餐。

`GET /bundle_pricing/user_bundles/{user_bundle_id}`

```go
	userBundle, err := client.BundlePricing.UserBundles.Get(
		context.TODO(),
		"ca1d2263-d1f1-43ac-ba53-248e7a4bb26a",
		telnyx.BundlePricingUserBundleGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", userBundle.Data)
```

## 取消激活用户套餐

根据 ID 取消激活用户套餐。

`DELETE /bundle_pricing/user_bundles/{user_bundle_id}`

```go
	response, err := client.BundlePricing.UserBundles.Deactivate(
		context.TODO(),
		"ca1d2263-d1f1-43ac-ba53-248e7a4bb26a",
		telnyx.BundlePricingUserBundleDeactivateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取用户套餐资源

根据 ID 获取用户套餐的资源信息。

`GET /bundle_pricing/user_bundles/{user_bundle_id}/resources`

```go
	response, err := client.BundlePricing.UserBundles.ListResources(
		context.TODO(),
		"ca1d2263-d1f1-43ac-ba53-248e7a4bb26a",
		telnyx.BundlePricingUserBundleListResourcesParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有文档链接

按创建时间降序列出所有文档链接。

`GET /document_links`

```go
	page, err := client.DocumentLinks.List(context.TODO(), telnyx.DocumentLinkListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出所有文档

按创建时间降序列出所有文档。

`GET /documents`

```go
	page, err := client.Documents.List(context.TODO(), telnyx.DocumentListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 上传文档

上传文档。<br /><br />上传的文件必须在 30 分钟内关联到某个服务，否则将被自动删除。

`POST /documents`

```go
	response, err := client.Documents.UploadJson(context.TODO(), telnyx.DocumentUploadJsonParams{
		Document: telnyx.DocumentUploadJsonParamsDocument{},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取文档

获取文档内容。

`GET /documents/{id}`

```go
	document, err := client.Documents.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", document.Data)
```

## 更新文档

更新文档内容。

`PATCH /documents/{id}`

```go
	document, err := client.Documents.Update(
		context.TODO(),
		"6a09cdc3-8948-47f0-aa62-74ac943d6c58",
		telnyx.DocumentUpdateParams{
			DocServiceDocument: telnyx.DocServiceDocumentParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", document.Data)
```

## 删除文档

删除文档。<br /><br />只有未关联到服务的文档才能被删除。

`DELETE /documents/{id}`

```go
	document, err := client.Documents.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", document.Data)
```

## 下载文档

下载文档内容。

`GET /documents/{id}/download`

```go
	response, err := client.Documents.Download(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 生成文档的临时下载链接

生成一个临时预签名链接，可以直接从存储后端下载文档，无需身份验证。

`GET /documents/{id}/download_link`

```go
	response, err := client.Documents.GenerateDownloadLink(context.TODO(), "550e8400-e29b-41d4-a716-446655440000")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有需求

支持过滤、排序和分页功能，列出所有需求。

`GET /requirements`

```go
	page, err := client.Requirements.List(context.TODO(), telnyx.RequirementListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取需求记录

获取单个需求记录。

`GET /requirements/{id}`

```go
	requirement, err := client.Requirements.Get(context.TODO(), "a9dad8d5-fdbd-49d7-aa23-39bb08a5ebaa")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirement.Data)
```

## 列出所有需求类型

按创建时间降序列出所有需求类型。

`GET /requirement_types`

```go
	requirementTypes, err := client.RequirementTypes.List(context.TODO(), telnyx.RequirementTypeListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementTypes.Data)
```

## 根据 ID 获取需求类型

根据 ID 获取特定需求类型。

`GET /requirement_types/{id}`

```go
	requirementType, err := client.RequirementTypes.Get(context.TODO(), "a38c217a-8019-48f8-bff6-0fdd9939075b")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementType.Data)
```

## 获取监管要求

获取所有监管要求信息。

`GET /regulatory_requirements`

```go
	regulatoryRequirement, err := client.RegulatoryRequirements.Get(context.TODO(), telnyx.RegulatoryRequirementGetParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", regulatoryRequirement.Data)
```

## 列出需求组

列出所有需求组。

`GET /requirement_groups`

```go
	requirementGroups, err := client.RequirementGroups.List(context.TODO(), telnyx.RequirementGroupListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementGroups)
```

## 创建新的需求组

创建新的需求组。<br />必填参数：`country_code`、`phone_number_type`、`action`

```go
	requirementGroup, err := client.RequirementGroups.New(context.TODO(), telnyx.RequirementGroupNewParams{
		Action:          telnyx.RequirementGroupNewParamsActionOrdering,
		CountryCode:     "US",
		PhoneNumberType: telnyx.RequirementGroupNewParamsPhoneNumberTypeLocal,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementGroup.ID)
```

## 根据 ID 获取需求组

根据 ID 获取单个需求组。

`GET /requirement_groups/{id}`

```go
	requirementGroup, err := client.RequirementGroups.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementGroup.ID)
```

## 更新需求组中的需求值

更新需求组中的需求值。

`PATCH /requirement_groups/{id}`

```go
	requirementGroup, err := client.RequirementGroups.Update(
		context.TODO(),
		"id",
		telnyx.RequirementGroupUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementGroup.ID)
```

## 根据 ID 删除需求组

根据 ID 删除需求组。

`DELETE /requirement_groups/{id}`

```go
	requirementGroup, err := client.RequirementGroups.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementGroup.ID)
```

## 提交需求组以供审批

提交需求组以供审批。

`POST /requirement_groups/{id}/submit_for_approval`

```go
	requirementGroup, err := client.RequirementGroups.SubmitForApproval(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", requirementGroup.ID)
```

## 列出所有已验证的号码

获取已验证号码的分页列表。

`GET /verified_numbers`

```go
	page, err := client.VerifiedNumbers.List(context.TODO(), telnyx.VerifiedNumberListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 请求电话号码验证

启动电话号码验证流程。

`POST /verified_numbers` — 必填参数：`phone_number`、`verification_method`

```go
	verifiedNumber, err := client.VerifiedNumbers.New(context.TODO(), telnyx.VerifiedNumberNewParams{
		PhoneNumber:        "+15551234567",
		VerificationMethod: telnyx.VerifiedNumberNewParamsVerificationMethodSMS,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifiedNumber.PhoneNumber)
```

## 获取已验证的号码

获取已验证的号码信息。

`GET /verified_numbers/{phone_number}`

```go
	verifiedNumberDataWrapper, err := client.VerifiedNumbers.Get(context.TODO(), "+15551234567")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifiedNumberDataWrapper.Data)
```

## 删除已验证的号码

删除已验证的号码。

`DELETE /verified_numbers/{phone_number}`

```go
	verifiedNumberDataWrapper, err := client.VerifiedNumbers.Delete(context.TODO(), "+15551234567")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifiedNumberDataWrapper.Data)
```

## 提交验证码

提交验证码。

`POST /verified_numbers/{phone_number}/actions/verify` — 必填参数：`verification_code`

```go
	verifiedNumberDataWrapper, err := client.VerifiedNumbers.Actions.SubmitVerificationCode(
		context.TODO(),
		"+15551234567",
		telnyx.VerifiedNumberActionSubmitVerificationCodeParams{
			VerificationCode: "123456",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", verifiedNumberDataWrapper.Data)
```