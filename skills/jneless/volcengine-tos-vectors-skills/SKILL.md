---
name: tos-vectors
description: 使用 TOS Vectors 服务来管理向量存储和相似性搜索。当处理嵌入数据、语义搜索、RAG（Retrieval with Adaptive Generation）系统、推荐引擎，或者用户提到向量数据库、相似性搜索或 TOS Vectors 操作时，可以使用该服务。
---

# TOS Vectors 技能

这是一套全面的技能，用于使用 TOS Vectors 服务管理向量存储、索引及相似性搜索。TOS Vectors 是一个专为人工智能应用优化的云原生向量数据库。

## 快速入门

### 初始化客户端
```python
import os
import tos

# Get credentials from environment
ak = os.getenv('TOS_ACCESS_KEY')
sk = os.getenv('TOS_SECRET_KEY')
account_id = os.getenv('TOS_ACCOUNT_ID')

# Configure endpoint and region
endpoint = 'https://tosvectors-cn-beijing.volces.com'
region = 'cn-beijing'

# Create client
client = tos.VectorClient(ak, sk, endpoint, region)
```

### 基本工作流程
```python
# 1. Create vector bucket (like a database)
client.create_vector_bucket('my-vectors')

# 2. Create vector index (like a table)
client.create_index(
    account_id=account_id,
    vector_bucket_name='my-vectors',
    index_name='embeddings-768d',
    data_type=tos.DataType.DataTypeFloat32,
    dimension=768,
    distance_metric=tos.DistanceMetricType.DistanceMetricCosine
)

# 3. Insert vectors
vectors = [
    tos.models2.Vector(
        key='doc-1',
        data=tos.models2.VectorData(float32=[0.1] * 768),
        metadata={'title': 'Document 1', 'category': 'tech'}
    )
]
client.put_vectors(
    vector_bucket_name='my-vectors',
    account_id=account_id,
    index_name='embeddings-768d',
    vectors=vectors
)

# 4. Search similar vectors
query_vector = tos.models2.VectorData(float32=[0.1] * 768)
results = client.query_vectors(
    vector_bucket_name='my-vectors',
    account_id=account_id,
    index_name='embeddings-768d',
    query_vector=query_vector,
    top_k=5,
    return_distance=True,
    return_metadata=True
)
```

## 核心操作

### 向量桶管理

- **创建向量桶**
```python
client.create_vector_bucket(bucket_name)
```

- **列出向量桶**
```python
result = client.list_vector_buckets(max_results=100)
for bucket in result.vector_buckets:
    print(bucket.vector_bucket_name)
```

- **删除向量桶**（必须为空）
```python
client.delete_vector_bucket(bucket_name, account_id)
```

### 向量索引管理

- **创建索引**
```python
client.create_index(
    account_id=account_id,
    vector_bucket_name=bucket_name,
    index_name='my-index',
    data_type=tos.DataType.DataTypeFloat32,
    dimension=128,
    distance_metric=tos.DistanceMetricType.DistanceMetricCosine
)
```

- **列出索引**
```python
result = client.list_indexes(bucket_name, account_id)
for index in result.indexes:
    print(f"{index.index_name}: {index.dimension}d")
```

### 向量数据操作

- **插入向量**（每次最多 500 个）
```python
vectors = []
for i in range(100):
    vector = tos.models2.Vector(
        key=f'vec-{i}',
        data=tos.models2.VectorData(float32=[...]),
        metadata={'category': 'example'}
    )
    vectors.append(vector)

client.put_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name=index_name,
    vectors=vectors
)
```

- **查询相似向量**（KNN 搜索）
```python
results = client.query_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name=index_name,
    query_vector=query_vector,
    top_k=10,
    filter={"$and": [{"category": "tech"}]},  # Optional metadata filter
    return_distance=True,
    return_metadata=True
)

for vec in results.vectors:
    print(f"Key: {vec.key}, Distance: {vec.distance}")
```

- **按键获取向量**
```python
result = client.get_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name=index_name,
    keys=['vec-1', 'vec-2'],
    return_data=True,
    return_metadata=True
)
```

- **删除向量**
```python
client.delete_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name=index_name,
    keys=['vec-1', 'vec-2']
)
```

## 常见用例

### 1. 语义搜索
- 为文档构建语义搜索系统：
```python
# Index documents
for doc in documents:
    embedding = get_embedding(doc.text)  # Your embedding model
    vector = tos.models2.Vector(
        key=doc.id,
        data=tos.models2.VectorData(float32=embedding),
        metadata={'title': doc.title, 'content': doc.text[:500]}
    )
    vectors.append(vector)

client.put_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name=index_name,
    vectors=vectors
)

# Search
query_embedding = get_embedding(user_query)
results = client.query_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name=index_name,
    query_vector=tos.models2.VectorData(float32=query_embedding),
    top_k=5,
    return_metadata=True
)
```

### 2. RAG（检索增强生成）
- 为大型语言模型（LLM）的提示检索相关上下文：
```python
# Retrieve relevant documents
question_embedding = get_embedding(user_question)
search_results = client.query_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name='knowledge-base',
    query_vector=tos.models2.VectorData(float32=question_embedding),
    top_k=3,
    return_metadata=True
)

# Build context
context = "\n\n".join([
    v.metadata.get('content', '') for v in search_results.vectors
])

# Generate answer with LLM
prompt = f"Context:\n{context}\n\nQuestion: {user_question}"
```

### 3. 推荐系统
- 根据用户偏好查找相似项目：
```python
# Query with metadata filtering
results = client.query_vectors(
    vector_bucket_name=bucket_name,
    account_id=account_id,
    index_name='products',
    query_vector=user_preference_vector,
    top_k=10,
    filter={"$and": [{"category": "electronics"}, {"price_range": "mid"}]},
    return_metadata=True
)
```

## 最佳实践

### 命名规范
- **向量桶名称**：3-32 个字符，仅包含小写字母、数字和连字符
- **索引名称**：3-63 个字符
- **向量键**：1-1024 个字符，使用有意义的标识符

### 批量操作
- 每次调用最多插入 500 个向量
- 每次调用最多删除 100 个向量
- 列表操作时使用分页

### 错误处理
```python
try:
    result = client.create_vector_bucket(bucket_name)
except tos.exceptions.TosClientError as e:
    print(f'Client error: {e.message}')
except tos.exceptions.TosServerError as e:
    print(f'Server error: {e.code}, Request ID: {e.request_id}')
```

### 性能技巧
- 选择合适的向量维度（在准确性和性能之间取得平衡）
- 使用元数据过滤来缩小搜索范围
- 对标准化向量使用余弦相似度
- 对绝对距离使用欧几里得距离

## 重要限制

- **每个账户最多拥有 100 个向量桶**
- **向量维度**：1-4096
- **批量插入**：每次调用最多 1000 个向量
- **批量获取/删除**：每次调用最多 100 个向量
- **查询前 K 个结果**：最多返回 30 个结果

## 额外资源

- 详细 API 参考，请参阅 [REFERENCE.md]
- 完整的工作流程，请参阅 [WORKFLOWS.md]
- 示例脚本，请查看 `scripts/` 目录