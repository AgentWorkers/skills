---
name: telnyx-sip-integrations-javascript
description: >-
  Manage call recordings, media storage, Dialogflow integration, and external
  connections for SIP trunking. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: sip-integrations
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip 集成 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出所有通话记录

返回您的通话记录列表。

`GET /recordings`

```javascript
// Automatically fetches more pages as needed.
for await (const recordingResponseData of client.recordings.list()) {
  console.log(recordingResponseData.id);
}
```

## 获取通话记录

检索现有通话记录的详细信息。

`GET /recordings/{recording_id}`

```javascript
const recording = await client.recordings.retrieve('recording_id');

console.log(recording.data);
```

## 删除通话记录

永久删除通话记录。

`DELETE /recordings/{recording_id}`

```javascript
const recording = await client.recordings.delete('recording_id');

console.log(recording.data);
```

## 删除通话记录列表

永久删除通话记录列表。

`POST /recordings/actions/delete`

```javascript
await client.recordings.actions.delete({
  ids: ['428c31b6-7af4-4bcb-b7f5-5013ef9657c1', '428c31b6-7af4-4bcb-b7f5-5013ef9657c2'],
});
```

## 列出所有通话转录记录

返回您的通话转录记录列表。

`GET /recording_transcriptions`

```javascript
const recordingTranscriptions = await client.recordingTranscriptions.list();

console.log(recordingTranscriptions.data);
```

## 获取通话转录记录

检索现有通话转录记录的详细信息。

`GET /recording_transcriptions/{recording_transcription_id}`

```javascript
const recordingTranscription = await client.recordingTranscriptions.retrieve(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(recordingTranscription.data);
```

## 删除通话转录记录

永久删除通话转录记录。

`DELETE /recording_transcriptions/{recording_transcription_id}`

```javascript
const recordingTranscription = await client.recordingTranscriptions.delete(
  '6a09cdc3-8948-47f0-aa62-74ac943d6c58',
);

console.log(recordingTranscription.data);
```

## 获取存储的凭据

返回有关自定义存储凭据的信息。

`GET /custom_storage_credentials/{connection_id}`

```javascript
const customStorageCredential = await client.customStorageCredentials.retrieve('connection_id');

console.log(customStorageCredential.connection_id);
```

## 创建自定义存储凭据

创建自定义存储凭据配置。

`POST /custom_storage_credentials/{connection_id}`

```javascript
const customStorageCredential = await client.customStorageCredentials.create('connection_id', {
  backend: 'gcs',
  configuration: { backend: 'gcs' },
});

console.log(customStorageCredential.connection_id);
```

## 更新存储的凭据

更新存储的自定义凭据配置。

`PUT /custom_storage_credentials/{connection_id}`

```javascript
const customStorageCredential = await client.customStorageCredentials.update('connection_id', {
  backend: 'gcs',
  configuration: { backend: 'gcs' },
});

console.log(customStorageCredential.connection_id);
```

## 删除存储的凭据

删除存储的自定义凭据配置。

`DELETE /custom_storage_credentials/{connection_id}`

```javascript
await client.customStorageCredentials.delete('connection_id');
```

## 获取存储的 Dialogflow 连接信息

返回与给定 CallControl 连接关联的 Dialogflow 连接的详细信息。

`GET /dialogflow_connections/{connection_id}`

```javascript
const dialogflowConnection = await client.dialogflowConnections.retrieve('connection_id');

console.log(dialogflowConnection.data);
```

## 创建 Dialogflow 连接

将 Dialogflow 凭据保存到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /dialogflow_connections/{connection_id}`

```javascript
const dialogflowConnection = await client.dialogflowConnections.create('connection_id', {
  service_account: {
    type: 'bar',
    project_id: 'bar',
    private_key_id: 'bar',
    private_key: 'bar',
    client_email: 'bar',
    client_id: 'bar',
    auth_uri: 'bar',
    token_uri: 'bar',
    auth_provider_x509_cert_url: 'bar',
    client_x509_cert_url: 'bar',
  },
});

