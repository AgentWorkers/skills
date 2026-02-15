---
name: telnyx-account-reports-java
description: >-
  Generate and retrieve usage reports for billing, analytics, and
  reconciliation. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: account-reports
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户报告 - Java

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

## 获取所有 MDR 详细报告请求

检索已认证用户的所有 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingListParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingListResponse;

MessagingListResponse messagings = client.legacy().reporting().batchDetailRecords().messaging().list();
```

## 创建新的 MDR 详细报告请求

使用指定的筛选条件创建新的 MDR 详细报告请求

`POST /legacy_reporting/batch_detail_records/messaging` — 必需参数：`start_time`、`end_time`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingCreateParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingCreateResponse;
import java.time.OffsetDateTime;

MessagingCreateParams params = MessagingCreateParams.builder()
    .endTime(OffsetDateTime.parse("2024-02-12T23:59:59Z"))
    .startTime(OffsetDateTime.parse("2024-02-01T00:00:00Z"))
    .build();
MessagingCreateResponse messaging = client.legacy().reporting().batchDetailRecords().messaging().create(params);
```

## 获取特定的 MDR 详细报告请求

通过 ID 获取特定的 MDR 详细报告请求

`GET /legacy_reporting/batch_detail_records/messaging/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingRetrieveParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingRetrieveResponse;

MessagingRetrieveResponse messaging = client.legacy().reporting().batchDetailRecords().messaging().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除 MDR 详细报告请求

通过 ID 删除特定的 MDR 详细报告请求

`DELETE /legacy_reporting/batch_detail_records/messaging/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingDeleteParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.messaging.MessagingDeleteResponse;

MessagingDeleteResponse messaging = client.legacy().reporting().batchDetailRecords().messaging().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取所有 CDR 报告请求

检索已认证用户的所有 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceListParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceListResponse;

VoiceListResponse voices = client.legacy().reporting().batchDetailRecords().voice().list();
```

## 创建新的 CDR 报告请求

使用指定的筛选条件创建新的 CDR 报告请求

`POST /legacy_reporting/batch_detail_records/voice` — 必需参数：`start_time`、`end_time`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceCreateParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceCreateResponse;
import java.time.OffsetDateTime;

VoiceCreateParams params = VoiceCreateParams.builder()
    .endTime(OffsetDateTime.parse("2024-02-12T23:59:59Z"))
    .startTime(OffsetDateTime.parse("2024-02-01T00:00:00Z"))
    .build();
VoiceCreateResponse voice = client.legacy().reporting().batchDetailRecords().voice().create(params);
```

## 获取特定的 CDR 报告请求

通过 ID 获取特定的 CDR 报告请求

`GET /legacy_reporting/batch_detail_records/voice/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceRetrieveParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceRetrieveResponse;

VoiceRetrieveResponse voice = client.legacy().reporting().batchDetailRecords().voice().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除 CDR 报告请求

通过 ID 删除特定的 CDR 报告请求

`DELETE /legacy_reporting/batch_detail_records/voice/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceDeleteParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceDeleteResponse;

VoiceDeleteResponse voice = client.legacy().reporting().batchDetailRecords().voice().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取可用的 CDR 报告字段

检索所有可用于 CDR 报告的字段

`GET /legacy_reporting/batch_detail_records/voice/fields`

```java
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceRetrieveFieldsParams;
import com.telnyx.sdk.models.legacy.reporting.batchdetailrecords.voice.VoiceRetrieveFieldsResponse;

VoiceRetrieveFieldsResponse response = client.legacy().reporting().batchDetailRecords().voice().retrieveFields();
```

## 列出 MDR 使用报告

获取所有之前的 MDR 使用报告请求

`GET /legacy_reporting/usage_reports/messaging`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingListPage;
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingListParams;

