---
name: netlify
description: 通过 API 管理 Netlify 网站、执行部署操作以及调用相关功能。部署并配置 Web 项目。
metadata: {"clawdbot":{"emoji":"🔷","requires":{"env":["NETLIFY_AUTH_TOKEN"]}}}
---
# Netlify  
一个用于Web应用的部署平台。  

## 环境配置  
```bash
export NETLIFY_AUTH_TOKEN="xxxxxxxxxx"
```  

## 命令行界面（CLI）命令  
```bash
netlify sites:list
netlify deploy --prod
netlify env:list
netlify functions:list
```  

## API  
- **列出所有网站**：  
```bash
curl "https://api.netlify.com/api/v1/sites" -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN"
```  
- **触发部署**：  
```bash
curl -X POST "https://api.netlify.com/api/v1/sites/{site_id}/builds" \
  -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN"
```  
- **查看已部署的网站**：  
```bash
curl "https://api.netlify.com/api/v1/sites/{site_id}/deploys" \
  -H "Authorization: Bearer $NETLIFY_AUTH_TOKEN"
```  

## 链接  
- **控制面板**：https://app.netlify.com  
- **文档**：https://docs.netlify.com/api/get-started/