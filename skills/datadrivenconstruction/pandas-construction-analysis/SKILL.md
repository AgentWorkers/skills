---
name: "pandas-construction-analysis"
description: "一个全面的Pandas工具包，用于建筑数据分析。支持过滤、分组、汇总BIM元素，计算数量，合并数据集，并从结构化的建筑数据中生成报告。"
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🐼", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---# Pandas在建筑数据分析中的应用

## 概述

本技能基于DDC方法论（第2.3章），提供了使用Pandas进行建筑数据处理的全面操作。Pandas堪称数据分析师的“瑞士军刀”——能够处理从简单的数据过滤到对数百万行数据进行复杂聚合的各种任务。

**参考书籍**：《Pandas DataFrame与LLM ChatGPT》  
> “通过使用Pandas，您可以管理和分析远超Excel处理能力的数据集。虽然Excel最多只能处理100万行数据，但Pandas可以轻松处理包含数千万行数据的数据集。”  
——DDC书籍，第2.3章

## 快速入门

```python
import pandas as pd

# Read construction data
df = pd.read_excel("bim_export.xlsx")

# Basic operations
print(df.head())           # First 5 rows
print(df.info())           # Column types and memory
print(df.describe())       # Statistics for numeric columns

# Filter structural elements
structural = df[df['Category'] == 'Structural']

# Calculate total volume
total_volume = df['Volume'].sum()
print(f"Total volume: {total_volume:.2f} m³")
```

## DataFrame基础

### 创建DataFrame

```python
import pandas as pd

# From dictionary (construction elements)
elements = pd.DataFrame({
    'ElementId': ['E001', 'E002', 'E003', 'E004'],
    'Category': ['Wall', 'Floor', 'Wall', 'Column'],
    'Material': ['Concrete', 'Concrete', 'Brick', 'Steel'],
    'Volume_m3': [45.5, 120.0, 32.0, 8.5],
    'Level': ['Level 1', 'Level 1', 'Level 2', 'Level 1']
})

# From CSV
df_csv = pd.read_csv("construction_data.csv")

# From Excel
df_excel = pd.read_excel("project_data.xlsx", sheet_name="Elements")

# From multiple Excel sheets
all_sheets = pd.read_excel("project.xlsx", sheet_name=None)  # Dict of DataFrames
```

### 建筑行业中的数据类型

```python
# Common data types for construction
df = pd.DataFrame({
    'element_id': pd.Series(['W001', 'W002'], dtype='string'),
    'quantity': pd.Series([10, 20], dtype='int64'),
    'volume': pd.Series([45.5, 32.0], dtype='float64'),
    'is_structural': pd.Series([True, False], dtype='bool'),
    'created_date': pd.to_datetime(['2024-01-15', '2024-01-16']),
    'category': pd.Categorical(['Wall', 'Slab'])
})

# Check data types
print(df.dtypes)

# Convert types
df['quantity'] = df['quantity'].astype('float64')
df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
```

## 过滤与选择

### 基本过滤

```python
# Single condition
walls = df[df['Category'] == 'Wall']

# Multiple conditions (AND)
large_concrete = df[(df['Material'] == 'Concrete') & (df['Volume_m3'] > 50)]

# Multiple conditions (OR)
walls_or_floors = df[(df['Category'] == 'Wall') | (df['Category'] == 'Floor')]

# Using isin for multiple values
structural = df[df['Category'].isin(['Wall', 'Column', 'Beam', 'Foundation'])]

# String contains
insulated = df[df['Description'].str.contains('insulated', case=False, na=False)]

# Null value filtering
incomplete = df[df['Cost'].isna()]
complete = df[df['Cost'].notna()]
```

### 高级选择

```python
# Select columns
volumes = df[['ElementId', 'Category', 'Volume_m3']]

# Query syntax (SQL-like)
result = df.query("Category == 'Wall' and Volume_m3 > 30")

# Loc and iloc
specific_row = df.loc[0]                    # By label
range_rows = df.iloc[0:10]                  # By position
specific_cell = df.loc[0, 'Volume_m3']      # Row and column
subset = df.loc[0:5, ['Category', 'Volume_m3']]  # Range with columns
```

## 分组与聚合

### GroupBy操作

