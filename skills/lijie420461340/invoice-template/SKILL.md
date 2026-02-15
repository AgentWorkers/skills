---
name: invoice-template
description: 根据提供的模板生成专业的PDF发票。
author: claude-office-skills
version: "1.0"
tags: ['invoice', 'pdf', 'template', 'billing']
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: easy-invoice-pdf
  url: https://github.com/nickmitchko/easy-invoice-pdf
  stars: 476
---

# 发票模板技能

## 概述

该技能能够根据结构化数据及模板生成专业的PDF发票。生成的发票包含公司品牌标识、商品明细列表、税费计算结果以及付款信息。

## 使用方法

1. 说明您想要完成的具体任务；
2. 提供所需的输入数据或文件；
3. 我将执行相应的操作。

**示例提示：**
- “根据订单数据生成发票”
- “创建定期生成的发票”
- “批量生成每月的发票”
- “根据客户需求定制发票模板”

## 相关领域知识


### 发票数据结构

```python
invoice_data = {
    "invoice_number": "INV-2026-001",
    "date": "2026-01-30",
    "due_date": "2026-02-28",
    
    "from": {
        "name": "Your Company",
        "address": "123 Business St",
        "email": "billing@company.com"
    },
    
    "to": {
        "name": "Client Name",
        "address": "456 Client Ave",
        "email": "client@example.com"
    },
    
    "items": [
        {"description": "Consulting", "quantity": 10, "rate": 150.00},
        {"description": "Development", "quantity": 20, "rate": 100.00}
    ],
    
    "tax_rate": 0.08,
    "notes": "Payment due within 30 days"
}
```

### 使用ReportLab生成PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_invoice(data: dict, output_path: str):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(1*inch, height - 1*inch, "INVOICE")
    
    # Invoice details
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, f"Invoice #: {data['invoice_number']}")
    c.drawString(1*inch, height - 1.75*inch, f"Date: {data['date']}")
    
    # From/To
    y = height - 2.5*inch
    c.drawString(1*inch, y, f"From: {data['from']['name']}")
    c.drawString(4*inch, y, f"To: {data['to']['name']}")
    
    # Items table
    y = height - 4*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1*inch, y, "Description")
    c.drawString(4*inch, y, "Qty")
    c.drawString(5*inch, y, "Rate")
    c.drawString(6*inch, y, "Amount")
    
    c.setFont("Helvetica", 10)
    subtotal = 0
    for item in data['items']:
        y -= 0.3*inch
        amount = item['quantity'] * item['rate']
        subtotal += amount
        c.drawString(1*inch, y, item['description'])
        c.drawString(4*inch, y, str(item['quantity']))
        c.drawString(5*inch, y, f"${item['rate']:.2f}")
        c.drawString(6*inch, y, f"${amount:.2f}")
    
    # Totals
    tax = subtotal * data['tax_rate']
    total = subtotal + tax
    
    y -= 0.5*inch
    c.drawString(5*inch, y, f"Subtotal: ${subtotal:.2f}")
    y -= 0.25*inch
    c.drawString(5*inch, y, f"Tax ({data['tax_rate']*100}%): ${tax:.2f}")
    y -= 0.25*inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(5*inch, y, f"Total: ${total:.2f}")
    
    c.save()
    return output_path
```

### 使用HTML模板生成发票

```python
from weasyprint import HTML
from jinja2 import Template

invoice_template = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; margin: 40px; }
        .header { display: flex; justify-content: space-between; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        .total { font-weight: bold; font-size: 18px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>INVOICE</h1>
        <div>
            <p>Invoice #: {{ invoice_number }}</p>
            <p>Date: {{ date }}</p>
        </div>
    </div>
    <table>
        <tr><th>Description</th><th>Qty</th><th>Rate</th><th>Amount</th></tr>
        {% for item in items %}
        <tr>
            <td>{{ item.description }}</td>
            <td>{{ item.quantity }}</td>
            <td>${{ "%.2f"|format(item.rate) }}</td>
            <td>${{ "%.2f"|format(item.quantity * item.rate) }}</td>
        </tr>
        {% endfor %}
    </table>
    <p class="total">Total: ${{ "%.2f"|format(total) }}</p>
</body>
</html>
"""

def create_invoice_html(data: dict, output_path: str):
    template = Template(invoice_template)
    
    # Calculate total
    total = sum(i['quantity'] * i['rate'] for i in data['items'])
    total *= (1 + data.get('tax_rate', 0))
    data['total'] = total
    
    html = template.render(**data)
    HTML(string=html).write_pdf(output_path)
    return output_path
```


## 最佳实践

1. **在生成发票前验证所有必填字段**；
2. **使用模板以确保品牌一致性**；
3. **自动计算总金额（不要依赖用户输入的数据）**；
4. **在发票中包含付款说明和条款**。

## 安装方法

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## 资源链接

- [easy-invoice-pdf仓库](https://github.com/nickmitchko/easy-invoice-pdf)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)