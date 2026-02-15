---
name: pmc-harvest
description: 使用 NCBI API 从 PubMed Central 获取文章。可以搜索期刊，通过 OAI-PMH 获取全文，并批量下载数据以供 RAG（Rule-Based Access Group）流程使用。无需 API 密钥。
version: 1.0.0
author: Ania
metadata:
  clawdbot:
    emoji: "📚"
    requires:
      bins: ["node"]
---
# PMC Harvest

使用 NCBI 的官方 API 从 PubMed Central 获取全文文章。

## 主要功能

- **E-Utilities 搜索** — 按期刊、年份或查询条件查找文章
- **OAI-PMH 全文下载** — 下载文章的完整 XML 格式（仅限开放获取内容）
- **批量处理** — 同时处理多个期刊
- **摘要获取** — 适用于审稿流程的快速摘要检索功能
- **无需 API 密钥** — 使用 NCBI 的公共 API（但存在请求速率限制）

## 使用方法

```bash
# Search a journal
node {baseDir}/scripts/pmc-harvest.js --search "J Stroke[journal]" --year 2025

# Fetch full text for a specific article
node {baseDir}/scripts/pmc-harvest.js --fetch PMC12345678

# Batch harvest from multiple journals
node {baseDir}/scripts/pmc-harvest.js --harvest journals.json --year 2025

# Test with known journals
node {baseDir}/scripts/pmc-harvest.js --test
```

## 命令选项

| 标志 | 说明 |
|------|-------------|
| `--search <查询>` | PMC 搜索查询（使用 `journal[name]` 格式） |
| `--year <年份>` | 按出版年份筛选 |
| `--max <n>` | 最大返回结果数量（默认：100 条） |
| `--fetch <pmcid>` | 为指定的 PMCID 下载全文 |
| `--harvest <文件>` | 从 JSON 格式的期刊列表中批量下载文章 |
| `--test` | 使用示例期刊进行测试 |

## 程序化 API

```javascript
const pmc = require('{baseDir}/lib/api.js');

// Search
const { count, pmcids } = await pmc.searchJournal('"J Stroke"[journal]', { year: 2025 });

// Get summaries
const summaries = await pmc.getSummaries(pmcids);

// Fetch full text
const { available, xml, reason } = await pmc.fetchFullText('PMC12345678');

// Parse JATS XML
const { title, abstract, body } = pmc.parseJATS(xml);

// Fetch abstract only (lightweight)
const { title, abstract } = await pmc.fetchAbstract('PMC12345678');
```

## 期刊查询示例

```javascript
const queries = {
  'Stroke': '"Stroke"[journal]',
  'Journal of Stroke': '"J Stroke"[journal]',
  'Stroke & Vascular Neurology': '"Stroke Vasc Neurol"[journal]',
  'European Stroke Journal': '"Eur Stroke J"[journal]',
  'BMC Neurology': '"BMC Neurol"[journal]'
};
```

## 注意事项

- **OAI-PMH 仅返回开放获取的文章** — 非开放获取的内容无法下载 |
- **请求速率限制** — 无 API 密钥时每秒最多只能发送 3 条请求 |
- **高峰时段** — NCBI 建议避免在东部时间上午 5 点至晚上 9 点期间进行大量数据下载

## API 参考文档

该工具使用了 NCBI 的官方 API：

- **E-Utilities**：`https://eutils.ncbi.nlm.nih.gov/entrez/eutils`
  - `esearch.fcgi` — 搜索 PMC 文章
  - `esummary.fcgi` — 获取文章元数据
- **OAI-PMH**：`https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh`
  - `GetRecord` — 下载文章的完整 XML 格式

更多文档请参考：https://www.ncbi.nlm.nih.gov/books/NBK25501/