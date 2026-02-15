---
name: telnyx-sip-javascript
description: >-
  Configure SIP trunking connections and outbound voice profiles. Use when
  connecting PBX systems or managing SIP infrastructure. This skill provides
  JavaScript SDK examples.
metadata:
  author: telnyx
  product: sip
  language: javascript
  generated_by: telnyx-ext-skills-generator
---

```markdown
<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip - JavaScript

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 获取所有出站语音配置文件

获取属于用户的、符合给定过滤条件的所有出站语音配置文件。

`GET /outbound_voice_profiles`

```javascript
// Automatically fetches more pages as needed.
for await (const outboundVoiceProfile of client.outboundVoiceProfiles.list()) {
  console.log(outboundVoiceProfile.id);
}
```

## 创建出站语音配置文件

创建一个新的出站语音配置文件。

`POST /outbound_voice_profiles` — 必需参数：`name`

```javascript
const outboundVoiceProfile = await client.outboundVoiceProfiles.create({ name: 'office' });

console.log(outboundVoiceProfile.data);
```

## 查询出站语音配置文件

查询现有出站语音配置文件的详细信息。

`GET /outbound_voice_profiles/{id}`

```javascript
const outboundVoiceProfile = await client.outboundVoiceProfiles.retrieve('1293384261075731499');

console.log(outboundVoiceProfile.data);
```

## 更新出站语音配置文件

更新现有出站语音配置文件的详细信息。

`PATCH /outbound_voice_profiles/{id}` — 必需参数：`name`

```javascript
const outboundVoiceProfile = await client.outboundVoiceProfiles.update('1293384261075731499', {
  name: 'office',
});

console.log(outboundVoiceProfile.data);
```

## 删除出站语音配置文件

删除现有的出站语音配置文件。

`DELETE /outbound_voice_profiles/{id}`

```javascript
const outboundVoiceProfile = await client.outboundVoiceProfiles.delete('1293384261075731499');

console.log(outboundVoiceProfile.data);
```

## 列出所有连接

返回所有类型的连接列表。

`GET /connections`

```javascript
// Automatically fetches more pages as needed.
for await (const connectionListResponse of client.connections.list()) {
  console.log(connectionListResponse.id);
}
```

## 查询连接信息

查询现有连接的详细信息。

`GET /connections/{id}`

```javascript
const connection = await client.connections.retrieve('id');

console.log(connection.data);
```

## 列出凭证连接

返回所有凭证连接的列表。

`GET /credential_connections`

```javascript
// Automatically fetches more pages as needed.
for await (const credentialConnection of client.credentialConnections.list()) {
  console.log(credentialConnection.id);
}
```

## 创建凭证连接

创建一个新的凭证连接。

`POST /credential_connections` — 必需参数：`user_name`, `password`, `connection_name`

```javascript
const credentialConnection = await client.credentialConnections.create({
  connection_name: 'my name',
  password: 'my123secure456password789',
  user_name: 'myusername123',
});

console.log(credentialConnection.data);
```

## 查询凭证连接信息

查询现有凭证连接的详细信息。

`GET /credential_connections/{id}`

```javascript
const credentialConnection = await client.credentialConnections.retrieve('id');

console.log(credentialConnection.data);
```

## 更新凭证连接

更新现有凭证连接的设置。

`PATCH /credential_connections/{id}`

```javascript
const credentialConnection = await client.credentialConnections.update('id');

console.log(credentialConnection.data);
```

## 删除凭证连接

删除现有的凭证连接。

`DELETE /credential_connections/{id}`

```javascript
const credentialConnection = await client.credentialConnections.delete('id');

console.log(credentialConnection.data);
```

## 检查凭证连接的注册状态

检查凭证连接的注册状态（`registration_status`）以及最后一次 SIP 注册事件的时间戳（`registration_status_updated_at`）。

`POST /credential_connections/{id}/actions/check_registration_status`

```javascript
const response = await client.credentialConnections.actions.checkRegistrationStatus('id');

console.log(response.data);
```

## 列出 IP 地址

获取属于用户的、符合给定过滤条件的所有 IP 地址。

`GET /ips`

```javascript
// Automatically fetches more pages as needed.
for await (const ip of client.ips.list()) {
  console.log(ip.id);
}
```

## 创建 IP 地址

创建一个新的 IP 对象。

`POST /ips` — 必需参数：`ip_address`

```javascript
const ip = await client.ips.create({ ip_address: '192.168.0.0' });

