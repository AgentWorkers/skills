---
name: xlsx-manipulation
description: 使用 openpyxl 以编程方式创建、编辑和操作 Excel 电子表格。
author: claude-office-skills
version: "1.0"
tags: [spreadsheet, excel, xlsx, openpyxl, data]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: openpyxl
  url: https://github.com/theorchard/openpyxl
  stars: 3.8k
---

# XLSX 操作技能

## 概述

该技能允许使用 **openpyxl** 库以编程方式创建、编辑和操作 Microsoft Excel (.xlsx) 电子表格。无需手动编辑，即可制作包含公式、格式设置、图表和数据验证的专业电子表格。

## 使用方法

1. 描述您想要创建或修改的电子表格。
2. 提供数据、公式或格式要求。
3. 我将生成 openpyxl 代码并执行它。

**示例提示：**
- “创建一个包含月度跟踪信息的预算电子表格”
- “添加条件格式，以突出显示超过阈值的值”
- “根据这些数据生成类似数据透视表的汇总表”
- “创建一个包含图表和关键绩效指标 (KPI) 的仪表板”

## 领域知识

### openpyxl 基础知识
```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Fill, Border, Alignment
from openpyxl.chart import BarChart, Reference

# Create new workbook
wb = Workbook()
ws = wb.active

# Or open existing
wb = load_workbook('existing.xlsx')
ws = wb.active
```

### 工作簿结构
```
Workbook
├── worksheets (sheets/tabs)
│   ├── cells (data storage)
│   ├── rows/columns (formatting)
│   ├── merged_cells
│   └── charts
├── defined_names (named ranges)
└── styles (formatting templates)
```

### 单元格操作

#### 基本单元格操作
```python
# By cell reference
ws['A1'] = 'Header'
ws['B1'] = 42

# By row, column
ws.cell(row=1, column=3, value='Data')

# Multiple cells
ws['A1:C1'] = [['Col1', 'Col2', 'Col3']]

# Append rows
ws.append(['Row', 'Data', 'Here'])
```

#### 读取单元格内容
```python
# Single cell
value = ws['A1'].value

# Cell range
for row in ws['A1:C3']:
    for cell in row:
        print(cell.value)

# Iterate rows
for row in ws.iter_rows(min_row=1, max_row=10, min_col=1, max_col=3):
    for cell in row:
        print(cell.value)
```

### 公式
```python
# Basic formulas
ws['D1'] = '=SUM(A1:C1)'
ws['D2'] = '=AVERAGE(A2:C2)'
ws['E1'] = '=IF(D1>100,"High","Low")'

# Named ranges
from openpyxl.workbook.defined_name import DefinedName
ref = "Sheet!$A$1:$C$10"
defn = DefinedName("SalesData", attr_text=ref)
wb.defined_names.add(defn)

# Use named range
ws['F1'] = '=SUM(SalesData)'
```

### 格式设置

#### 单元格样式
```python
from openpyxl.styles import Font, Fill, PatternFill, Border, Side, Alignment

# Font
ws['A1'].font = Font(
    name='Arial',
    size=14,
    bold=True,
    italic=False,
    color='FF0000'  # Red
)

# Fill (background)
ws['A1'].fill = PatternFill(
    start_color='FFFF00',  # Yellow
    end_color='FFFF00',
    fill_type='solid'
)

# Border
thin_border = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
ws['A1'].border = thin_border

# Alignment
ws['A1'].alignment = Alignment(
    horizontal='center',
    vertical='center',
    wrap_text=True
)
```

#### 数字格式
```python
# Currency
ws['B2'].number_format = '$#,##0.00'

# Percentage
ws['C2'].number_format = '0.00%'

# Date
ws['D2'].number_format = 'YYYY-MM-DD'

# Custom
ws['E2'].number_format = '#,##0.00 "units"'
```

#### 条件格式
```python
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.styles import PatternFill

# Color scale (heatmap)
color_scale = ColorScaleRule(
    start_type='min', start_color='FF0000',
    end_type='max', end_color='00FF00'
)
ws.conditional_formatting.add('A1:A10', color_scale)

# Cell value rule
red_fill = PatternFill(start_color='FFCCCC', end_color='FFCCCC', fill_type='solid')
rule = CellIsRule(operator='greaterThan', formula=['100'], fill=red_fill)
ws.conditional_formatting.add('B1:B10', rule)
```

### 图表
```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference

# Prepare data
data = Reference(ws, min_col=2, min_row=1, max_col=3, max_row=5)
categories = Reference(ws, min_col=1, min_row=2, max_row=5)

# Bar Chart
chart = BarChart()
chart.type = "col"  # or "bar" for horizontal
chart.title = "Sales by Region"
chart.add_data(data, titles_from_data=True)
chart.set_categories(categories)
chart.shape = 4
ws.add_chart(chart, "E1")

# Line Chart
line = LineChart()
line.title = "Trend Analysis"
line.add_data(data, titles_from_data=True)
line.set_categories(categories)
ws.add_chart(line, "E15")

# Pie Chart
pie = PieChart()
pie.add_data(data, titles_from_data=True)
pie.set_categories(categories)
ws.add_chart(pie, "M1")
```

### 数据验证
```python
from openpyxl.worksheet.datavalidation import DataValidation

# Dropdown list
dv = DataValidation(
    type="list",
    formula1='"Option1,Option2,Option3"',
    allow_blank=True
)
dv.error = "Please select from list"
dv.errorTitle = "Invalid Input"
ws.add_data_validation(dv)
dv.add('A1:A100')

# Number range
dv_num = DataValidation(
    type="whole",
    operator="between",
    formula1="1",
    formula2="100"
)
ws.add_data_validation(dv_num)
dv_num.add('B1:B100')
```

