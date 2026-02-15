---
name: telnyx-porting-in-java
description: >-
  Port phone numbers into Telnyx. Check portability, create port orders, upload
  LOA documents, and track porting status. This skill provides Java SDK
  examples.
metadata:
  author: telnyx
  product: porting-in
  language: java
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 移动号码服务（Java 版本）

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

## 列出所有移动号码迁移事件

返回所有移动号码迁移事件的列表。

`GET /porting/events`

```java
import com.telnyx.sdk.models.porting.events.EventListPage;
import com.telnyx.sdk.models.porting.events.EventListParams;

EventListPage page = client.porting().events().list();
```

## 显示特定迁移事件

显示特定的迁移事件。

`GET /porting/events/{id}`

```java
import com.telnyx.sdk.models.porting.events.EventRetrieveParams;
import com.telnyx.sdk.models.porting.events.EventRetrieveResponse;

EventRetrieveResponse event = client.porting().events().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 重新发布迁移事件

重新发布特定的迁移事件。

`POST /porting/events/{id}/republish`

```java
import com.telnyx.sdk.models.porting.events.EventRepublishParams;

client.porting().events().republish("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 预览 LOA（Letter of Authorization）配置参数

无需创建 LOA 配置即可预览其模板。

`POST /porting/loa_configuration_preview`

```java
import com.telnyx.sdk.core.http.HttpResponse;
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationPreview0Params;

LoaConfigurationPreview0Params params = LoaConfigurationPreview0Params.builder()
    .address(LoaConfigurationPreview0Params.Address.builder()
        .city("Austin")
        .countryCode("US")
        .state("TX")
        .streetAddress("600 Congress Avenue")
        .zipCode("78701")
        .build())
    .companyName("Telnyx")
    .contact(LoaConfigurationPreview0Params.Contact.builder()
        .email("testing@telnyx.com")
        .phoneNumber("+12003270001")
        .build())
    .logo(LoaConfigurationPreview0Params.Logo.builder()
        .documentId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
        .build())
    .name("My LOA Configuration")
    .build();
HttpResponse response = client.porting().loaConfigurations().preview0(params);
```

## 列出 LOA 配置

列出所有的 LOA 配置。

`GET /porting/loa_configurations`

```java
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationListPage;
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationListParams;

LoaConfigurationListPage page = client.porting().loaConfigurations().list();
```

## 创建 LOA 配置

创建一个新的 LOA 配置。

`POST /porting/loa_configurations`

```java
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationCreateParams;
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationCreateResponse;

LoaConfigurationCreateParams params = LoaConfigurationCreateParams.builder()
    .address(LoaConfigurationCreateParams.Address.builder()
        .city("Austin")
        .countryCode("US")
        .state("TX")
        .streetAddress("600 Congress Avenue")
        .zipCode("78701")
        .build())
    .companyName("Telnyx")
    .contact(LoaConfigurationCreateParams.Contact.builder()
        .email("testing@telnyx.com")
        .phoneNumber("+12003270001")
        .build())
    .logo(LoaConfigurationCreateParams.Logo.builder()
        .documentId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
        .build())
    .name("My LOA Configuration")
    .build();
LoaConfigurationCreateResponse loaConfiguration = client.porting().loaConfigurations().create(params);
```

## 获取 LOA 配置

获取特定的 LOA 配置。

`GET /porting/loa_configurations/{id}`

```java
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationRetrieveParams;
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationRetrieveResponse;

LoaConfigurationRetrieveResponse loaConfiguration = client.porting().loaConfigurations().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 更新 LOA 配置

更新特定的 LOA 配置。

`PATCH /porting/loa_configurations/{id}`

```java
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationUpdateParams;
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationUpdateResponse;

LoaConfigurationUpdateParams params = LoaConfigurationUpdateParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .address(LoaConfigurationUpdateParams.Address.builder()
        .city("Austin")
        .countryCode("US")
        .state("TX")
        .streetAddress("600 Congress Avenue")
        .zipCode("78701")
        .build())
    .companyName("Telnyx")
    .contact(LoaConfigurationUpdateParams.Contact.builder()
        .email("testing@telnyx.com")
        .phoneNumber("+12003270001")
        .build())
    .logo(LoaConfigurationUpdateParams.Logo.builder()
        .documentId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
        .build())
    .name("My LOA Configuration")
    .build();
LoaConfigurationUpdateResponse loaConfiguration = client.porting().loaConfigurations().update(params);
```

## 删除 LOA 配置

删除特定的 LOA 配置。

`DELETE /porting/loa_configurations/{id}`

```java
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationDeleteParams;

client.porting().loaConfigurations().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 预览 LOA 配置

预览特定的 LOA 配置。

`GET /porting/loa_configurations/{id}/preview`

```java
import com.telnyx.sdk.core.http.HttpResponse;
import com.telnyx.sdk.models.porting.loaconfigurations.LoaConfigurationPreview1Params;

HttpResponse response = client.porting().loaConfigurations().preview1("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出所有迁移订单

返回所有迁移订单的列表。

`GET /porting_orders`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderListPage;
import com.telnyx.sdk.models.portingorders.PortingOrderListParams;

PortingOrderListPage page = client.portingOrders().list();
```

## 创建迁移订单

创建一个新的迁移订单对象。

`POST /porting_orders` — 必需参数：`phone_numbers`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderCreateParams;
import com.telnyx.sdk.models.portingorders.PortingOrderCreateResponse;
import java.util.List;

PortingOrderCreateParams params = PortingOrderCreateParams.builder()
    .phoneNumbers(List.of(
      "+13035550000",
      "+13035550001",
      "+13035550002"
    ))
    .build();
PortingOrderCreateResponse portingOrder = client.portingOrders().create(params);
```

## 获取迁移订单详情

获取现有迁移订单的详细信息。

`GET /porting_orders/{id}`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveParams;
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveResponse;

PortingOrderRetrieveResponse portingOrder = client.portingOrders().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 编辑迁移订单

编辑现有迁移订单的详细信息。

`PATCH /porting_orders/{id}`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderUpdateParams;
import com.telnyx.sdk.models.portingorders.PortingOrderUpdateResponse;

PortingOrderUpdateResponse portingOrder = client.portingOrders().update("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除迁移订单

删除现有的迁移订单。

`DELETE /porting_orders/{id}`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderDeleteParams;

client.portingOrders().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 异步激活迁移订单中的每个号码

异步激活迁移订单中的每个号码。

`POST /porting_orders/{id}/actions/activate`

```java
import com.telnyx.sdk.models.portingorders.actions.ActionActivateParams;
import com.telnyx.sdk.models.portingorders.actions.ActionActivateResponse;

ActionActivateResponse response = client.portingOrders().actions().activate("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 取消迁移订单

取消迁移订单。

`POST /porting_orders/{id}/actions/cancel`

```java
import com.telnyx.sdk.models.portingorders.actions.ActionCancelParams;
import com.telnyx.sdk.models.portingorders.actions.ActionCancelResponse;

ActionCancelResponse response = client.portingOrders().actions().cancel("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 提交迁移订单

确认并提交迁移订单。

`POST /porting_orders/{id}/actions/confirm`

```java
import com.telnyx.sdk.models.portingorders.actions.ActionConfirmParams;
import com.telnyx.sdk.models.portingorders.actions.ActionConfirmResponse;

ActionConfirmResponse response = client.portingOrders().actions().confirm("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 共享迁移订单

为迁移订单创建共享令牌。

`POST /porting_orders/{id}/actions/share`

```java
import com.telnyx.sdk.models.portingorders.actions.ActionShareParams;
import com.telnyx.sdk.models.portingorders.actions.ActionShareResponse;

ActionShareResponse response = client.portingOrders().actions().share("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出所有迁移激活任务

返回所有迁移激活任务的列表。

`GET /porting_orders/{id}/activation_jobs`

```java
import com.telnyx.sdk.models.portingorders.activationjobs.ActivationJobListPage;
import com.telnyx.sdk.models.portingorders.activationjobs.ActivationJobListParams;

ActivationJobListPage page = client.portingOrders().activationJobs().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取迁移激活任务详情

获取特定的迁移激活任务。

`GET /porting_orders/{id}/activation_jobs/{activationJobId}`

```java
import com.telnyx.sdk.models.portingorders.activationjobs.ActivationJobRetrieveParams;
import com.telnyx.sdk.models.portingorders.activationjobs.ActivationJobRetrieveResponse;

ActivationJobRetrieveParams params = ActivationJobRetrieveParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .activationJobId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
ActivationJobRetrieveResponse activationJob = client.portingOrders().activationJobs().retrieve(params);
```

## 更新迁移激活任务

更新迁移激活任务的激活时间。

`PATCH /porting_orders/{id}/activation_jobs/{activationJobId}`

```java
import com.telnyx.sdk.models.portingorders.activationjobs.ActivationJobUpdateParams;
import com.telnyx.sdk.models.portingorders.activationjobs.ActivationJobUpdateResponse;

ActivationJobUpdateParams params = ActivationJobUpdateParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .activationJobId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
ActivationJobUpdateResponse activationJob = client.portingOrders().activationJobs().update(params);
```

## 列出附加文档

返回迁移订单的所有附加文档列表。

`GET /porting_orders/{id}/additional_documents`

```java
import com.telnyx.sdk.models.portingorders.additionaldocuments.AdditionalDocumentListPage;
import com.telnyx.sdk.models.portingorders.additionaldocuments.AdditionalDocumentListParams;

AdditionalDocumentListPage page = client.portingOrders().additionalDocuments().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 创建附加文档列表

为迁移订单创建附加文档列表。

`POST /porting_orders/{id}/additional_documents`

```java
import com.telnyx.sdk.models.portingorders.additionaldocuments.AdditionalDocumentCreateParams;
import com.telnyx.sdk.models.portingorders.additionaldocuments.AdditionalDocumentCreateResponse;

AdditionalDocumentCreateResponse additionalDocument = client.portingOrders().additionalDocuments().create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除附加文档

删除迁移订单中的附加文档。

`DELETE /porting_orders/{id}/additional_documents/{additional_document_id}`

```java
import com.telnyx.sdk.models.portingorders.additionaldocuments.AdditionalDocumentDeleteParams;

AdditionalDocumentDeleteParams params = AdditionalDocumentDeleteParams.builder()
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .additionalDocumentId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
client.portingOrders().additionalDocuments().delete(params);
```

## 列出允许的 FOC（Free of Charge）日期

返回迁移订单允许的 FOC 日期列表。

`GET /porting_orders/{id}/allowed_foc_windows`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveAllowedFocWindowsParams;
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveAllowedFocWindowsResponse;

PortingOrderRetrieveAllowedFocWindowsResponse response = client.portingOrders().retrieveAllowedFocWindows("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出迁移订单的所有评论

返回迁移订单的所有评论列表。

`GET /porting_orders/{id}/comments`

```java
import com.telnyx.sdk.models.portingorders.comments.CommentListPage;
import com.telnyx.sdk.models.portingorders.comments.CommentListParams;

CommentListPage page = client.portingOrders().comments().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 为迁移订单创建评论

为迁移订单创建新的评论。

`POST /porting_orders/{id}/comments`

```java
import com.telnyx.sdk.models.portingorders.comments.CommentCreateParams;
import com.telnyx.sdk.models.portingorders.comments.CommentCreateResponse;

CommentCreateResponse comment = client.portingOrders().comments().create("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 下载迁移订单的 LOA 模板

下载迁移订单的 LOA 模板。

`GET /porting_orders/{id}/loa_template`

```java
import com.telnyx.sdk.core.http.HttpResponse;
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveLoaTemplateParams;

HttpResponse response = client.portingOrders().retrieveLoaTemplate("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出迁移订单的需求

根据国家/号码类型列出所有迁移订单的需求。

`GET /porting_orders/{id}/requirements`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveRequirementsPage;
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveRequirementsParams;

PortingOrderRetrieveRequirementsPage page = client.portingOrders().retrieveRequirements("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取关联的 V1 子请求 ID 和端口请求 ID

获取迁移订单的关联 V1 子请求 ID 和端口请求 ID。

`GET /porting_orders/{id}/sub_request`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveSubRequestParams;
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveSubRequestResponse;

PortingOrderRetrieveSubRequestResponse response = client.portingOrders().retrieveSubRequest("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 获取验证代码

获取迁移订单的所有验证代码。

`GET /porting_orders/{id}/verification_codes`

```java
import com.telnyx.sdk.models.portingorders.verificationcodes.VerificationCodeListPage;
import com.telnyx.sdk.models.portingorders.verificationcodes.VerificationCodeListParams;

VerificationCodeListPage page = client.portingOrders().verificationCodes().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 发送验证代码

为所有迁移号码发送验证代码。

`POST /porting_orders/{id}/verification_codes/send`

```java
import com.telnyx.sdk.models.portingorders.verificationcodes.VerificationCodeSendParams;

client.portingOrders().verificationCodes().send("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 验证一系列号码的验证代码

验证一系列号码的验证代码。

`POST /porting_orders/{id}/verification_codes/verify`

```java
import com.telnyx.sdk.models.portingorders.verificationcodes.VerificationCodeVerifyParams;
import com.telnyx.sdk.models.portingorders.verificationcodes.VerificationCodeVerifyResponse;

VerificationCodeVerifyResponse response = client.portingOrders().verificationCodes().verify("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出迁移订单的动作需求

列出特定迁移订单的所有动作需求。

`GET /porting_orders/{porting_order_id}/action_requirements`

```java
import com.telnyx.sdk.models.portingorders.actionrequirements.ActionRequirementListPage;
import com.telnyx.sdk.models.portingorders.actionrequirements.ActionRequirementListParams;

ActionRequirementListPage page = client.portingOrders().actionRequirements().list("porting_order_id");
```

## 启动动作需求

为迁移订单启动特定的动作需求。

`POST /porting_orders/{porting_order_id}/action_requirements/{id}/initiate`

```java
import com.telnyx.sdk.models.portingorders.actionrequirements.ActionRequirementInitiateParams;
import com.telnyx.sdk.models.portingorders.actionrequirements.ActionRequirementInitiateResponse;

ActionRequirementInitiateParams params = ActionRequirementInitiateParams.builder()
    .portingOrderId("porting_order_id")
    .id("id")
    .params(ActionRequirementInitiateParams.Params.builder()
        .firstName("John")
        .lastName("Doe")
        .build())
    .build();
ActionRequirementInitiateResponse response = client.portingOrders().actionRequirements().initiate(params);
```

## 列出所有关联的号码

列出迁移订单的所有关联号码。

`GET /porting_orders/{id}/associated_phone_numbers`

```java
import com.telnyx.sdk.models.portingorders.associatedphonenumbers.AssociatedPhoneNumberListPage;
import com.telnyx.sdk.models.portingorders.associatedphonenumbers.AssociatedPhoneNumberListParams;

AssociatedPhoneNumberListPage page = client.portingOrders().associatedPhoneNumbers().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 创建关联号码

为迁移订单创建新的关联号码。

`POST /porting_orders/{id}/associated_phone_numbers`

```java
import com.telnyx.sdk.models.portingorders.associatedphonenumbers.AssociatedPhoneNumberCreateParams;
import com.telnyx.sdk.models.portingorders.associatedphonenumbers.AssociatedPhoneNumberCreateResponse;

AssociatedPhoneNumberCreateParams params = AssociatedPhoneNumberCreateParams.builder()
    .portingOrderId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .action(AssociatedPhoneNumberCreateParams.Action.KEEP)
    .phoneNumberRange(AssociatedPhoneNumberCreateParams.PhoneNumberRange.builder().build())
    .build();
AssociatedPhoneNumberCreateResponse associatedPhoneNumber = client.portingOrders().associatedPhoneNumbers().create(params);
```

## 删除关联号码

从迁移订单中删除关联号码。

`DELETE /porting_orders/{id}/associated_phone_numbers/{id}`

```java
import com.telnyx.sdk.models.portingorders.associatedphonenumbers.AssociatedPhoneNumberDeleteParams;
import com.telnyx.sdk.models.portingorders.associatedphonenumbers.AssociatedPhoneNumberDeleteResponse;

AssociatedPhoneNumberDeleteParams params = AssociatedPhoneNumberDeleteParams.builder()
    .portingOrderId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
AssociatedPhoneNumberDeleteResponse associatedPhoneNumber = client.portingOrders().associatedPhoneNumbers().delete(params);
```

## 列出所有号码块

返回迁移订单的所有号码块列表。

`GET /porting_orders/{id}/phone_number_blocks`

```java
import com.telnyx.sdk.models.portingorders.phonenumberblocks.PhoneNumberBlockListPage;
import com.telnyx.sdk.models.portingorders.phonenumberblocks.PhoneNumberBlockListParams;

PhoneNumberBlockListPage page = client.portingOrders().phoneNumberBlocks().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 创建号码块

为迁移订单创建新的号码块。

`POST /porting_orders/{id}/phone_number_blocks`

```java
import com.telnyx.sdk.models.portingorders.phonenumberblocks.PhoneNumberBlockCreateParams;
import com.telnyx.sdk.models.portingorders.phonenumberblocks.PhoneNumberBlockCreateResponse;

PhoneNumberBlockCreateParams params = PhoneNumberBlockCreateParams.builder()
    .portingOrderId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .addActivationRange(PhoneNumberBlockCreateParams.ActivationRange.builder()
        .endAt("+4930244999910")
        .startAt("+4930244999901")
        .build())
    .phoneNumberRange(PhoneNumberBlockCreateParams.PhoneNumberRange.builder()
        .endAt("+4930244999910")
        .startAt("+4930244999901")
        .build())
    .build();
PhoneNumberBlockCreateResponse phoneNumberBlock = client.portingOrders().phoneNumberBlocks().create(params);
```

## 删除号码块

删除迁移订单中的号码块。

`DELETE /porting_orders/{id}/phone_number_blocks/{id}`

```java
import com.telnyx.sdk.models.portingorders.phonenumberblocks.PhoneNumberBlockDeleteParams;
import com.telnyx.sdk.models.portingorders.phonenumberblocks.PhoneNumberBlockDeleteResponse;

PhoneNumberBlockDeleteParams params = PhoneNumberBlockDeleteParams.builder()
    .portingOrderId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
PhoneNumberBlockDeleteResponse phoneNumberBlock = client.portingOrders().phoneNumberBlocks().delete(params);
```

## 列出所有号码扩展名

返回迁移订单的所有号码扩展名列表。

`GET /porting_orders/{id}/phone_numberextensions`

```java
import com.telnyx.sdk.models.portingorders.phonenumberextensions.PhoneNumberExtensionListPage;
import com.telnyx.sdk.models.portingorders.phonenumberextensions.PhoneNumberExtensionListParams;

PhoneNumberExtensionListPage page = client.portingOrders().phoneNumberExtensions().list("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 创建号码扩展名

为迁移订单创建新的号码扩展名。

`POST /porting_orders/{id}/phone_numberextensions`

```java
import com.telnyx.sdk.models.portingorders.phonenumberextensions.PhoneNumberExtensionCreateParams;
import com.telnyx.sdk.models.portingorders.phonenumberextensions.PhoneNumberExtensionCreateResponse;

PhoneNumberExtensionCreateParams params = PhoneNumberExtensionCreateParams.builder()
    .portingOrderId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .addActivationRange(PhoneNumberExtensionCreateParams.ActivationRange.builder()
        .endAt(10L)
        .startAt(1L)
        .build())
    .extensionRange(PhoneNumberExtensionCreateParams.ExtensionRange.builder()
        .endAt(10L)
        .startAt(1L)
        .build())
    .portingPhoneNumberId("f24151b6-3389-41d3-8747-7dd8c681e5e2")
    .build();
PhoneNumberExtensionCreateResponse phoneNumberExtension = client.portingOrders().phoneNumberExtensions().create(params);
```

## 删除号码扩展名

删除迁移订单中的号码扩展名。

`DELETE /porting_orders/{id}/phone_number_extensions/{id}`

```java
import com.telnyx.sdk.models.portingorders.phonenumberextensions.PhoneNumberExtensionDeleteParams;
import com.telnyx.sdk.models.portingorders.phonenumberextensions.PhoneNumberExtensionDeleteResponse;

PhoneNumberExtensionDeleteParams params = PhoneNumberExtensionDeleteParams.builder()
    .portingOrderId("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .id("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e")
    .build();
PhoneNumberExtensionDeleteResponse phoneNumberExtension = client.portingOrders().phoneNumberExtensions().delete(params);
```

## 列出所有可能的异常类型

返回迁移订单的所有可能异常类型列表。

`GET /porting_orders/exception_types`

```java
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveExceptionTypesParams;
import com.telnyx.sdk.models.portingorders.PortingOrderRetrieveExceptionTypesResponse;

PortingOrderRetrieveExceptionTypesResponse response = client.portingOrders().retrieveExceptionTypes();
```

## 列出所有号码配置

分页显示迁移订单的所有号码配置。

`GET /porting_orders/phone_number_configurations`

```java
import com.telnyx.sdk.models.portingorders.phonenumberconfigurations.PhoneNumberConfigurationListPage;
import com.telnyx.sdk.models.portingorders.phonenumberconfigurations.PhoneNumberConfigurationListParams;

PhoneNumberConfigurationListPage page = client.portingOrders().phoneNumberConfigurations().list();
```

## 创建号码配置列表

创建迁移订单的所有号码配置列表。

`POST /porting_orders/phone_number_configurations`

```java
import com.telnyx.sdk.models.portingorders.phonenumberconfigurations.PhoneNumberConfigurationCreateParams;
import com.telnyx.sdk.models.portingorders.phonenumberconfigurations.PhoneNumberConfigurationCreateResponse;

PhoneNumberConfigurationCreateResponse phoneNumberConfiguration = client.portingOrders().phoneNumberConfigurations().create();
```

## 列出所有迁移号码

返回您的所有迁移号码列表。

`GET /porting/phone_numbers`

```java
import com.telnyx.sdk.models.portingphonenumbers.PortingPhoneNumberListPage;
import com.telnyx.sdk.models.portingphonenumbers.PortingPhoneNumberListParams;

PortingPhoneNumberListPage page = client.portingPhoneNumbers().list();
```

## 列出与迁移相关的报告

列出与迁移操作相关的报告。

`GET /porting/reports`

```java
import com.telnyx.sdk.models.porting.reports.ReportListPage;
import com.telnyx.sdk.models.porting.reports.ReportListParams;

ReportListPage page = client.porting().reports().list();
```

## 创建迁移相关报告

生成与迁移操作相关的报告。

`POST /porting/reports`

```java
import com.telnyx.sdk.models.porting.reports.ExportPortingOrdersCsvReport;
import com.telnyx.sdk.models.porting.reports.ReportCreateParams;
import com.telnyx.sdk.models.porting.reports.ReportCreateResponse;

ReportCreateParams params = ReportCreateParams.builder()
    .params(ExportPortingOrdersCsvReport.builder()
        .filters(ExportPortingOrdersCsvReport.Filters.builder().build())
        .build())
    .reportType(ReportCreateParams.ReportType.EXPORT_PORTING_ORDERS_CSV)
    .build();
ReportCreateResponse report = client.porting().reports().create(params);
```

## 获取报告

获取特定的报告。

`GET /porting/reports/{id}`

```java
import com.telnyx.sdk.models.porting.reports.ReportRetrieveParams;
import com.telnyx.sdk.models.porting.reports.ReportRetrieveResponse;

ReportRetrieveResponse report = client.porting().reports().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出英国的可用运营商

列出英国的可用运营商。

`GET /porting/uk_carriers`

```java
import com.telnyx.sdk.models.porting.PortingListUkCarriersParams;
import com.telnyx.sdk.models.porting.PortingListUkCarriersResponse;

PortingListUkCarriersResponse response = client.porting().listUkCarriers();
```

## 运行迁移检查

立即运行迁移检查并返回结果。

`POST /portability_checks`

```java
import com.telnyx.sdk.models.portabilitychecks.PortabilityCheckRunParams;
import com.telnyx.sdk.models.portabilitychecks.PortabilityCheckRunResponse;

PortabilityCheckRunResponse response = client.portabilityChecks().run();
```
```