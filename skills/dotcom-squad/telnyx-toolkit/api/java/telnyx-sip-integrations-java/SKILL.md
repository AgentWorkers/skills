---
name: telnyx-sip-integrations-java
description: >-
  Manage call recordings, media storage, Dialogflow integration, and external
  connections for SIP trunking. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: sip-integrations
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip 集成 - Java

## 安装

```text
// See https://github.com/team-telnyx/telnyx-java for Maven/Gradle setup
```

## 设置

```java
import com.telnyx.sdk.client.TelnyxClient;
import com.telnyx.sdk.client.okhttp.TelnyxOkHttpClient;

TelnyxClient client = TelnyxOkHttpClient.fromEnv();
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出所有通话记录

返回您的通话记录列表。

`GET /recordings`

```java
import com.telnyx.sdk.models.recordings.RecordingListPage;
import com.telnyx.sdk.models.recordings.RecordingListParams;

RecordingListPage page = client.recordings().list();
```

## 获取通话记录

检索现有通话记录的详细信息。

`GET /recordings/{recording_id}`

```java
import com.telnyx.sdk.models.recordings.RecordingRetrieveParams;
import com.telnyx.sdk.models.recordings.RecordingRetrieveResponse;

RecordingRetrieveResponse recording = client.recordings().retrieve("recording_id");
```

## 删除通话记录

永久删除通话记录。

`DELETE /recordings/{recording_id}`

```java
import com.telnyx.sdk.models.recordings.RecordingDeleteParams;
import com.telnyx.sdk.models.recordings.RecordingDeleteResponse;

RecordingDeleteResponse recording = client.recordings().delete("recording_id");
```

## 删除通话记录列表

永久删除通话记录列表。

`POST /recordings/actions/delete`

```java
import com.telnyx.sdk.models.recordings.actions.ActionDeleteParams;

ActionDeleteParams params = ActionDeleteParams.builder()
    .addId("428c31b6-7af4-4bcb-b7f5-5013ef9657c1")
    .addId("428c31b6-7af4-4bcb-b7f5-5013ef9657c2")
    .build();
client.recordings().actions().delete(params);
```

## 列出所有通话转录内容

返回您的通话转录内容列表。

`GET /recording_transcriptions`

```java
import com.telnyx.sdk.models.recordingtranscriptions.RecordingTranscriptionListParams;
import com.telnyx.sdk.models.recordingtranscriptions.RecordingTranscriptionListResponse;

RecordingTranscriptionListResponse recordingTranscriptions = client.recordingTranscriptions().list();
```

## 获取通话转录内容

检索现有通话转录内容的详细信息。

`GET /recording_transcriptions/{recording_transcription_id}`

```java
import com.telnyx.sdk.models.recordingtranscriptions.RecordingTranscriptionRetrieveParams;
import com.telnyx.sdk.models.recordingtranscriptions.RecordingTranscriptionRetrieveResponse;

RecordingTranscriptionRetrieveResponse recordingTranscription = client.recordingTranscriptions().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 删除通话转录内容

永久删除通话转录内容。

`DELETE /recording_transcriptions/{recording_transcription_id}`

```java
import com.telnyx.sdk.models.recordingtranscriptions.RecordingTranscriptionDeleteParams;
import com.telnyx.sdk.models.recordingtranscriptions.RecordingTranscriptionDeleteResponse;

RecordingTranscriptionDeleteResponse recordingTranscription = client.recordingTranscriptions().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 获取存储的凭据

返回关于自定义存储凭据的信息。

`GET /custom_storage_credentials/{connection_id}`

```java
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageCredentialRetrieveParams;
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageCredentialRetrieveResponse;

CustomStorageCredentialRetrieveResponse customStorageCredential = client.customStorageCredentials().retrieve("connection_id");
```

## 创建自定义存储凭据

创建自定义存储凭据配置。

`POST /custom_storage_credentials/{connection_id}`

```java
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageConfiguration;
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageCredentialCreateParams;
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageCredentialCreateResponse;
import com.telnyx.sdk.models.customstoragecredentials.GcsConfigurationData;

