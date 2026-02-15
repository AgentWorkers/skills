---
name: telnyx-numbers-config-java
description: >-
  Configure phone number settings including caller ID, call forwarding,
  messaging enablement, and connection assignments. This skill provides Java SDK
  examples.
metadata:
  author: telnyx
  product: numbers-config
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字配置 - Java

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

## 列出电话号码块任务

`GET /phone_number_blocks/jobs`

```java
import com.telnyx.sdk.models.phonenumberblocks.jobs.JobListPage;
import com.telnyx.sdk.models.phonenumberblocks.jobs.JobListParams;

JobListPage page = client.phoneNumberBlocks().jobs().list();
```

## 获取电话号码块任务信息

`GET /phone_number_blocks/jobs/{id}`

```java
import com.telnyx.sdk.models.phonenumberblocks.jobs.JobRetrieveParams;
import com.telnyx.sdk.models.phonenumberblocks.jobs.JobRetrieveResponse;

JobRetrieveResponse job = client.phoneNumberBlocks().jobs().retrieve("id");
```

## 删除与电话号码块关联的所有号码

创建一个新的后台任务，以删除与指定块关联的所有号码。

`POST /phone_number_blocks/jobs/delete_phone_number_block` — 必需参数：`phone_number_block_id`

```java
import com.telnyx.sdk.models.phonenumberblocks.jobs.JobDeletePhoneNumberBlockParams;
import com.telnyx.sdk.models.phonenumberblocks.jobs.JobDeletePhoneNumberBlockResponse;

JobDeletePhoneNumberBlockParams params = JobDeletePhoneNumberBlockParams.builder()
    .phoneNumberBlockId("f3946371-7199-4261-9c3d-81a0d7935146")
    .build();
JobDeletePhoneNumberBlockResponse response = client.phoneNumberBlocks().jobs().deletePhoneNumberBlock(params);
```

## 列出电话号码

`GET /phone_numbers`

```java
import com.telnyx.sdk.models.phonenumbers.PhoneNumberListPage;
import com.telnyx.sdk.models.phonenumbers.PhoneNumberListParams;

PhoneNumberListPage page = client.phoneNumbers().list();
```

## 获取电话号码信息

`GET /phone_numbers/{id}`

```java
import com.telnyx.sdk.models.phonenumbers.PhoneNumberRetrieveParams;
import com.telnyx.sdk.models.phonenumbers.PhoneNumberRetrieveResponse;

PhoneNumberRetrieveResponse phoneNumber = client.phoneNumbers().retrieve("1293384261075731499");
```

## 更新电话号码信息

`PATCH /phone_numbers/{id}`

```java
import com.telnyx.sdk.models.phonenumbers.PhoneNumberUpdateParams;
import com.telnyx.sdk.models.phonenumbers.PhoneNumberUpdateResponse;

PhoneNumberUpdateResponse phoneNumber = client.phoneNumbers().update("1293384261075731499");
```

## 删除电话号码

`DELETE /phone_numbers/{id}`

```java
import com.telnyx.sdk.models.phonenumbers.PhoneNumberDeleteParams;
import com.telnyx.sdk.models.phonenumbers.PhoneNumberDeleteResponse;

PhoneNumberDeleteResponse phoneNumber = client.phoneNumbers().delete("1293384261075731499");
```

## 更改电话号码的捆绑状态（将其添加到捆绑包中或从捆绑包中移除）

`PATCH /phone_numbers/{id}/actions/bundle_status_change` — 必需参数：`bundle_id`

```java
import com.telnyx.sdk.models.phonenumbers.actions.ActionChangeBundleStatusParams;
import com.telnyx.sdk.models.phonenumbers.actions.ActionChangeBundleStatusResponse;

ActionChangeBundleStatusParams params = ActionChangeBundleStatusParams.builder()
    .id("1293384261075731499")
    .bundleId("5194d8fc-87e6-4188-baa9-1c434bbe861b")
    .build();
ActionChangeBundleStatusResponse response = client.phoneNumbers().actions().changeBundleStatus(params);
```

## 为电话号码启用紧急呼叫功能

`POST /phone_numbers/{id}/actions/enable_emergency` — 必需参数：`emergency_enabled`, `emergency_address_id`

