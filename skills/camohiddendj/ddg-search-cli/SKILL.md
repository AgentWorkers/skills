---
name: ddg-search
description: DuckDuckGo HTML搜索爬虫命令行工具（CLI），支持JSON、CSV、OpenSearch、Markdown以及压缩格式的输出结果。
homepage: https://github.com/camohiddendj/ddg-search
metadata:
  {
    "openclaw":
      {
        "emoji": "🦆",
        "requires": { "bins": ["ddg-search"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "ddg-search",
              "bins": ["ddg-search"],
              "label": "Install ddg-search CLI (npm)",
            },
          ],
      },
  }
---
# ddg-search  
从命令行搜索 DuckDuckGo。搜索结果输出到标准输出（stdout），进度信息输出到标准错误（stderr）。  

## 快速参考  
```bash
ddg-search "query"                          # default: JSON, 5 pages
ddg-search -f compact "query"               # minimal-token output (best for LLM context)
ddg-search -f jsonl "query"                 # one JSON object per line
ddg-search -n 10 "query"                    # stop after 10 results
ddg-search -p 2 -f json "query"             # 2 pages, JSON
ddg-search -r us-en -t w "recent topic"     # US-English, past week
ddg-search -p 0 "query"                     # unlimited pages (scrape all)
```  

## 选项  
| 标志 | 长格式 | 描述 | 默认值 |  
|------|------|-------------|---------|  
| `-f` | `--format` | 输出格式：`json`、`jsonl`、`csv`、`opensearch`、`markdown`、`compact` | `json` |  
| `-p` | `--pages` | 最大抓取页数（0 = 无限制） | `5` |  
| `-n` | `--max-results` | 抓取到指定数量的结果后停止 | `all` |  
| `-r` | `--region` | 地区代码（例如 `us-en`、`uk-en`） | 所有地区 |  
| `-t` | `--time` | 时间筛选：`d`（天）、`w`（周）、`m`（月）、`y`（年） | 无 |  

## 选择输出格式  
- **`compact`**：适用于输入到大型语言模型（LLM）中。输出格式简洁，无 JSON 开销。  
- **`jsonl`**：适用于通过管道传输给基于行的工具或流处理程序。  
- **`json`**：提供结构化数据以及 OpenSearch 元数据，支持即时查询结果和拼写校正。可以使用 `jq` 进行字段提取（例如 `| jq '.items[].link'`）。  
- **`csv`**：适用于电子表格或表格分析。  
- **`markdown`**：适用于人类可读的输出或嵌入到文档中。  
- **`opensearch`**：适用于生成 Atom XML 数据源。  

## 从 JSON 输出中提取 URL  
```bash
ddg-search "query" | jq -r '.items[].link'
```  

## 注意事项  
- 使用 DuckDuckGo 可能会触发机器人检测机制，导致工具提前停止并返回已收集的所有结果。  
- 系统会自动在页面请求之间插入随机延迟（800–2900 毫秒）。  
- 进度信息会显示在标准错误中，因此将标准输出（stdout）重定向只能获取到搜索结果。