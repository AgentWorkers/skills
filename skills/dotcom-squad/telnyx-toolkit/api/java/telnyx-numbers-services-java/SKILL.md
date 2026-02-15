---
name: telnyx-numbers-services-java
description: >-
  Configure voicemail, voice channels, and emergency (E911) services for your
  phone numbers. This skill provides Java SDK examples.
metadata:
  author: telnyx
  product: numbers-services
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 数字服务 - Java

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

以下所有示例均假设 `client` 已按上述方式初始化。

## 列出动态紧急地址

根据筛选条件返回动态紧急地址

`GET /dynamic_emergency_addresses`

```java
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressListPage;
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressListParams;

DynamicEmergencyAddressListPage page = client.dynamicEmergencyAddresses().list();
```

## 创建动态紧急地址

创建一个动态紧急地址。

`POST /dynamic_emergency_addresses` — 必需参数：`house_number`、`street_name`、`locality`、`administrative_area`、`postal_code`、`country_code`

```java
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddress;
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressCreateParams;
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressCreateResponse;

DynamicEmergencyAddress params = DynamicEmergencyAddress.builder()
    .administrativeArea("TX")
    .countryCode(DynamicEmergencyAddress.CountryCode.US)
    .houseNumber("600")
    .locality("Austin")
    .postalCode("78701")
    .streetName("Congress")
    .build();
DynamicEmergencyAddressCreateResponse dynamicEmergencyAddress = client.dynamicEmergencyAddresses().create(params);
```

## 获取动态紧急地址

根据提供的 ID 返回动态紧急地址

`GET /dynamic_emergency_addresses/{id}`

```java
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressRetrieveParams;
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressRetrieveResponse;

DynamicEmergencyAddressRetrieveResponse dynamicEmergencyAddress = client.dynamicEmergencyAddresses().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除动态紧急地址

根据提供的 ID 删除动态紧急地址

`DELETE /dynamic_emergency_addresses/{id}`

```java
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressDeleteParams;
import com.telnyx.sdk.models.dynamicemergencyaddresses.DynamicEmergencyAddressDeleteResponse;

DynamicEmergencyAddressDeleteResponse dynamicEmergencyAddress = client.dynamicEmergencyAddresses().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出动态紧急终端点

根据筛选条件返回动态紧急终端点

`GET /dynamic_emergency_endpoints`

```java
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointListPage;
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointListParams;

DynamicEmergencyEndpointListPage page = client.dynamicEmergencyEndpoints().list();
```

## 创建动态紧急终端点

创建一个动态紧急终端点。

`POST /dynamic_emergency_endpoints` — 必需参数：`dynamic_emergency_address_id`、`callback_number`、`caller_name`

```java
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpoint;
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointCreateParams;
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointCreateResponse;

DynamicEmergencyEndpoint params = DynamicEmergencyEndpoint.builder()
    .callbackNumber("+13125550000")
    .callerName("Jane Doe Desk Phone")
    .dynamicEmergencyAddressId("0ccc7b54-4df3-4bca-a65a-3da1ecc777f0")
    .build();
DynamicEmergencyEndpointCreateResponse dynamicEmergencyEndpoint = client.dynamicEmergencyEndpoints().create(params);
```

## 获取动态紧急终端点

根据提供的 ID 返回动态紧急终端点

`GET /dynamic_emergency_endpoints/{id}`

```java
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointRetrieveParams;
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointRetrieveResponse;

DynamicEmergencyEndpointRetrieveResponse dynamicEmergencyEndpoint = client.dynamicEmergencyEndpoints().retrieve("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 删除动态紧急终端点

根据提供的 ID 删除动态紧急终端点

`DELETE /dynamic_emergency_endpoints/{id}`

```java
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointDeleteParams;
import com.telnyx.sdk.models.dynamicemergencyendpoints.DynamicEmergencyEndpointDeleteResponse;

