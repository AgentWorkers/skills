---
name: telnyx-porting-in-go
description: >-
  Port phone numbers into Telnyx. Check portability, create port orders, upload
  LOA documents, and track porting status. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: porting-in
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 的端口迁移功能（Go 语言实现）

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

## 列出所有端口迁移事件

返回所有端口迁移事件的列表。

`GET /porting/events`

```go
	page, err := client.Porting.Events.List(context.TODO(), telnyx.PortingEventListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 显示单个端口迁移事件

显示特定的端口迁移事件。

`GET /porting/events/{id}`

```go
	event, err := client.Porting.Events.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", event.Data)
```

## 重新发布端口迁移事件

重新发布特定的端口迁移事件。

`POST /porting/events/{id}/republish`

```go
	err := client.Porting.Events.Republish(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 预览 LOA（Letter of Authorization）配置参数

无需创建 LOA 配置即可预览其模板。

`POST /porting/loa_configuration_preview`

```go
	response, err := client.Porting.LoaConfigurations.Preview0(context.TODO(), telnyx.PortingLoaConfigurationPreview0Params{
		Address: telnyx.PortingLoaConfigurationPreview0ParamsAddress{
			City:          "Austin",
			CountryCode:   "US",
			State:         "TX",
			StreetAddress: "600 Congress Avenue",
			ZipCode:       "78701",
		},
		CompanyName: "Telnyx",
		Contact: telnyx.PortingLoaConfigurationPreview0ParamsContact{
			Email:       "testing@telnyx.com",
			PhoneNumber: "+12003270001",
		},
		Logo: telnyx.PortingLoaConfigurationPreview0ParamsLogo{
			DocumentID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
		Name: "My LOA Configuration",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 列出 LOA 配置

列出所有的 LOA 配置。

`GET /porting/loa_configurations`

```go
	page, err := client.Porting.LoaConfigurations.List(context.TODO(), telnyx.PortingLoaConfigurationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 LOA 配置

创建一个新的 LOA 配置。

`POST /porting/loa_configurations`

```go
	loaConfiguration, err := client.Porting.LoaConfigurations.New(context.TODO(), telnyx.PortingLoaConfigurationNewParams{
		Address: telnyx.PortingLoaConfigurationNewParamsAddress{
			City:          "Austin",
			CountryCode:   "US",
			State:         "TX",
			StreetAddress: "600 Congress Avenue",
			ZipCode:       "78701",
		},
		CompanyName: "Telnyx",
		Contact: telnyx.PortingLoaConfigurationNewParamsContact{
			Email:       "testing@telnyx.com",
			PhoneNumber: "+12003270001",
		},
		Logo: telnyx.PortingLoaConfigurationNewParamsLogo{
			DocumentID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
		Name: "My LOA Configuration",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", loaConfiguration.Data)
```

## 检索 LOA 配置

检索特定的 LOA 配置。

`GET /porting/loa_configurations/{id}`

```go
	loaConfiguration, err := client.Porting.LoaConfigurations.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", loaConfiguration.Data)
```

## 更新 LOA 配置

更新特定的 LOA 配置。

`PATCH /porting/loa_configurations/{id}`

```go
	loaConfiguration, err := client.Porting.LoaConfigurations.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingLoaConfigurationUpdateParams{
			Address: telnyx.PortingLoaConfigurationUpdateParamsAddress{
				City:          "Austin",
				CountryCode:   "US",
				State:         "TX",
				StreetAddress: "600 Congress Avenue",
				ZipCode:       "78701",
			},
			CompanyName: "Telnyx",
			Contact: telnyx.PortingLoaConfigurationUpdateParamsContact{
				Email:       "testing@telnyx.com",
				PhoneNumber: "+12003270001",
			},
			Logo: telnyx.PortingLoaConfigurationUpdateParamsLogo{
				DocumentID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
			},
			Name: "My LOA Configuration",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", loaConfiguration.Data)
```

## 删除 LOA 配置

删除特定的 LOA 配置。

`DELETE /porting/loa_configurations/{id}`

```go
	err := client.Porting.LoaConfigurations.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 预览 LOA 配置

预览特定的 LOA 配置。

`GET /porting/loa_configurations/{id}/preview`

```go
	response, err := client.Porting.LoaConfigurations.Preview1(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 列出所有端口迁移订单

返回所有端口迁移订单的列表。

`GET /porting_orders`

```go
	page, err := client.PortingOrders.List(context.TODO(), telnyx.PortingOrderListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建端口迁移订单

创建一个新的端口迁移订单。

`POST /porting_orders` — 必需参数：`phone_numbers`

```go
	portingOrder, err := client.PortingOrders.New(context.TODO(), telnyx.PortingOrderNewParams{
		PhoneNumbers: []string{"+13035550000", "+13035550001", "+13035550002"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", portingOrder.Data)
```

## 检索端口迁移订单

检索现有端口迁移订单的详细信息。

`GET /porting_orders/{id}`

```go
	portingOrder, err := client.PortingOrders.Get(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderGetParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", portingOrder.Data)
```

## 修改端口迁移订单

修改现有端口迁移订单的详细信息。

`PATCH /porting_orders/{id}`

```go
	portingOrder, err := client.PortingOrders.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", portingOrder.Data)
```

## 删除端口迁移订单

删除现有的端口迁移订单。

`DELETE /porting_orders/{id}`

```go
	err := client.PortingOrders.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 异步激活端口迁移订单中的每个号码

异步激活端口迁移订单中的每个号码。

`POST /porting_orders/{id}/actions/activate`

```go
	response, err := client.PortingOrders.Actions.Activate(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 取消端口迁移订单

取消端口迁移订单。

`POST /porting_orders/{id}/actions/cancel`

```go
	response, err := client.PortingOrders.Actions.Cancel(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 提交端口迁移订单

确认并提交端口迁移订单。

`POST /porting_orders/{id}/actions/confirm`

```go
	response, err := client.PortingOrders.Actions.Confirm(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 共享端口迁移订单

为端口迁移订单创建共享令牌。

`POST /porting_orders/{id}/actions/share`

```go
	response, err := client.PortingOrders.Actions.Share(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderActionShareParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有端口迁移激活任务

返回所有端口迁移激活任务的列表。

`GET /porting/orders/{id}/activation_jobs`

```go
	page, err := client.PortingOrders.ActivationJobs.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderActivationJobListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 检索端口迁移激活任务

检索特定的端口迁移激活任务。

`GET /porting/orders/{id}/activation_jobs/{activationJobId}`

```go
	activationJob, err := client.PortingOrders.ActivationJobs.Get(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderActivationJobGetParams{
			ID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", activationJob.Data)
```

## 更新端口迁移激活任务

更新端口迁移激活任务的激活时间。

`PATCH /porting/orders/{id}/activation_jobs/{activationJobId}`

```go
	activationJob, err := client.PortingOrders.ActivationJobs.Update(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderActivationJobUpdateParams{
			ID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", activationJob.Data)
```

## 列出所有附加文档

返回端口迁移订单的所有附加文档的列表。

`GET /porting/orders/{id}/additional_documents`

```go
	page, err := client.PortingOrders.AdditionalDocuments.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderAdditionalDocumentListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建附加文档列表

为端口迁移订单创建附加文档的列表。

`POST /porting/orders/{id}/additional_documents`

```go
	additionalDocument, err := client.PortingOrders.AdditionalDocuments.New(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderAdditionalDocumentNewParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", additionalDocument.Data)
```

## 删除附加文档

删除端口迁移订单中的附加文档。

`DELETE /porting/orders/{id}/additional_documents/{additional_document_id}`

```go
	err := client.PortingOrders.AdditionalDocuments.Delete(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderAdditionalDocumentDeleteParams{
			ID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 列出允许的 FOC（Free of Charge）日期

返回端口迁移订单允许的 FOC 日期列表。

`GET /porting/orders/{id}/allowed_foc_windows`

```go
	response, err := client.PortingOrders.GetAllowedFocWindows(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出端口迁移订单的所有评论

返回端口迁移订单的所有评论列表。

`GET /porting/orders/{id}/comments`

```go
	page, err := client.PortingOrders.Comments.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderCommentListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 为端口迁移订单创建评论

为端口迁移订单创建新的评论。

`POST /porting/orders/{id}/comments`

```go
	comment, err := client.PortingOrders.Comments.New(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderCommentNewParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", comment.Data)
```

## 下载端口迁移订单的 LOA 模板

下载端口迁移订单的 LOA 模板。

`GET /porting/orders/{id}/loa_template`

```go
	response, err := client.PortingOrders.GetLoaTemplate(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderGetLoaTemplateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response)
```

## 列出端口迁移订单的需求

根据国家/号码类型返回该订单的所有需求列表。

`GET /porting/orders/{id}/requirements`

```go
	page, err := client.PortingOrders.GetRequirements(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderGetRequirementsParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 检索关联的 V1 子请求 ID 和端口请求 ID

检索与端口迁移订单关联的 V1 子请求 ID 和端口请求 ID。

`GET /porting/orders/{id}/sub_request`

```go
	response, err := client.PortingOrders.GetSubRequest(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出验证码

返回端口迁移订单的所有验证码列表。

`GET /porting/orders/{id}/verification_codes`

```go
	page, err := client.PortingOrders.VerificationCodes.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderVerificationCodeListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 发送验证码

为所有端口迁移号码发送验证码。

`POST /porting/orders/{id}/verification_codes/send`

```go
	err := client.PortingOrders.VerificationCodes.Send(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderVerificationCodeSendParams{},
	)
	if err != nil {
		panic(err.Error())
	}
```

## 验证一组号码的验证码

验证一组号码的验证码。

`POST /porting/orders/{id}/verification_codes/verify`

```go
	response, err := client.PortingOrders.VerificationCodes.Verify(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderVerificationCodeVerifyParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出端口迁移订单的动作需求

返回特定端口迁移订单的所有动作需求列表。

`GET /porting_orders/{porting_order_id}/action_requirements`

```go
	page, err := client.PortingOrders.ActionRequirements.List(
		context.TODO(),
		"porting_order_id",
		telnyx.PortingOrderActionRequirementListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 启动动作需求

为特定端口迁移订单启动一个动作需求。

`POST /porting/orders/{porting_order_id}/action_requirements/{id}/initiate`

```go
	response, err := client.PortingOrders.ActionRequirements.Initiate(
		context.TODO(),
		"id",
		telnyx.PortingOrderActionRequirementInitiateParams{
			PortingOrderID: "porting_order_id",
			Params: telnyx.PortingOrderActionRequirementInitiateParamsParams{
				FirstName: "John",
				LastName:  "Doe",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有关联的号码

返回与端口迁移订单关联的所有号码列表。

`GET /porting_orders/{id}/associated_phone_numbers`

```go
	page, err := client.PortingOrders.AssociatedPhoneNumbers.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderAssociatedPhoneNumberListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建关联号码

为端口迁移订单创建新的关联号码。

`POST /porting_orders/{id}/associated_phone_numbers`

```go
	associatedPhoneNumber, err := client.PortingOrders.AssociatedPhoneNumbers.New(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderAssociatedPhoneNumberNewParams{
			Action:           telnyx.PortingOrderAssociatedPhoneNumberNewParamsActionKeep,
			PhoneNumberRange: telnyx.PortingOrderAssociatedPhoneNumberNewParamsPhoneNumberRange{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", associatedPhoneNumber.Data)
```

## 删除关联号码

从端口迁移订单中删除关联号码。

`DELETE /porting_orders/{id}/associated_phone_numbers/{id}`

```go
	associatedPhoneNumber, err := client.PortingOrders.AssociatedPhoneNumbers.Delete(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderAssociatedPhoneNumberDeleteParams{
			PortingOrderID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", associatedPhoneNumber.Data)
```

## 列出所有号码块

返回端口迁移订单的所有号码块列表。

`GET /porting_orders/{id}/phone_number_blocks`

```go
	page, err := client.PortingOrders.PhoneNumberBlocks.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderPhoneNumberBlockListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建号码块

为端口迁移订单创建新的号码块。

`POST /porting_orders/{id}/phone_number_blocks`

```go
	phoneNumberBlock, err := client.PortingOrders.PhoneNumberBlocks.New(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderPhoneNumberBlockNewParams{
			ActivationRanges: []telnyx.PortingOrderPhoneNumberBlockNewParamsActivationRange{{
				EndAt:   "+4930244999910",
				StartAt: "+4930244999901",
			}},
			PhoneNumberRange: telnyx.PortingOrderPhoneNumberBlockNewParamsPhoneNumberRange{
				EndAt:   "+4930244999910",
				StartAt: "+4930244999901",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberBlock.Data)
```

## 删除号码块

删除号码块。

`DELETE /porting_orders/{id}/phone_number_blocks/{id}`

```go
	phoneNumberBlock, err := client.PortingOrders.PhoneNumberBlocks.Delete(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderPhoneNumberBlockDeleteParams{
			PortingOrderID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberBlock.Data)
```

## 列出所有号码扩展码

返回端口迁移订单的所有号码扩展码列表。

`GET /porting_orders/{id}/phone_number_extensions`

```go
	page, err := client.PortingOrders.PhoneNumberExtensions.List(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderPhoneNumberExtensionListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建号码扩展码

为端口迁移订单创建新的号码扩展码。

`POST /porting_orders/{id}/phone_number_extensions`

```go
	phoneNumberExtension, err := client.PortingOrders.PhoneNumberExtensions.New(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderPhoneNumberExtensionNewParams{
			ActivationRanges: []telnyx.PortingOrderPhoneNumberExtensionNewParamsActivationRange{{
				EndAt:   10,
				StartAt: 1,
			}},
			ExtensionRange: telnyx.PortingOrderPhoneNumberExtensionNewParamsExtensionRange{
				EndAt:   10,
				StartAt: 1,
			},
			PortingPhoneNumberID: "f24151b6-3389-41d3-8747-7dd8c681e5e2",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberExtension.Data)
```

## 删除号码扩展码

删除号码扩展码。

`DELETE /porting_orders/{id}/phone_number_extensions/{id}`

```go
	phoneNumberExtension, err := client.PortingOrders.PhoneNumberExtensions.Delete(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortingOrderPhoneNumberExtensionDeleteParams{
			PortingOrderID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberExtension.Data)
```

## 列出所有可能的异常类型

返回端口迁移订单的所有可能异常类型列表。

`GET /porting_orders/exception_types`

```go
	response, err := client.PortingOrders.GetExceptionTypes(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有号码配置

分页显示端口迁移订单的所有号码配置。

`GET /porting/orders/phone_number_configurations`

```go
	page, err := client.PortingOrders.PhoneNumberConfigurations.List(context.TODO(), telnyx.PortingOrderPhoneNumberConfigurationListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建号码配置列表

创建号码配置的列表。

`POST /porting_orders/phone_number_configurations`

```go
	phoneNumberConfiguration, err := client.PortingOrders.PhoneNumberConfigurations.New(context.TODO(), telnyx.PortingOrderPhoneNumberConfigurationNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumberConfiguration.Data)
```

## 列出所有迁移中的号码

返回所有迁移中的号码列表。

`GET /porting/phone_numbers`

```go
	page, err := client.PortingPhoneNumbers.List(context.TODO(), telnyx.PortingPhoneNumberListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出与端口迁移相关的报告

列出与端口迁移操作相关的报告。

`GET /porting/reports`

```go
	page, err := client.Porting.Reports.List(context.TODO(), telnyx.PortingReportListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建与端口迁移相关的报告

生成与端口迁移操作相关的报告。

`POST /porting/reports`

```go
	report, err := client.Porting.Reports.New(context.TODO(), telnyx.PortingReportNewParams{
		Params: telnyx.ExportPortingOrdersCsvReportParam{
			Filters: telnyx.ExportPortingOrdersCsvReportFiltersParam{},
		},
		ReportType: telnyx.PortingReportNewParamsReportTypeExportPortingOrdersCsv,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", report.Data)
```

## 检索报告

检索特定的报告。

`GET /porting/reports/{id}`

```go
	report, err := client.Porting.Reports.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", report.Data)
```

## 列出英国的可用运营商

列出英国的可用运营商。

`GET /porting/uk_carriers`

```go
	response, err := client.Porting.ListUkCarriers(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 运行端口迁移检查

立即运行端口迁移检查并返回结果。

`POST /portability_checks`

```go
	response, err := client.PortabilityChecks.Run(context.TODO(), telnyx.PortabilityCheckRunParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```
```