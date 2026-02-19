---
name: pubmed-edirect
description: 使用 NCBI 的 EDirect 命令行工具从 PubMed 中搜索和检索文献。⚠️ 这是一项高级技能，需要手动安装相关工具。
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
    kind: manual
    label: Manual Installation Required - Review INSTALL.md
    docs: https://www.ncbi.nlm.nih.gov/books/NBK179288/
    note: "⚠️ User must manually download and review official installer script"
    security_level: elevated
metadata:
  openclaw:
    emoji: 🔬
    category: advanced
    security_level: elevated
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
        description: Email address to identify yourself to NCBI
---
# PubMed EDirect 技能

使用 NCBI 的 EDirect 命令行工具从 PubMed 中搜索和检索文献。

## ⚠️ 安全提示

**重要提示**：此技能需要安装外部命令行工具。安装过程包括：

1. **执行外部脚本**：从官方 NCBI FTP 服务器下载并执行安装脚本
2. **系统修改**：将相关目录添加到您的 PATH 环境变量中
3. **权限要求**：可能需要安装 Perl 模块及其依赖项

**在安装之前，您必须**：
1. 下载后查看安装脚本的内容
2. 确认来源的可靠性（官方域名 `ftp.ncbi.nlm.nih.gov`）
3. 在测试环境中进行验证
4. 了解所有将要执行的命令

## 概述

此技能通过官方的 EDirect（Entrez Direct）工具集提供对 PubMed 和其他 NCBI 数据库的访问。EDirect 是一组程序，允许您通过 Unix 终端访问 NCBI 的各种互连数据库（如出版物、序列、结构、基因、变异、表达等数据）。

**注意：这是一个本地安装技能**——所有工具都在您的系统上直接运行，无需使用 Docker 或容器化技术。请按照 [INSTALL.md](INSTALL.md) 文档进行本地设置。

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

1. **阅读安装指南**：请查看 [INSTALL.md](INSTALL.md) 以了解安全安装步骤
2. **手动安装 EDirect**：
   ```bash
   # Step 1: Download the script
   wget -q https://ftp.ncbi.nlm.nih.gov/entrez/entrezdirect/install-edirect.sh
   
   # Step 2: Review content (important for security)
   less install-edirect.sh
   
   # Step 3: Execute installation
   ./install-edirect.sh
   ```
3. **验证安装**：
   ```bash
   esearch -db pubmed -query "test" -retmax 1
   ```
4. **查看示例**：请查阅 [EXAMPLES.md](EXAMPLES.md)

## 核心工具

该技能通过 OpenClaw 的 `exec` 功能提供对 EDirect 工具的访问：

- `esearch` - 搜索数据库
- `efetch` - 检索记录
- `elink` - 查找相关记录
- `efilter` - 过滤结果
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

## 主要特性

- **命令行访问**：通过命令行访问 NCBI 数据库
- **管道架构**：使用 Unix 管道进行数据传输
- **结构化数据提取**：通过 XML 解析
- **批量处理**：支持批量处理任务
- **跨数据库链接**：支持在不同数据库之间进行数据关联

## 获取帮助

- 对任何 EDirect 命令使用 `-help` 命令查看帮助信息：`esearch -help`
- 查阅 [官方文档](https://www.ncbi.nlm.nih.gov/books/NBK179288/)
- 参考安装指南中的故障排除方法

## 包含的脚本

`scripts/` 目录中包含一些可用的 bash 脚本：

### `batch_fetch_abstracts.sh`

批量获取 PMID 列表的摘要，并提供错误处理和速率限制功能。

```bash
./scripts/batch_fetch_abstracts.sh pmids.txt abstracts/ 0.5
```

### `search_export_csv.sh`

搜索 PubMed 并将结果导出为包含元数据的 CSV 文件。

```bash
./scripts/search_export_csv.sh "CRISPR [TIAB]" 100 results.csv
```

### `publication_trends.sh`

分析随时间变化的出版物趋势，并提供可视化展示。

```bash
./scripts/publication_trends.sh "machine learning" 2010 2023 trends.csv
```

## 安全最佳实践

### 1. 脚本审核
```bash
# Always download first and review scripts
wget -q SOURCE_URL -O script.sh
less script.sh  # or cat script.sh | head -50
# Execute only after review
./script.sh
```

### 2. 环境隔离
- 在 Docker 容器中运行以增强安全性
- 使用虚拟机进行测试
- 设置专用用户账户

### 3. 最小权限原则
- 不要以 root 用户身份运行程序
- 设置适当的文件权限
- 为数据使用专用目录

### 4. 网络控制
- 配置防火墙规则
- 使用代理服务器进行受控访问
- 监控网络流量

## 注意事项

**重要提示**：此技能需要手动安装和配置。所有安装步骤都需要用户的明确确认和执行。

该技能通过本地安装 EDirect 工具，为您提供对 NCBI 数据库的命令行访问权限。