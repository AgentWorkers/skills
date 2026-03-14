---
name: technical-accounting-research
description: 研究特定交易的技术会计处理方法以及财务报表的披露要求，参考美国通用会计准则（GAAP）和证券交易委员会（SEC）的相关规定。当用户询问如何对某笔交易进行会计处理、需要哪些会计分录、如何进行报表编制或信息披露时，或者需要以备忘录、电子邮件或问答文档（DOCX格式）的形式提供会计相关资料时，可参考本内容。
---
# 技术会计研究

## 概述

通过固定的流程处理与交易相关的会计问题：收集事实、确认输出格式、在线查找相关指导、应用会计准则，并生成 DOCX 格式的报告。

## 必须遵循的行为规范

- 在进行分析之前，提出需要澄清的问题。
- 确认所需的输出格式：`备忘录`（memo）、`电子邮件`（email）或 `问答形式`（q-and-a）。
- 即使某些指导内容看起来很熟悉，也应在得出最终结论之前先进行网络搜索。
- 区分权威性指导与解释性指导。
- 在最终成果中注明引用来源的链接及访问日期。
- 当某些事实尚不明确时，应明确说明所做出的假设。

## 工作流程

### 1. 问题收集与范围界定

- 用一句话概括用户的问题。
- 确认报告的基础和适用范围（例如：`美国公认会计原则`（US GAAP）、`证券交易委员会（SEC）的文件提交状态`，以及报告内容是针对上市公司还是私营公司）。
- 确认报告期间和重要性标准。

### 2. 澄清问题（必填）

- 参考 [references/clarification-question-bank.md](references/clarification-question-bank.md) 中提供的问题库。
- 仅提出与实际情况相关的问题，不要遗漏关键信息。
- 在收集到足够的事实以形成合理的结论之前，暂停分析。
- 如果事实仍然不完整，应基于明确的假设继续进行分析，并附上敏感性说明。

### 3. 确认输出格式（必填）

- 询问所需的输出格式：`备忘录`（用于正式文档）、`电子邮件`（用于简洁沟通）或 `问答形式`（用于直接回答问题）。
- 如果用户没有指定偏好，默认使用 `备忘录` 格式。

### 4. 查找指导资料

- 根据 [references/source-priority.md](references/source-priority.md) 中规定的优先级和可靠性规则来查找资料来源。
- 优先选择主要和权威性的资料来源（如 FASB/SEC/AICPA 的标准制定文件）。
- 可以使用四大会计师事务所（Big 4）的出版物作为解释性参考，但不要将其作为唯一依据。
- 记录每个引用来源的标签和网址。

### 5. 技术分析

- 明确会计问题的核心内容。
- 将收集到的事实与会计中的确认、计量、列报和披露要求进行对照。
- 评估各种可行的处理方案，并解释拒绝某些方案的理由。
- 最后提出推荐的会计处理方法、披露内容以及潜在风险。
- 在适用的情况下，提供分录示例以帮助实际操作。

### 6. 起草并生成 DOCX 报告

- 使用 [references/report-json-schema.md](references/report-json-schema.md) 中定义的 JSON 格式来构建报告内容。
- 运行以下脚本：

```bash
python scripts/build_accounting_report_docx.py \
  --input-json <analysis.json> \
  --output-docx <technical-accounting-report.docx> \
  --format <memo|email|q-and-a>
```

- 该脚本会生成一个 DOCX 文件，其中包含：
- 报告的标题和元数据。
- 收集到的事实及问题描述。
- 包含链接的指导资料表格。
- 分析结果和结论。
- 关于信息披露的注意事项。
- 未解决的问题及所做的假设。

### 7. 质量检查

- 确认结论与参考的指导原则一致。
- 确保所有重要的假设都被明确披露。
- 确认输出格式符合用户的要求。
- 确保报告中列出了所有分析中使用的外部资料来源的网址。

## 可用资源

- 问题澄清清单：[references/clarification-question-bank.md](references/clarification-question-bank.md)
- 资料来源的优先级和引用规则：[references/source-priority.md](references/source-priority.md)
- 用于生成 DOCX 的 JSON 格式：[references/report-json-schema.md](references/report-json-schema.md)
- 报告示例数据：[references/example_report_input.json](references/example_report_input.json)
- DOCX 生成工具：`scripts/build_accounting_report_docx.py`

## 依赖项

如有需要，请安装以下软件：

```bash
python -m pip install --user python-docx
```