```java
import com.telnyx.sdk.models.phonenumbers.actions.ActionEnableEmergencyParams;
import com.telnyx.sdk.models.phonenumbers.actions.ActionEnableEmergencyResponse;

ActionEnableEmergencyParams params = ActionEnableEmergencyParams.builder()
    .id("1293384261075731499")
    .emergencyAddressId("53829456729313")
    .emergencyEnabled(true)
    .build();
ActionEnableEmergencyResponse response = client.phoneNumbers().actions().enableEmergency(params);
```

## 获取带有语音设置的电话号码信息

`GET /phone_numbers/{id}/voice`

```java
import com.telnyx.sdk.models.phonenumbers.voice.VoiceRetrieveParams;
import com.telnyx.sdk.models.phonenumbers.voice.VoiceRetrieveResponse;

VoiceRetrieveResponse voice = client.phoneNumbers().voice().retrieve("1293384261075731499");
```

## 更新电话号码的语音设置

`PATCH /phone_numbers/{id}/voice`

```java
import com.telnyx.sdk.models.phonenumbers.voice.UpdateVoiceSettings;
import com.telnyx.sdk.models.phonenumbers.voice.VoiceUpdateParams;
import com.telnyx.sdk.models.phonenumbers.voice.VoiceUpdateResponse;

VoiceUpdateParams params = VoiceUpdateParams.builder()
    .id("1293384261075731499")
    .updateVoiceSettings(UpdateVoiceSettings.builder().build())
    .build();
VoiceUpdateResponse voice = client.phoneNumbers().voice().update(params);
```

## 验证电话号码的所有权

验证提供的电话号码的所有权，并返回号码与其 ID 的映射关系，以及未在账户中找到的号码列表。

`POST /phone_numbers/actions/verify_ownership` — 必需参数：`phone_numbers`

```java
import com.telnyx.sdk.models.phonenumbers.actions.ActionVerifyOwnershipParams;
import com.telnyx.sdk.models.phonenumbers.actions.ActionVerifyOwnershipResponse;

ActionVerifyOwnershipParams params = ActionVerifyOwnershipParams.builder()
    .addPhoneNumber("+15551234567")
    .build();
ActionVerifyOwnershipResponse response = client.phoneNumbers().actions().verifyOwnership(params);
```

## 列出 CSV 下载内容

`GET /phone_numbers/csv_downloads`

```java
import com.telnyx.sdk.models.phonenumbers.csvdownloads.CsvDownloadListPage;
import com.telnyx.sdk.models.phonenumbers.csvdownloads.CsvDownloadListParams;

CsvDownloadListPage page = client.phoneNumbers().csvDownloads().list();
```

## 创建 CSV 下载文件

`POST /phone_numbers/csv_downloads`

```java
import com.telnyx.sdk.models.phonenumbers.csvdownloads.CsvDownloadCreateParams;
import com.telnyx.sdk.models.phonenumbers.csvdownloads.CsvDownloadCreateResponse;

CsvDownloadCreateResponse csvDownload = client.phoneNumbers().csvDownloads().create();
```

## 获取 CSV 下载文件

`GET /phone_numbers/csv_downloads/{id}`

```java
import com.telnyx.sdk.models.phonenumbers.csvdownloads.CsvDownloadRetrieveParams;
import com.telnyx.sdk.models.phonenumbers.csvdownloads.CsvDownloadRetrieveResponse;

CsvDownloadRetrieveResponse csvDownload = client.phoneNumbers().csvDownloads().retrieve("id");
```

## 列出电话号码任务

`GET /phone_numbers/jobs`

```java
import com.telnyx.sdk.models.phonenumbers.jobs.JobListPage;
import com.telnyx.sdk.models.phonenumbers.jobs.JobListParams;

JobListPage page = client.phoneNumbers().jobs().list();
```

## 获取电话号码任务信息

`GET /phone_numbers/jobs/{id}`

```java
import com.telnyx.sdk.models.phonenumbers.jobs.JobRetrieveParams;
import com.telnyx.sdk.models.phonenumbers.jobs.JobRetrieveResponse;

JobRetrieveResponse job = client.phoneNumbers().jobs().retrieve("id");
```

## 删除一批号码

创建一个新的后台任务，以删除一批号码。

`POST /phone_numbers/jobs/delete_phone_numbers` — 必需参数：`phone_numbers`