### 工作表操作
```python
# Create new sheet
ws2 = wb.create_sheet("Data")
ws3 = wb.create_sheet("Summary", 0)  # At position 0

# Rename
ws.title = "Main Report"

# Delete
del wb["Sheet2"]

# Copy
source = wb["Template"]
target = wb.copy_worksheet(source)
```

### 行/列操作
```python
# Set column width
ws.column_dimensions['A'].width = 20

# Set row height
ws.row_dimensions[1].height = 30

# Hide column
ws.column_dimensions['C'].hidden = True

# Freeze panes
ws.freeze_panes = 'B2'  # Freeze row 1 and column A

# Auto-filter
ws.auto_filter.ref = "A1:D100"
```

## 最佳实践

1. **使用模板**：对于复杂的格式设置，从现有的 .xlsx 模板开始。
2. **批量操作**：尽量减少逐个单元格的操作，以提高效率。
3. **命名范围**：使用定义的名称使公式更易于理解。
4. **数据验证**：添加验证机制以防止输入错误。
5. **分阶段保存**：对于大型文件，定期进行保存。

## 常见模式

### 数据导入
```python
def import_csv_to_xlsx(csv_path, xlsx_path):
    import csv
    wb = Workbook()
    ws = wb.active
    
    with open(csv_path) as f:
        reader = csv.reader(f)
        for row in reader:
            ws.append(row)
    
    wb.save(xlsx_path)
```

### 报告模板
```python
def create_monthly_report(data, output_path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Monthly Report"
    
    # Headers
    headers = ['Date', 'Revenue', 'Expenses', 'Profit']
    ws.append(headers)
    
    # Style headers
    for col in range(1, 5):
        cell = ws.cell(1, col)
        cell.font = Font(bold=True)
        cell.fill = PatternFill('solid', fgColor='4472C4')
        cell.font = Font(bold=True, color='FFFFFF')
    
    # Data
    for row in data:
        ws.append(row)
    
    # Add totals
    last_row = len(data) + 1
    ws.cell(last_row + 1, 1, 'TOTAL')
    ws.cell(last_row + 1, 2, f'=SUM(B2:B{last_row})')
    ws.cell(last_row + 1, 3, f'=SUM(C2:C{last_row})')
    ws.cell(last_row + 1, 4, f'=SUM(D2:D{last_row})')
    
    wb.save(output_path)
```

## 示例

### 示例 1：预算跟踪器
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Budget 2024"

# Headers
months = ['Category', 'Jan', 'Feb', 'Mar', 'Q1 Total']
ws.append(months)

# Categories and data
budget_data = [
    ['Salary', 5000, 5000, 5000],
    ['Rent', -1500, -1500, -1500],
    ['Utilities', -200, -180, -220],
    ['Food', -400, -450, -380],
    ['Transport', -150, -160, -140],
    ['Entertainment', -200, -250, -200],
]

for row in budget_data:
    ws.append(row + [f'=SUM(B{ws.max_row + 1}:D{ws.max_row + 1})'])

# Total row
ws.append(['TOTAL', 
    f'=SUM(B2:B{ws.max_row})',
    f'=SUM(C2:C{ws.max_row})',
    f'=SUM(D2:D{ws.max_row})',
    f'=SUM(E2:E{ws.max_row})'
])

# Formatting
header_fill = PatternFill('solid', fgColor='366092')
header_font = Font(bold=True, color='FFFFFF')

for cell in ws[1]:
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal='center')

# Currency format
for row in ws.iter_rows(min_row=2, min_col=2, max_col=5):
    for cell in row:
        cell.number_format = '$#,##0.00'

# Column widths
ws.column_dimensions['A'].width = 15
for col in range(2, 6):
    ws.column_dimensions[get_column_letter(col)].width = 12

wb.save('budget_2024.xlsx')
```

### 示例 2：销售仪表板
```python
from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Sales Dashboard"

# Data
ws.append(['Region', 'Q1', 'Q2', 'Q3', 'Q4'])
data = [
    ['North', 150000, 165000, 180000, 195000],
    ['South', 120000, 125000, 140000, 155000],
    ['East', 180000, 190000, 210000, 225000],
    ['West', 95000, 110000, 125000, 140000],
]
for row in data:
    ws.append(row)

# Bar Chart
data_ref = Reference(ws, min_col=2, min_row=1, max_col=5, max_row=5)
cats_ref = Reference(ws, min_col=1, min_row=2, max_row=5)

bar = BarChart()
bar.type = "col"
bar.title = "Quarterly Sales by Region"
bar.add_data(data_ref, titles_from_data=True)
bar.set_categories(cats_ref)
bar.height = 10
bar.width = 15
ws.add_chart(bar, "A8")

# Pie Chart - Q4 breakdown
pie_data = Reference(ws, min_col=5, min_row=1, max_row=5)
pie = PieChart()
pie.title = "Q4 Market Share"
pie.add_data(pie_data, titles_from_data=True)
pie.set_categories(cats_ref)
ws.add_chart(pie, "J8")

wb.save('sales_dashboard.xlsx')
```

## 限制

- 无法执行 VBA 宏
- 复杂的数据透视表功能支持有限
- 小图表 (sparkline) 的支持不足
- 不支持外部数据连接
- 某些高级图表类型不可用

## 安装

```bash
pip install openpyxl
```

## 资源

- [openpyxl 文档](https://openpyxl.readthedocs.io/)
- [GitHub 仓库](https://github.com/theorchard/openpyxl)
- [关于样式设置的使用](https://openpyxl.readthedocs.io/en/stable/styles.html)