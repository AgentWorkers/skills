---
name: arxiv-osiris
version: 1.0.0
description: 从 arXiv.org 搜索并下载研究论文 - OpenClaw 代理的研究版本
metadata: {"openclaw": {"emoji": "📚", "requires": {"bins": ["python"], "pip": ["arxiv"]}, "homepage": "https://arxiv.org"}}
---
# ArXiv Skill

这是一个用于从 arXiv.org（世界上最大的免费科学预印本分发平台）搜索和下载科学论文的工具。

## 功能介绍

- **搜索**：可以通过关键词、标题或摘要来查找论文。
- **下载**：可以直接下载 PDF 格式的论文。
- **筛选**：可以根据学科类别（如物理学、计算机科学、数学等）进行筛选。
- **获取元数据**：包括作者信息、论文发表日期和所属类别等。

## 安装

```powershell
# Install Python dependency
pip install arxiv
```

## 使用方法

### 搜索论文

```powershell
# Basic search
.\arxiv.ps1 -Action search -Query "quantum computing"

# With max results
.\arxiv.ps1 -Action search -Query "machine learning" -MaxResults 10

# With category filter (physics, cs, math, q-bio, etc.)
.\arxiv.ps1 -Action search -Query "neural networks" -Categories "cs,stat"
```

### 下载论文

```powershell
# By arXiv ID
.\arxiv.ps1 -Action download -ArxivId "2310.12345"
```

### Python API

```python
from arxiv import search, download

# Search
results = search("simulation hypothesis", max_results=5)
for paper in results:
    print(f"{paper.title} - {paper.pdf_url}")

# Download
paper.download("/path/to/save")
```

## 学科分类

常见的 arXiv 学科分类：
- `cs.*` - 计算机科学
- `physics.*` - 物理学
- `math.*` - 数学
- `q-bio.*` - 定量生物学
- `q-fin.*` - 定量金融
- `stat.*` - 统计学

## 使用示例

- 搜索关于“意识”的论文：`arxiv.ps1 -search "consciousness" -max 5`
- 查找物理学论文：`arxiv.ps1 -search "quantum" -cats "physics" -max 10`
- 下载论文：`arxiv.ps1 -download "1706.03762"`（论文标题：Attention is All You Need）

## 注意事项

- arXiv 是免费且开放的资源。
- 提供的论文均为预印本，可能尚未经过同行评审。
- 是获取最新研究动态的理想工具。