MessagingListPage page = client.legacy().reporting().usageReports().messaging().list();
```

## 创建新的传统使用 V2 MDR 报告请求

使用指定的筛选条件创建新的传统使用 V2 MDR 报告请求

`POST /legacy_reporting/usage_reports/messaging`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingCreateParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingCreateResponse;

MessagingCreateParams params = MessagingCreateParams.builder()
    .aggregationType(0)
    .build();
MessagingCreateResponse messaging = client.legacy().reporting().usageReports().messaging().create(params);
```

## 获取 MDR 使用报告

通过 ID 获取单个 MDR 使用报告

`GET /legacy_reporting/usage_reports/messaging/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingRetrieveParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingRetrieveResponse;

MessagingRetrieveResponse messaging = client.legacy().reporting().usageReports().messaging().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除 V2 传统使用 MDR 报告请求

通过 ID 删除特定的 V2 传统使用 MDR 报告请求

`DELETE /legacy_reporting/usage_reports/messaging/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingDeleteParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.messaging.MessagingDeleteResponse;

MessagingDeleteResponse messaging = client.legacy().reporting().usageReports().messaging().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出电信数据使用报告

获取分页的电信数据使用报告列表

`GET /legacy_reporting/usage_reports/number_lookup`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.numberlookup.NumberLookupListParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.numberlookup.NumberLookupListResponse;

NumberLookupListResponse numberLookups = client.legacy().reporting().usageReports().numberLookup().list();
```

## 提交电信数据使用报告

提交新的电信数据使用报告

`POST /legacy_reporting/usage_reports/number_lookup`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.numberlookup.NumberLookupCreateParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.numberlookup.NumberLookupCreateResponse;

NumberLookupCreateResponse numberLookup = client.legacy().reporting().usageReports().numberLookup().create();
```

## 通过 ID 获取电信数据使用报告

通过 ID 获取特定的电信数据使用报告

`GET /legacy_reporting/usage_reports/number_lookup/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.numberlookup.NumberLookupRetrieveParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.numberlookup.NumberLookupRetrieveResponse;

NumberLookupRetrieveResponse numberLookup = client.legacy().reporting().usageReports().numberLookup().retrieve("id");
```

## 删除电信数据使用报告

通过 ID 删除特定的电信数据使用报告

`DELETE /legacy_reporting/usage_reports/number_lookup/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.numberlookup.NumberLookupDeleteParams;

client.legacy().reporting().usageReports().numberLookup().delete("id");
```

## 获取语音转文本使用报告

生成并同步获取语音转文本使用报告

`GET /legacy_reporting/usage_reports/speech_to_text`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.UsageReportRetrieveSpeechToTextParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.UsageReportRetrieveSpeechToTextResponse;

UsageReportRetrieveSpeechToTextResponse response = client.legacy().reporting().usageReports().retrieveSpeechToText();
```

## 列出 CDR 使用报告

获取所有之前的 CDR 使用报告请求

`GET /legacy_reporting/usage_reports/voice`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceListPage;
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceListParams;

VoiceListPage page = client.legacy().reporting().usageReports().voice().list();
```

## 创建新的传统使用 V2 CDR 报告请求

使用指定的筛选条件创建新的传统使用 V2 CDR 报告请求

`POST /legacy_reporting/usage_reports/voice`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceCreateParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceCreateResponse;
import java.time.OffsetDateTime;

VoiceCreateParams params = VoiceCreateParams.builder()
    .endTime(OffsetDateTime.parse("2024-02-01T00:00:00Z"))
    .startTime(OffsetDateTime.parse("2024-02-01T00:00:00Z"))
    .build();
VoiceCreateResponse voice = client.legacy().reporting().usageReports().voice().create(params);
```

## 获取 CDR 使用报告

通过 ID 获取单个 CDR 使用报告

`GET /legacy_reporting/usage_reports/voice/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceRetrieveParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceRetrieveResponse;

VoiceRetrieveResponse voice = client.legacy().reporting().usageReports().voice().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除 V2 传统使用 CDR 报告请求

通过 ID 删除特定的 V2 传统使用 CDR 报告请求

`DELETE /legacy_reporting/usage_reports/voice/{id}`