CustomStorageCredentialCreateParams params = CustomStorageCredentialCreateParams.builder()
    .connectionId("connection_id")
    .customStorageConfiguration(CustomStorageConfiguration.builder()
        .backend(CustomStorageConfiguration.Backend.GCS)
        .configuration(GcsConfigurationData.builder()
            .backend(GcsConfigurationData.Backend.GCS)
            .build())
        .build())
    .build();
CustomStorageCredentialCreateResponse customStorageCredential = client.customStorageCredentials().create(params);
```

## 更新存储的凭据

更新存储的自定义凭据配置。

`PUT /custom_storage_credentials/{connection_id}`

```java
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageConfiguration;
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageCredentialUpdateParams;
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageCredentialUpdateResponse;
import com.telnyx.sdk.models.customstoragecredentials.GcsConfigurationData;

CustomStorageCredentialUpdateParams params = CustomStorageCredentialUpdateParams.builder()
    .connectionId("connection_id")
    .customStorageConfiguration(CustomStorageConfiguration.builder()
        .backend(CustomStorageConfiguration.Backend.GCS)
        .configuration(GcsConfigurationData.builder()
            .backend(GcsConfigurationData.Backend.GCS)
            .build())
        .build())
    .build();
CustomStorageCredentialUpdateResponse customStorageCredential = client.customStorageCredentials().update(params);
```

## 删除存储的凭据

删除存储的自定义凭据配置。

`DELETE /custom_storage_credentials/{connection_id}`

```java
import com.telnyx.sdk.models.customstoragecredentials.CustomStorageCredentialDeleteParams;

client.customStorageCredentials().delete("connection_id");
```

## 获取存储的 Dialogflow 连接信息

返回与给定 CallControl 连接关联的 Dialogflow 连接的详细信息。

`GET /dialogflow_connections/{connection_id}`

```java
import com.telnyx.sdk.models.dialogflowconnections.DialogflowConnectionRetrieveParams;
import com.telnyx.sdk.models.dialogflowconnections.DialogflowConnectionRetrieveResponse;

DialogflowConnectionRetrieveResponse dialogflowConnection = client.dialogflowConnections().retrieve("connection_id");
```

## 创建 Dialogflow 连接

将 Dialogflow 凭据保存到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /dialogflow_connections/{connection_id}`

```java
import com.telnyx.sdk.core.JsonValue;
import com.telnyx.sdk.models.dialogflowconnections.DialogflowConnectionCreateParams;
import com.telnyx.sdk.models.dialogflowconnections.DialogflowConnectionCreateResponse;

DialogflowConnectionCreateParams params = DialogflowConnectionCreateParams.builder()
    .connectionId("connection_id")
    .serviceAccount(DialogflowConnectionCreateParams.ServiceAccount.builder()
        .putAdditionalProperty("type", JsonValue.from("bar"))
        .putAdditionalProperty("project_id", JsonValue.from("bar"))
        .putAdditionalProperty("private_key_id", JsonValue.from("bar"))
        .putAdditionalProperty("private_key", JsonValue.from("bar"))
        .putAdditionalProperty("client_email", JsonValue.from("bar"))
        .putAdditionalProperty("client_id", JsonValue.from("bar"))
        .putAdditionalProperty("auth_uri", JsonValue.from("bar"))
        .putAdditionalProperty("token_uri", JsonValue.from("bar"))
        .putAdditionalProperty("auth_provider_x509_cert_url", JsonValue.from("bar"))
        .putAdditionalProperty("client_x509_cert_url", JsonValue.from("bar"))
        .build())
    .build();
DialogflowConnectionCreateResponse dialogflowConnection = client.dialogflowConnections().create(params);
```

## 更新存储的 Dialogflow 连接

