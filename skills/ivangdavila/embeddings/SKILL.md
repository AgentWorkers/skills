---
name: Embeddings
slug: embeddings
description: 生成、存储和搜索向量嵌入数据；支持提供者选择（provider selection）、分块策略（chunking strategies）以及相似性搜索优化（similarity search optimization）。
---

## 使用场景

用户需要将文本或图像转换为向量数据，构建语义搜索系统，或将嵌入模型集成到应用程序中。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 提供商比较与选择 | `providers.md` |
| 内容分块策略与代码实现 | `chunking.md` |
| 向量数据库模式 | `storage.md` |
| 搜索与检索优化 | `search.md` |

## 核心功能

1. **生成嵌入向量** — 调用第三方提供商的 API（如 OpenAI、Cohere、Voyage 或本地模型）  
2. **内容分块** — 根据内容重叠程度、语义边界或字符长度限制对文档进行分割  
3. **存储向量数据** — 将生成的向量存储到 Pinecone、Weaviate、Qdrant、pgvector、Chroma 等数据库中  
4. **相似性查询** — 支持基于 top-k 结果的查询、过滤操作以及混合搜索方式  
5. **批量处理** — 支持处理大规模数据集，并提供速率限制和重试机制  
6. **模型性能评估** — 针对特定应用场景评估嵌入向量的质量  

## 决策流程

在推荐解决方案之前，请考虑以下问题：  
- [ ] 需要处理的内容类型是什么？（文本、代码、图像还是多模态数据）  
- [ ] 数据量及更新频率如何？  
- [ ] 对延迟有怎样的要求？（实时处理还是批量处理）  
- [ ] 预算有限吗？（考虑 API 使用成本与自托管方案的差异）  
- [ ] 现有的基础设施是什么？（云服务提供商或本地服务器）  

## 重要规则  

- **统一模型标准** — 所有查询操作必须使用与文档生成时相同的嵌入模型  
- **存储前进行数据标准化** — 大多数相似性度量方法要求输入数据为单位向量  
- **合理设置分块重叠比例** — 10–20% 的重叠可以避免数据边界处的信息丢失  
- **批量调用 API** — 在生产环境中切勿一次性仅处理一个数据项  
- **缓存嵌入结果** — 重新生成嵌入向量成本较高，建议使用数据源的哈希值进行缓存  
- **选择合适的维度** — 维度数并非越高越好；通常 768–1536 个维度最为合适  

## 提供商快速选择指南  

| 需求 | 推荐提供商 | 选择理由 |
|------|----------|-----|
| 最高质量（不限成本） | OpenAI `text-embedding-3-large` | 在各项基准测试中表现最佳  
| 关注成本效益 | OpenAI `text-embedding-3-small` | 成本仅为前者五分之一，但质量仍能满足大部分需求  
| 支持多语言处理 | Cohere `embed-multilingual-v3` | 支持 100 多种语言  
| 适用于代码处理场景 | Voyage `voyage-code-2` | 专为代码处理优化  
| 需要保护隐私或离线使用 | 本地部署方案（如 e5、bge、nomic） | 数据不会离开服务器  
| 图像处理 | OpenAI CLIP、Cohere 多模态服务 | 支持跨模态搜索 |

## 常见使用模式  

```python
# Batch embedding with retry
def embed_batch(texts, model="text-embedding-3-small"):
    results = []
    for chunk in batched(texts, 100):  # API limit
        response = client.embeddings.create(input=chunk, model=model)
        results.extend([e.embedding for e in response.data])
    return results

# Similarity search with filter
results = index.query(
    vector=query_embedding,
    top_k=10,
    filter={"category": "technical"},
    include_metadata=True
)
```