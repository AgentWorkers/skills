---
name: telnyx-webrtc-java
description: >-
  Manage WebRTC credentials and mobile push notification settings. Use when
  building browser-based or mobile softphone applications. This skill provides
  Java SDK examples.
metadata:
  author: telnyx
  product: webrtc
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Webrtc - Java

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 列出移动推送凭据

`GET /mobile_push_credentials`

```java
import com.telnyx.sdk.models.mobilepushcredentials.MobilePushCredentialListPage;
import com.telnyx.sdk.models.mobilepushcredentials.MobilePushCredentialListParams;

MobilePushCredentialListPage page = client.mobilePushCredentials().list();
```

## 创建新的移动推送凭据

`POST /mobile_push_credentials`

```java
import com.telnyx.sdk.models.mobilepushcredentials.MobilePushCredentialCreateParams;
import com.telnyx.sdk.models.mobilepushcredentials.PushCredentialResponse;

MobilePushCredentialCreateParams params = MobilePushCredentialCreateParams.builder()
    .createMobilePushCredentialRequest(MobilePushCredentialCreateParams.CreateMobilePushCredentialRequest.Ios.builder()
        .alias("LucyIosCredential")
        .certificate("-----BEGIN CERTIFICATE----- MIIGVDCCBTKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END CERTIFICATE-----")
        .privateKey("-----BEGIN RSA PRIVATE KEY----- MIIEpQIBAAKCAQEAsNlRJVZn9ZvXcECQm65czs... -----END RSA PRIVATE KEY-----")
        .build())
    .build();
PushCredentialResponse pushCredentialResponse = client.mobilePushCredentials().create(params);
```

## 获取移动推送凭据

根据给定的 `push_credential_id` 获取移动推送凭据

`GET /mobile_push_credentials/{push_credential_id}`

```java
import com.telnyx.sdk.models.mobilepushcredentials.MobilePushCredentialRetrieveParams;
import com.telnyx.sdk.models.mobilepushcredentials.PushCredentialResponse;

PushCredentialResponse pushCredentialResponse = client.mobilePushCredentials().retrieve("0ccc7b76-4df3-4bca-a05a-3da1ecc389f0");
```

## 删除移动推送凭据

根据给定的 `push_credential_id` 删除移动推送凭据

`DELETE /mobile_push_credentials/{push_credential_id}`

```java
import com.telnyx.sdk.models.mobilepushcredentials.MobilePushCredentialDeleteParams;

client.mobilePushCredentials().delete("0ccc7b76-4df3-4bca-a05a-3da1ecc389f0");
```

## 列出所有凭据

列出所有按需生成的凭据。

`GET /telephony_credentials`

```java
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialListPage;
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialListParams;

TelephonyCredentialListPage page = client.telephonyCredentials().list();
```

## 创建凭据

创建一个新的凭据。

`POST /telephony_credentials` — 必需参数：`connection_id`

```java
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialCreateParams;
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialCreateResponse;

TelephonyCredentialCreateParams params = TelephonyCredentialCreateParams.builder()
    .connectionId("1234567890")
    .build();
TelephonyCredentialCreateResponse telephonyCredential = client.telephonyCredentials().create(params);
```

## 获取凭据详情

获取现有按需生成凭据的详细信息。

`GET /telephony_credentials/{id}`

```java
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialRetrieveParams;
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialRetrieveResponse;

TelephonyCredentialRetrieveResponse telephonyCredential = client.telephonyCredentials().retrieve("id");
```

## 更新凭据

更新现有的凭据。

`PATCH /telephony_credentials/{id}`

```java
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialUpdateParams;
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialUpdateResponse;

TelephonyCredentialUpdateResponse telephonyCredential = client.telephonyCredentials().update("id");
```

## 删除凭据

删除现有的凭据。

`DELETE /telephony_credentials/{id}`

```java
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialDeleteParams;
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialDeleteResponse;

TelephonyCredentialDeleteResponse telephonyCredential = client.telephonyCredentials().delete("id");
```

## 创建访问令牌

为该凭据创建一个访问令牌（JWT）。

`POST /telephony_credentials/{id}/token`

```java
import com.telnyx.sdk.models.telephonycredentials.TelephonyCredentialCreateTokenParams;

String response = client.telephonyCredentials().createToken("id");
```