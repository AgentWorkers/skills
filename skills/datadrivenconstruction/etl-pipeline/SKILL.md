---
slug: "etl-pipeline"
display_name: "ETL Pipeline"
description: "构建自动化的数据提取（Extract）、转换（Transform）和加载（Load，简称ETL）管道，用于处理建筑相关数据。支持处理PDF文件、Excel表格以及BIM格式的输出文件。能够生成报告和仪表板，并与其他系统进行集成。支持使用Airflow或n8n等工具进行流程编排。"
---

# 建筑数据ETL管道

## 概述

基于DDC方法论（第4.2章），本技能可帮助构建自动化数据管道，从各种来源提取数据，将其转换为可用格式，然后加载到目标系统中或生成报告。

**参考书籍**：《ETL与流程自动化》（"ETL и автоматизация процессов"）

> “ETL：从手动管理向自动化的转变使企业能够在无需持续人工干预的情况下处理数据。”
> — DDC书籍，第4.2章

## ETL组件

```
┌─────────┐    ┌───────────┐    ┌────────┐
│ EXTRACT │ -> │ TRANSFORM │ -> │  LOAD  │
└─────────┘    └───────────┘    └────────┘
   │               │               │
   ▼               ▼               ▼
 Sources        Process         Outputs
 - PDF          - Clean         - Excel
 - Excel        - Validate      - PDF
 - CSV          - Calculate     - Database
 - BIM          - Merge         - API
 - API          - Aggregate     - Dashboard
```

## 快速入门

```python
import pandas as pd

# Simple ETL Pipeline
def simple_etl_pipeline(input_file, output_file):
    # EXTRACT
    df = pd.read_excel(input_file)

    # TRANSFORM
    df = df.dropna()  # Clean
    df['Total'] = df['Quantity'] * df['Unit_Price']  # Calculate
    summary = df.groupby('Category')['Total'].sum()  # Aggregate

    # LOAD
    summary.to_excel(output_file)
    return summary

# Run
result = simple_etl_pipeline("raw_data.xlsx", "processed_report.xlsx")
```

## 数据提取（Extract）：数据来源

### 从多个Excel文件中提取数据

```python
import pandas as pd
from pathlib import Path

def extract_excel_files(folder_path, pattern="*.xlsx"):
    """Extract data from multiple Excel files"""
    files = Path(folder_path).glob(pattern)
    all_data = []

    for file in files:
        try:
            df = pd.read_excel(file)
            df['_source_file'] = file.name
            all_data.append(df)
            print(f"Extracted: {file.name}")
        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

# Usage
df = extract_excel_files("./project_data/")
```

### 从PDF文档中提取数据

```python
import pdfplumber
import pandas as pd

def extract_from_pdfs(pdf_folder):
    """Extract tables from all PDFs in folder"""
    files = Path(pdf_folder).glob("*.pdf")
    all_tables = []

    for pdf_path in files:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables:
                    if table and len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        df['_source'] = pdf_path.name
                        all_tables.append(df)

    return pd.concat(all_tables, ignore_index=True) if all_tables else pd.DataFrame()
```

### 从API中提取数据

```python
import requests
import pandas as pd

def extract_from_api(api_url, headers=None):
    """Extract data from REST API"""
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return pd.DataFrame(data)
    else:
        raise Exception(f"API error: {response.status_code}")

# Usage
df = extract_from_api("https://api.example.com/projects")
```

### 从数据库中提取数据

```python
import pandas as pd
import sqlite3

def extract_from_database(db_path, query):
    """Extract data using SQL query"""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Usage
df = extract_from_database(
    "construction.db",
    "SELECT * FROM elements WHERE category = 'Wall'"
)
```

## 数据转换（Transform）：数据处理

### 数据清洗

```python
def clean_construction_data(df):
    """Standard cleaning for construction data"""
    # Remove empty rows
    df = df.dropna(how='all')

    # Strip whitespace
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()

    # Standardize category names
    if 'Category' in df.columns:
        df['Category'] = df['Category'].str.title()

    # Convert numeric columns
    numeric_cols = ['Volume', 'Area', 'Length', 'Quantity', 'Cost']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Remove duplicates
    df = df.drop_duplicates()

    return df
```

