---
name: telnyx-numbers-config-go
description: >-
  Configure phone number settings including caller ID, call forwarding,
  messaging enablement, and connection assignments. This skill provides Go SDK
  examples.
metadata:
  author: telnyx
  product: numbers-config
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字信息配置 - Go

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

## 列出电话号码相关任务

`GET /phone_number_blocks/jobs`

```go
	page, err := client.PhoneNumberBlocks.Jobs.List(context.TODO(), telnyx.PhoneNumberBlockJobListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取电话号码相关任务的信息

`GET /phone_number_blocks/jobs/{id}`

```go
	job, err := client.PhoneNumberBlocks.Jobs.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", job.Data)
```

## 删除与某个电话号码块关联的所有号码

创建一个新的后台任务，以删除与该号码块关联的所有号码。

`POST /phone_number_blocks/jobs/delete_phone_number_block` — 必需参数：`phone_number_block_id`

```go
	response, err := client.PhoneNumberBlocks.Jobs.DeletePhoneNumberBlock(context.TODO(), telnyx.PhoneNumberBlockJobDeletePhoneNumberBlockParams{
		PhoneNumberBlockID: "f3946371-7199-4261-9c3d-81a0d7935146",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有电话号码

`GET /phone_numbers`

```go
	page, err := client.PhoneNumbers.List(context.TODO(), telnyx.PhoneNumberListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取单个电话号码的信息

`GET /phone_numbers/{id}`

```go
	phoneNumber, err := client.PhoneNumbers.Get(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumber.Data)
```

## 更新电话号码信息

`PATCH /phone_numbers/{id}`

```go
	phoneNumber, err := client.PhoneNumbers.Update(
		context.TODO(),
		"1293384261075731499",
		telnyx.PhoneNumberUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumber.Data)
```

## 删除电话号码

`DELETE /phone_numbers/{id}`

```go
	phoneNumber, err := client.PhoneNumbers.Delete(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumber.Data)
```

## 更改电话号码的捆绑状态（将其添加到捆绑包中或从捆绑包中移除）

`PATCH /phone_numbers/{id}/actions/bundle_status_change` — 必需参数：`bundle_id`

```go
	response, err := client.PhoneNumbers.Actions.ChangeBundleStatus(
		context.TODO(),
		"1293384261075731499",
		telnyx.PhoneNumberActionChangeBundleStatusParams{
			BundleID: "5194d8fc-87e6-4188-baa9-1c434bbe861b",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 为电话号码启用紧急呼叫功能

`POST /phone_numbers/{id}/actions/enable_emergency` — 必需参数：`emergency_enabled`, `emergency_address_id`

```go
	response, err := client.PhoneNumbers.Actions.EnableEmergency(
		context.TODO(),
		"1293384261075731499",
		telnyx.PhoneNumberActionEnableEmergencyParams{
			EmergencyAddressID: "53829456729313",
			EmergencyEnabled:   true,
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取带有语音设置的电话号码信息

`GET /phone_numbers/{id}/voice`

```go
	voice, err := client.PhoneNumbers.Voice.Get(context.TODO(), "1293384261075731499")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 更新带有语音设置的电话号码信息

`PATCH /phone_numbers/{id}/voice`

```go
	voice, err := client.PhoneNumbers.Voice.Update(
		context.TODO(),
		"1293384261075731499",
		telnyx.PhoneNumberVoiceUpdateParams{
			UpdateVoiceSettings: telnyx.UpdateVoiceSettingsParam{},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 验证电话号码的所有权

验证提供的电话号码的所有权，并返回号码与其 ID 的对应关系，以及未在账户中找到的号码列表。

`POST /phone_numbers/actions/verify_ownership` — 必需参数：`phone_numbers`

```go
	response, err := client.PhoneNumbers.Actions.VerifyOwnership(context.TODO(), telnyx.PhoneNumberActionVerifyOwnershipParams{
		PhoneNumbers: []string{"+15551234567"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查看 CSV 下载记录

`GET /phone_numbers/csv_downloads`

```go
	page, err := client.PhoneNumbers.CsvDownloads.List(context.TODO(), telnyx.PhoneNumberCsvDownloadListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 CSV 下载文件

`POST /phone_numbers/csv_downloads`

```go
	csvDownload, err := client.PhoneNumbers.CsvDownloads.New(context.TODO(), telnyx.PhoneNumberCsvDownloadNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", csvDownload.Data)
```

## 获取 CSV 下载文件

`GET /phone_numbers/csv_downloads/{id}`

```go
	csvDownload, err := client.PhoneNumbers.CsvDownloads.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", csvDownload.Data)
```

## 列出电话号码相关任务

`GET /phone_numbers/jobs`

```go
	page, err := client.PhoneNumbers.Jobs.List(context.TODO(), telnyx.PhoneNumberJobListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取单个电话号码相关任务的信息

`GET /phone_numbers/jobs/{id}`

```go
	job, err := client.PhoneNumbers.Jobs.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", job.Data)
```

## 删除一批电话号码

创建一个新的后台任务，以删除一批电话号码。

`POST /phone_numbers/jobs/delete_phone_numbers` — 必需参数：`phone_numbers`

```go
	response, err := client.PhoneNumbers.Jobs.DeleteBatch(context.TODO(), telnyx.PhoneNumberJobDeleteBatchParams{
		PhoneNumbers: []string{"+19705555098", "+19715555098", "32873127836"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 更新一批电话号码的紧急呼叫设置

创建一个新的后台任务，以更新一批电话号码的紧急呼叫设置。

`POST /phone_numbers/jobs/update_emergency_settings` — 必需参数：`emergency_enabled`, `phone_numbers`

```go
	response, err := client.PhoneNumbers.Jobs.UpdateEmergencySettingsBatch(context.TODO(), telnyx.PhoneNumberJobUpdateEmergencySettingsBatchParams{
		EmergencyEnabled: true,
		PhoneNumbers:     []string{"+19705555098", "+19715555098", "32873127836"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 更新一批电话号码的信息

创建一个新的后台任务，以更新一批电话号码的信息。

`POST /phone_numbers/jobs/update_phone_numbers` — 必需参数：`phone_numbers`

```go
	response, err := client.PhoneNumbers.Jobs.UpdateBatch(context.TODO(), telnyx.PhoneNumberJobUpdateBatchParams{
		PhoneNumbers: []string{"1583466971586889004", "+13127367254"},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取一批电话号码的监管要求信息

`GET /phone_numbers/regulatory_requirements`

```go
	phoneNumbersRegulatoryRequirement, err := client.PhoneNumbersRegulatoryRequirements.Get(context.TODO(), telnyx.PhoneNumbersRegulatoryRequirementGetParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumbersRegulatoryRequirement.Data)
```

## 精简版电话号码列表

列出电话号码，此端点的性能更高，但数据量限制更严格。

`GET /phone_numbers/slim`

```go
	page, err := client.PhoneNumbers.SlimList(context.TODO(), telnyx.PhoneNumberSlimListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出带有语音设置的电话号码

`GET /phone_numbers/voice`

```go
	page, err := client.PhoneNumbers.Voice.List(context.TODO(), telnyx.PhoneNumberVoiceListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 列出手机号码

`GET /v2/mobile_phone_numbers`

```go
	page, err := client.MobilePhoneNumbers.List(context.TODO(), telnyx.MobilePhoneNumberListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取手机号码信息

`GET /v2/mobile_phone_numbers/{id}`

```go
	mobilePhoneNumber, err := client.MobilePhoneNumbers.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mobilePhoneNumber.Data)
```

## 更新手机号码信息

`PATCH /v2/mobile_phone_numbers/{id}`

```go
	mobilePhoneNumber, err := client.MobilePhoneNumbers.Update(
		context.TODO(),
		"id",
		telnyx.MobilePhoneNumberUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mobilePhoneNumber.Data)
```