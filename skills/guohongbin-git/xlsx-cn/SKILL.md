---
name: xlsx-cn
description: "Excel表格处理 | Excel电子表格处理：创建、读取、编辑Excel文件；支持公式、图表和数据分析功能。  
关键词：Excel、表格、xlsx格式。"
metadata:
  openclaw:
    emoji: 📊
    fork-of: "https://github.com/anthropics/skills"
---
# 输出要求

## 所有 Excel 文件

### 专业字体
- 除非用户另有指示，否则所有交付成果均应使用一致的专业字体（例如 Arial、Times New Roman）。

### 全部公式无误
- 每个 Excel 模型在交付时必须确保没有任何公式错误（如 #REF!、#DIV/0!、#VALUE!、#N/A、#NAME?）。

### 保留现有模板（在更新模板时）
- 在修改文件时，必须仔细研究并完全遵循现有的格式、样式和规范；
- 不要对已有固定格式的文件强加标准化格式；
- 现有模板的规定优先于本指南。

## 财务模型

### 颜色编码标准
- 除非用户另有说明或模板已有规定：

#### 行业标准的颜色约定：
- **蓝色文本（RGB: 0,0,255）**：硬编码的输入值以及用户需要根据不同情景进行修改的数字；
- **黑色文本（RGB: 0,0,0）**：所有公式和计算结果；
- **绿色文本（RGB: 0,128,0）**：引用同一工作簿内其他工作表的链接；
- **红色文本（RGB: 255,0,0）**：指向其他外部文件的链接；
- **黄色背景（RGB: 255,255,0）**：需要特别注意的关键假设或需要更新的单元格。

### 数字格式标准

#### 必须遵循的格式规则：
- **年份**：以文本字符串格式显示（例如 "2024" 而不是 "2,024"）；
- **货币**：使用 $#,##0 格式；在标题中必须明确标注单位（例如 "收入（$mm）"）；
- **零值**：使用数字格式将所有零显示为 "-"，包括百分比（例如 "$#,##0;($#,##0);-"）；
- **百分比**：默认显示为 0.0% 的格式（保留一位小数）；
- **倍数**：对于估值倍数（如 EV/EBITDA、P/E）使用 0.0x 的格式；
- **负数**：使用括号表示（例如 123 而不是 -123）。

### 公式编写规则