```python
# Basic groupby
by_category = df.groupby('Category')['Volume_m3'].sum()

# Multiple aggregations
summary = df.groupby('Category').agg({
    'Volume_m3': ['sum', 'mean', 'count'],
    'Cost': ['sum', 'mean']
})

# Named aggregations (cleaner output)
summary = df.groupby('Category').agg(
    total_volume=('Volume_m3', 'sum'),
    avg_volume=('Volume_m3', 'mean'),
    element_count=('ElementId', 'count'),
    total_cost=('Cost', 'sum')
).reset_index()

# Multiple grouping columns
by_level_cat = df.groupby(['Level', 'Category']).agg({
    'Volume_m3': 'sum',
    'Cost': 'sum'
}).reset_index()
```

### 数据透视表

```python
# Create pivot table
pivot = pd.pivot_table(
    df,
    values='Volume_m3',
    index='Level',
    columns='Category',
    aggfunc='sum',
    fill_value=0,
    margins=True,           # Add totals
    margins_name='Total'
)

# Multiple values
pivot_detailed = pd.pivot_table(
    df,
    values=['Volume_m3', 'Cost'],
    index='Level',
    columns='Category',
    aggfunc={'Volume_m3': 'sum', 'Cost': 'mean'}
)
```

## 数据转换

### 添加计算列

```python
# Simple calculation
df['Cost_Total'] = df['Volume_m3'] * df['Unit_Price']

# Conditional column
df['Size_Category'] = df['Volume_m3'].apply(
    lambda x: 'Large' if x > 50 else ('Medium' if x > 20 else 'Small')
)

# Using np.where for binary conditions
import numpy as np
df['Is_Large'] = np.where(df['Volume_m3'] > 50, True, False)

# Using cut for binning
df['Volume_Bin'] = pd.cut(
    df['Volume_m3'],
    bins=[0, 10, 50, 100, float('inf')],
    labels=['XS', 'S', 'M', 'L']
)
```

### 字符串操作

```python
# Extract from strings
df['Level_Number'] = df['Level'].str.extract(r'(\d+)').astype(int)

# Split and expand
df[['Building', 'Floor']] = df['Location'].str.split('-', expand=True)

# Clean strings
df['Category'] = df['Category'].str.strip().str.lower().str.title()

# Replace values
df['Material'] = df['Material'].str.replace('Reinforced Concrete', 'RC')
```

### 日期操作

```python
# Parse dates
df['Start_Date'] = pd.to_datetime(df['Start_Date'])

# Extract components
df['Year'] = df['Start_Date'].dt.year
df['Month'] = df['Start_Date'].dt.month
df['Week'] = df['Start_Date'].dt.isocalendar().week
df['DayOfWeek'] = df['Start_Date'].dt.day_name()

# Calculate duration
df['Duration_Days'] = (df['End_Date'] - df['Start_Date']).dt.days

# Filter by date range
recent = df[df['Start_Date'] >= '2024-01-01']
```

## 合并与连接

### 合并DataFrame

```python
# Elements data
elements = pd.DataFrame({
    'ElementId': ['E001', 'E002', 'E003'],
    'Category': ['Wall', 'Floor', 'Column'],
    'Volume_m3': [45.5, 120.0, 8.5]
})

# Unit prices
prices = pd.DataFrame({
    'Category': ['Wall', 'Floor', 'Column', 'Beam'],
    'Unit_Price': [150, 80, 450, 200]
})

# Inner join (only matching)
merged = elements.merge(prices, on='Category', how='inner')

# Left join (keep all elements)
merged = elements.merge(prices, on='Category', how='left')

# Join on different column names
result = df1.merge(df2, left_on='elem_id', right_on='ElementId')
```

### 连接DataFrame

```python
# Vertical concatenation (stacking)
all_floors = pd.concat([floor1_df, floor2_df, floor3_df], ignore_index=True)

# Horizontal concatenation
combined = pd.concat([quantities, costs, schedule], axis=1)

# Append new rows
new_elements = pd.DataFrame({'ElementId': ['E004'], 'Category': ['Beam']})
df = pd.concat([df, new_elements], ignore_index=True)
```

## 建筑行业特有的分析

### 数量统计（QTO）

```python
def generate_qto_report(df):
    """Generate Quantity Take-Off summary by category"""
    qto = df.groupby(['Category', 'Material']).agg(
        count=('ElementId', 'count'),
        total_volume=('Volume_m3', 'sum'),
        total_area=('Area_m2', 'sum'),
        avg_volume=('Volume_m3', 'mean')
    ).round(2)

    # Add percentage column
    qto['volume_pct'] = (qto['total_volume'] /
                          qto['total_volume'].sum() * 100).round(1)

    return qto.sort_values('total_volume', ascending=False)

# Usage
qto_report = generate_qto_report(df)
qto_report.to_excel("qto_report.xlsx")
```

