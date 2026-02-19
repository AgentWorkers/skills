---
name: qdrant-advanced
version: 1.0.0
description: "适用于 AI 代理的高级 Qdrant 向量数据库操作功能：包括语义搜索、基于分块的文档导入、集合管理、快照生成以及迁移工具等。这些功能为 Qdrant 的完整生命周期提供了现成的脚本支持。适用场景包括：  
(1) 在多个集合中实现语义搜索；  
(2) 通过智能分块技术导入文档；  
(3) 以编程方式管理集合内容；  
(4) 创建备份并进行数据迁移。"
metadata:
  openclaw:
    requires:
      bins: ["curl", "python3", "bash"]
      env: ["QDRANT_HOST", "QDRANT_PORT", "OPENAI_API_KEY"]
      config: []
    user-invocable: true
  homepage: https://github.com/yoder-bawt
  author: yoder-bawt
---
# Qdrant Advanced

专为AI代理设计的、可投入生产的Qdrant向量数据库操作工具。提供完整的功能集，包括语义搜索、文档导入、集合管理、备份和迁移等。

## 快速入门

```bash
# Set environment variables
export QDRANT_HOST="localhost"
export QDRANT_PORT="6333"
export OPENAI_API_KEY="sk-..."

# List collections
bash manage.sh list

# Create a collection
bash manage.sh create my_collection 1536 cosine

# Ingest a document
bash ingest.sh /path/to/document.txt my_collection paragraph

# Search
bash search.sh "my search query" my_collection 5
```

## 脚本概述

| 脚本 | 功能 | 主要特性 |
|--------|---------|--------------|
| `search.sh` | 语义搜索 | 支持多集合搜索、设置过滤条件、调整分数阈值 |
| `ingest.sh` | 文档导入 | 支持上下文分割、批量上传、显示上传进度 |
| `manage.sh` | 集合管理 | 创建、删除、列出、查看集合信息、优化集合 |
| `backup.sh` | 备份 | 生成集合快照、恢复数据、列出快照 |
| `migrate.sh` | 数据迁移 | 在不同集合间迁移数据、升级嵌入模型 |

## 环境变量

| 变量 | 是否必需 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `QDRANT_HOST` | 否 | `localhost` | Qdrant服务器主机名 |
| `QDRANT_PORT` | 否 | `6333` | Qdrant服务器端口 |
| `OPENAI_API_KEY` | 是* | - | 用于嵌入模型的OpenAI API密钥 |
| `QDRANT_API_KEY` | 否 | - | （如果启用了身份验证）Qdrant API密钥 |

*`OPENAI_API_KEY` 对于文档导入和搜索操作是必需的。

## 详细使用说明

### 语义搜索

```bash
bash search.sh <query> <collection> [limit] [filter_json]
```

**示例：**

```bash
# Basic search
bash search.sh "machine learning tutorials" my_docs 10

# With metadata filter
bash search.sh "deployment guide" my_docs 5 '{"must": [{"key": "category", "match": {"value": "devops"}}]}'

# Score threshold
bash search.sh "error handling" my_docs 10 "" 0.8
```

**输出：**
```json
{
  "results": [
    {
      "id": "doc-001",
      "score": 0.92,
      "text": "When handling errors in production...",
      "metadata": {"source": "docs/error-handling.md"}
    }
  ]
}
```

### 文档导入

```bash
bash ingest.sh <file_path> <collection> [chunk_strategy] [metadata_json]
```

**分割策略：**

| 策略 | 说明 | 适用场景 |
|----------|-------------|----------|
| `paragraph` | 按段落（`\n\n`）分割 | 文章、文档 |
| `sentence` | 按句子分割 | 短内容 |
| `fixed` | 固定1000个字符的分割块 | 代码、日志 |
| `semantic` | 基于语义分割 | 长文档 |

**示例：**

```bash
# Ingest with paragraph chunking
bash ingest.sh article.md my_collection paragraph

# With custom metadata
bash ingest.sh api.md my_collection paragraph '{"category": "api", "version": "2.0"}'

# Ingest multiple files
for f in docs/*.md; do
    bash ingest.sh "$f" my_collection paragraph
done
```

### 集合管理

```bash
bash manage.sh <command> [args...]
```

**命令：**

| 命令 | 参数 | 说明 |
|---------|-----------|-------------|
| `list` | - | 列出所有集合 |
| `create` | `名称` `维度` `距离` | 创建新集合 |
| `delete` | `名称` | 删除集合 |
| `info` | `名称` | 查看集合信息 |
| `optimize` | `名称` | 优化集合 |

**示例：**

