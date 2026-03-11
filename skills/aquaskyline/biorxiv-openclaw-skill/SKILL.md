---
name: biorxiv
version: 1.1.0
description: Access bioRxiv preprint repository for biology preprints. Use for: (1) Fetching recent preprints from specific categories like bioinformatics, genomics, molecular-biology, etc., (2) Getting papers by date range, (3) Listing available subject collections, (4) Retrieving paper metadata including titles, authors, DOIs, dates, and categories. No authentication required.
---

# bioRxiv 技能

该技能允许通过官方的 bioRxiv API 访问 bioRxiv 预印本存储库。

## 使用场景

- 用户需要查看最近的生物学预印本
- 用户希望获取特定 bioRxiv 分类（如生物信息学、基因组学等）的论文
- 用户需要论文的元数据（标题、作者、DOI、日期、分类）
- 用户需要指定日期范围内的预印本

## 快速入门

### 列出可用的分类
```bash
python scripts/biorxiv.py --list
```

### 获取最新论文
```bash
# Default: bioinformatics papers
python scripts/biorxiv.py --collection bioinformatics

# Other collections
python scripts/biorxiv.py --collection genomics
python scripts/biorxiv.py --collection neuroscience
python scripts/biorxiv.py --collection microbiology

# Specific date range
python scripts/biorxiv.py --collection bioinformatics --start 2026-03-01 --end 2026-03-09

# Limit results
python scripts/biorxiv.py --collection bioinformatics --limit 10
```

### 以 JSON 格式输出结果
```bash
python scripts/biorxiv.py --collection bioinformatics --json
```

## 可用的分类
- 生物信息学
- 基因组学
- 分子生物学
- 细胞生物学
- 遗传学
- 进化生物学
- 生态学
- 神经科学
- 植物生物学
- 微生物学
- 免疫学
- 癌症生物学
- 生物化学
- 生物物理学
- 结构生物学
- 系统生物学
- 合成生物学
- 发育生物学
- 计算生物学

## API 说明

### 官方 bioRxiv API
- **基础 URL：** `https://api.biorxiv.org/details/biorxiv/{start_date}/{end_date}/{cursor}`
- **无需身份验证**
- 每次调用最多返回 100 篇论文
- 支持通过查询参数进行分类过滤

### API 端点
- `/details/biorxiv/[start]/[end]/[cursor]` — 论文元数据
- `/pub/[start]/[end]/[cursor]` — 仅返回已发表的文章

## 使用方式

### 概述最新论文
1. 从所需分类中获取论文
2. 解析论文的标题和摘要
3. 如果有多个论文，按主题进行分组
4. 提供简洁的摘要

### 按主题查找论文
1. 在多个相关分类中搜索
2. 通过标题中的关键词进行过滤
3. 返回最相关的结果