---
name: telnyx-fax-java
description: >-
  Send and receive faxes programmatically. Manage fax applications and media.
  This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: fax
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 传真 - Java

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

以下所有示例均假设 `client` 已经按照上述方式初始化完成。

## 列出所有传真应用

此端点会在响应的 `data` 属性中返回您的所有传真应用列表。

`GET /fax_applications`

```java
import com.telnyx.sdk.models.faxapplications.FaxApplicationListPage;
import com.telnyx.sdk.models.faxapplications.FaxApplicationListParams;

FaxApplicationListPage page = client.faxApplications().list();
```

## 创建传真应用

根据请求中发送的参数创建一个新的传真应用。

`POST /fax_applications` — 必需参数：`application_name`、`webhook_event_url`

```java
import com.telnyx.sdk.models.faxapplications.FaxApplicationCreateParams;
import com.telnyx.sdk.models.faxapplications.FaxApplicationCreateResponse;

FaxApplicationCreateParams params = FaxApplicationCreateParams.builder()
    .applicationName("fax-router")
    .webhookEventUrl("https://example.com")
    .build();
FaxApplicationCreateResponse faxApplication = client.faxApplications().create(params);
```

## 查询传真应用信息

在响应的 `data` 属性中返回现有传真应用的详细信息。

`GET /fax_applications/{id}`

```java
import com.telnyx.sdk.models.faxapplications.FaxApplicationRetrieveParams;
import com.telnyx.sdk.models.faxapplications.FaxApplicationRetrieveResponse;

FaxApplicationRetrieveResponse faxApplication = client.faxApplications().retrieve("1293384261075731499");
```

## 更新传真应用

根据请求中的参数更新现有传真应用的设置。

`PATCH /fax_applications/{id}` — 必需参数：`application_name`、`webhook_event_url`

```java
import com.telnyx.sdk.models.faxapplications.FaxApplicationUpdateParams;
import com.telnyx.sdk.models.faxapplications.FaxApplicationUpdateResponse;

FaxApplicationUpdateParams params = FaxApplicationUpdateParams.builder()
    .id("1293384261075731499")
    .applicationName("fax-router")
    .webhookEventUrl("https://example.com")
    .build();
FaxApplicationUpdateResponse faxApplication = client.faxApplications().update(params);
```

## 删除传真应用

永久删除一个传真应用。

`DELETE /fax_applications/{id}`

```java
import com.telnyx.sdk.models.faxapplications.FaxApplicationDeleteParams;
import com.telnyx.sdk.models.faxapplications.FaxApplicationDeleteResponse;

FaxApplicationDeleteResponse faxApplication = client.faxApplications().delete("1293384261075731499");
```

## 查看传真列表

`GET /faxes`

```java
import com.telnyx.sdk.models.faxes.FaxListPage;
import com.telnyx.sdk.models.faxes.FaxListParams;

FaxListPage page = client.faxes().list();
```

## 发送传真

发送传真。

`POST /faxes` — 必需参数：`connection_id`、`from`、`to`

```java
import com.telnyx.sdk.models.faxes.FaxCreateParams;
import com.telnyx.sdk.models.faxes.FaxCreateResponse;

FaxCreateParams params = FaxCreateParams.builder()
    .connectionId("234423")
    .from("+13125790015")
    .to("+13127367276")
    .build();
FaxCreateResponse fax = client.faxes().create(params);
```

## 查看传真详情

`GET /faxes/{id}`

```java
import com.telnyx.sdk.models.faxes.FaxRetrieveParams;
import com.telnyx.sdk.models.faxes.FaxRetrieveResponse;

FaxRetrieveResponse fax = client.faxes().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除传真

`DELETE /faxes/{id}`

```java
import com.telnyx.sdk.models.faxes.FaxDeleteParams;

client.faxes().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 取消传真

取消处于以下状态之一的传出传真：`queued`、`media.processed`、`originated` 或 `sending`

`POST /faxes/{id}/actions/cancel`

```java
import com.telnyx.sdk.models.faxes.actions.ActionCancelParams;
import com.telnyx.sdk.models.faxes.actions.ActionCancelResponse;

ActionCancelResponse response = client.faxes().actions().cancel("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 刷新传真信息

当传入的传真信息过期时，刷新其媒体链接。

`POST /faxes/{id}/actions/refresh`

```java
import com.telnyx.sdk.models.faxes.actions.ActionRefreshParams;
import com.telnyx.sdk.models.faxes.actions.ActionRefreshResponse;

ActionRefreshResponse response = client.faxes().actions().refresh("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL：
所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `fax.delivered` | 传真已送达 |
| `fax.failed` | 传真发送失败 |
| `fax.media.processed` | 传真媒体文件已处理 |
| `fax.queued` | 传真已排队 |
| `fax.sendingstarted` | 传真发送开始 |