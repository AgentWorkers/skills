---
name: telnyx-account-reports-go
description: >-
  Generate and retrieve usage reports for billing, analytics, and
  reconciliation. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: account-reports
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户报告 - Go

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

## 获取所有 MDR 详细报告请求

检索已认证用户的所有 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging`

```go
	messagings, err := client.Legacy.Reporting.BatchDetailRecords.Messaging.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messagings.Data)
```

## 创建新的 MDR 详细报告请求

使用指定的过滤器创建新的 MDR 详细报告请求

`POST /legacy_reporting/batch_detail_records/messaging` — 必需参数：`start_time`、`end_time`

```go
	messaging, err := client.Legacy.Reporting.BatchDetailRecords.Messaging.New(context.TODO(), telnyx.LegacyReportingBatchDetailRecordMessagingNewParams{
		EndTime:   time.Now(),
		StartTime: time.Now(),
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 获取特定的 MDR 详细报告请求

通过 ID 获取特定的 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging/{id}`

```go
	messaging, err := client.Legacy.Reporting.BatchDetailRecords.Messaging.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 删除 MDR 详细报告请求

通过 ID 删除特定的 MDR 详细报告请求

`DELETE /legacy_reporting/batch_detail_records/messaging/{id}`

```go
	messaging, err := client.Legacy.Reporting.BatchDetailRecords.Messaging.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 获取所有 CDR 报告请求

检索已认证用户的所有 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice`

```go
	voices, err := client.Legacy.Reporting.BatchDetailRecords.Voice.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voices.Data)
```

## 创建新的 CDR 报告请求

使用指定的过滤器创建新的 CDR 报告请求

`POST /legacy_reporting/batch_detail_records/voice` — 必需参数：`start_time`、`end_time`

```go
	voice, err := client.Legacy.Reporting.BatchDetailRecords.Voice.New(context.TODO(), telnyx.LegacyReportingBatchDetailRecordVoiceNewParams{
		EndTime:   time.Now(),
		StartTime: time.Now(),
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 获取特定的 CDR 报告请求

通过 ID 获取特定的 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice/{id}`

```go
	voice, err := client.Legacy.Reporting.BatchDetailRecords.Voice.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 删除 CDR 报告请求

通过 ID 删除特定的 CDR 报告请求

`DELETE /legacy_reporting/batch_detail_records/voice/{id}`

```go
	voice, err := client.Legacy.Reporting.BatchDetailRecords.Voice.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 获取可用的 CDR 报告字段

检索所有可用于 CDR 报告的字段

`GET /legacy_reporting/batch_detail_records/voice/fields`

```go
	response, err := client.Legacy.Reporting.BatchDetailRecords.Voice.GetFields(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Billing)
```

## 列出 MDR 使用报告

获取所有之前的 MDR 使用报告请求

`GET /legacy_reporting/usage_reports/messaging`

```go
	page, err := client.Legacy.Reporting.UsageReports.Messaging.List(context.TODO(), telnyx.LegacyReportingUsageReportMessagingListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的传统使用 V2 MDR 报告请求

使用指定的过滤器创建新的传统使用 V2 MDR 报告请求

`POST /legacy_reporting/usage_reports/messaging`

```go
	messaging, err := client.Legacy.Reporting.UsageReports.Messaging.New(context.TODO(), telnyx.LegacyReportingUsageReportMessagingNewParams{
		AggregationType: 0,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 获取 MDR 使用报告

通过 ID 获取单个 MDR 使用报告

`GET /legacy_reporting/usage_reports/messaging/{id}`

```go
	messaging, err := client.Legacy.Reporting.UsageReports.Messaging.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 删除 V2 传统使用 MDR 报告请求

通过 ID 删除特定的 V2 传统使用 MDR 报告请求

`DELETE /legacy_reporting/usage_reports/messaging/{id}`

```go
	messaging, err := client.Legacy.Reporting.UsageReports.Messaging.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", messaging.Data)
```

## 列出电信数据使用报告

获取分页的电信数据使用报告列表

`GET /legacy_reporting/usage_reports/number_lookup`

```go
	numberLookups, err := client.Legacy.Reporting.UsageReports.NumberLookup.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberLookups.Data)
```

## 提交电信数据使用报告

提交新的电信数据使用报告

`POST /legacy_reporting/usage_reports/number_lookup`

```go
	numberLookup, err := client.Legacy.Reporting.UsageReports.NumberLookup.New(context.TODO(), telnyx.LegacyReportingUsageReportNumberLookupNewParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberLookup.Data)
```

## 通过 ID 获取电信数据使用报告

通过 ID 获取特定的电信数据使用报告

`GET /legacy_reporting/usage_reports/number_lookup/{id}`

```go
	numberLookup, err := client.Legacy.Reporting.UsageReports.NumberLookup.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", numberLookup.Data)
```

## 删除电信数据使用报告

通过 ID 删除特定的电信数据使用报告

`DELETE /legacy_reporting/usage_reports/number_lookup/{id}`

```go
	err := client.Legacy.Reporting.UsageReports.NumberLookup.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
```

## 获取语音转文本使用报告

生成并同步获取语音转文本使用报告

`GET /legacy_reporting/usage_reports/speech_to_text`

```go
	response, err := client.Legacy.Reporting.UsageReports.GetSpeechToText(context.TODO(), telnyx.LegacyReportingUsageReportGetSpeechToTextParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出 CDR 使用报告

获取所有之前的 CDR 使用报告请求

`GET /legacy_reporting/usage_reports/voice`

```go
	page, err := client.Legacy.Reporting.UsageReports.Voice.List(context.TODO(), telnyx.LegacyReportingUsageReportVoiceListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建新的传统使用 V2 CDR 报告请求

使用指定的过滤器创建新的传统使用 V2 CDR 报告请求

`POST /legacy_reporting/usage_reports/voice`

```go
	voice, err := client.Legacy.Reporting.UsageReports.Voice.New(context.TODO(), telnyx.LegacyReportingUsageReportVoiceNewParams{
		EndTime:   time.Now(),
		StartTime: time.Now(),
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 获取 CDR 使用报告

通过 ID 获取单个 CDR 使用报告

`GET /legacy_reporting/usage_reports/voice/{id}`

```go
	voice, err := client.Legacy.Reporting.UsageReports.Voice.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 删除 V2 传统使用 CDR 报告请求

通过 ID 删除特定的 V2 传统使用 CDR 报告请求

`DELETE /legacy_reporting/usage_reports/voice/{id}`

```go
	voice, err := client.Legacy.Reporting.UsageReports.Voice.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", voice.Data)
```

## 获取所有消息使用报告

获取所有消息使用报告

`GET /reports/mdr_usage_reports`

```go
	page, err := client.Reports.MdrUsageReports.List(context.TODO(), telnyx.ReportMdrUsageReportListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建 MDR 使用报告

提交新的消息使用报告请求

`POST /reports/mdr_usage_reports`

```go
	mdrUsageReport, err := client.Reports.MdrUsageReports.New(context.TODO(), telnyx.ReportMdrUsageReportNewParams{
		AggregationType: telnyx.ReportMdrUsageReportNewParamsAggregationTypeNoAggregation,
		EndDate:         time.Now(),
		StartDate:       time.Now(),
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mdrUsageReport.Data)
```

## 获取消息使用报告

通过 ID 获取单个消息使用报告

`GET /reports/mdr_usage_reports/{id}`

```go
	mdrUsageReport, err := client.Reports.MdrUsageReports.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mdrUsageReport.Data)
```

## 删除 MDR 使用报告

通过 ID 删除消息使用报告

`DELETE /reports/mdr_usage_reports/{id}`

```go
	mdrUsageReport, err := client.Reports.MdrUsageReports.Delete(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", mdrUsageReport.Data)
```

## 生成并获取 MDR 使用报告

同步生成并获取消息使用报告

`GET /reports/mdr_usage_reports/sync`

```go
	response, err := client.Reports.MdrUsageReports.FetchSync(context.TODO(), telnyx.ReportMdrUsageReportFetchSyncParams{
		AggregationType: telnyx.ReportMdrUsageReportFetchSyncParamsAggregationTypeProfile,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 生成并获取 CDR 使用报告

同步生成并获取语音使用报告

`GET /reports/cdr_usage_reports/sync`

```go
	response, err := client.Reports.CdrUsageReports.FetchSync(context.TODO(), telnyx.ReportCdrUsageReportFetchSyncParams{
		AggregationType:  telnyx.ReportCdrUsageReportFetchSyncParamsAggregationTypeNoAggregation,
		ProductBreakdown: telnyx.ReportCdrUsageReportFetchSyncParamsProductBreakdownNoBreakdown,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取 Telnyx 产品使用数据（测试版）

按指定维度获取 Telnyx 产品使用数据

`GET /usage_reports`

```go
	page, err := client.UsageReports.List(context.TODO(), telnyx.UsageReportListParams{
		Dimensions: []string{"string"},
		Metrics:    []string{"string"},
		Product:    "product",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取使用报告查询选项（测试版）

获取用于查询使用情况的报告选项，包括可用的产品及其相应的指标和维度

`GET /usage_reports/options`

```go
	response, err := client.UsageReports.GetOptions(context.TODO(), telnyx.UsageReportGetOptionsParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```