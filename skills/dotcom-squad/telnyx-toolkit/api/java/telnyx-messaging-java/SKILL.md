---
name: telnyx-messaging-java
description: >-
  Send and receive SMS/MMS messages, manage messaging-enabled phone numbers, and
  handle opt-outs. Use when building messaging applications, implementing 2FA,
  or sending notifications. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: messaging
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息服务 - Java

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

## 发送消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来发送消息。

`POST /messages` — 必需参数：`to`

```java
import com.telnyx.sdk.models.messages.MessageSendParams;
import com.telnyx.sdk.models.messages.MessageSendResponse;

MessageSendParams params = MessageSendParams.builder()
    .to("+18445550001")
    .build();
MessageSendResponse response = client.messages().send(params);
```

## 获取消息

注意：此 API 端点仅能获取创建时间不超过 10 天的消息。

`GET /messages/{id}`

```java
import com.telnyx.sdk.models.messages.MessageRetrieveParams;
import com.telnyx.sdk.models.messages.MessageRetrieveResponse;

MessageRetrieveResponse message = client.messages().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 取消已安排的消息

取消尚未发送的已安排消息。

`DELETE /messages/{id}`

```java
import com.telnyx.sdk.models.messages.MessageCancelScheduledParams;
import com.telnyx.sdk.models.messages.MessageCancelScheduledResponse;

