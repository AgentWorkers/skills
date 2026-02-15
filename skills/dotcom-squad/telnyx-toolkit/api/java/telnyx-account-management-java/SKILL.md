---
name: telnyx-account-management-java
description: >-
  Manage sub-accounts for reseller and enterprise scenarios. This skill provides
  Java SDK examples.
metadata:
  author: telnyx
  product: account-management
  language: java
  generated_by: telnyx-ext-skills-generator
---

<!-- 由 Telnyx OpenAPI 规范自动生成，请勿编辑。 -->

# Telnyx 账户管理 - Java

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

## 列出当前用户管理的账户

列出当前用户管理的账户。

`GET /managed_accounts`

```java
import com.telnyx.sdk.models.managedaccounts.ManagedAccountListPage;
import com.telnyx.sdk.models.managedaccounts.ManagedAccountListParams;

ManagedAccountListPage page = client.managedAccounts().list();
```

## 创建一个新的受管理的账户

创建一个由已认证用户拥有的新受管理账户。

`POST /managed_accounts` — 必需参数：`business_name`

```java
import com.telnyx.sdk.models.managedaccounts.ManagedAccountCreateParams;
import com.telnyx.sdk.models.managedaccounts.ManagedAccountCreateResponse;

ManagedAccountCreateParams params = ManagedAccountCreateParams.builder()
    .businessName("Larry's Cat Food Inc")
    .build();
ManagedAccountCreateResponse managedAccount = client.managedAccounts().create(params);
```

## 获取受管理的账户信息

获取单个受管理账户的详细信息。

`GET /managed_accounts/{id}`

```java
import com.telnyx.sdk.models.managedaccounts.ManagedAccountRetrieveParams;
import com.telnyx.sdk.models.managedaccounts.ManagedAccountRetrieveResponse;

ManagedAccountRetrieveResponse managedAccount = client.managedAccounts().retrieve("id");
```

## 更新受管理的账户

更新单个受管理的账户。

`PATCH /managed_accounts/{id}`

```java
import com.telnyx.sdk.models.managedaccounts.ManagedAccountUpdateParams;
import com.telnyx.sdk.models.managedaccounts.ManagedAccountUpdateResponse;

ManagedAccountUpdateResponse managedAccount = client.managedAccounts().update("id");
```

## 禁用受管理的账户

禁用受管理的账户，使其无法使用 Telnyx 服务（包括发送或接收电话通话和短信）。

`POST /managed_accounts/{id}/actions/disable`

```java
import com.telnyx.sdk.models.managedaccounts.actions.ActionDisableParams;
import com.telnyx.sdk.models.managedaccounts.actions.ActionDisableResponse;

ActionDisableResponse response = client.managedAccounts().actions().disable("id");
```

## 恢复受管理的账户

启用受管理的账户及其子用户使用 Telnyx 服务。

`POST /managed_accounts/{id}/actions/enable`

```java
import com.telnyx.sdk.models.managedaccounts.actions.ActionEnableParams;
import com.telnyx.sdk.models.managedaccounts.actions.ActionEnableResponse;

ActionEnableResponse response = client.managedAccounts().actions().enable("id");
```

## 更新分配给特定受管理账户的全球出站通道数量

更新分配给特定受管理账户的全球出站通道数量。

`PATCH /managed_accounts/{id}/update_global_channel_limit`

```java
import com.telnyx.sdk.models.managedaccounts.ManagedAccountUpdateGlobalChannelLimitParams;
import com.telnyx.sdk.models.managedaccounts.ManagedAccountUpdateGlobalChannelLimitResponse;

ManagedAccountUpdateGlobalChannelLimitResponse response = client.managedAccounts().updateGlobalChannelLimit("id");
```

## 显示当前用户可用的全球出站通道信息

显示当前用户可用的全球出站通道信息。

`GET /managed.accounts/allocatable_global_outbound_channels`

```java
import com.telnyx.sdk.models.managedaccounts.ManagedAccountGetAllocatableGlobalOutboundChannelsParams;
import com.telnyx.sdk.models.managedaccounts.ManagedAccountGetAllocatableGlobalOutboundChannelsResponse;

ManagedAccountGetAllocatableGlobalOutboundChannelsResponse response = client.managedAccounts().getAllocatableGlobalOutboundChannels();
```