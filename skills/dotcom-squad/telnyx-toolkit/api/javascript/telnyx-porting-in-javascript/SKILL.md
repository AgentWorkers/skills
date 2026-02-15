---
name: telnyx-porting-in-javascript
description: >-
  Port phone numbers into Telnyx. Check portability, create port orders, upload
  LOA documents, and track porting status. This skill provides JavaScript SDK
  examples.
metadata:
  author: telnyx
  product: porting-in
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 的端口迁移功能 - JavaScript

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

## 列出所有端口迁移事件

返回所有端口迁移事件的列表。

`GET /porting/events`

```javascript
// Automatically fetches more pages as needed.
for await (const eventListResponse of client.porting.events.list()) {
  console.log(eventListResponse);
}
```

## 显示特定端口迁移事件

显示特定的端口迁移事件。

`GET /porting/events/{id}`

```javascript
const event = await client.porting.events.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(event.data);
```

## 重新发布端口迁移事件

重新发布特定的端口迁移事件。

`POST /porting/events/{id}/republish`

```javascript
await client.porting.events.republish('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 预览 LOA 配置参数

预览生成的 LOA 模板，无需创建 LOA 配置。

`POST /porting/loa_configuration_preview`

```javascript
const response = await client.porting.loaConfigurations.preview0({
  address: {
    city: 'Austin',
    country_code: 'US',
    state: 'TX',
    street_address: '600 Congress Avenue',
    zip_code: '78701',
  },
  company_name: 'Telnyx',
  contact: { email: 'testing@telnyx.com', phone_number: '+12003270001' },
  logo: { document_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
  name: 'My LOA Configuration',
});

console.log(response);

const content = await response.blob();
console.log(content);
```

## 列出 LOA 配置

列出所有 LOA 配置。

`GET /porting/loa_configurations`

```javascript
// Automatically fetches more pages as needed.
for await (const portingLoaConfiguration of client.porting.loaConfigurations.list()) {
  console.log(portingLoaConfiguration.id);
}
```

## 创建 LOA 配置

创建一个新的 LOA 配置。

`POST /porting/loa_configurations`

```javascript
const loaConfiguration = await client.porting.loaConfigurations.create({
  address: {
    city: 'Austin',
    country_code: 'US',
    state: 'TX',
    street_address: '600 Congress Avenue',
    zip_code: '78701',
  },
  company_name: 'Telnyx',
  contact: { email: 'testing@telnyx.com', phone_number: '+12003270001' },
  logo: { document_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
  name: 'My LOA Configuration',
});

console.log(loaConfiguration.data);
```

## 获取 LOA 配置

获取特定的 LOA 配置。

`GET /porting/loa_configurations/{id}`

```javascript
const loaConfiguration = await client.porting.loaConfigurations.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(loaConfiguration.data);
```

## 更新 LOA 配置

更新特定的 LOA 配置。

`PATCH /porting/loa_configurations/{id}`

```javascript
const loaConfiguration = await client.porting.loaConfigurations.update(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  {
    address: {
      city: 'Austin',
      country_code: 'US',
      state: 'TX',
      street_address: '600 Congress Avenue',
      zip_code: '78701',
    },
    company_name: 'Telnyx',
    contact: { email: 'testing@telnyx.com', phone_number: '+12003270001' },
    logo: { document_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
    name: 'My LOA Configuration',
  },
);

console.log(loaConfiguration.data);
```

## 删除 LOA 配置

删除特定的 LOA 配置。

`DELETE /porting/loa_configurations/{id}`

```javascript
await client.porting.loaConfigurations.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 预览 LOA 配置

预览特定的 LOA 配置。

`GET /porting/loa_configurations/{id}/preview`

```javascript
const response = await client.porting.loaConfigurations.preview1(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response);

const content = await response.blob();
console.log(content);
```

## 列出所有端口迁移订单

返回所有端口迁移订单的列表。

`GET /porting_orders`

```javascript
// Automatically fetches more pages as needed.
for await (const portingOrder of client.portingOrders.list()) {
  console.log(portingOrder.id);
}
```

## 创建端口迁移订单

创建一个新的端口迁移订单对象。

`POST /porting_orders` — 必需参数：`phone_numbers`

```javascript
const portingOrder = await client.portingOrders.create({
  phone_numbers: ['+13035550000', '+13035550001', '+13035550002'],
});

console.log(portingOrder.data);
```

## 获取端口迁移订单详情

获取现有端口迁移订单的详细信息。

`GET /porting_orders/{id}`

```javascript
const portingOrder = await client.portingOrders.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(portingOrder.data);
```

## 编辑端口迁移订单

编辑现有端口迁移订单的详细信息。

`PATCH /porting_orders/{id}`

```javascript
const portingOrder = await client.portingOrders.update('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(portingOrder.data);
```

## 删除端口迁移订单

删除现有的端口迁移订单。

`DELETE /porting_orders/{id}`

```javascript
await client.portingOrders.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 异步激活端口迁移订单中的每个号码

异步激活端口迁移订单中的每个号码。

`POST /porting_orders/{id}/actions/activate`

```javascript
const response = await client.portingOrders.actions.activate(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response.data);
```

## 取消端口迁移订单

`POST /porting_orders/{id}/actions/cancel`

```javascript
const response = await client.portingOrders.actions.cancel('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(response.data);
```

## 提交端口迁移订单

确认并提交端口迁移订单。

`POST /porting_orders/{id}/actions/confirm`

```javascript
const response = await client.portingOrders.actions.confirm('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(response.data);
```

## 共享端口迁移订单

为端口迁移订单创建共享令牌。

`POST /porting/orders/{id}/actions/share`

```javascript
const response = await client.portingOrders.actions.share('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(response.data);
```

## 列出所有端口迁移激活任务

返回所有端口迁移激活任务的列表。

`GET /porting/orders/{id}/activation_jobs`

```javascript
// Automatically fetches more pages as needed.
for await (const portingOrdersActivationJob of client.portingOrders.activationJobs.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(portingOrdersActivationJob.id);
}
```

## 获取端口迁移激活任务详情

获取特定的端口迁移激活任务的详细信息。

`GET /porting/orders/{id}/activation_jobs/{activationJobId}`

```javascript
const activationJob = await client.portingOrders.activationJobs.retrieve(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);

console.log(activationJob.data);
```

## 更新端口迁移激活任务

更新端口迁移激活任务的激活时间。

`PATCH /porting/orders/{id}/activation_jobs/{activationJobId}`

```javascript
const activationJob = await client.portingOrders.activationJobs.update(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);

console.log(activationJob.data);
```

## 列出附加文档

返回端口迁移订单的所有附加文档的列表。

`GET /porting/orders/{id}/additional_documents`

```javascript
// Automatically fetches more pages as needed.
for await (const additionalDocumentListResponse of client.portingOrders.additionalDocuments.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(additionalDocumentListResponse.id);
}
```

## 创建附加文档列表

为端口迁移订单创建附加文档的列表。

`POST /porting/orders/{id}/additional_documents`

```javascript
const additionalDocument = await client.portingOrders.additionalDocuments.create(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(additionalDocument.data);
```

## 删除附加文档

删除端口迁移订单中的附加文档。

`DELETE /porting/orders/{id}/additional_documents/{additional_document_id}`

```javascript
await client.portingOrders.additionalDocuments.delete('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e', {
  id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
});
```

## 列出允许的 FOC 日期

返回端口迁移订单允许的 FOC 日期列表。

`GET /porting/orders/{id}/allowed_foc_windows`

```javascript
const response = await client.portingOrders.retrieveAllowedFocWindows(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response.data);
```

## 列出端口迁移订单的所有评论

返回端口迁移订单的所有评论列表。

`GET /porting/orders/{id}/comments`

```javascript
// Automatically fetches more pages as needed.
for await (const commentListResponse of client.portingOrders.comments.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(commentListResponse.id);
}
```

## 为端口迁移订单创建评论

为端口迁移订单创建新的评论。

`POST /porting/orders/{id}/comments`

```javascript
const comment = await client.portingOrders.comments.create('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(comment.data);
```

## 下载端口迁移订单的 LOA 模板

`GET /porting/orders/{id}/loa_template`

```javascript
const response = await client.portingOrders.retrieveLoaTemplate(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response);

const content = await response.blob();
console.log(content);
```

## 列出端口迁移订单的要求

根据国家/号码类型，返回该端口迁移订单的所有要求列表。

`GET /porting/orders/{id}/requirements`

```javascript
// Automatically fetches more pages as needed.
for await (const portingOrderRetrieveRequirementsResponse of client.portingOrders.retrieveRequirements(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(portingOrderRetrieveRequirementsResponse.field_type);
}
```

## 获取关联的 V1 子请求 ID 和端口请求 ID

`GET /porting/orders/{id}/sub_request`

```javascript
const response = await client.portingOrders.retrieveSubRequest(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response.data);
```

## 列出验证代码

返回端口迁移订单的所有验证代码列表。

`GET /porting/orders/{id}/verification_codes`

```javascript
// Automatically fetches more pages as needed.
for await (const verificationCodeListResponse of client.portingOrders.verificationCodes.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(verificationCodeListResponse.id);
}
```

## 发送验证代码

为所有端口迁移号码发送验证代码。

`POST /porting/orders/{id}/verification_codes/send`

```javascript
await client.portingOrders.verificationCodes.send('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');
```

## 验证一系列号码的验证代码

验证一系列号码的验证代码。

`POST /porting/orders/{id}/verification_codes/verify`

```javascript
const response = await client.portingOrders.verificationCodes.verify(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
);

console.log(response.data);
```

## 列出端口迁移订单的动作要求

返回特定端口迁移订单的所有动作要求列表。

`GET /porting_orders/{porting_order_id}/action_requirements`

```javascript
// Automatically fetches more pages as needed.
for await (const actionRequirementListResponse of client.portingOrders.actionRequirements.list(
  'porting_order_id',
)) {
  console.log(actionRequirementListResponse.id);
}
```

## 启动动作要求

为特定端口迁移订单启动特定的动作要求。

`POST /porting_orders/{id}/action_requirements/{id}/initiate`

```javascript
const response = await client.portingOrders.actionRequirements.initiate('id', {
  porting_order_id: 'porting_order_id',
  params: { first_name: 'John', last_name: 'Doe' },
});

console.log(response.data);
```

## 列出所有关联的号码

返回端口迁移订单的所有关联号码列表。

`GET /porting_orders/{id}/associated_phone_numbers`

```javascript
// Automatically fetches more pages as needed.
for await (const portingAssociatedPhoneNumber of client.portingOrders.associatedPhoneNumbers.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(portingAssociatedPhoneNumber.id);
}
```

## 创建关联号码

为端口迁移订单创建新的关联号码。

`POST /porting_orders/{id}/associated_phone_numbers`

```javascript
const associatedPhoneNumber = await client.portingOrders.associatedPhoneNumbers.create(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  {
    action: 'keep',
    phone_number_range: {},
  },
);

console.log(associatedPhoneNumber.data);
```

## 删除关联号码

从端口迁移订单中删除关联号码。

`DELETE /porting_orders/{id}/associated_phone_numbers/{id}`

```javascript
const associatedPhoneNumber = await client.portingOrders.associatedPhoneNumbers.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { porting_order_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);

console.log(associatedPhoneNumber.data);
```

## 列出所有号码块

返回端口迁移订单的所有号码块列表。

`GET /porting_orders/{id}/phone_number_blocks`

```javascript
// Automatically fetches more pages as needed.
for await (const portingPhoneNumberBlock of client.portingOrders.phoneNumberBlocks.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(portingPhoneNumberBlock.id);
}
```

## 创建号码块

为端口迁移订单创建新的号码块。

`POST /porting_orders/{id}/phone_number_blocks`

```javascript
const phoneNumberBlock = await client.portingOrders.phoneNumberBlocks.create(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  {
    activation_ranges: [{ end_at: '+4930244999910', start_at: '+4930244999901' }],
    phone_number_range: { end_at: '+4930244999910', start_at: '+4930244999901' },
  },
);

console.log(phoneNumberBlock.data);
```

## 删除号码块

删除号码块。

`DELETE /porting_orders/{id}/phone_number_blocks/{id}`

```javascript
const phoneNumberBlock = await client.portingOrders.phoneNumberBlocks.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { porting_order_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);

console.log(phoneNumberBlock.data);
```

## 列出所有号码扩展

返回端口迁移订单的所有号码扩展列表。

`GET /porting_orders/{id}/phone_number_extensions`

```javascript
// Automatically fetches more pages as needed.
for await (const portingPhoneNumberExtension of client.portingOrders.phoneNumberExtensions.list(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
)) {
  console.log(portingPhoneNumberExtension.id);
}
```

## 创建号码扩展

为端口迁移订单创建新的号码扩展。

`POST /porting_orders/{id}/phone_numberextensions`

```javascript
const phoneNumberExtension = await client.portingOrders.phoneNumberExtensions.create(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  {
    activation_ranges: [{ end_at: 10, start_at: 1 }],
    extension_range: { end_at: 10, start_at: 1 },
    porting_phone_number_id: 'f24151b6-3389-41d3-8747-7dd8c681e5e2',
  },
);

console.log(phoneNumberExtension.data);
```

## 删除号码扩展

删除号码扩展。

`DELETE /porting_orders/{id}/phone_number_extensions/{id}`

```javascript
const phoneNumberExtension = await client.portingOrders.phoneNumberExtensions.delete(
  '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e',
  { porting_order_id: '182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e' },
);

console.log(phoneNumberExtension.data);
```

## 列出所有可能的异常类型

返回端口迁移订单的所有可能异常类型列表。

`GET /porting_orders/exception_types`

```javascript
const response = await client.portingOrders.retrieveExceptionTypes();

console.log(response.data);
```

## 列出所有号码配置

分页显示端口迁移订单的所有号码配置。

`GET /porting_orders/phone_number_configurations`

```javascript
// Automatically fetches more pages as needed.
for await (const phoneNumberConfigurationListResponse of client.portingOrders.phoneNumberConfigurations.list()) {
  console.log(phoneNumberConfigurationListResponse.id);
}
```

## 创建号码配置列表

创建号码配置的列表。

`POST /porting/orders/phone_number_configurations`

```javascript
const phoneNumberConfiguration = await client.portingOrders.phoneNumberConfigurations.create();

console.log(phoneNumberConfiguration.data);
```

## 列出所有迁移的号码

返回所有迁移的号码列表。

`GET /porting/phone_numbers`

```javascript
// Automatically fetches more pages as needed.
for await (const portingPhoneNumberListResponse of client.portingPhoneNumbers.list()) {
  console.log(portingPhoneNumberListResponse.porting_order_id);
}
```

## 列出与端口迁移相关的报告

列出关于端口迁移操作的报告。

`GET /porting/reports`

```javascript
// Automatically fetches more pages as needed.
for await (const portingReport of client.porting.reports.list()) {
  console.log(portingReport.id);
}
```

## 创建与端口迁移相关的报告

生成关于端口迁移操作的报告。

`POST /porting/reports`

```javascript
const report = await client.porting.reports.create({
  params: { filters: {} },
  report_type: 'export_porting_orders_csv',
});

console.log(report.data);
```

## 获取报告

获取特定的报告。

`GET /porting/reports/{id}`

```javascript
const report = await client.porting.reports.retrieve('182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e');

console.log(report.data);
```

## 列出英国的可用运营商

列出英国的可用运营商。

`GET /porting/uk_carriers`

```javascript
const response = await client.porting.listUkCarriers();

console.log(response.data);
```

## 运行端口迁移检查

运行端口迁移检查，并立即返回结果。

`POST /portability_checks`

```javascript
const response = await client.portabilityChecks.run();

console.log(response.data);
```
```