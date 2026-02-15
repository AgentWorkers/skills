---
name: azure-cosmos-py
description: |
  Azure Cosmos DB SDK for Python (NoSQL API). Use for document CRUD, queries, containers, and globally distributed data.
  Triggers: "cosmos db", "CosmosClient", "container", "document", "NoSQL", "partition key".
package: azure-cosmos
---

# Azure Cosmos DB 的 Python 客户端库

这是一个用于 Azure Cosmos DB（一种分布式、多模型的 NoSQL 数据库）的客户端库。

## 安装

```bash
pip install azure-cosmos azure-identity
```

## 环境变量

```bash
COSMOS_ENDPOINT=https://<account>.documents.azure.com:443/
COSMOS_DATABASE=mydb
COSMOS_CONTAINER=mycontainer
```

## 认证

```python
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

credential = DefaultAzureCredential()
endpoint = "https://<account>.documents.azure.com:443/"

client = CosmosClient(url=endpoint, credential=credential)
```

## 客户端结构

| 客户端 | 功能 | 获取方式 |
|--------|---------|----------|
| `CosmosClient` | 账户级别的操作 | 直接实例化 |
| `DatabaseProxy` | 数据库操作 | `client.get_database_client()` |
| `ContainerProxy` | 容器/项目操作 | `database.get_container_client()` |

## 核心工作流程

### 设置数据库和容器

```python
# Get or create database
database = client.create_database_if_not_exists(id="mydb")

# Get or create container with partition key
container = database.create_container_if_not_exists(
    id="mycontainer",
    partition_key=PartitionKey(path="/category")
)

# Get existing
database = client.get_database_client("mydb")
container = database.get_container_client("mycontainer")
```

### 创建项目

```python
item = {
    "id": "item-001",           # Required: unique within partition
    "category": "electronics",   # Partition key value
    "name": "Laptop",
    "price": 999.99,
    "tags": ["computer", "portable"]
}

created = container.create_item(body=item)
print(f"Created: {created['id']}")
```

### 读取项目

```python
# Read requires id AND partition key
item = container.read_item(
    item="item-001",
    partition_key="electronics"
)
print(f"Name: {item['name']}")
```

### 更新项目

```python
item = container.read_item(item="item-001", partition_key="electronics")
item["price"] = 899.99
item["on_sale"] = True

updated = container.replace_item(item=item["id"], body=item)
```

### 插入/更新项目（Upsert）

```python
# Create if not exists, replace if exists
item = {
    "id": "item-002",
    "category": "electronics",
    "name": "Tablet",
    "price": 499.99
}

result = container.upsert_item(body=item)
```

### 删除项目

```python
container.delete_item(
    item="item-001",
    partition_key="electronics"
)
```

## 查询

### 基本查询

```python
# Query within a partition (efficient)
query = "SELECT * FROM c WHERE c.price < @max_price"
items = container.query_items(
    query=query,
    parameters=[{"name": "@max_price", "value": 500}],
    partition_key="electronics"
)

for item in items:
    print(f"{item['name']}: ${item['price']}")
```

### 跨分区查询

```python
# Cross-partition (more expensive, use sparingly)
query = "SELECT * FROM c WHERE c.price < @max_price"
items = container.query_items(
    query=query,
    parameters=[{"name": "@max_price", "value": 500}],
    enable_cross_partition_query=True
)

for item in items:
    print(item)
```

### 带有投影的查询

```python
query = "SELECT c.id, c.name, c.price FROM c WHERE c.category = @category"
items = container.query_items(
    query=query,
    parameters=[{"name": "@category", "value": "electronics"}],
    partition_key="electronics"
)
```

### 读取所有项目

```python
# Read all in a partition
items = container.read_all_items()  # Cross-partition
# Or with partition key
items = container.query_items(
    query="SELECT * FROM c",
    partition_key="electronics"
)
```

## 分区键

**重要提示**：为了确保操作的效率，请务必包含分区键。

```python
from azure.cosmos import PartitionKey

# Single partition key
container = database.create_container_if_not_exists(
    id="orders",
    partition_key=PartitionKey(path="/customer_id")
)

# Hierarchical partition key (preview)
container = database.create_container_if_not_exists(
    id="events",
    partition_key=PartitionKey(path=["/tenant_id", "/user_id"])
)
```

## 吞吐量

```python
# Create container with provisioned throughput
container = database.create_container_if_not_exists(
    id="mycontainer",
    partition_key=PartitionKey(path="/pk"),
    offer_throughput=400  # RU/s
)

# Read current throughput
offer = container.read_offer()
print(f"Throughput: {offer.offer_throughput} RU/s")

# Update throughput
container.replace_throughput(throughput=1000)
```

## 异步客户端

```python
from azure.cosmos.aio import CosmosClient
from azure.identity.aio import DefaultAzureCredential

async def cosmos_operations():
    credential = DefaultAzureCredential()
    
    async with CosmosClient(endpoint, credential=credential) as client:
        database = client.get_database_client("mydb")
        container = database.get_container_client("mycontainer")
        
        # Create
        await container.create_item(body={"id": "1", "pk": "test"})
        
        # Read
        item = await container.read_item(item="1", partition_key="test")
        
        # Query
        async for item in container.query_items(
            query="SELECT * FROM c",
            partition_key="test"
        ):
            print(item)

import asyncio
asyncio.run(cosmos_operations())
```

## 错误处理

```python
from azure.cosmos.exceptions import CosmosHttpResponseError

try:
    item = container.read_item(item="nonexistent", partition_key="pk")
except CosmosHttpResponseError as e:
    if e.status_code == 404:
        print("Item not found")
    elif e.status_code == 429:
        print(f"Rate limited. Retry after: {e.headers.get('x-ms-retry-after-ms')}ms")
    else:
        raise
```

## 最佳实践

1. **在进行点读取和查询时，务必指定分区键**。
2. **使用参数化查询**以防止注入攻击并提高缓存效率。
3. **尽可能避免跨分区查询**。
4. **使用 `upsert_item` 方法进行幂等写入操作**。
5. **在高吞吐量场景下使用异步客户端**。
6. **合理设计分区键，以实现数据均匀分布**。
7. **对于单个文档的检索，建议使用 `read_item` 方法而非直接查询。

## 参考文件

| 文件 | 内容 |
|------|----------|
| [references/partitioning.md](references/partitioning.md) | 分区键策略、分层键设计、热点分区检测与缓解方法 |
| [references/query-patterns.md](references/query-patterns.md) | 查询优化、聚合操作、分页、事务处理、变更流 |
| [scripts/setup_cosmos_container.py](scripts/setup_cosmos_container.py) | 用于创建容器（包含分区设置、配置吞吐量和索引的 CLI 工具） |