---
name: telnyx-sip-integrations-python
description: >-
  Manage call recordings, media storage, Dialogflow integration, and external
  connections for SIP trunking. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: sip-integrations
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip 集成 - Python

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有通话记录

返回您的通话记录列表。

`GET /recordings`

```python
page = client.recordings.list()
page = page.data[0]
print(page.id)
```

## 获取通话记录

检索现有通话记录的详细信息。

`GET /recordings/{recording_id}`

```python
recording = client.recordings.retrieve(
    "recording_id",
)
print(recording.data)
```

## 删除通话记录

永久删除通话记录。

`DELETE /recordings/{recording_id}`

```python
recording = client.recordings.delete(
    "recording_id",
)
print(recording.data)
```

## 删除通话记录列表

永久删除通话记录列表。

`POST /recordings/actions/delete`

```python
client.recordings.actions.delete(
    ids=["428c31b6-7af4-4bcb-b7f5-5013ef9657c1", "428c31b6-7af4-4bcb-b7f5-5013ef9657c2"],
)
```

## 列出所有通话转录内容

返回您的通话转录内容列表。

`GET /recording_transcriptions`

```python
recording_transcriptions = client.recording_transcriptions.list()
print(recording_transcriptions.data)
```

## 获取通话转录内容

检索现有通话转录内容的详细信息。

`GET /recording_transcriptions/{recording_transcription_id}`

```python
recording_transcription = client.recording_transcriptions.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(recording_transcription.data)
```

## 删除通话转录内容

永久删除通话转录内容。

`DELETE /recording_transcriptions/{recording_transcription_id}`

```python
recording_transcription = client.recording_transcriptions.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(recording_transcription.data)
```

## 获取存储的凭据信息

返回有关自定义存储凭据的信息。

`GET /custom_storage_credentials/{connection_id}`

```python
custom_storage_credential = client.custom_storage_credentials.retrieve(
    "connection_id",
)
print(custom_storage_credential.connection_id)
```

## 创建自定义存储凭据

创建自定义存储凭据配置。

`POST /custom_storage_credentials/{connection_id}`

```python
custom_storage_credential = client.custom_storage_credentials.create(
    connection_id="connection_id",
    backend="gcs",
    configuration={
        "backend": "gcs"
    },
)
print(custom_storage_credential.connection_id)
```

## 更新存储的凭据

更新存储的自定义凭据配置。

`PUT /custom_storage_credentials/{connection_id}`

```python
custom_storage_credential = client.custom_storage_credentials.update(
    connection_id="connection_id",
    backend="gcs",
    configuration={
        "backend": "gcs"
    },
)
print(custom_storage_credential.connection_id)
```

## 删除存储的凭据

删除存储的自定义凭据配置。

`DELETE /custom_storage_credentials/{connection_id}`

```python
client.custom_storage_credentials.delete(
    "connection_id",
)
```

## 获取存储的 Dialogflow 连接信息

返回与给定 CallControl 连接关联的 Dialogflow 连接的详细信息。

`GET /dialogflow_connections/{connection_id}`

```python
dialogflow_connection = client.dialogflow_connections.retrieve(
    "connection_id",
)
print(dialogflow_connection.data)
```

## 创建 Dialogflow 连接

