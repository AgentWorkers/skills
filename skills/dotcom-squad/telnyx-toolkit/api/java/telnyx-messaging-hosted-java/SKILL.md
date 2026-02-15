---
name: telnyx-messaging-hosted-java
description: >-
  Set up hosted SMS numbers, toll-free verification, and RCS messaging. Use when
  migrating numbers or enabling rich messaging features. This skill provides
  Java SDK examples.
metadata:
  author: telnyx
  product: messaging-hosted
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 消息托管服务 - Java

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

## 列出托管消息服务的号码订单

`GET /messaging_hosted_number_orders`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderListPage;
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderListParams;

MessagingHostedNumberOrderListPage page = client.messagingHostedNumberOrders().list();
```

## 创建托管消息服务的号码订单

`POST /messaging_hosted_number_orders`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderCreateParams;
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderCreateResponse;

MessagingHostedNumberOrderCreateResponse messagingHostedNumberOrder = client.messagingHostedNumberOrders().create();
```

## 获取托管消息服务的号码订单信息

`GET /messaging_hosted_number_orders/{id}`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderRetrieveParams;
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderRetrieveResponse;

MessagingHostedNumberOrderRetrieveResponse messagingHostedNumberOrder = client.messagingHostedNumberOrders().retrieve("id");
```

## 删除托管消息服务的号码订单

删除托管消息服务的号码订单及其所有关联的电话号码。

`DELETE /messaging_hosted_number_orders/{id}`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderDeleteParams;
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderDeleteResponse;

MessagingHostedNumberOrderDeleteResponse messagingHostedNumberOrder = client.messagingHostedNumberOrders().delete("id");
```

## 上传托管号码相关文档

`POST /messaging_hosted_number_orders/{id}/actions/file_upload`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.actions.ActionUploadFileParams;
import com.telnyx.sdk.models.messaginghostednumberorders.actions.ActionUploadFileResponse;

ActionUploadFileResponse response = client.messagingHostedNumberOrders().actions().uploadFile("id");
```

## 验证托管号码的验证码

验证发送到托管号码的验证码。

`POST /messaging_hosted_number_orders/{id}/validation_codes` — 必需参数：`verification_codes`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderValidateCodesParams;
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderValidateCodesResponse;

MessagingHostedNumberOrderValidateCodesParams params = MessagingHostedNumberOrderValidateCodesParams.builder()
    .id("id")
    .addVerificationCode(MessagingHostedNumberOrderValidateCodesParams.VerificationCode.builder()
        .code("code")
        .phoneNumber("phone_number")
        .build())
    .build();
MessagingHostedNumberOrderValidateCodesResponse response = client.messagingHostedNumberOrders().validateCodes(params);
```

## 生成托管号码的验证码

为托管号码生成验证码。

`POST /messaging_hosted_number_orders/{id}/verification_codes` — 必需参数：`phone_numbers`, `verification_method`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderCreateVerificationCodesParams;
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderCreateVerificationCodesResponse;

MessagingHostedNumberOrderCreateVerificationCodesParams params = MessagingHostedNumberOrderCreateVerificationCodesParams.builder()
    .id("id")
    .addPhoneNumber("string")
    .verificationMethod(MessagingHostedNumberOrderCreateVerificationCodesParams.VerificationMethod.SMS)
    .build();
MessagingHostedNumberOrderCreateVerificationCodesResponse response = client.messagingHostedNumberOrders().createVerificationCodes(params);
```

## 检查托管号码的适用性

`POST /messaging_hosted_number_orders/eligibility_numbers_check` — 必需参数：`phone_numbers`

```java
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderCheckEligibilityParams;
import com.telnyx.sdk.models.messaginghostednumberorders.MessagingHostedNumberOrderCheckEligibilityResponse;

MessagingHostedNumberOrderCheckEligibilityParams params = MessagingHostedNumberOrderCheckEligibilityParams.builder()
    .addPhoneNumber("string")
    .build();
MessagingHostedNumberOrderCheckEligibilityResponse response = client.messagingHostedNumberOrders().checkEligibility(params);
```

## 删除托管消息服务的号码

`DELETE /messaging_hosted_numbers/{id}`

```java
import com.telnyx.sdk.models.messaginghostednumbers.MessagingHostedNumberDeleteParams;
import com.telnyx.sdk.models.messaginghostednumbers.MessagingHostedNumberDeleteResponse;

MessagingHostedNumberDeleteResponse messagingHostedNumber = client.messagingHostedNumbers().delete("id");
```

## 发送 RCS 消息

`POST /messages/rcs` — 必需参数：`agent_id`, `to`, `messaging_profile_id`, `agent_message`

```java
import com.telnyx.sdk.models.messages.RcsAgentMessage;
import com.telnyx.sdk.models.messages.rcs.RcSendParams;
import com.telnyx.sdk.models.messages.rcs.RcSendResponse;