更新存储的 Dialogflow 连接信息。

`PUT /dialogflow_connections/{connection_id}`

```java
import com.telnyx.sdk.core.JsonValue;
import com.telnyx.sdk.models.dialogflowconnections.DialogflowConnectionUpdateParams;
import com.telnyx.sdk.models.dialogflowconnections.DialogflowConnectionUpdateResponse;

DialogflowConnectionUpdateParams params = DialogflowConnectionUpdateParams.builder()
    .connectionId("connection_id")
    .serviceAccount(DialogflowConnectionUpdateParams.ServiceAccount.builder()
        .putAdditionalProperty("type", JsonValue.from("bar"))
        .putAdditionalProperty("project_id", JsonValue.from("bar"))
        .putAdditionalProperty("private_key_id", JsonValue.from("bar"))
        .putAdditionalProperty("private_key", JsonValue.from("bar"))
        .putAdditionalProperty("client_email", JsonValue.from("bar"))
        .putAdditionalProperty("client_id", JsonValue.from("bar"))
        .putAdditionalProperty("auth_uri", JsonValue.from("bar"))
        .putAdditionalProperty("token_uri", JsonValue.from("bar"))
        .putAdditionalProperty("auth_provider_x509_cert_url", JsonValue.from("bar"))
        .putAdditionalProperty("client_x509_cert_url", JsonValue.from("bar"))
        .build())
    .build();
DialogflowConnectionUpdateResponse dialogflowConnection = client.dialogflowConnections().update(params);
```

## 删除存储的 Dialogflow 连接

删除存储的 Dialogflow 连接。

`DELETE /dialogflow_connections/{connection_id}`

```java
import com.telnyx.sdk.models.dialogflowconnections.DialogflowConnectionDeleteParams;

client.dialogflowConnections().delete("connection_id");
```

## 列出所有外部连接

此端点会返回响应中的 "data" 属性所包含的所有外部连接列表。

`GET /external_connections`

```java
import com.telnyx.sdk.models.externalconnections.ExternalConnectionListPage;
import com.telnyx.sdk.models.externalconnections.ExternalConnectionListParams;

ExternalConnectionListPage page = client.externalConnections().list();
```

## 创建外部连接

根据请求中发送的参数创建新的外部连接。

`POST /external_connections` — 必需参数：`external_sip_connection`, `outbound`

```java
import com.telnyx.sdk.models.externalconnections.ExternalConnectionCreateParams;
import com.telnyx.sdk.models.externalconnections.ExternalConnectionCreateResponse;

ExternalConnectionCreateParams params = ExternalConnectionCreateParams.builder()
    .externalSipConnection(ExternalConnectionCreateParams.ExternalSipConnection.ZOOM)
    .outbound(ExternalConnectionCreateParams.Outbound.builder().build())
    .build();
ExternalConnectionCreateResponse externalConnection = client.externalConnections().create(params);
```

## 获取外部连接信息

返回响应中的 "data" 属性所包含的现有外部连接的详细信息。

`GET /external_connections/{id}`

```java
import com.telnyx.sdk.models.externalconnections.ExternalConnectionRetrieveParams;
import com.telnyx.sdk.models.externalconnections.ExternalConnectionRetrieveResponse;

ExternalConnectionRetrieveResponse externalConnection = client.externalConnections().retrieve("id");
```

## 更新外部连接

根据请求的参数更新现有外部连接的设置。

`PATCH /external_connections/{id}` — 必需参数：`outbound`

```java
import com.telnyx.sdk.models.externalconnections.ExternalConnectionUpdateParams;
import com.telnyx.sdk.models.externalconnections.ExternalConnectionUpdateResponse;

ExternalConnectionUpdateParams params = ExternalConnectionUpdateParams.builder()
    .id("id")
    .outbound(ExternalConnectionUpdateParams.Outbound.builder()
        .outboundVoiceProfileId("outbound_voice_profile_id")
        .build())
    .build();
ExternalConnectionUpdateResponse externalConnection = client.externalConnections().update(params);
```

