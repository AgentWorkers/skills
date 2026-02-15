---
name: telnyx-sip-python
description: >-
  Configure SIP trunking connections and outbound voice profiles. Use when
  connecting PBX systems or managing SIP infrastructure. This skill provides
  Python SDK examples.
metadata:
  author: telnyx
  product: sip
  language: python
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip - Python

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

## 获取所有出站语音配置文件

获取符合指定条件的用户的所有出站语音配置文件。

`GET /outbound_voice_profiles`

```python
page = client.outbound_voice_profiles.list()
page = page.data[0]
print(page.id)
```

## 创建一个出站语音配置文件

创建一个新的出站语音配置文件。

`POST /outbound_voice_profiles` — 必需参数：`name`

```python
outbound_voice_profile = client.outbound_voice_profiles.create(
    name="office",
)
print(outbound_voice_profile.data)
```

## 查询出站语音配置文件

查询现有出站语音配置文件的详细信息。

`GET /outbound_voice_profiles/{id}`

```python
outbound_voice_profile = client.outbound_voice_profiles.retrieve(
    "1293384261075731499",
)
print(outbound_voice_profile.data)
```

## 更新现有出站语音配置文件

更新现有出站语音配置文件的详细信息。

`PATCH /outbound_voice_profiles/{id}` — 必需参数：`name`

```python
outbound_voice_profile = client.outbound_voice_profiles.update(
    id="1293384261075731499",
    name="office",
)
print(outbound_voice_profile.data)
```

## 删除出站语音配置文件

删除现有的出站语音配置文件。

`DELETE /outbound_voice_profiles/{id}`

```python
outbound_voice_profile = client.outbound_voice_profiles.delete(
    "1293384261075731499",
)
print(outbound_voice_profile.data)
```

## 列出所有连接

返回所有类型的连接列表。

`GET /connections`

```python
page = client.connections.list()
page = page.data[0]
print(page.id)
```

## 查询连接信息

查询现有连接的详细信息。

`GET /connections/{id}`

```python
connection = client.connections.retrieve(
    "id",
)
print(connection.data)
```

## 列出凭证连接

返回所有凭证连接的列表。

`GET /credential_connections`

```python
page = client.credential_connections.list()
page = page.data[0]
print(page.id)
```

## 创建凭证连接

创建一个新的凭证连接。

`POST /credential_connections` — 必需参数：`user_name`、`password`、`connection_name`

```python
credential_connection = client.credential_connections.create(
    connection_name="my name",
    password="my123secure456password789",
    user_name="myusername123",
)
print(credential_connection.data)
```

## 查询凭证连接信息

查询现有凭证连接的详细信息。

`GET /credential_connections/{id}`

```python
credential_connection = client.credential_connections.retrieve(
    "id",
)
print(credential_connection.data)
```

## 更新凭证连接信息

更新现有凭证连接的设置。

`PATCH /credential_connections/{id}`

```python
credential_connection = client.credential_connections.update(
    id="id",
)
print(credential_connection.data)
```

## 删除凭证连接

删除现有的凭证连接。

`DELETE /credential_connections/{id}`

```python
credential_connection = client.credential_connections.delete(
    "id",
)
print(credential_connection.data)
```

## 检查凭证连接的注册状态

检查凭证连接的注册状态（`registration_status`）以及最后一次 SIP 注册事件的时间戳（`registration_status_updated_at`）。

`POST /credential_connections/{id}/actions/check_registration_status`

```python
response = client.credential_connections.actions.check_registration_status(
    "id",
)
print(response.data)
```

## 列出 IP 地址

获取符合指定条件的用户的所有 IP 地址。

`GET /ips`

```python
page = client.ips.list()
page = page.data[0]
print(page.id)
```

## 创建 IP 地址

创建一个新的 IP 对象。

`POST /ips` — 必需参数：`ip_address`

```python
ip = client.ips.create(
    ip_address="192.168.0.0",
)
print(ip.data)
```

## 查询 IP 地址信息

返回特定 IP 地址的详细信息。

`GET /ips/{id}`

```python
ip = client.ips.retrieve(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(ip.data)
```

## 更新 IP 地址信息

更新特定 IP 地址的详细信息。

`PATCH /ips/{id}` — 必需参数：`ip_address`

```python
ip = client.ips.update(
    id="6a09cdc3-8948-47f0-aa62-74ac943d6c58",
    ip_address="192.168.0.0",
)
print(ip.data)
```

## 删除 IP 地址

删除指定的 IP 地址。

`DELETE /ips/{id}`

```python
ip = client.ips.delete(
    "6a09cdc3-8948-47f0-aa62-74ac943d6c58",
)
print(ip.data)
```

