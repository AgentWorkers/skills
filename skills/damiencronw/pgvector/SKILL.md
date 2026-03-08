---
name: pgvector
description: "PostgreSQL 的向量数据库功能通过 `pgvector` 扩展得以实现。该扩展支持向量相似性搜索、嵌入数据的存储、RAG（Retrieval-Augmented Generation，检索增强生成）流程，以及结合向量搜索和关键词搜索的混合搜索方式。适用场景包括：存储/检索嵌入数据、开发需要向量搜索功能的 AI 应用程序、实现 RAG 算法、进行语义搜索，或任何需要使用向量数据库功能的场景。"
metadata:
  {
    "openclaw": { "emoji": "🔢" },
    "version": "1.0.0",
  }
---
# pgvector 技能

PostgreSQL + pgvector 扩展用于向量相似性搜索。

## 快速连接

```bash
# Connect to pgvector database (default port 5433)
psql -h localhost -p 5433 -U damien -d postgres

# Or use environment variables
export PGHOST=localhost
export PGPORT=5433
export PGUSER=damien
export PGPASSWORD=''
export PGDATABASE=postgres
```

## 环境配置

- **主机**: localhost
- **端口**: 5433
- **用户名**: damien
- **密码**: （空）
- **数据库**: postgres

## 核心功能

### 1. 创建向量表

```sql
-- Basic vector table (1536 dimensions for OpenAI embeddings)
CREATE TABLE IF NOT EXISTS documents (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(1536) NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create HNSW index for fast similarity search
CREATE INDEX ON documents USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- Or use IVFFlat index (faster build, slower search)
CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

### 2. 插入嵌入向量

```sql
-- Manual insert (replace with actual embedding)
INSERT INTO documents (content, embedding)
VALUES ('Your text here', '[0.1, 0.2, ..., 0.1536]');

-- With metadata
INSERT INTO documents (content, embedding, metadata)
VALUES (
    'AI is transforming technology',
    '[0.1, 0.3, ..., 0.5]',
    '{"source": "article", "author": "John"}'::jsonb
);
```

### 3. 向量相似性搜索

```sql
-- Cosine similarity (most common)
SELECT id, content, (1 - (embedding <=> '[query_embedding]')) AS similarity
FROM documents
ORDER BY embedding <=> '[query_embedding]'
LIMIT 5;

-- Euclidean distance
SELECT id, content, (embedding <-> '[query_embedding]') AS distance
FROM documents
ORDER BY embedding <-> '[query_embedding]'
LIMIT 5;

-- Inner product (for normalized vectors)
SELECT id, content, (embedding <#> '[query_embedding]') AS similarity
FROM documents
ORDER BY embedding <#> '[query_embedding]'
LIMIT 5;
```

### 4. 混合搜索（向量 + 关键词）

```sql
-- Combine vector search with full-text search
SELECT id, content,
    (1 - (embedding <=> '[query_embedding]')) AS vector_score,
    ts_rank(to_tsvector('english', content), plainto_tsquery('english', 'search terms')) AS text_score
FROM documents
WHERE content ILIKE '%search terms%'
ORDER BY (vector_score * 0.7 + text_score * 0.3) DESC
LIMIT 10;
```

### 5. RAG 管道示例

```sql
-- Store document chunks with embeddings
CREATE TABLE document_chunks (
    id BIGSERIAL PRIMARY KEY,
    document_id BIGINT REFERENCES documents(id),
    chunk_text TEXT NOT NULL,
    chunk_embedding vector(1536) NOT NULL,
    chunk_index INT NOT NULL
);

-- Retrieve relevant chunks for LLM context
SELECT chunk_text
FROM document_chunks
WHERE document_id = ?
ORDER BY chunk_embedding <=> '[question_embedding]'
LIMIT 5;
```

## 管理命令

### 检查 pgvector 扩展的状态

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

### 表信息查询

```sql
-- List all tables with vectors
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Check index sizes
SELECT pg_size_pretty(pg_total_relation_size('documents'));
```

### 监控

```sql
-- Check query performance
EXPLAIN ANALYZE
SELECT * FROM documents
ORDER BY embedding <=> '[query_embedding]'
LIMIT 5;

-- Index usage stats
SELECT * FROM pg_stat_user_indexes
WHERE indexname LIKE '%embedding%';
```

## 常用操作

### 更新嵌入向量

```sql
UPDATE documents
SET embedding = '[new_embedding]'
WHERE id = 1;
```

### 删除数据

```sql
DELETE FROM documents WHERE id = 1;
```

### 批量插入（Python）

```python
import psycopg2
import numpy as np

conn = psycopg2.connect(
    host="localhost",
    port=5433,
    user="damien",
    password="",
    database="postgres"
)

cur = conn.cursor()
for text, embedding in documents:
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (text, embedding.tolist())
    )
conn.commit()
```

## 距离运算符

| 运算符 | 描述 |
|----------|-------------|
| `<->` | 欧几里得距离 |
| `<=>` | 余弦距离 |
| `<#>` | 内积 |
| `<=>` | 余弦距离（1 - 余弦相似度） |

## 使用场景

1. **语义搜索** - 根据文档的含义进行搜索，而非关键词
2. **RAG** - 为大型语言模型（LLM）提示检索相关上下文
3. **推荐系统** - 查找相似的项目/产品
4. **异常检测** - 识别嵌入向量中的异常值
5. **图像/视频搜索** - 存储和查询视觉嵌入向量

## 注意事项

- 向量的维度必须与您的嵌入模型相匹配
- HNSW 算法在准确性方面表现更好，IVFFlat 更适合处理大型数据集
- 在计算余弦相似度之前，请对向量进行归一化处理
- pgvector 支持最多 16,000 个维度