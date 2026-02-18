---
name: tavily-search
description: "使用 Tavily API 进行 AI 优化的搜索和内容提取。功能包括深度搜索、新闻过滤以及为大型语言模型（LLM）处理而提取的原始内容。"
homepage: https://tavily.com
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["TAVILY_API_KEY"]}}}
---
# Tavily 搜索

Tavily 是一款专为 AI 代理（大型语言模型，LLMs）设计的搜索引擎。该工具能够提供优化的搜索结果和内容提取功能。

## 先决条件

1. 已安装 Node.js。
2. **Tavily API 密钥**：请在 [tavily.com](https://tavily.com) 获取 API 密钥。
3. **环境变量**：在您的环境中设置 `TAVILY_API_KEY`。

## 使用方法

### 搜索

执行针对 AI 的优化搜索。

```bash
node scripts/search.mjs "What are the latest developments in agentic AI?"
```

**选项：**
- `-n <数字>`：显示的结果数量（默认值：5，最大值：20）。
- `--deep`：使用更深入的搜索方式（处理更多文本片段，从而获得更准确的结果）。
- `--topic <general|news>`：按主题筛选搜索结果（默认值：general）。
- `--days <数字>`：对于新闻主题，将结果限制在过去的 N 天内。

## 从 URL 中提取内容

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

**注意事项：**
- 需要使用从 [https://tavily.com] 获取的 `TAVILY_API_KEY`。
- Tavily 针对 AI 设计，能够返回简洁、相关的文本片段。
- 对于复杂的研究问题，可以使用 `--deep` 选项。
- 对于当前事件，可以使用 `--topic news` 选项进行搜索。

## 故障排除

- **API 密钥缺失**：确保 `TAVILY_API_KEY` 已正确设置或导出到环境中。
- **网络问题**：检查您的网络连接以及 Tavily 的 API 使用配额。