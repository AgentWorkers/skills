---
name: clarity-literature
description: 搜索研究论文并从 Clarity Protocol 获取出版物详细信息。当用户请求搜索研究论文、查找出版物、PubMed 参考文献、关于蛋白质的文献或引用详情时使用该功能。功能包括：搜索论文、通过 PMID 获取论文详细信息。
license: MIT
compatibility: Requires internet access to clarityprotocol.io. Optional CLARITY_API_KEY env var for 100 req/min (vs 10 req/min).
metadata:
  author: clarity-protocol
  version: "1.0.0"
  homepage: https://clarityprotocol.io
---
# Clarity 文献检索技能

该技能允许您从 Clarity Protocol 提供的文献数据库中搜索和检索研究论文。这些论文来源于 PubMed，并通过 Semantic Scholar 增强了引用指标信息。

## 快速入门

- 列出数据库中的所有论文：  
  ```bash
  ```bash
python scripts/search_papers.py
```
  ```

- 通过 PMID 获取特定论文的详细信息：  
  ```bash
  ```bash
python scripts/get_paper.py --pmid 12345678
```
  ```

- 以可读格式获取论文详细信息：  
  ```bash
  ```bash
python scripts/get_paper.py --pmid 12345678 --format summary
```
  ```

## 论文字段

每篇论文包含以下字段：  
- `pmid`：PubMed 标识符  
- `doi`：数字对象标识符（Digital Object Identifier）  
- `title`：论文标题  
- `first_author`：第一作者姓名  
- `publication_year`：发表年份  
- `journal`：期刊名称  
- `abstract`：论文摘要（如有提供）  
- `citation_count`：引用次数（来自 Semantic Scholar）  
- `influential_citations`：高影响力引用次数  
- `has_fulltext`：是否在 PubMed Central 提供全文  

## 使用限制  

- **匿名访问（无 API 密钥）**：每分钟 10 次请求  
- **使用 API 密钥**：每分钟 100 次请求  

要使用 API 密钥，请设置 `CLARITY_API_KEY` 环境变量：  
  ```bash
  ```bash
export CLARITY_API_KEY=your_key_here
python scripts/search_papers.py
```
  ```  
  您可以在 [https://clarityprotocol.io](https://clarityprotocol.io) 获取您的 API 密钥。  

## 错误处理  

- **404 Not Found**：指定的 PMID 对应的论文不存在于数据库中。  
- **429 Rate Limit**：您已超出使用限制。系统会显示需要等待的时间。  
- **500 Server Error**：API 服务器出现错误，请稍后再试。  
- **Timeout**：请求耗时超过 30 秒。  

## 分页  

论文列表支持分页。API 会返回 `next_cursor` 字段，表示是否有更多结果可用。  

## 使用场景  

- 查找与蛋白质变异相关的研究论文  
- 获取特定论文的引用指标  
- 检查论文是否提供全文  
- 为文献综述提取摘要  
- 为蛋白质研究构建参考文献列表