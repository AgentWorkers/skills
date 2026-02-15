---
name: telnyx-account-management-go
description: >-
  Manage sub-accounts for reseller and enterprise scenarios. This skill provides
  Go SDK examples.
metadata:
  author: telnyx
  product: account-management
  language: go
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户管理 - Go

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出当前用户管理的账户

列出当前用户管理的账户。

`GET /managed_accounts`

```go
	page, err := client.ManagedAccounts.List(context.TODO(), telnyx.ManagedAccountListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建一个新的受管理的账户

创建一个由已认证用户拥有的新受管理账户。

`POST /managed_accounts` — 必需参数：`business_name`

```go
	managedAccount, err := client.ManagedAccounts.New(context.TODO(), telnyx.ManagedAccountNewParams{
		BusinessName: "Larry's Cat Food Inc",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", managedAccount.Data)
```

## 获取受管理的账户信息

检索单个受管理账户的详细信息。

`GET /managed_accounts/{id}`

```go
	managedAccount, err := client.ManagedAccounts.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", managedAccount.Data)
```

## 更新受管理的账户

更新单个受管理的账户。

`PATCH /managed_accounts/{id}`

```go
	managedAccount, err := client.ManagedAccounts.Update(
		context.TODO(),
		"id",
		telnyx.ManagedAccountUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", managedAccount.Data)
```

## 禁用受管理的账户

禁用受管理的账户，使其无法使用 Telnyx 服务（包括发送或接收电话呼叫和短信）。

`POST /managed_accounts/{id}/actions/disable`

```go
	response, err := client.ManagedAccounts.Actions.Disable(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 恢复受管理的账户

启用受管理的账户及其子用户使用 Telnyx 服务。

`POST /managed_accounts/{id}/actions/enable`

```go
	response, err := client.ManagedAccounts.Actions.Enable(
		context.TODO(),
		"id",
		telnyx.ManagedAccountActionEnableParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 更新分配给特定受管理账户的全球出站通道数量

更新分配给特定受管理账户的全球出站通道数量。

`PATCH /managed_accounts/{id}/update_global_channel_limit`

```go
	response, err := client.ManagedAccounts.UpdateGlobalChannelLimit(
		context.TODO(),
		"id",
		telnyx.ManagedAccountUpdateGlobalChannelLimitParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 显示当前用户可用的全球出站通道信息

显示当前用户可用的全球出站通道信息。

`GET /managed_accounts/allocatable_global_outbound_channels`

```go
	response, err := client.ManagedAccounts.GetAllocatableGlobalOutboundChannels(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```