console.log(dialogflowConnection.data);
```

## 更新存储的 Dialogflow 连接

更新存储的 Dialogflow 连接信息。

`PUT /dialogflow_connections/{connection_id}`

```javascript
const dialogflowConnection = await client.dialogflowConnections.update('connection_id', {
  service_account: {
    type: 'bar',
    project_id: 'bar',
    private_key_id: 'bar',
    private_key: 'bar',
    client_email: 'bar',
    client_id: 'bar',
    auth_uri: 'bar',
    token_uri: 'bar',
    auth_provider_x509_cert_url: 'bar',
    client_x509_cert_url: 'bar',
  },
});

console.log(dialogflowConnection.data);
```

## 删除存储的 Dialogflow 连接

删除存储的 Dialogflow 连接。

`DELETE /dialogflow_connections/{connection_id}`

```javascript
await client.dialogflowConnections.delete('connection_id');
```

## 列出所有外部连接

此端点返回响应中 'data' 属性内的所有外部连接列表。

`GET /external_connections`

```javascript
// Automatically fetches more pages as needed.
for await (const externalConnection of client.externalConnections.list()) {
  console.log(externalConnection.id);
}
```

## 创建外部连接

根据请求中发送的参数创建新的外部连接。

`POST /external_connections` — 必需参数：`external_sip_connection`, `outbound`

```javascript
const externalConnection = await client.externalConnections.create({
  external_sip_connection: 'zoom',
  outbound: {},
});

console.log(externalConnection.data);
```

## 获取外部连接信息

返回响应中 'data' 属性内的现有外部连接的详细信息。

`GET /external_connections/{id}`

```javascript
const externalConnection = await client.externalConnections.retrieve('id');

console.log(externalConnection.data);
```

## 更新外部连接

根据请求的参数更新现有外部连接的设置。

`PATCH /external_connections/{id}` — 必需参数：`outbound`

```javascript
const externalConnection = await client.externalConnections.update('id', {
  outbound: { outbound_voice_profile_id: 'outbound_voice_profile_id' },
});

console.log(externalConnection.data);
```

## 删除外部连接

永久删除外部连接。

`DELETE /external_connections/{id}`

```javascript
const externalConnection = await client.externalConnections.delete('id');

console.log(externalConnection.data);
```

## 列出所有公民地址和位置信息

从 Microsoft Teams 中获取公民地址和位置信息。

`GET /external_connections/{id}/civic_addresses`

```javascript
const civicAddresses = await client.externalConnections.civicAddresses.list('id');

console.log(civicAddresses.data);
```

## 获取公民地址信息

返回现有公民地址的详细信息及其位置信息（位于响应的 'data' 属性中）。

`GET /external_connections/{id}/civic_addresses/{address_id}`

```javascript
const civicAddress = await client.externalConnections.civicAddresses.retrieve(
  '318fb664-d341-44d2-8405-e6bfb9ced6d9',
  { id: 'id' },
);

console.log(civicAddress.data);
```

## 更新位置的静态紧急地址

`PATCH /external_connections/{id}/locations/{location_id}` — 必需参数：`static_emergency_address_id`

```javascript
const response = await client.externalConnections.updateLocation(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  {
    id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
    static_emergency_address_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  },
);

console.log(response.data);
```

## 列出所有电话号码

返回与给定外部连接关联的所有活跃电话号码列表。

`GET /external_connections/{id}/phone_numbers`

```javascript
// Automatically fetches more pages as needed.
for await (const externalConnectionPhoneNumber of client.externalConnections.phoneNumbers.list(
  'id',
)) {
  console.log(externalConnectionPhoneNumber.civic_address_id);
}
```

## 获取电话号码信息

返回与给定外部连接关联的电话号码的详细信息。

`GET /external_connections/{id}/phone_numbers/{phone_number_id}`

```javascript
const phoneNumber = await client.externalConnections.phoneNumbers.retrieve('1234567889', {
  id: 'id',
});

console.log(phoneNumber.data);
```

## 更新电话号码信息

异步更新与给定外部连接关联的电话号码设置。

`PATCH /external_connections/{id}/phone_numbers/{phone_number_id}`

```javascript
const phoneNumber = await client.externalConnections.phoneNumbers.update('1234567889', {
  id: 'id',
});

console.log(phoneNumber.data);
```

## 列出所有发布记录

返回与给定外部连接关联的所有发布记录列表。

`GET /external_connections/{id}/releases`

```javascript
// Automatically fetches more pages as needed.
for await (const releaseListResponse of client.externalConnections.releases.list('id')) {
  console.log(releaseListResponse.tenant_id);
}
```

## 获取发布请求信息

返回发布请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/releases/{release_id}`

