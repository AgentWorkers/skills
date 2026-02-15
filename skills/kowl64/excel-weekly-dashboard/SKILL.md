---
name: excel-weekly-dashboard
description: 设计可刷新的 Excel 仪表板（使用 Power Query、结构化表格、数据验证以及数据透视报告功能）。当您需要一个每周更新的 KPI 工作簿，并且希望该工作簿能够通过文件自动更新、同时尽量减少人工干预时，可以使用这种方法。
---

# 大规模使用的Excel周度仪表板

## 目的  
设计可刷新的Excel仪表板（结合Power Query、结构化表格、数据验证和数据透视功能）。

## 使用场景  
- **需求**：  
  - 为该文件构建一个Power Query数据管道，实现每周自动刷新，无需人工干预。  
  - 将数据转换为结构化表格，并添加数据验证规则和清晰的数据输入规范。  
  - 创建一个基于数据透视功能的周度仪表板，支持按年份和ISO周进行筛选。  
  - 修复Excel模型，确保在新增列时数据刷新仍能正常进行。  
  - 设计一个可复用的KPI报告包，该报告包能从CSV文件文件夹中自动更新数据。  

- **不适用场景**：  
  - 需要高级预测/估值建模（此技能适用于重复性报告流程）。  
  - 需要使用BI工具（如Power BI或Tableau）而非Excel。  
  - 需要通过网页抓取方式获取数据。  

## 输入内容  
- **必填项**：  
  - 数据源文件（CSV、XLSX、DOCX或PDF格式）；“周”的定义（建议使用ISO周）以及所需的KPI字段。  
- **可选项**：  
  - 数据字典/列定义；已知的数据错误模式（例如空PayNumber字段、无效日期）。  
  - 需要重构的现有工作簿。  
- **示例**：  
  - 包含每周CSV文件的文件夹（例如：`exports/2026-W02/*.csv`）；  
  - 每月列内容都会变化的单一XLSX文件。  

## 输出内容  
- **仅请求计划时**：提供详细的构建步骤、Power Query脚本、表格布局及数据验证规则。  
- **请求生成实际成果时**：  
  - `workbook_spec.md`（工作簿结构及命名表格的文档）  
  - `power_query_steps.pq`（Power Query数据管道的M代码模板）  
  - `refresh-checklist.md`（用于检查数据刷新状态的文档，位于`assets/`目录下）  

**成功标准**：  
  - 新添加数据后，仪表板能自动刷新且无需人工编辑；  
  - 数据验证机制能有效识别并处理错误数据。  

## 工作流程  
1. 确定数据源类型（CSV/XLSX/DOCX/PDF）及关键业务字段（如PayNumber）。  
2. 定义标准表格结构：  
  - 明确所需列、数据类型、允许的值以及未知值的处理方式。  
3. 设计数据导入流程（使用Power Query）：  
  - 建议使用文件夹导入方式，并设置缺失列的处理逻辑。  
  - 规范化列名（去除多余字符、统一大小写、合并空格）。  
4. 设计数据清洗与验证流程：  
  - 创建`Data_Staging`查询（原始数据清洗）和`Data_Clean`查询（数据验证）。  
  - 添加验证字段（如`IsValidPayNumber`、`IsValidDate`、`IssueReason`）。  
5. 构建报表层：  
  - 基于`Data_Clean`结果生成数据透视表，并添加筛选器（按年份、ISO周等维度）。  
6. 添加“刷新状态”工作表：  
  - 显示上次刷新时间、行数、查询错误信息以及当前处理的周数。  

**注意事项**：  
- 在开始工作前，请确认以下内容：  
  - 是否指定了所需的KPI和列；  
  - 数据源文件是否包含关键业务字段；  
  - 周的定义和时区规则是否明确；  
  - 是否需要用户提供可可靠提取数据的PDF/DOCX文件格式。  

## 输出格式说明  
- 在生成计划时，请使用以下模板：  
```text
WORKBOOK PLAN
- Sheets:
  - Data_Staging (query output)
  - Data_Clean (query output + validation flags)
  - Dashboard (pivots/charts)
  - Refresh_Status (counts + health checks)
- Canonical Schema:
  - <Column>: <Type> | Required? | Validation
- Power Query:
  - Query 1: Ingest_<name> (Folder/File)
  - Query 2: Clean_<name>
  - Key transforms: <bullets>
- Validation rules:
  - <rule> -> <action>
- Pivot design:
  - Rows/Columns/Values
  - Slicers
```  

**若需生成实际成果，请同时提供以下文件：**  
- `assets/power-query-folder-ingest-template.pq`（数据导入模板）  
- `assets/refresh-checklist.md`（刷新状态检查文档）  

**安全与特殊处理**：  
- 默认情况下，仅提供计划文档和代码片段；用户明确请求时才生成完整文件。  
- 严禁删除或覆盖用户文件；建议为输出文件指定新的文件名。  
- 为确保系统稳定性，务必包含行数检查及错误提示功能。  
- 对于PDF/DOCX格式的数据源，需用户提供可提取的CSV/XLSX文件，否则需明确提示提取风险。  

**示例**：  
- **输入**：“包含PayNumber、Name、Date字段的每周CSV文件文件夹。”  
- **输出**：数据导入模板、表格结构、刷新状态检查文档以及仪表板构建方案。  
- **输入**：“新增列后数据刷新失败。”  
- **输出**：针对缺失列的防护逻辑、列名规范化方案以及表格结构设计文档。