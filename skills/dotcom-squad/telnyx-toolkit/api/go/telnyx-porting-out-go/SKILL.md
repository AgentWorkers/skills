---
name: telnyx-porting-out-go
description: >-
  Manage port-out requests when numbers are being ported away from Telnyx. List,
  view, and update port-out status. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: porting-out
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx 的 Porting Out 功能（Go 语言实现）

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

以下所有示例均假设 `client` 已经按照上述方式初始化完成。

## 列出 Portout 请求

根据筛选条件返回 Portout 请求：

`GET /portouts`

```go
	page, err := client.Portouts.List(context.TODO(), telnyx.PortoutListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取 Portout 请求

根据提供的 ID 获取相应的 Portout 请求：

`GET /portouts/{id}`

```go
	portout, err := client.Portouts.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", portout.Data)
```

## 查看 Portout 请求的评论

返回 Portout 请求的所有评论：

`GET /portouts/{id}/comments`

```go
	comments, err := client.Portouts.Comments.List(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", comments.Data)
```

## 为 Portout 请求添加评论

为 Portout 请求创建新的评论：

`POST /portouts/{id}/comments`

```go
	comment, err := client.Portouts.Comments.New(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortoutCommentNewParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", comment.Data)
```

## 查看 Portout 请求的相关支持文档

列出 Portout 请求的所有支持文档：

`GET /portouts/{id}/supporting_documents`

```go
	supportingDocuments, err := client.Portouts.SupportingDocuments.List(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", supportingDocuments.Data)
```

## 创建 Portout 请求的支持文档

为 Portout 请求创建新的支持文档：

`POST /portouts/{id}/supporting_documents`

```go
	supportingDocument, err := client.Portouts.SupportingDocuments.New(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.PortoutSupportingDocumentNewParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", supportingDocument.Data)
```

## 更新 Portout 请求的状态

授权或拒绝 Portout 请求：

`PATCH /portouts/{id}/{status}` — 必需参数：`reason`

```go
	response, err := client.Portouts.UpdateStatus(
		context.TODO(),
		telnyx.PortoutUpdateStatusParamsStatusAuthorized,
		telnyx.PortoutUpdateStatusParams{
			ID:     "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
			Reason: "I do not recognize this transaction",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有 Portout 事件

返回所有 Portout 事件的列表：

`GET /portouts/events`

```go
	page, err := client.Portouts.Events.List(context.TODO(), telnyx.PortoutEventListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 查看具体的 Portout 事件

显示特定的 Portout 事件：

`GET /portouts/events/{id}`

```go
	event, err := client.Portouts.Events.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", event.Data)
```

## 重新发布 Portout 事件

重新发布特定的 Portout 事件：

`POST /portouts/events/{id}/republish`

```go
	err := client.Portouts.Events.Republish(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
```

## 查看特定 Portout 的拒绝代码

根据提供的 Portout ID，列出该 Portout 可能接受的拒绝代码：

`GET /portouts/rejections/{portout_id}`

```go
	response, err := client.Portouts.ListRejectionCodes(
		context.TODO(),
		"329d6658-8f93-405d-862f-648776e8afd7",
		telnyx.PortoutListRejectionCodesParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 查看与 Portout 相关的报告

列出与 Portout 操作相关的所有报告：

`GET /portouts/reports`

```go
	page, err := client.Portouts.Reports.List(context.TODO(), telnyx.PortoutReportListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建与 Portout 相关的报告

生成关于 Portout 操作的报告：

`POST /portouts/reports`

```go
	report, err := client.Portouts.Reports.New(context.TODO(), telnyx.PortoutReportNewParams{
		Params: telnyx.ExportPortoutsCsvReportParam{
			Filters: telnyx.ExportPortoutsCsvReportFiltersParam{},
		},
		ReportType: telnyx.PortoutReportNewParamsReportTypeExportPortoutsCsv,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", report.Data)
```

## 获取报告

检索特定的报告：

`GET /portouts/reports/{id}`

```go
	report, err := client.Portouts.Reports.Get(context.TODO(), "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", report.Data)
```