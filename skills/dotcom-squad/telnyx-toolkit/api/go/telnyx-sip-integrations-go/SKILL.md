---
name: telnyx-sip-integrations-go
description: >-
  Manage call recordings, media storage, Dialogflow integration, and external
  connections for SIP trunking. This skill provides Go SDK examples.
metadata:
  author: telnyx
  product: sip-integrations
  language: go
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由Telnix OpenAPI规范自动生成，请勿编辑。 -->

# Telnyx Sip集成 - Go

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

以下所有示例均假设`client`已按照上述方式初始化。

## 列出所有通话记录

返回您的通话记录列表。

`GET /recordings`

```go
	page, err := client.Recordings.List(context.TODO(), telnyx.RecordingListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取通话记录

检索现有通话记录的详细信息。

`GET /recordings/{recording_id}`

```go
	recording, err := client.Recordings.Get(context.TODO(), "recording_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", recording.Data)
```

## 删除通话记录

永久删除通话记录。

`DELETE /recordings/{recording_id}`

```go
	recording, err := client.Recordings.Delete(context.TODO(), "recording_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", recording.Data)
```

## 删除通话记录列表

永久删除通话记录列表。

`POST /recordings/actions/delete`

```go
	err := client.Recordings.Actions.Delete(context.TODO(), telnyx.RecordingActionDeleteParams{
		IDs: []string{"428c31b6-7af4-4bcb-b7f5-5013ef9657c1", "428c31b6-7af4-4bcb-b7f5-5013ef9657c2"},
	})
	if err != nil {
		panic(err.Error())
	}
