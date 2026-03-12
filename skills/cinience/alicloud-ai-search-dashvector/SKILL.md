---
name: alicloud-ai-search-dashvector
description: 使用 Python SDK 通过 DashVector 构建向量检索功能。该功能适用于创建数据集合、更新文档内容（upserting），以及在 Claude Code/Codex 中执行带有过滤条件的相似性搜索。
version: 1.0.0
---
**类别：提供者（Provider）**

# DashVector 向量搜索（Vector Search）

使用 DashVector 管理数据集合，并执行向量相似性搜索，支持可选的过滤条件和稀疏向量（sparse vectors）。

## 先决条件

- 安装 SDK（建议在虚拟环境（venv）中安装，以避免违反 PEP 668 的限制）：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install dashvector
```

- 通过环境变量提供凭据和端点信息：
  - `DASHVECTOR_API_KEY`
  - `DASHVECTOR_ENDPOINT`（集群端点）

## 常用操作

### 创建数据集合（Create Collection）
- `name`（字符串）
- `dimension`（整数）
- `metric`（字符串：`cosine` | `dotproduct` | `euclidean`）
- `fields_schema`（可选的字典，包含字段类型）

### 插入/更新文档（Upsert Docs）
- `docs`：包含 `{id, vector, fields}` 的列表或元组
- 支持稀疏向量（sparse vectors）和多向量集合

### 查询文档（Query Docs）
- `vector` 或 `id`（必须提供一个）；如果两者都为空，则仅应用过滤条件
- `topk`（整数）
- `filter`（类似 SQL 的 where 子句）
- `output_fields`（字段名称列表）
- `include_vector`（布尔值）

## 快速入门（Python SDK）**

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

## 脚本快速入门**

```bash
python skills/ai/search/alicloud-ai-search-dashvector/scripts/quickstart.py
```

**环境变量：**
- `DASHVECTOR_API_KEY`
- `DASHVECTOR_ENDPOINT`
- `DASHVECTOR COLLECTION`（可选）
- `DASHVECTOR_DIMENSION`（可选）

**可选参数：**
- `--collection`、`--dimension`、`--topk`、`--filter`

## 对 Claude Code/Codex 的说明：
- 建议使用 `upsert` 方法进行幂等性数据插入（idempotent data insertion）。
- 确保 `dimension` 与您的嵌入模型输出大小一致。
- 使用过滤条件来限制数据访问范围（例如，按租户或数据集划分）。
- 如果使用稀疏向量，在插入或查询时传递 `sparse_vector={token_id: weight, ...}`。

## 错误处理：
- 401/403：`DASHVECTOR_API_KEY` 无效
- 400：集合模式或维度不匹配
- 429/5xx：采用指数退避策略重试

## 验证：
- 命令执行成功时返回 0，并生成 `output/alicloud-ai-search-dashvector/validate.txt` 文件。

## 输出与证据：
- 将输出结果、命令输出和 API 响应保存在 `output/alicloud-ai-search-dashvector/` 目录下。
- 在证据文件中包含关键参数（区域/资源 ID/时间范围），以便重现实验结果。

## 工作流程：
1) 确认用户意图、操作区域、所需标识符以及操作是只读还是修改操作。
2) 首先运行一个最小的只读查询以验证连接性和权限。
3) 使用明确的参数和受限的范围执行目标操作。
4) 验证结果并保存输出文件和证据文件。

## 参考资料：
- DashVector Python SDK：`Client.create`、`Collection.upsert`、`Collection.query`
- 参考文档列表：`references/sources.md`