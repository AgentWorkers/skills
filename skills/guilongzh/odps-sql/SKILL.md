---
name: "ODPS (MaxCompute) Data Query"
description: >
  当用户需要查询、分析或探索阿里云 ODPS（MaxCompute）中的数据时，请使用此技能。  
  该技能通过运行 `odps_helper.py` 命令行脚本来执行 SQL 查询、列出表格以及检查表格结构。  
  适用于以下请求：查询 ODPS 数据、列出 MaxCompute 表格、在 ODPS 上运行 SQL 语句、检查表格结构、分析存储在 ODPS 中的业务数据，或任何涉及阿里云 MaxCompute/ODPS 的数据探索任务。
metadata:
  { "openclaw": { "requires": { "bins": ["python"], "env": ["ALIYUN_ACCESS_ID", "ALIYUN_ACCESS_SECRET", "ALIYUN_PROJECT_NAME", "ALIYUN_END_POINT"] } } }
---
## 设置（仅限首次使用）

1. 复制凭证模板并填写您的信息：
   ```bash
   cd mcp-odps/
   cp config.example.env .env
   # Edit .env with your Alibaba Cloud credentials
   ```

2. 激活您的 Python 环境并安装所需依赖项：
   ```bash
   # conda users:
   conda activate <your-env>
   # venv users:
   source .venv/bin/activate

   pip install pyodps
   ```

## 执行命令

首先激活您的 Python 环境，然后从项目根目录运行所有命令：

```bash
SCRIPT=mcp-odps/scripts/odps_helper.py
```

### 列表表格

```bash
python $SCRIPT --list-tables
```

**按名称过滤**：
```bash
python $SCRIPT --list-tables --pattern <keyword>
```

### 获取表格结构

```bash
python $SCRIPT --describe <table_name>
```

### 执行 SQL 查询

```bash
python $SCRIPT --query "<SQL statement>" [--limit <n>]
```

默认查询结果限制为 100 行。

## 数据任务的工作流程

当用户询问 ODPS 数据时，请遵循以下步骤：

1. **发现** — 如果表格名称未知，请运行 `--list-tables --pattern <关键词>` 来查找它。
2. **检查** — 运行 `--describe <表格>` 以了解列、类型和分区结构。
3. **查询** — 构建 SQL 语句并运行 `--query`。对于已分区的表格，请务必添加分区过滤条件（`WHERE dt = '...'`），以避免全表扫描。
4. **展示结果** — 为用户清晰地汇总查询结果。

## ODPS SQL 与标准 SQL 的主要区别

| 特性 | 标准 SQL | ODPS SQL |
|---------|-------------|----------|
| 字符串连接 | `a \|\| b` | `CONCAT(a, b)` |
| 当前时间 | `NOW()` | `GETDATE()` |
| 空值合并 | `IFNULL(x, y)` | `NVL(x, y)` |
| 正则表达式匹配 | `REGEXP` | `RLIKE` |
| 日期字面量 | `'2024-01-01'` | `TO_DATE('2024-01-01','yyyy-mm-dd')` |

对于已分区的表格，**必须** 使用分区过滤条件（分区列通常为 `dt`）：
```sql
SELECT * FROM table_name WHERE dt = '2024-01-01' LIMIT 100
```

有关完整的 SQL 参考，请参阅 `mcp-odps/references/odps_sql_guide.md`。

## 错误处理

- 如果出现 “`pyodps` 未找到” 的错误，请在设置步骤中运行安装命令。
- 如果凭证信息缺失，请检查 `mcp-odps/.env` 文件是否存在，并确保所有四个字段都已填写。
- 如果找不到表格，请使用 `--list-tables --pattern` 来查找正确的表格名称。
- 如果出现 SQL 语法错误，请参考上述 ODPS SQL 与标准 SQL 的区别；避免使用 MySQL/PostgreSQL 特有的语法。