---
name: elasticsearch
description: 通过 `curl` 命令使用 REST API 与 Elasticsearch 和 Kibana 进行交互。适用于查询、索引管理、检查集群健康状况、编写聚合数据、部署仪表板或排查 Elasticsearch 相关问题。需要提供集群的 URL 和 API 密钥。涵盖的内容包括：搜索（Query DSL）、CRUD 操作、索引管理、映射（Mappings）、聚合数据（Aggregations）、集群健康检查、索引生命周期管理（ILM）、ES|QL 语法、Kibana API（仪表板、数据视图、保存的对象）、OpenTelemetry 数据格式以及常见的故障排查方法。
---
# Elasticsearch

与Elasticsearch的所有交互都通过REST API使用`curl`来完成。无需任何SDK或客户端库。

## 认证

每个请求都需要集群URL和API密钥：

```bash
# Set these for your session (or export in .env / shell profile)
ES_URL="https://your-cluster.es.cloud.elastic.co:443"
ES_API_KEY="your-base64-api-key"

# All requests follow this pattern:
curl -s "${ES_URL%/}/<endpoint>" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '<json-body>'
```

**API密钥格式：** Base64编码的`id:api_key`字符串。直接将其作为`Authorization: ApiKey`头部传递。

如果用户提供了URL和密钥，请在运行命令之前将它们分别设置为`ES_URL`和`ES_API_KEY`。

**重要提示——在curl中使用变量扩展：**
- 在curl头部中始终使用`$(printenv ES_API_KEY)`，而不是`$ES_API_KEY`。`$ES_API_KEY`变量可能在shell中无法正确扩展，导致`Authorization`头部为空并引发401错误。
- 始终使用`${ES_URL}/`来去除URL末尾的斜杠，以避免双斜杠路径问题（例如`//_cluster/health`）。

## 快速健康检查

```bash
# Cluster health (green/yellow/red) — NOT available on serverless
curl -s "${ES_URL%/}/_cluster/health" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Node stats summary — NOT available on serverless
curl -s "${ES_URL%/}/_cat/nodes?v&h=name,heap.percent,ram.percent,cpu,load_1m,disk.used_percent"  \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Index overview (works on both serverless and traditional)
curl -s "${ES_URL%/}/_cat/indices?v&s=store.size:desc&h=index,health,status,docs.count,store.size" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"
```

**无服务器Elasticsearch：** 如果遇到`api_not_available_exception`错误，说明集群正在无服务器模式下运行。以下API在无服务器模式下**不可用**：
- `_cluster/health`、`_cluster/settings`、`_cluster/allocation/explain`、`_cluster/pending_tasks`
- `_cat/nodes`、`_cat/shards`
- `_nodes/hot_threads`、`_nodes/stats`
- ILM API（`_ilm/*`）

请改用 `_cat/indices`和 `_search` API作为起点——这些API在所有模式下都可用。

## 搜索（查询DSL）

```bash
# Simple match query
curl -s "${ES_URL%/}/my-index/_search" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": { "match": { "message": "error timeout" } },
    "size": 10
  }' | jq .

# Bool query (must + filter + must_not)
curl -s "${ES_URL%/}/my-index/_search" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "bool": {
        "must": [ { "match": { "message": "error" } } ],
        "filter": [ { "range": { "@timestamp": { "gte": "now-1h" } } } ],
        "must_not": [ { "term": { "level": "debug" } } ]
      }
    },
    "size": 20,
    "sort": [ { "@timestamp": { "order": "desc" } } ]
  }' | jq .
```

有关完整的Query DSL参考（术语、范围、通配符、正则表达式、嵌套查询、存在性检查、多条件匹配等），请参阅[references/query-dsl.md](references/query-dsl.md)。

## 索引与文档操作

