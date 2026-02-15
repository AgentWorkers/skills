---
name: telnyx-numbers-compliance-java
description: >-
  Manage regulatory requirements, number bundles, supporting documents, and
  verified numbers for compliance. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: numbers-compliance
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字合规性 - Java

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

## 获取套餐信息

获取所有允许使用的套餐信息。

`GET /bundle_pricing/billing_bundles`

```java
import com.telnyx.sdk.models.bundlepricing.billingbundles.BillingBundleListPage;
import com.telnyx.sdk.models.bundlepricing.billingbundles.BillingBundleListParams;

BillingBundleListPage page = client.bundlePricing().billingBundles().list();
```

## 根据 ID 获取套餐

根据 ID 获取单个套餐。

`GET /bundle_pricing/billing_bundles/{bundle_id}`

```java
import com.telnyx.sdk.models.bundlepricing.billingbundles.BillingBundleRetrieveParams;
import com.telnyx.sdk.models.bundlepricing.billingbundles.BillingBundleRetrieveResponse;

BillingBundleRetrieveResponse billingBundle = client.bundlePricing().billingBundles().retrieve("8661948c-a386-4385-837f-af00f40f111a");
```

## 获取用户套餐

获取用户套餐的分页列表。

`GET /bundle_pricing/user_bundles`

```java
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleListPage;
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleListParams;

UserBundleListPage page = client.bundlePricing().userBundles().list();
```

## 创建用户套餐

为用户创建多个套餐。

`POST /bundle_pricing/user_bundles/bulk`

```java
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleCreateParams;
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleCreateResponse;

UserBundleCreateResponse userBundle = client.bundlePricing().userBundles().create();
```

## 获取未使用的用户套餐

返回所有未使用的用户套餐。

`GET /bundle_pricing/user_bundles/unused`

```java
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleListUnusedParams;
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleListUnusedResponse;

UserBundleListUnusedResponse response = client.bundlePricing().userBundles().listUnused();
```

## 根据 ID 获取用户套餐

根据 ID 获取用户套餐。

`GET /bundle_pricing/user_bundles/{user_bundle_id}`

```java
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleRetrieveParams;
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleRetrieveResponse;

UserBundleRetrieveResponse userBundle = client.bundlePricing().userBundles().retrieve("ca1d2263-d1f1-43ac-ba53-248e7a4bb26a");
```

## 取消激活用户套餐

根据 ID 取消激活用户套餐。

`DELETE /bundle_pricing/user_bundles/{user_bundle_id}`

```java
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleDeactivateParams;
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleDeactivateResponse;

UserBundleDeactivateResponse response = client.bundlePricing().userBundles().deactivate("ca1d2263-d1f1-43ac-ba53-248e7a4bb26a");
```

## 获取用户套餐资源

根据 ID 获取用户套餐的资源信息。

`GET /bundle_pricing/user_bundles/{user_bundle_id}/resources`

```java
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleListResourcesParams;
import com.telnyx.sdk.models.bundlepricing.userbundles.UserBundleListResourcesResponse;

UserBundleListResourcesResponse response = client.bundlePricing().userBundles().listResources("ca1d2263-d1f1-43ac-ba53-248e7a4bb26a");
```

## 列出所有文档链接

按创建时间降序列出所有文档链接。

`GET /document_links`

```java
import com.telnyx.sdk.models.documentlinks.DocumentLinkListPage;
import com.telnyx.sdk.models.documentlinks.DocumentLinkListParams;

DocumentLinkListPage page = client.documentLinks().list();
```

## 列出所有文档

按创建时间降序列出所有文档。

`GET /documents`

```java
import com.telnyx.sdk.models.documents.DocumentListPage;
import com.telnyx.sdk.models.documents.DocumentListParams;

DocumentListPage page = client.documents().list();
```

## 上传文档

上传文档。<br /><br />上传的文件必须在 30 分钟内关联到某个服务，否则将被自动删除。

`POST /documents`

```java
import com.telnyx.sdk.models.documents.DocumentUploadJsonParams;
import com.telnyx.sdk.models.documents.DocumentUploadJsonResponse;

DocumentUploadJsonResponse response = client.documents().uploadJson();
```