### 数据验证

```python
def validate_construction_data(df, rules):
    """
    Validate data against rules

    Args:
        rules: list of dicts like
        [{'column': 'Volume', 'rule': 'positive'},
         {'column': 'Category', 'rule': 'not_null'}]
    """
    errors = []

    for rule in rules:
        col = rule['column']
        rule_type = rule['rule']

        if col not in df.columns:
            errors.append(f"Missing column: {col}")
            continue

        if rule_type == 'positive':
            invalid = df[df[col] <= 0]
            if len(invalid) > 0:
                errors.append(f"{len(invalid)} rows with non-positive {col}")

        elif rule_type == 'not_null':
            null_count = df[col].isna().sum()
            if null_count > 0:
                errors.append(f"{null_count} null values in {col}")

        elif rule_type == 'unique':
            duplicates = df[col].duplicated().sum()
            if duplicates > 0:
                errors.append(f"{duplicates} duplicate values in {col}")

    return errors

# Usage
validation_rules = [
    {'column': 'Volume', 'rule': 'positive'},
    {'column': 'Category', 'rule': 'not_null'},
    {'column': 'ElementId', 'rule': 'unique'}
]
errors = validate_construction_data(df, validation_rules)
```

### 数据聚合

```python
def aggregate_by_hierarchy(df, hierarchy=['Project', 'Building', 'Level', 'Category']):
    """Aggregate data at different hierarchy levels"""
    results = {}

    for i in range(1, len(hierarchy) + 1):
        level_cols = hierarchy[:i]
        if all(col in df.columns for col in level_cols):
            agg = df.groupby(level_cols).agg({
                'Volume': 'sum',
                'Cost': 'sum',
                'ElementId': 'count'
            }).rename(columns={'ElementId': 'Count'})

            level_name = '_'.join(level_cols)
            results[level_name] = agg

    return results

# Usage
aggregations = aggregate_by_hierarchy(df)
for name, data in aggregations.items():
    print(f"\n{name}:")
    print(data.head())
```

### 数据增强

```python
def enrich_with_prices(df, prices_df):
    """Enrich element data with pricing information"""
    # Merge with price database
    enriched = df.merge(prices_df, on='Category', how='left')

    # Calculate costs
    enriched['Material_Cost'] = enriched['Volume'] * enriched['Unit_Price']
    enriched['Labor_Cost'] = enriched['Volume'] * enriched['Labor_Rate']
    enriched['Total_Cost'] = enriched['Material_Cost'] + enriched['Labor_Cost']

    return enriched
```

## 数据加载（Load）：输出生成

### 生成Excel报告

```python
def generate_excel_report(df, summary, output_path):
    """Generate formatted Excel report"""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Raw data
        df.to_excel(writer, sheet_name='Data', index=False)

        # Summary by category
        summary.to_excel(writer, sheet_name='Summary')

        # Pivot table
        if 'Level' in df.columns and 'Category' in df.columns:
            pivot = pd.pivot_table(
                df, values='Volume',
                index='Level', columns='Category',
                aggfunc='sum', fill_value=0
            )
            pivot.to_excel(writer, sheet_name='By_Level')

    print(f"Report saved: {output_path}")

# Usage
generate_excel_report(df, summary, "project_report.xlsx")
```

### 生成PDF报告

```python
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf_report(df, output_path, title="Construction Report"):
    """Generate PDF report from DataFrame"""
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph(title, styles['Title']))

    # Convert DataFrame to table
    data = [df.columns.tolist()] + df.values.tolist()
    table = Table(data)

    # Style the table
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)
    print(f"PDF saved: {output_path}")

# Usage
generate_pdf_report(summary, "report.pdf")
```

### 将数据加载到数据库中

```python
import sqlite3

def load_to_database(df, db_path, table_name, if_exists='replace'):
    """Load DataFrame to SQLite database"""
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists=if_exists, index=False)
    conn.close()
    print(f"Loaded {len(df)} rows to {table_name}")

# Usage
load_to_database(df, "construction.db", "elements")
```

## 完整的ETL管道

