---
name: telnyx-sip-java
description: >-
  Configure SIP trunking connections and outbound voice profiles. Use when
  connecting PBX systems or managing SIP infrastructure. This skill provides
  Java SDK examples.
metadata:
  author: telnyx
  product: sip
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx Sip - Java

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

## 获取所有出站语音配置文件

获取符合给定过滤条件的用户的所有出站语音配置文件。

`GET /outbound_voice_profiles`

```java
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileListPage;
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileListParams;

OutboundVoiceProfileListPage page = client.outboundVoiceProfiles().list();
```

## 创建出站语音配置文件

创建一个新的出站语音配置文件。

`POST /outbound_voice_profiles` — 必需参数：`name`

```java
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileCreateParams;
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileCreateResponse;

OutboundVoiceProfileCreateParams params = OutboundVoiceProfileCreateParams.builder()
    .name("office")
    .build();
OutboundVoiceProfileCreateResponse outboundVoiceProfile = client.outboundVoiceProfiles().create(params);
```

## 查询出站语音配置文件

查询现有出站语音配置文件的详细信息。

`GET /outbound_voice_profiles/{id}`

```java
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileRetrieveParams;
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileRetrieveResponse;

OutboundVoiceProfileRetrieveResponse outboundVoiceProfile = client.outboundVoiceProfiles().retrieve("1293384261075731499");
```

## 更新出站语音配置文件

更新现有出站语音配置文件的详细信息。

`PATCH /outbound_voice_profiles/{id}` — 必需参数：`name`

```java
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileUpdateParams;
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileUpdateResponse;

OutboundVoiceProfileUpdateParams params = OutboundVoiceProfileUpdateParams.builder()
    .id("1293384261075731499")
    .name("office")
    .build();
OutboundVoiceProfileUpdateResponse outboundVoiceProfile = client.outboundVoiceProfiles().update(params);
```

## 删除出站语音配置文件

删除现有的出站语音配置文件。

`DELETE /outbound_voice_profiles/{id}`

```java
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileDeleteParams;
import com.telnyx.sdk.models.outboundvoiceprofiles.OutboundVoiceProfileDeleteResponse;

OutboundVoiceProfileDeleteResponse outboundVoiceProfile = client.outboundVoiceProfiles().delete("1293384261075731499");
```

## 列出连接信息

返回所有类型的连接信息。

`GET /connections`

```java
import com.telnyx.sdk.models.connections.ConnectionListPage;
import com.telnyx.sdk.models.connections.ConnectionListParams;

ConnectionListPage page = client.connections().list();
```

## 查询连接信息

查询现有连接的详细信息。

`GET /connections/{id}`

```java
import com.telnyx.sdk.models.connections.ConnectionRetrieveParams;
import com.telnyx.sdk.models.connections.ConnectionRetrieveResponse;

ConnectionRetrieveResponse connection = client.connections().retrieve("id");
```

## 列出凭证连接信息

返回所有凭证连接的详细信息。

`GET /credential_connections`

```java
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionListPage;
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionListParams;

CredentialConnectionListPage page = client.credentialConnections().list();
```

## 创建凭证连接

创建一个新的凭证连接。

`POST /credential_connections` — 必需参数：`user_name`, `password`, `connection_name`

```java
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionCreateParams;
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionCreateResponse;

CredentialConnectionCreateParams params = CredentialConnectionCreateParams.builder()
    .connectionName("my name")
    .password("my123secure456password789")
    .userName("myusername123")
    .build();
CredentialConnectionCreateResponse credentialConnection = client.credentialConnections().create(params);
```

## 查询凭证连接信息

查询现有凭证连接的详细信息。

`GET /credential_connections/{id}`

```java
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionRetrieveParams;
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionRetrieveResponse;

CredentialConnectionRetrieveResponse credentialConnection = client.credentialConnections().retrieve("id");
```

## 更新凭证连接信息

更新现有凭证连接的设置。

`PATCH /credential_connections/{id}`

```java
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionUpdateParams;
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionUpdateResponse;

CredentialConnectionUpdateResponse credentialConnection = client.credentialConnections().update("id");
```

## 删除凭证连接

删除现有的凭证连接。

`DELETE /credential_connections/{id}`

```java
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionDeleteParams;
import com.telnyx.sdk.models.credentialconnections.CredentialConnectionDeleteResponse;

CredentialConnectionDeleteResponse credentialConnection = client.credentialConnections().delete("id");
```

## 检查凭证连接的注册状态

检查凭证连接的注册状态（`registration_status`）以及最后一次 SIP 注册事件的时间戳（`registration_status_updated_at`）。