## 删除外部连接

永久删除外部连接。

`DELETE /external_connections/{id}`

```java
import com.telnyx.sdk.models.externalconnections.ExternalConnectionDeleteParams;
import com.telnyx.sdk.models.externalconnections.ExternalConnectionDeleteResponse;

ExternalConnectionDeleteResponse externalConnection = client.externalConnections().delete("id");
```

## 列出所有公民地址和位置信息

从 Microsoft Teams 中获取公民地址和位置信息。

`GET /external_connections/{id}/civic_addresses`

```java
import com.telnyx.sdk.models.externalconnections.civicaddresses.CivicAddressListParams;
import com.telnyx.sdk.models.externalconnections.civicaddresses.CivicAddressListResponse;

CivicAddressListResponse civicAddresses = client.externalConnections().civicAddresses().list("id");
```

## 获取公民地址信息

返回响应中的 "data" 属性所包含的现有公民地址及其位置的详细信息。

`GET /external_connections/{id}/civic_addresses/{address_id}`

```java
import com.telnyx.sdk.models.externalconnections.civicaddresses.CivicAddressRetrieveParams;
import com.telnyx.sdk.models.externalconnections.civicaddresses.CivicAddressRetrieveResponse;

CivicAddressRetrieveParams params = CivicAddressRetrieveParams.builder()
    .id("id")
    .addressId("318fb664-d341-44d2-8405-e6bfb9ced6d9")
    .build();
CivicAddressRetrieveResponse civicAddress = client.externalConnections().civicAddresses().retrieve(params);
```

## 更新位置的静态紧急地址

`PATCH /external_connections/{id}/locations/{location_id}` — 必需参数：`static_emergency_address_id`

```java
import com.telnyx.sdk.models.externalconnections.ExternalConnectionUpdateLocationParams;
import com.telnyx.sdk.models.externalconnections.ExternalConnectionUpdateLocationResponse;

ExternalConnectionUpdateLocationParams params = ExternalConnectionUpdateLocationParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .locationId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .staticEmergencyAddressId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
ExternalConnectionUpdateLocationResponse response = client.externalConnections().updateLocation(params);
```

## 列出所有电话号码

返回与给定外部连接关联的所有活动电话号码列表。

`GET /external_connections/{id}/phone_numbers`

```java
import com.telnyx.sdk.models.externalconnections.phonenumbers.PhoneNumberListPage;
import com.telnyx.sdk.models.externalconnections.phonenumbers.PhoneNumberListParams;

PhoneNumberListPage page = client.externalConnections().phoneNumbers().list("id");
```

## 获取电话号码信息

返回与给定外部连接关联的电话号码的详细信息。

`GET /external_connections/{id}/phone_numbers/{phone_number_id}`

```java
import com.telnyx.sdk.models.externalconnections.phonenumbers.PhoneNumberRetrieveParams;
import com.telnyx.sdk.models.externalconnections.phonenumbers.PhoneNumberRetrieveResponse;

PhoneNumberRetrieveParams params = PhoneNumberRetrieveParams.builder()
    .id("id")
    .phoneNumberId("1234567889")
    .build();
PhoneNumberRetrieveResponse phoneNumber = client.externalConnections().phoneNumbers().retrieve(params);
```

## 更新电话号码信息

异步更新与给定外部连接关联的电话号码的设置。

`PATCH /external_connections/{id}/phone_numbers/{phone_number_id}`

```java
import com.telnyx.sdk.models.externalconnections.phonenumbers.PhoneNumberUpdateParams;
import com.telnyx.sdk.models.externalconnections.phonenumbers.PhoneNumberUpdateResponse;

PhoneNumberUpdateParams params = PhoneNumberUpdateParams.builder()
    .id("id")
    .phoneNumberId("1234567889")
    .build();
PhoneNumberUpdateResponse phoneNumber = client.externalConnections().phoneNumbers().update(params);
```