```bash
# Create index with mappings
curl -s -X PUT "${ES_URL%/}/my-index" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "settings": { "number_of_shards": 1, "number_of_replicas": 1 },
    "mappings": {
      "properties": {
        "message":    { "type": "text" },
        "@timestamp": { "type": "date" },
        "level":      { "type": "keyword" },
        "count":      { "type": "integer" }
      }
    }
  }'

# Index a document (auto-generate ID)
curl -s -X POST "${ES_URL%/}/my-index/_doc" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "message": "hello world", "@timestamp": "2026-01-31T12:00:00Z", "level": "info" }'

# Index with specific ID
curl -s -X PUT "${ES_URL%/}/my-index/_doc/doc-123" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "message": "specific doc", "level": "warn" }'

# Get document
curl -s "${ES_URL%/}/my-index/_doc/doc-123" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Update document (partial)
curl -s -X POST "${ES_URL%/}/my-index/_update/doc-123" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "doc": { "level": "error" } }'

# Delete document
curl -s -X DELETE "${ES_URL%/}/my-index/_doc/doc-123" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Bulk operations (newline-delimited JSON)
curl -s -X POST "${ES_URL%/}/_bulk" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/x-ndjson" \
  --data-binary @- << 'EOF'
{"index":{"_index":"my-index"}}
{"message":"bulk doc 1","level":"info","@timestamp":"2026-01-31T12:00:00Z"}
{"index":{"_index":"my-index"}}
{"message":"bulk doc 2","level":"warn","@timestamp":"2026-01-31T12:01:00Z"}
EOF
```

## 聚合操作

```bash
# Terms aggregation (top values)
curl -s "${ES_URL%/}/my-index/_search?size=0" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "aggs": {
      "levels": { "terms": { "field": "level", "size": 10 } }
    }
  }' | jq '.aggregations'

# Date histogram + nested metric
curl -s "${ES_URL%/}/my-index/_search?size=0" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": { "range": { "@timestamp": { "gte": "now-24h" } } },
    "aggs": {
      "over_time": {
        "date_histogram": { "field": "@timestamp", "fixed_interval": "1h" },
        "aggs": {
          "avg_count": { "avg": { "field": "count" } }
        }
      }
    }
  }' | jq '.aggregations'
```

有关更多聚合类型（基数、百分位数、复合聚合、过滤器、重要术语等），请参阅[references/aggregations.md](references/aggregations.md)。

## 映射与索引管理

```bash
# Get mapping
curl -s "${ES_URL%/}/my-index/_mapping" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Add field to existing mapping (mappings are additive — you can't change existing field types)
curl -s -X PUT "${ES_URL%/}/my-index/_mapping" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "properties": { "new_field": { "type": "keyword" } } }'

# Reindex (change mappings, rename index, etc.)
curl -s -X POST "${ES_URL%/}/_reindex" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "source": { "index": "old-index" },
    "dest":   { "index": "new-index" }
  }'

# Delete index
curl -s -X DELETE "${ES_URL%/}/my-index" -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Index aliases
curl -s -X POST "${ES_URL%/}/_aliases" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "actions": [
      { "add": { "index": "my-index-v2", "alias": "my-index" } },
      { "remove": { "index": "my-index-v1", "alias": "my-index" } }
    ]
  }'

# Index templates (for time-series / rollover patterns)
curl -s -X PUT "${ES_URL%/}/_index_template/my-template" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "index_patterns": ["logs-*"],
    "template": {
      "settings": { "number_of_shards": 1 },
      "mappings": {
        "properties": {
          "message":    { "type": "text" },
          "@timestamp": { "type": "date" }
        }
      }
    }
  }'
```

## 集群与故障排除

> **注意：** 本节中的大多数API在无服务器Elasticsearch中**不可用**。它们仅适用于自我管理的或传统的Elastic Cloud部署。