将 Dialogflow 凭据保存到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /dialogflow_connections/{connection_id}`

```python
dialogflow_connection = client.dialogflow_connections.create(
    connection_id="connection_id",
    service_account={
        "type": "bar",
        "project_id": "bar",
        "private_key_id": "bar",
        "private_key": "bar",
        "client_email": "bar",
        "client_id": "bar",
        "auth_uri": "bar",
        "token_uri": "bar",
        "auth_provider_x509_cert_url": "bar",
        "client_x509_cert_url": "bar",
    },
)
print(dialogflow_connection.data)
```

## 更新存储的 Dialogflow 连接

更新存储的 Dialogflow 连接。

`PUT /dialogflow_connections/{connection_id}`

```python
dialogflow_connection = client.dialogflow_connections.update(
    connection_id="connection_id",
    service_account={
        "type": "bar",
        "project_id": "bar",
        "private_key_id": "bar",
        "private_key": "bar",
        "client_email": "bar",
        "client_id": "bar",
        "auth_uri": "bar",
        "token_uri": "bar",
        "auth_provider_x509_cert_url": "bar",
        "client_x509_cert_url": "bar",
    },
)
print(dialogflow_connection.data)
```

## 删除存储的 Dialogflow 连接

删除存储的 Dialogflow 连接。

`DELETE /dialogflow_connections/{connection_id}`

```python
client.dialogflow_connections.delete(
    "connection_id",
)
```

## 列出所有外部连接

此端点返回响应中 'data' 属性内的所有外部连接列表。

`GET /external_connections`

```python
page = client.external_connections.list()
page = page.data[0]
print(page.id)
```

## 创建外部连接

根据请求中发送的参数创建新的外部连接。

`POST /external_connections` — 必需参数：`external_sip_connection`, `outbound`

```python
external_connection = client.external_connections.create(
    external_sip_connection="zoom",
    outbound={},
)
print(external_connection.data)
```

## 获取外部连接信息

返回响应中 'data' 属性内的现有外部连接的详细信息。

`GET /external_connections/{id}`

```python
external_connection = client.external_connections.retrieve(
    "id",
)
print(external_connection.data)
```

## 更新外部连接

根据请求的参数更新现有外部连接的设置。

`PATCH /external_connections/{id}` — 必需参数：`outbound`

```python
external_connection = client.external_connections.update(
    id="id",
    outbound={
        "outbound_voice_profile_id": "outbound_voice_profile_id"
    },
)
print(external_connection.data)
```

## 删除外部连接

永久删除外部连接。

`DELETE /external_connections/{id}`

```python
external_connection = client.external_connections.delete(
    "id",
)
print(external_connection.data)
```

## 列出所有市民地址和位置信息

从 Microsoft Teams 中获取市民地址和位置信息。

`GET /external_connections/{id}/civic_addresses`

```python
civic_addresses = client.external_connections.civic_addresses.list(
    id="id",
)
print(civic_addresses.data)
```

## 获取市民地址信息

返回响应中 'data' 属性内的现有市民地址及其位置的详细信息。

`GET /external_connections/{id}/civic_addresses/{address_id}`

```python
civic_address = client.external_connections.civic_addresses.retrieve(
    address_id="318fb664-d341-44d2-8405-e6bfb9ced6d9",
    id="id",
)
print(civic_address.data)
```

## 更新位置的静态紧急地址

`PATCH /external_connections/{id}/locations/{location_id}` — 必需参数：`static_emergency_address_id`

```python
response = client.external_connections.update_location(
    location_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    static_emergency_address_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 列出所有电话号码

返回与给定外部连接关联的所有活跃电话号码列表。

`GET /external_connections/{id}/phone_numbers`

```python
page = client.external_connections.phone_numbers.list(
    id="id",
)
page = page.data[0]
print(page.civic_address_id)
```

## 获取电话号码信息

返回与给定外部连接关联的电话号码的详细信息。

`GET /external_connections/{id}/phone_numbers/{phone_number_id}`

```python
phone_number = client.external_connections.phone_numbers.retrieve(
    phone_number_id="1234567889",
    id="id",
)
print(phone_number.data)
```

## 更新电话号码信息

异步更新与给定外部连接关联的电话号码设置。

`PATCH /external_connections/{id}/phone_numbers/{phone_number_id}`

```python
phone_number = client.external_connections.phone_numbers.update(
    phone_number_id="1234567889",
    id="id",
)
print(phone_number.data)
```

## 列出所有发布记录

返回与给定外部连接关联的所有发布记录列表。

`GET /external_connections/{id}/releases`

```python
page = client.external_connections.releases.list(
    id="id",
)
page = page.data[0]
print(page.tenant_id)
```

## 获取发布请求信息

返回发布请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/releases/{release_id}`

```python
release = client.external_connections.releases.retrieve(
    release_id="7b6a6449-b055-45a6-81f6-f6f0dffa4cc6",
    id="id",
)
print(release.data)
```

## 列出所有上传请求

返回与给定外部连接关联的所有上传请求列表。

`GET /external_connections/{id}/uploads`

```python
page = client.external_connections.uploads.list(
    id="id",
)
page = page.data[0]
print(page.location_id)
```

## 创建上传请求

创建一个新的上传请求，包含关联的电话号码。

`POST /external_connections/{id}/uploads` — 必需参数：`number_ids`

```python
upload = client.external_connections.uploads.create(
    id="id",
    number_ids=["3920457616934164700", "3920457616934164701", "3920457616934164702", "3920457616934164703"],
)
print(upload.ticket_id)
```

## 刷新所有上传请求的状态

强制在后台重新检查给定外部连接的所有待处理上传请求的状态。

`POST /external_connections/{id}/uploads/refresh`

```python
response = client.external_connections.uploads.refresh_status(
    "id",
)
print(response.success)
```

## 获取待处理上传请求的数量

返回给定外部连接的所有待处理上传请求的数量。

`GET /external_connections/{id}/uploads/status`

```python
response = client.external_connections.uploads.pending_count(
    "id",
)
print(response.data)
```

## 获取上传请求信息

返回上传请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/uploads/{ticket_id}`

```python
upload = client.external_connections.uploads.retrieve(
    ticket_id="7b6a6449-b055-45a6-81f6-f6f0dffa4cc6",
    id="id",
)
print(upload.data)
```

## 重试上传请求

如果上传过程中出现任何错误，此端点将重试上传请求。

`POST /external_connections/{id}/uploads/{ticket_id}/retry`

```python
response = client.external_connections.uploads.retry(
    ticket_id="7b6a6449-b055-45a6-81f6-f6f0dffa4cc6",
    id="id",
)
print(response.data)
```

## 列出所有日志消息

检索与您的账户关联的所有外部连接的日志消息列表。

`GET /external_connections/log_messages`

```python
page = client.external_connections.log_messages.list()
page = page.log_messages[0]
print(page.code)
```

## 获取日志消息

检索与您的账户关联的外部连接的日志消息。

`GET /external_connections/log_messages/{id}`

```python
log_message = client.external_connections.log_messages.retrieve(
    "id",
)
print(log_message.log_messages)
```

## 删除日志消息

删除与您的账户关联的外部连接的日志消息。

`DELETE /external_connections/log_messages/{id}`

```python
response = client.external_connections.log_messages.dismiss(
    "id",
)
print(response.success)
```

## 刷新 Operator Connect 集成

此端点将异步请求以刷新当前用户与 Microsoft Teams 的 Operator Connect 集成。

`POST /operator_connect/actions/refresh`

```python
response = client.operator_connect.actions.refresh()
print(response.message)
```

## 列出已上传的媒体文件

返回存储的媒体文件列表。

`GET /media`

```python
media = client.media.list()
print(media.data)
```

## 上传媒体文件

将媒体文件上传到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /media` — 必需参数：`media_url`

```python
response = client.media.upload(
    media_url="http://www.example.com/audio.mp3",
)
print(response.data)
```

## 获取存储的媒体文件信息

返回存储的媒体文件的详细信息。

`GET /media/{media_name}`

```python
media = client.media.retrieve(
    "media_name",
)
print(media.data)
```

## 更新存储的媒体文件

更新存储的媒体文件。

`PUT /media/{media_name}`

```python
media = client.media.update(
    media_name="media_name",
)
print(media.data)
```

## 删除存储的媒体文件

删除存储的媒体文件。

`DELETE /media/{media_name}`

```python
client.media.delete(
    "media_name",
)
```

## 下载存储的媒体文件

下载存储的媒体文件。

`GET /media/{media_name}/download`

```python
response = client.media.download(
    "media_name",
)
print(response)
content = response.read()
print(content)
```