`POST /credential_connections/{id}/actions/check_registration_status`

```java
import com.telnyx.sdk.models.credentialconnections.actions.ActionCheckRegistrationStatusParams;
import com.telnyx.sdk.models.credentialconnections.actions.ActionCheckRegistrationStatusResponse;

ActionCheckRegistrationStatusResponse response = client.credentialConnections().actions().checkRegistrationStatus("id");
```

## 列出 IP 地址

获取符合给定过滤条件的用户的所有 IP 地址。

`GET /ips`

```java
import com.telnyx.sdk.models.ips.IpListPage;
import com.telnyx.sdk.models.ips.IpListParams;

IpListPage page = client.ips().list();
```

## 创建 IP 地址

创建一个新的 IP 对象。

`POST /ips` — 必需参数：`ip_address`

```java
import com.telnyx.sdk.models.ips.IpCreateParams;
import com.telnyx.sdk.models.ips.IpCreateResponse;

IpCreateParams params = IpCreateParams.builder()
    .ipAddress("192.168.0.0")
    .build();
IpCreateResponse ip = client.ips().create(params);
```

## 查询 IP 地址信息

返回特定 IP 地址的详细信息。

`GET /ips/{id}`

```java
import com.telnyx.sdk.models.ips.IpRetrieveParams;
import com.telnyx.sdk.models.ips.IpRetrieveResponse;

IpRetrieveResponse ip = client.ips().retrieve("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 更新 IP 地址信息

更新特定 IP 地址的详细信息。

`PATCH /ips/{id}` — 必需参数：`ip_address`

```java
import com.telnyx.sdk.models.ips.IpUpdateParams;
import com.telnyx.sdk.models.ips.IpUpdateResponse;

IpUpdateParams params = IpUpdateParams.builder()
    .id("6a09cdc3-8948-47f0-aa62-74ac943d6c58")
    .ipAddress("192.168.0.0")
    .build();
IpUpdateResponse ip = client.ips().update(params);
```

## 删除 IP 地址

删除指定的 IP 地址。

`DELETE /ips/{id}`

```java
import com.telnyx.sdk.models.ips.IpDeleteParams;
import com.telnyx.sdk.models.ips.IpDeleteResponse;

IpDeleteResponse ip = client.ips().delete("6a09cdc3-8948-47f0-aa62-74ac943d6c58");
```

## 列出 IP 连接信息

返回所有 IP 连接的详细信息。

`GET /ip_connections`

```java
import com.telnyx.sdk.models.ipconnections.IpConnectionListPage;
import com.telnyx.sdk.models.ipconnections.IpConnectionListParams;

IpConnectionListPage page = client.ipConnections().list();
```

## 创建 IP 连接

创建一个新的 IP 连接。

`POST /ip_connections`

```java
import com.telnyx.sdk.models.ipconnections.IpConnectionCreateParams;
import com.telnyx.sdk.models.ipconnections.IpConnectionCreateResponse;

IpConnectionCreateResponse ipConnection = client.ipConnections().create();
```

## 查询 IP 连接信息

查询现有 IP 连接的详细信息。

`GET /ip_connections/{id}`

```java
import com.telnyx.sdk.models.ipconnections.IpConnectionRetrieveParams;
import com.telnyx.sdk.models.ipconnections.IpConnectionRetrieveResponse;

IpConnectionRetrieveResponse ipConnection = client.ipConnections().retrieve("id");
```

## 更新 IP 连接信息

更新现有 IP 连接的设置。

`PATCH /ip_connections/{id}`

```java
import com.telnyx.sdk.models.ipconnections.IpConnectionUpdateParams;
import com.telnyx.sdk.models.ipconnections.IpConnectionUpdateResponse;

IpConnectionUpdateResponse ipConnection = client.ipConnections().update("id");
```

## 删除 IP 连接

删除现有的 IP 连接。

`DELETE /ip_connections/{id}`

```java
import com.telnyx.sdk.models.ipconnections.IpConnectionDeleteParams;
import com.telnyx.sdk.models.ipconnections.IpConnectionDeleteResponse;

IpConnectionDeleteResponse ipConnection = client.ipConnections().delete("id");
```

## 列出 FQDN（Fully Qualified Domain Names）

获取符合给定过滤条件的用户的所有 FQDN。

`GET /fqdns`

```java
import com.telnyx.sdk.models.fqdns.FqdnListPage;
import com.telnyx.sdk.models.fqdns.FqdnListParams;

FqdnListPage page = client.fqdns().list();
```

## 创建 FQDN

创建一个新的 FQDN 对象。

`POST /fqdns` — 必需参数：`fqdn`, `dns_record_type`, `connection_id`

```java
import com.telnyx.sdk.models.fqdns.FqdnCreateParams;
import com.telnyx.sdk.models.fqdns.FqdnCreateResponse;