## 列出所有发布记录

返回与给定外部连接关联的所有发布记录列表。

`GET /external_connections/{id}/releases`

```java
import com.telnyx.sdk.models.externalconnections.releases.ReleaseListPage;
import com.telnyx.sdk.models.externalconnections.releases.ReleaseListParams;

ReleaseListPage page = client.externalConnections().releases().list("id");
```

## 获取发布请求信息

返回发布请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/releases/{release_id}`

```java
import com.telnyx.sdk.models.externalconnections.releases.ReleaseRetrieveParams;
import com.telnyx.sdk.models.externalconnections.releases.ReleaseRetrieveResponse;

ReleaseRetrieveParams params = ReleaseRetrieveParams.builder()
    .id("id")
    .releaseId("7b6a6449-b055-45a6-81f6-f6f0dffa4cc6")
    .build();
ReleaseRetrieveResponse release = client.externalConnections().releases().retrieve(params);
```

## 列出所有上传请求

返回与给定外部连接关联的所有上传请求列表。

`GET /external_connections/{id}/uploads`

```java
import com.telnyx.sdk.models.externalconnections.uploads.UploadListPage;
import com.telnyx.sdk.models.externalconnections.uploads.UploadListParams;

UploadListPage page = client.externalConnections().uploads().list("id");
```

## 创建上传请求

创建一个新的上传请求，关联指定的电话号码。

`POST /external_connections/{id}/uploads` — 必需参数：`number_ids`

```java
import com.telnyx.sdk.models.externalconnections.uploads.UploadCreateParams;
import com.telnyx.sdk.models.externalconnections.uploads.UploadCreateResponse;
import java.util.List;

UploadCreateParams params = UploadCreateParams.builder()
    .id("id")
    .numberIds(List.of(
      "3920457616934164700",
      "3920457616934164701",
      "3920457616934164702",
      "3920457616934164703"
    ))
    .build();
UploadCreateResponse upload = client.externalConnections().uploads().create(params);
```

## 刷新所有上传请求的状态

强制重新检查给定外部连接的所有待处理上传请求的状态。

`POST /external_connections/{id}/uploads/refresh`

```java
import com.telnyx.sdk.models.externalconnections.uploads.UploadRefreshStatusParams;
import com.telnyx.sdk.models.externalconnections.uploads.UploadRefreshStatusResponse;

UploadRefreshStatusResponse response = client.externalConnections().uploads().refreshStatus("id");
```

## 获取待处理上传请求的数量

返回给定外部连接的所有待处理上传请求的数量。

`GET /external_connections/{id}/uploads/status`

```java
import com.telnyx.sdk.models.externalconnections.uploads.UploadPendingCountParams;
import com.telnyx.sdk.models.externalconnections.uploads.UploadPendingCountResponse;

UploadPendingCountResponse response = client.externalConnections().uploads().pendingCount("id");
```

## 获取上传请求信息

返回上传请求的详细信息及其关联的电话号码。

`GET /external_connections/{id}/uploads/{ticket_id}`

```java
import com.telnyx.sdk.models.externalconnections.uploads.UploadRetrieveParams;
import com.telnyx.sdk.models.externalconnections.uploads.UploadRetrieveResponse;

UploadRetrieveParams params = UploadRetrieveParams.builder()
    .id("id")
    .ticketId("7b6a6449-b055-45a6-81f6-f6f0dffa4cc6")
    .build();
UploadRetrieveResponse upload = client.externalConnections().uploads().retrieve(params);
```

## 重试上传请求

如果上传过程中出现错误，此端点将重试上传请求。

`POST /external_connections/{id}/uploads/{ticket_id}/retry`

```java
import com.telnyx.sdk.models.externalconnections.uploads.UploadRetryParams;
import com.telnyx.sdk.models.externalconnections.uploads.UploadRetryResponse;

