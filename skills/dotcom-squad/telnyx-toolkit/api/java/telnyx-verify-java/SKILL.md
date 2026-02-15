---
name: telnyx-verify-java
description: >-
  Look up phone number information (carrier, type, caller name) and verify users
  via SMS/voice OTP. Use for phone verification and data enrichment. This skill
  provides Java SDK examples.
metadata:
  author: telnyx
  product: verify
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Verify - Java

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 查找电话号码信息

返回关于提供的电话号码的信息。

`GET /number_lookup/{phone_number}`

```java
import com.telnyx.sdk.models.numberlookup.NumberLookupRetrieveParams;
import com.telnyx.sdk.models.numberlookup.NumberLookupRetrieveResponse;

NumberLookupRetrieveResponse numberLookup = client.numberLookup().retrieve("+18665552368");
```

## 触发电话验证

`POST /verifications/call` — 必需参数：`phone_number`, `verify_profile_id`

```java
import com.telnyx.sdk.models.verifications.CreateVerificationResponse;
import com.telnyx.sdk.models.verifications.VerificationTriggerCallParams;

VerificationTriggerCallParams params = VerificationTriggerCallParams.builder()
    .phoneNumber("+13035551234")
    .verifyProfileId("12ade33a-21c0-473b-b055-b3c836e1c292")
    .build();
CreateVerificationResponse createVerificationResponse = client.verifications().triggerCall(params);
```

## 触发闪现式电话验证

`POST /verifications/flashcall` — 必需参数：`phone_number`, `verify_profile_id`

```java
import com.telnyx.sdk.models.verifications.CreateVerificationResponse;
import com.telnyx.sdk.models.verifications.VerificationTriggerFlashcallParams;

VerificationTriggerFlashcallParams params = VerificationTriggerFlashcallParams.builder()
    .phoneNumber("+13035551234")
    .verifyProfileId("12ade33a-21c0-473b-b055-b3c836e1c292")
    .build();
CreateVerificationResponse createVerificationResponse = client.verifications().triggerFlashcall(params);
```

## 触发短信验证

`POST /verifications/sms` — 必需参数：`phone_number`, `verify_profile_id`

```java
import com.telnyx.sdk.models.verifications.CreateVerificationResponse;
import com.telnyx.sdk.models.verifications.VerificationTriggerSmsParams;

VerificationTriggerSmsParams params = VerificationTriggerSmsParams.builder()
    .phoneNumber("+13035551234")
    .verifyProfileId("12ade33a-21c0-473b-b055-b3c836e1c292")
    .build();
CreateVerificationResponse createVerificationResponse = client.verifications().triggerSms(params);
```

## 获取验证结果

`GET /verifications/{verification_id}`

```java
import com.telnyx.sdk.models.verifications.VerificationRetrieveParams;
import com.telnyx.sdk.models.verifications.VerificationRetrieveResponse;

VerificationRetrieveResponse verification = client.verifications().retrieve("12ade33a-21c0-473b-b055-b3c836e1c292");
```

## 根据 ID 验证验证码

`POST /verifications/{verification_id}/actions/verify`

```java
import com.telnyx.sdk.models.verifications.actions.ActionVerifyParams;
import com.telnyx.sdk.models.verifications.byphonenumber.actions.VerifyVerificationCodeResponse;

VerifyVerificationCodeResponse verifyVerificationCodeResponse = client.verifications().actions().verify("12ade33a-21c0-473b-b055-b3c836e1c292");
```

## 按电话号码列出验证记录

`GET /verifications/by_phone_number/{phone_number}`

```java
import com.telnyx.sdk.models.verifications.byphonenumber.ByPhoneNumberListParams;
import com.telnyx.sdk.models.verifications.byphonenumber.ByPhoneNumberListResponse;

ByPhoneNumberListResponse byPhoneNumbers = client.verifications().byPhoneNumber().list("+13035551234");
```

## 根据电话号码验证验证码

`POST /verifications/by_phone_number/{phone_number}/actions/verify` — 必需参数：`code`, `verify_profile_id`

```java
import com.telnyx.sdk.models.verifications.byphonenumber.actions.ActionVerifyParams;
import com.telnyx.sdk.models.verifications.byphonenumber.actions.VerifyVerificationCodeResponse;

ActionVerifyParams params = ActionVerifyParams.builder()
    .phoneNumber("+13035551234")
    .code("17686")
    .verifyProfileId("12ade33a-21c0-473b-b055-b3c836e1c292")
    .build();
VerifyVerificationCodeResponse verifyVerificationCodeResponse = client.verifications().byPhoneNumber().actions().verify(params);
```

## 列出所有验证配置文件

获取分页显示的验证配置文件列表。

`GET /verify_profiles`

```java
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileListPage;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileListParams;

VerifyProfileListPage page = client.verifyProfiles().list();
```

## 创建验证配置文件

创建一个新的验证配置文件，用于关联验证操作。

`POST /verify_profiles` — 必需参数：`name`

```java
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileCreateParams;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileData;

VerifyProfileCreateParams params = VerifyProfileCreateParams.builder()
    .name("Test Profile")
    .build();
VerifyProfileData verifyProfileData = client.verifyProfiles().create(params);
```

## 获取验证配置文件信息

获取单个验证配置文件的信息。

`GET /verify_profiles/{verify_profile_id}`

```java
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileData;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileRetrieveParams;

VerifyProfileData verifyProfileData = client.verifyProfiles().retrieve("12ade33a-21c0-473b-b055-b3c836e1c292");
```

## 更新验证配置文件

`PATCH /verify_profiles/{verify_profile_id}`

```java
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileData;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileUpdateParams;

VerifyProfileData verifyProfileData = client.verifyProfiles().update("12ade33a-21c0-473b-b055-b3c836e1c292");
```

## 删除验证配置文件

`DELETE /verify_profiles/{verify_profile_id}`

```java
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileData;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileDeleteParams;

VerifyProfileData verifyProfileData = client.verifyProfiles().delete("12ade33a-21c0-473b-b055-b3c836e1c292");
```

## 获取验证配置文件消息模板

列出所有的验证配置文件消息模板。

`GET /verify_profiles/templates`

```java
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileRetrieveTemplatesParams;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileRetrieveTemplatesResponse;

VerifyProfileRetrieveTemplatesResponse response = client.verifyProfiles().retrieveTemplates();
```

## 创建消息模板

创建一个新的验证配置文件消息模板。

`POST /verify_profiles/templates` — 必需参数：`text`

```java
import com.telnyx.sdk.models.verifyprofiles.MessageTemplate;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileCreateTemplateParams;

VerifyProfileCreateTemplateParams params = VerifyProfileCreateTemplateParams.builder()
    .text("Your {{app_name}} verification code is: {{code}}.")
    .build();
MessageTemplate messageTemplate = client.verifyProfiles().createTemplate(params);
```

## 更新消息模板

更新现有的验证配置文件消息模板。

`PATCH /verify_profiles/templates/{template_id}` — 必需参数：`text`

```java
import com.telnyx.sdk.models.verifyprofiles.MessageTemplate;
import com.telnyx.sdk.models.verifyprofiles.VerifyProfileUpdateTemplateParams;

VerifyProfileUpdateTemplateParams params = VerifyProfileUpdateTemplateParams.builder()
    .templateId("12ade33a-21c0-473b-b055-b3c836e1c292")
    .text("Your {{app_name}} verification code is: {{code}}.")
    .build();
MessageTemplate messageTemplate = client.verifyProfiles().updateTemplate(params);
```