### 成本估算

```python
def calculate_project_cost(elements_df, prices_df, markup=0.15):
    """Calculate total project cost with markup"""
    # Merge with prices
    df = elements_df.merge(prices_df, on='Category', how='left')

    # Calculate base cost
    df['Base_Cost'] = df['Volume_m3'] * df['Unit_Price']

    # Apply markup
    df['Total_Cost'] = df['Base_Cost'] * (1 + markup)

    # Summary by category
    summary = df.groupby('Category').agg(
        volume=('Volume_m3', 'sum'),
        base_cost=('Base_Cost', 'sum'),
        total_cost=('Total_Cost', 'sum')
    ).round(2)

    return df, summary, summary['total_cost'].sum()

# Usage
detailed, summary, total = calculate_project_cost(elements, prices)
print(f"Project Total: ${total:,.2f}")
```

### 材料汇总

```python
def material_summary(df):
    """Summarize materials across project"""
    summary = df.groupby('Material').agg({
        'Volume_m3': 'sum',
        'Weight_kg': 'sum',
        'ElementId': 'nunique'
    }).rename(columns={'ElementId': 'Element_Count'})

    summary['Volume_Pct'] = (summary['Volume_m3'] /
                              summary['Volume_m3'].sum() * 100).round(1)

    return summary.sort_values('Volume_m3', ascending=False)
```

### 分层分析

```python
def analyze_by_level(df):
    """Analyze construction quantities by building level"""
    level_summary = df.pivot_table(
        values=['Volume_m3', 'Cost'],
        index='Level',
        columns='Category',
        aggfunc='sum',
        fill_value=0
    )

    level_summary['Total_Volume'] = level_summary['Volume_m3'].sum(axis=1)
    level_summary['Total_Cost'] = level_summary['Cost'].sum(axis=1)

    return level_summary
```

## 数据导出

### 导出为包含多个工作表的Excel文件

```python
def export_to_excel_formatted(df, summary, filepath):
    """Export with multiple sheets"""
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Details', index=False)
        summary.to_excel(writer, sheet_name='Summary')

        pivot = pd.pivot_table(df, values='Volume_m3',
                               index='Level', columns='Category')
        pivot.to_excel(writer, sheet_name='By_Level')

# Usage
export_to_excel_formatted(elements, qto_summary, "project_report.xlsx")
```

### 导出为CSV文件

```python
# Basic export
df.to_csv("output.csv", index=False)

# With encoding for special characters
df.to_csv("output.csv", index=False, encoding='utf-8-sig')

# Specific columns
df[['ElementId', 'Category', 'Volume_m3']].to_csv("volumes.csv", index=False)
```

## 性能优化技巧

```python
# Use categories for string columns with few unique values
df['Category'] = df['Category'].astype('category')

# Read only needed columns
df = pd.read_csv("large_file.csv", usecols=['ElementId', 'Category', 'Volume'])

# Use chunking for very large files
chunks = pd.read_csv("huge_file.csv", chunksize=100000)
result = pd.concat([chunk[chunk['Category'] == 'Wall'] for chunk in chunks])

# Check memory usage
print(df.memory_usage(deep=True).sum() / 1024**2, "MB")
```

## 快速参考

| 操作          | 代码                |
|---------------|-------------------|
| 读取Excel文件     | `pd.read_excel("file.xlsx")`    |
| 读取CSV文件     | `pd.read_csv("file.csv")`    |
| 过滤行         | `df[df['Column'] == 'Value']`    |
| 选择列         | `df[['Col1', 'Col2']]`     |
| 分组并求和     | `df.groupby('Cat')['Vol'].sum()`   |
| 数据透视表       | `pd.pivot_table(df, values='Vol', index='Level')` |
| 合并DataFrame     | `df1.merge(df2, on='key')`     |
| 添加新列       | `df['New'] = df['A'] * df['B']`    |
| 导出为Excel文件   | `df.to_excel("out.xlsx", index=False)` |

## 资源

- **书籍**：Artem Boiko所著的《Data-Driven Construction》，第2.3章  
- **网站**：https://datadrivenconstruction.io  
- **Pandas文档**：https://pandas.pydata.org/docs/

## 下一步

- 可参考`llm-data-automation`以了解如何利用AI生成Pandas代码  
- 可参考`qto-report`以获取专门的QTO计算工具  
- 可参考`cost-estimation-resource`以获取详细的成本计算方法