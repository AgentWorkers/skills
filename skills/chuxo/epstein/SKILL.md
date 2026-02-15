---
name: epstein
description: >
  Search 44,886+ DOJ-released Jeffrey Epstein documents (Jan 2026 release).
  Free, no payment required. Search by name, topic, location, or keyword across
  the full DugganUSA index of declassified Epstein files. Returns document previews,
  people mentioned, locations, aircraft, evidence types, and source references.
metadata:
  author: project-einstein
  version: "1.1.0"
  clawdbot:
    emoji: "📂"
    homepage: "https://emc2ai.io"
    requires:
      bins: ["node", "curl"]
---

# 埃普斯坦文件搜索——免费的司法部文档搜索工具  

您可以搜索美国司法部于2026年1月30日公开的44,886多份解密的杰弗里·埃普斯坦相关文件。该工具由[DugganUSA](https://analytics.dugganusa.com)提供的公共索引支持。  

**完全免费。无需API密钥、无需注册账户，也无需支付任何费用。**  

## 快速入门  

```bash
# Search by name
node scripts/epstein.mjs search --query "Ghislaine Maxwell" --limit 10

# Search by topic
node scripts/epstein.mjs search --query "flight logs" --limit 20

# Search by location
node scripts/epstein.mjs search --query "Little St James"

# Get index statistics
node scripts/epstein.mjs stats
```  

## 命令  

### `search` — 搜索埃普斯坦相关文件  
您可以通过关键词、文件名称、主题或文件位置来搜索所有已索引的文件。  

```bash
node scripts/epstein.mjs search --query "SEARCH TERMS" [--limit N]
```  

| 标志 | 描述 | 默认值 |
|------|-------------|---------|
| `--query <术语>` | 搜索查询（必填） | — |
| `--limit <数量>` | 显示的结果数量（1-500条） | `10` |

**示例：**  

```bash
# Search for a specific person
node scripts/epstein.mjs search --query "Prince Andrew"

# Search for a topic
node scripts/epstein.mjs search --query "financial transactions"

# Search for locations
node scripts/epstein.mjs search --query "New York mansion"

# Get more results
node scripts/epstein.mjs search --query "flight logs" --limit 50

# Search for evidence types
node scripts/epstein.mjs search --query "phone records"
```  

### `stats` — 索引统计信息  
您可以获取文档索引的当前状态，包括总文件数量、数据库大小以及最后一次更新时间。  

```bash
node scripts/epstein.mjs stats
```  

## 输出格式  
搜索结果以JSON格式输出到标准输出（stdout），便于进一步处理；状态信息和PDF文件的直接链接会输出到标准错误输出（stderr），方便查看。  

### 搜索结果的结构  
每个搜索结果包含以下信息：  
- `doj_url`（PDF文件的直接链接）  
- `doj_listing_url`（相关数据集的页面链接）  

**v1.1.0的新功能：** 每个搜索结果现在都包含这些信息。此外，命令行界面（CLI）也会在标准错误输出中显示PDF文件的直接链接。  

```
--- Quick Links ---
1. EFTA-00001234: https://www.justice.gov/epstein/files/DataSet%209/EFTA-00001234.pdf
2. EFTA-00001235: https://www.justice.gov/epstein/files/DataSet%209/EFTA-00001235.pdf
```  

## 数据来源  
所有文件均来自美国司法部于2026年1月30日公开的杰弗里·埃普斯坦相关记录。这些文件通过[DugganUSA](https://analytics.dugganusa.com)提供的公共API进行索引和搜索。  

- **数据来源**：[美国司法部埃普斯坦相关记录](https://www.justice.gov/epstein)  
- **索引服务**：[DugganUSA Analytics](https://analytics.dugganusa.com)  
- **文件数量**：44,886多份（总计超过300万页）  
- **内容类型**：法庭文件、证词记录、飞行日志、财务记录、通信记录、证据清单等  

## 数据处理与集成  
搜索结果以JSON格式输出到标准输出（stdout），方便将其导入其他工具中进行进一步处理。  

```bash
# Pipe to jq for filtering
node scripts/epstein.mjs search --query "Maxwell" --limit 100 | jq '.hits[] | .people'

# Save results to file
node scripts/epstein.mjs search --query "flight logs" --limit 500 > flight-logs.json

# Count total hits
node scripts/epstein.mjs search --query "Palm Beach" | jq '.totalHits'

# Extract all mentioned people
node scripts/epstein.mjs search --query "2005" --limit 100 | jq '[.hits[].people[]?] | unique'
```  

## 常见问题解答  

**“无法访问API”**  
请检查您的网络连接。DugganUSA的API可能会暂时处于关闭状态。  

**“未找到结果”**  
尝试使用更宽泛的搜索关键词。该工具基于关键词进行搜索，请使用文件名称、位置或文件类型，而非完整的句子。  

**响应速度较慢**  
API的响应时间通常在100-900毫秒之间；如果查询结果数量较多（`--limit`参数大于100），响应时间可能会稍长。  

## 参考资料  
- [美国司法部埃普斯坦相关记录](https://www.justice.gov/epstein) — 官方发布页面  
- [DugganUSA API](https://analytics.dugganusa.com) — 索引服务提供商  
- [Project Einstein](https://emc2ai.io) — 内置埃普斯坦文件搜索功能的人工智能工具