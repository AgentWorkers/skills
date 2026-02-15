---
name: telnyx-sip-integrations-ruby
description: >-
  Manage call recordings, media storage, Dialogflow integration, and external
  connections for SIP trunking. This skill provides Ruby SDK examples.
metadata:
  author: telnyx
  product: sip-integrations
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip 集成 - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有通话记录

返回您的通话记录列表。

`GET /recordings`

```ruby
page = client.recordings.list

puts(page)
```

## 获取通话记录

检索现有通话记录的详细信息。

`GET /recordings/{recording_id}`

```ruby
recording = client.recordings.retrieve("recording_id")

puts(recording)
```

## 删除通话记录

永久删除通话记录。

`DELETE /recordings/{recording_id}`

```ruby
recording = client.recordings.delete("recording_id")

puts(recording)
```

## 删除通话记录列表

永久删除通话记录列表。

`POST /recordings/actions/delete`

```ruby
result = client.recordings.actions.delete(
  ids: ["428c31b6-7af4-4bcb-b7f5-5013ef9657c1", "428c31b6-7af4-4bcb-b7f5-5013ef9657c2"]
)

puts(result)
```

## 列出所有通话转录内容

返回您的通话转录内容列表。

`GET /recording_transcriptions`

```ruby
recording_transcriptions = client.recording_transcriptions.list

puts(recording_transcriptions)
```

## 获取通话转录内容

检索现有通话转录内容的详细信息。

`GET /recording_transcriptions/{recording_transcription_id}`

```ruby
recording_transcription = client.recording_transcriptions.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(recording_transcription)
```

## 删除通话转录内容

永久删除通话转录内容。

`DELETE /recording_transcriptions/{recording_transcription_id}`

```ruby
recording_transcription = client.recording_transcriptions.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(recording_transcription)
```

## 获取存储的凭据

返回关于自定义存储凭据的信息。

`GET /custom_storage_credentials/{connection_id}`

```ruby
custom_storage_credential = client.custom_storage_credentials.retrieve("connection_id")

puts(custom_storage_credential)
```

## 创建自定义存储凭据

创建自定义存储凭据配置。

`POST /custom_storage_credentials/{connection_id}`

```ruby
custom_storage_credential = client.custom_storage_credentials.create("connection_id", backend: :gcs, configuration: {backend: :gcs})

puts(custom_storage_credential)
```

## 更新存储的凭据

更新存储的自定义凭据配置。

`PUT /custom_storage_credentials/{connection_id}`

```ruby
custom_storage_credential = client.custom_storage_credentials.update("connection_id", backend: :gcs, configuration: {backend: :gcs})

puts(custom_storage_credential)
```

## 删除存储的凭据

删除存储的自定义凭据配置。

`DELETE /custom_storage_credentials/{connection_id}`

```ruby
result = client.custom_storage_credentials.delete("connection_id")

puts(result)
```

## 获取存储的 Dialogflow 连接信息

返回与给定 CallControl 连接关联的 Dialogflow 连接的详细信息。

`GET /dialogflow_connections/{connection_id}`

```ruby
dialogflow_connection = client.dialogflow_connections.retrieve("connection_id")

puts(dialogflow_connection)
```

## 创建 Dialogflow 连接

将 Dialogflow 凭据保存到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /dialogflow_connections/{connection_id}`

```ruby
dialogflow_connection = client.dialogflow_connections.create(
  "connection_id",
  service_account: {
    type: "bar",
    project_id: "bar",
    private_key_id: "bar",
    private_key: "bar",
    client_email: "bar",
    client_id: "bar",
    auth_uri: "bar",
    token_uri: "bar",
    auth_provider_x509_cert_url: "bar",
    client_x509_cert_url: "bar"
  }
)

puts(dialogflow_connection)
```

## 更新存储的 Dialogflow 连接

更新存储的 Dialogflow 连接信息。

`PUT /dialogflow_connections/{connection_id}`

```ruby
dialogflow_connection = client.dialogflow_connections.update(
  "connection_id",
  service_account: {
    type: "bar",
    project_id: "bar",
    private_key_id: "bar",
    private_key: "bar",
    client_email: "bar",
    client_id: "bar",
    auth_uri: "bar",
    token_uri: "bar",
    auth_provider_x509_cert_url: "bar",
    client_x509_cert_url: "bar"
  }
)

puts(dialogflow_connection)
```

## 删除存储的 Dialogflow 连接

删除存储的 Dialogflow 连接。

`DELETE /dialogflow_connections/{connection_id}`

```ruby
result = client.dialogflow_connections.delete("connection_id")

puts(result)
```

## 列出所有外部连接

此端点返回响应中的 'data' 属性内的所有外部连接列表。

`GET /external_connections`

```ruby
page = client.external_connections.list

puts(page)
```

## 创建外部连接

根据请求中发送的参数创建新的外部连接。

`POST /external_connections` — 必需参数：`external_sip_connection`, `outbound`

```ruby
external_connection = client.external_connections.create(external_sip_connection: :zoom, outbound: {})

puts(external_connection)
```

## 获取外部连接信息

返回响应中的 'data' 属性内的现有外部连接的详细信息。

`GET /external_connections/{id}`

```ruby
external_connection = client.external_connections.retrieve("id")

puts(external_connection)
```

## 更新外部连接

根据请求的参数更新现有外部连接的设置。

`PATCH /external_connections/{id}` — 必需参数：`outbound`

```ruby
external_connection = client.external_connections.update(
  "id",
  outbound: {outbound_voice_profile_id: "outbound_voice_profile_id"}
)

puts(external_connection)
```

## 删除外部连接

永久删除外部连接。

`DELETE /external_connections/{id}`

```ruby
external_connection = client.external_connections.delete("id")

