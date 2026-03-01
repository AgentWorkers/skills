---
name: shared-pinecone-rag
description: 使用共享的 Pinecone RAG 索引来处理此工作空间中的任何代理。当代理需要将 Markdown/文本文档导入 pulse-rag，或从共享索引中查询语义上下文时，请使用该索引。
---
# 共享的 Pinecone RAG（Shared Pinecone RAG）

请使用位于以下路径的中央 RAG 项目：
`/home/Mike/.openclaw/workspace/rag-pinecone-starter`

当与 `hybrid-db-health` 结合使用时，可将其视为一个 **持久内存技能堆栈（Persistent Memory skill stack）**：
- `shared-pinecone-rag`：负责数据检索和导入（retrieval + ingest）功能
- `hybrid-db-health`：负责系统的可靠性与健康监控（reliability/health monitoring）

## 查询（所有代理）（Query for all agents）

```bash
bash scripts/query-shared-rag.sh "your question"
```

## 导入文档（所有代理）（Ingest documents for all agents）

1. 将 `.md` 或 `.txt` 文件放入以下路径：
`/home/Mike/.openclaw/workspace/rag-pinecone-starter/docs/`
2. 运行以下命令：

```bash
bash scripts/ingest-shared-rag.sh
```

## 必备条件（Requirements）

- 确保在 `rag-pinecone-starter/.env` 文件中设置了 `PINECONE_API_KEY`
- 在 `rag-pinecone-starter/.venv` 中创建了 Python 虚拟环境（Python venv）

## 注意事项（Notes）

- 索引名称默认为 `pulse-rag`。
- 数据检索操作会从 `default` 命名空间中读取数据。
- 该技能是共享的；除非有明确要求，否则不要为每个代理单独创建重复的 RAG 堆栈。