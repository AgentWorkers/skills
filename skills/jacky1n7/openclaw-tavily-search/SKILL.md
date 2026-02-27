---
name: tavily-search
description: "通过 Tavily API 进行网页搜索（作为 Brave 的替代方案）。当用户需要搜索网页、查找资料或链接，但 Brave 的网页搜索功能不可用或不符合用户需求时，可以使用此方法。该 API 会返回少量相关结果（包括标题、网址和内容摘要），并可选择性地提供简短的答案总结。"
---
# Tavily 搜索

使用随软件提供的脚本，通过 Tavily 在网页上进行搜索。

## 要求

- 通过以下方式提供 API 密钥：
  - 环境变量：`TAVILY_API_KEY`，
  - 或者在 `~/.openclaw/.env` 文件中设置：`TAVILY_API_KEY=...`

## 命令

在 OpenClaw 工作区中运行以下命令：

```bash
# raw JSON (default)
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5

# include short answer (if available)
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5 --include-answer

# stable schema (closer to web_search): {query, results:[{title,url,snippet}], answer?}
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5 --format brave

# human-readable Markdown list
python3 {baseDir}/scripts/tavily_search.py --query "..." --max-results 5 --format md
```

## 输出格式

### 原始格式（默认）
- JSON 格式：`{"query": ..., "answer": ..., "results": [{"title": ..., "url": ..., "content": ...}]`

### brave 格式
- JSON 格式：`{"query": ..., "answer": ..., "results": [{"title": ..., "url": ..., "snippet": ...}]`

### md 格式
- 一种简洁的 Markdown 列表格式，包含标题、网址和摘要。

## 注意事项

- 默认情况下，`max-results` 的值较小（3–5），以减少对系统资源的消耗（如令牌使用量和读取负担）。
- 建议优先返回网址和摘要；仅在需要时才获取完整页面内容。