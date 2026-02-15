---
name: pingdom
description: 通过 Pingdom API 监控系统的正常运行时间和性能。管理检测任务并查看报告。
metadata: {"clawdbot":{"emoji":"📡","requires":{"env":["PINGDOM_API_TOKEN"]}}}
---
# Pingdom  
**服务可用性监控（Uptime Monitoring）**  

## 环境配置（Environment Configuration）  
```bash
export PINGDOM_API_TOKEN="xxxxxxxxxx"
```  

## 检查项列表（List of Checks）  
```bash
curl "https://api.pingdom.com/api/3.1/checks" -H "Authorization: Bearer $PINGDOM_API_TOKEN"
```  

## 获取检查结果（Get Check Results）  
```bash
curl "https://api.pingdom.com/api/3.1/results/{checkId}" -H "Authorization: Bearer $PINGDOM_API_TOKEN"
```  

## 创建新的检查项（Create a New Check）  
```bash
curl -X POST "https://api.pingdom.com/api/3.1/checks" \
  -H "Authorization: Bearer $PINGDOM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Website", "host": "example.com", "type": "http"}'
```  

## 链接（Links）  
- 文档：https://docs.pingdom.com/api/