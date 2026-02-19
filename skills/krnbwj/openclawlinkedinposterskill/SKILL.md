---
name: linkedin-poster
description: 通过 OAuth 将更新内容发布到用户的 LinkedIn 个人资料中。
metadata:
  openclaw:
    skillKey: linkedin-poster
    requires:
      env:
        - LINKEDIN_CLIENT_ID
        - LINKEDIN_CLIENT_SECRET
    invocation:
      policy: on-demand
      triggers:
        - pattern: "post to linkedin"
        - pattern: "share on linkedin"
        - pattern: "linkedin post"
        - pattern: "post to linkedin org"
        - pattern: "linkedin company post"
---
# LinkedIn 发帖工具

您可以直接通过 OpenClaw 更新 LinkedIn 个人资料中的帖子内容。

## 主要功能

- 支持 OAuth 2.0 认证（只需设置一次）
- 自动管理访问令牌（令牌有效期为 60 天）
- 可通过命令行或 WhatsApp 进行操作
- 提供可用于生产环境的回调服务器

## 设置步骤

### 1. 配置 LinkedIn 应用

1. 在 [LinkedIn 开发者平台](https://www.linkedin.com/developers/apps) 创建一个 LinkedIn 应用。
2. 添加回调 URL：`https://linkedin-oauth-server-production.up.railway.app/callback`
3. 申请 “在 LinkedIn 上分享” 和 “使用 LinkedIn 登录” 的权限。
4. 复制您的客户端 ID（Client ID）和客户端密钥（Client Secret）。

### 2. 环境变量设置

将以下配置添加到您的 `openclaw.json` 文件中：

```json
{
  "plugins": {
    "env": {
      "LINKEDIN_CLIENT_ID": "your_client_id",
      "LINKEDIN_CLIENT_SECRET": "your_client_secret"
    }
  }
}
```

### 3. 首次使用时的授权流程

首次使用该工具时，系统会：
1. 打开浏览器进行 LinkedIn 认证。
2. 将访问令牌保存到本地。
3. 之后使用该令牌进行发帖操作。

## 使用方法

### 通过 WhatsApp

向 OpenClaw 发送消息：
```
post to linkedin: Just shipped a new feature! 🚀
```

或：
```
share on linkedin: Excited to announce our new product launch!
```

### 通过命令行

```bash
node skills/linkedin-poster/runner.cjs "Your message here"
```

### 发帖到公司页面

如果您是某个 LinkedIn 公司页面的管理员，可以按照以下步骤进行发帖：
```bash
node skills/linkedin-poster/runner.cjs "Company update!" --org "My Company Name"
```

该工具会自动搜索您管理的公司页面，并将内容发布到最匹配的页面上。

**注意：** 为了正常使用此功能，您需要在 LinkedIn 应用设置中启用 “w_organization_social” 权限（属于 Marketing API/公司页面管理范畴）。

## 工作原理

1. **首次使用**：打开浏览器进行认证 → 保存访问令牌。
2. **后续使用**：直接使用已保存的令牌进行发帖。
3. **令牌过期**：令牌在 60 天后自动过期，系统会提示您重新授权。

## OAuth 回调服务器

该工具使用以下地址作为回调服务器：
`https://linkedin-oauth-server-production.up.railway.app`

该服务器能够安全地处理 OAuth 回调请求，适用于所有使用该工具的用户。

## 常见问题解决方法

- **“redirect_uri 不匹配”**：请确保在 LinkedIn 应用设置中添加了 `https://linkedin-oauth-server-production.up.railway.app/callback` 作为回调 URL。
- **“授权超时”**：该工具会等待 60 秒后再尝试授权，请尽快完成授权操作。
- **“令牌过期”**：重新运行该工具，系统会自动启动新的 OAuth 认证流程。