---
name: auth-tool-cloudbase
description: 使用 CloudBase Auth 工具来配置和管理 Web 应用程序的认证提供者——启用/禁用登录方式（短信、电子邮件、微信开放平台、Google、匿名登录、用户名/密码、OAuth、SAML、CAS、钉钉等），并通过 MCP 工具 `callCloudApi` 来配置提供者的相关设置。
alwaysApply: false
---
## 概述

您可以配置 CloudBase 的认证提供者，包括匿名登录、用户名/密码登录、短信登录、邮箱登录、微信登录、Google 登录等。

**前提条件**：需要 CloudBase 环境 ID（`env`）。

---

## 认证场景

### 1. 获取登录策略

查询当前的登录配置：
```js
{
    "params": { "EnvId": `env` },
    "service": "lowcode",
    "action": "DescribeLoginStrategy"
}
```
返回 `LoginStrategy` 对象；如果未配置，则返回 `false`。

---

### 2. 匿名登录

1. 获取 `LoginStrategy`（参见场景 1）
2. 将 `LoginStrategy.AnonymousLogin` 设置为 `true`（启用）或 `false`（禁用）
3. 更新配置：
```js
{
    "params": { "EnvId": `env`, ...LoginStrategy },
    "service": "lowcode",
    "action": "ModifyLoginStrategy"
}
```

---

### 3. 用户名/密码登录

1. 获取 `LoginStrategy`（参见场景 1）
2. 将 `LoginStrategyUserNameLogin` 设置为 `true`（启用）或 `false`（禁用）
3. 更新配置：
```js
{
    "params": { "EnvId": `env`, ...LoginStrategy },
    "service": "lowcode",
    "action": "ModifyLoginStrategy"
}
```

---

### 4. 短信登录

1. 获取 `LoginStrategy`（参见场景 1）
2. 修改配置：
   - **启用**：`LoginStrategy.PhoneNumberLogin = true`
   - **禁用**：`LoginStrategy.PhoneNumberLogin = false`
   - **配置**（可选）：
     ```js
     LoginStrategy.SmsVerificationConfig = {
         Type: 'default',      // 'default' or 'apis'
         Method: 'methodName',
         SmsDayLimit: 30       // -1 = unlimited
     }
     ```
3. 更新配置：
```js
{
    "params": { "EnvId": `env`, ...LoginStrategy },
    "service": "lowcode",
    "action": "ModifyLoginStrategy"
}
```

---

### 5. 邮箱登录

**启用（腾讯云邮箱）：**
```js
{
    "params": {
        "EnvId": `env`,
        "Id": "email",
        "On": "TRUE",
        "EmailConfig": { "On": "TRUE", "SmtpConfig": {} }
    },
    "service": "tcb",
    "action": "ModifyProvider"
}
```

**禁用：**
```js
{
    "params": { "EnvId": `env`, "Id": "email", "On": "FALSE" },
    "service": "tcb",
    "action": "ModifyProvider"
}
```

**启用（自定义 SMTP）：**
```js
{
    "params": {
        "EnvId": `env`,
        "Id": "email",
        "On": "TRUE",
        "EmailConfig": {
            "On": "FALSE",
            "SmtpConfig": {
                "AccountPassword": "password",
                "AccountUsername": "username",
                "SecurityMode": "SSL",
                "SenderAddress": "sender@example.com",
                "ServerHost": "smtp.qq.com",
                "ServerPort": 465
            }
        }
    },
    "service": "tcb",
    "action": "ModifyProvider"
}
```

---

### 6. 微信登录

1. 获取微信配置信息：
```js
{
    "params": { "EnvId": `env` },
    "service": "tcb",
    "action": "GetProviders"
}
```
通过 `Id == "wx_open"` 进行过滤，并将结果保存到 `WeChatProvider` 变量中。

2. 从 [微信开放平台](https://open.weixin.qq.com/cgi-bin/readtemplate?t=regist/regist_tmpl) 获取以下凭证：
   - `AppID`
   - `AppSecret`

3. 更新配置：
```js
{
    "params": {
        "EnvId": `env`,
        "Id": "wx_open",
        "On": "TRUE",  // "FALSE" to disable
        "Config": {
            ...WeChatProvider.Config,
            ClientId: `AppID`,
            ClientSecret: `AppSecret`
        }
    },
    "service": "tcb",
    "action": "ModifyProvider"
}
```

---

### 7. Google 登录

1. 获取重定向 URI：
```js
{
    "params": { "EnvId": `env` },
    "service": "lowcode",
    "action": "DescribeStaticDomain"
}
```
将 `result.Data.StaticDomain` 保存到 `staticDomain` 变量中。

2. 在 [Google Cloud 控制台](https://console.cloud.google.com/apis/credentials) 进行配置：
   - 创建 OAuth 2.0 客户端 ID
   - 设置重定向 URI：`https://{staticDomain}/__auth/`
   - 获取 `Client ID` 和 `Client Secret`

3. 启用 Google 登录功能：
```js
{
    "params": {
        "EnvId": `env`,
        "ProviderType": "OAUTH",
        "Id": "google",
        "On": "TRUE",  // "FALSE" to disable
        "Name": { "Message": "Google" },
        "Description": { "Message": "" },
        "Config": {
            "ClientId": `Client ID`,
            "ClientSecret": `Client Secret`,
            "Scope": "email openid profile",
            "AuthorizationEndpoint": "https://accounts.google.com/o/oauth2/v2/auth",
            "TokenEndpoint": "https://oauth2.googleapis.com/token",
            "UserinfoEndpoint": "https://www.googleapis.com/oauth2/v3/userinfo",
            "TokenEndpointAuthMethod": "CLIENT_SECRET_BASIC",
            "RequestParametersMap": {
                "RegisterUserSyncScope": "syncEveryLogin",
                "IsGoogle": "TRUE"
            }
        },
        "Picture": "https://qcloudimg.tencent-cloud.cn/raw/f9131c00dcbcbccd5899a449d68da3ba.png",
        "TransparentMode": "FALSE",
        "ReuseUserId": "TRUE",
        "AutoSignUpWithProviderUser": "TRUE"
    },
    "service": "tcb",
    "action": "ModifyProvider"
}
```

### 8. 获取可发布密钥（Publishable Key）

**查询现有密钥：**
```js
{
    "params": { "EnvId": `env`, "KeyType": "publish_key", "PageNumber": 1, "PageSize": 10 },
    "service": "lowcode",
    "action": "DescribeApiKeyTokens"
}
```
如果存在密钥，则返回 `PublishableKeyApiKey`（通过 `Name == "publish_key"` 进行过滤）。

**创建新密钥**（如果不存在）：
```js
{
    "params": { "EnvId": `env`, "KeyType": "publish_key", "KeyName": "publish_key" },
    "service": "lowcode",
    "action": "CreateApiKeyToken"
}
```
如果创建失败，请引导用户访问以下链接：`https://tcb.cloud.tencent.com/dev?envId=`env`#/env/apikey`