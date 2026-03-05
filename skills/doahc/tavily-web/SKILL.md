---
name: tavily
description: 使用 Tavily 的 Search/Extract/Research API 进行网页搜索和内容提取（支持 bearer 认证）。适用于需要获取网页结果（如通用信息、新闻、财经内容）的情况，同时支持按日期、主题或领域进行筛选，以及获取内容来源的引用信息。若希望使用 Tavily 代替内置的 web_search 或 Firecrawl 功能，请使用此方法。使用此功能需要 TAVILY_API_KEY。
version: 1.0.0
compatibility: Requires env var TAVILY_API_KEY
requires_env: [TAVILY_API_KEY]
primary_credential: TAVILY_API_KEY
outbound_hosts: ["api.tavily.com"]
metadata:
  hermes:
    tags: [Web, Search, Tavily, Research, API, Citations]
    requires_env: [TAVILY_API_KEY]
    outbound_hosts: ["api.tavily.com"]
  openclaw:
    requires:
      env: ["TAVILY_API_KEY"]
---
# Tavily（网络搜索/提取/研究）

## 先决条件

- 确保在Hermes环境中设置了`TAVILY_API_KEY`（通常位于`~/.hermes/.env`文件中）。
- 请勿将API密钥硬编码到聊天日志中。详情请参阅`references/bp-api-key-management.md`。

## 安全注意事项

- 随附的CLI工具（`scripts/tavily.py`）仅从环境变量中读取`TAVILY_API_KEY`，并且只会向`https://api.tavily.com`发送请求。
- 在进行搜索时，建议使用`search`功能而非`include_raw_content`功能，以减小输出数据量并避免意外泄露敏感信息。

## 快速参考

使用终端工具运行随附的CLI脚本（输出为JSON格式）。
`SKILL_DIR`是包含此`SKILL.md`文件的目录。

```bash
# Search (general)
python3 SKILL_DIR/scripts/tavily.py search --query "latest OpenAI API changes" --max-results 5

# Search (news) with recency filter
python3 SKILL_DIR/scripts/tavily.py search --query "latest OpenAI API changes" --topic news --time-range week --max-results 5

# High-precision search (more cost/latency)
python3 SKILL_DIR/scripts/tavily.py search --query "OpenAI API rate limits March 2026" --search-depth advanced --chunks-per-source 3 --max-results 5

# Search + answer (still cite URLs from results)
python3 SKILL_DIR/scripts/tavily.py search --query "What is X?" --include-answer basic --max-results 5

# Extract (targeted chunks; prefer this over include_raw_content on search)
python3 SKILL_DIR/scripts/tavily.py extract --url "https://example.com" --query "pricing" --chunks-per-source 3 --format markdown

# Research (creates task + polls until complete)
python3 SKILL_DIR/scripts/tavily.py research --input "Summarize the EU AI Act enforcement timeline. Provide numbered citations." --model auto --citation-format numbered --max-wait-seconds 180
```

在最终答案中，可以使用返回的`results[].url`字段作为引用/来源。

## 无脚本选项（使用curl）

可以直接通过curl调用Tavily服务（使用相同的API端点，无需额外的脚本）：

```bash
curl -s "https://api.tavily.com/search" \
  -H "Authorization: Bearer <TAVILY_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"query":"latest OpenAI API changes","topic":"news","time_range":"week","max_results":5}'

curl -s "https://api.tavily.com/extract" \
  -H "Authorization: Bearer <TAVILY_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"urls":"https://example.com","query":"pricing","chunks_per_source":3,"extract_depth":"basic","format":"markdown"}'
```

## 使用步骤

1. 将用户请求转换为一个简洁的搜索查询（长度建议控制在400个字符以内）。对于包含多个部分的问题，将其拆分为2-4个子查询。
2. 选择搜索主题：
   - `general`：适用于大多数搜索场景
   - `news`：用于查询当前事件（建议同时设置`time_range`或日期范围）
   - `finance`：用于查询市场/金融相关内容
3. 选择搜索深度：
   - 默认使用`basic`模式（1个信用点数）；如需更高精度，可使用`advanced`模式（2个信用点数），并通过`chunks_per_source`参数控制返回内容的数量。
4. 将`max_results`设置为较小的值（默认为5），并根据结果得分和域名可信度进行筛选。
5. 对于主要文本内容，可以对排名前1-3个URL使用`extract`功能进行提取：
   - 使用`extract --query ... --chunks-per-source N`命令，以避免将整个页面内容直接包含在结果中。
6. 如果需要跨多个子主题进行综合分析并引用相关内容，可以使用`research`功能，并持续执行该操作直到状态变为`completed`。

## 注意事项

- 使用`include_raw_content`功能可能会导致输出数据量急剧增加；建议采用“搜索”（search）→“提取”（extract）的步骤顺序。
- `auto_parameters`功能可能会自动选择`search_depth=advanced`（2个信用点数）；如果需要控制搜索成本，请明确指定`--search-depth`参数。
- `exact_match`模式的搜索效果较为严格；请在`--query`参数中用引号括住搜索词，以获得更少的搜索结果。
- `country`参数仅适用于`topic=general`的搜索。
- 在遇到错误时，请保留响应中的`request_id`以便后续支持或调试。

## 验证方法

- 检查信用点数和使用限制：运行`python3 SKILL_DIR/scripts/tavily.py usage`命令。
- 如果需要查看每次请求的具体使用情况，可以在`search`或`extract`命令后添加`--include-usage`参数。

## 参考资料

- `references/search.md`
- `references/extract.md`
- `references/research.md`
- `references/research-get.md`
- `references/bp-search.md`
- `references/bp-extract.md`
- `references/bp-research.md`
- `references/bp-api-key-management.md`
- `references/usage.md`