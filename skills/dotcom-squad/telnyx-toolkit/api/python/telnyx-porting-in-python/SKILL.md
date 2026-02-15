---
name: telnyx-porting-in-python
description: >-
  Port phone numbers into Telnyx. Check portability, create port orders, upload
  LOA documents, and track porting status. This skill provides Python SDK
  examples.
metadata:
  author: telnyx
  product: porting-in
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 的端口迁移功能（Python）

## 安装

```bash
pip install telnyx
```

## 设置

```python
import os
from telnyx import Telnyx

client = Telnyx(
    api_key=os.environ.get("TELNYX_API_KEY"),  # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出所有端口迁移事件

返回所有端口迁移事件的列表。

`GET /porting/events`

```python
page = client.porting.events.list()
page = page.data[0]
print(page)
```

## 显示单个端口迁移事件

显示特定的端口迁移事件。

`GET /porting/events/{id}`

```python
event = client.porting.events.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(event.data)
```

## 重新发布端口迁移事件

重新发布特定的端口迁移事件。

`POST /porting/events/{id}/republish`

```python
client.porting.events.republish(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 预览 LOA 配置参数

无需创建 LOA 配置即可预览 LOA 模板。

`POST /porting/loa_configuration_preview`

```python
response = client.porting.loa_configurations.preview_0(
    address={
        "city": "Austin",
        "country_code": "US",
        "state": "TX",
        "street_address": "600 Congress Avenue",
        "zip_code": "78701",
    },
    company_name="Telnyx",
    contact={
        "email": "testing@telnyx.com",
        "phone_number": "+12003270001",
    },
    logo={
        "document_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
    },
    name="My LOA Configuration",
)
print(response)
content = response.read()
print(content)
```

## 列出 LOA 配置

列出所有 LOA 配置。

`GET /porting/loa_configurations`

```python
page = client.porting.loa_configurations.list()
page = page.data[0]
print(page.id)
```

## 创建 LOA 配置

创建一个新的 LOA 配置。

`POST /porting/loa_configurations`

```python
loa_configuration = client.porting.loa_configurations.create(
    address={
        "city": "Austin",
        "country_code": "US",
        "state": "TX",
        "street_address": "600 Congress Avenue",
        "zip_code": "78701",
    },
    company_name="Telnyx",
    contact={
        "email": "testing@telnyx.com",
        "phone_number": "+12003270001",
    },
    logo={
        "document_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
    },
    name="My LOA Configuration",
)
print(loa_configuration.data)
```

## 获取 LOA 配置

获取特定的 LOA 配置。

`GET /porting/loa_configurations/{id}`

```python
loa_configuration = client.porting.loa_configurations.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(loa_configuration.data)
```

## 更新 LOA 配置

更新特定的 LOA 配置。

`PATCH /porting/loa_configurations/{id}`

```python
loa_configuration = client.porting.loa_configurations.update(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    address={
        "city": "Austin",
        "country_code": "US",
        "state": "TX",
        "street_address": "600 Congress Avenue",
        "zip_code": "78701",
    },
    company_name="Telnyx",
    contact={
        "email": "testing@telnyx.com",
        "phone_number": "+12003270001",
    },
    logo={
        "document_id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e"
    },
    name="My LOA Configuration",
)
print(loa_configuration.data)
```

## 删除 LOA 配置

删除特定的 LOA 配置。

`DELETE /porting/loa_configurations/{id}`

```python
client.porting.loa_configurations.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 预览 LOA 配置

预览特定的 LOA 配置。

`GET /porting/loa_configurations/{id}/preview`

```python
response = client.porting.loa_configurations.preview_1(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response)
content = response.read()
print(content)
```

## 列出所有端口迁移订单

返回所有端口迁移订单的列表。

`GET /porting_orders`

```python
page = client.porting_orders.list()
page = page.data[0]
print(page.id)
```

## 创建端口迁移订单

创建一个新的端口迁移订单。

`POST /porting_orders` — 必需参数：`phone_numbers`

```python
porting_order = client.porting_orders.create(
    phone_numbers=["+13035550000", "+13035550001", "+13035550002"],
)
print(porting_order.data)
```

## 获取端口迁移订单详情

获取现有端口迁移订单的详细信息。

`GET /porting_orders/{id}`

```python
porting_order = client.porting_orders.retrieve(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(porting_order.data)
```

## 编辑端口迁移订单

编辑现有端口迁移订单的详细信息。

`PATCH /porting_orders/{id}`

```python
porting_order = client.porting_orders.update(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(porting_order.data)
```

## 删除端口迁移订单

删除现有的端口迁移订单。

`DELETE /porting_orders/{id}`

```python
client.porting_orders.delete(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 异步激活端口迁移订单中的每个号码

异步激活端口迁移订单中的每个号码。

`POST /porting_orders/{id}/actions/activate`

```python
response = client.porting_orders.actions.activate(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 取消端口迁移订单

取消端口迁移订单。

`POST /porting_orders/{id}/actions/cancel`

```python
response = client.porting_orders.actions.cancel(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 提交端口迁移订单

确认并提交端口迁移订单。

`POST /porting_orders/{id}/actions/confirm`

```python
response = client.porting_orders.actions.confirm(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 共享端口迁移订单

为端口迁移订单创建共享令牌。

`POST /porting_orders/{id}/actions/share`

```python
response = client.porting_orders.actions.share(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 列出所有端口迁移激活作业

返回所有端口迁移激活作业的列表。

`GET /porting_orders/{id}/activation_jobs`

```python
page = client.porting_orders.activation_jobs.list(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 获取端口迁移激活作业详情

获取特定的端口迁移激活作业的详细信息。

`GET /porting_orders/{id}/activation_jobs/{activationJobId}`

```python
activation_job = client.porting_orders.activation_jobs.retrieve(
    activation_job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(activation_job.data)
```

## 更新端口迁移激活作业

更新端口迁移激活作业的激活时间。

`PATCH /porting/orders/{id}/activation_jobs/{activationJobId}`

```python
activation_job = client.porting_orders.activation_jobs.update(
    activation_job_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(activation_job.data)
```

## 列出所有附加文档

返回端口迁移订单的所有附加文档的列表。

`GET /porting/orders/{id}/additional_documents`

```python
page = client.porting_orders.additional_documents.list(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 创建附加文档列表

为端口迁移订单创建附加文档列表。

`POST /porting/orders/{id}/additional_documents`

```python
additional_document = client.porting_orders.additional_documents.create(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(additional_document.data)
```

## 删除附加文档

删除端口迁移订单中的附加文档。

`DELETE /porting/orders/{id}/additional_documents/{additional_document_id}`

```python
client.porting_orders.additional_documents.delete(
    additional_document_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 列出允许的 FOC 日期

返回端口迁移订单允许的 FOC 日期列表。

`GET /porting/orders/{id}/allowed_foc_windows`

```python
response = client.porting_orders.retrieve_allowed_foc_windows(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 列出端口迁移订单的所有评论

返回端口迁移订单的所有评论列表。

`GET /porting/orders/{id}/comments`

```python
page = client.porting_orders.comments.list(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 为端口迁移订单创建评论

为端口迁移订单创建新的评论。

`POST /porting_orders/{id}/comments`

```python
comment = client.porting_orders.comments.create(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(comment.data)
```

## 下载端口迁移订单的 LOA 模板

下载端口迁移订单的 LOA 模板。

`GET /porting/orders/{id}/loa_template`

```python
response = client.porting_orders.retrieve_loa_template(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response)
content = response.read()
print(content)
```

## 列出端口迁移订单的需求

根据国家/号码类型返回所有需求列表。

`GET /porting/orders/{id}/requirements`

```python
page = client.porting_orders.retrieve_requirements(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.field_type)
```

## 获取关联的 V1 子请求 ID 和端口请求 ID

获取关联的 V1 子请求 ID 和端口请求 ID。

`GET /porting_orders/{id}/sub_request`

```python
response = client.porting_orders.retrieve_sub_request(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 列出验证代码

返回端口迁移订单的所有验证代码列表。

`GET /porting_orders/{id}/verification_codes`

```python
page = client.porting_orders.verification_codes.list(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 发送验证代码

为所有端口迁移号码发送验证代码。

`POST /porting_orders/{id}/verification_codes/send`

```python
client.porting_orders.verification_codes.send(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
```

## 验证一系列号码的验证代码

验证一系列号码的验证代码。

`POST /porting_orders/{id}/verification_codes/verify`

```python
response = client.porting_orders.verification_codes.verify(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(response.data)
```

## 列出端口迁移订单的动作需求

返回特定端口迁移订单的所有动作需求列表。

`GET /porting_orders/{porting_order_id}/action_requirements`

```python
page = client.porting_orders.action_requirements.list(
    porting_order_id="porting_order_id",
)
page = page.data[0]
print(page.id)
```

## 启动动作需求

为特定端口迁移订单启动特定的动作需求。

`POST /porting_orders/{porting_order_id}/action_requirements/{id}/initiate`

```python
response = client.porting_orders.action_requirements.initiate(
    id="id",
    porting_order_id="porting_order_id",
    params={
        "first_name": "John",
        "last_name": "Doe",
    },
)
print(response.data)
```

## 列出所有关联的号码

返回端口迁移订单的所有关联号码列表。

`GET /porting_orders/{id}/associated_phone_numbers`

```python
page = client.porting_orders.associated_phone_numbers.list(
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 创建关联号码

为端口迁移订单创建新的关联号码。

`POST /porting_orders/{id}/associated_phone_numbers`

```python
associated_phone_number = client.porting_orders.associated_phone_numbers.create(
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    action="keep",
    phone_number_range={},
)
print(associated_phone_number.data)
```

## 删除关联号码

从端口迁移订单中删除关联号码。

`DELETE /porting_orders/{id}/associated_phone_numbers/{id}`

```python
associated_phone_number = client.porting_orders.associated_phone_numbers.delete(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(associated_phone_number.data)
```

## 列出所有号码块

返回端口迁移订单的所有号码块列表。

`GET /porting_orders/{id}/phone_number_blocks`

```python
page = client.porting_orders.phone_number_blocks.list(
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 创建号码块

为端口迁移订单创建新的号码块。

`POST /porting_orders/{id}/phone_number_blocks`

```python
phone_number_block = client.porting_orders.phone_number_blocks.create(
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    activation_ranges=[{
        "end_at": "+4930244999910",
        "start_at": "+4930244999901",
    }],
    phone_number_range={
        "end_at": "+4930244999910",
        "start_at": "+4930244999901",
    },
)
print(phone_number_block.data)
```

## 删除号码块

删除号码块。

`DELETE /porting_orders/{id}/phone_number_blocks/{id}`

```python
phone_number_block = client.porting_orders.phone_number_blocks.delete(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(phone_number_block.data)
```

## 列出所有号码扩展名

返回端口迁移订单的所有号码扩展名列表。

`GET /porting_orders/{id}/phone_numberextensions`

```python
page = client.porting_orders.phone_number_extensions.list(
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
page = page.data[0]
print(page.id)
```

## 创建号码扩展名

为端口迁移订单创建新的号码扩展名。

`POST /porting_orders/{id}/phone_numberextensions`

```python
phone_number_extension = client.porting_orders.phone_number_extensions.create(
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    activation_ranges=[{
        "end_at": 10,
        "start_at": 1,
    }],
    extension_range={
        "end_at": 10,
        "start_at": 1,
    },
    porting_phone_number_id="f24151b6-3389-41d3-8747-7dd8c681e5e2",
)
print(phone_number_extension.data)
```

## 删除号码扩展名

删除号码扩展名。

`DELETE /porting_orders/{id}/phone_number_extensions/{id}`

```python
phone_number_extension = client.porting_orders.phone_number_extensions.delete(
    id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
    porting_order_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(phone_number_extension.data)
```

## 列出所有可能的异常类型

返回端口迁移订单的所有可能异常类型列表。

`GET /porting_orders/exception_types`

```python
response = client.porting_orders.retrieve_exception_types()
print(response.data)
```

## 列出所有号码配置

分页返回所有号码配置列表。

`GET /porting_orders/phone_number_configurations`

```python
page = client.porting_orders.phone_number_configurations.list()
page = page.data[0]
print(page.id)
```

## 创建号码配置列表

创建号码配置列表。

`POST /porting_orders/phone_number_configurations`

```python
phone_number_configuration = client.porting_orders.phone_number_configurations.create()
print(phone_number_configuration.data)
```

## 列出所有迁移中的号码

返回所有迁移中的号码列表。

`GET /porting/phone_numbers`

```python
page = client.porting_phone_numbers.list()
page = page.data[0]
print(page.porting_order_id)
```

## 列出与端口迁移相关的报告

列出与端口迁移操作相关的报告。

`GET /porting/reports`

```python
page = client.porting.reports.list()
page = page.data[0]
print(page.id)
```

## 创建与端口迁移相关的报告

生成与端口迁移操作相关的报告。

`POST /porting/reports`

```python
report = client.porting.reports.create(
    params={
        "filters": {}
    },
    report_type="export_porting_orders_csv",
)
print(report.data)
```

## 获取报告

获取特定的报告。

`GET /porting/reports/{id}`

```python
report = client.porting.reports.retrieve(
    "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
)
print(report.data)
```

## 列出英国的可用运营商

列出英国的可用运营商。

`GET /porting/uk_carriers`

```python
response = client.porting.list_uk_carriers()
print(response.data)
```

## 运行端口迁移检查

立即运行端口迁移检查并返回结果。

`POST /portability_checks`

```python
response = client.portability_checks.run()
print(response.data)
```
```