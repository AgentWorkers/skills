---
name: telnyx-numbers-compliance-python
description: >-
  Manage regulatory requirements, number bundles, supporting documents, and
  verified numbers for compliance. This skill provides Python SDK examples.
metadata:
  author: telnyx
  product: numbers-compliance
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字合规性 - Python

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

以下所有示例均假设 `client` 已按照上述方式初始化。

## 获取捆绑包

获取所有允许使用的捆绑包。

`GET /bundle_pricing/billing_bundles`

```python
page = client.bundle_pricing.billing_bundles.list()
page = page.data[0]
print(page.id)
```

## 根据 ID 获取捆绑包

根据 ID 获取单个捆绑包。

`GET /bundle_pricing/billing_bundles/{bundle_id}`

```python
billing_bundle = client.bundle_pricing.billing_bundles.retrieve(
    bundle_id="8661948c-a386-4385-837f-af00f40f111a",
)
print(billing_bundle.data)
```

## 获取用户捆绑包

获取用户捆绑包的分页列表。

`GET /bundle_pricing/user_bundles`

```python
page = client.bundle_pricing.user_bundles.list()
page = page.data[0]
print(page.id)
```

## 创建用户捆绑包

为用户创建多个捆绑包。

`POST /bundle_pricing/user_bundles/bulk`

```python
user_bundle = client.bundle_pricing.user_bundles.create()
print(user_bundle.data)
```

## 获取未使用的用户捆绑包

返回所有未使用的用户捆绑包。

`GET /bundle_pricing/user_bundles/unused`

```python
response = client.bundle_pricing.user_bundles.list_unused()
print(response.data)
```

## 根据 ID 获取用户捆绑包

根据 ID 获取用户捆绑包。

`GET /bundle_pricing/user_bundles/{user_bundle_id}`

```python
user_bundle = client.bundle_pricing.user_bundles.retrieve(
    user_bundle_id="ca1d2263-d1f1-43ac-ba53-248e7a4bb26a",
)
print(user_bundle.data)
```

## 取消激活用户捆绑包

根据 ID 取消激活用户捆绑包。

`DELETE /bundle_pricing/user_bundles/{user_bundle_id}`

```python
response = client.bundle_pricing.user_bundles.deactivate(
    user_bundle_id="ca1d2263-d1f1-43ac-ba53-248e7a4bb26a",
)
print(response.data)
```

## 获取用户捆绑包的资源

根据 ID 获取用户捆绑包的资源。

`GET /bundle_pricing/user_bundles/{user_bundle_id}/resources`

```python
response = client.bundle_pricing.user_bundles.list_resources(
    user_bundle_id="ca1d2263-d1f1-43ac-ba53-248e7a4bb26a",
)
print(response.data)
```

## 列出所有文档链接

按创建时间降序列出所有文档链接。

`GET /document_links`

```python
page = client.document_links.list()
page = page.data[0]
print(page.id)
```

## 列出所有文档

按创建时间降序列出所有文档。

`GET /documents`

```python
page = client.documents.list()
page = page.data[0]
print(page.id)
```

## 上传文档

上传文档。<br /><br />上传的文件必须在 30 分钟内关联到某个服务，否则将被自动删除。

`POST /documents`

```python
response = client.documents.upload_json(
    document={},
)
print(response.data)
```

## 获取文档

获取文档。

`GET /documents/{id}`

```python
document = client.documents.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(document.data)
```

## 更新文档

更新文档。

`PATCH /documents/{id}`

```python
document = client.documents.update(
    document_id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(document.data)
```

## 删除文档

删除文档。<br /><br />只有未关联到任何服务的文档才能被删除。

`DELETE /documents/{id}`

```python
document = client.documents.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(document.data)
```

## 下载文档

下载文档。

`GET /documents/{id}/download`

```python
response = client.documents.download(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(response)
content = response.read()
print(content)
```

## 生成文档的临时下载链接

生成一个临时预签名 URL，可以直接从存储后端下载文档，无需认证。

`GET /documents/{id}/download_link`

```python
response = client.documents.generate_download_link(
    "550e8400-e29b-41d4-a716-446655440000",
)
print(response.data)
```

## 列出所有需求

支持过滤、排序和分页功能，列出所有需求。

`GET /requirements`

```python
page = client.requirements.list()
page = page.data[0]
print(page.id)
```

## 获取文档需求记录

获取文档需求记录。

`GET /requirements/{id}`

```python
requirement = client.requirements.retrieve(
    "a9dad8d5-fdbd-49d7-aa23-39bb08a5ebaa",
)
print(requirement.data)
```

## 列出所有需求类型

按创建时间降序列出所有需求类型。

`GET /requirement_types`

```python
requirement_types = client.requirement_types.list()
print(requirement_types.data)
```

## 根据 ID 获取需求类型

根据 ID 获取需求类型。

`GET /requirement_types/{id}`

```python
requirement_type = client.requirement_types.retrieve(
    "a38c217a-8019-48f8-bff6-0fdd9939075b",
)
print(requirement_type.data)
```

## 获取监管要求

`GET /regulatory_requirements`

```python
regulatory_requirement = client.regulatory_requirements.retrieve()
print(regulatory_requirement.data)
```

## 列出需求组

`GET /requirement_groups`

```python
requirement_groups = client.requirement_groups.list()
print(requirement_groups)
```

## 创建新的需求组

`POST /requirement_groups` — 必需参数：`country_code`、`phone_number_type`、`action`

```python
requirement_group = client.requirement_groups.create(
    action="ordering",
    country_code="US",
    phone_number_type="local",
)
print(requirement_group.id)
```

## 根据 ID 获取单个需求组

根据 ID 获取单个需求组。

`GET /requirement_groups/{id}`

```python
requirement_group = client.requirement_groups.retrieve(
    "id",
)
print(requirement_group.id)
```

## 更新需求组中的需求值

`PATCH /requirement_groups/{id}`

```python
requirement_group = client.requirement_groups.update(
    id="id",
)
print(requirement_group.id)
```

## 根据 ID 删除需求组

`DELETE /requirement_groups/{id}`

```python
requirement_group = client.requirement_groups.delete(
    "id",
)
print(requirement_group.id)
```

## 提交需求组以供审批

`POST /requirement_groups/{id}/submit_for_approval`

```python
requirement_group = client.requirement_groups.submit_for_approval(
    "id",
)
print(requirement_group.id)
```

## 列出所有已验证的号码

获取已验证号码的分页列表。

`GET /verified_numbers`

```python
page = client.verified_numbers.list()
page = page.data[0]
print(page.phone_number)
```

## 请求电话号码验证

启动电话号码验证流程。

`POST /verified_numbers` — 必需参数：`phone_number`、`verification_method`

```python
verified_number = client.verified_numbers.create(
    phone_number="+15551234567",
    verification_method="sms",
)
print(verified_number.phone_number)
```

## 获取已验证的号码

`GET /verified_numbers/{phone_number}`

```python
verified_number_data_wrapper = client.verified_numbers.retrieve(
    "+15551234567",
)
print(verified_number_data_wrapper.data)
```

## 删除已验证的号码

`DELETE /verified_numbers/{phone_number}`

```python
verified_number_data_wrapper = client.verified_numbers.delete(
    "+15551234567",
)
print(verified_number_data_wrapper.data)
```

## 提交验证码

`POST /verified_numbers/{phone_number}/actions/verify` — 必需参数：`verification_code`

```python
verified_number_data_wrapper = client.verified_numbers.actions.submit_verification_code(
    phone_number="+15551234567",
    verification_code="123456",
)
print(verified_number_data_wrapper.data)
```