---
name: graphiti
description: 通过 Graphiti API 进行知识图谱操作：搜索事实、添加新数据（episodes），以及提取实体（entities）和它们之间的关系（relationships）。
homepage: https://github.com/getzep/graphiti
metadata: {"clawdbot":{"emoji":"🕸️","requires":{"services":["neo4j","qdrant","graphiti"]},"install":[{"id":"docker","kind":"docker-compose","label":"Install Graphiti stack (Docker)"}]}}
---

# Graphiti知识图谱

您可以使用Graphiti的REST API查询和管理您的知识图谱，该API支持动态服务发现功能。

## 先决条件

- Neo4j数据库（用于存储图结构）
- Qdrant（用于向量搜索）
- Graphiti服务已启动（默认地址：http://localhost:8001）

## 工具

### graphiti_search
用于在知识图谱中搜索相关信息。

**使用方法：**
```bash
bash command:"
GRAPHITI_URL=\$({baseDir}/references/env-check.sh)
curl -s -X POST \"\$GRAPHITI_URL/facts/search\" \
  -H 'Content-Type: application/json' \
  -d '{\"query\": \"YOUR_QUERY\", \"max_facts\": 10}' | jq .
"
```

### graphiti_add
用于向知识图谱中添加新的条目/记忆（memory）。

**使用方法：**
```bash
bash command:"
GRAPHITI_URL=\$({baseDir}/references/env-check.sh)
curl -s -X POST \"\$GRAPHITI_URL/messages\" \
  -H 'Content-Type: application/json' \
  -d '{\"name\": \"EPISODE_NAME\", \"content\": \"EPISODE_CONTENT\"}' | jq .
"
```

## 动态配置

该功能通过环境变量自动查找Graphiti的地址：

1. **Clawdbot配置**：`clawdbot config get skills.graphitibaseUrl`
2. **系统环境变量**：`$GRAPHITI_URL`
3. **默认备用地址**：`http://localhost:8001`

要更改Graphiti的URL，请执行以下操作：
```bash
export GRAPHITI_URL="http://10.0.0.10:8001"
# OR
clawdbot config set skills.graphiti.baseUrl "http://10.0.0.10:8001"
```

## 示例

- 搜索信息：
```bash
bash command:"
GRAPHITI_URL=\$({baseDir}/references/env-check.sh)
curl -s -X POST \"\$GRAPHITI_URL/facts/search\" \
  -H 'Content-Type: application/json' \
  -d '{\"query\": \"Tell me about Essam Masoudy\", \"max_facts\": 5}'
"
```

- 添加新条目：
```bash
bash command:"
GRAPHITI_URL=\$({baseDir}/references/env-check.sh)
curl -s -X POST \"\$GRAPHITI_URL/messages\" \
  -H 'Content-Type: application/json' \
  -d '{\"name\": \"Project Update\", \"content\": \"Completed Phase 1 of Clawdbot integration\"}'
"
```