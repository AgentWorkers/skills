---
name: citation-verifier
description: 验证、规范并丰富单个引用或论文标识符。当用户粘贴 DOI、URL、arXiv ID、PubMed ID、引用字符串或论文标题并希望对其进行检查时，可以使用此功能。
---
# 引用验证器

当用户希望快速验证或规范单个论文引用时，可以使用此技能，而无需进行完整的文献搜索。

## 工作流程

1. 接收用户提供的任何信息：DOI、URL、arXiv ID、PubMed ID、引用字符串或部分标题。
2. 使用原始输入调用 `verify_citation` 函数进行验证。
3. 如果验证成功，使用解析后的标识符调用 `fetch` 函数获取完整的论文记录。
4. 显示规范化的结果。

## 输出格式

返回一个结构清晰的信息卡片，包含以下内容：

- **标题** — 论文的完整标题
- **作者** — 前三名作者；如果作者较多，则使用 “et al.” 表示
- **年份** — 发表年份
- **出版物** — 期刊或会议名称
- **DOI** — 如果可用，则显示规范的 DOI
- **标识符** — 其他相关标识符（如 arXiv、PubMed、Semantic Scholar）
- **状态** — 引用是否验证成功，或是否存在问题

如果验证失败或结果不明确，请明确告知用户，并建议他们可以尝试的方法（例如提供更完整的标题或不同的标识符）。

## 工具使用指南

### 使用 `verify_citation`

请始终首先调用此函数。它支持以下类型的输入：
- DOI 字符串（无论是否带有解析前缀）
- arXiv ID（例如：`2301.12345`、`arXiv:2301.12345`）
- PubMed ID
- 来自出版商网站、Semantic Scholar 或 Google Scholar 的完整或部分 URL
- 自由文本形式的引用字符串（例如：“Smith et al. 2020, Neural networks for...”）

### 使用 `fetch`

在验证成功后调用此函数，以获取论文的完整记录，包括摘要、引用次数和出版物详细信息。

### 不推荐使用的功能

- `search_literature` — 该技能用于已知引用的验证，而非主题发现
- `get_citation_graph` — 用户需要的是引用验证，而非引用关系图谱的探索

## 示例

- 用户输入：`10.1038/s41586-021-03819-2`
- 用户输入：`https://arxiv.org/abs/2301.12345`
- 用户请求：`验证这个引用：Vaswani et al., Attention Is All You Need, NeurIPS 2017`
- 用户询问：`这个 DOI 是否有效？10.1234/fake.doi.000`
- 用户输入来自 Semantic Scholar 或 Google Scholar 的 URL