FqdnCreateParams params = FqdnCreateParams.builder()
    .connectionId("1516447646313612565")
    .dnsRecordType("a")
    .fqdn("example.com")
    .build();
FqdnCreateResponse fqdn = client.fqdns().create(params);
```

## 查询 FQDN 信息

返回特定 FQDN 的详细信息。

`GET /fqdns/{id}`

```java
import com.telnyx.sdk.models.fqdns.FqdnRetrieveParams;
import com.telnyx.sdk.models.fqdns.FqdnRetrieveResponse;

FqdnRetrieveResponse fqdn = client.fqdns().retrieve("id");
```

## 更新 FQDN 信息

更新特定 FQDN 的详细信息。

`PATCH /fqdns/{id}`

```java
import com.telnyx.sdk.models.fqdns.FqdnUpdateParams;
import com.telnyx.sdk.models.fqdns.FqdnUpdateResponse;

FqdnUpdateResponse fqdn = client.fqdns().update("id");
```

## 删除 FQDN

删除指定的 FQDN。

`DELETE /fqdns/{id}`

```java
import com.telnyx.sdk.models.fqdns.FqdnDeleteParams;
import com.telnyx.sdk.models.fqdns.FqdnDeleteResponse;

FqdnDeleteResponse fqdn = client.fqdns().delete("id");
```

## 列出 FQDN 连接信息

返回所有 FQDN 连接的详细信息。

`GET /fqdn_connections`

```java
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionListPage;
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionListParams;

FqdnConnectionListPage page = client.fqdnConnections().list();
```

## 创建 FQDN 连接

创建一个新的 FQDN 连接。

`POST /fqdn_connections` — 必需参数：`connection_name`

```java
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionCreateParams;
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionCreateResponse;

FqdnConnectionCreateParams params = FqdnConnectionCreateParams.builder()
    .connectionName("string")
    .build();
FqdnConnectionCreateResponse fqdnConnection = client.fqdnConnections().create(params);
```

## 查询 FQDN 连接信息

查询现有 FQDN 连接的详细信息。

`GET /fqdn_connections/{id}`

```java
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionRetrieveParams;
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionRetrieveResponse;

FqdnConnectionRetrieveResponse fqdnConnection = client.fqdnConnections().retrieve("id");
```

## 更新 FQDN 连接信息

更新现有 FQDN 连接的设置。

`PATCH /fqdn_connections/{id}`

```java
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionUpdateParams;
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionUpdateResponse;

FqdnConnectionUpdateResponse fqdnConnection = client.fqdnConnections().update("id");
```

## 删除 FQDN 连接

删除现有的 FQDN 连接。

`DELETE /fqdn_connections/{id}`

```java
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionDeleteParams;
import com.telnyx.sdk.models.fqdnconnections.FqdnConnectionDeleteResponse;

FqdnConnectionDeleteResponse fqdnConnection = client.fqdnConnections().delete("id");
```

## 列出移动语音连接信息

获取所有移动语音连接的详细信息。

`GET /v2/mobile_voice_connections`

```java
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionListPage;
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionListParams;

MobileVoiceConnectionListPage page = client.mobileVoiceConnections().list();
```

## 创建移动语音连接

创建一个新的移动语音连接。

`POST /v2/mobile_voice_connections`

```java
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionCreateParams;
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionCreateResponse;

MobileVoiceConnectionCreateResponse mobileVoiceConnection = client.mobileVoiceConnections().create();
```

## 查询移动语音连接信息

查询特定移动语音连接的详细信息。

`GET /v2/mobile_voice_connections/{id}`

```java
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionRetrieveParams;
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionRetrieveResponse;

MobileVoiceConnectionRetrieveResponse mobileVoiceConnection = client.mobileVoiceConnections().retrieve("id");
```

## 更新移动语音连接信息

更新现有移动语音连接的设置。

`PATCH /v2/mobile_voice_connections/{id}`

```java
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionUpdateParams;
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionUpdateResponse;

MobileVoiceConnectionUpdateResponse mobileVoiceConnection = client.mobileVoiceConnections().update("id");
```

## 删除移动语音连接

删除指定的移动语音连接。

`DELETE /v2/mobile_voice_connections/{id}`

```java
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionDeleteParams;
import com.telnyx.sdk.models.mobilevoiceconnections.MobileVoiceConnectionDeleteResponse;

MobileVoiceConnectionDeleteResponse mobileVoiceConnection = client.mobileVoiceConnections().delete("id");
```