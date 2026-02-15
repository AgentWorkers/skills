---
name: telnyx-numbers-compliance-javascript
description: >-
  Manage regulatory requirements, number bundles, supporting documents, and
  verified numbers for compliance. This skill provides JavaScript SDK examples.
metadata:
  author: telnyx
  product: numbers-compliance
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字合规性 - JavaScript

## 安装

```bash
npm install telnyx
```

## 设置

```javascript
import Telnyx from 'telnyx';

const client = new Telnyx({
  apiKey: process.env['TELNYX_API_KEY'], // This is the default and can be omitted
});
```

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取捆绑包

获取所有允许使用的捆绑包。

`GET /bundle_pricing/billing_bundles`

```javascript
// Automatically fetches more pages as needed.
for await (const billingBundleSummary of client.bundlePricing.billingBundles.list()) {
  console.log(billingBundleSummary.id);
}
```

## 根据 ID 获取捆绑包

根据 ID 获取单个捆绑包。

`GET /bundle_pricing/billing_bundles/{bundle_id}`

```javascript
const billingBundle = await client.bundlePricing.billingBundles.retrieve(
  '8661948c-a386-4385-837f-af00f40f111a',
);

console.log(billingBundle.data);
```

## 获取用户捆绑包

获取用户捆绑包的分页列表。

`GET /bundle_pricing/user_bundles`

```javascript
// Automatically fetches more pages as needed.
for await (const userBundle of client.bundlePricing.userBundles.list()) {
  console.log(userBundle.id);
}
```

## 创建用户捆绑包

为用户创建多个捆绑包。

`POST /bundle_pricing/user_bundles/bulk`

```javascript
const userBundle = await client.bundlePricing.userBundles.create();

console.log(userBundle.data);
```

## 获取未使用的用户捆绑包

返回所有未使用的用户捆绑包。

`GET /bundle_pricing/user_bundles/unused`

```javascript
const response = await client.bundlePricing.userBundles.listUnused();

console.log(response.data);
```

## 根据 ID 获取用户捆绑包

根据 ID 获取用户捆绑包。

`GET /bundle_pricing/user_bundles/{user_bundle_id}`

```javascript
const userBundle = await client.bundlePricing.userBundles.retrieve(
  'ca1d2263-d1f1-43ac-ba53-248e7a4bb26a',
);

console.log(userBundle.data);
```

## 取消激活用户捆绑包

根据 ID 取消激活用户捆绑包。

`DELETE /bundle_pricing/user_bundles/{user_bundle_id}`

```javascript
const response = await client.bundlePricing.userBundles.deactivate(
  'ca1d2263-d1f1-43ac-ba53-248e7a4bb26a',
);

console.log(response.data);
```

## 获取用户捆绑包的资源

根据 ID 获取用户捆绑包的资源。

`GET /bundle_pricing/user_bundles/{user_bundle_id}/resources`

```javascript
const response = await client.bundlePricing.userBundles.listResources(
  'ca1d2263-d1f1-43ac-ba53-248e7a4bb26a',
);

console.log(response.data);
```

## 列出所有文档链接

按创建时间降序列出所有文档链接。

`GET /document_links`

```javascript
// Automatically fetches more pages as needed.
for await (const documentLinkListResponse of client.documentLinks.list()) {
  console.log(documentLinkListResponse.id);
}
```

## 列出所有文档

按创建时间降序列出所有文档。

`GET /documents`

```javascript
// Automatically fetches more pages as needed.
for await (const docServiceDocument of client.documents.list()) {
  console.log(docServiceDocument.id);
}
```

## 上传文档

上传文档。<br /><br />上传的文件必须在 30 分钟内关联到某个服务，否则将被自动删除。

`POST /documents`

```javascript
const response = await client.documents.uploadJson({ document: {} });

console.log(response.data);
```

## 获取文档

获取文档。

`GET /documents/{id}`

```javascript
const document = await client.documents.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(document.data);
```

## 更新文档

更新文档。

`PATCH /documents/{id}`

```javascript
const document = await client.documents.update('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(document.data);
```

## 删除文档

删除文档。<br /><br />只有未关联到任何服务的文档才能被删除。

`DELETE /documents/{id}`

```javascript
const document = await client.documents.delete('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(document.data);
```

## 下载文档

下载文档。

`GET /documents/{id}/download`

