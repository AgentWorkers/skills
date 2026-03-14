---
name: accounting-finance-system-research
description: 研究和解决与会计和财务软件系统（如ERP、GL、AP/AR、计费、结账以及报告工具）相关的问题。当用户需要了解特定系统的操作步骤、设置指南或故障排除帮助时，可以使用这种方法，并将结果以快速备忘录或简单的问答文档（DOCX格式）的形式记录下来。
---
# 会计与财务系统研究

## 概述

系统支持的工作流程如下：收集相关信息，提出澄清性问题，确认输出格式，确认理解情况，研究外部指导资料，分析最佳解决方案，并生成 DOCX 格式的交付成果。

## 必须遵循的行为规范

- 在提出解决方案之前，先提出澄清性问题。
- 确认输出内容应该是“快速备忘录”还是“简单问答”格式。
- 在进行网络搜索之前，先重新陈述自己的理解并等待用户的确认。
- 在获得确认后，开始在网上进行研究，优先参考官方供应商的指导资料。
- 将基于官方来源的指导内容与个人假设或推断区分开来。
- 在交付成果中包含来源链接及访问日期。
- 生成用户选择的 DOCX 格式的报告。

## 工作流程

### 1) 收集需求与明确范围

- 用一句话概括用户的目标。
- 确认系统的名称及版本/版本号（例如：NetSuite、SAP S/4HANA Cloud、Dynamics 365 Finance、QuickBooks）。
- 明确需要处理的模块或工作流程领域（例如：应付账款、应收账款、对账、报表生成）。
- 了解用户的角色/权限限制以及任何时间压力。

### 2) 提出澄清性问题（必填）

- 参考 [references/clarification-question-bank.md](references/clarification-question-bank.md) 中提供的问题库。
- 仅提出必要的关键问题，避免重复提问。
- 在收集到足够的信息之前，暂停解决方案的制定。
- 如果某些信息仍然未知，可以基于现有假设提供有条件的指导。

### 3) 确认输出格式（必填）

- 请用户选择以下格式之一：
- “快速备忘录”：包含建议和具体步骤的简洁专业总结。
- “简单问答”：以编号形式呈现的直接答案。
- 仅在用户未明确选择时，默认使用“快速备忘录”格式。

### 4) 确认用户理解情况（必填）

- 重新说明：
  - 问题描述
  - 系统背景
  - 仍存在的疑问或假设
  - 选择的输出格式
- 在开始研究之前，请求用户的明确确认。

### 5) 研究外部指导资料

- 按照 [references/source-priority.md](references/source-priority.md) 中列出的优先级顺序查找资料来源。
- 尽可能收集至少两个相关的参考资料。
- 如果有官方供应商的资料，请务必包含在内。
- 记录每个资料的元数据：标题、发布者、URL、更新/发布日期以及访问日期。
- 优先选择针对当前版本的特定指导内容，而非过时的通用资料。

### 6) 分析并制定建议

- 将研究结果转化为用户可执行的操作步骤。
- 说明每个操作步骤所需的先决条件和权限。
- 当主要解决方案不可行时，提供备用方案。
- 包含验证步骤以确保操作的正确完成。
- 指出可能存在的风险及未解决的依赖关系。

### 7) 生成 DOCX 格式的交付成果

- 使用 [references/report-json-schema.md](references/report-json-schema.md) 中定义的 JSON 格式生成输入数据。
- 运行以下代码块：

```bash
python scripts/build_system_guidance_docx.py \
  --input-json <analysis.json> \
  --output-docx <system-guidance.docx> \
  --format <memo|q-and-a>
```

- 将“快速备忘录”内容转换为相应的 DOCX 格式。
- 将“简单问答”内容转换为相应的 DOCX 格式。
- 确保文档包含以下内容：
  - 任务摘要和系统背景
  - 澄清的问题和假设
  - 参考资料的链接
  - 建议的操作步骤
  - 验证检查内容
  - 存在的风险及未解决的问题

### 8) 质量检查

- 确保建议内容与参考资料一致。
- 确保所有假设都明确且易于理解。
- 确认交付成果的格式符合用户要求。
- 确保所有参考资料都有对应的 URL 和访问日期。
- 确保输出文件为 `.docx` 格式且可正常阅读。

## 可用资源

- 澄清问题清单：[references/clarification-question-bank.md](references/clarification-question-bank.md)
- 资料来源优先级排序：[references/source-priority.md](references/source-priority.md)
- 报告 JSON 架构：[references/report-json-schema.md](references/report-json-schema.md)
- 报告示例输入文件：[references/example_report_input.json]
- DOCX 生成工具：`scripts/build_system_guidance_docx.py`

## 依赖项

（如需安装相关工具，请执行以下代码块：）

```bash
python -m pip install --user python-docx
```