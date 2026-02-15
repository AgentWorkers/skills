---
name: appraisal-archive-search
description: >
  Scan, index, and search a directory of archived appraisal reports.
  Converts .docx narratives to searchable markdown, builds a master index
  with property metadata (address, type, value, date, client, county,
  appraiser, purpose), and searches the archive by filters or keywords.
  Use when: (1) setting up or updating an appraisal archive, (2) finding
  past appraisals by property type, location, date, or value range,
  (3) finding boilerplate language or narrative examples for a new
  assignment, (4) referencing similar past work before starting a report.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["python3", "npx"] },
      },
  }
---

# 评估档案搜索

包含三个脚本：**scan**（将.docx文件转换为.md格式）、**build index**（提取元数据）和**search**（通过过滤器/关键词进行查询）。完全不依赖pip包，仅使用Python的标准库以及`npx mammoth`工具进行文件转换。

## 扫描档案

将.docx格式的评估报告转换为markdown格式。脚本会遍历包含年度档案的文件夹，并优先处理名为`NARRATIVE/`的子文件夹。

```bash
python3 scripts/scan_archive.py --archive-path /path/to/archives --output-path /path/to/md-output
```

可选参数：
- `--years 2020-2024`：指定需要扫描的年份范围
- `--force`：强制重新转换已存在的.md文件
输出结果：每个档案文件夹会生成一个对应的.md文件。

## 构建索引

从转换后的.md文件中提取元数据，并将其保存到`INDEX.md`和`INDEX.json`文件中。

```bash
python3 scripts/build_index.py --md-path /path/to/md-output
```

提取的元数据包括：
- 作业编号（job_number）
- 房产地址（property_address）
- 房产类型/子类型（property_type/subtype）
- 客户信息（client）
- 生效日期（effective_date）
- 评估价值（concluded_value）
- 土地面积（land_area）
- 郡县名称（county）
- 评估师信息（appraiser）
- 评估目的（purpose）
- 使用的评估方法（approaches_used）
有关正则表达式模式的详细信息，请参阅`references/field-extraction.md`文件。

## 查询

可以对索引进行查询。所有查询参数都是可选的，并且可以组合使用。

```bash
python3 scripts/search_archive.py --index /path/to/INDEX.json --type commercial --county Jefferson
```

| 参数 | 说明 |
|------|---------|
| `--type` | `commercial`（商业地产）、`residential`（住宅地产）、`land`（土地）、`agricultural`（农业用地）、`industrial`（工业用地） |
| `--subtype` | `office`（办公用地）、`sfr`（单户住宅）、`ranch`（牧场）、`conservation-easement`（保护地役权） |
| `--county` | 需要查询的郡县名称（例如：Jefferson、Denver、Boulder） |
| `--purpose` | 评估目的（例如：condemnation、estate、lending、litigation） |
| `--date-from` / `--date-to` | 时间范围（例如：2022-01-01） |
| `--value-min` / `--value-max` | 评估价值范围（例如：500000） |
| `--keyword` | 需要搜索的关键词（例如：“conservation easement”） |
| `--limit` | 查询结果数量限制（默认为10条） |

## 示例

查询结果会按照关键词的相关性和时间顺序进行排序（最新结果排在最前面），并以markdown表格的形式输出。