DynamicEmergencyEndpointDeleteResponse dynamicEmergencyEndpoint = client.dynamicEmergencyEndpoints().delete("182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e");
```

## 列出非美国区域的语音通道

列出您账户中的非美国区域语音通道。

`GET /channel_zones`

```java
import com.telnyx.sdk.models.channelzones.ChannelZoneListPage;
import com.telnyx.sdk.models.channelzones.ChannelZoneListParams;

ChannelZoneListPage page = client.channelZones().list();
```

## 更新非美国区域的语音通道

更新非美国区域的语音通道数量。

`PUT /channel_zones/{channel_zone_id}` — 必需参数：`channels`

```java
import com.telnyx.sdk.models.channelzones.ChannelZoneUpdateParams;
import com.telnyx.sdk.models.channelzones.ChannelZoneUpdateResponse;

ChannelZoneUpdateParams params = ChannelZoneUpdateParams.builder()
    .channelZoneId("channel_zone_id")
    .channels(0L)
    .build();
ChannelZoneUpdateResponse channelZone = client.channelZones().update(params);
```

## 列出美国区域的语音通道

列出您账户中的美国区域语音通道。

`GET /inbound_channels`

```java
import com.telnyx.sdk.models.inboundchannels.InboundChannelListParams;
import com.telnyx.sdk.models.inboundchannels.InboundChannelListResponse;

InboundChannelListResponse inboundChannels = client.inboundChannels().list();
```

## 更新美国区域的语音通道

更新美国区域的语音通道数量。

`PATCH /inbound_channels` — 必需参数：`channels`

```java
import com.telnyx.sdk.models.inboundchannels.InboundChannelUpdateParams;
import com.telnyx.sdk.models.inboundchannels.InboundChannelUpdateResponse;

InboundChannelUpdateParams params = InboundChannelUpdateParams.builder()
    .channels(7L)
    .build();
InboundChannelUpdateResponse inboundChannel = client.inboundChannels().update(params);
```

## 列出使用通道计费的电话号码

检索按区域分组的、使用通道计费的全部电话号码。

`GET /list`

```java
import com.telnyx.sdk.models.list.ListRetrieveAllParams;
import com.telnyx.sdk.models.list.ListRetrieveAllResponse;

ListRetrieveAllResponse response = client.list().retrieveAll();
```

## 列出特定区域的使用通道计费的电话号码

检索特定区域中使用通道计费的电话号码列表。

`GET /list/{channel_zone_id}`

```java
import com.telnyx.sdk.models.list.ListRetrieveByZoneParams;
import com.telnyx.sdk.models.list.ListRetrieveByZoneResponse;

ListRetrieveByZoneResponse response = client.list().retrieveByZone("channel_zone_id");
```

## 获取语音信箱

获取电话号码的语音信箱设置

`GET /phone_numbers/{phone_number_id}/voicemail`

```java
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailRetrieveParams;
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailRetrieveResponse;

VoicemailRetrieveResponse voicemail = client.phoneNumbers().voicemail().retrieve("123455678900");
```

## 创建语音信箱

为电话号码创建语音信箱设置

`POST /phone_numbers/{phone_number_id}/voicemail`

```java
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailCreateParams;
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailCreateResponse;
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailRequest;

VoicemailCreateParams params = VoicemailCreateParams.builder()
    .phoneNumberId("123455678900")
    .voicemailRequest(VoicemailRequest.builder().build())
    .build();
VoicemailCreateResponse voicemail = client.phoneNumbers().voicemail().create(params);
```

## 更新语音信箱

更新电话号码的语音信箱设置

`PATCH /phone_numbers/{phone_number_id}/voicemail`

```java
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailRequest;
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailUpdateParams;
import com.telnyx.sdk.models.phonenumbers.voicemail.VoicemailUpdateResponse;

VoicemailUpdateParams params = VoicemailUpdateParams.builder()
    .phoneNumberId("123455678900")
    .voicemailRequest(VoicemailRequest.builder().build())
    .build();
VoicemailUpdateResponse voicemail = client.phoneNumbers().voicemail().update(params);
```