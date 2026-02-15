---
name: telnyx-voice-java
description: >-
  Make and receive calls, transfer, bridge, and manage call lifecycle with Call
  Control. Includes application management and call events. This skill provides
  Java SDK examples.
metadata:
  author: telnyx
  product: voice
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Voice - Java

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

## 接听来电

接听传入的电话。

`POST /calls/{call_control_id}/actions/answer`

```java
import com.telnyx.sdk.models.calls.actions.ActionAnswerParams;
import com.telnyx.sdk.models.calls.actions.ActionAnswerResponse;

ActionAnswerResponse response = client.calls().actions().answer("call_control_id");
```

## 桥接通话

将两个通话连接桥接起来。

`POST /calls/{call_control_id}/actions/bridge` — 必需参数：`call_control_id`

```java
import com.telnyx.sdk.models.calls.actions.ActionBridgeParams;
import com.telnyx.sdk.models.calls.actions.ActionBridgeResponse;

ActionBridgeParams params = ActionBridgeParams.builder()
    .callControlIdToBridge("call_control_id")
    .callControlId("v3:MdI91X4lWFEs7IgbBEOT9M4AigoY08M0WWZFISt1Yw2axZ_IiE4pqg")
    .build();
ActionBridgeResponse response = client.calls().actions().bridge(params);
```

## 拨打电话

从指定的连接拨打一个号码或 SIP URI。

`POST /calls` — 必需参数：`connection_id`, `to`, `from`

```java
import com.telnyx.sdk.models.calls.CallDialParams;
import com.telnyx.sdk.models.calls.CallDialResponse;

CallDialParams params = CallDialParams.builder()
    .connectionId("7267xxxxxxxxxxxxxx")
    .from("+18005550101")
    .to("+18005550100")
    .build();
CallDialResponse response = client.calls().dial(params);
```

## 结束通话

挂断通话。

`POST /calls/{call_control_id}/actions/hangup`

```java
import com.telnyx.sdk.models.calls.actions.ActionHangupParams;
import com.telnyx.sdk.models.calls.actions.ActionHangupResponse;

ActionHangupResponse response = client.calls().actions().hangup("call_control_id");
```

## 转接通话

将通话转接到新的目的地。

`POST /calls/{call_control_id}/actions/transfer` — 必需参数：`to`

```java
import com.telnyx.sdk.models.calls.actions.ActionTransferParams;
import com.telnyx.sdk.models.calls.actions.ActionTransferResponse;

ActionTransferParams params = ActionTransferParams.builder()
    .callControlId("call_control_id")
    .to("+18005550100")
    .build();
ActionTransferResponse response = client.calls().actions().transfer(params);
```

## 列出指定连接的所有活跃通话

列出指定连接的所有活跃通话。

`GET /connections/{connection_id}/active_calls`

```java
import com.telnyx.sdk.models.connections.ConnectionListActiveCallsPage;
import com.telnyx.sdk.models.connections.ConnectionListActiveCallsParams;

ConnectionListActiveCallsPage page = client.connections().listActiveCalls("1293384261075731461");
```

## 列出通话控制应用程序

返回通话控制应用程序的列表。

`GET /call_control_applications`

```java
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationListPage;
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationListParams;

CallControlApplicationListPage page = client.callControlApplications().list();
```

## 创建通话控制应用程序

创建一个新的通话控制应用程序。

`POST /call_control_applications` — 必需参数：`application_name`, `webhook_event_url`

```java
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationCreateParams;
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationCreateResponse;

CallControlApplicationCreateParams params = CallControlApplicationCreateParams.builder()
    .applicationName("call-router")
    .webhookEventUrl("https://example.com")
    .build();
CallControlApplicationCreateResponse callControlApplication = client.callControlApplications().create(params);
```

## 查询通话控制应用程序的详细信息

获取现有通话控制应用程序的详细信息。

`GET /call_control_applications/{id}`

```java
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationRetrieveParams;
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationRetrieveResponse;

CallControlApplicationRetrieveResponse callControlApplication = client.callControlApplications().retrieve("id");
```

## 更新通话控制应用程序

更新现有通话控制应用程序的设置。

`PATCH /call_control_applications/{id}` — 必需参数：`application_name`, `webhook_event_url`

```java
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationUpdateParams;
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationUpdateResponse;

CallControlApplicationUpdateParams params = CallControlApplicationUpdateParams.builder()
    .id("id")
    .applicationName("call-router")
    .webhookEventUrl("https://example.com")
    .build();
CallControlApplicationUpdateResponse callControlApplication = client.callControlApplications().update(params);
```

## 删除通话控制应用程序

删除通话控制应用程序。

`DELETE /call_control_applications/{id}`

```java
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationDeleteParams;
import com.telnyx.sdk.models.callcontrolapplications.CallControlApplicationDeleteResponse;

CallControlApplicationDeleteResponse callControlApplication = client.callControlApplications().delete("id");
```

## 列出通话事件

根据指定的过滤参数筛选通话事件。

`GET /call_events`

---

## Webhook

以下 Webhook 事件会被发送到您配置的 Webhook URL。所有 Webhook 都包含 `telnyx-timestamp` 和 `telnyx-signature-ed25519` 头部信息以进行验证（兼容标准 Webhook）。

| 事件 | 描述 |
|-------|-------------|
| `callAnswered` | 电话被接听 |
| `callStreamingStarted` | 通话流开始 |
| `callStreamingStopped` | 通话流停止 |
| `callStreamingFailed` | 通话流失败 |
| `callBridged` | 通话被桥接 |
| `callInitiated` | 通话开始 |
| `callHangup` | 通话挂断 |
| `callRecordingSaved` | 通话录音保存 |
| `callMachineDetectionEnded` | 机器检测结束 |
| `callMachineGreetingEnded` | 机器问候结束 |
| `callMachinePremiumDetectionEnded` | 机器高级检测结束 |
| `callMachinePremiumGreetingEnded` | 机器高级问候结束 |