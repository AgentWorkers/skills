---
name: telnyx-account-java
description: >-
  Manage account balance, payments, invoices, webhooks, and view audit logs and
  detail records. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: account
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户 - Java

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

## 列出审计日志

检索审计日志条目列表。

`GET /audit_events`

```java
import com.telnyx.sdk.models.auditevents.AuditEventListPage;
import com.telnyx.sdk.models.auditevents.AuditEventListParams;

AuditEventListPage page = client.auditEvents().list();
```

## 获取用户余额详情

`GET /balance`

```java
import com.telnyx.sdk.models.balance.BalanceRetrieveParams;
import com.telnyx.sdk.models.balance.BalanceRetrieveResponse;

BalanceRetrieveResponse balance = client.balance().retrieve();
```

## 搜索详细记录

在 Telnyx 平台上搜索任何详细记录。

`GET /detail_records`

```java
import com.telnyx.sdk.models.detailrecords.DetailRecordListPage;
import com.telnyx.sdk.models.detailrecords.DetailRecordListParams;

DetailRecordListPage page = client.detailRecords().list();
```

## 列出发票

检索分页显示的发票列表。

`GET /invoices`

```java
import com.telnyx.sdk.models.invoices.InvoiceListPage;
import com.telnyx.sdk.models.invoices.InvoiceListParams;

InvoiceListPage page = client.invoices().list();
```

## 根据 ID 获取发票

根据唯一标识符检索单张发票。

`GET /invoices/{id}`

```java
import com.telnyx.sdk.models.invoices.InvoiceRetrieveParams;
import com.telnyx.sdk.models.invoices.InvoiceRetrieveResponse;

InvoiceRetrieveResponse invoice = client.invoices().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出自动充值偏好设置

返回支付自动充值偏好设置。

`GET /payments/auto_recharge_prefs`

```java
import com.telnyx.sdk.models.payment.autorechargeprefs.AutoRechargePrefListParams;
import com.telnyx.sdk.models.payment.autorechargeprefs.AutoRechargePrefListResponse;

AutoRechargePrefListResponse autoRechargePrefs = client.payment().autoRechargePrefs().list();
```

## 更新自动充值偏好设置

更新支付自动充值偏好设置。

`PATCH /payments/auto_recharge_prefs`

```java
import com.telnyx.sdk.models.payment.autorechargeprefs.AutoRechargePrefUpdateParams;
import com.telnyx.sdk.models.payment.autorechargeprefs.AutoRechargePrefUpdateResponse;

AutoRechargePrefUpdateResponse autoRechargePref = client.payment().autoRechargePrefs().update();
```

## 列出用户标签

列出所有用户标签。

`GET /user_tags`

```java
import com.telnyx.sdk.models.usertags.UserTagListParams;
import com.telnyx.sdk.models.usertags.UserTagListResponse;

UserTagListResponse userTags = client.userTags().list();
```

## 列出 Webhook 交付记录

列出已认证用户的 Webhook 交付记录。

`GET /webhook_deliveries`

```java
import com.telnyx.sdk.models.webhookdeliveries.WebhookDeliveryListPage;
import com.telnyx.sdk.models.webhookdeliveries.WebhookDeliveryListParams;

WebhookDeliveryListPage page = client.webhookDeliveries().list();
```

## 根据 ID 查找 Webhook 交付详情

提供 Webhook 交付的调试数据，如时间戳、交付状态和尝试次数。

`GET /webhook_deliveries/{id}`

```java
import com.telnyx.sdk.models.webhookdeliveries.WebhookDeliveryRetrieveParams;
import com.telnyx.sdk.models.webhookdeliveries.WebhookDeliveryRetrieveResponse;

WebhookDeliveryRetrieveResponse webhookDelivery = client.webhookDeliveries().retrieve("C9C0797E-901D-4349-A33C-C2C8F31A92C2");
```