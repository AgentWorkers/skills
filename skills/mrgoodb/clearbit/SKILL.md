---
name: clearbit
description: 通过 Clearbit API 丰富潜在客户和公司的信息。获取公司和个人的相关数据。
metadata: {"clawdbot":{"emoji":"✨","requires":{"env":["CLEARBIT_API_KEY"]}}}
---
# Clearbit  
数据增强服务。  

## 环境  
```bash
export CLEARBIT_API_KEY="sk_xxxxxxxxxx"
```  

## 个人信息增强  
```bash
curl "https://person.clearbit.com/v2/people/find?email=user@example.com" \
  -u "$CLEARBIT_API_KEY:"
```  

## 公司信息增强  
```bash
curl "https://company.clearbit.com/v2/companies/find?domain=example.com" \
  -u "$CLEARBIT_API_KEY:"
```  

## 综合信息增强  
```bash
curl "https://person.clearbit.com/v2/combined/find?email=user@example.com" \
  -u "$CLEARBIT_API_KEY:"
```  

## 关联信息揭示（IP地址与公司信息）  
```bash
curl "https://reveal.clearbit.com/v1/companies/find?ip=8.8.8.8" \
  -u "$CLEARBIT_API_KEY:"
```  

## 链接  
- 仪表盘：https://dashboard.clearbit.com  
- 文档：https://clearbit.com/docs