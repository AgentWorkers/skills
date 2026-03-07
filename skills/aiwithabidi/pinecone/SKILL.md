---
name: pinecone
description: "Pinecone向量数据库：通过Pinecone API管理索引、执行数据的插入/更新操作（upsert）、查询数据之间的相似性、管理命名空间以及跟踪数据集合。该数据库支持构建语义搜索系统、推荐系统以及基于高性能向量存储的RAG（Retrieval, Augmentation, and Generation）流程。专为AI应用设计，仅依赖Python标准库，无任何外部依赖。适用于向量搜索、语义相似性分析、RAG应用、推荐引擎以及AI内存系统的开发。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🌲", "requires": {"env": ["PINECONE_API_KEY"]}, "primaryEnv": "PINECONE_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🌲 Pinecone

Pinecone 是一个向量数据库，支持通过 Pinecone API 来管理索引、插入/更新向量数据、执行相似性搜索、管理命名空间以及跟踪数据集合。

## 主要功能

- **索引管理**：创建、配置和删除索引。
- **向量插入/更新**：插入并更新带有元数据的向量。
- **相似性搜索**：查询最接近的相似向量。
- **命名空间管理**：按命名空间对向量进行分类。
- **元数据过滤**：根据元数据字段过滤搜索结果。
- **集合管理**：为索引创建快照。
- **批量操作**：批量插入或删除数据。
- **索引统计**：提供向量的数量、维度和使用情况等统计信息。
- **混合搜索**：支持对稀疏向量的搜索。
- **无服务器架构**：采用自动扩展的无服务器索引服务。

## 必需配置项

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `PINECONE_API_KEY` | ✅ | 用于访问 Pinecone API 的密钥/令牌 |

## 快速入门

```bash
# List indexes
python3 {baseDir}/scripts/pinecone.py indexes
```

```bash
# Get index details
python3 {baseDir}/scripts/pinecone.py index-get my-index
```

```bash
# Create an index
python3 {baseDir}/scripts/pinecone.py index-create '{"name":"my-index","dimension":1536,"metric":"cosine","spec":{"serverless":{"cloud":"aws","region":"us-east-1"}}}'
```

```bash
# Delete an index
python3 {baseDir}/scripts/pinecone.py index-delete my-index
```



## 命令说明

### `indexes`  
列出所有索引。  
```bash
python3 {baseDir}/scripts/pinecone.py indexes
```

### `index-get`  
获取索引的详细信息。  
```bash
python3 {baseDir}/scripts/pinecone.py index-get my-index
```

### `index-create`  
创建一个新的索引。  
```bash
python3 {baseDir}/scripts/pinecone.py index-create '{"name":"my-index","dimension":1536,"metric":"cosine","spec":{"serverless":{"cloud":"aws","region":"us-east-1"}}}'
```

### `index-delete`  
删除指定的索引。  
```bash
python3 {baseDir}/scripts/pinecone.py index-delete my-index
```

### `upsert`  
插入或更新向量数据（同时包含元数据）。  
```bash
python3 {baseDir}/scripts/pinecone.py upsert --index my-index '{"vectors":[{"id":"vec1","values":[0.1,0.2,...],"metadata":{"text":"hello"}}]}'
```

### `query`  
查询与指定向量相似的向量。  
```bash
python3 {baseDir}/scripts/pinecone.py query --index my-index '{"vector":[0.1,0.2,...],"topK":10,"includeMetadata":true}'
```

### `fetch`  
根据 ID 获取向量数据。  
```bash
python3 {baseDir}/scripts/pinecone.py fetch --index my-index --ids vec1,vec2,vec3
```

### `delete`  
删除指定的向量。  
```bash
python3 {baseDir}/scripts/pinecone.py delete --index my-index --ids vec1,vec2
```

### `delete-namespace`  
删除指定命名空间中的所有向量。  
```bash
python3 {baseDir}/scripts/pinecone.py delete-namespace --index my-index --namespace docs
```

### `stats`  
获取索引的统计信息。  
```bash
python3 {baseDir}/scripts/pinecone.py stats --index my-index
```

### `collections`  
列出所有数据集合。  
```bash
python3 {baseDir}/scripts/pinecone.py collections
```

### `collection-create`  
根据索引创建一个新的数据集合。  
```bash
python3 {baseDir}/scripts/pinecone.py collection-create '{"name":"backup","source":"my-index"}'
```

### `namespaces`  
列出索引中所有的命名空间。  
```bash
python3 {baseDir}/scripts/pinecone.py namespaces --index my-index
```


## 输出格式

所有命令默认以 JSON 格式输出。若需以更易读的格式查看输出，可添加 `--human` 参数。  
```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/pinecone.py indexes --limit 5

# Human-readable
python3 {baseDir}/scripts/pinecone.py indexes --limit 5 --human
```

## 脚本参考

| 脚本 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/pinecone.py` | 主要的命令行工具（CLI），用于执行所有 Pinecone 操作 |

## 数据存储政策

本技能 **从不将数据存储在本地**。所有请求都会直接发送到 Pinecone API，结果会返回到标准输出（stdout），数据始终保存在 Pinecone 服务器上。

## 致谢  
Pinecone 由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
相关视频教程可在 [YouTube](https://youtube.com/@aiwithabidi) 查看，代码示例可在 [GitHub](https://github.com/aiwithabidi) 获取。  
本技能属于 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)