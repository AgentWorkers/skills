---
name: report-generator
description: 生成包含图表、表格和可视化元素的专业数据报告。
author: claude-office-skills
version: "1.0"
tags: [report, visualization, charts, data, automation]
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
---

# 报告生成器技能

## 概述

该技能能够自动生成专业的数据报告。您可以使用该技能创建仪表板、关键绩效指标（KPI）汇总报告以及包含图表、表格和数据分析结果的分析报告。

## 使用方法

1. 提供数据（格式为 CSV、Excel 或 JSON，或通过文字描述数据内容）；
2. 指定所需的报告类型；
3. 我将为您生成包含可视化内容的格式化报告。

**示例提示：**
- “根据这些数据生成一份销售报告”；
- “创建一个每月的 KPI 仪表板”；
- “制作一份包含图表的高管总结报告”；
- “生成一份数据分析报告”。

## 相关领域知识

### 报告的组成部分

```python
# Report structure
report = {
    'title': 'Monthly Sales Report',
    'period': 'January 2024',
    'sections': [
        'executive_summary',
        'kpi_dashboard',
        'detailed_analysis',
        'charts',
        'recommendations'
    ]
}
```

### 使用 Python 生成报告

```python
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(data, output_path):
    # Load data
    df = pd.read_csv(data)
    
    # Calculate KPIs
    total_revenue = df['revenue'].sum()
    avg_order = df['revenue'].mean()
    growth = df['revenue'].pct_change().mean()
    
    # Create charts
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    df.plot(kind='bar', ax=axes[0,0], title='Revenue by Month')
    df.plot(kind='line', ax=axes[0,1], title='Trend')
    plt.savefig('charts.png')
    
    # Generate PDF
    # ... PDF generation code
    
    return output_path
```

### HTML 报告模板

```python
def generate_html_report(data, title):
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            .kpi {{ display: flex; gap: 20px; }}
            .kpi-card {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
            .metric {{ font-size: 2em; font-weight: bold; color: #2563eb; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div class="kpi">
            <div class="kpi-card">
                <div class="metric">${data['revenue']:,.0f}</div>
                <div>Total Revenue</div>
            </div>
            <div class="kpi-card">
                <div class="metric">{data['growth']:.1%}</div>
                <div>Growth Rate</div>
            </div>
        </div>
        <!-- More content -->
    </body>
    </html>
    '''
    return html
```

## 示例：销售报告

```python
import pandas as pd
import matplotlib.pyplot as plt

def create_sales_report(csv_path, output_path):
    # Read data
    df = pd.read_csv(csv_path)
    
    # Calculate metrics
    metrics = {
        'total_revenue': df['amount'].sum(),
        'total_orders': len(df),
        'avg_order': df['amount'].mean(),
        'top_product': df.groupby('product')['amount'].sum().idxmax()
    }
    
    # Create visualizations
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Revenue by product
    df.groupby('product')['amount'].sum().plot(
        kind='bar', ax=axes[0,0], title='Revenue by Product'
    )
    
    # Monthly trend
    df.groupby('month')['amount'].sum().plot(
        kind='line', ax=axes[0,1], title='Monthly Revenue'
    )
    
    plt.tight_layout()
    plt.savefig(output_path.replace('.html', '_charts.png'))
    
    # Generate HTML report
    html = generate_html_report(metrics, 'Sales Report')
    
    with open(output_path, 'w') as f:
        f.write(html)
    
    return output_path

create_sales_report('sales_data.csv', 'sales_report.html')
```

## 可用资源

- [Matplotlib](https://matplotlib.org/)  
- [Plotly](https://plotly.com/)  
- [ReportLab](https://www.reportlab.com/)