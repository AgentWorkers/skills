---
name: tavily
description: 使用 Tavily 的网络搜索/发现功能来查找 URL/来源，进行初步的研究，收集最新的链接，或者从网页结果中生成一份带有引用的摘要。
metadata: {"openclaw":{"requires":{"env":["TAVILY_API_KEY"]},"primaryEnv":"TAVILY_API_KEY"}}
---
# Tavily

使用随附的命令行工具（CLI）可以从终端快速执行 Tavily 搜索并收集相关资源。

## 快速入门（CLI）

这些脚本 **需要** 在环境中设置 `TAVILY_API_KEY`（通常以 `Authorization: Bearer ...` 的形式提供）。

```bash
export TAVILY_API_KEY="..."
node skills/tavily/scripts/tavily_search.js --query "best rust http client" --max_results 5
```

- JSON 响应会被输出到 **标准输出（stdout）**。
- 默认情况下，简单的 URL 列表会被输出到 **标准错误输出（stderr）**。

## 常见用法

### 仅获取 URL

```bash
export TAVILY_API_KEY="..."
node skills/tavily/scripts/tavily_search.js --query "OpenTelemetry collector config" --urls-only
```

### 限制搜索范围（或排除特定域名）

```bash
export TAVILY_API_KEY="..."
node skills/tavily/scripts/tavily_search.js \
  --query "oauth device code flow" \
  --include_domains oauth.net,datatracker.ietf.org \
  --exclude_domains medium.com
```

## 注意事项

- 随附的 CLI 仅支持 Tavily 提供的部分请求字段（如 query、max_results、include_domains、exclude_domains）。
- 有关 API 字段的详细说明及更多示例，请参阅：`references/tavily-api.md`。
- 可选的使用脚本：`scripts/tavily_search.sh`。