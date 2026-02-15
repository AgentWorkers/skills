---
name: parallel-enrichment
description: "通过 Parallel API 进行批量数据增强。该功能可将从网页获取的字段（如 CEO 名称、融资信息、联系方式等）添加到公司、人员或产品的列表中，适用于丰富 CSV 文件或内联数据。"
homepage: https://parallel.ai
---

# 并行数据增强（Parallel Data Enrichment）

该功能用于批量处理数据，将从网络获取的字段添加到公司、人员或产品的列表中。请用自然语言描述您的需求。

## 使用场景

当用户提出以下请求时，可以使用此功能：
- “用……丰富这个列表”，“在……中添加CEO的名字”，“查找这些公司的融资信息……”
- “查询……的联系方式”，“获取……的LinkedIn个人资料”
- 对CSV文件或列表进行批量数据操作
- 向现有数据集中添加网络获取的列
- 客户信息补充、公司研究、产品对比

## 快速入门

```bash
# Inline data
parallel-cli enrich run \
  --data '[{"company": "Google"}, {"company": "Microsoft"}]' \
  --intent "CEO name and founding year" \
  --target output.csv

# CSV file
parallel-cli enrich run \
  --source-type csv --source input.csv \
  --target output.csv \
  --intent "CEO name and founding year"
```

## 命令行接口（CLI）参考

### 基本用法

```bash
parallel-cli enrich run [options]
```

**注意：** `enrich` 命令没有 `--json` 参数。处理结果会直接写入目标文件。

### 常用参数

| 参数 | 说明 |
|------|-------------|
| `--data "<json>"` | 进行处理的JSON记录数组 |
| `--source-type csv` | 数据源文件类型 |
| `--source <path>` | 输入CSV文件路径 |
| `--target <path>` | 输出CSV文件路径 |
| `--source-columns "<json>"` | 输入列的描述 |
| `--enriched-columns "<json>"` | 指定输出列 |
| `--intent "<description>"` | 指定需要查找的信息的描述（用自然语言） |
| `--processor <tier>` | 处理层级（见下表） |

### 处理层级

| 处理层级 | 适用场景 |
|-----------|----------|
| `lite-fast` | 简单查询 |
| `base-fast` | 基本数据增强 |
| `core-fast` | 标准数据增强 |
| `pro-fast` | 深度数据增强（默认） |
| `ultra-fast` | 复杂的多源数据增强 |

### 示例

**内联数据增强：**
```bash
parallel-cli enrich run \
  --data '[{"company": "Stripe"}, {"company": "Square"}, {"company": "Adyen"}]' \
  --intent "CEO name, headquarters city, and latest funding round" \
  --target ./companies-enriched.csv
```

**CSV文件数据增强：**
```bash
parallel-cli enrich run \
  --source-type csv \
  --source ./leads.csv \
  --target ./leads-enriched.csv \
  --source-columns '[{"name": "company_name", "description": "Company name"}]' \
  --intent "Find CEO name, company size, and LinkedIn company page URL"
```

**指定输出列：**
```bash
parallel-cli enrich run \
  --data '[{"name": "Sam Altman"}, {"name": "Satya Nadella"}]' \
  --source-columns '[{"name": "name", "description": "Person full name"}]' \
  --enriched-columns '[
    {"name": "current_company", "description": "Current company/employer"},
    {"name": "title", "description": "Current job title"},
    {"name": "twitter", "description": "Twitter/X handle"}
  ]' \
  --target ./people-enriched.csv
```

**使用AI推荐列：**
```bash
# First, get AI suggestions
parallel-cli enrich suggest \
  --source-type csv \
  --source ./companies.csv \
  --intent "competitor analysis data"

# Then run with suggested columns
parallel-cli enrich run \
  --source-type csv \
  --source ./companies.csv \
  --target ./companies-analysis.csv \
  --intent "competitor analysis: market position, key products, recent news"
```

## 最佳提示方式

### 指定需求描述

请用1-2句话描述：
- 您希望添加的具体字段
- 数据的背景信息（例如：B2B公司、科技初创企业等）
- 任何限制条件（例如：最新数据、特定数据源）

**示例：**
```
--intent "Find CEO name, total funding raised, and number of employees for B2B SaaS companies"
```

**示例（描述不当）：**
```
--intent "Find stuff about these companies"
```

### 数据源列描述

使用 `--source-columns` 时，请提供相关背景信息：

```json
[
  {"name": "company", "description": "Company name, may include Inc/LLC suffix"},
  {"name": "website", "description": "Company website URL, may be partial"}
]
```

## 输出格式

CLI的输出包括：
- 用于跟踪处理进度的监控URL
- 处理过程中每行的状态更新
- 最终处理结果写入目标CSV文件

目标CSV文件包含：
- 来自源文件的所有原始列
- 指定的新增强列
- 一个 `_parallel_status` 列，用于指示每行的处理结果（成功/失败）

## 结果处理

数据增强完成后：
1. 报告处理过的行数
2. 预览前几行：`head -6 output.csv`
3. 分享输出文件的完整路径
4. 注意处理失败的行

## 配置文件

对于复杂的数据增强任务，请使用YAML格式的配置文件：

```yaml
# enrich-config.yaml
source:
  type: csv
  path: ./input.csv
  columns:
    - name: company_name
      description: "Company legal name"
    - name: website
      description: "Company website URL"

target:
  type: csv
  path: ./output.csv

enriched_columns:
  - name: ceo_name
    description: "Current CEO full name"
  - name: employee_count
    description: "Approximate number of employees"
  - name: funding_total
    description: "Total funding raised in USD"

processor: pro-fast
```

然后运行命令：
```bash
parallel-cli enrich run enrich-config.yaml
```

## 数据量过大？

对于处理大量数据的情况，可以先保存结果，再使用 `sessions_spawn` 命令启动子代理进行后续处理：

```bash
parallel-cli enrich run --source-type csv --source input.csv --target /tmp/enriched-<topic>.csv --intent "..."
```

之后再启动子代理进行数据处理：
```json
{
  "tool": "sessions_spawn",
  "task": "Read /tmp/enriched-<topic>.csv and summarize the results. Report row count, success rate, and preview first 5 rows.",
  "label": "enrich-summary"
}
```

## 错误处理

| 错误代码 | 含义 |
|-----------|---------|
| 0 | 操作成功 |
| 1 | 发生意外错误（网络问题或解析错误） |
| 2 | 参数无效 |
| 3 | API错误（非2xx状态码） |

**常见问题：**
- **数据行处理失败**：检查输出文件中的 `_parallel_status` 列
- **超时**：尝试分批处理数据或选择较低的处理层级
- **速率限制**：在处理大量数据时适当增加延迟

## 先决条件

1. 在 [parallel.ai](https://parallel.ai) 获取API密钥
2. 安装相应的CLI工具：

```bash
curl -fsSL https://parallel.ai/install.sh | bash
export PARALLEL_API_KEY=your-key
```

## 参考资料

- [API文档](https://docs.parallel.ai)
- [数据增强API参考](https://docs.parallel.ai/api-reference/enrichment)