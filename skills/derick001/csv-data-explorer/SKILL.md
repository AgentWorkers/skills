---
name: csv-data-explorer
description: 您可以直接在终端中使用交互式查询来探索、过滤、汇总和可视化 CSV 数据。
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python:
        - pandas
        - matplotlib
---
# CSV 数据探索器

## 功能介绍

这是一个命令行（CLI）工具，用于直接在终端中探索、分析和可视化 CSV 数据。无需离开终端，即可加载 CSV 文件、过滤数据行、计算统计信息、生成摘要以及创建基本的可视化图表。

**主要功能：**
- **加载并预览 CSV 文件**：自动检测文件的分隔符。
- **探索数据结构**：查看列、数据类型及缺失值。
- **根据条件过滤数据行**（等于、不等于、包含、正则表达式）。
- **选择列**：包含或排除特定列。
- **计算统计信息**：平均值、中位数、最小值、最大值、标准差、百分位数。
- **生成摘要**：计数、唯一值、频率分布。
- **基本可视化**：直方图、条形图、散点图（以 ASCII 或简单的终端输出形式）。
- **导出结果**：将过滤后的数据、统计信息和摘要导出为新的 CSV/JSON 文件。
- **交互式模式**：提供逐步指导的操作流程。
- **命令行模式**：支持脚本化操作以实现自动化。

## 使用场景

- 需要在不打开电子表格的情况下快速浏览 CSV 数据。
- 需要对数据进行过滤和分析以用于报告或调试。
- 需要对数据集计算基本统计信息。
- 在没有图形用户界面（GUI）工具的服务器或远程机器上工作。
- 需要在脚本中自动化 CSV 数据处理。
- 需要与团队成员共享分析结果。
- 在终端环境中教授数据分析概念。

## 使用方法

基本命令：

```bash
# Load and preview a CSV file
python3 scripts/main.py preview data.csv

# Show basic statistics
python3 scripts/main.py stats data.csv

# Filter rows where column 'age' > 30
python3 scripts/main.py filter data.csv --where "age > 30"

# Select specific columns
python3 scripts/main.py select data.csv --columns name,age,salary

# Generate histogram for a column
python3 scripts/main.py histogram data.csv --column age --bins 10

# Count unique values in a column
python3 scripts/main.py unique data.csv --column category

# Export filtered data
python3 scripts/main.py filter data.csv --where "salary > 50000" --output filtered.csv

# Interactive exploration mode
python3 scripts/main.py interactive data.csv
```

## 示例

### 示例 1：预览和基本统计信息

```bash
python3 scripts/main.py preview sales.csv --limit 10
```

输出：
```
CSV File: sales.csv (1000 rows × 5 columns)

First 10 rows:
┌─────┬────────────┬───────────┬────────┬───────────┐
│ Row │ Date       │ Product   │ Amount │ Region    │
├─────┼────────────┼───────────┼────────┼───────────┤
│ 1   │ 2024-01-01 │ Widget A  │ 150.50 │ North     │
│ 2   │ 2024-01-01 │ Widget B  │ 89.99  │ South     │
│ ... │ ...        │ ...       │ ...    │ ...       │
└─────┴────────────┴───────────┴────────┴───────────┘

Column summary:
- Date: 1000 non-null, type: datetime
- Product: 1000 non-null, type: string (5 unique values)
- Amount: 1000 non-null, type: float (min: 10.00, max: 999.99)
- Region: 1000 non-null, type: string (4 unique values)
```

### 示例 2：过滤数据并计算统计信息

```bash
python3 scripts/main.py filter sales.csv --where "Region == 'North' and Amount > 100" --stats
```

输出：
```
Filtered data: 237 rows (from 1000 total)

Statistics for filtered data:
- Count: 237
- Mean Amount: 245.67
- Median Amount: 210.50
- Min Amount: 101.00
- Max Amount: 999.99
- Standard Deviation: 145.23
```

### 示例 3：生成直方图

```bash
python3 scripts/main.py histogram sales.csv --column Amount --bins 5
```

输出（ASCII 格式）：
```
Amount Distribution (5 bins):
[10.00 - 207.99]  ████████████████████████████ 312
[208.00 - 405.99] ████████████████████ 241
[406.00 - 603.99] ██████████ 152
[604.00 - 801.99] █████ 78
[802.00 - 999.99] ███ 45
```

### 示例 4：交互式模式

交互式模式会引导您完成以下步骤：
1. 加载文件并预览数据。
2. 选择和过滤列。
3. 进行统计分析。
4. 选择可视化方式。
5. 导出结果。

## 系统要求

- Python 3.x。
- 需要 `pandas` 库来处理数据（已自动安装或通过 pip 安装）。
- 需要 `matplotlib` 库来生成可视化图表（可选，用于更复杂的图表）。

**安装缺失的依赖项：**
```bash
pip3 install pandas matplotlib
```

## 限制

- 大文件（>100MB）的处理速度可能较慢。
- 可视化效果为 ASCII 格式或简单的终端图表。
- 仅支持 CSV 格式，不支持 Excel 文件或其他格式。
- 仅提供基本统计功能，不支持高级分析。
- 不支持时间序列分析或复杂的聚合操作。
- 内存使用量会随文件大小增加而增加。
- 不支持数据库连接。
- 不支持流式处理或处理非常大的数据集。
- 可视化效果受终端功能的限制。
- 不支持地理数据或地图的可视化。
- 对格式错误的 CSV 文件的处理能力有限。
- 不提供内置的数据清洗或转换功能。
- 性能可能不如 R 或专用库等工具。

## 目录结构

该工具支持当前目录或指定路径下的 CSV 文件，无需额外的配置目录。

## 错误处理

- 对于无效的 CSV 文件，会显示包含行号的错误信息。
- 如果缺少某些列，会提示可用的列名。
- 类型转换错误会显示预期类型与实际类型之间的差异。
- 内存错误提示使用较小的文件或先进行数据过滤。
- 文件未找到时，会提示检查路径和权限。

## 贡献方式

此工具由 Skill Factory 开发。如有问题或改进建议，请通过 OpenClaw 项目进行反馈。