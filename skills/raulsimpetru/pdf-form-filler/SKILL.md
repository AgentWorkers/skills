---
name: pdf-form-filler
description: **使用编程方式将文本值和复选框填充到 PDF 表单中**  
当您需要将数据填充到可填写的 PDF 表单（如政府表格、申请表、调查问卷等）中时，可以使用此方法。该方法支持设置文本字段和复选框的外观状态，以确保它们在显示时能够正确呈现。
version: 0.2.0
---

# PDF表单填充工具

该工具可编程地为PDF表单填充文本值和复选框内容。它使用`pdfrw`库来设置表单字段的值，同时保留表单的外观样式，以确保在各种PDF阅读器中能够正确显示。

## 快速入门

使用一个包含字段名称及对应值的字典来填充PDF表单：

```python
from pdf_form_filler import fill_pdf_form

fill_pdf_form(
    input_pdf="form.pdf",
    output_pdf="form_filled.pdf",
    data={
        "Name": "John Doe",
        "Email": "john@example.com",
        "Herr": True,  # Checkbox
        "Dienstreise": True,
    }
)
```

## 主要功能

- **文本字段**：可以设置任何文本内容（如姓名、日期、地址等）。
- **复选框**：可以设置布尔值（选中时为`True`，未选中时为`False`或`None`）。
- **外观状态**：能够正确设置复选框的显示状态（`/On`或`/Off`）。
- **保持结构完整**：填充后表单仍可被进一步编辑。
- **无依赖库**：仅依赖轻量级的Python库`pdfrw`。

## 工作原理

1. 打开PDF模板文件。
2. 遍历所有表单字段。
3. 为匹配的字段名称设置相应的值。
4. 对于复选框，同时设置其值（`/V`）和外观状态（`/AS`）。
5. 保存填充后的PDF文件。

## 字段名称匹配规则

字段名称必须与PDF表单中显示的名称完全一致。常见字段名称示例：
- 德文表单：`Herr`（先生）、`Frau`（女士）、`Dienstreise`（出差）、`Geschäftsnummer LfF`（公司编号）。
- 英文表单：`Full Name`（全名）、`Email`（电子邮件）、`Agree`（同意）、`Submit`（提交）。
- 日期字段：`Date`（日期）、`DOB`（出生日期）、`Start Date`（开始日期）。

要获取PDF文件中的所有字段名称，可以使用`list_pdf_fields()`函数：

```python
from pdf_form_filler import list_pdf_fields

fields = list_pdf_fields("form.pdf")
for field_name, field_type in fields:
    print(f"{field_name}: {field_type}")
```

字段类型：
- `text`：文本输入字段
- `checkbox`：布尔型复选框
- `radio`：单选按钮
- `dropdown`：下拉菜单
- `signature`：签名字段

## 示例：求职申请表

```python
fill_pdf_form(
    input_pdf="job_application.pdf",
    output_pdf="job_application_filled.pdf",
    data={
        "Full Name": "Jane Smith",
        "Email": "jane.smith@example.com",
        "Phone": "555-1234",
        "Position": "Software Engineer",
        "Years Experience": "5",
        
        # Checkboxes
        "Willing to relocate": True,
        "Available immediately": False,
        "Background check consent": True,
    }
)
```

## 高级用法

### 部分填充

仅填充特定字段，其他字段保持空白：

```python
data = {"Name": "Jane Doe"}  # Only Name is set
fill_pdf_form("form.pdf", "form_filled.pdf", data)
```

### 动态字段检测

自动获取所有字段并提示用户输入值：

```python
from pdf_form_filler import list_pdf_fields

fields = list_pdf_fields("form.pdf")
data = {}
for field_name, field_type in fields:
    if field_type == "text":
        data[field_name] = input(f"Enter {field_name}: ")
    elif field_type == "checkbox":
        data[field_name] = input(f"Check {field_name}? (y/n): ").lower() == 'y'

fill_pdf_form("form.pdf", "form_filled.pdf", data)
```

### 批量填充

使用相同的数据批量填充多个PDF文件：

```python
import os
from pdf_form_filler import fill_pdf_form

data = {"Name": "John Doe", "Date": "2026-01-24"}

for filename in os.listdir("forms/"):
    if filename.endswith(".pdf"):
        fill_pdf_form(
            f"forms/{filename}",
            f"forms_filled/{filename}",
            data
        )
```

## 常见问题及解决方法

### 复选框无法正确显示

某些PDF阅读器可能不会立即显示复选框的状态。虽然值已正确设置（`/On`或`/Off`），但复选框的外观可能不会更新。可以尝试在以下软件中打开PDF文件：
- Adobe Reader（通常能正确显示复选框状态）
- Firefox（对表单的支持较好）
- Linux系统上的`evince`或`okular`阅读器（通常也能正常显示）。

### 无法找到字段名称

使用`list_pdf_fields()`函数确认字段名称是否正确。注意：
- 有些PDF表单的字段名称可能不直观（例如使用`Field_1`而非描述性名称）。
- 有些表单包含嵌套字段结构。

### 文本显示被截断

如果PDF表单中的文本字段宽度过窄，可以尝试：
- 使用更短的文本内容。
- 在PDF模板中减小字体大小。
- 填充完成后手动调整文本显示效果。

## 完整实现脚本

完整的实现代码请参见`scripts/fill_pdf_form.py`文件（使用`pdfrw`库编写）。