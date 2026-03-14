---
name: form-1040-review
description: 审核最近一个纳税年度的美国个人所得税申报表（Form 1040/1040-SR），将申报表中的主要项目与当年的税法规定进行对比；如果提供了多个年度的申报表，还需检查这些申报表之间的数据一致性；生成独立的 DOCX 风险登记文件，并根据申报表内容估算审计的可能性。该工具适用于涉及 1040 表格合规性审核、多年数据一致性分析、税法验证或审计风险评估的任务。
---
# 1040表格审核

## 概述

对提供的数据集中最新纳税年度的标准化1040表格数据进行结构化审核。生成三个结果文件：一个详细的审核结果JSON文件、一个Markdown格式的总结报告，以及一个独立的DOCX格式的风险报告，其中列出了主要问题及相关风险。

## 快速入门

1. 使用[references/input_schema.json](references/input_schema.json)准备标准化的输入JSON数据。
2. 在使用之前，确认[references/current_tax_law_2025.json](references/current_tax_law_2025.json)中规定的现行法律参数。
3. 运行以下命令：

```bash
python scripts/review_1040.py --input <normalized_returns.json> --output-dir output/form-1040-review
```

4. 查看输出文件：
- `review_summary.md`
- `review_findings.json`
- `form-1040-risk-report.docx`

## 工作流程

### 1. 确定当前纳税年度的表格
- 从输入数据中选择最高的`tax_year`作为当前纳税年度的表格。
- 将所有之前的年份视为历史对比数据。

### 2. 进行当前年度的法律检查
- 验证表格中的内部算术运算及各项数据之间的逻辑关系。
- 将当前年度的主要项目与法律规定进行对比：
  - 根据申报状态和年龄计算标准扣除额。
  - 在没有优惠收入的情况下，计算普通税率下的税款。
  - 儿童税收抵免（Child Tax Credit）和ACTC（Additional Child Tax Credit）的限额。
  - 自雇税（Self-employment Tax）和额外医疗保险税（Additional Medicare Tax）的门槛。

### 3. 进行多年数据一致性检查
- 将当前年度的表格与最近的前一年数据进行对比。
- 标记工资、调整后总收入（AGI）、应纳税收入、税收抵免、税款支付以及退税/欠款金额的显著变化。
- 标记申报状态和受抚养人数量的变化，并进行说明。

### 4. 生成风险报告
- 生成一个结构化的审核结果文件（`review_findings.json`）。
- 生成一个易于阅读的总结报告（`review_summary.md`）。
- 生成一个独立的DOCX格式风险报告（`form-1040-risk-report.docx`），列出每个主要问题、问题的严重程度、观察结果以及建议的补充文件。
- 根据审核结果和表格的复杂性，估算审计的可能性。

## 输入数据

使用[references/input_schema.json](references/input_schema.json)中的标准化数据结构。至少需要包含以下字段：
- `tax_year`（纳税年度）
- `filing_status`（申报状态）
- `major_items`（1040表格中的核心项目，如调整后总收入、扣除额、应纳税收入、税款、税款支付、退税/欠款金额）

请参考[references/major_items_reference.md](references/major_items_reference.md)以获取字段的规范映射。

## 法律依据

- 当纳税年度发生变化或IRS发布修订内容时，及时更新[references/current_tax_law_2025.json](references/current_tax_law_2025.json)。
- 数值阈值请严格使用IRS/SSA的官方规定。
- 如果法律数据早于所分析的纳税年度，请将结果标记为过时数据，并在最终确认前手动更新。

## 脚本

`scripts/review_1040.py`脚本负责执行以下任务：
- 当前年度的算术运算和法律检查。
- 多年数据的一致性检查。
- 基于审核结果进行风险评分。
- 使用`python-docx`生成DOCX格式的风险报告。

如果`python-docx`未安装，请先进行安装：

```bash
python scripts/review_1040.py --input <normalized_returns.json> --output-dir output/form-1040-review
```

## 输出解读

- 将审核结果视为风险信号，而非最终的法律判定。
- 声明申报决策需由注册会计师（CPA）或税务专家（EA）进行审核。
- 所提供的审计可能性是基于表格模式和发现的问题得出的初步估计，并不构成法律保证。

## 示例命令

```bash
python scripts/review_1040.py \
  --input references/example_returns.json \
  --output-dir output/form-1040-review
```