MessageCancelScheduledResponse response = client.messages().cancelScheduled("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 发送 Whatsapp 消息

`POST /messages/whatsapp` — 必需参数：`from`, `to`, `whatsapp_message`

```java
import com.telnyx.sdk.models.messages.MessageSendWhatsappParams;
import com.telnyx.sdk.models.messages.MessageSendWhatsappResponse;

MessageSendWhatsappParams params = MessageSendWhatsappParams.builder()
    .from("+13125551234")
    .to("+13125551234")
    .whatsappMessage(MessageSendWhatsappParams.WhatsappMessage.builder().build())
    .build();
MessageSendWhatsappResponse response = client.messages().sendWhatsapp(params);
```

## 发送群组 MMS 消息

`POST /messages/group_mms` — 必需参数：`from`, `to`

```java
import com.telnyx.sdk.models.messages.MessageSendGroupMmsParams;
import com.telnyx.sdk.models.messages.MessageSendGroupMmsResponse;

MessageSendGroupMmsParams params = MessageSendGroupMmsParams.builder()
    .from("+13125551234")
    .addTo("+18655551234")
    .addTo("+14155551234")
    .build();
MessageSendGroupMmsResponse response = client.messages().sendGroupMms(params);
```

## 发送长码消息

`POST /messages/long_code` — 必需参数：`from`, `to`

```java
import com.telnyx.sdk.models.messages.MessageSendLongCodeParams;
import com.telnyx.sdk.models.messages.MessageSendLongCodeResponse;

MessageSendLongCodeParams params = MessageSendLongCodeParams.builder()
    .from("+18445550001")
    .to("+13125550002")
    .build();
MessageSendLongCodeResponse response = client.messages().sendLongCode(params);
```

## 使用号码池发送消息

`POST /messages/number_pool` — 必需参数：`to`, `messaging_profile_id`

```java
import com.telnyx.sdk.models.messages.MessageSendNumberPoolParams;
import com.telnyx.sdk.models.messages.MessageSendNumberPoolResponse;

MessageSendNumberPoolParams params = MessageSendNumberPoolParams.builder()
    .messagingProfileId("abc85f64-5717-4562-b3fc-2c9600000000")
    .to("+13125550002")
    .build();
MessageSendNumberPoolResponse response = client.messages().sendNumberPool(params);
```

## 安排消息

可以使用电话号码、字母数字发送者 ID、短代码或号码池来安排消息的发送。

`POST /messages/schedule` — 必需参数：`to`

```java
import com.telnyx.sdk.models.messages.MessageScheduleParams;
import com.telnyx.sdk.models.messages.MessageScheduleResponse;

MessageScheduleParams params = MessageScheduleParams.builder()
    .to("+18445550001")
    .build();
MessageScheduleResponse response = client.messages().schedule(params);
```

## 发送短代码消息

`POST /messages/short_code` — 必需参数：`from`, `to`

```java
import com.telnyx.sdk.models.messages.MessageSendShortCodeParams;
import com.telnyx.sdk.models.messages.MessageSendShortCodeResponse;

MessageSendShortCodeParams params = MessageSendShortCodeParams.builder()
    .from("+18445550001")
    .to("+18445550001")
    .build();
MessageSendShortCodeResponse response = client.messages().sendShortCode(params);
```

## 获取用户退订信息

获取用户的退订信息列表。

`GET /messaging_optouts`

```java
import com.telnyx.sdk.models.messagingoptouts.MessagingOptoutListPage;
import com.telnyx.sdk.models.messagingoptouts.MessagingOptoutListParams;

MessagingOptoutListPage page = client.messagingOptouts().list();
```

## 获取带有消息功能的电话号码信息

`GET /phone_numbers/{id}/messaging`

```java
import com.telnyx.sdk.models.phonenumbers.messaging.MessagingRetrieveParams;
import com.telnyx.sdk.models.phonenumbers.messaging.MessagingRetrieveResponse;

MessagingRetrieveResponse messaging = client.phoneNumbers().messaging().retrieve("id");
```

## 更新电话号码的消息功能配置

`PATCH /phone_numbers/{id}/messaging`

```java
import com.telnyx.sdk.models.phonenumbers.messaging.MessagingUpdateParams;
import com.telnyx.sdk.models.phonenumbers.messaging.MessagingUpdateResponse;

MessagingUpdateResponse messaging = client.phoneNumbers().messaging().update("id");
```

## 获取带有消息功能的电话号码列表

`GET /phone_numbers/messaging`

```java
import com.telnyx.sdk.models.phonenumbers.messaging.MessagingListPage;
import com.telnyx.sdk.models.phonenumbers.messaging.MessagingListParams;

MessagingListPage page = client.phoneNumbers().messaging().list();
```

## 获取带有消息功能的手机号码信息

`GET /mobile_phone_numbers/{id}/messaging`

```java
import com.telnyx.sdk.models.mobilephonenumbers.messaging.MessagingRetrieveParams;
import com.telnyx.sdk.models.mobilephonenumbers.messaging.MessagingRetrieveResponse;

MessagingRetrieveResponse messaging = client.mobilePhoneNumbers().messaging().retrieve("id");
```

## 获取带有消息功能的手机号码列表

`GET /mobile_phone_numbers/messaging`

```java
import com.telnyx.sdk.models.mobilephonenumbers.messaging.MessagingListPage;
import com.telnyx.sdk.models.mobilephonenumbers.messaging.MessagingListParams;

MessagingListPage page = client.mobilePhoneNumbers().messaging().list();
```

## 批量更新电话号码配置

`POST /messaging_numbers/bulk_updates` — 必需参数：`messaging_profile_id`, `numbers`

```java
import com.telnyx.sdk.models.messagingnumbersbulkupdates.MessagingNumbersBulkUpdateCreateParams;
import com.telnyx.sdk.models.messagingnumbersbulkupdates.MessagingNumbersBulkUpdateCreateResponse;
import java.util.List;

MessagingNumbersBulkUpdateCreateParams params = MessagingNumbersBulkUpdateCreateParams.builder()
    .messagingProfileId("00000000-0000-0000-0000-000000000000")
    .numbers(List.of(
      "+18880000000",
      "+18880000001",
      "+18880000002"
    ))
    .build();
MessagingNumbersBulkUpdateCreateResponse messagingNumbersBulkUpdate = client.messagingNumbersBulkUpdates().create(params);
```

## 获取批量更新状态

`GET /messaging_numbers/bulk_updates/{order_id}`

```java
import com.telnyx.sdk.models.messagingnumbersbulkupdates.MessagingNumbersBulkUpdateRetrieveParams;
import com.telnyx.sdk.models.messagingnumbersbulkupdates.MessagingNumbersBulkUpdateRetrieveResponse;

MessagingNumbersBulkUpdateRetrieveResponse messagingNumbersBulkUpdate = client.messagingNumbersBulkUpdates().retrieve("order_id");
```

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 标头以供验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `deliveryUpdate` | 消息投递更新 |
| `inboundMessage` | 收到的消息 |
| `replacedLinkClick` | 替换链接被点击 |
```
```