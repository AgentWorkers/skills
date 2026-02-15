---
name: template-engine
description: 使用数据自动填充文档模板——适用于任何格式的邮件合并功能
author: claude-office-skills
version: "1.0"
tags: ['template', 'mail-merge', 'autofill', 'automation']
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: docxtpl / yumdocs
  url: https://github.com/elapouya/python-docxtpl
  stars: 2.1k
---

# 模板引擎技能

## 概述

该技能支持基于模板的文档生成——您可以定义包含占位符的模板，然后自动用数据填充这些占位符。该技能适用于 Word、Excel、PowerPoint 等文档格式。

## 使用方法

1. 说明您想要完成的具体任务。
2. 提供所需的输入数据或文件。
3. 我将执行相应的操作。

**示例提示：**
- “批量生成信件/合同的邮件合并内容”
- “根据数据生成个性化报告”
- “根据模板创建证书”
- “使用用户数据自动填充表单”

## 相关领域知识

### 模板语法（基于 Jinja2）

```
{{ variable }}           - Simple substitution
{% for item in list %}   - Loop
{% if condition %}       - Conditional
{{ date | format_date }} - Filter
```

### Word 模板示例

```python
from docxtpl import DocxTemplate

# Create template with placeholders:
# Dear {{ name }},
# Thank you for your order #{{ order_id }}...

def fill_template(template_path: str, data: dict, output_path: str):
    doc = DocxTemplate(template_path)
    doc.render(data)
    doc.save(output_path)
    return output_path

# Usage
fill_template(
    "templates/order_confirmation.docx",
    {
        "name": "John Smith",
        "order_id": "ORD-12345",
        "items": [
            {"name": "Product A", "qty": 2, "price": 29.99},
            {"name": "Product B", "qty": 1, "price": 49.99}
        ],
        "total": 109.97
    },
    "output/confirmation_john.docx"
)
```

### Excel 模板示例

```python
from openpyxl import load_workbook
import re

def fill_excel_template(template_path: str, data: dict, output_path: str):
    wb = load_workbook(template_path)
    ws = wb.active
    
    # Find and replace placeholders like {{name}}
    for row in ws.iter_rows():
        for cell in row:
            if cell.value and isinstance(cell.value, str):
                for key, value in data.items():
                    placeholder = "{{" + key + "}}"
                    if placeholder in cell.value:
                        cell.value = cell.value.replace(placeholder, str(value))
    
    wb.save(output_path)
    return output_path
```

### 批量生成（邮件合并）

```python
import csv
from pathlib import Path

def mail_merge(template_path: str, data_csv: str, output_dir: str):
    """Generate documents for each row in CSV."""
    
    Path(output_dir).mkdir(exist_ok=True)
    
    with open(data_csv) as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader):
            output_path = f"{output_dir}/document_{i+1}.docx"
            fill_template(template_path, row, output_path)
            print(f"Generated: {output_path}")

# Usage with contacts.csv:
# name,email,company
# John,john@example.com,Acme
# Jane,jane@example.com,Corp

mail_merge(
    "templates/welcome_letter.docx",
    "data/contacts.csv",
    "output/letters"
)
```

### 高级功能：条件内容处理

```python
from docxtpl import DocxTemplate

# Template with conditionals:
# {% if vip %}
# Thank you for being a VIP member!
# {% else %}
# Thank you for your purchase.
# {% endif %}

doc = DocxTemplate("template.docx")
doc.render({
    "name": "John",
    "vip": True,
    "discount": 20
})
doc.save("output.docx")
```

## 最佳实践

1. **使用清晰的占位符名称（例如：{{client_name}}）**
2. **在渲染之前验证数据**
3. **优雅地处理缺失的数据**
4. **对模板进行版本控制**

## 安装方法

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## 资源推荐

- [docxtpl / yumdocs 仓库](https://github.com/elapouya/python-docxtpl)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)