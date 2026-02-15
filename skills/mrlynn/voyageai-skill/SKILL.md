---
name: voyageai
description: >
  Voyage AI embedding and reranking CLI integrated with MongoDB Atlas Vector Search.
  Use for: generating text embeddings, reranking search results, storing embeddings in Atlas,
  performing vector similarity search, creating vector search indexes, listing available models,
  comparing text similarity, bulk ingestion, interactive demos, and learning about AI concepts.
  Triggers: embed text, generate embeddings, vector search, rerank documents, voyage ai,
  semantic search, similarity search, store embeddings, atlas vector search, embedding models,
  cosine similarity, bulk ingest, explain embeddings.
metadata:
  openclaw:
    emoji: "🧭"
    author:
      name: Michael Lynn
      url: https://mlynn.org
      github: mrlynn
    version: "1.4.0"
    license: MIT
    tags:
      - embeddings
      - vector-search
      - reranking
      - mongodb
      - atlas
      - semantic-search
      - rag
      - voyage-ai
    requires:
      bins:
        - vai
      env:
        - VOYAGE_API_KEY
    install:
      - id: npm
        kind: npm
        package: voyageai-cli
        global: true
---

# 🧭 Voyage AI Skill

该工具使用 `vai` 命令行界面（[voyageai-cli](https://github.com/mrlynn/voyageai-cli)）来处理 Voyage AI 的嵌入、重新排序功能以及 MongoDB Atlas 的向量搜索功能。完全基于 Node.js 开发，无需使用 Python。

## 设置

```bash
npm install -g voyageai-cli
```

### 环境变量

| 变量 | 必需条件 | 说明 |
|----------|-------------|-------------|
| `VOYAGE_API_KEY` | embed, rerank, store, search, similarity, ingest, ping | 来自 MongoDB Atlas 的模型 API 密钥 |
| `MONGODB_URI` | store, search, index, ingest, ping （可选） | Atlas 连接字符串 |

获取您的 API 密钥：**MongoDB Atlas → AI Models → 创建模型 API 密钥**

## 命令参考（共 14 条命令）

### embed — 生成嵌入向量

```bash
vai embed "What is MongoDB?"
vai embed "search query" --model voyage-4-large --input-type query --dimensions 512
vai embed --file document.txt --input-type document
cat texts.txt | vai embed
vai embed "hello" --output-format array
```

### rerank — 重新排序文档

```bash
vai rerank --query "database performance" --documents "MongoDB is fast" "SQL is relational"
vai rerank --query "best database" --documents-file candidates.json --top-k 3
```

### store — 将数据嵌入并存储到 Atlas 中

```bash
vai store --db mydb --collection docs --field embedding \
  --text "MongoDB Atlas is a cloud database" \
  --metadata '{"source": "docs"}'

# Batch from JSONL
vai store --db mydb --collection docs --field embedding --file documents.jsonl
```

### search — 执行向量搜索

```bash
vai search --query "cloud database" --db mydb --collection docs \
  --index vector_index --field embedding

# With pre-filter
vai search --query "performance" --db mydb --collection docs \
  --index vector_index --field embedding --filter '{"category": "guides"}' --limit 5
```

### index — 管理向量搜索索引

```bash
vai index create --db mydb --collection docs --field embedding \
  --dimensions 1024 --similarity cosine --index-name my_index
vai index list --db mydb --collection docs
vai index delete --db mydb --collection docs --index-name my_index
```

### models — 列出可用的模型

```bash
vai models
vai models --type embedding
vai models --type reranking
vai models --json
```

### ping — 测试连接是否正常

```bash
vai ping
vai ping --json
```

### config — 管理配置信息

```bash
vai config set api-key "pa-your-key"
echo "pa-your-key" | vai config set api-key --stdin
vai config get
vai config delete api-key
vai config path
vai config reset
```

### demo — 交互式引导式操作流程

```bash
vai demo
vai demo --no-pause
vai demo --skip-pipeline
vai demo --keep
```

### explain — 了解 AI 相关概念

```bash
vai explain                      # List all topics
vai explain embeddings
vai explain reranking
vai explain vector-search
vai explain rag
vai explain cosine-similarity
vai explain two-stage-retrieval
vai explain input-type
vai explain models
vai explain api-keys
vai explain api-access
vai explain batch-processing
```

### similarity — 比较文本的相似度

```bash
vai similarity "MongoDB is a document database" "MongoDB Atlas is a cloud database"
vai similarity "database performance" --against "MongoDB is fast" "PostgreSQL is relational"
vai similarity --file1 doc1.txt --file2 doc2.txt
vai similarity "text A" "text B" --json
```

### ingest — 批量导入数据并显示进度

```bash
vai ingest --file corpus.jsonl --db myapp --collection docs --field embedding
vai ingest --file data.csv --db myapp --collection docs --field embedding --text-column content
vai ingest --file corpus.jsonl --db myapp --collection docs --field embedding \
  --model voyage-4 --batch-size 100 --input-type document
vai ingest --file corpus.jsonl --db myapp --collection docs --field embedding --dry-run
```

### completions — 提供 Shell 自动补全功能

```bash
vai completions bash    # Output bash completion script
vai completions zsh     # Output zsh completion script

# Install bash completions
vai completions bash >> ~/.bashrc && source ~/.bashrc

# Install zsh completions
vai completions zsh > ~/.zsh/completions/_vai
```

### help — 显示帮助信息

```bash
vai help
vai help embed
vai embed --help
```

## 常见工作流程

### 嵌入 → 存储 → 搜索流程

```bash
# 1. Store documents
vai store --db myapp --collection articles --field embedding \
  --text "MongoDB Atlas provides a fully managed cloud database" \
  --metadata '{"title": "Atlas Overview"}'

# 2. Create index
vai index create --db myapp --collection articles --field embedding \
  --dimensions 1024 --similarity cosine --index-name article_search

# 3. Search
vai search --query "how does cloud database work" \
  --db myapp --collection articles --index article_search --field embedding
```

### 两阶段检索流程（嵌入 + 重新排序）

```bash
# 1. Get candidates via vector search
vai search --query "database scaling" --db myapp --collection articles \
  --index article_search --field embedding --limit 20 --json > candidates.json

# 2. Rerank for precision
vai rerank --query "database scaling" --documents-file candidates.json --top-k 5
```

### 批量导入数据流程

```bash
# 1. Validate data (dry run)
vai ingest --file corpus.jsonl --db myapp --collection docs --field embedding --dry-run

# 2. Ingest with progress
vai ingest --file corpus.jsonl --db myapp --collection docs --field embedding

# 3. Create index
vai index create --db myapp --collection docs --field embedding \
  --dimensions 1024 --similarity cosine
```

## 全局参数

| 参数 | 说明 |
|------|-------------|
| `--json` | 以机器可读的 JSON 格式输出结果 |
| `--quiet` | 抑制非必要的输出信息 |

## 参考资料

- [模型目录](references/models.md) — 所有模型及其价格和规格信息 |
- [向量搜索指南](references/vector-search.md) — MongoDB Atlas 的向量搜索集成说明