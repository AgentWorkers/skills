---
name: Weaviate
slug: weaviate
version: 1.0.0
description: 使用 Weaviate 的 v4 语法、正确的模块配置以及适用于生产环境的模式来构建向量搜索系统。
metadata: {"clawdbot":{"emoji":"🔷","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 重要提示：仅适用于 v4 版本（2024 年 12 月及以后）

v3 语法已被弃用。在生成任何 Weaviate 代码之前，请务必遵循以下规则：

1. **验证客户端版本** — 必须满足 `weaviate-client>=4.0` 的要求。
2. **使用上下文管理器** — 使用 `with weaviate.connect_to_*() as client:` 或显式调用 `client.close()` 来管理连接。
3. **新的导入语句** — 使用 `from weaviate.classes.config import Configure, Property` 进行模块导入。

如果您发现代码中仍然使用 v3 的语法（如 `weaviate.Client()`, `client.schema.create_class()`, `path=[...]` 等），请立即停止使用并重新编写代码。

## 快速参考

| 主题 | 文件 |
|-------|------|
| 从 v3 迁移到 v4 的指南 | `v4-syntax.md` |
| 模块配置 | `modules.md` |
| 批量处理、混合搜索、HNSW 索引 | `operations.md` |

## v4 语法要点

```python
# Connection (ALWAYS close)
with weaviate.connect_to_local() as client:
    # Collections (not classes)
    collection = client.collections.get("Article")
    
    # Queries
    response = collection.query.hybrid("search term", alpha=0.7)
    
    # Vector access
    vector = obj.vector["default"]  # Dict, not List
    
    # Filters
    Filter.by_property("category").equal("tech")
```

## 技能范围

本技能涵盖以下内容：
- RAG（Retrieval with Aggregation）和语义搜索的架构设计
- 向量化器及重新排序器的配置
- 带错误处理的批量导入功能
- 混合搜索的调优（包括 `alpha` 参数的设置）
- 用于提升搜索效率的 HNSW（Hierarchical Non-negative Semantic Weighting）索引配置

## 核心规则

### 1. 始终检查模块是否已启用
在使用 `text2vec-openai`, `generative-openai` 或重新排序器之前，请确保这些模块已正确启用：
```yaml
# docker-compose.yml
ENABLE_MODULES: 'text2vec-openai,generative-openai,reranker-cohere'
```

### 2. 在请求头中添加 API 密钥
```python
client = weaviate.connect_to_local(
    headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]}
)
```

### 3. 使用上下文管理器进行批量处理
```python
with client.batch.dynamic() as batch:
    for item in data:
        batch.add_object(properties=item, collection="Name")
```

### 4. 混合搜索中的 `alpha` 参数
- `alpha=0`：仅使用 BM25 算法（基于关键词的搜索）
- `alpha=1`：仅使用向量表示法（基于语义的搜索）
- `alpha=0.5-0.75`：平衡使用 BM25 和向量表示法（适用于 RAG 模型）

### 5. 在向量搜索前应用过滤条件
请先在 `where` 子句中应用过滤条件，以缩小搜索范围；务必在调用 `near_text`/`near_vector` 之前进行过滤。

### 6. 使用命名向量还是单个向量
每个数据集应统一选择一种向量表示方式：
```python
# Single vector (simpler)
vectorizer_config=Configure.Vectorizer.text2vec_openai()

# Named vectors (multiple embeddings per object)
vector_config=[
    Configure.Vectors.text2vec_openai(name="content", source_properties=["body"]),
]
```

### 7. 调试空结果
排查问题时，请按以下顺序检查：  
- 检查数据集的架构是否正确  
- 确保向量化器已成功运行  
- 检查距离阈值是否合理  
- 检查过滤条件的语法是否正确  
- 使用 `_additional { vector }` 来验证向量是否已成功生成。