puts(external_connection)
```

## 列出所有市民地址和位置信息

从 Microsoft Teams 中获取市民地址和位置信息。

`GET /external_connections/{id}/civic_addresses`

```ruby
civic_addresses = client.external_connections.civic_addresses.list("id")

puts(civic_addresses)
```

## 获取市民地址信息

返回现有市民地址的详细信息及其位置信息（位于响应的 'data' 属性中）。

`GET /external_connections/{id}/civic_addresses/{address_id}`

```ruby
civic_address = client.external_connections.civic_addresses.retrieve("318fb664-d341-44d2-8405-e6bfb9ced6d9", id: "id")

puts(civic_address)
```

## 更新位置的静态紧急地址

`PATCH /external_connections/{id}/locations/{location_id}` — 必需参数：`static_emergency_address_id`

```ruby
response = client.external_connections.update_location(
  "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
  static_emergency_address_id: "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
)

puts(response)
```

## 列出所有电话号码

返回与给定外部连接关联的所有活跃电话号码列表。

`GET /external_connections/{id}/phone_numbers`

```ruby
page = client.external_connections.phone_numbers.list("id")

puts(page)
```

## 获取电话号码信息

返回与给定外部连接关联的电话号码的详细信息。

`GET /external_connections/{id}/phone_numbers/{phone_number_id}`

```ruby
phone_number = client.external_connections.phone_numbers.retrieve("1234567889", id: "id")

puts(phone_number)
```

## 更新电话号码信息

异步更新与给定外部连接关联的电话号码设置。

`PATCH /external_connections/{id}/phone_numbers/{phone_number_id}`

```ruby
phone_number = client.external_connections.phone_numbers.update("1234567889", id: "id")

puts(phone_number)
```

## 列出所有发布版本

返回与给定外部连接关联的所有发布版本列表。

`GET /external_connections/{id}/releases`

```ruby
page = client.external_connections.releases.list("id")

puts(page)
```

## 获取发布请求信息

返回发布请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/releases/{release_id}`

```ruby
release = client.external_connections.releases.retrieve("7b6a6449-b055-45a6-81f6-f6f0dffa4cc6", id: "id")

puts(release)
```

## 列出所有上传请求

返回与给定外部连接关联的所有上传请求列表。

`GET /external_connections/{id}/uploads`

```ruby
page = client.external_connections.uploads.list("id")

puts(page)
```

## 创建上传请求

向 Microsoft Teams 创建新的上传请求，并附带相关电话号码。

`POST /external_connections/{id}/uploads` — 必需参数：`number_ids`

```ruby
upload = client.external_connections.uploads.create(
  "id",
  number_ids: ["3920457616934164700", "3920457616934164701", "3920457616934164702", "3920457616934164703"]
)

puts(upload)
```

## 刷新所有上传请求的状态

强制重新检查给定外部连接的所有待处理上传请求的状态。

`POST /external_connections/{id}/uploads/refresh`

```ruby
response = client.external_connections.uploads.refresh_status("id")

puts(response)
```

## 获取待处理上传请求的数量

返回给定外部连接的所有待处理上传请求的数量。

`GET /external_connections/{id}/uploads/status`

```ruby
response = client.external_connections.uploads.pending_count("id")

puts(response)
```

## 获取上传请求信息

返回上传请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/uploads/{ticket_id}`

```ruby
upload = client.external_connections.uploads.retrieve("7b6a6449-b055-45a6-81f6-f6f0dffa4cc6", id: "id")

puts(upload)
```

## 重试上传请求

如果上传过程中出现错误，此端点将重新尝试上传请求。

`POST /external_connections/{id}/uploads/{ticket_id}/retry`

```ruby
response = client.external_connections.uploads.retry_("7b6a6449-b055-45a6-81f6-f6f0dffa4cc6", id: "id")

puts(response)
```

## 列出所有日志消息

检索与您的账户关联的所有外部连接的日志消息列表。

`GET /external_connections/log_messages`

```ruby
page = client.external_connections.log_messages.list

puts(page)
```

## 获取日志消息

检索与您的账户关联的某个外部连接的日志消息。

`GET /external_connections/log_messages/{id}`

```ruby
log_message = client.external_connections.log_messages.retrieve("id")

puts(log_message)
```

## 删除日志消息

删除与您的账户关联的某个外部连接的日志消息。

`DELETE /external_connections/log_messages/{id}`

```ruby
response = client.external_connections.log_messages.dismiss("id")

puts(response)
```

## 刷新 Operator Connect 集成

此端点将异步请求以刷新当前用户与 Microsoft Teams 的 Operator Connect 集成。

`POST /operator_connect/actions/refresh`

```ruby
response = client.operator_connect.actions.refresh

puts(response)
```

## 列出已上传的媒体文件

返回存储的媒体文件列表。

`GET /media`

```ruby
media = client.media.list

puts(media)
```

## 上传媒体文件

将媒体文件上传到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /media` — 必需参数：`media_url`

```ruby
response = client.media.upload(media_url: "http://www.example.com/audio.mp3")

puts(response)
```

## 获取存储的媒体文件信息

返回存储的媒体文件的信息。

`GET /media/{media_name}`

```ruby
media = client.media.retrieve("media_name")

puts(media)
```

## 更新存储的媒体文件

更新存储的媒体文件。

`PUT /media/{media_name}`

```ruby
media = client.media.update("media_name")

puts(media)
```

## 删除存储的媒体文件

删除存储的媒体文件。

`DELETE /media/{media_name}`

```ruby
result = client.media.delete("media_name")

puts(result)
```

## 下载存储的媒体文件

下载存储的媒体文件。

`GET /media/{media_name}/download`

```ruby
response = client.media.download("media_name")

puts(response)
```
```