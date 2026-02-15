---
name: pubmed-edirect
description: 使用 NCBI 的 EDirect 命令行工具从 PubMed 中搜索并检索文献。
requires:
  bins:
    - esearch
    - efetch
    - elink
    - xtract
    - einfo
    - efilter
install:
  - id: edirect
    kind: script
    label: Install NCBI EDirect from official source
    source: https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh
    docs: https://www.ncbi.nlm.nih.gov/books/NBK179288/
metadata:
  openclaw:
    emoji: 🔬
    requires:
      bins:
        - esearch
        - efetch
        - elink
        - xtract
        - einfo
        - efilter
    env:
      - name: NCBI_API_KEY
        optional: true
        description: NCBI API key for increased rate limits (10 requests/sec vs 3 requests/sec)
      - name: NCBI_EMAIL
        optional: true
        description: Email address to identify yourself to NCBI (recommended)
---

# PubMed EDirect 技能

使用 NCBI 的 EDirect 命令行工具从 PubMed 中搜索和检索文献。

## 概述

该技能通过官方的 EDirect（Entrez Direct）工具提供对 PubMed 以及其他 NCBI 数据库的访问。EDirect 是一套程序，允许从 Unix 终端访问 NCBI 的各种互连数据库（包括出版物、序列、结构、基因、变异、表达等信息）。

**注意：这是一个本地安装技能**——所有工具都在您的系统上直接运行，无需 Docker 或容器化。请按照 [INSTALL.md](INSTALL.md) 文档进行本地设置。

## 结构

该技能包含以下文件：

- **`INSTALL.md`** - 安装和配置指南
- **`BASICS.md`** - 基本用法和常用命令
- **`ADVANCED.md`** - 高级技术和复杂查询
- **`EXAMPLES.md`** - 实用示例
- **`REFERENCE.md`** - 快速参考（字段限定符、格式等）
- **`OPENCLAW_INTEGRATION.md`** - 专门针对 OpenClaw 的使用指南
- **`scripts/`** - 用于常见任务的有用 bash 脚本

## 快速入门

1. **安装 EDirect**（请参阅 [INSTALL.md](INSTALL.md)）
2. **尝试基本搜索**：
   ```bash
   esearch -db pubmed -query "CRISPR [TIAB]" | efetch -format abstract
   ```
3. **查看 [EXAMPLES.md](EXAMPLES.md) 中的示例**

## 核心工具

该技能通过 OpenClaw 的 `exec` 功能提供对 EDirect 工具的访问：

- `esearch` - 搜索数据库
- `efetch` - 检索记录
- `elink` - 查找相关记录
- `efilter` - 筛选结果
- `xtract` - 从 XML 中提取数据
- `einfo` - 获取数据库信息

## 支持的数据库

EDirect 支持众多 NCBI 数据库，包括：

- `pubmed` - 生物医学文献
- `pmc` - PubMed Central 的全文文章
- `gene` - 基因信息
- `nuccore` - 核苷酸序列
- `protein` - 蛋白质序列
- `mesh` - 医学主题词
- 以及更多……

## 主要特点

- **命令行访问** NCBI 数据库
- **使用 Unix 管道（pipe）的流程化架构**
- **通过 XML 解析进行结构化数据提取**
- **批处理功能**
- **记录之间的跨数据库链接**

## 获取帮助

- 对任何 EDirect 命令使用 `-help`：`esearch -help`
- 查阅 [官方文档](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
- 查看安装指南中的故障排除方法

## 包含的脚本

`scripts/` 目录中包含一些可用的 bash 脚本：

### `batch_fetch_abstracts.sh`

批量获取 PMID 列表的摘要，并具有错误处理和速率限制功能。

```bash
./scripts/batch_fetch_abstracts.sh pmids.txt abstracts/ 0.5
```

### `search_export_csv.sh`

搜索 PubMed 并将结果连同元数据导出为 CSV 文件。

```bash
./scripts/search_export_csv.sh "CRISPR [TIAB]" 100 results.csv
```

### `publication_trends.sh`

分析随时间变化的出版物趋势，并提供可视化展示。

```bash
./scripts/publication_trends.sh "machine learning" 2010 2023 trends.csv
```

## 注意事项

使用该技能之前，需要在您的系统上安装并配置 EDirect。它提供了可以通过 OpenClaw 的 `exec` 工具执行的命令模板和示例。

对于复杂的工作流程，可以考虑创建可重用的 shell 脚本或使用这些内置脚本。