## 列出 IP 连接

返回所有 IP 连接的列表。

`GET /ip_connections`

```python
page = client.ip_connections.list()
page = page.data[0]
print(page.id)
```

## 创建 IP 连接

创建一个新的 IP 连接。

`POST /ip_connections`

```python
ip_connection = client.ip_connections.create()
print(ip_connection.data)
```

## 查询 IP 连接信息

查询现有 IP 连接的详细信息。

`GET /ip_connections/{id}`

```python
ip_connection = client.ip_connections.retrieve(
    "id",
)
print(ip_connection.data)
```

## 更新 IP 连接信息

更新现有 IP 连接的设置。

`PATCH /ip_connections/{id}`

```python
ip_connection = client.ip_connections.update(
    id="id",
)
print(ip_connection.data)
```

## 删除 IP 连接

删除现有的 IP 连接。

`DELETE /ip_connections/{id}`

```python
ip_connection = client.ip_connections.delete(
    "id",
)
print(ip_connection.data)
```

## 列出 FQDN（完全 qualified domain names）

获取符合指定条件的用户的所有 FQDN。

`GET /fqdns`

```python
page = client.fqdns.list()
page = page.data[0]
print(page.id)
```

## 创建 FQDN

创建一个新的 FQDN 对象。

`POST /fqdns` — 必需参数：`fqdn`、`dns_record_type`、`connection_id`

```python
fqdn = client.fqdns.create(
    connection_id="1516447646313612565",
    dns_record_type="a",
    fqdn="example.com",
)
print(fqdn.data)
```

## 查询 FQDN 信息

返回特定 FQDN 的详细信息。

`GET /fqdns/{id}`

```python
fqdn = client.fqdns.retrieve(
    "id",
)
print(fqdn.data)
```

## 更新 FQDN 信息

更新特定 FQDN 的详细信息。

`PATCH /fqdns/{id}`

```python
fqdn = client.fqdns.update(
    id="id",
)
print(fqdn.data)
```

## 删除 FQDN

删除指定的 FQDN。

`DELETE /fqdns/{id}`

```python
fqdn = client.fqdns.delete(
    "id",
)
print(fqdn.data)
```

## 列出 FQDN 连接

返回所有 FQDN 连接的列表。

`GET /fqdn_connections`

```python
page = client.fqdn_connections.list()
page = page.data[0]
print(page.id)
```

## 创建 FQDN 连接

创建一个新的 FQDN 连接。

`POST /fqdn_connections` — 必需参数：`connection_name`

```python
fqdn_connection = client.fqdn_connections.create(
    connection_name="string",
)
print(fqdn_connection.data)
```

## 查询 FQDN 连接信息

查询现有 FQDN 连接的详细信息。

`GET /fqdn_connections/{id}`

```python
fqdn_connection = client.fqdn_connections.retrieve(
    "id",
)
print(fqdn_connection.data)
```

## 更新 FQDN 连接信息

更新现有 FQDN 连接的设置。

`PATCH /fqdn_connections/{id}`

```python
fqdn_connection = client.fqdn_connections.update(
    id="id",
)
print(fqdn_connection.data)
```

## 删除 FQDN 连接

删除现有的 FQDN 连接。

`DELETE /fqdn_connections/{id}`

```python
fqdn_connection = client.fqdn_connections.delete(
    "id",
)
print(fqdn_connection.data)
```

## 列出移动语音连接

获取所有移动语音连接的列表。

`GET /v2/mobile_voice_connections`

```python
page = client.mobile_voice_connections.list()
page = page.data[0]
print(page.id)
```

## 创建移动语音连接

创建一个新的移动语音连接。

`POST /v2/mobile_voice_connections`

```python
mobile_voice_connection = client.mobile_voice_connections.create()
print(mobile_voice_connection.data)
```

## 查询移动语音连接信息

查询特定移动语音连接的详细信息。

`GET /v2/mobile_voice_connections/{id}`

```python
mobile_voice_connection = client.mobile_voice_connections.retrieve(
    "id",
)
print(mobile_voice_connection.data)
```

## 更新移动语音连接信息

更新现有移动语音连接的设置。

`PATCH /v2/mobile_voice_connections/{id}`

```python
mobile_voice_connection = client.mobile_voice_connections.update(
    id="id",
)
print(mobile_voice_connection.data)
```

## 删除移动语音连接

删除现有的移动语音连接。

`DELETE /v2/mobile_voice_connections/{id}`

```python
mobile_voice_connection = client.mobile_voice_connections.delete(
    "id",
)
print(mobile_voice_connection.data)
```