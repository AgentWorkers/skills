---
name: scihub-paper-downloader
description: "从 Sci-Hub 下载学术论文。给定一个 DOI（Digital Object Identifier），返回该论文的 PDF 下载链接。"
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["python3"] } } }
allowed-tools: ["exec"]
---
# Sci-Hub 论文下载器

通过论文的 DOI（Digital Object Identifier）从 Sci-Hub 获取 PDF 下载链接。系统会自动尝试访问官方镜像站点（sci-hub.se、sci-hub.st、sci-hub.ru）。

## 使用方法

```
python3 {baseDir}/scihub-paper-downloader.py <DOI>
```

输出 JSON 格式的数据：

```json
{"doi": "10.xxx", "pdf_url": "https://...", "mirror": "https://sci-hub.st", "status": "found"}
```

- 当找到 PDF 下载链接时，`status` 的值为 `found`；
- 当所有镜像站点均无法访问时，`status` 的值为 `not_found`。

## 下载 PDF

该工具仅返回 PDF 下载链接。您可以使用 `curl` 命令来下载文件：

```
curl -L -o paper.pdf "<pdf_url>"
```

## 查找论文

在使用该工具之前，您可以先通过以下方式查找论文的 DOI：

- **Web 搜索** — 适用于一般性的查询，速度较快；
- **Google Scholar** (`site:scholar.google.com`) — 提供全面的学术搜索服务；
- **Semantic Scholar** (`site:semanticscholar.org`) — 可查看论文的引用关系及相关论文；
- **arXiv** (`site:arxiv.org`) — 提供预印本资源（通常免费，无需通过 Sci-Hub）；
- **PubMed** (`site:pubmed.ncbi.nlm.nih.gov`) — 提供生物医学领域的文献资源。