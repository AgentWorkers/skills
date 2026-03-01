# Google Scholar 搜索

> **基于 AI 的学术文献搜索工具** - 通过 Google Scholar 搜索学术论文

## 描述

通过 Google Scholar 搜索学术文献和研究报告。该工具提供了强大的搜索功能，包括针对特定作者的搜索以及按年份筛选的结果。

## 特点

- **关键词搜索**：通过关键词、标题或主题搜索论文
- **高级搜索**：根据作者和发表年份范围筛选结果
- **作者信息**：获取作者的详细信息，包括研究兴趣和引用次数
- **丰富的元数据**：可以查看论文的标题、作者、摘要和直接链接
- **JSON 导出**：将搜索结果导出为 JSON 格式以便进一步处理

## 使用方法

```
/google-scholar-search Search for papers about "machine learning in healthcare"
/google-scholar-search Find papers by author "Andrew Ng" about "deep learning"
/google-scholar-search Search for "neural networks" from 2018 to 2022
/google-scholar-search Get author information for "Geoffrey Hinton"
```

## 示例

### 基本搜索

```
/google-scholar-search Find papers about "transformer architecture"
```

### 带作者的高级搜索

```
/google-scholar-search Search for "deep learning" by author "Yann LeCun"
```

### 按年份范围搜索

```
/google-scholar-search Find papers about "GANs" from 2018 to 2023
```

### 查看作者信息

```
/google-scholar-search Get author profile for "Yoshua Bengio"
```

## 命令参考

### search

**用法：** 通过关键词搜索论文

| 选项 | 描述 |
|--------|-------------|
| `--query` | 搜索查询字符串 |
| `--results` | 结果数量（默认：10） |
| `--output` | 输出文件路径 |
| `--format` | 输出格式：控制台、json |

### advanced

**用法：** 使用过滤器进行高级搜索

| 选项 | 描述 |
|--------|-------------|
| `--query` | 搜索查询字符串 |
| `--author` | 按作者名称筛选 |
| `--year-start` | 开始年份（可选） |
| `--year-end` | 结束年份（可选） |
| `--results` | 结果数量（默认：10） |
| `--output` | 输出文件路径 |
| `--format` | 输出格式：控制台、json |

### author

**用法：** 获取作者的个人信息和发表的论文

| 选项 | 描述 |
|--------|-------------|
| `--name` | 作者名称 |
| `--output` | 输出文件路径 |
| `--format` | 输出格式：控制台、json |

## 输出格式

### 控制台输出

```
标题: Attention Is All You Need
作者: Vaswani, A., et al.
摘要: This paper proposes the Transformer architecture...
链接: https://...
```

### 作者信息输出

```
姓名: Geoffrey Hinton
机构: University of Toronto
研究领域: Machine Learning, Deep Learning, Neural Networks
总引用数: 150000+
近期论文:
  - 1. Forward-Forward (2022) - 引用数: 150
  - 2. Deep Learning (2015) - 引用数: 50000+
```

## 注意事项

- Google Scholar 没有提供官方 API — 该工具使用网络爬虫技术获取数据
- 由于 Google 的反爬虫措施，搜索结果可能会有所变化
- 为确保稳定的访问效果，建议使用 Semantic Scholar 或 PubMed 的 API
- 按作者搜索时，返回的是第一个匹配的作者信息

## 相关技能

- [semanticscholar-search-skill](../semanticscholar-search-skill/) - 在 Semantic Scholar 数据库中搜索
- [pubmed-search-skill](../pubmed-search-skill/) - 搜索生物医学文献
- [sci-hub-search-skill](../sci-hub-search-skill/) - 从 Sci-Hub 下载论文