```python
class ConstructionETLPipeline:
    """Complete ETL pipeline for construction data"""

    def __init__(self, config):
        self.config = config
        self.data = None
        self.errors = []

    def extract(self):
        """Extract data from configured sources"""
        print("Extracting data...")
        sources = []

        # Excel files
        if 'excel_folder' in self.config:
            df = extract_excel_files(self.config['excel_folder'])
            sources.append(df)

        # PDF files
        if 'pdf_folder' in self.config:
            df = extract_from_pdfs(self.config['pdf_folder'])
            sources.append(df)

        self.data = pd.concat(sources, ignore_index=True)
        print(f"Extracted {len(self.data)} records")
        return self

    def transform(self):
        """Apply transformations"""
        print("Transforming data...")

        # Clean
        self.data = clean_construction_data(self.data)

        # Validate
        if 'validation_rules' in self.config:
            self.errors = validate_construction_data(
                self.data, self.config['validation_rules']
            )

        # Enrich with prices if available
        if 'prices_file' in self.config:
            prices = pd.read_excel(self.config['prices_file'])
            self.data = enrich_with_prices(self.data, prices)

        print(f"Transformed {len(self.data)} records")
        return self

    def load(self):
        """Load to configured outputs"""
        print("Loading data...")

        # Excel report
        if 'excel_output' in self.config:
            summary = self.data.groupby('Category').agg({
                'Volume': 'sum', 'Cost': 'sum'
            })
            generate_excel_report(
                self.data, summary, self.config['excel_output']
            )

        # Database
        if 'database' in self.config:
            load_to_database(
                self.data,
                self.config['database'],
                self.config.get('table_name', 'elements')
            )

        print("Pipeline complete!")
        return self

    def run(self):
        """Run complete pipeline"""
        return self.extract().transform().load()

# Usage
config = {
    'excel_folder': './input_data/',
    'prices_file': './prices.xlsx',
    'validation_rules': [
        {'column': 'Volume', 'rule': 'positive'},
        {'column': 'Category', 'rule': 'not_null'}
    ],
    'excel_output': './output/report.xlsx',
    'database': './output/project.db',
    'table_name': 'elements'
}

pipeline = ConstructionETLPipeline(config)
pipeline.run()
```

## 使用Airflow进行调度

```python
# airflow_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'construction_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'construction_etl',
    default_args=default_args,
    description='Daily construction data ETL',
    schedule_interval='@daily',
)

def extract_task():
    # Extract logic
    pass

def transform_task():
    # Transform logic
    pass

def load_task():
    # Load logic
    pass

t1 = PythonOperator(task_id='extract', python_callable=extract_task, dag=dag)
t2 = PythonOperator(task_id='transform', python_callable=transform_task, dag=dag)
t3 = PythonOperator(task_id='load', python_callable=load_task, dag=dag)

t1 >> t2 >> t3
```

## 快速参考

| 阶段 | 任务 | 工具/方法 |
|-------|------|-------------|
| 数据提取 | 读取Excel文件 | `pd.read_excel()` |
| 数据提取 | 读取CSV文件 | `pd.read_csv()` |
| 数据提取 | 读取PDF文件 | `pdfplumber` |
| 数据提取 | 从API中获取数据 | `requests.get()` |
| 数据转换 | 数据清洗 | `df.dropna()`, `df.str.strip()` |
| 数据转换 | 数据验证 | 自定义验证函数 |
| 数据转换 | 数据计算 | `df['new'] = df['a'] * df['b']` |
| 数据转换 | 数据聚合 | `df.groupby().agg()` |
| 数据加载 | 生成Excel报告 | `df.to_excel()` |
| 数据加载 | 生成PDF报告 | `reportlab` |
| 数据加载 | 将数据插入数据库 | `df.to_sql()` |
| 数据加载 | 将数据发送到API | `requests.post()` |

## 资源

- **书籍**：Artem Boiko所著的《数据驱动的建筑》（"Data-Driven Construction"），第4.2章
- **网站**：https://datadrivenconstruction.io
- **Airflow**：https://airflow.apache.org
- **n8n**：https://n8n.io

## 下一步操作

- 查看`bim-validation-pipeline`以了解BIM数据验证功能
- 查看`pdf-report-generator`以了解高级PDF生成方法
- 查看`workflow-automation`以了解n8n集成方案