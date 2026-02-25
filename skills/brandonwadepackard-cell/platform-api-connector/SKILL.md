---
name: platform-api-connector
description: 通过访问开发者门户、创建应用程序、获取 OAuth 令牌以及存储凭证，您可以连接到社交媒体和内容平台的 API。本文档涵盖了 Facebook Graph API、Instagram Business API、YouTube Data API、Twitter/X API v2 以及 TikTok Content Posting API。这些内容适用于为任何社交媒体平台设置 API 访问权限、刷新过期的 OAuth 令牌或调试认证流程。
---
# 平台 API 连接器

用于导航开发者门户并获取社交/内容平台的 API 凭据。将这些凭据存储在 Supabase（或其他数据库）中以供后续使用。

## 通用流程

1. 在平台的开发者门户上创建开发者应用。
2. 配置 OAuth 重定向 URI 和权限范围。
3. 完成 OAuth 流程（或生成 API 密钥）。
4. 以结构化格式存储凭据。
5. 通过简单的 API 调用进行测试。

## Facebook + Instagram

Facebook 和 Instagram 使用相同的认证系统。一个 Facebook 页面令牌可以同时用于这两个平台。

### 设置步骤
1. 访问 `developers.facebook.com/apps` → 创建应用 → 选择“企业”类型。
2. 添加“Facebook 登录”功能。
3. 在 Graph API Explorer（`developers.facebook.com/tools/explorer/`）中：
   - 选择你的应用。
   - 添加以下权限：`pages_show_list`、`pages_read_engagement`、`pages_manage_posts`、`instagram_basic`、`instagram_content_publish`。
   - 生成用户访问令牌（User Access Token）→ 授权。
   - 将用户访问令牌兑换为长期有效的令牌：`GET /oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={secret}&fb_exchange_token={short_token}`。
4. 获取页面访问令牌（Page Access Token）：`GET /me/accounts` → 查找目标页面 → 复制 `access_token`。
5. 获取 Instagram 企业账户 ID：`GET /{page_id}?fields=instagram_business_account`。

### 凭据存储
```json
{
  "platform": "facebook",
  "credentials": {
    "app_id": "...",
    "app_secret": "...",
    "page_id": "...",
    "page_access_token": "...",
    "ig_user_id": "..."
  }
}
```

### 注意事项
- 从 Graph API Explorer 获取的页面访问令牌是**短期有效的**，除非你先使用用户访问令牌兑换成长期有效的令牌，然后再使用该长期令牌来获取页面令牌。从长期有效用户令牌生成的页面令牌是**永久有效的**（无过期时间）。

## YouTube

### 设置步骤
1. 访问 `console.cloud.google.com` → API 与服务 → 凭据。
2. 创建 OAuth 2.0 客户端 ID（Web 应用类型）。
3. 添加重定向 URI：`http://localhost:8422/callback`（或你的回调 URL）。
4. 启用 YouTube 数据 API v3。
5. 运行本地 OAuth 流程：

```python
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/youtube.upload',
            'https://www.googleapis.com/auth/youtube.readonly']
)
creds = flow.run_local_server(port=8422)
# creds.token, creds.refresh_token, creds.expiry
```

### 凭据存储
```json
{
  "platform": "youtube",
  "credentials": {
    "client_id": "...",
    "client_secret": "...",
    "access_token": "...",
    "refresh_token": "...",
    "token_expiry": "..."
  }
}
```

### 注意事项
- 如果用户之前仅获得了有限的权限范围，刷新令牌可能无法覆盖 `youtube.upload` 功能。需要重新授权（使用 `prompt='consent'`），以获取具有完整权限范围的新的刷新令牌。

## Twitter/X

### 设置步骤
1. 访问 `developer.x.com/en/portal/dashboard`。
2. 创建项目并应用（免费 tier：每月 100 条帖子）。
3. 在“密钥和令牌”（Keys and Tokens）部分：
   - API 密钥（API Key）+ 秘密密钥（Secret Key）：用于客户端身份验证。
   - 承载令牌（Bearer Token）：仅用于读取数据的客户端身份验证。
   - 访问令牌（Access Token）+ 秘密密钥（Secret Key）：用于写入数据的用户身份验证——需要配置读写权限。
4. 如果在生成令牌时仅授予了读取权限，需要在权限更改为读写权限后**重新生成**访问令牌。

### 凭据存储
```json
{
  "platform": "twitter",
  "credentials": {
    "api_key": "...",
    "api_secret": "...",
    "bearer_token": "...",
    "access_token": "...",
    "access_token_secret": "..."
  }
}
```

### 注意事项
- 免费 tier 的使用限制是每月 100 条帖子（以账单日期为准，而非日历月份）。免费 tier 不支持数据删除或分析功能。

## TikTok

### 设置步骤
1. 访问 `developers.tiktok.com` → 创建应用。
2. 添加所需的功能：登录工具包（Login Kit）+ 内容发布 API（Content Posting API）。
3. 配置应用信息：应用图标（1024x1024 像素）、类别、服务条款 URL、隐私政策 URL、重定向 URI。
4. **提交审核**——TikTok 需要一个展示应用功能的演示视频。
5. 在获得批准之前，可以使用**手动模式**（生成内容但需手动发布）。

### 注意事项
- TikTok 的内容发布 API 需要经过完整的审核流程，并提供演示视频。审核过程可能需要几天到几周的时间。在审核期间，可以使用**手动模式**作为临时解决方案。登录工具包可以在沙箱模式下用于开发。

## 凭据存储方式

使用一个包含 JSONB 数据类型的表格来存储凭据，这样可以灵活地管理不同平台的认证信息：

```sql
CREATE TABLE platform_connections (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  platform TEXT NOT NULL,
  account_name TEXT,
  credentials JSONB NOT NULL,
  scopes TEXT[],
  status TEXT DEFAULT 'active',
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

JSONB 可以适应不同平台的认证需求，而无需更改数据结构。

## 令牌刷新方式

```python
async def get_valid_token(platform: str) -> dict:
    conn = await get_connection(platform)
    creds = conn['credentials']
    
    if platform == 'youtube' and is_expired(creds.get('token_expiry')):
        new_token = refresh_google_token(creds['refresh_token'], creds['client_id'], creds['client_secret'])
        creds['access_token'] = new_token
        await update_connection(conn['id'], creds)
    
    # Facebook page tokens don't expire (if derived from long-lived user token)
    # Twitter tokens don't expire
    # TikTok tokens expire in 24h — refresh with refresh_token
    
    return creds
```