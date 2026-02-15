---
name: onelogin
description: 通过 OneLogin API 管理用户和应用程序。支持单点登录（SSO）和身份管理功能。
metadata: {"clawdbot":{"emoji":"1️⃣","requires":{"env":["ONELOGIN_CLIENT_ID","ONELOGIN_CLIENT_SECRET","ONELOGIN_REGION"]}}}
---
# OneLogin  
身份与访问管理  

## 环境  
```bash
export ONELOGIN_CLIENT_ID="xxxxxxxxxx"
export ONELOGIN_CLIENT_SECRET="xxxxxxxxxx"
export ONELOGIN_REGION="us"  # or eu
```  

## 获取访问令牌  
```bash
curl -X POST "https://api.$ONELOGIN_REGION.onelogin.com/auth/oauth2/v2/token" \
  -u "$ONELOGIN_CLIENT_ID:$ONELOGIN_CLIENT_SECRET" \
  -d "grant_type=client_credentials"
```  

## 列出用户  
```bash
curl "https://api.$ONELOGIN_REGION.onelogin.com/api/2/users" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```  

## 创建用户  
```bash
curl -X POST "https://api.$ONELOGIN_REGION.onelogin.com/api/2/users" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "firstname": "John", "lastname": "Doe"}'
```  

## 链接  
- 管理员：https://your-org.onelogin.com/admin  
- 文档：https://developers.onelogin.com