```java
import com.telnyx.sdk.models.phonenumbers.jobs.JobDeleteBatchParams;
import com.telnyx.sdk.models.phonenumbers.jobs.JobDeleteBatchResponse;
import java.util.List;

JobDeleteBatchParams params = JobDeleteBatchParams.builder()
    .phoneNumbers(List.of(
      "+19705555098",
      "+19715555098",
      "32873127836"
    ))
    .build();
JobDeleteBatchResponse response = client.phoneNumbers().jobs().deleteBatch(params);
```

## 更新一批号码的紧急呼叫设置

创建一个新的后台任务，以更新一批号码的紧急呼叫设置。

`POST /phone_numbers/jobs/update_emergency_settings` — 必需参数：`emergency_enabled`, `phone_numbers`

```java
import com.telnyx.sdk.models.phonenumbers.jobs.JobUpdateEmergencySettingsBatchParams;
import com.telnyx.sdk.models.phonenumbers.jobs.JobUpdateEmergencySettingsBatchResponse;
import java.util.List;

JobUpdateEmergencySettingsBatchParams params = JobUpdateEmergencySettingsBatchParams.builder()
    .emergencyEnabled(true)
    .phoneNumbers(List.of(
      "+19705555098",
      "+19715555098",
      "32873127836"
    ))
    .build();
JobUpdateEmergencySettingsBatchResponse response = client.phoneNumbers().jobs().updateEmergencySettingsBatch(params);
```

## 更新一批号码的信息

创建一个新的后台任务，以更新一批号码的信息。

`POST /phone_numbers/jobs/update_phone_numbers` — 必需参数：`phone_numbers`

```java
import com.telnyx.sdk.models.phonenumbers.jobs.JobUpdateBatchParams;
import com.telnyx.sdk.models.phonenumbers.jobs.JobUpdateBatchResponse;

JobUpdateBatchParams params = JobUpdateBatchParams.builder()
    .addPhoneNumber("1583466971586889004")
    .addPhoneNumber("+13127367254")
    .build();
JobUpdateBatchResponse response = client.phoneNumbers().jobs().updateBatch(params);
```

## 获取一批电话号码的监管要求信息

`GET /phone_numbers/regulatory_requirements`

```java
import com.telnyx.sdk.models.phonenumbersregulatoryrequirements.PhoneNumbersRegulatoryRequirementRetrieveParams;
import com.telnyx.sdk.models.phonenumbersregulatoryrequirements.PhoneNumbersRegulatoryRequirementRetrieveResponse;

PhoneNumbersRegulatoryRequirementRetrieveResponse phoneNumbersRegulatoryRequirement = client.phoneNumbersRegulatoryRequirements().retrieve();
```

## 简化版电话号码列表

列出电话号码，此端点的性能更高，且具有更低的请求速率限制。

`GET /phone_numbers/slim`

```java
import com.telnyx.sdk.models.phonenumbers.PhoneNumberSlimListPage;
import com.telnyx.sdk.models.phonenumbers.PhoneNumberSlimListParams;

PhoneNumberSlimListPage page = client.phoneNumbers().slimList();
```

## 列出带有语音设置的电话号码

`GET /phone_numbers/voice`

```java
import com.telnyx.sdk.models.phonenumbers.voice.VoiceListPage;
import com.telnyx.sdk.models.phonenumbers.voice.VoiceListParams;

VoiceListPage page = client.phoneNumbers().voice().list();
```

## 列出手机号码

`GET /v2/mobile_phone_numbers`

```java
import com.telnyx.sdk.models.mobilephonenumbers.MobilePhoneNumberListPage;
import com.telnyx.sdk.models.mobilephonenumbers.MobilePhoneNumberListParams;

MobilePhoneNumberListPage page = client.mobilePhoneNumbers().list();
```

## 获取手机号码信息

`GET /v2/mobile_phone_numbers/{id}`

```java
import com.telnyx.sdk.models.mobilephonenumbers.MobilePhoneNumberRetrieveParams;
import com.telnyx.sdk.models.mobilephonenumbers.MobilePhoneNumberRetrieveResponse;

MobilePhoneNumberRetrieveResponse mobilePhoneNumber = client.mobilePhoneNumbers().retrieve("id");
```

## 更新手机号码信息

`PATCH /v2/mobile_phone_numbers/{id}`

```java
import com.telnyx.sdk.models.mobilephonenumbers.MobilePhoneNumberUpdateParams;
import com.telnyx.sdk.models.mobilephonenumbers.MobilePhoneNumberUpdateResponse;

MobilePhoneNumberUpdateResponse mobilePhoneNumber = client.mobilePhoneNumbers().update("id");
```