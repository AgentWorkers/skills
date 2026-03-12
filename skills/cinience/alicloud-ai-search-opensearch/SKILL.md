---
name: alicloud-ai-search-opensearch
description: 通过 Python SDK (ha3engine) 使用 OpenSearch 的向量搜索功能来推送文档并执行 HA/SQL 搜索。非常适合 Claude Code/Codex 中的 RAG（Retrieval with Attention and Generative）和向量检索流程。
version: 1.0.0
---
**类别：提供者**  
# OpenSearch 向量搜索版  

使用 `ha3engine` SDK 来推送文档并执行 HA/SQL 搜索。本技能仅关注 API/SDK 的使用方法（不包含控制台操作步骤）。  

## 先决条件  
- 安装 SDK（建议在虚拟环境（`venv`）中安装，以避免违反 PEP 668 规范）：  
```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install alibabacloud-ha3engine
```  
- 通过环境变量提供连接配置：  
  - `OPENSEARCH_ENDPOINT`（API 域名）  
  - `OPENSEARCH_INSTANCE_ID`  
  - `OPENSEARCH_USERNAME`  
  - `OPENSEARCH_PASSWORD`  
  - `OPENSEARCH_DATASOURCE`（数据源名称）  
  - `OPENSEARCH_PK_FIELD`（主键字段名称）  

## 快速入门（推送 + 搜索）  
```python
import os
from alibabacloud_ha3engine import models, client
from Tea.exceptions import TeaException, RetryError

cfg = models.Config(
    endpoint=os.getenv("OPENSEARCH_ENDPOINT"),
    instance_id=os.getenv("OPENSEARCH_INSTANCE_ID"),
    protocol="http",
    access_user_name=os.getenv("OPENSEARCH_USERNAME"),
    access_pass_word=os.getenv("OPENSEARCH_PASSWORD"),
)
ha3 = client.Client(cfg)

def push_docs():
    data_source = os.getenv("OPENSEARCH_DATASOURCE")
    pk_field = os.getenv("OPENSEARCH_PK_FIELD", "id")

    documents = [
        {"fields": {"id": 1, "title": "hello", "content": "world"}, "cmd": "add"},
        {"fields": {"id": 2, "title": "faq", "content": "vector search"}, "cmd": "add"},
    ]
    req = models.PushDocumentsRequestModel({}, documents)
    return ha3.push_documents(data_source, pk_field, req)


def search_ha():
    # HA query example. Replace cluster/table names as needed.
    query_str = (
        "config=hit:5,format:json,qrs_chain:search"
        "&&query=title:hello"
        "&&cluster=general"
    )
    ha_query = models.SearchQuery(query=query_str)
    req = models.SearchRequestModel({}, ha_query)
    return ha3.search(req)

try:
    print(push_docs().body)
    print(search_ha())
except (TeaException, RetryError) as e:
    print(e)
```  

## 脚本快速入门  
```bash
python skills/ai/search/alicloud-ai-search-opensearch/scripts/quickstart.py
```  

**环境变量：**  
- `OPENSEARCH_ENDPOINT`  
- `OPENSEARCH_INSTANCE_ID`  
- `OPENSEARCH_USERNAME`  
- `OPENSEARCH_PASSWORD`  
- `OPENSEARCH_DATASOURCE`  
- `OPENSEARCH_PK_FIELD`（可选，默认为 `id`）  
- `OPENSEARCH_CLUSTER`（可选，默认为 `general`）  

**可选参数：**  
`--cluster`、`--hit`、`--query`  

## SQL 风格的搜索  
```python
from alibabacloud_ha3engine import models

sql = "select * from <indexTableName>&&kvpair=trace:INFO;formatType:json"
sql_query = models.SearchQuery(sql=sql)
req = models.SearchRequestModel({}, sql_query)
resp = ha3.search(req)
print(resp)
```  

## 对 Claude Code/Codex 的说明：**  
- 使用 `push_documents` 进行添加/删除操作。  
- 大型查询字符串（>30KB）应使用 RESTful 搜索 API。  
- HA 查询适用于向量数据和关键词检索，而 SQL 更适合结构化数据的查询。  

## 错误处理：**  
- **认证错误**：验证用户名/密码及实例访问权限。  
- **推送时出现 4xx 错误**：检查模式字段和 `pk_field` 的匹配情况。  
- **出现 5xx 错误**：尝试重试并设置延迟时间。  

## 验证：**  
命令执行成功时返回 0，同时会生成 `output/alicloud-ai-search-opensearch/validate.txt` 文件。  

## 输出与证据：**  
- 将生成的结果、命令输出以及 API 响应摘要保存在 `output/alicloud-ai-search-opensearch/` 目录下。  
- 在证据文件中包含关键参数（地区/资源 ID/时间范围），以便重现操作过程。  

## 工作流程：**  
1) 确认用户意图、操作区域、所需标识符，以及操作是只读还是修改操作。  
2) 先运行一个最小的只读查询以验证连接性和权限。  
3) 使用明确的参数和受限的范围执行目标操作。  
4) 验证结果并保存输出文件和证据文件。  

## 参考资料：**  
- SDK 包：`alibabacloud-ha3engine`  
- 示例：OpenSearch 文档中的数据推送及 HA/SQL 搜索示例  
- 参考资源列表：`references/sources.md`