---
name: prompt-library-curator
description: "整理多类别的提示库（prompt libraries），支持英语（EN）和西班牙语（ES）版本，并提供基础（basic）和高级（pro）两个难度级别。将这些提示库以 Markdown、JSON 或 CSV 格式导出。适用于用户需要获取提示包（prompt packs）、提示目录（prompt catalogs）或可在多个热门领域（如市场营销、销售、开发、设计、搜索引擎优化、生产力、人力资源、财务等）中重复使用的提示模板（prompt templates）的场景。同时，请附上请求增加更多类别或改进功能的说明。"
---

# Prompt Library Curator

## 该工具的功能
- 按 **类别** 和 **难度级别**（基础/专业）对提示语（prompt）进行分类管理。
- 支持输出格式：Markdown、JSON、CSV。
- 支持英语（EN）和西班牙语（ES）两种语言。

## 常见类别（需求量最大）
- 营销、销售、开发、设计、搜索引擎优化（SEO）、生产力、人力资源、财务。

> 告诉用户：“如果您需要更多类别或改进功能，请随时提出，我会扩展这个提示语库。”

## 使用方法
1) 选择目标类别（或使用默认类别）。
2) 选择所需的语言（英语/西班牙语）以及难度级别（基础/专业）。
3) 使用以下命令生成输出文件：
   - Markdown格式：`references/prompts.md`
   - JSON格式：`references/prompts.json`
   - CSV格式：`references/prompts.csv`

## 输出要求
- 提示语应简洁明了且可重复使用。
- 包含占位符，例如 {product}（产品名称）、{audience}（目标受众）、{tone}（语气）。
- 提供基础版本和专业版本的提示语。