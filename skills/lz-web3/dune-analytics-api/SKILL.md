---
name: dune-analytics-api
version: 1.1.2
description: "**Dune Analytics API：用于区块链数据查询**  
该API支持以下功能：  
1. 发现数据库中的表并检查其结构；  
2. 执行或刷新Dune查询；  
3. 优化针对Solana/EVM区块链的SQL查询性能；  
4. 区分`dex.trades`与`dex_aggregator.trades`数据类型；  
5. 操作Solana交易并解析相关日志；  
6. 管理查询参数及查询结果；  
7. 将CSV/NDJSON格式的数据上传至Dune数据库；  
8. 根据合约地址查找已解码的表数据；  
9. 搜索Dune相关的文档资料。  
**触发事件包括：**  
- Dune查询的执行；  
- 区块链数据的更新；  
- DEX交易的发生；  
- Solana交易的完成；  
- 在链上的数据分析操作；  
- 查询性能的优化；  
- 数据的上传；  
- 表结构的发现；  
- 合约地址的查询；  
- 已解码表数据的获取；  
- Dune文档的搜索。"
homepage: https://github.com/LZ-Web3/dune-analytics-api-skills
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      bins:
        - python3
      env:
        - DUNE_API_KEY
    primaryEnv: DUNE_API_KEY
    files:
      - "references/*"
---
# Dune Analytics API

这是一项通过[Dune Analytics](https://dune.com) API查询和分析区块链数据的技能。

## 设置

```bash
pip install dune-client
```

请通过环境变量、`.env`文件或代理配置来设置`DUNE_API_KEY`。

## ⚠️ 使用规则

1. **在编写SQL之前阅读相关文档** — 在编写任何查询之前，请先选择并阅读相关的参考文件（参见[参考文档选择](#reference-selection)）。请勿跳过此步骤。
2. **优先使用私有查询** — 先尝试设置`is_private=True`。如果失败（适用于免费计划），则使用公共查询，并通知用户。
3. **避免重复创建查询** — 除非明确要求创建新的查询，否则请重用或更新现有的查询。
4. **更新前请确认** — 在修改现有查询之前，请先征得用户的同意。
5. **记录使用情况** — 每次执行查询后，请记录所消耗的信用额度。详情请参见[query-execution.md](references/query-execution.md#credits-tracking)。

## 参考文档选择

**在编写任何SQL之前，请根据您的任务选择相应的参考文档：**

| 任务内容 | 需要阅读的参考文档 |
|-----------------|-------------------|
| 查找表格/检查架构/发现协议 | [table-discovery.md](references/table-discovery.md) |
| 根据合约地址查找解码后的表格 | [table-discovery.md](references/table-discovery.md#search-tables-by-contract-address) |
| 查找Dune的文档/指南/示例 | [table-discovery.md](references/table-discovery.md#search-dune-documentation) |
| 钱包/地址追踪/路由器识别 | [wallet-analysis.md](references/wallet-analysis.md) |
| 表格选择/常用表格名称 | [common-tables.md](references/common-tables.md) |
| SQL性能/复杂连接/数组操作 | [sql-optimization.md](references/sql-optimization.md) |
| API调用/执行/缓存/参数 | [query-execution.md](references/query-execution.md) |
| 将CSV/NDJSON数据上传到Dune | [data-upload.md](references/data-upload.md) |

如果您的任务涉及多个类别，请阅读**所有**相关的文档。不要猜测表格名称或查询模式——这些参考文档中包含了本概述中未涵盖的关键细节（例如，专门的表格、最佳实践等）。

## 快速入门

```python
from dune_client.client import DuneClient
from dune_client.query import QueryBase
import os

client = DuneClient(api_key=os.environ['DUNE_API_KEY'])

# Execute a query
result = client.run_query(query=QueryBase(query_id=123456), performance='medium', ping_frequency=5)
print(f"Rows: {len(result.result.rows)}")

# Get cached result (no re-execution)
result = client.get_latest_result(query_id=123456)

# Get/update SQL
sql = client.get_query(123456).sql
client.update_query(query_id=123456, query_sql="SELECT ...")

# Upload CSV data (quick, overwrites existing)
client.upload_csv(
    data="col1,col2\nval1,val2",
    description="My data",
    table_name="my_table",
    is_private=True
)

# Create table + insert (supports append)
client.create_table(
    namespace="my_user",
    table_name="my_table",
    schema=[{"name": "col1", "type": "varchar"}, {"name": "col2", "type": "double"}],
    is_private=True
)
import io
client.insert_data(
    namespace="my_user",
    table_name="my_table",
    data=io.BytesIO(b"col1,col2\nabc,1.5"),
    content_type="text/csv"
)
```

## 订阅等级

| 方法 | 描述 | 计划 |
|--------|-------------|------|
| `run_query` | 执行保存的查询（支持`{{param}}`） | 免费 |
| `run_sql` | 直接执行SQL（不带参数） | 需付费 |

## 关键概念

### `dex.trades` 与 `dex_aggregator.trades`

| 表格 | 使用场景 | 数据量 |
|-------|----------|--------|
| `dex.trades` | 每个池的分析 | 数据量可能被夸大约30%（因为多次计算了多跳交易） |
| `dex_aggregator.trades` | 用户/钱包分析 | 数据更准确 |

> ⚠️ **对于钱包/地址分析**，请使用`dex_aggregator.trades`，并使用`tx_to`字段与`dune.lz_web3.dataset_crypto_wallet.router`中的路由器地址进行匹配。**不要**使用`labels.all`字段进行钱包路由器查询。详细模式请参见[wallet-analysis.md](references/wallet-analysis.md)。

Solana没有`dex_aggregator_solana.trades`表格。请通过`tx_id`字段来去重数据：
```sql
SELECT tx_id, MAX(amount_usd) as amount_usd
FROM dex_solana.trades
GROUP BY tx_id
```

### 数据更新频率

| 数据类型 | 更新延迟 | 示例 |
|-------|-------|---------|
| 原始数据 | < 1分钟 | `ethereum.transactions`, `solana.transactions` |
| 解码后的数据 | 15-60秒 | `uniswap_v3_ethereum.evt_Swap` |
| 经过处理的数据 | 约1小时以上 | `dex.trades`, `dex_solana.trades` |

为了确保数据的完整性，请在UTC时间12:00之后查询前一天的数据。

## 参考文档

详细文档存储在`references/`目录中：

| 文件 | 描述 |
|------|-------------|
| [table-discovery.md](references/table-discovery.md) | 表格查找：按名称搜索表格、检查架构/列、列出架构并上传数据 |
| [query-execution.md](references/query-execution.md) | API使用模式：执行查询、更新数据、缓存、多日数据获取、信用额度跟踪、子查询 |
| [common-tables.md](references/common-tables.md) | 常用表格的快速参考：原始数据、解码后的数据、经过处理的数据、社区数据 |
| [sql-optimization.md](references/sql-optimization.md) | SQL优化：公共表表达式（CTE）、连接策略、数组操作、分区修剪 |
| [wallet-analysis.md](references/wallet-analysis.md) | 钱包分析：Solana/EVM相关查询、多链数据聚合、费用分析 |
| [data-upload.md](references/data-upload.md) | 数据上传：CSV/NDJSON格式的数据上传、创建表格、插入数据、管理表格、信用额度管理 |