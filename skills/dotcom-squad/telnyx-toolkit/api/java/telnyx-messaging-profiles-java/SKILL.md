---
name: telnyx-messaging-profiles-java
description: >-
  Create and manage messaging profiles with number pools, sticky sender, and
  geomatch features. Configure short codes for high-volume messaging. This skill
  provides Java SDK examples.
metadata:
  author: telnyx
  product: messaging-profiles
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息传递配置文件 - Java

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

## 列出消息传递配置文件

`GET /messaging_profiles`

```java
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileListPage;
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileListParams;

MessagingProfileListPage page = client.messagingProfiles().list();
```

## 创建消息传递配置文件

`POST /messaging_profiles` — 必需参数：`name`、`whitelisted_destinations`

```java
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileCreateParams;
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileCreateResponse;

MessagingProfileCreateParams params = MessagingProfileCreateParams.builder()
    .name("My name")
    .addWhitelistedDestination("US")
    .build();
MessagingProfileCreateResponse messagingProfile = client.messagingProfiles().create(params);
```

## 获取消息传递配置文件

`GET /messagingprofiles/{id}`

```java
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileRetrieveParams;
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileRetrieveResponse;

MessagingProfileRetrieveResponse messagingProfile = client.messagingProfiles().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 更新消息传递配置文件

`PATCH /messagingprofiles/{id}`

```java
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileUpdateParams;
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileUpdateResponse;

MessagingProfileUpdateResponse messagingProfile = client.messagingProfiles().update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除消息传递配置文件

`DELETE /messagingprofiles/{id}`

```java
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileDeleteParams;
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileDeleteResponse;

MessagingProfileDeleteResponse messagingProfile = client.messagingProfiles().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取与消息传递配置文件关联的电话号码

`GET /messagingprofiles/{id}/phone_numbers`

```java
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileListPhoneNumbersPage;
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileListPhoneNumbersParams;

MessagingProfileListPhoneNumbersPage page = client.messagingProfiles().listPhoneNumbers("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取与消息传递配置文件关联的短代码

`GET /messagingprofiles/{id}/short_codes`

```java
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileListShortCodesPage;
import com.telnyx.sdk.models.messagingprofiles.MessagingProfileListShortCodesParams;

MessagingProfileListShortCodesPage page = client.messagingProfiles().listShortCodes("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 查看自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs`

```java
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutorespConfigListParams;
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutorespConfigListResponse;

AutorespConfigListResponse autorespConfigs = client.messagingProfiles().autorespConfigs().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 创建自动应答设置

`POST /messagingprofiles/{profile_id}/autoresp_configs` — 必需参数：`op`、`keywords`、`country_code`

```java
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutoRespConfigCreate;
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutoRespConfigResponse;
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutorespConfigCreateParams;

AutorespConfigCreateParams params = AutorespConfigCreateParams.builder()
    .profileId("profile_id")
    .autoRespConfigCreate(AutoRespConfigCreate.builder()
        .countryCode("US")
        .addKeyword("keyword1")
        .addKeyword("keyword2")
        .op(AutoRespConfigCreate.Op.START)
        .build())
    .build();
AutoRespConfigResponse autoRespConfigResponse = client.messagingProfiles().autorespConfigs().create(params);
```

## 获取自动应答设置

`GET /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```java
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutoRespConfigResponse;
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutorespConfigRetrieveParams;

AutorespConfigRetrieveParams params = AutorespConfigRetrieveParams.builder()
    .profileId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .autorespCfgId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
AutoRespConfigResponse autoRespConfigResponse = client.messagingProfiles().autorespConfigs().retrieve(params);
```

## 更新自动应答设置

`PUT /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}` — 必需参数：`op`、`keywords`、`country_code`

```java
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutoRespConfigCreate;
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutoRespConfigResponse;
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutorespConfigUpdateParams;

AutorespConfigUpdateParams params = AutorespConfigUpdateParams.builder()
    .profileId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .autorespCfgId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .autoRespConfigCreate(AutoRespConfigCreate.builder()
        .countryCode("US")
        .addKeyword("keyword1")
        .addKeyword("keyword2")
        .op(AutoRespConfigCreate.Op.START)
        .build())
    .build();
AutoRespConfigResponse autoRespConfigResponse = client.messagingProfiles().autorespConfigs().update(params);
```

## 删除自动应答设置

`DELETE /messagingprofiles/{profile_id}/autoresp_configs/{autoresp_cfg_id}`

```java
import com.telnyx.sdk.models.messagingprofiles.autorespconfigs.AutorespConfigDeleteParams;

AutorespConfigDeleteParams params = AutorespConfigDeleteParams.builder()
    .profileId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .autorespCfgId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
String autorespConfig = client.messagingProfiles().autorespConfigs().delete(params);
```

## 列出所有短代码

`GET /short_codes`

```java
import com.telnyx.sdk.models.shortcodes.ShortCodeListPage;
import com.telnyx.sdk.models.shortcodes.ShortCodeListParams;

ShortCodeListPage page = client.shortCodes().list();
```

## 获取指定短代码的信息

`GET /short_codes/{id}`

```java
import com.telnyx.sdk.models.shortcodes.ShortCodeRetrieveParams;
import com.telnyx.sdk.models.shortcodes.ShortCodeRetrieveResponse;

ShortCodeRetrieveResponse shortCode = client.shortCodes().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 更新短代码的设置

`PATCH /short_codes/{id}` — 必需参数：`messaging_profile_id`

```java
import com.telnyx.sdk.models.shortcodes.ShortCodeUpdateParams;
import com.telnyx.sdk.models.shortcodes.ShortCodeUpdateResponse;

ShortCodeUpdateParams params = ShortCodeUpdateParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .messagingProfileId("abc85f64-5717-4562-b3fc-2c9600000000")
    .build();
ShortCodeUpdateResponse shortCode = client.shortCodes().update(params);
```