```

## 列出所有通话转录记录

返回您的通话转录记录列表。

`GET /recording_transcriptions`

```go
	recordingTranscriptions, err := client.RecordingTranscriptions.List(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", recordingTranscriptions.Data)
```

## 获取通话转录记录

检索现有通话转录记录的详细信息。

`GET /recording_transcriptions/{recording_transcription_id}`

```go
	recordingTranscription, err := client.RecordingTranscriptions.Get(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", recordingTranscription.Data)
```

## 删除通话转录记录

永久删除通话转录记录。

`DELETE /recording_transcriptions/{recording_transcription_id}`

```go
	recordingTranscription, err := client.RecordingTranscriptions.Delete(context.TODO(), "6a09cdc3-8948-47f0-aa62-74ac943d6c58")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", recordingTranscription.Data)
```

## 获取存储的凭据

返回有关自定义存储凭据的信息。

`GET /custom_storage_credentials/{connection_id}`

```go
	customStorageCredential, err := client.CustomStorageCredentials.Get(context.TODO(), "connection_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", customStorageCredential.ConnectionID)
```

## 创建自定义存储凭据

创建自定义存储凭据配置。

`POST /custom_storage_credentials/{connection_id}`

```go
	customStorageCredential, err := client.CustomStorageCredentials.New(
		context.TODO(),
		"connection_id",
		telnyx.CustomStorageCredentialNewParams{
			CustomStorageConfiguration: telnyx.CustomStorageConfigurationParam{
				Backend: telnyx.CustomStorageConfigurationBackendGcs,
				Configuration: telnyx.CustomStorageConfigurationConfigurationUnionParam{
					OfGcs: &telnyx.GcsConfigurationDataParam{
						Backend: telnyx.GcsConfigurationDataBackendGcs,
					},
				},
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", customStorageCredential.ConnectionID)
```

## 更新存储的凭据

更新存储的自定义凭据配置。

`PUT /custom_storage_credentials/{connection_id}`

```go
	customStorageCredential, err := client.CustomStorageCredentials.Update(
		context.TODO(),
		"connection_id",
		telnyx.CustomStorageCredentialUpdateParams{
			CustomStorageConfiguration: telnyx.CustomStorageConfigurationParam{
				Backend: telnyx.CustomStorageConfigurationBackendGcs,
				Configuration: telnyx.CustomStorageConfigurationConfigurationUnionParam{
					OfGcs: &telnyx.GcsConfigurationDataParam{
						Backend: telnyx.GcsConfigurationDataBackendGcs,
					},
				},
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", customStorageCredential.ConnectionID)
```

## 删除存储的凭据

删除存储的自定义凭据配置。

`DELETE /custom_storage_credentials/{connection_id}`

```go
	err := client.CustomStorageCredentials.Delete(context.TODO(), "connection_id")
	if err != nil {
		panic(err.Error())
	}
```

## 获取存储的Dialogflow连接信息

返回与给定CallControl连接关联的Dialogflow连接详细信息。

`GET /dialogflow_connections/{connection_id}`

```go
	dialogflowConnection, err := client.DialogflowConnections.Get(context.TODO(), "connection_id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dialogflowConnection.Data)
```

## 创建Dialogflow连接

将Dialogflow凭据保存到Telnix，以便与其他Telnix服务一起使用。

`POST /dialogflow_connections/{connection_id}`

```go
	dialogflowConnection, err := client.DialogflowConnections.New(
		context.TODO(),
		"connection_id",
		telnyx.DialogflowConnectionNewParams{
			ServiceAccount: map[string]any{
				"type":                        "bar",
				"project_id":                  "bar",
				"private_key_id":              "bar",
				"private_key":                 "bar",
				"client_email":                "bar",
				"client_id":                   "bar",
				"auth_uri":                    "bar",
				"token_uri":                   "bar",
				"auth_provider_x509_cert_url": "bar",
				"client_x509_cert_url":        "bar",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dialogflowConnection.Data)
```

## 更新存储的Dialogflow连接

更新存储的Dialogflow连接信息。

`PUT /dialogflow_connections/{connection_id}`

```go
	dialogflowConnection, err := client.DialogflowConnections.Update(
		context.TODO(),
		"connection_id",
		telnyx.DialogflowConnectionUpdateParams{
			ServiceAccount: map[string]any{
				"type":                        "bar",
				"project_id":                  "bar",
				"private_key_id":              "bar",
				"private_key":                 "bar",
				"client_email":                "bar",
				"client_id":                   "bar",
				"auth_uri":                    "bar",
				"token_uri":                   "bar",
				"auth_provider_x509_cert_url": "bar",
				"client_x509_cert_url":        "bar",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", dialogflowConnection.Data)
```

## 删除存储的Dialogflow连接

删除存储的Dialogflow连接。

`DELETE /dialogflow_connections/{connection_id}`

```go
	err := client.DialogflowConnections.Delete(context.TODO(), "connection_id")
	if err != nil {
		panic(err.Error())
	}
```

## 列出所有外部连接

此端点会返回响应中`data`属性内的所有外部连接列表。

`GET /external_connections`

```go
	page, err := client.ExternalConnections.List(context.TODO(), telnyx.ExternalConnectionListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建外部连接

根据请求中发送的参数创建新的外部连接。

`POST /external_connections` — 必需参数：`external_sip_connection`, `outbound`

```go
	externalConnection, err := client.ExternalConnections.New(context.TODO(), telnyx.ExternalConnectionNewParams{
		ExternalSipConnection: telnyx.ExternalConnectionNewParamsExternalSipConnectionZoom,
		Outbound:              telnyx.ExternalConnectionNewParamsOutbound{},
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", externalConnection.Data)
```

## 获取外部连接信息

返回响应中`data`属性内的现有外部连接详细信息。

`GET /external_connections/{id}`

```go
	externalConnection, err := client.ExternalConnections.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", externalConnection.Data)
```

## 更新外部连接

根据请求的参数更新现有外部连接的设置。

`PATCH /external_connections/{id}` — 必需参数：`outbound`

```go
	externalConnection, err := client.ExternalConnections.Update(
		context.TODO(),
		"id",
		telnyx.ExternalConnectionUpdateParams{
			Outbound: telnyx.ExternalConnectionUpdateParamsOutbound{
				OutboundVoiceProfileID: "outbound_voice_profile_id",
			},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", externalConnection.Data)
```

## 删除外部连接

永久删除外部连接。

`DELETE /external_connections/{id}`

```go
	externalConnection, err := client.ExternalConnections.Delete(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", externalConnection.Data)
```

## 列出所有市民地址和位置信息

从Microsoft Teams中返回市民地址和位置信息。

`GET /external_connections/{id}/civic_addresses`

```go
	civicAddresses, err := client.ExternalConnections.CivicAddresses.List(
		context.TODO(),
		"id",
		telnyx.ExternalConnectionCivicAddressListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", civicAddresses.Data)
```

## 获取市民地址信息

返回现有市民地址的详细信息及其位置信息（包含在响应的`data`属性中）。

`GET /external_connections/{id}/civic_addresses/{address_id}`

```go
	civicAddress, err := client.ExternalConnections.CivicAddresses.Get(
		context.TODO(),
		"318fb664-d341-44d2-8405-e6bfb9ced6d9",
		telnyx.ExternalConnectionCivicAddressGetParams{
			ID: "id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", civicAddress.Data)
```

## 更新位置的静态紧急地址

`PATCH /external_connections/{id}/locations/{location_id}` — 必需参数：`static_emergency_address_id`

```go
	response, err := client.ExternalConnections.UpdateLocation(
		context.TODO(),
		"182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		telnyx.ExternalConnectionUpdateLocationParams{
			ID:                       "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
			StaticEmergencyAddressID: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有电话号码

返回与给定外部连接关联的所有活跃电话号码列表。

`GET /external_connections/{id}/phone_numbers`

```go
	page, err := client.ExternalConnections.PhoneNumbers.List(
		context.TODO(),
		"id",
		telnyx.ExternalConnectionPhoneNumberListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取电话号码信息

返回与给定外部连接关联的电话号码的详细信息。

`GET /external_connections/{id}/phone_numbers/{phone_number_id}`

```go
	phoneNumber, err := client.ExternalConnections.PhoneNumbers.Get(
		context.TODO(),
		"1234567889",
		telnyx.ExternalConnectionPhoneNumberGetParams{
			ID: "id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumber.Data)
```

## 更新电话号码信息

异步更新与给定外部连接关联的电话号码设置。

`PATCH /external_connections/{id}/phone_numbers/{phone_number_id}`

```go
	phoneNumber, err := client.ExternalConnections.PhoneNumbers.Update(
		context.TODO(),
		"1234567889",
		telnyx.ExternalConnectionPhoneNumberUpdateParams{
			ID: "id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", phoneNumber.Data)
```

## 列出所有发布记录

返回与给定外部连接关联的所有发布记录列表。

`GET /external_connections/{id}/releases`

```go
	page, err := client.ExternalConnections.Releases.List(
		context.TODO(),
		"id",
		telnyx.ExternalConnectionReleaseListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取发布请求信息

返回发布请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/releases/{release_id}`

```go
	release, err := client.ExternalConnections.Releases.Get(
		context.TODO(),
		"7b6a6449-b055-45a6-81f6-f6f0dffa4cc6",
		telnyx.ExternalConnectionReleaseGetParams{
			ID: "id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", release.Data)
```

## 列出所有上传请求

返回与给定外部连接关联的所有上传请求列表。

`GET /external_connections/{id}/uploads`

```go
	page, err := client.ExternalConnections.Uploads.List(
		context.TODO(),
		"id",
		telnyx.ExternalConnectionUploadListParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 创建上传请求

创建新的上传请求并关联电话号码。

`POST /external_connections/{id}/uploads` — 必需参数：`number_ids`

```go
	upload, err := client.ExternalConnections.Uploads.New(
		context.TODO(),
		"id",
		telnyx.ExternalConnectionUploadNewParams{
			NumberIDs: []string{"3920457616934164700", "3920457616934164701", "3920457616934164702", "3920457616934164703"},
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", upload.TicketID)
```

## 刷新所有上传请求的状态

强制重新检查给定外部连接的所有待处理上传请求的状态。

`POST /external_connections/{id}/uploads/refresh`

```go
	response, err := client.ExternalConnections.Uploads.RefreshStatus(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Success)
```

## 获取待处理上传请求的数量

返回给定外部连接的所有待处理上传请求的数量。

`GET /external_connections/{id}/uploads/status`

```go
	response, err := client.ExternalConnections.Uploads.PendingCount(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取上传请求详细信息

返回上传请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/uploads/{ticket_id}`

```go
	upload, err := client.ExternalConnections.Uploads.Get(
		context.TODO(),
		"7b6a6449-b055-45a6-81f6-f6f0dffa4cc6",
		telnyx.ExternalConnectionUploadGetParams{
			ID: "id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", upload.Data)
```

## 重试上传请求

如果上传过程中出现错误，此端点将重试上传请求。

`POST /external_connections/{id}/uploads/{ticket_id}/retry`

```go
	response, err := client.ExternalConnections.Uploads.Retry(
		context.TODO(),
		"7b6a6449-b055-45a6-81f6-f6f0dffa4cc6",
		telnyx.ExternalConnectionUploadRetryParams{
			ID: "id",
		},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 列出所有日志消息

检索与您的账户关联的所有外部连接的日志消息列表。

`GET /external_connections/log_messages`

```go
	page, err := client.ExternalConnections.LogMessages.List(context.TODO(), telnyx.ExternalConnectionLogMessageListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", page)
```

## 获取日志消息

检索与您的账户关联的特定外部连接的日志消息。

`GET /external_connections/log_messages/{id}`

```go
	logMessage, err := client.ExternalConnections.LogMessages.Get(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", logMessage.LogMessages)
```

## 删除日志消息

删除与您的账户关联的特定外部连接的日志消息。

`DELETE /external_connections/log_messages/{id}`

```go
	response, err := client.ExternalConnections.LogMessages.Dismiss(context.TODO(), "id")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Success)
```

## 刷新Operator Connect集成

此端点将异步请求以刷新当前用户与Microsoft Teams的Operator Connect集成。

`POST /operator_connect/actions/refresh`

```go
	response, err := client.OperatorConnect.Actions.Refresh(context.TODO())
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Message)
```

## 列出上传的媒体文件

返回存储的媒体文件列表。

`GET /media`

```go
	media, err := client.Media.List(context.TODO(), telnyx.MediaListParams{})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", media.Data)
```

## 上传媒体文件

将媒体文件上传到Telnix，以便与其他Telnix服务一起使用。

`POST /media` — 必需参数：`media_url`

```go
	response, err := client.Media.Upload(context.TODO(), telnyx.MediaUploadParams{
		MediaURL: "http://www.example.com/audio.mp3",
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", response.Data)
```

## 获取存储的媒体文件信息

返回存储的媒体文件详细信息。

`GET /media/{media_name}`

```go
	media, err := client.Media.Get(context.TODO(), "media_name")
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", media.Data)
```

## 更新存储的媒体文件

更新存储的媒体文件。

`PUT /media/{media_name}`

```go
	media, err := client.Media.Update(
		context.TODO(),
		"media_name",
		telnyx.MediaUpdateParams{},
	)
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", media.Data)
```

## 删除存储的媒体文件

删除存储的媒体文件。

`DELETE /media/{media_name}`

```go
	err := client.Media.Delete(context.TODO(), "media_name")
	if err != nil {
		panic(err.Error())
	}
```

## 下载存储的媒体文件

下载存储的媒体文件。

`GET /media/{media_name}/download`
```