UploadRetryParams params = UploadRetryParams.builder()
    .id("id")
    .ticketId("7b6a6449-b055-45a6-81f6-f6f0dffa4cc6")
    .build();
UploadRetryResponse response = client.externalConnections().uploads().retry(params);
```

## 列出所有日志消息

检索与您的账户关联的所有外部连接的日志消息列表。

`GET /external_connections/log_messages`

```java
import com.telnyx.sdk.models.externalconnections.logmessages.LogMessageListPage;
import com.telnyx.sdk.models.externalconnections.logmessages.LogMessageListParams;

LogMessageListPage page = client.externalConnections().logMessages().list();
```

## 获取日志消息

检索与您的账户关联的某个外部连接的日志消息。

`GET /external_connections/log_messages/{id}`

```java
import com.telnyx.sdk.models.externalconnections.logmessages.LogMessageRetrieveParams;
import com.telnyx.sdk.models.externalconnections.logmessages.LogMessageRetrieveResponse;

LogMessageRetrieveResponse logMessage = client.externalConnections().logMessages().retrieve("id");
```

## 删除日志消息

删除与您的账户关联的某个外部连接的日志消息。

`DELETE /external_connections/log_messages/{id}`

```java
import com.telnyx.sdk.models.externalconnections.logmessages.LogMessageDismissParams;
import com.telnyx.sdk.models.externalconnections.logmessages.LogMessageDismissResponse;

LogMessageDismissResponse response = client.externalConnections().logMessages().dismiss("id");
```

## 刷新 Operator Connect 集成

此端点将异步请求以刷新当前用户与 Microsoft Teams 的 Operator Connect 集成。

`POST /operator_connect/actions/refresh`

```java
import com.telnyx.sdk.models.operatorconnect.actions.ActionRefreshParams;
import com.telnyx.sdk.models.operatorconnect.actions.ActionRefreshResponse;

ActionRefreshResponse response = client.operatorConnect().actions().refresh();
```

## 列出上传的媒体文件

返回存储的媒体文件列表。

`GET /media`

```java
import com.telnyx.sdk.models.media.MediaListParams;
import com.telnyx.sdk.models.media.MediaListResponse;

MediaListResponse media = client.media().list();
```

## 上传媒体文件

将媒体文件上传到 Telnyx，以便与其他 Telnyx 服务一起使用。

`POST /media` — 必需参数：`media_url`

```java
import com.telnyx.sdk.models.media.MediaUploadParams;
import com.telnyx.sdk.models.media.MediaUploadResponse;

MediaUploadParams params = MediaUploadParams.builder()
    .mediaUrl("http://www.example.com/audio.mp3")
    .build();
MediaUploadResponse response = client.media().upload(params);
```

## 获取存储的媒体文件信息

返回存储的媒体文件的详细信息。

`GET /media/{media_name}`

```java
import com.telnyx.sdk.models.media.MediaRetrieveParams;
import com.telnyx.sdk.models.media.MediaRetrieveResponse;

MediaRetrieveResponse media = client.media().retrieve("media_name");
```

## 更新存储的媒体文件

更新存储的媒体文件。

`PUT /media/{media_name}`

```java
import com.telnyx.sdk.models.media.MediaUpdateParams;
import com.telnyx.sdk.models.media.MediaUpdateResponse;

MediaUpdateResponse media = client.media().update("media_name");
```

## 删除存储的媒体文件

删除存储的媒体文件。

`DELETE /media/{media_name}`

```java
import com.telnyx.sdk.models.media.MediaDeleteParams;

client.media().delete("media_name");
```

## 下载存储的媒体文件

下载存储的媒体文件。

`GET /media/{media_name}/download`

```java
import com.telnyx.sdk.core.http.HttpResponse;
import com.telnyx.sdk.models.media.MediaDownloadParams;

HttpResponse response = client.media().download("media_name");
```
```