---
name: telnyx-account-management-python
description: >-
  Manage sub-accounts for reseller and enterprise scenarios. This skill provides
  Python SDK examples.
metadata:
  author: telnyx
  product: account-management
  language: python
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户管理 - Python

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

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 列出当前用户管理的账户

列出当前用户管理的账户。

`GET /managed_accounts`

```python
page = client.managed_accounts.list()
page = page.data[0]
print(page.id)
```

## 创建一个新的受管理的账户

创建一个由已认证用户拥有的新受管理账户。

`POST /managed_accounts` — 必需参数：`business_name`

```python
managed_account = client.managed_accounts.create(
    business_name="Larry's Cat Food Inc",
)
print(managed_account.data)
```

## 检索受管理的账户信息

检索单个受管理账户的详细信息。

`GET /managedaccounts/{id}`

```python
managed_account = client.managed_accounts.retrieve(
    "id",
)
print(managed_account.data)
```

## 更新受管理的账户

更新单个受管理的账户。

`PATCH /managed_accounts/{id}`

```python
managed_account = client.managed_accounts.update(
    id="id",
)
print(managed_account.data)
```

## 禁用受管理的账户

禁用受管理的账户，使其无法使用 Telnyx 服务（包括发送或接收电话呼叫和短信）。

`POST /managed_accounts/{id}/actions/disable`

```python
response = client.managed_accounts.actions.disable(
    "id",
)
print(response.data)
```

## 恢复受管理的账户

启用受管理的账户及其子用户使用 Telnyx 服务。

`POST /managed_accounts/{id}/actions/enable`

```python
response = client.managed_accounts.actions.enable(
    id="id",
)
print(response.data)
```

## 更新分配给特定受管理账户的全球出站通道数量

更新分配给特定受管理账户的全球出站通道数量。

`PATCH /managed_accounts/{id}/update_global_channel_limit`

```python
response = client.managed_accounts.update_global_channel_limit(
    id="id",
)
print(response.data)
```

## 显示当前用户可用的全球出站通道信息

显示当前用户可用的全球出站通道信息。

`GET /managed_accounts/allocatable_global_outbound_channels`

```python
response = client.managed_accounts.get_allocatable_global_outbound_channels()
print(response.data)
```
```