```java
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceDeleteParams;
import com.telnyx.sdk.models.legacy.reporting.usagereports.voice.VoiceDeleteResponse;

VoiceDeleteResponse voice = client.legacy().reporting().usageReports().voice().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取所有消息使用报告

获取所有消息使用报告

`GET /reports/mdr_usage_reports`

```java
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportListPage;
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportListParams;

MdrUsageReportListPage page = client.reports().mdrUsageReports().list();
```

## 创建 MDR 使用报告

提交新的消息使用报告请求

`POST /reports/mdr_usage_reports`

```java
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportCreateParams;
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportCreateResponse;
import java.time.OffsetDateTime;

MdrUsageReportCreateParams params = MdrUsageReportCreateParams.builder()
    .aggregationType(MdrUsageReportCreateParams.AggregationType.NO_AGGREGATION)
    .endDate(OffsetDateTime.parse("2020-07-01T00:00:00-06:00"))
    .startDate(OffsetDateTime.parse("2020-07-01T00:00:00-06:00"))
    .build();
MdrUsageReportCreateResponse mdrUsageReport = client.reports().mdrUsageReports().create(params);
```

## 获取消息使用报告

通过 ID 获取单个消息使用报告

`GET /reports/mdr_usage_reports/{id}`

```java
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportRetrieveParams;
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportRetrieveResponse;

MdrUsageReportRetrieveResponse mdrUsageReport = client.reports().mdrUsageReports().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除 MDR 使用报告

通过 ID 删除消息使用报告

`DELETE /reports/mdr_usage_reports/{id}`

```java
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportDeleteParams;
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportDeleteResponse;

MdrUsageReportDeleteResponse mdrUsageReport = client.reports().mdrUsageReports().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 生成并获取 MDR 使用报告

同步生成并获取消息使用报告

`GET /reports/mdr_usage_reports/sync`

```java
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportFetchSyncParams;
import com.telnyx.sdk.models.reports.mdrusagereports.MdrUsageReportFetchSyncResponse;

MdrUsageReportFetchSyncParams params = MdrUsageReportFetchSyncParams.builder()
    .aggregationType(MdrUsageReportFetchSyncParams.AggregationType.PROFILE)
    .build();
MdrUsageReportFetchSyncResponse response = client.reports().mdrUsageReports().fetchSync(params);
```

## 生成并获取 CDR 使用报告

同步生成并获取语音使用报告

`GET /reports/cdr_usage_reports/sync`

```java
import com.telnyx.sdk.models.reports.cdrusagereports.CdrUsageReportFetchSyncParams;
import com.telnyx.sdk.models.reports.cdrusagereports.CdrUsageReportFetchSyncResponse;

CdrUsageReportFetchSyncParams params = CdrUsageReportFetchSyncParams.builder()
    .aggregationType(CdrUsageReportFetchSyncParams.AggregationType.NO_AGGREGATION)
    .productBreakdown(CdrUsageReportFetchSyncParams.ProductBreakdown.NO_BREAKDOWN)
    .build();
CdrUsageReportFetchSyncResponse response = client.reports().cdrUsageReports().fetchSync(params);
```

## 获取 Telnyx 产品使用数据（测试版）

按指定的维度获取 Telnyx 产品使用数据

`GET /usage_reports`

```java
import com.telnyx.sdk.models.usagereports.UsageReportListPage;
import com.telnyx.sdk.models.usagereports.UsageReportListParams;

UsageReportListParams params = UsageReportListParams.builder()
    .addDimension("string")
    .addMetric("string")
    .product("product")
    .build();
UsageReportListPage page = client.usageReports().list(params);
```

## 获取使用报告查询选项（测试版）

获取用于查询使用情况的报告选项，包括可用的产品及其相应的指标和维度

`GET /usage_reports/options`

```java
import com.telnyx.sdk.models.usagereports.UsageReportGetOptionsParams;
import com.telnyx.sdk.models.usagereports.UsageReportGetOptionsResponse;

UsageReportGetOptionsResponse response = client.usageReports().getOptions();
```