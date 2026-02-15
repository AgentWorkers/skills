---
name: office-mcp
description: MCP服务器：通过人工智能支持Word、Excel和PowerPoint文件的操作
author: claude-office-skills
version: "1.0"
tags: ['mcp', 'office', 'word', 'excel', 'powerpoint']
models: [claude-sonnet-4, claude-opus-4]
tools: [computer, code_execution, file_operations]
library:
  name: Office MCP
  url: https://github.com/anthropics/skills
  stars: N/A
---

# Office Mcp Skill

## 概述

该技能将Office文档操作封装为MCP工具，使Claude能够通过标准化的接口创建、编辑和操作Word、Excel和PowerPoint文件。

## 使用方法

1. 说明您想要完成的任务。
2. 提供所需的输入数据或文件。
3. 我将执行相应的操作。

**示例提示：**
- “使用AI生成的内容创建Word文档”
- “使用公式制作Excel电子表格”
- “生成PowerPoint演示文稿”
- “批量编辑Office文档”

## 领域知识


### Office MCP工具

| 工具 | 输入 | 输出 |
|------|-------|--------|
| `create_docx` | 标题、章节、样式 | .docx文件 |
| `edit_docx` | 文件路径、修改内容 | 更新后的.docx文件 |
| `create_xlsx` | 数据、公式 | .xlsx文件 |
| `create_pptx` | 幻灯片、布局 | .pptx文件 |

### 与Claude技能的集成

```markdown
# Example: Combining Skills + MCP

User: "Create a sales report from this data"

1. Data Analysis Skill → Analyze data
2. office-mcp/create_docx → Generate Word report
3. office-mcp/create_xlsx → Generate Excel summary
4. office-mcp/create_pptx → Generate PowerPoint deck
```

### MCP服务器实现

```python
from mcp import Server
from docx import Document
from openpyxl import Workbook

server = Server("office-mcp")

@server.tool("create_docx")
async def create_docx(title: str, content: str, output_path: str):
    doc = Document()
    doc.add_heading(title, 0)
    doc.add_paragraph(content)
    doc.save(output_path)
    return {"status": "success", "path": output_path}

@server.tool("create_xlsx")
async def create_xlsx(data: list, output_path: str):
    wb = Workbook()
    ws = wb.active
    for row in data:
        ws.append(row)
    wb.save(output_path)
    return {"status": "success", "path": output_path}
```


## 最佳实践

1. 在执行文档操作之前验证输入数据。
2. 对于大型文档，使用临时文件。
3. 返回包含文件路径的结构化响应。
4. 以有意义的方式优雅地处理错误。

## 安装

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## 资源

- [Office MCP仓库](https://github.com/anthropics/skills)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)