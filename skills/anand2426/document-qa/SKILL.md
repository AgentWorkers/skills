---
name: document-qa
description: "根据上传的文档（PDF、DOCX、TXT格式）内容回答问题，支持处理单个文件或整个文件夹。"
---
# 文档问答技能

该技能允许您上传文档（PDF、DOCX、TXT格式），并针对文档内容提出问题。

## 使用方法

要使用此技能，请运行 `run_qa.py` 脚本，传入文档的路径或文件夹路径以及您的问题。该技能会从支持的文件类型（PDF、DOCX、TXT）中提取文本，并将这些文本作为回答问题的依据。

**命令格式：**
`python ~/.openclaw/workspace/skills/document-qa/scripts/run_qa.py "<文件或文件夹路径>" "<您的问题>"`

**示例：**
*   询问单个 PDF 文件的内容：
    `python ~/.openclaw/workspace/skills/document-qa/scripts/run_qa.py "C:\Users\anandraj\.openclaw\workspace\my_docs\report.pdf" "主要结论是什么？"`
*   询问文件夹中的所有文档内容：
    `python ~/.openclaw/workspace/skills/document-qa/scripts/run_qa.py "C:\Users\anandraj\.openclaw\workspace\project_docs" "总结项目目标。"`

系统会提取所有相关文本，并将其与您的问题一起呈现出来，以便我根据提供的内容生成答案。

## 支持的文档类型

*   PDF (.pdf) **（需要安装 'iyeque-pdf-reader-1.1.0' 技能）**
*   Microsoft Word (.docx)
*   纯文本 (.txt)
*   Microsoft Excel (.xlsx)

**注意：**
*   要支持 PDF 格式的文档，请确保您的工作空间中已安装了 `iyeque-pdf-reader-1.1.0` 技能。
*   如果您的环境中尚未安装 `pandas` 和 `openpyxl` 库，可能需要先安装它们：
    `pip install pandas openpyxl`