console.log(ip.data);
```

## 查询 IP 地址信息

返回特定 IP 地址的详细信息。

`GET /ips/{id}`

```javascript
const ip = await client.ips.retrieve('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(ip.data);
```

## 更新 IP 地址信息

更新特定 IP 地址的详细信息。

`PATCH /ips/{id}` — 必需参数：`ip_address`

```javascript
const ip = await client.ips.update('6a09cdc3-8948-47f0-aa62-74ac943d6c58', {
  ip_address: '192.168.0.0',
});

console.log(ip.data);
```

## 删除 IP 地址

删除指定的 IP 地址。

`DELETE /ips/{id}`

```javascript
const ip = await client.ips.delete('6a09cdc3-8948-47f0-aa62-74ac943d6c58');

console.log(ip.data);
```

## 列出 IP 连接

返回所有 IP 连接的列表。

`GET /ip_connections`

```javascript
// Automatically fetches more pages as needed.
for await (const ipConnection of client.ipConnections.list()) {
  console.log(ipConnection.id);
}
```

## 创建 IP 连接

创建一个新的 IP 连接。

`POST /ip_connections`

```javascript
const ipConnection = await client.ipConnections.create();

console.log(ipConnection.data);
```

## 查询 IP 连接信息

查询现有 IP 连接的详细信息。

`GET /ip_connections/{id}`

```javascript
const ipConnection = await client.ipConnections.retrieve('id');

console.log(ipConnection.data);
```

## 更新 IP 连接信息

更新现有 IP 连接的设置。

`PATCH /ip_connections/{id}`

```javascript
const ipConnection = await client.ipConnections.update('id');

console.log(ipConnection.data);
```

## 删除 IP 连接

删除现有的 IP 连接。

`DELETE /ip_connections/{id}`

```javascript
const ipConnection = await client.ipConnections.delete('id');

console.log(ipConnection.data);
```

## 列出 FQDN（Fully Qualified Domain Names）

获取属于用户的、符合给定过滤条件的所有 FQDN。

`GET /fqdns`

```javascript
// Automatically fetches more pages as needed.
for await (const fqdn of client.fqdns.list()) {
  console.log(fqdn.id);
}
```

## 创建 FQDN

创建一个新的 FQDN 对象。

`POST /fqdns` — 必需参数：`fqdn`, `dns_record_type`, `connection_id`

```javascript
const fqdn = await client.fqdns.create({
  connection_id: '1516447646313612565',
  dns_record_type: 'a',
  fqdn: 'example.com',
});

console.log(fqdn.data);
```

## 查询 FQDN 信息

返回特定 FQDN 的详细信息。

`GET /fqdns/{id}`

```javascript
const fqdn = await client.fqdns.retrieve('id');

console.log(fqdn.data);
```

## 更新 FQDN 信息

更新特定 FQDN 的详细信息。

`PATCH /fqdns/{id}`

```javascript
const fqdn = await client.fqdns.update('id');

console.log(fqdn.data);
```

## 删除 FQDN

删除指定的 FQDN。

`DELETE /fqdns/{id}`

```javascript
const fqdn = await client.fqdns.delete('id');

console.log(fqdn.data);
```

## 列出 FQDN 连接

返回所有 FQDN 连接的列表。

`GET /fqdn_connections`

```javascript
// Automatically fetches more pages as needed.
for await (const fqdnConnection of client.fqdnConnections.list()) {
  console.log(fqdnConnection.id);
}
```

## 创建 FQDN 连接

创建一个新的 FQDN 连接。

`POST /fqdn_connections` — 必需参数：`connection_name`

```javascript
const fqdnConnection = await client.fqdnConnections.create({ connection_name: 'string' });

console.log(fqdnConnection.data);
```

## 查询 FQDN 连接信息

查询现有 FQDN 连接的详细信息。

`GET /fqdn_connections/{id}`

```javascript
const fqdnConnection = await client.fqdnConnections.retrieve('id');

console.log(fqdnConnection.data);
```

## 更新 FQDN 连接信息

更新现有 FQDN 连接的设置。

`PATCH /fqdn_connections/{id}`

```javascript
const fqdnConnection = await client.fqdnConnections.update('id');

console.log(fqdnConnection.data);
```

## 删除 FQDN 连接

删除现有的 FQDN 连接。

`DELETE /fqdn_connections/{id}`

```javascript
const fqdnConnection = await client.fqdnConnections.delete('id');

console.log(fqdnConnection.data);
```

## 列出移动语音连接

获取所有移动语音连接的列表。

`GET /v2/mobile_voice_connections`

```javascript
// Automatically fetches more pages as needed.
for await (const mobileVoiceConnection of client.mobileVoiceConnections.list()) {
  console.log(mobileVoiceConnection.id);
}
```

## 创建移动语音连接

创建一个新的移动语音连接。

`POST /v2/mobile_voice_connections`

```javascript
const mobileVoiceConnection = await client.mobileVoiceConnections.create();

console.log(mobileVoiceConnection.data);
```

## 查询移动语音连接信息

查询特定移动语音连接的详细信息。

`GET /v2/mobile_voice_connections/{id}`

```javascript
const mobileVoiceConnection = await client.mobileVoiceConnections.retrieve('id');

console.log(mobileVoiceConnection.data);
```

## 更新移动语音连接

更新现有移动语音连接的设置。

`PATCH /v2/mobile_voice_connections/{id}`

```javascript
const mobileVoiceConnection = await client.mobileVoiceConnections.update('id');

console.log(mobileVoiceConnection.data);
```

## 删除移动语音连接

删除指定的移动语音连接。

`DELETE /v2/mobile_voice_connections/{id}`

```javascript
const mobileVoiceConnection = await client.mobileVoiceConnections.delete('id');

console.log(mobileVoiceConnection.data);
```
```