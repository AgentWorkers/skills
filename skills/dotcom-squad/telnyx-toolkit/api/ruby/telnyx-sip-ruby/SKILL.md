---
name: telnyx-sip-ruby
description: >-
  Configure SIP trunking connections and outbound voice profiles. Use when
  connecting PBX systems or managing SIP infrastructure. This skill provides
  Ruby SDK examples.
metadata:
  author: telnyx
  product: sip
  language: ruby
  generated_by: telnyx-ext-skills-generator
---

<!-- 本文档由 Telnyx OpenAPI 规范自动生成，请勿修改。 -->

# Telnyx Sip - Ruby

## 安装

```bash
gem install telnyx
```

## 设置

```ruby
require "telnyx"

client = Telnyx::Client.new(
  api_key: ENV["TELNYX_API_KEY"], # This is the default and can be omitted
)
```

以下所有示例均假设 `client` 已经按照上述方式初始化。

## 获取所有出站语音配置文件

获取符合指定条件的用户的所有出站语音配置文件。

`GET /outbound_voice_profiles`

```ruby
page = client.outbound_voice_profiles.list

puts(page)
```

## 创建出站语音配置文件

创建一个新的出站语音配置文件。

`POST /outbound_voice_profiles` — 必需参数：`name`

```ruby
outbound_voice_profile = client.outbound_voice_profiles.create(name: "office")

puts(outbound_voice_profile)
```

## 查询出站语音配置文件信息

查询现有出站语音配置文件的详细信息。

`GET /outbound_voice_profiles/{id}`

```ruby
outbound_voice_profile = client.outbound_voice_profiles.retrieve("1293384261075731499")

puts(outbound_voice_profile)
```

## 更新出站语音配置文件

更新现有出站语音配置文件的详细信息。

`PATCH /outbound_voice_profiles/{id}` — 必需参数：`name`

```ruby
outbound_voice_profile = client.outbound_voice_profiles.update("1293384261075731499", name: "office")

puts(outbound_voice_profile)
```

## 删除出站语音配置文件

删除现有的出站语音配置文件。

`DELETE /outbound_voice_profiles/{id}`

```ruby
outbound_voice_profile = client.outbound_voice_profiles.delete("1293384261075731499")

puts(outbound_voice_profile)
```

## 列出所有连接

列出用户所有的连接（无论类型如何）。

`GET /connections`

```ruby
page = client.connections.list

puts(page)
```

## 查询连接信息

查询现有连接的详细信息。

`GET /connections/{id}`

```ruby
connection = client.connections.retrieve("id")

puts(connection)
```

## 列出凭证连接

列出用户所有的凭证连接。

`GET /credential_connections`

```ruby
page = client.credential_connections.list

puts(page)
```

## 创建凭证连接

创建一个新的凭证连接。

`POST /credential_connections` — 必需参数：`user_name`, `password`, `connection_name`

```ruby
credential_connection = client.credential_connections.create(
  connection_name: "my name",
  password: "my123secure456password789",
  user_name: "myusername123"
)

puts(credential_connection)
```

## 查询凭证连接信息

查询现有凭证连接的详细信息。

`GET /credential_connections/{id}`

```ruby
credential_connection = client.credential_connections.retrieve("id")

puts(credential_connection)
```

## 更新凭证连接信息

更新现有凭证连接的设置。

`PATCH /credential_connections/{id}`

```ruby
credential_connection = client.credential_connections.update("id")

puts(credential_connection)
```

## 删除凭证连接

删除现有的凭证连接。

`DELETE /credential_connections/{id}`

```ruby
credential_connection = client.credential_connections.delete("id")

puts(credential_connection)
```

## 检查凭证连接的注册状态

检查凭证连接的注册状态（`registration_status`）以及最后一次 SIP 注册事件的时间戳（`registration_status_updated_at`）。

`POST /credential_connections/{id}/actions/check_registration_status`

```ruby
response = client.credential_connections.actions.check_registration_status("id")

puts(response)
```

## 列出 IP 地址

获取符合指定条件的用户所有的 IP 地址。

`GET /ips`

```ruby
page = client.ips.list

puts(page)
```

## 创建 IP 地址

创建一个新的 IP 地址对象。

`POST /ips` — 必需参数：`ip_address`

```ruby
ip = client.ips.create(ip_address: "192.168.0.0")

puts(ip)
```

## 查询 IP 地址信息

查询特定 IP 地址的详细信息。

`GET /ips/{id}`

```ruby
ip = client.ips.retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(ip)
```

## 更新 IP 地址信息

更新特定 IP 地址的详细信息。

`PATCH /ips/{id}` — 必需参数：`ip_address`