```javascript
const response = await client.documents.download('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(response);

const content = await response.blob();
console.log(content);
```

## 生成文档的临时下载链接

生成一个临时预签名 URL，可以直接从存储后端下载文档，无需身份验证。

`GET /documents/{id}/download_link`

```javascript
const response = await client.documents.generateDownloadLink(
  '550e8400-e29b-41d4-a716-446655440000',
);

console.log(response.data);
```

## 列出所有需求

支持过滤、排序和分页功能，列出所有需求。

`GET /requirements`

```javascript
// Automatically fetches more pages as needed.
for await (const requirementListResponse of client.requirements.list()) {
  console.log(requirementListResponse.id);
}
```

## 获取文档需求

获取文档需求记录。

`GET /requirements/{id}`

```javascript
const requirement = await client.requirements.retrieve('a9dad8d5-fdbd-49d7-aa23-39bb08a5ebaa');

console.log(requirement.data);
```

## 列出所有需求类型

按创建时间降序列出所有需求类型。

`GET /requirement_types`

```javascript
const requirementTypes = await client.requirementTypes.list();

console.log(requirementTypes.data);
```

## 根据 ID 获取需求类型

根据 ID 获取需求类型。

`GET /requirement_types/{id}`

```javascript
const requirementType = await client.requirementTypes.retrieve(
  'a38c217a-8019-48f8-bff6-0fdd9939075b',
);

console.log(requirementType.data);
```

## 获取监管要求

`GET /regulatory_requirements`

```javascript
const regulatoryRequirement = await client.regulatoryRequirements.retrieve();

console.log(regulatoryRequirement.data);
```

## 列出需求组

`GET /requirement_groups`

```javascript
const requirementGroups = await client.requirementGroups.list();

console.log(requirementGroups);
```

## 创建新的需求组

`POST /requirement_groups` — 必需参数：`country_code`、`phone_number_type`、`action`

```javascript
const requirementGroup = await client.requirementGroups.create({
  action: 'ordering',
  country_code: 'US',
  phone_number_type: 'local',
});

console.log(requirementGroup.id);
```

## 根据 ID 获取单个需求组

根据 ID 获取单个需求组。

`GET /requirement_groups/{id}`

```javascript
const requirementGroup = await client.requirementGroups.retrieve('id');

console.log(requirementGroup.id);
```

## 更新需求组中的需求值

`PATCH /requirement_groups/{id}`

```javascript
const requirementGroup = await client.requirementGroups.update('id');

console.log(requirementGroup.id);
```

## 根据 ID 删除需求组

`DELETE /requirement_groups/{id}`

```javascript
const requirementGroup = await client.requirementGroups.delete('id');

console.log(requirementGroup.id);
```

## 提交需求组以供审批

`POST /requirement_groups/{id}/submit_for_approval`

```javascript
const requirementGroup = await client.requirementGroups.submitForApproval('id');

console.log(requirementGroup.id);
```

## 列出所有已验证的号码

获取已验证号码的分页列表。

`GET /verified_numbers`

```javascript
// Automatically fetches more pages as needed.
for await (const verifiedNumber of client.verifiedNumbers.list()) {
  console.log(verifiedNumber.phone_number);
}
```

## 请求电话号码验证

启动电话号码验证流程。

`POST /verified_numbers` — 必需参数：`phone_number`、`verification_method`

```javascript
const verifiedNumber = await client.verifiedNumbers.create({
  phone_number: '+15551234567',
  verification_method: 'sms',
});

console.log(verifiedNumber.phone_number);
```

## 获取已验证的号码

`GET /verified_numbers/{phone_number}`

```javascript
const verifiedNumberDataWrapper = await client.verifiedNumbers.retrieve('+15551234567');

console.log(verifiedNumberDataWrapper.data);
```

## 删除已验证的号码

`DELETE /verified_numbers/{phone_number}`

```javascript
const verifiedNumberDataWrapper = await client.verifiedNumbers.delete('+15551234567');

console.log(verifiedNumberDataWrapper.data);
```

## 提交验证码

`POST /verified_numbers/{phone_number}/actions/verify` — 必需参数：`verification_code`

```javascript
const verifiedNumberDataWrapper = await client.verifiedNumbers.actions.submitVerificationCode(
  '+15551234567',
  { verification_code: '123456' },
);

console.log(verifiedNumberDataWrapper.data);
```