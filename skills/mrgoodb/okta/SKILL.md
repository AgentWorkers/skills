---
name: okta
description: 通过 Okta API 管理用户、组和应用程序。处理身份和访问管理相关事宜。
metadata: {"clawdbot":{"emoji":"🔑","requires":{"env":["OKTA_DOMAIN","OKTA_API_TOKEN"]}}}
---
# Okta  
企业级身份管理解决方案。  

## 环境配置  
```bash
export OKTA_DOMAIN="your-org.okta.com"
export OKTA_API_TOKEN="xxxxxxxxxx"
```  

## 用户管理  
```bash
curl "https://$OKTA_DOMAIN/api/v1/users" \
  -H "Authorization: SSWS $OKTA_API_TOKEN"
```  

## 创建用户  
```bash
curl -X POST "https://$OKTA_DOMAIN/api/v1/users?activate=true" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"profile": {"firstName": "John", "lastName": "Doe", "email": "john@example.com", "login": "john@example.com"}}'
```  

## 组织管理  
```bash
curl "https://$OKTA_DOMAIN/api/v1/groups" -H "Authorization: SSWS $OKTA_API_TOKEN"
```  

## 应用程序管理  
```bash
curl "https://$OKTA_DOMAIN/api/v1/apps" -H "Authorization: SSWS $OKTA_API_TOKEN"
```  

## 链接  
- 管理员入口：https://your-org-admin.okta.com  
- 文档中心：https://developer.okta.com/docs/reference/