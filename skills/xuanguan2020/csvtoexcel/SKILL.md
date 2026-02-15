---
name: csv-to-excel
description: "将 CSV 文件转换为格式规范的 Excel 工作簿，支持中文字符、自动格式设置以及多工作表功能。适用于以下场景：  
1. 将单个 CSV 文件转换为 Excel 文件；  
2. 将多个 CSV 文件合并为一个包含多个工作表的 Excel 文件；  
3. 为 CSV 数据添加标题、边框，并自动调整列宽；  
4. 处理 CSV 文件中的中文或其他非 ASCII 字符；  
5. 从 CSV 数据生成专业的 Excel 报表。"
---
# CSV 转 Excel 转换器

## 概述

该工具能够将 CSV 文件转换为 Excel 格式，支持专业的格式设置、正确的中文字符编码处理，并支持将多个 CSV 文件合并为一个包含多个工作表的 Excel 工作簿。

## 快速入门

使用 `csv_to_excel.py` 脚本进行所有转换操作：

```bash
# Single CSV to Excel
python scripts/csv_to_excel.py input.csv output.xlsx

# Multiple CSVs to one Excel (each becomes a sheet)
python scripts/csv_to_excel.py file1.csv file2.csv file3.csv --output combined.xlsx

# With custom sheet names
python scripts/csv_to_excel.py sales.csv inventory.csv --output report.xlsx --sheet-names "销售数据" "库存数据"
```

## 功能特点

### 自动编码检测
- 自动检测 CSV 文件的编码格式（UTF-8、GBK、GB2312、UTF-8-SIG）
- 确保中文字符在 Excel 中正确显示
- 无需手动指定编码方式

### 专业格式设置
- **标题行**：蓝色背景上的加粗白色文本
- **边框**：所有单元格周围都有细边框
- **列宽**：根据内容自动调整（正确处理中文字符）
- **冻结窗格**：冻结标题行以便于滚动
- **对齐方式**：标题居中显示

### 多工作表支持
- 将多个 CSV 文件合并为一个 Excel 工作簿
- 每个 CSV 文件对应一个单独的工作表
- 支持自定义工作表名称
- 工作表名称默认为 CSV 文件名（最多 31 个字符）

## 常见使用场景

### 场景 1：单个文件转换
用户需求：“将这个 data.csv 文件转换为 Excel 格式”

```bash
python scripts/csv_to_excel.py data.csv data.xlsx
```

### 场景 2：多个文件合并为多工作表 Excel
用户需求：“将这些 CSV 文件合并成一个 Excel 文件，每个文件对应一个工作表”

**输出结果**：`report.xlsx`，包含 3 个工作表，分别命名为 “sales_2024”、“sales_2025” 和 “inventory”

### 场景 3：自定义工作表名称
用户需求：“使用这些 CSV 文件创建一个 Excel 文件，并为工作表设置中文名称”

```bash
python scripts/csv_to_excel.py q1.csv q2.csv q3.csv q4.csv --output 年度报告.xlsx --sheet-names "第一季度" "第二季度" "第三季度" "第四季度"
```

### 场景 4：处理中文内容
用户需求：“这个 CSV 文件包含中文文本，但在 Excel 中显示为乱码”

脚本会自动检测编码并正确处理中文字符：
```bash
python scripts/csv_to_excel.py 中文数据.csv 输出.xlsx
```

## 技术细节

### 编码支持
脚本按以下顺序尝试检测编码：
1. UTF-8
2. GBK（Windows 系统常用的中文编码）
3. GB2312（简体中文编码）
4. UTF-8-SIG（带 BOM 的 UTF-8 编码）
5. Latin1（备用编码）

### CSV 格式检测
- 自动识别分隔符（逗号、分号、制表符等）
- 支持带引号的字段
- 支持多种 CSV 格式

### 列宽计算
- 中文字符计为 2 个宽度单位
- ASCII 字符计为 1 个宽度单位
- 列宽最大限制为 50 个单位，以保持良好的可读性
- 为视觉效果添加 2 个单位的边距

## 所需依赖库

该脚本依赖于 `openpyxl` 库：

```bash
pip install openpyxl
```

## 常见问题及解决方法

**问题**：中文字符仍然显示为乱码
- **解决方法**：CSV 文件可能使用了特殊的编码格式。可以先使用文本编辑器将文件转换为 UTF-8 格式。

**问题**：工作表名称错误
- **解决方法**：Excel 工作表名称长度不能超过 31 个字符。脚本会自动截断名称，但也可以手动指定更短的名称。

**问题**：生成了空白工作表
- **解决方法**：请确保 CSV 文件不为空且格式正确。

**问题**：脚本无法找到
- **解决方法**：请从技能目录中运行脚本，或使用完整路径：`python .kiro/skills/csv-to-excel/scripts/csv_to_excel.py`