RcSendParams params = RcSendParams.builder()
    .agentId("Agent007")
    .agentMessage(RcsAgentMessage.builder().build())
    .messagingProfileId("messaging_profile_id")
    .to("+13125551234")
    .build();
RcSendResponse response = client.messages().rcs().send(params);
```

## 列出所有 RCS 代理

`GET /messaging/rcs/agents`

```java
import com.telnyx.sdk.models.messaging.rcs.agents.AgentListPage;
import com.telnyx.sdk.models.messaging.rcs.agents.AgentListParams;

AgentListPage page = client.messaging().rcs().agents().list();
```

## 获取单个 RCS 代理的信息

`GET /messaging/rcs/agents/{id}`

```java
import com.telnyx.sdk.models.messaging.rcs.agents.AgentRetrieveParams;
import com.telnyx.sdk.models.rcsagents.RcsAgentResponse;

RcsAgentResponse rcsAgentResponse = client.messaging().rcs().agents().retrieve("id");
```

## 修改 RCS 代理的信息

`PATCH /messaging/rcs/agents/{id}`

```java
import com.telnyx.sdk.models.messaging.rcs.agents.AgentUpdateParams;
import com.telnyx.sdk.models.rcsagents.RcsAgentResponse;

RcsAgentResponse rcsAgentResponse = client.messaging().rcs().agents().update("id");
```

## 检查 RCS 功能（批量）

`POST /messaging/rcs/bulk_capabilities` — 必需参数：`agent_id`, `phone_numbers`

```java
import com.telnyx.sdk.models.messaging.rcs.RcListBulkCapabilitiesParams;
import com.telnyx.sdk.models.messaging.rcs.RcListBulkCapabilitiesResponse;

RcListBulkCapabilitiesParams params = RcListBulkCapabilitiesParams.builder()
    .agentId("TestAgent")
    .addPhoneNumber("+13125551234")
    .build();
RcListBulkCapabilitiesResponse response = client.messaging().rcs().listBulkCapabilities(params);
```

## 检查单个 RCS 代理的功能

`GET /messaging/rcs/capabilities/{agent_id}/{phone_number}`

```java
import com.telnyx.sdk.models.messaging.rcs.RcRetrieveCapabilitiesParams;
import com.telnyx.sdk.models.messaging.rcs.RcRetrieveCapabilitiesResponse;

RcRetrieveCapabilitiesParams params = RcRetrieveCapabilitiesParams.builder()
    .agentId("agent_id")
    .phoneNumber("phone_number")
    .build();
RcRetrieveCapabilitiesResponse response = client.messaging().rcs().retrieveCapabilities(params);
```

## 添加 RCS 测试号码

为 RCS 代理添加测试电话号码以供测试使用。

`PUT /messaging/rcs/test_number_invite/{id}/{phone_number}`

```java
import com.telnyx.sdk.models.messaging.rcs.RcInviteTestNumberParams;
import com.telnyx.sdk.models.messaging.rcs.RcInviteTestNumberResponse;

RcInviteTestNumberParams params = RcInviteTestNumberParams.builder()
    .id("id")
    .phoneNumber("phone_number")
    .build();
RcInviteTestNumberResponse response = client.messaging().rcs().inviteTestNumber(params);
```

## 生成 RCS 深链接

生成可用于与特定代理发起 RCS 对话的深链接。

`GET /messages/rcs_deeplinks/{agent_id}`

```java
import com.telnyx.sdk.models.messages.rcs.RcGenerateDeeplinkParams;
import com.telnyx.sdk.models.messages.rcs.RcGenerateDeeplinkResponse;

RcGenerateDeeplinkResponse response = client.messages().rcs().generateDeeplink("agent_id");
```

## 列出验证码请求

获取之前提交的免费电话号码验证码请求列表

`GET /messaging_tollfree/verification/requests`

```java
import com.telnyx.sdk.models.messagingtollfree.verification.requests.RequestListPage;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.RequestListParams;

RequestListParams params = RequestListParams.builder()
    .page(1L)
    .pageSize(1L)
    .build();
RequestListPage page = client.messagingTollfree().verification().requests().list(params);
```

## 提交验证码请求

提交新的免费电话号码验证码请求

`POST /messaging_tollfree/verification/requests` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```java
import com.telnyx.sdk.models.messagingtollfree.verification.requests.RequestCreateParams;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.TfPhoneNumber;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.TfVerificationRequest;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.Url;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.UseCaseCategories;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.VerificationRequestEgress;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.Volume;