```javascript
const release = await client.externalConnections.releases.retrieve(
  '7b6a6449-b055-45a6-81f6-f6f0dffa4cc6',
  { id: 'id' },
);

console.log(release.data);
```

## 列出所有上传请求

返回与给定外部连接关联的所有上传请求列表。

`GET /external_connections/{id}/uploads`

```javascript
// Automatically fetches more pages as needed.
for await (const upload of client.externalConnections.uploads.list('id')) {
  console.log(upload.location_id);
}
```

## 创建上传请求

创建一个新的上传请求到 Microsoft Teams（包含关联的电话号码）。

`POST /external_connections/{id}/uploads` — 必需参数：`number_ids`

```javascript
const upload = await client.externalConnections.uploads.create('id', {
  number_ids: [
    '3920457616934164700',
    '3920457616934164701',
    '3920457616934164702',
    '3920457616934164703',
  ],
});

console.log(upload.ticket_id);
```

## 刷新所有上传请求的状态

强制重新检查给定外部连接的所有待处理上传请求的状态。

`POST /external_connections/{id}/uploads/refresh`

```javascript
const response = await client.externalConnections.uploads.refreshStatus('id');

console.log(response.success);
```

## 获取待处理上传请求的数量

返回给定外部连接的所有待处理上传请求的数量。

`GET /external_connections/{id}/uploads/status`

```javascript
const response = await client.externalConnections.uploads.pendingCount('id');

console.log(response.data);
```

## 获取上传请求信息

返回上传请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/uploads/{ticket_id}`

```javascript
const upload = await client.externalConnections.uploads.retrieve(
  '7b6a6449-b055-45a6-81f6-f6f0dffa4cc6',
  { id: 'id' },
);

console.log(upload.data);
```

## 重试上传请求

如果上传过程中出现错误，此端点将重试上传请求。

`POST /external_connections/{id}/uploads/{ticket_id}/retry`

```javascript
const response = await client.externalConnections.uploads.retry(
  '7b6a6449-b055-45a6-81f6-f6f0dffa4cc6',
  { id: 'id' },
);

console.log(response.data);
```

## 列出所有日志消息

检索与您的账户关联的所有外部连接的日志消息列表。

`GET /external_connections/log_messages`

```javascript
// Automatically fetches more pages as needed.
for await (const logMessageListResponse of client.externalConnections.logMessages.list()) {
  console.log(logMessageListResponse.code);
}
```

## 获取日志消息

检索与您的账户关联的某个外部连接的日志消息。

`GET /external_connections/log_messages/{id}`

```javascript
const logMessage = await client.externalConnections.logMessages.retrieve('id');

console.log(logMessage.log_messages);
```

## 删除日志消息

删除与您的账户关联的某个外部连接的日志消息。

`DELETE /external_connections/log_messages/{id}`

```javascript
const response = await client.externalConnections.logMessages.dismiss('id');

console.log(response.success);
```

## 刷新 Operator Connect 集成

此端点将异步请求以刷新当前用户与 Microsoft Teams 的 Operator Connect 集成。

`POST /operator_connect/actions/refresh`

```javascript
const response = await client.operatorConnect.actions.refresh();

console.log(response.message);
```

## 列出上传的媒体文件

返回存储的媒体文件列表。

`GET /media`

```javascript
const media = await client.media.list();

console.log(media.data);
```

## 上传媒体文件

将媒体文件上传到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /media` — 必需参数：`media_url`

```javascript
const response = await client.media.upload({ media_url: 'http://www.example.com/audio.mp3' });

console.log(response.data);
```

## 获取存储的媒体文件信息

返回存储的媒体文件的相关信息。

`GET /media/{media_name}`

```javascript
const media = await client.media.retrieve('media_name');

console.log(media.data);
```

## 更新存储的媒体文件

更新存储的媒体文件。

`PUT /media/{media_name}`

```javascript
const media = await client.media.update('media_name');

console.log(media.data);
```

## 删除存储的媒体文件

删除存储的媒体文件。

`DELETE /media/{media_name}`

```javascript
await client.media.delete('media_name');
```

## 下载存储的媒体文件

下载存储的媒体文件。

`GET /media/{media_name}/download`

```javascript
const response = await client.media.download('media_name');

console.log(response);

const content = await response.blob();
console.log(content);
```
```