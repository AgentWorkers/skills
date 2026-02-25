# ChromaDB 内存

ChromaDB 是一个长期存储系统，支持使用 Ollama 嵌入模型进行数据存储。在每次操作之前，系统会自动检索并插入相关的上下文信息。

## 主要特性

- 与 ChromaDB 向量数据库集成
- 支持 Ollama 嵌入模型
- 自动检索相关记忆内容
- 支持自定义集合名称

## 配置

```json
{
  "chromaUrl": "http://localhost:8100",
  "collectionName": "longterm_memory",
  "ollamaUrl": "http://localhost:11434",
  "embeddingModel": "nomic-embed-text",
  "autoRecall": true,
  "autoRecallResults": 3,
  "minScore": 0.5
}
```