---
name: supabase
description: 连接到 Supabase 以执行数据库操作、向量搜索和数据存储。它可用于存储数据、运行 SQL 查询、使用 pgvector 进行相似性搜索以及管理表格。当涉及到数据库、向量存储、嵌入数据或 Supabase 本身的请求时，会触发相应的触发器。
metadata: {"clawdbot":{"requires":{"env":["SUPABASE_URL","SUPABASE_SERVICE_KEY"]}}}
---

# Supabase CLI

用于与 Supabase 项目进行交互：执行查询、CRUD 操作、向量搜索以及表管理。

## 设置

```bash
# Required
export SUPABASE_URL="https://yourproject.supabase.co"
export SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIs..."

# Optional: for management API
export SUPABASE_ACCESS_TOKEN="sbp_xxxxx"
```

## 快速命令

```bash
# SQL query
{baseDir}/scripts/supabase.sh query "SELECT * FROM users LIMIT 5"

# Insert data
{baseDir}/scripts/supabase.sh insert users '{"name": "John", "email": "john@example.com"}'

# Select with filters
{baseDir}/scripts/supabase.sh select users --eq "status:active" --limit 10

# Update
{baseDir}/scripts/supabase.sh update users '{"status": "inactive"}' --eq "id:123"

# Delete
{baseDir}/scripts/supabase.sh delete users --eq "id:123"

# Vector similarity search
{baseDir}/scripts/supabase.sh vector-search documents "search query" --match-fn match_documents --limit 5

# List tables
{baseDir}/scripts/supabase.sh tables

# Describe table
{baseDir}/scripts/supabase.sh describe users
```

## 命令参考

### query - 运行原始 SQL 语句

```bash
{baseDir}/scripts/supabase.sh query "<SQL>"

# Examples
{baseDir}/scripts/supabase.sh query "SELECT COUNT(*) FROM users"
{baseDir}/scripts/supabase.sh query "CREATE TABLE items (id serial primary key, name text)"
{baseDir}/scripts/supabase.sh query "SELECT * FROM users WHERE created_at > '2024-01-01'"
```

### select - 带过滤条件的表查询

```bash
{baseDir}/scripts/supabase.sh select <table> [options]

Options:
  --columns <cols>    Comma-separated columns (default: *)
  --eq <col:val>      Equal filter (can use multiple)
  --neq <col:val>     Not equal filter
  --gt <col:val>      Greater than
  --lt <col:val>      Less than
  --like <col:val>    Pattern match (use % for wildcard)
  --limit <n>         Limit results
  --offset <n>        Offset results
  --order <col>       Order by column
  --desc              Descending order

# Examples
{baseDir}/scripts/supabase.sh select users --eq "status:active" --limit 10
{baseDir}/scripts/supabase.sh select posts --columns "id,title,created_at" --order created_at --desc
{baseDir}/scripts/supabase.sh select products --gt "price:100" --lt "price:500"
```

### insert - 插入行

```bash
{baseDir}/scripts/supabase.sh insert <table> '<json>'

# Single row
{baseDir}/scripts/supabase.sh insert users '{"name": "Alice", "email": "alice@test.com"}'

# Multiple rows
{baseDir}/scripts/supabase.sh insert users '[{"name": "Bob"}, {"name": "Carol"}]'
```

### update - 更新行

```bash
{baseDir}/scripts/supabase.sh update <table> '<json>' --eq <col:val>

# Example
{baseDir}/scripts/supabase.sh update users '{"status": "inactive"}' --eq "id:123"
{baseDir}/scripts/supabase.sh update posts '{"published": true}' --eq "author_id:5"
```

### upsert - 插入或更新行

```bash
{baseDir}/scripts/supabase.sh upsert <table> '<json>'

# Example (requires unique constraint)
{baseDir}/scripts/supabase.sh upsert users '{"id": 1, "name": "Updated Name"}'
```

### delete - 删除行

```bash
{baseDir}/scripts/supabase.sh delete <table> --eq <col:val>

# Example
{baseDir}/scripts/supabase.sh delete sessions --lt "expires_at:2024-01-01"
```

### vector-search - 使用 pgvector 进行相似性搜索

```bash
{baseDir}/scripts/supabase.sh vector-search <table> "<query>" [options]

Options:
  --match-fn <name>     RPC function name (default: match_<table>)
  --limit <n>           Number of results (default: 5)
  --threshold <n>       Similarity threshold 0-1 (default: 0.5)
  --embedding-model <m> Model for query embedding (default: uses OpenAI)

# Example
{baseDir}/scripts/supabase.sh vector-search documents "How to set up authentication" --limit 10

# Requires a match function like:
# CREATE FUNCTION match_documents(query_embedding vector(1536), match_threshold float, match_count int)
```

### tables - 列出所有表

```bash
{baseDir}/scripts/supabase.sh tables
```

### describe - 显示表结构

```bash
{baseDir}/scripts/supabase.sh describe <table>
```

### rpc - 调用存储过程

```bash
{baseDir}/scripts/supabase.sh rpc <function_name> '<json_params>'

# Example
{baseDir}/scripts/supabase.sh rpc get_user_stats '{"user_id": 123}'
```

## 向量搜索设置

### 1. 启用 pgvector 扩展

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### 2. 创建包含嵌入列的表

```sql
CREATE TABLE documents (
  id bigserial PRIMARY KEY,
  content text,
  metadata jsonb,
  embedding vector(1536)
);
```

### 3. 创建相似性搜索功能

```sql
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding vector(1536),
  match_threshold float DEFAULT 0.5,
  match_count int DEFAULT 5
)
RETURNS TABLE (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.content,
    documents.metadata,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

### 4. 为提高性能创建索引

```sql
CREATE INDEX ON documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);
```

## 环境变量

| 变量 | 是否必填 | 说明 |
|----------|----------|-------------|
| SUPABASE_URL | 是 | 项目 URL（例如：https://xxx.supabase.co） |
| SUPABASE_SERVICE_KEY | 是 | 服务角色密钥（具有完整访问权限） |
| SUPABASE_ANON_KEY | 否 | 匿名密钥（仅限受限访问） |
| SUPABASE_ACCESS_TOKEN | 否 | 管理 API 令牌 |
| OPENAI_API_KEY | 否 | 用于生成嵌入向量 |

## 注意事项：

- 服务角色密钥可绕过 RLS（行级安全）机制 |
- 使用匿名密钥进行客户端访问或受限访问 |
- 向量搜索需要启用 pgvector 扩展 |
- 嵌入向量的默认类型为 OpenAI 的 text-embedding-ada-002（1536 维度）