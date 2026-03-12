---
name: dune-analytics-api
version: 2.0.0
description: "**Dune Analytics API**：用于查询、分析及上传区块链数据的专业工具。无论用户提到“Dune”、“链上数据”、“区块链分析”、“代币交易量”、“去中心化交易所（DEX）活动”、“钱包追踪”、“Solana/EVM交易分析”或任何与加密货币数据相关的内容，均可使用此API。此外，该API还适用于以下场景：运行或创建Dune查询、查找区块链表结构和数据模式、将CSV/NDJSON格式的数据上传至Dune平台、优化DuneSQL（Trino）中的SQL查询语句、查询代币价格或交易对信息、分析钱包行为，以及处理与去中心化交易所交易、解码后的事件日志或原始区块链交易相关的任务。
**触发条件**：  
- Dune相关操作  
- 区块链数据相关操作  
- 链上交易相关操作  
- 代币交易量相关操作  
- Solana交易相关操作  
- 钱包分析相关操作  
- 查询优化相关操作  
- 数据上传相关操作  
- 表结构发现相关操作  
- 合同地址查询相关操作  
- 加密货币分析相关操作  
- DuneSQL相关操作"
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
      - "scripts/*"
---
# Dune Analytics API

这是一项通过[Dune Analytics](https://dune.com) API查询和分析区块链数据的技能。

## 设置

```bash
pip install dune-client
```

请通过环境变量、`.env`文件或代理配置来设置`DUNE_API_KEY`。

## 最佳实践

1. **先阅读参考资料** — 参考文件中包含了重要的表名、常见的错误模式以及仅从表名无法直接了解的链特定问题。在编写SQL之前阅读相应的参考资料，可以避免一些常见的错误，例如将`dex.trades`用于钱包分析（这会导致交易量被夸大约30%），或者忽略Solana的数据去重要求。

2. **优先使用私有查询** — 使用`is_private=True`创建查询可以保持用户工作区的整洁，并避免污染公共的Dune命名空间。如果私有查询不可用（受免费计划限制），则可以使用公共查询，并告知用户这一情况。

3. **先重用现有查询** — Dune会根据每次执行收取费用。重用或更新现有查询可以避免不必要的重复操作，并便于追踪费用使用情况。只有在用户明确要求时才创建新的查询。

4. **更新前先确认** — 修改现有查询的SQL可能会导致数据丢失（因为默认情况下不会保存旧版本）。快速确认可以防止覆盖用户可能希望保留的数据。

5. **追踪费用使用情况** — 每次执行查询都会根据性能等级和扫描的数据量产生费用。记录费用使用情况有助于用户管理预算。详情请参阅[query-execution.md](references/query-execution.md#credits-tracking)。

## 脚本 — 常见操作

对于常见的操作，可以使用`scripts/`目录中的脚本来避免重复编写代码。所有脚本都会自动从环境变量中读取`DUNE_API_KEY`。

| 脚本 | 命令 | 功能 |
|--------|---------|-------------|
| `dune_query.py` | `execute --query-id ID` | 执行保存的查询（支持`--params`、`--performance`、`--format`参数） |
| `dune_query.py` | `get_latest --query-id ID` | 获取缓存结果（无需重新执行） |
| `dune_query.py` | `get_sql --query-id ID` | 打印查询的SQL语句 |
| `dune_query.py` | `update_sql --query-id ID --sql "..."` | 更新查询的SQL语句 |
| `dune_discover.py` | `search --keyword "uniswap"` | 根据关键词搜索表格 |
| `dune_discover.py` | `schema --table "dex.trades"` | 显示表格的列和类型 |
| `dune_discover.py` | `list_schemas --namespace "uniswap_v3"` | 列出指定命名空间内的表格 |
| `dune_discover.py` | `contract --address "0x..."` | 根据合约地址查找解码后的表格 |
| `dune_discover.py` | `docs --keyword "dex"` | 搜索Dune的文档 |
| `dune_upload.py` | `upload_csv --file data.csv --table-name tbl` | 快速上传CSV文件（会覆盖现有数据） |
| `dune_upload.py` | `create_table --table-name tbl --namespace ns --schema '[...]'` | 使用指定模式创建表格 |
| `dune_upload.py` | `insert --file data.csv --table-name tbl --namespace ns` | 向现有表格中插入数据 |

**示例：**
```bash
# Execute query with parameters
python scripts/dune_query.py execute --query-id 123456 --params '{"token":"ETH"}' --format table

# Upload a CSV privately
python scripts/dune_upload.py upload_csv --file wallets.csv --table-name my_wallets --private
```

## 参考资料选择

**在编写任何SQL代码之前，请根据你的任务选择正确的参考文件：**

| 任务内容 | 需要阅读的参考文件 |
|-----------------|-------------------|
| 查找表格/检查表结构/发现协议 | [table-discovery.md](references/table-discovery.md) |
| 根据合约地址查找解码后的表格 | [table-discovery.md](references/table-discovery.md#search-tables-by-contract-address) |
| 搜索Dune文档/指南/示例 | [table-discovery.md](references/table-discovery.md#search-dune-documentation) |
| 钱包/地址追踪/路由器识别 | [wallet-analysis.md](references/wallet-analysis.md) |
| 表格选择/常用表名 | [common-tables.md](references/common-tables.md) |
| SQL性能/复杂连接/数组操作 | [sql-optimization.md](references/sql-optimization.md) |
| API调用/执行/缓存/参数设置 | [query-execution.md](references/query-execution.md) |
| 将CSV/NDJSON数据上传到Dune | [data-upload.md](references/data-upload.md) |

如果你的任务涉及多个类别，请阅读**所有**相关的参考文件。这些参考文件包含了本概述中未涵盖的关键细节（例如特殊表格、常见错误模式）。随意猜测表名或查询模式可能会导致隐藏的错误。

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

| 方法 | 描述 | 计划费用 |
|--------|-------------|------|
| `run_query` | 执行保存的查询（支持`{{param}}`参数） | 免费 |
| `run_sql` | 直接执行SQL语句（不支持参数） | 需额外付费 |

## 关键概念

### `dex.trades` 与 `dex_aggregator.trades` 的区别

| 表格 | 使用场景 | 交易量统计方式 |
|-------|----------|--------|
| `dex.trades` | 按池进行分析 | ⚠️ 由于多次计算多跳交易，导致交易量被夸大约30% |
| `dex_aggregator.trades` | 用户/钱包分析 | 数据更准确 |

> **为什么这很重要：** 如果你正在分析特定钱包的交易活动，并使用`dex.trades`，可能会发现交易量被夸大，因为通过聚合器进行的单次交易会被多次计入不同池的交易中。`dex_aggregator.trades`能够准确反映用户的实际交易行为——每个用户的交易只记录一行。更多详细信息请参阅[wallet-analysis.md](references/wallet-analysis.md)。

Solana没有`dex_aggregator.solana.trades`表格。可以通过`tx_id`进行数据去重：
```sql
SELECT tx_id, MAX(amount_usd) as amount_usd
FROM dex_solana.trades
GROUP BY tx_id
```

### 数据的新鲜度

| 数据类型 | 更新延迟 | 示例 |
|-------|-------|---------|
| 原始数据 | < 1分钟 | `ethereum.transactions`、`solana.transactions` |
| 解码后的数据 | 15-60秒 | `uniswap_v3_ethereum.evt_Swap` |
| 经过处理的数据 | 约1小时以上 | `dex.trades`、`dex_solana.trades` |

为了确保数据的完整性，请在**UTC时间12:00**之后查询前一天的数据。

## 参考资料

详细的文档存储在`references/`目录中：

| 文件 | 说明 |
|------|-------------|
| [table-discovery.md](references/table-discovery.md) | 表格查找：按名称搜索表格、检查表结构/列、列出表格及上传数据 |
| [query-execution.md](references/query-execution.md) | API使用指南：执行查询、更新数据、缓存、多日数据获取、费用追踪、子查询 |
| [common-tables.md](references/common-tables.md) | 常用表格的快速参考：原始数据、解码后的数据、经过处理的数据 |
| [sql-optimization.md](references/sql-optimization.md) | SQL优化：公共表表达式（CTE）、连接策略、数组操作、数据分区优化 |
| [wallet-analysis.md](references/wallet-analysis.md) | 钱包分析：Solana/EVM相关查询、跨链数据聚合、费用分析 |
| [data-upload.md](references/data-upload.md) | 数据上传：CSV/NDJSON格式的数据上传、创建表格、插入数据、管理表格、费用记录 |