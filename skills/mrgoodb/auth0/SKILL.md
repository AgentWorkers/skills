---
name: auth0
description: 通过 Auth0 Management API 来管理用户、应用程序和身份验证。
metadata: {"clawdbot":{"emoji":"🔐","requires":{"env":["AUTH0_DOMAIN","AUTH0_MGMT_TOKEN"]}}}
---
# Auth0
身份验证平台（Identity platform）。

## 环境设置（Environment）
```bash
export AUTH0_DOMAIN="your-tenant.auth0.com"
export AUTH0_MGMT_TOKEN="xxxxxxxxxx"
```

## 用户管理（User Management）
```bash
curl "https://$AUTH0_DOMAIN/api/v2/users" -H "Authorization: Bearer $AUTH0_MGMT_TOKEN"
```

## 创建用户（Create User）
```bash
curl -X POST "https://$AUTH0_DOMAIN/api/v2/users" \
  -H "Authorization: Bearer $AUTH0_MGMT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "Pass123!", "connection": "Username-Password-Authentication"}'
```

## 获取用户信息（Get User Information）
```bash
curl "https://$AUTH0_DOMAIN/api/v2/users/{userId}" -H "Authorization: Bearer $AUTH0_MGMT_TOKEN"
```

## 应用程序管理（Application Management）
```bash
curl "https://$AUTH0_DOMAIN/api/v2/clients" -H "Authorization: Bearer $AUTH0_MGMT_TOKEN"
```

## 链接（Links）
- 仪表板：https://manage.auth0.com
- 文档：https://auth0.com/docs/api/management/v2