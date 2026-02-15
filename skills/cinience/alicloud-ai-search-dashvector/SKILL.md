---
name: alicloud-ai-search-dashvector
description: 使用 Python SDK 通过 DashVector 构建向量检索功能。该功能适用于创建数据集合、更新文档内容，以及在 Claude Code/Codex 中执行带有过滤条件的相似性搜索。
---

**类别：provider**  
# DashVector：向量搜索工具  

使用 DashVector 可以管理数据集合，并执行带有可选过滤条件和稀疏向量的向量相似性搜索。  

## 先决条件  
- 安装 SDK（建议在虚拟环境中安装，以避免违反 PEP 668 的限制）：  

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashvector
```  
- 通过环境变量提供凭据和端点信息：  
  - `DASHVECTOR_API_KEY`  
  - `DASHVECTOR_ENDPOINT`（集群端点）  

## 常用操作  

### 创建数据集合  
- `name`（字符串）  
- `dimension`（整数）  
- `metric`（字符串：`cosine` | `dotproduct` | `euclidean`）  
- `fields_schema`（可选的字典，包含字段类型）  

### 插入/更新文档  
- `docs`：包含 `{id, vector, fields}` 的列表或元组  
- 支持稀疏向量（`sparse_vector`）和多向量集合  

### 查询文档  
- `vector` 或 `id`（必须提供一个）；如果两者都为空，则仅应用过滤条件  
- `topk`（整数）  
- `filter`（类似 SQL 的 `WHERE` 子句）  
- `output_fields`（字段名称列表）  
- `include_vector`（布尔值）  

## 快速入门（Python SDK）  

```python
import os
import dashvector
from dashvector import Doc

client = dashvector.Client(
    api_key=os.getenv("DASHVECTOR_API_KEY"),
    endpoint=os.getenv("DASHVECTOR_ENDPOINT"),
)

# 1) Create a collection
ret = client.create(
    name="docs",
    dimension=768,
    metric="cosine",
    fields_schema={"title": str, "source": str, "chunk": int},
)
assert ret

# 2) Upsert docs
collection = client.get(name="docs")
ret = collection.upsert(
    [
        Doc(id="1", vector=[0.01] * 768, fields={"title": "Intro", "source": "kb", "chunk": 0}),
        Doc(id="2", vector=[0.02] * 768, fields={"title": "FAQ", "source": "kb", "chunk": 1}),
    ]
)
assert ret

# 3) Query
ret = collection.query(
    vector=[0.01] * 768,
    topk=5,
    filter="source = 'kb' AND chunk >= 0",
    output_fields=["title", "source", "chunk"],
    include_vector=False,
)
for doc in ret:
    print(doc.id, doc.fields)
```  

## 脚本快速入门  

```bash
python skills/ai/search/alicloud-ai-search-dashvector/scripts/quickstart.py
```  

**环境变量：**  
- `DASHVECTOR_API_KEY`  
- `DASHVECTOR_ENDPOINT`  
- `DASHVECTOR COLLECTION`（可选）  
- `DASHVECTOR_DIMENSION`（可选）  

**可选参数：**  
- `--collection`  
- `--dimension`  
- `--topk`  
- `--filter`  

**关于 Claude Code/Codex 的注意事项：**  
- 建议使用 `upsert` 方法进行幂等性数据插入。  
- 确保 `dimension` 与嵌入模型的输出尺寸一致。  
- 使用过滤条件来限定数据集的范围。  
- 如果使用稀疏向量，在插入或查询时传递 `sparse_vector={token_id: weight, ...}`。  

## 错误处理**  
- 401/403：`DASHVECTOR_API_KEY` 无效  
- 400：集合模式或维度不匹配  
- 429/5xx：采用指数退避策略重试  

## 参考资料**  
- DashVector Python SDK：`Client.create`、`Collection.upsert`、`Collection.query`  
- 源代码列表：`references/sources.md`