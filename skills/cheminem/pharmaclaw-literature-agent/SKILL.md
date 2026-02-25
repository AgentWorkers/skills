---
name: pharmaclaw-literature-agent
description: Literature mining agent v2.0.0 for novel drug discovery: PubMed/Semantic Scholar + ClinicalTrials Phase II/III + bioRxiv preprints. Novelty scoring, phase/FDA query boosts. Best for latest breakthroughs. Searches PubMed (NCBI E-utilities) and Semantic Scholar for papers related to compounds, targets, diseases, mechanisms, reactions, and catalysts. Returns structured results with titles, authors, abstracts, DOIs, MeSH terms, citation counts, TLDR summaries, and open-access PDFs. Supports paper lookup by DOI/PMID, citation tracking, and related paper discovery. Chains from any PharmaClaw agent (compound name, target, disease) and recommends next agents based on findings. No API keys required. Triggers on literature, papers, publications, PubMed, search papers, citations, references, what's published, research on, studies about, review articles, recent papers, state of the art.
---

# Literature Agent v1.0.0

## 概述

本工具采用双源文献搜索机制，结合了PubMed（专注于生物医学领域）和Semantic Scholar（覆盖更广泛的计算机科学、机器学习及人工智能领域）。系统能够消除数据重复，并通过引用指标和简短摘要（TLDR）对搜索结果进行丰富。

**主要功能：**
- 使用MeSH术语、摘要及出版物类型在PubMed中进行搜索；
- 在Semantic Scholar中搜索论文，同时提供引用次数、具有影响力的引用信息及简短摘要；
- 通过DOI或PMID查询论文详情；
- 跟踪论文的引用情况（哪些论文引用了该论文）；
- 发现与目标论文相关的其他论文；
- 根据化合物、靶点或疾病信息自动生成查询语句；
- 实现跨数据源的重复检测与数据整合。

## 快速入门

```bash
# Search by topic
python scripts/pubmed_search.py --query "KRAS G12C inhibitor" --max-results 5

# Search Semantic Scholar (includes ML/AI papers)
python scripts/semantic_scholar.py --query "graph neural network drug discovery"

# Full chain: compound + disease context
python scripts/chain_entry.py --input-json '{"compound": "sotorasib", "disease": "lung cancer"}'

# Look up a specific paper and find who cited it
python scripts/semantic_scholar.py --paper-id "DOI:10.1038/s41586-021-03819-2" --citations

# Recent papers only (last 3 years)
python scripts/pubmed_search.py --query "organometallic catalyst drug synthesis" --years 3
```

## 脚本

### `scripts/pubmed_search.py`
通过NCBI的E-utilities工具访问PubMed（公开API，无需密钥，请求速率限制为每秒3次）。

```
--query <text>          Required. Search query
--max-results <N>       1-50 (default: 10)
--sort <type>           relevance | date (default: relevance)
--years <N>             Limit to last N years
```

返回结果包括：PMID、标题、作者、期刊、发表年份、DOI、摘要、MeSH术语及关键词、出版物类型。

### `scripts/semantic_scholar.py`
使用Semantic Scholar的API进行搜索（公开API，无需密钥，请求速率限制为每5分钟100次）。

```
--query <text>          Search query
--paper-id <id>         Paper ID (DOI:xxx, PMID:xxx, ArXiv:xxx)
--related               Get references of a paper (requires --paper-id)
--citations             Get papers citing a paper (requires --paper-id)
--max-results <N>       1-50 (default: 10)
--year-range <range>    e.g., "2020-2026" or "2023-"
```

返回结果包括：论文标题、作者、发表年份、摘要、简短摘要（TLDR）、引用次数、具有影响力的引用信息、DOI以及ArXiv链接（如论文为开放获取格式）。

### `scripts/chain_entry.py`
该脚本实现了与PharmaClaw的标准接口，能够同时搜索PubMed和Semantic Scholar的数据，消除重复结果，并根据论文的引用影响力对结果进行排序。

输入参数：
- `query`：查询关键词
- `compound`/`name`：化合物名称/SMILES
- `target`：靶点名称
- `disease`：疾病名称
- `mechanism`：作用机制
- `reaction`：反应类型
- `topic`：研究主题
- `doi`：论文的DOI
- `pmid`：论文的PMID
- `max_results`：返回的最大结果数量
- `years`：搜索时间范围（年份）
- `context`：搜索上下文（如“化学查询”或“药理学验证”等）

示例查询语句：
`{"compound": "aspirin", "disease": "colorectal cancer"}` → 会搜索与“阿司匹林”和“结直肠癌”相关的研究论文。

## 数据链式处理流程

| 来源          | 输入参数            | 目标            |
|--------------|------------------|-------------------|
| 化学查询        | 化合物名称/SMILES       | **文献**         | 查找相关研究论文         |
| 催化剂设计      | 反应类型           | **文献**         | 查找催化剂优化相关论文       |
| **文献**        | 关键研究结果       | 药理学           | 验证研究结论         |
| **文献**        | 合成参考文献       | 化学查询         | 用于逆合成研究         |
| **文献**        | 专利提及         | 知识产权分析       | 用于专利挖掘           |