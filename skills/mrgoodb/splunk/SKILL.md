---
name: splunk
description: 通过 Splunk API 搜索和分析机器数据。执行搜索操作并管理仪表板。
metadata: {"clawdbot":{"emoji":"📊","requires":{"env":["SPLUNK_URL","SPLUNK_TOKEN"]}}}
---
# Splunk  
数据分析与安全信息事件管理（SIEM）。  

## 环境配置  
```bash
export SPLUNK_URL="https://splunk.example.com:8089"
export SPLUNK_TOKEN="xxxxxxxxxx"
```  

## 运行搜索  
```bash
curl -X POST "$SPLUNK_URL/services/search/jobs" \
  -H "Authorization: Bearer $SPLUNK_TOKEN" \
  -d "search=search index=main | head 10"
```  

## 获取搜索结果  
```bash
curl "$SPLUNK_URL/services/search/jobs/{sid}/results?output_mode=json" \
  -H "Authorization: Bearer $SPLUNK_TOKEN"
```  

## 列出保存的搜索记录  
```bash
curl "$SPLUNK_URL/services/saved/searches?output_mode=json" \
  -H "Authorization: Bearer $SPLUNK_TOKEN"
```  

## 链接  
- 文档：https://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTprolog