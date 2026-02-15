---
name: "llm-data-automation"
description: "使用大型语言模型（如 ChatGPT、Claude、LLaMA）自动化处理构建数据。无需深厚的编程知识，即可生成 Python/Pandas 脚本，从文档中提取数据，并创建自动化的数据处理流程。"
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🐼", "os": ["win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---# 建筑行业中的大型语言模型（LLM）数据自动化

## 概述

基于DDC方法论（第2.3章），该技能利用大型语言模型（LLM）实现建筑数据处理的自动化。无需手动编写数据转换代码，只需用自然语言描述所需操作，LLM会自动生成相应的Python/Pandas代码。

**参考书籍**：《Pandas DataFrame与LLM ChatGPT》  
> “像ChatGPT和LLaMA这样的LLM模型，让没有深厚编程知识的专业人员也能参与到公司的自动化和业务流程改进中。”  
—— DDC书籍，第2.3章

## 快速入门

### 选项1：使用ChatGPT/Claude Online  
只需用自然语言描述您的数据处理任务：  
```
Prompt: "Write Python code to read an Excel file with construction materials,
filter rows where quantity > 100, and save to CSV."
```

### 选项2：运行本地LLM（Ollama）  
```bash
# Install Ollama from ollama.com
ollama pull mistral

# Run a query
ollama run mistral "Write Pandas code to calculate total cost from quantity * unit_price"
```

### 选项3：使用LM Studio（图形用户界面）  
1. 从lmstudio.ai下载软件  
2. 安装并选择一个模型（例如Mistral、LLaMA）  
3. 开始与本地AI进行交互  

## 核心概念  

### DataFrame作为通用数据格式  
```python
import pandas as pd

# Construction project as DataFrame
# Rows = elements, Columns = attributes
df = pd.DataFrame({
    'element_id': ['W001', 'W002', 'C001'],
    'category': ['Wall', 'Wall', 'Column'],
    'material': ['Concrete', 'Brick', 'Steel'],
    'volume_m3': [45.5, 32.0, 8.2],
    'cost_per_m3': [150, 80, 450]
})

# Calculate total cost
df['total_cost'] = df['volume_m3'] * df['cost_per_m3']
print(df)
```

### 用于建筑任务的LLM提示语  

**数据导入：**  
```
"Write code to import Excel file with construction schedule,
parse dates, and create a Pandas DataFrame"
```

**数据过滤：**  
```
"Filter construction elements where category is 'Structural'
and cost exceeds budget limit of 50000"
```

**数据聚合：**  
```
"Group construction data by floor level,
calculate total volume and cost for each floor"
```

**报告生成：**  
```
"Create summary report with material quantities grouped by category,
export to Excel with formatting"
```

## 常见用例  

### 1. 从PDF文档中提取数据  
```python
# Prompt to ChatGPT:
# "Write code to extract tables from PDF and convert to DataFrame"

import pdfplumber
import pandas as pd

def pdf_to_dataframe(pdf_path):
    """Extract tables from PDF file"""
    all_tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    df = pd.DataFrame(table[1:], columns=table[0])
                    all_tables.append(df)

    if all_tables:
        return pd.concat(all_tables, ignore_index=True)
    return pd.DataFrame()

# Usage
df = pdf_to_dataframe("construction_spec.pdf")
df.to_excel("extracted_data.xlsx", index=False)
```

### 2. 处理BIM元素数据  
```python
# Prompt: "Analyze BIM elements, group by category, calculate volumes"

import pandas as pd

def analyze_bim_elements(csv_path):
    """Analyze BIM element data from CSV export"""
    df = pd.read_csv(csv_path)

    # Group by category
    summary = df.groupby('Category').agg({
        'Volume': 'sum',
        'Area': 'sum',
        'ElementId': 'count'
    }).rename(columns={'ElementId': 'Count'})

    return summary

# Usage
summary = analyze_bim_elements("revit_export.csv")
print(summary)
```

### 3. 成本估算流程  
```python
# Prompt: "Create cost estimation from quantities and unit prices"

import pandas as pd

def calculate_cost_estimate(quantities_df, prices_df):
    """
    Calculate project cost estimate

    Args:
        quantities_df: DataFrame with columns [item_code, quantity]
        prices_df: DataFrame with columns [item_code, unit_price, unit]

    Returns:
        DataFrame with cost calculations
    """
    # Merge quantities with prices
    result = quantities_df.merge(prices_df, on='item_code', how='left')

    # Calculate costs
    result['total_cost'] = result['quantity'] * result['unit_price']

    # Add summary
    result['cost_percentage'] = (result['total_cost'] /
                                  result['total_cost'].sum() * 100).round(2)

    return result

# Usage
quantities = pd.DataFrame({
    'item_code': ['C001', 'S001', 'W001'],
    'quantity': [150, 2000, 500]
})

prices = pd.DataFrame({
    'item_code': ['C001', 'S001', 'W001'],
    'unit_price': [120, 45, 85],
    'unit': ['m3', 'kg', 'm2']
})

estimate = calculate_cost_estimate(quantities, prices)
print(estimate)
```

### 4. 安排数据处理任务  
```python
# Prompt: "Parse construction schedule, calculate durations, identify delays"

import pandas as pd
from datetime import datetime

def analyze_schedule(schedule_path):
    """Analyze construction schedule for delays"""
    df = pd.read_excel(schedule_path)

    # Parse dates
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['actual_end'] = pd.to_datetime(df['actual_end'])

    # Calculate durations
    df['planned_duration'] = (df['end_date'] - df['start_date']).dt.days
    df['actual_duration'] = (df['actual_end'] - df['start_date']).dt.days

    # Identify delays
    df['delay_days'] = df['actual_duration'] - df['planned_duration']
    df['is_delayed'] = df['delay_days'] > 0

    return df

# Usage
schedule = analyze_schedule("project_schedule.xlsx")
delayed_tasks = schedule[schedule['is_delayed']]
print(f"Delayed tasks: {len(delayed_tasks)}")
```

## 本地LLM设置（无需网络连接）  

### 使用Ollama  
```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Download models
ollama pull mistral      # General purpose, 7B params
ollama pull codellama    # Code-focused
ollama pull deepseek-coder  # Best for coding tasks

# Run
ollama run mistral "Write Pandas code to merge two DataFrames on project_id"
```

### 使用LlamaIndex处理公司文档  
```python
# Load company documents into local LLM
from llama_index import SimpleDirectoryReader, VectorStoreIndex

# Read all PDFs from folder
reader = SimpleDirectoryReader("company_documents/")
documents = reader.load_data()

# Create searchable index
index = VectorStoreIndex.from_documents(documents)

# Query your documents
query_engine = index.as_query_engine()
response = query_engine.query(
    "What are the standard concrete mix specifications?"
)
print(response)
```

## 开发环境推荐  

| 开发环境 | 适用场景 | 主要特点 |
|---------|-----------|-------------------|
| **Jupyter Notebook** | 学习、实验 | 交互式单元格、可视化功能 |
| **Google Colab** | 免费GPU、快速上手 | 基于云的环境、预装库 |
| **VS Code** | 专业开发 | 扩展插件、GitHub Copilot集成 |
| **PyCharm** | 大型项目 | 高级调试、代码重构功能 |

### 使用Jupyter的快速设置  
```bash
pip install jupyter pandas openpyxl pdfplumber
jupyter notebook
```

## 最佳实践  

1. **从简单开始**：使用清晰、具体的提示语进行尝试  
2. **迭代优化**：根据结果不断调整提示语  
3. **验证代码**：运行前务必检查生成的代码  
4. **记录提示语**：保存有用的提示语以备后续使用  
5. **数据安全**：处理敏感公司数据时使用本地LLM  

## 常见提示语库  

### 数据导入  
- “读取Excel文件并显示前10行”  
- “以自定义分隔符和编码格式导入CSV文件”  
- “将多个Excel工作表加载到DataFrame字典中”  

### 数据清洗  
- “根据`element_id`删除重复行”  
- “用列平均值填充缺失值”  
- “将列数据转换为数值类型，并处理异常值”  

### 数据分析  
- “计算数值列的描述性统计信息”  
- “分析成本与耗时之间的关联”  
- “使用IQR方法识别异常值”  

### 数据导出  
- “导出为包含多个工作表的Excel文件”  
- “以指定编码格式保存为CSV文件”  
- “生成格式化的PDF报告”  

## 参考资源  

- **书籍**：Artem Boiko所著的《Data-Driven Construction》，第2.3章  
- **网站**：https://datadrivenconstruction.io  
- **Pandas官方文档**：https://pandas.pydata.org/docs/  
- **Ollama**：https://ollama.com  
- **LM Studio**：https://lmstudio.ai  
- **Google Colab**：https://colab.research.google.com  

## 下一步建议  

- 查阅`pandas-construction-analysis`以学习更高级的Pandas操作  
- 查阅`pdf-to-structured`以了解文档处理方法  
- 查阅`etl-pipeline`以了解自动化数据管道的实现  
- 查阅`rag-construction`以了解如何使用RAG技术处理建筑相关文档