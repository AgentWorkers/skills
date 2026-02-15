---
name: telnyx-porting-out-java
description: >-
  Manage port-out requests when numbers are being ported away from Telnyx. List,
  view, and update port-out status. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: porting-out
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Porting Out - Java

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

## 列出 portout 请求

根据过滤器返回 portout 请求

`GET /portouts`

```java
import com.telnyx.sdk.models.portouts.PortoutListPage;
import com.telnyx.sdk.models.portouts.PortoutListParams;

PortoutListPage page = client.portouts().list();
```

## 获取 portout 请求

根据提供的 ID 返回 portout 请求

`GET /portouts/{id}`

```java
import com.telnyx.sdk.models.portouts.PortoutRetrieveParams;
import com.telnyx.sdk.models.portouts.PortoutRetrieveResponse;

PortoutRetrieveResponse portout = client.portouts().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 查看 portout 请求的评论

返回 portout 请求的评论列表

`GET /portouts/{id}/comments`

```java
import com.telnyx.sdk.models.portouts.comments.CommentListParams;
import com.telnyx.sdk.models.portouts.comments.CommentListResponse;

CommentListResponse comments = client.portouts().comments().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 为 portout 请求创建评论

为 portout 请求创建评论

`POST /portouts/{id}/comments`

```java
import com.telnyx.sdk.models.portouts.comments.CommentCreateParams;
import com.telnyx.sdk.models.portouts.comments.CommentCreateResponse;

CommentCreateResponse comment = client.portouts().comments().create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 查看 portout 请求的相关支持文档

查看 portout 请求的所有支持文档

`GET /portouts/{id}/supporting_documents`

```java
import com.telnyx.sdk.models.portouts.supportingdocuments.SupportingDocumentListParams;
import com.telnyx.sdk.models.portouts.supportingdocuments.SupportingDocumentListResponse;

SupportingDocumentListResponse supportingDocuments = client.portouts().supportingDocuments().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 为 portout 请求创建支持文档列表

创建 portout 请求的支持文档列表

`POST /portouts/{id}/supporting_documents`

```java
import com.telnyx.sdk.models.portouts.supportingdocuments.SupportingDocumentCreateParams;
import com.telnyx.sdk.models.portouts.supportingdocuments.SupportingDocumentCreateResponse;

SupportingDocumentCreateResponse supportingDocument = client.portouts().supportingDocuments().create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 更新状态

授权或拒绝 portout 请求

`PATCH /portouts/{id}/{status}` — 必需参数：`reason`

```java
import com.telnyx.sdk.models.portouts.PortoutUpdateStatusParams;
import com.telnyx.sdk.models.portouts.PortoutUpdateStatusResponse;

PortoutUpdateStatusParams params = PortoutUpdateStatusParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .status(PortoutUpdateStatusParams.Status.AUTHORIZED)
    .reason("I do not recognize this transaction")
    .build();
PortoutUpdateStatusResponse response = client.portouts().updateStatus(params);
```

## 列出所有 port-out 事件

返回所有 port-out 事件的列表

`GET /portouts/events`

```java
import com.telnyx.sdk.models.portouts.events.EventListPage;
import com.telnyx.sdk.models.portouts.events.EventListParams;

EventListPage page = client.portouts().events().list();
```

## 查看特定的 port-out 事件

查看特定的 port-out 事件

`GET /portouts/events/{id}`

```java
import com.telnyx.sdk.models.portouts.events.EventRetrieveParams;
import com.telnyx.sdk.models.portouts.events.EventRetrieveResponse;

EventRetrieveResponse event = client.portouts().events().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 重新发布 port-out 事件

重新发布特定的 port-out 事件

`POST /portouts/events/{id}/republish`

```java
import com.telnyx.sdk.models.portouts.events.EventRepublishParams;

client.portouts().events().republish("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出特定 port-out 的拒绝代码

根据给定的 port-out ID，列出适用于该 port-out 的拒绝代码

`GET /portouts/rejections/{portout_id}`

```java
import com.telnyx.sdk.models.portouts.PortoutListRejectionCodesParams;
import com.telnyx.sdk.models.portouts.PortoutListRejectionCodesResponse;

PortoutListRejectionCodesResponse response = client.portouts().listRejectionCodes("329d6658-8f93-405d-862f-648776e8afd7");
```

## 查看 port-out 相关的报告

列出关于 port-out 操作生成的报告

`GET /portouts/reports`

```java
import com.telnyx.sdk.models.portouts.reports.ReportListPage;
import com.telnyx.sdk.models.portouts.reports.ReportListParams;

ReportListPage page = client.portouts().reports().list();
```

## 创建 port-out 相关的报告

生成关于 port-out 操作的报告

`POST /portouts/reports`

```java
import com.telnyx.sdk.models.portouts.reports.ExportPortoutsCsvReport;
import com.telnyx.sdk.models.portouts.reports.ReportCreateParams;
import com.telnyx.sdk.models.portouts.reports.ReportCreateResponse;

ReportCreateParams params = ReportCreateParams.builder()
    .params(ExportPortoutsCsvReport.builder()
        .filters(ExportPortoutsCsvReport.Filters.builder().build())
        .build())
    .reportType(ReportCreateParams.ReportType.EXPORT_PORTOUTS_CSV)
    .build();
ReportCreateResponse report = client.portouts().reports().create(params);
```

## 获取报告

检索特定生成的报告

`GET /portouts/reports/{id}`

```java
import com.telnyx.sdk.models.portouts.reports.ReportRetrieveParams;
import com.telnyx.sdk.models.portouts.reports.ReportRetrieveResponse;

ReportRetrieveResponse report = client.portouts().reports().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```