TfVerificationRequest params = TfVerificationRequest.builder()
    .additionalInformation("additionalInformation")
    .businessAddr1("600 Congress Avenue")
    .businessCity("Austin")
    .businessContactEmail("email@example.com")
    .businessContactFirstName("John")
    .businessContactLastName("Doe")
    .businessContactPhone("+18005550100")
    .businessName("Telnyx LLC")
    .businessState("Texas")
    .businessZip("78701")
    .corporateWebsite("http://example.com")
    .isvReseller("isvReseller")
    .messageVolume(Volume.V_100000)
    .optInWorkflow("User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset")
    .addOptInWorkflowImageUrl(Url.builder()
        .url("https://telnyx.com/sign-up")
        .build())
    .addOptInWorkflowImageUrl(Url.builder()
        .url("https://telnyx.com/company/data-privacy")
        .build())
    .addPhoneNumber(TfPhoneNumber.builder()
        .phoneNumber("+18773554398")
        .build())
    .addPhoneNumber(TfPhoneNumber.builder()
        .phoneNumber("+18773554399")
        .build())
    .productionMessageContent("Your Telnyx OTP is XXXX")
    .useCase(UseCaseCategories.TWO_FA)
    .useCaseSummary("This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal")
    .build();
VerificationRequestEgress verificationRequestEgress = client.messagingTollfree().verification().requests().create(params);
```

## 获取验证码请求信息

通过 ID 获取单个验证码请求的详细信息。

`GET /messaging_tollfree/verification/requests/{id}`

```java
import com.telnyx.sdk.models.messagingtollfree.verification.requests.RequestRetrieveParams;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.VerificationRequestStatus;

VerificationRequestStatus verificationRequestStatus = client.messagingTollfree().verification().requests().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 更新验证码请求

更新现有的免费电话号码验证码请求。

`PATCH /messaging_tollfree/verification/requests/{id}` — 必需参数：`businessName`, `corporateWebsite`, `businessAddr1`, `businessCity`, `businessState`, `businessZip`, `businessContactFirstName`, `businessContactLastName`, `businessContactEmail`, `businessContactPhone`, `messageVolume`, `phoneNumbers`, `useCase`, `useCaseSummary`, `productionMessageContent`, `optInWorkflow`, `optInWorkflowImageURLs`, `additionalInformation`, `isvReseller`

```java
import com.telnyx.sdk.models.messagingtollfree.verification.requests.RequestUpdateParams;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.TfPhoneNumber;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.TfVerificationRequest;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.Url;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.UseCaseCategories;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.VerificationRequestEgress;
import com.telnyx.sdk.models.messagingtollfree.verification.requests.Volume;

RequestUpdateParams params = RequestUpdateParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .tfVerificationRequest(TfVerificationRequest.builder()
        .additionalInformation("additionalInformation")
        .businessAddr1("600 Congress Avenue")
        .businessCity("Austin")
        .businessContactEmail("email@example.com")
        .businessContactFirstName("John")
        .businessContactLastName("Doe")
        .businessContactPhone("+18005550100")
        .businessName("Telnyx LLC")
        .businessState("Texas")
        .businessZip("78701")
        .corporateWebsite("http://example.com")
        .isvReseller("isvReseller")
        .messageVolume(Volume.V_100000)
        .optInWorkflow("User signs into the Telnyx portal, enters a number and is prompted to select whether they want to use 2FA verification for security purposes. If they've opted in a confirmation message is sent out to the handset")
        .addOptInWorkflowImageUrl(Url.builder()
            .url("https://telnyx.com/sign-up")
            .build())
        .addOptInWorkflowImageUrl(Url.builder()
            .url("https://telnyx.com/company/data-privacy")
            .build())
        .addPhoneNumber(TfPhoneNumber.builder()
            .phoneNumber("+18773554398")
            .build())
        .addPhoneNumber(TfPhoneNumber.builder()
            .phoneNumber("+18773554399")
            .build())
        .productionMessageContent("Your Telnyx OTP is XXXX")
        .useCase(UseCaseCategories.TWO_FA)
        .useCaseSummary("This is a use case where Telnyx sends out 2FA codes to portal users to verify their identity in order to sign into the portal")
        .build())
    .build();
VerificationRequestEgress verificationRequestEgress = client.messagingTollfree().verification().requests().update(params);
```

## 删除验证码请求

只有当验证码请求处于“被拒绝”状态时，才能删除该请求。

`DELETE /messaging_tollfree/verification/requests/{id}`

```java
import com.telnyx.sdk.models.messagingtollfree.verification.requests.RequestDeleteParams;

client.messagingTollfree().verification().requests().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```