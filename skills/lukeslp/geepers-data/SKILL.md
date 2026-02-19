---
name: geepers-data
description: 通过一个单一的端点，可以从17个权威API（包括arXiv、美国人口普查局、GitHub、NASA、Wikipedia、PubMed、新闻、天气、金融等）获取结构化数据。当您需要来自这些权威来源的真实数据用于研究、可视化或分析时，可以使用此服务。
---
# Dreamer Data

您可以通过 `https://api.dr.eamer.dev` 访问 17 个结构化数据源。

## 认证

```bash
export DREAMER_API_KEY=your_key_here
```

## 端点

### 列出可用数据源
```
GET https://api.dr.eamer.dev/v1/data
```

### 在多个数据源中搜索
```
POST https://api.dr.eamer.dev/v1/data/search
Body:
{
  "source": "arxiv",
  "query": "machine learning interpretability",
  "limit": 10
}
```

### 可用数据源
| 数据源 | ID | 提供的数据类型 |
|--------|-----|-----------------|
| arXiv | `arxiv` | 学术论文 |
| 美国人口普查局 | `census` | 美国人口统计数据 |
| GitHub | `github` | 代码仓库、问题、用户信息 |
| NASA | `nasa` | 太空数据、图像、天文学信息 |
| 维基百科 | `wikipedia` | 百科全书条目 |
| PubMed | `pubmed` | 生物医学文献 |
| 新闻 | `news` | 来自 80 多家新闻机构的实时事件 |
| 天气 | `weather` | 当前及未来天气预报 |
| 金融 | `finance` | 股票价格和市场数据 |
| FEC | `fec` | 美国联邦竞选财务数据 |
| OpenLibrary | `openlibrary` | 书籍和图书馆记录 |
| Semantic Scholar | `semantic_scholar` | 学术引用图谱 |
| YouTube | `youtube` | 视频元数据 |
| Wolfram Alpha | `wolfram` | 计算机知识 |
| Wayback Machine | `archive` | 网页存档快照 |
| 司法部 | `judiciary` | 美国法院记录 |
| MAL | `mal` | 动画和漫画数据 |

## 适用场景
- 需要经过验证、可引用的研究数据 |
- 从权威数据源构建数据管道 |
- 用外部信息丰富现有数据集

## 不适用场景
- 所需数据源未在列表中（请先查看 `/v1/data`） |
- 您已直接通过 API 访问该数据源，且该 API 有较高的使用频率限制