```ruby
ip = client.ips.update("6a09cdc3-8948-47f0-aa62-74ac943d6c58", ip_address: "192.168.0.0")

puts(ip)
```

## 删除 IP 地址

删除指定的 IP 地址。

`DELETE /ips/{id}`

```ruby
ip = client.ips.delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58")

puts(ip)
```

## 列出 IP 连接

列出用户所有的 IP 连接。

`GET /ip_connections`

```ruby
page = client.ip_connections.list

puts(page)
```

## 创建 IP 连接

创建一个新的 IP 连接。

`POST /ip_connections`

```ruby
ip_connection = client.ip_connections.create

puts(ip_connection)
```

## 查询 IP 连接信息

查询现有 IP 连接的详细信息。

`GET /ip_connections/{id}`

```ruby
ip_connection = client.ip_connections.retrieve("id")

puts(ip_connection)
```

## 更新 IP 连接信息

更新现有 IP 连接的设置。

`PATCH /ip_connections/{id}`

```ruby
ip_connection = client.ip_connections.update("id")

puts(ip_connection)
```

## 删除 IP 连接

删除现有的 IP 连接。

`DELETE /ip_connections/{id}`

```ruby
ip_connection = client.ip_connections.delete("id")

puts(ip_connection)
```

## 列出 FQDN（Fully Qualified Domain Names）

获取符合指定条件的用户所有的 FQDN。

`GET /fqdns`

```ruby
page = client.fqdns.list

puts(page)
```

## 创建 FQDN

创建一个新的 FQDN 对象。

`POST /fqdns` — 必需参数：`fqdn`, `dns_record_type`, `connection_id`

```ruby
fqdn = client.fqdns.create(connection_id: "1516447646313612565", dns_record_type: "a", fqdn: "example.com")

puts(fqdn)
```

## 查询 FQDN 信息

查询特定 FQDN 的详细信息。

`GET /fqdns/{id}`

```ruby
fqdn = client.fqdns.retrieve("id")

puts(fqdn)
```

## 更新 FQDN 信息

更新特定 FQDN 的详细信息。

`PATCH /fqdns/{id}`

```ruby
fqdn = client.fqdns.update("id")

puts(fqdn)
```

## 删除 FQDN

删除指定的 FQDN。

`DELETE /fqdns/{id}`

```ruby
fqdn = client.fqdns.delete("id")

puts(fqdn)
```

## 列出 FQDN 连接

列出用户所有的 FQDN 连接。

`GET /fqdn_connections`

```ruby
page = client.fqdn_connections.list

puts(page)
```

## 创建 FQDN 连接

创建一个新的 FQDN 连接。

`POST /fqdn_connections` — 必需参数：`connection_name`

```ruby
fqdn_connection = client.fqdn_connections.create(connection_name: "string")

puts(fqdn_connection)
```

## 查询 FQDN 连接信息

查询现有 FQDN 连接的详细信息。

`GET /fqdn_connections/{id}`

```ruby
fqdn_connection = client.fqdn_connections.retrieve("id")

puts(fqdn_connection)
```

## 更新 FQDN 连接信息

更新现有 FQDN 连接的设置。

`PATCH /fqdn_connections/{id}`

```ruby
fqdn_connection = client.fqdn_connections.update("id")

puts(fqdn_connection)
```

## 删除 FQDN 连接

删除现有的 FQDN 连接。

`DELETE /fqdn_connections/{id}`

```ruby
fqdn_connection = client.fqdn_connections.delete("id")

puts(fqdn_connection)
```

## 列出移动语音连接

列出用户所有的移动语音连接。

`GET /v2/mobile_voice_connections`

```ruby
page = client.mobile_voice_connections.list

puts(page)
```

## 创建移动语音连接

创建一个新的移动语音连接。

`POST /v2/mobile_voice_connections`

```ruby
mobile_voice_connection = client.mobile_voice_connections.create

puts(mobile_voice_connection)
```

## 查询移动语音连接信息

查询特定移动语音连接的详细信息。

`GET /v2/mobile_voice_connections/{id}`

```ruby
mobile_voice_connection = client.mobile_voice_connections.retrieve("id")

puts(mobile_voice_connection)
```

## 更新移动语音连接信息

更新现有移动语音连接的设置。

`PATCH /v2/mobile_voice_connections/{id}`

```ruby
mobile_voice_connection = client.mobile_voice_connections.update("id")

puts(mobile_voice_connection)
```

## 删除移动语音连接

删除现有的移动语音连接。

`DELETE /v2/mobile_voice_connections/{id}`

```ruby
mobile_voice_connection = client.mobile_voice_connections.delete("id")

puts(mobile_voice_connection)
```