```bash
bash manage.sh list
bash manage.sh create my_vectors 1536 cosine
bash manage.sh create my_vectors 768 euclid
bash manage.sh info my_vectors
bash manage.sh optimize my_vectors
bash manage.sh delete my_vectors
```

### 备份与恢复

```bash
bash backup.sh <command> [args...]
```

**命令：**

| 命令 | 参数 | 说明 |
|---------|-----------|-------------|
| `snapshot` | `集合 [快照名称]` | 创建快照 |
| `restore` | `集合 快照名称` | 从快照恢复数据 |
| `list` | `集合` | 列出快照 |
| `delete` | `集合 快照名称` | 删除快照 |

**示例：**

```bash
# Create snapshot
bash backup.sh snapshot my_collection
bash backup.sh snapshot my_collection backup_2026_02_10

# List snapshots
bash backup.sh list my_collection

# Restore
bash backup.sh restore my_collection backup_2026_02_10

# Delete old snapshot
bash backup.sh delete my_collection old_backup
```

### 数据迁移

**迁移类型：**

1. **复制集合**：保持相同的嵌入模型，仅更改集合名称 |
2. **模型升级**：将数据迁移到新的嵌入模型 |
3. **过滤迁移**：迁移包含特定过滤条件的数据子集 |

**示例：**

```bash
# Simple copy
bash migrate.sh old_collection new_collection

# With model upgrade (re-embeds all content)
bash migrate.sh old_collection new_collection --upgrade-model

# Filtered migration
bash migrate.sh old_collection new_collection --filter '{"category": "public"}'

# Batch size for large collections
bash migrate.sh old_collection new_collection --batch-size 50
```

## 分割策略详解

导入脚本采用了智能的分割策略来保留文档的上下文：

### 段落分割
- 根据双换行符分割段落
- 保留段落的完整结构
- 每个分割块之间会包含两个句子的内容
- 适用于：文章、文档、博客等长文本

### 句子分割
- 根据句子边界分割文本
- 分割块之间几乎没有重叠
- 适用于：短内容、推文、引文等

### 固定长度分割
- 每个分割块固定1000个字符
- 分割块之间有200个字符的重叠部分
- 适用于：代码文件、日志、非结构化文本

### 基于语义的分割
- 结合段落和标题信息进行分割
- 保留文档的结构
- 适用于：包含标题的长文档

## API参考

所有脚本均通过Qdrant的REST API进行交互：

```
GET    /collections              # List collections
PUT    /collections/{name}       # Create collection
DELETE /collections/{name}       # Delete collection
GET    /collections/{name}       # Collection info
POST   /collections/{name}/points/search     # Search
PUT    /collections/{name}/points           # Upsert points
POST   /snapshots                # Create snapshot
GET    /collections/{name}/snapshots         # List snapshots
```

完整文档：https://qdrant.tech/documentation/

## 性能优化建议

1. **批量上传**：`ingest.sh`脚本会自动进行批量上传（默认每次上传100条数据） |
2. **批量插入后进行优化**：执行 `bash manage.sh optimize my_collection` 命令优化集合性能 |
3. **使用过滤条件**：通过元数据过滤来缩小搜索范围 |
4. **设置分数阈值**：筛选掉质量较低的搜索结果 |
5. **索引元数据**：为元数据添加索引以提高搜索效率 |

## 常见问题解决方法

### “连接被拒绝”
- 确保Qdrant服务器正在运行：`curl http://$QDRANT_HOST:$QDRANT_PORT/healthz`
- 检查`QDRANT_HOST`和`QDRANT_PORT`环境变量的设置是否正确

### “找不到集合”
- 使用 `bash manage.sh list` 命令列出所有集合 |
- 检查集合名称的拼写是否正确

### “没有搜索结果”
- 确认文档已成功导入：`bash manage.sh info my_collection` |
- 检查文档的嵌入维度是否正确（例如，文本嵌入模型应为1536维） |
- 尝试降低分数阈值以提高搜索效果

### 嵌入模型相关问题
- 确保`OPENAI_API_KEY`已设置 |
- 检查API密钥是否有使用权限 |
- 确保能够正常访问OpenAI API

### 备份失败
- 检查磁盘空间是否充足 |
- 确保Qdrant具有创建快照的权限 |
- 对于大型集合，建议在网络流量较低的时候进行备份

## 系统要求

- Qdrant服务器版本需达到1.0及以上 |
- 需要安装`curl`、`python3`和`bash`工具 |
- 需要OpenAI API密钥（用于嵌入模型） |
- 确保系统能够访问Qdrant和OpenAI API

## 相关资源

- Qdrant官方文档：https://qdrant.tech/documentation/
- OpenAI嵌入模型文档：https://platform.openai.com/docs/guides/embeddings |
- 向量搜索指南：https://qdrant.tech/documentation/concepts/search/