## 获取文档

获取文档信息。

`GET /documents/{id}`

```java
import com.telnyx.sdk.models.documents.DocumentRetrieveParams;
import com.telnyx.sdk.models.documents.DocumentRetrieveResponse;

DocumentRetrieveResponse document = client.documents().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新文档

更新文档内容。

`PATCH /documents/{id}`

```java
import com.telnyx.sdk.models.documents.DocServiceDocument;
import com.telnyx.sdk.models.documents.DocumentUpdateParams;
import com.telnyx.sdk.models.documents.DocumentUpdateResponse;

DocumentUpdateParams params = DocumentUpdateParams.builder()
    .documentId("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .docServiceDocument(DocServiceDocument.builder().build())
    .build();
DocumentUpdateResponse document = client.documents().update(params);
```

## 删除文档

删除文档。<br /><br />只有未关联到任何服务的文档才能被删除。

`DELETE /documents/{id}`

```java
import com.telnyx.sdk.models.documents.DocumentDeleteParams;
import com.telnyx.sdk.models.documents.DocumentDeleteResponse;

DocumentDeleteResponse document = client.documents().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 下载文档

下载文档。

`GET /documents/{id}/download`

```java
import com.telnyx.sdk.core.http.HttpResponse;
import com.telnyx.sdk.models.documents.DocumentDownloadParams;

HttpResponse response = client.documents().download("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 生成文档的临时下载链接

生成一个临时预签名 URL，可以直接从存储后端下载文档，无需身份验证。

`GET /documents/{id}/download_link`

```java
import com.telnyx.sdk.models.documents.DocumentGenerateDownloadLinkParams;
import com.telnyx.sdk.models.documents.DocumentGenerateDownloadLinkResponse;

DocumentGenerateDownloadLinkResponse response = client.documents().generateDownloadLink("550e8400-e29b-41d4-a716-446655440000");
```

## 列出所有需求

支持过滤、排序和分页功能，列出所有需求。

`GET /requirements`

```java
import com.telnyx.sdk.models.requirements.RequirementListPage;
import com.telnyx.sdk.models.requirements.RequirementListParams;

RequirementListPage page = client.requirements().list();
```

## 获取文档需求信息

获取单个文档需求记录。

`GET /requirements/{id}`

```java
import com.telnyx.sdk.models.requirements.RequirementRetrieveParams;
import com.telnyx.sdk.models.requirements.RequirementRetrieveResponse;

RequirementRetrieveResponse requirement = client.requirements().retrieve("a9dad8d5-fdbd-49d7-aa23-39bb08a5ebaa");
```

## 列出所有需求类型

按创建时间降序列出所有需求类型。

`GET /requirement_types`

```java
import com.telnyx.sdk.models.requirementtypes.RequirementTypeListParams;
import com.telnyx.sdk.models.requirementtypes.RequirementTypeListResponse;

RequirementTypeListResponse requirementTypes = client.requirementTypes().list();
```

## 根据 ID 获取需求类型

根据 ID 获取特定需求类型。

`GET /requirement_types/{id}`

```java
import com.telnyx.sdk.models.requirementtypes.RequirementTypeRetrieveParams;
import com.telnyx.sdk.models.requirementtypes.RequirementTypeRetrieveResponse;

RequirementTypeRetrieveResponse requirementType = client.requirementTypes().retrieve("a38c217a-8019-48f8-bff6-0fdd9939075b");
```

## 获取监管要求

获取所有监管要求信息。

`GET /regulatory_requirements`

```java
import com.telnyx.sdk.models.regulatoryrequirements.RegulatoryRequirementRetrieveParams;
import com.telnyx.sdk.models.regulatoryrequirements.RegulatoryRequirementRetrieveResponse;

RegulatoryRequirementRetrieveResponse regulatoryRequirement = client.regulatoryRequirements().retrieve();
```

## 列出需求组

列出所有需求组。

`GET /requirement_groups`

```java
import com.telnyx.sdk.models.requirementgroups.RequirementGroup;
import com.telnyx.sdk.models.requirementgroups.RequirementGroupListParams;

List<RequirementGroup> requirementGroups = client.requirementGroups().list();
```

## 创建新的需求组

创建新的需求组。<br />必需参数：`country_code`、`phone_number_type`、`action`

```java
import com.telnyx.sdk.models.requirementgroups.RequirementGroup;
import com.telnyx.sdk.models.requirementgroups.RequirementGroupCreateParams;

RequirementGroupCreateParams params = RequirementGroupCreateParams.builder()
    .action(RequirementGroupCreateParams.Action.ORDERING)
    .countryCode("US")
    .phoneNumberType(RequirementGroupCreateParams.PhoneNumberType.LOCAL)
    .build();
RequirementGroup requirementGroup = client.requirementGroups().create(params);
```

## 根据 ID 获取单个需求组

根据 ID 获取特定需求组。

`GET /requirement_groups/{id}`

```java
import com.telnyx.sdk.models.requirementgroups.RequirementGroup;
import com.telnyx.sdk.models.requirementgroups.RequirementGroupRetrieveParams;

RequirementGroup requirementGroup = client.requirementGroups().retrieve("id");
```

## 更新需求组中的需求信息

更新需求组中的需求信息。

`PATCH /requirement_groups/{id}`

```java
import com.telnyx.sdk.models.requirementgroups.RequirementGroup;
import com.telnyx.sdk.models.requirementgroups.RequirementGroupUpdateParams;

RequirementGroup requirementGroup = client.requirementGroups().update("id");
```

## 根据 ID 删除需求组

根据 ID 删除需求组。

`DELETE /requirement_groups/{id}`

```java
import com.telnyx.sdk.models.requirementgroups.RequirementGroup;
import com.telnyx.sdk.models.requirementgroups.RequirementGroupDeleteParams;

RequirementGroup requirementGroup = client.requirementGroups().delete("id");
```

## 提交需求组以供审批

提交需求组以供审批。

`POST /requirement_groups/{id}/submit_for_approval`

```java
import com.telnyx.sdk.models.requirementgroups.RequirementGroup;
import com.telnyx.sdk.models.requirementgroups.RequirementGroupSubmitForApprovalParams;

RequirementGroup requirementGroup = client.requirementGroups().submitForApproval("id");
```

## 列出所有已验证的号码

获取已验证号码的分页列表。

`GET /verified_numbers`

```java
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberListPage;
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberListParams;

VerifiedNumberListPage page = client.verifiedNumbers().list();
```

## 请求电话号码验证

启动电话号码验证流程。

`POST /verified_numbers` — 必需参数：`phone_number`、`verification_method`

```java
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberCreateParams;
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberCreateResponse;

VerifiedNumberCreateParams params = VerifiedNumberCreateParams.builder()
    .phoneNumber("+15551234567")
    .verificationMethod(VerifiedNumberCreateParams.VerificationMethod.SMS)
    .build();
VerifiedNumberCreateResponse verifiedNumber = client.verifiedNumbers().create(params);
```

## 获取已验证的号码

获取已验证的号码信息。

`GET /verified_numbers/{phone_number}`

```java
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberDataWrapper;
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberRetrieveParams;

VerifiedNumberDataWrapper verifiedNumberDataWrapper = client.verifiedNumbers().retrieve("+15551234567");
```

## 删除已验证的号码

删除已验证的号码。

`DELETE /verified_numbers/{phone_number}`

```java
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberDataWrapper;
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberDeleteParams;

VerifiedNumberDataWrapper verifiedNumberDataWrapper = client.verifiedNumbers().delete("+15551234567");
```

## 提交验证码

提交验证码。

`POST /verified_numbers/{phone_number}/actions/verify` — 必需参数：`verification_code`

```java
import com.telnyx.sdk.models.verifiednumbers.VerifiedNumberDataWrapper;
import com.telnyx.sdk.models.verifiednumbers.actions.ActionSubmitVerificationCodeParams;

ActionSubmitVerificationCodeParams params = ActionSubmitVerificationCodeParams.builder()
    .phoneNumber("+15551234567")
    .verificationCode("123456")
    .build();
VerifiedNumberDataWrapper verifiedNumberDataWrapper = client.verifiedNumbers().actions().submitVerificationCode(params);
```