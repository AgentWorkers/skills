---
name: zoominfo
description: 通过 ZoomInfo API 访问 B2B 联系人和公司数据，优化潜在客户信息并发现新的业务机会。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["ZOOMINFO_USERNAME","ZOOMINFO_PASSWORD"]}}}
---
# ZoomInfo  
B2B智能平台。  

## 环境  
```bash
export ZOOMINFO_USERNAME="xxxxxxxxxx"
export ZOOMINFO_PASSWORD="xxxxxxxxxx"
```  

## 获取访问令牌  
```bash
curl -X POST "https://api.zoominfo.com/authenticate" \
  -H "Content-Type: application/json" \
  -d '{"username": "'$ZOOMINFO_USERNAME'", "password": "'$ZOOMINFO_PASSWORD'"}'
```  

## 搜索公司  
```bash
curl -X POST "https://api.zoominfo.com/search/company" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companyName": "Acme Inc", "rpp": 10}'
```  

## 搜索联系人  
```bash
curl -X POST "https://api.zoominfo.com/search/contact" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companyId": "123456", "jobTitle": "CEO"}'
```  

## 企业信息补充  
```bash
curl -X POST "https://api.zoominfo.com/enrich/company" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"companyName": "Acme Inc", "companyWebsite": "acme.com"}'
```  

## 链接  
- 仪表盘：https://app.zoominfo.com  
- 文档：https://api-docs.zoominfo.com