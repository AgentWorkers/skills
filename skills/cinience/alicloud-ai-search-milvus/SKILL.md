---
name: alicloud-ai-search-milvus
description: 使用阿里云Milvus（无服务器架构）结合PyMilvus来创建数据集合、插入向量数据，并执行过滤后的相似性搜索。该方案专为Claude Code/Codex的向量检索流程进行了优化。
version: 1.0.0
---
**类别：提供者（Provider）**  
**# 通过 PyMilvus 使用阿里云 Milvus（无服务器架构）**  

本技能使用标准的 PyMilvus API 来连接阿里云 Milvus 并执行向量搜索操作。  

## 先决条件  
- 安装 SDK（建议在虚拟环境（venv）中安装，以避免 PEP 668 规范的限制）：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pymilvus
```  

- 通过环境变量配置连接信息：  
  - `MILVUS_URI`（例如：`http://<host>:19530`）  
  - `MILVUS_TOKEN`（格式：`<username>:<password>`）  
  - `MILVUS_DB`（默认值：`default`）  

## 快速入门（Python）  
```python
import os
from pymilvus import MilvusClient

client = MilvusClient(
    uri=os.getenv("MILVUS_URI"),
    token=os.getenv("MILVUS_TOKEN"),
    db_name=os.getenv("MILVUS_DB", "default"),
)

# 1) Create a collection
client.create_collection(
    collection_name="docs",
    dimension=768,
)

# 2) Insert data
items = [
    {"id": 1, "vector": [0.01] * 768, "source": "kb", "chunk": 0},
    {"id": 2, "vector": [0.02] * 768, "source": "kb", "chunk": 1},
]
client.insert(collection_name="docs", data=items)

# 3) Search
query_vectors = [[0.01] * 768]
res = client.search(
    collection_name="docs",
    data=query_vectors,
    limit=5,
    filter='source == "kb" and chunk >= 0',
    output_fields=["source", "chunk"],
)
print(res)
```  

## 脚本快速入门  
```bash
python skills/ai/search/alicloud-ai-search-milvus/scripts/quickstart.py
```  

**所需环境变量：**  
- `MILVUS_URI`  
- `MILVUS_TOKEN`  
- `MILVUS_DB`（可选）  
- `MILVUS COLLECTION`（可选）  
- `MILVUS_DIMENSION`（可选）  

**可选参数：**  
`--collection`、`--dimension`、`--limit`、`--filter`  

## 对 Claude Code/Codex 的注意事项：**  
- 数据插入操作是异步的；请等待几秒钟后再搜索新插入的数据。  
- 确保向量维度与您的嵌入模型相匹配。  
- 使用过滤器来实现租户权限控制或数据集分区。  

## 错误处理：**  
- **认证错误**：检查 `MILVUS_TOKEN` 以及实例的访问权限。  
- **维度不匹配**：确保所有向量的维度与集合维度一致。  
- **网络错误**：验证实例上的 VPC/公共访问设置。  

## 验证规则：**  
命令执行成功时返回 0，同时会生成 `output/alicloud-ai-search-milvus/validate.txt` 文件。  

## 输出与证据：**  
- 将所有生成的结果、命令输出以及 API 响应内容保存到 `output/alicloud-ai-search-milvus/` 目录下。  
- 在证据文件中记录关键参数（区域、资源 ID、时间范围），以便后续复现操作。  

## 工作流程：**  
1. 确认用户操作意图、目标区域、所需数据标识符，以及操作是只读还是修改操作。  
2. 先执行一个最小的只读查询以验证连接性和权限。  
3. 使用明确的参数和受限的范围执行目标操作。  
4. 验证操作结果，并保存输出文件和证据文件。  

## 参考资料：**  
- PyMilvus 的 `MilvusClient` 示例（用于阿里云 Milvus）  
- 参考资源列表：`references/sources.md`