---
name: office-document-specialist-suite
description: 这是一个用于创建、编辑和分析 Microsoft Office 文档（Word、Excel、PowerPoint）的高级工具套件。它提供了专门的工具，用于自动化报告生成和文档管理。
metadata:
  {
    "openclaw": {
      "emoji": "📄",
      "requires": { "bins": ["python3"], "pip": ["python-docx", "openpyxl", "python-pptx"] }
    }
  }
---
# Office Document Specialist Suite

一套专为专业文档处理设计的工具集。

## 功能

- **Word (.docx)**：创建和编辑专业报告，管理样式，插入表格/图片。
- **Excel (.xlsx)**：数据分析，自动生成电子表格，支持复杂的格式设置。
- **PowerPoint (.pptx)**：根据结构化数据自动生成幻灯片。

## 使用方式

该工具集中的每个工具均可通过代理程序或提供的 CLI 脚本进行编程调用。

## 安装

运行随附的 `setup.sh` 脚本，以初始化 Python 虚拟环境并安装所需依赖项。