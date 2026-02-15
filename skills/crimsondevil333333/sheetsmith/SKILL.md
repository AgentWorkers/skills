---
name: sheetsmith
description: 基于Pandas的CSV和Excel管理工具，支持快速预览、数据汇总、过滤、数据转换以及格式转换。无论何时你需要查看电子表格文件、计算列级统计数据、应用查询或表达式，或者将处理后的数据导出为新的CSV/TSV/XLSX格式文件（而无需每次都重新编写Pandas代码），都可以使用这个工具。
---

# Sheetsmith

## 概述
Sheetsmith 是一个轻量级的 pandas 包装工具，专注于处理 CSV/Excel 文件：可以在一个地方预览、描述、过滤、转换和转换这些文件。其命令行接口（CLI）位于 `skills/sheetsmith/scripts/sheetsmith.py`，能够自动加载任何 CSV/TSV/Excel 文件，报告文件的结构元数据，执行 pandas 表达式，并将结果安全地写入新文件。

## 快速入门
1. 将电子表格（CSV、TSV 或 XLS/XLSX 格式）放入工作目录中，或通过完整路径引用它。
2. 运行 `python3 skills/sheetsmith/scripts/sheetsmith.py <command> <path>`，其中 `<command>` 是下面列出的命令之一。
3. 修改数据后，可以选择使用 `--output new-file` 保存副本，或使用 `--inplace` 直接覆盖源文件。
4. 查看 `references/usage.md` 以获取更多示例命令和技巧。

## 命令
### summary
打印行数/列数、数据类型分布、包含缺失数据的列以及数据的前几行/最后几行的预览。使用 `--rows` 控制摘要后显示的行数，使用 `--tail` 查看数据的最后几行而非前几行。

### describe
执行 `pandas.DataFrame.describe(include='all')`（可通过 `--include` 自定义），以便立即查看数值统计信息、数据类型和频率分布。添加 `--percentiles` 可以显示百分位数。

### preview
快速查看数据的前几行（`--rows`）或最后几行（`--tail`），以便在采取进一步操作前检查列顺序和格式是否正确。

### filter
通过 `--query` 输入 pandas 查询语句（例如 `state == 'CA' and population > 1e6`）。该命令可以打印过滤后的数据，或者通过 `--output` 将结果写入新的 CSV/TSV/XLSX 文件。使用 `--sample` 可以查看随机子集而非全部数据。

### transform
创建新列、重命名或删除现有列，并立即查看转换后的表格。提供一个或多个 `--expr` 表达式（如 `total = quantity * price`）。使用 `--rename old:new` 和 `--drop column` 来调整表格结构，并通过 `--output` 或 `--inplace` 保存更改。预览版本（不写入文件）会使用与其他命令相同的 `--rows`/`--tail` 参数。

### convert
在支持的格式（CSV/TSV/Excel）之间进行转换。务必指定目标格式的扩展名（如 `--output csv`），脚本会自动选择合适的写入器（Excel 使用 `openpyxl`，CSV 保留逗号分隔符，TSV 使用制表符）。这是在进行其他操作前标准化数据的最简单方法。

## 工作流程规则
- 始终保留原始文件的副本或将其写入新路径；只有在使用 `--inplace` 时脚本才会覆盖原始文件。
- 使用相同的 CLI 进行数据探索（`summary`、`preview`、`describe`）和编辑（`filter`、`transform`）。`--output` 参数适用于过滤和转换操作，便于分离处理结果。
- 脚本内部依赖 pandas 和 `tabulate` 来生成 Markdown 预览，同时支持 Excel/CSV/TSV 格式，因此请确保系统中已安装这些依赖库（pandas、openpyxl、xlrd、tabulate）。
- 如果基本命令描述不足以满足需求，请参考 `references/usage.md` 以获取更多示例（多步骤数据清洗、数据集比较、表达式技巧等）。

## 参考资料
- **使用指南：** `references/usage.md`（包含可直接复用的命令、表达式模式和数据集清洗方法）。

## 资源
- **GitHub：** https://github.com/CrimsonDevil333333/sheetsmith
- **ClawHub：** https://www.clawhub.ai/skills/sheetsmith