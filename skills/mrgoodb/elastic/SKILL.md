---
name: elastic
description: 通过 Elasticsearch API 搜索和分析数据。对集群进行索引、搜索和管理。
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["ELASTICSEARCH_URL","ELASTICSEARCH_API_KEY"]}}}
---
# Elasticsearch  
分布式搜索与分析工具。  

## 环境配置  
```bash
export ELASTICSEARCH_URL="https://elastic.example.com:9200"
export ELASTICSEARCH_API_KEY="xxxxxxxxxx"
```  

## 集群健康状况  
```bash
curl "$ELASTICSEARCH_URL/_cluster/health" -H "Authorization: ApiKey $ELASTICSEARCH_API_KEY"
```  

## 搜索功能  
```bash
curl -X POST "$ELASTICSEARCH_URL/my-index/_search" \
  -H "Authorization: ApiKey $ELASTICSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": {"match": {"message": "error"}}}'
```  

## 索引与文档  
```bash
curl -X POST "$ELASTICSEARCH_URL/my-index/_doc" \
  -H "Authorization: ApiKey $ELASTICSEARCH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Log entry", "timestamp": "2024-01-30T10:00:00Z"}'
```  

## 参考资料  
- 文档：https://www.elastic.co/guide/en/elasticsearch/reference/current/rest-apis.html