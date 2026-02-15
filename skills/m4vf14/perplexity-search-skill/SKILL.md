---
name: perplexity-search
description: 使用 Perplexity 的 Search API 在网络上进行搜索，可获取排名靠前的实时网页结果，并支持高级过滤功能。当您需要查找最新信息、进行市场研究或关注热门话题时，或者当 Brave Search 无法使用时，这个 API 非常实用。该 API 支持按时间范围（天/周/月/年）进行过滤，并返回包含标题、网址和内容摘要的结构化搜索结果。
metadata:
  openclaw:
    emoji: 🔍
    requires:
      env:
        - PERPLEXITY_API_KEY
    primaryEnv: PERPLEXITY_API_KEY
---

# Perplexity 搜索

使用 Perplexity 的搜索 API 在网络上进行搜索，可获取排名靠前的实时搜索结果。

## 快速入门

**基本搜索：**
```bash
python3 {baseDir}/scripts/search.py "your search query"
```

**带选项的搜索：**
```bash
# Get 10 results
python3 {baseDir}/scripts/search.py "AI trends 2024" --count 10

# Filter by recency
python3 {baseDir}/scripts/search.py "recent AI news" --recency week

# Get raw JSON output
python3 {baseDir}/scripts/search.py "market research" --json
```

## API 密钥设置

该脚本需要一个名为 `PERPLEXITY_API_KEY` 的环境变量。

**选项 1：在 OpenClaw 配置文件中设置**（推荐）

将以下内容添加到 `~/.openclaw/openclaw.json` 文件中：
```json
{
  "skills": {
    "perplexity-search": {
      "env": {
        "PERPLEXITY_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**选项 2：通过环境变量设置**

```bash
export PERPLEXITY_API_KEY="your-api-key-here"
```

请从以下链接获取您的 API 密钥：https://perplexity.ai/account/api

## 参数

- `query` - 搜索查询字符串（必填）
- `--count N` - 结果数量（1-10，默认值：5）
- `--recency FILTER` - 新近度筛选：`day`（天）、`week`（周）、`month`（月）或 `year`（年）
- `--json` - 以原始 JSON 格式输出结果，而不是格式化后的结果

## 响应格式

API 返回的结果格式如下：
```json
{
  "results": [
    {
      "title": "Article title",
      "url": "https://example.com/article",
      "snippet": "Brief excerpt from the page...",
      "date": "2024-01-15",
      "last_updated": "2024-02-01"
    }
  ],
  "id": "search-request-id"
}
```

## 使用场景

**市场研究：**
```bash
python3 {baseDir}/scripts/search.py "golf coaching Instagram trends" --count 10
```

**最新新闻：**
```bash
python3 {baseDir}/scripts/search.py "AI regulation updates" --recency week
```

**竞争分析：**
```bash
python3 {baseDir}/scripts/search.py "AI golf training apps" --count 10
```

## 价格

Perplexity 搜索 API 的费用为：**每 1,000 次请求 5 美元**

您可以在以下链接查看自己的使用情况：https://perplexity.ai/account/api

## 安全性

- API 密钥仅从环境变量中加载，从不硬编码
- 输出内容经过安全处理，可防止终端注入攻击
- 错误信息不会暴露敏感信息
- 设有 30 秒的超时机制，可防止请求挂起
- 所有参数都经过输入验证

## 注意事项

- 结果按相关性排序
- 包含实时网络数据
- 支持按时间顺序筛选结果
- 可以返回结构化的 JSON 数据或格式化的文本
- 使用量会受到您所选 Perplexity 计划的限制