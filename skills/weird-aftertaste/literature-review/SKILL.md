---
name: literature-review
version: 1.2.0
description: 通过 Semantic Scholar、OpenAlex、Crossref 和 PubMed API 搜索学术资源，以协助撰写文献综述。当用户需要查找某个主题的相关论文、获取特定 DOI 的详细信息，或起草包含正确引用的文献综述章节时，可以使用这些工具。
---

# 文献综述

本工具支持使用多引擎搜索集成（Semantic Scholar (S2)、OpenAlex (OA)、Crossref (CR) 和 PubMed (PM) 来辅助撰写学术文献综述。

## 功能特点

- **多源搜索**：通过 Semantic Scholar (S2)、OpenAlex (OA)、Crossref (CR) 和 PubMed (PM) 查找相关学术论文。
- **完整摘要**：所有来源现在均返回论文的完整摘要（PubMed 使用 `efetch` 功能获取完整的 XML 记录）。
- **DOI 提取**：从所有来源中提取 DOI，以便进行交叉引用和去重处理。
- **自动去重**：在同时搜索多个来源时（使用 `--source all` 或 `--source both`），结果会通过 DOI 自动去重。
- **礼貌访问**：通过 `USER_EMAIL` 环境变量自动识别 OpenAlex/Crossref 的“礼貌访问”权限。
- **摘要重构**：能够从 OpenAlex 的倒排索引格式中重新生成摘要内容。
- **内容整合**：根据元数据将论文按主题分类，并起草综述章节。

## 环境变量

| 变量          | 用途                                      | 默认值            |
|----------------|-----------------------------------------|-------------------|
| `USER_EMAIL`     | 用于礼貌访问 API 的电子邮件地址                | `anonymous@example.org`     |
| `CLAWDBOT_EMAIL`    | 如果 `USER_EMAIL` 未设置时的备用地址                |                    |
| `SEMANTIC_SCHOLAR_API_KEY` | 可选的 Semantic Scholar API 密钥（可提高访问速率） |                    |
| `OPENALEX_API_KEY`    | 可选的 OpenAlex API 密钥                    |                    |

## 工作流程

### 1. 全面搜索（所有数据库）
从所有主要的学术数据库中获取全面的论文列表。结果会通过 DOI 自动去重。
```bash
python3 scripts/lit_search.py search "impact of glycyrrhiza on bifidobacterium" --limit 5 --source all
```

### 2. 定向搜索
- **OpenAlex** (`oa`）：搜索速度快，摘要质量高。
- **Semantic Scholar** (`s2`）：提供高质量的引用数据和简短摘要（TL;DR）。
- **Crossref** (`cr`）：基于 DOI 的精确元数据（不提供摘要）。
- **PubMed** (`pm`）：生物医学研究的黄金标准，提供完整摘要和 PMID。

```bash
python3 scripts/lit_search.py search "prebiotic effects of liquorice" --source pm
```

### 3. 比较多个来源
同时搜索 S2 和 OA，确保不会遗漏任何论文。结果默认会自动去重。
```bash
python3 scripts/lit_search.py search "Bifidobacterium infantis growth" --source both
```

### 4. 获取详细信息（S2）
检索包含简短摘要（TL;DR）的详细元数据。
```bash
python3 scripts/lit_search.py details "DOI:10.1016/j.foodchem.2023.136000"
```

### 5. 撰写综述
1. **提取关键内容**：从找到的摘要中提取关键信息。
2. **组织内容**：将提取的信息按逻辑结构（如时间顺序或主题）进行分类。
3. **起草综述**：采用“逐步思考”的方法，将多个来源的信息整合成连贯的叙述。

## 输出格式
每个搜索结果包含以下信息：
- `id`：来源特定的标识符（PubMed 的 PMID、OpenAlex 的 ID、S2 论文的 ID、Crossref 的 DOI）。
- `doi`：可用的 DOI（用于去重）。
- `title`：论文标题。
- `year`：发表年份。
- `authors`：作者列表。
- `abstract`：完整摘要文本（如有提供）。
- `venue`：期刊或会议名称。
- `citationCount`：引用次数（S2、OA）。
- `source`：结果来自的数据库。

## 成功撰写综述的技巧
- **引用**：务必通过 DOI 或 PMID 进行交叉引用，以确保参考文献的准确性。
- **筛选**：优先选择引用次数较多或发表年份较新的论文，以获得更现代的综述内容。
- **医学领域**：使用 `--source pm` 选项可获取最可靠的生物医学文献。
- **去重**：多源搜索会自动去除重复结果；如需原始引用次数，可单独使用某个数据库。