#### 假设值的放置
- 将所有假设值（增长率、利润率、倍数等）放在单独的假设单元格中；
- 在公式中使用单元格引用，而不是硬编码的值；
- 例如：使用 =B5*(1+$B$6）而不是 =B5*1.05。

#### 公式错误预防
- 验证所有单元格引用是否正确；
- 检查范围中的错误（例如数值偏移）；
- 确保所有预测期间的公式保持一致；
- 使用边界情况（零值、负数）进行测试；
- 验证是否存在意外的循环引用。

#### 硬编码值的文档要求
- 在相关单元格中添加注释（如果位于表格末尾）；格式如下：“来源：[系统/文档]，[日期]，[具体引用]，[如适用请提供 URL]”；
- 例如：
  - “来源：公司 2024 年度报告（10-K 文件），第 45 页，收入说明，[SEC EDGAR URL]”；
  - “来源：公司 2025 年第二季度报告（10-Q 文件），附件 99.1，[SEC EDGAR URL]”；
  - “来源：Bloomberg 终端，2025 年 8 月 15 日，AAPL 美国股票”；
  - “来源：FactSet，2025 年 8 月 20 日，共识预测屏幕”。

# XLSX 文件的创建、编辑与分析

## 概述
用户可能会要求您创建、编辑或分析 .xlsx 文件的内容。您可以使用不同的工具和工作流程来完成这些任务。

## 重要要求

**重新计算公式需要安装 LibreOffice**：您需要确保已安装 LibreOffice，以便使用 `scripts/recalc.py` 脚本重新计算公式值。该脚本在首次运行时会自动配置 LibreOffice，即使在限制 Unix 套接字的沙箱环境中也能正常工作（由 `scripts/office/soffice.py` 处理）。

## 数据的读取与分析

### 使用 pandas 进行数据分析
- 使用 `pandas` 进行数据分析、数据可视化及基本操作，它提供了强大的数据操作功能：

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Excel 文件的工作流程

## 关键要求：使用公式，而非硬编码的值
**始终使用 Excel 公式，而不是在 Python 中计算数值并硬编码它们**。这样可以确保电子表格保持动态性和可更新性。

### ❌ 错误做法 - 硬编码计算结果
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### ✅ 正确做法 - 使用 Excel 公式
```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

这适用于所有计算——总和、百分比、比率、差异等。当源数据发生变化时，电子表格应能够自动重新计算。

## 常见的工作流程
1. **选择工具**：使用 pandas 处理数据，使用 openpyxl 处理公式和格式；
2. **创建/加载**：创建新的工作簿或加载现有文件；
3. **修改**：添加/编辑数据、公式和格式；
4. **保存**：将更改写入文件；
5. **重新计算公式（如果使用公式，则必须执行此步骤）**：使用 `scripts/recalc.py` 脚本；
   ```bash
   python scripts/recalc.py output.xlsx
   ```
6. **验证并修复错误**：
   - 该脚本会返回包含错误详情的 JSON 数据；
   - 如果 `status` 为 `errors_found`，请查看 `error_summary` 以获取具体的错误类型和位置；
   - 修复发现的错误并重新计算；
   - 常见需要修复的错误包括：
     - `#REF!`：无效的单元格引用；
     - `#DIV/0!`：除数为零；
     - `#VALUE!`：公式中的数据类型错误；
     - `#NAME?`：未识别的公式名称。

### 创建新的 Excel 文件
```python
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### 编辑现有的 Excel 文件
```python
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## 重新计算公式
由 openpyxl 创建或修改的 Excel 文件中的公式以字符串形式存在，而非计算结果。请使用提供的 `scripts/recalc.py` 脚本来重新计算公式：

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

示例：
```bash
python scripts/recalc.py output.xlsx 30
```

该脚本的功能包括：
- 在首次运行时自动设置 LibreOffice 宏；
- 重新计算所有工作表中的公式；
- 检查所有单元格中的错误（如 #REF!、#DIV/0! 等）；
- 返回包含详细错误位置和数量的 JSON 数据；
- 该脚本支持 Linux 和 macOS 系统。

## 公式验证检查清单
- 快速检查以确保公式正确运行：

### 必须进行的验证
- [ ] **测试 2-3 个示例引用**：在构建完整模型之前，验证它们是否能获取正确的值；
- [ ] **列映射**：确认 Excel 列的对应关系（例如，第 64 列对应 BL 而不是 BK）；
- [ ] **行索引**：记住 Excel 的行是从 1 开始计数的（DataFrame 的第 5 行对应 Excel 的第 6 行）。

### 常见问题
- [ ] **处理空值**：使用 `pd.notna()` 检查空值；
- [ ] **数据位置**：财务数据通常位于第 50 列及以后的列；
- [ ] **多重匹配**：查找所有匹配项，而不仅仅是第一个；
- [ ] **除数为零**：在公式中使用 `/` 之前检查分母是否为零；
- [ ] **引用错误**：确认所有单元格引用都指向正确的单元格；
- [ ] **跨工作表引用**：使用正确的格式（例如 Sheet1!A1）来链接不同工作表。

### 公式测试策略
- [ ] **从小范围开始**：先在 2-3 个单元格上测试公式，然后再全面应用；
- [ ] **验证依赖关系**：检查公式中引用的所有单元格是否存在；
- [ ] **测试边界情况**：包括零值、负数和非常大的数值。

### 解释 `scripts/recalc.py` 的输出结果
该脚本会返回包含错误详情的 JSON 数据：
```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## 最佳实践

### 库的选择
- **pandas**：最适合数据分析和批量操作，以及简单的数据导出；
- **openpyxl**：最适合复杂的格式设置、公式处理以及 Excel 的特定功能。

### 使用 openpyxl 时需要注意的事项
- 单元格索引是从 1 开始的（例如，第 1 行对应 A1 单元格）；
- 使用 `data_only=True` 读取计算结果：`load_workbook('file.xlsx', data_only=True)`；
- **警告**：如果使用 `data_only=True` 打开文件后再次保存，公式将被替换为实际数值并永久丢失；
- 对于大型文件：使用 `read_only=True` 仅读取数据，或使用 `write_only=True` 仅写入数据；
- 公式会被保留但不会被计算——请使用 `scripts/recalc.py` 来更新数值。

### 使用 pandas 时需要注意的事项
- 明确指定数据类型以避免类型推断问题：`pd.read_excel('file.xlsx', dtype={'id': str})`；
- 对于大型文件，可以仅读取特定列：`pd.read_excel('file.xlsx', usecols=['A', 'C', 'E']`；
- 正确处理日期格式：`pd.read_excel('file.xlsx', parse_dates=['date_column'])`。

## 代码风格指南
**重要提示**：在为 Excel 操作编写 Python 代码时：
- 代码应简洁明了，避免不必要的注释和冗余操作；
- 避免使用冗长的变量名和多余的代码语句；
- 对于包含复杂公式或重要假设的单元格，添加注释；
- 为硬编码的值标注数据来源；
- 为关键计算和模型部分添加说明。