```bash
# Allocation explanation (why is a shard unassigned?) — NOT serverless
curl -s "${ES_URL%/}/_cluster/allocation/explain" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{ "index": "my-index", "shard": 0, "primary": true }' | jq .

# Pending tasks
curl -s "${ES_URL%/}/_cluster/pending_tasks" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Hot threads (performance debugging)
curl -s "${ES_URL%/}/_nodes/hot_threads" -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Shard allocation
curl -s "${ES_URL%/}/_cat/shards?v&s=store:desc&h=index,shard,prirep,state,docs,store,node" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)"

# Task management (long-running operations)
curl -s "${ES_URL%/}/_tasks?actions=*search&detailed" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Cluster settings (persistent + transient)
curl -s "${ES_URL%/}/_cluster/settings?include_defaults=false" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .
```

有关Kibana API操作（仪表板、数据视图、保存的对象、警报规则等），请参阅[references/kibana-api.md](references/kibana-api.md)。

## 数据流与ILM

> **注意：** ILM API（`_ilm/*`）在无服务器模式下**不可用**。不过数据流列表功能在两种模式下都可用。

```bash
# List data streams
curl -s "${ES_URL%/}/_data_stream" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .

# Create ILM policy
curl -s -X PUT "${ES_URL%/}/_ilm/policy/my-policy" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "policy": {
      "phases": {
        "hot":    { "actions": { "rollover": { "max_age": "7d", "max_size": "50gb" } } },
        "warm":   { "min_age": "30d", "actions": { "shrink": { "number_of_shards": 1 } } },
        "delete": { "min_age": "90d", "actions": { "delete": {} } }
      }
    }
  }'

# Check ILM status for an index
curl -s "${ES_URL%/}/my-index/_ilm/explain" -H "Authorization: ApiKey $(printenv ES_API_KEY)" | jq .
```

## ES|QL（Elasticsearch查询语言）

从Elasticsearch 8.11版本开始，ES|QL提供了基于管道的查询语法：

```bash
curl -s -X POST "${ES_URL%/}/_query" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM logs-* | WHERE level == \"error\" | STATS count = COUNT(*) BY service.name | SORT count DESC | LIMIT 10"
  }' | jq .
```

有关查询OpenTelemetry数据（OTEL日志、跟踪记录、指标、关联模式等），请参阅[references/otel-data.md](references/otel-data.md)。

## 数据摄取管道

```bash
# Create pipeline
curl -s -X PUT "${ES_URL%/}/_ingest/pipeline/my-pipeline" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "processors": [
      { "grok": { "field": "message", "patterns": ["%{TIMESTAMP_ISO8601:timestamp} %{LOGLEVEL:level} %{GREEDYDATA:msg}"] } },
      { "date": { "field": "timestamp", "formats": ["ISO8601"] } },
      { "remove": { "field": "timestamp" } }
    ]
  }'

# Test pipeline
curl -s -X POST "${ES_URL%/}/_ingest/pipeline/my-pipeline/_simulate" \
  -H "Authorization: ApiKey $(printenv ES_API_KEY)" \
  -H "Content-Type: application/json" \
  -d '{
    "docs": [
      { "_source": { "message": "2026-01-31T12:00:00Z ERROR something broke" } }
    ]
  }' | jq .
```

## 提示

- **始终使用`jq`来格式化JSON输出**——Elasticsearch的响应内容较为冗长。
- 在搜索请求中添加`?size=0`以仅获取聚合结果（跳过实际匹配的文档）。
- `_cat` API（`_cat/indices`、`_cat/shards`、`_cat/nodes`）会返回易于阅读的表格格式输出；添加`?v`可显示头部信息，添加`?format=json`可获取JSON格式的结果。
- 对于大量数据导出，建议使用`PIT`（Paginated Iteration）功能——避免使用`from`/`size`参数超过10,000条记录。改用`search_after` + `PIT`。
- **字段类型很重要**：`keyword`用于精确匹配和聚合操作，`text`用于全文搜索。在查询前请检查相应的映射设置。
- **索引名称中的日期运算**：`logs-{now/d}`表示今天的日期。这对于基于时间的索引非常有用。