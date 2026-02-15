---
name: searxng
description: 这是一个尊重用户隐私的元搜索引擎，它使用您本地的 SearXNG 实例来执行搜索功能。您可以在此搜索网页、图片、新闻等内容，而无需依赖任何外部 API。
author: Avinash Venkatswamy
version: 1.0.1
homepage: https://searxng.org
triggers:
  - "search for"
  - "search web"
  - "find information"
  - "look up"
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"]},"config":{"env":{"SEARXNG_URL":{"description":"SearXNG instance URL","default":"http://localhost:8080","required":true}}}}}
---

# SearXNG 搜索

使用您本地的 SearXNG 实例进行网页搜索——这是一个注重隐私的元搜索引擎。

## 命令

### 网页搜索
```bash
uv run {baseDir}/scripts/searxng.py search "query"              # Top 10 results
uv run {baseDir}/scripts/searxng.py search "query" -n 20        # Top 20 results
uv run {baseDir}/scripts/searxng.py search "query" --format json # JSON output
```

### 分类搜索
```bash
uv run {baseDir}/scripts/searxng.py search "query" --category images
uv run {baseDir}/scripts/searxng.py search "query" --category news
uv run {baseDir}/scripts/searxng.py search "query" --category videos
```

### 高级选项
```bash
uv run {baseDir}/scripts/searxng.py search "query" --language en
uv run {baseDir}/scripts/searxng.py search "query" --time-range day
```

## 配置

**必填项：** 将 `SEARXNG_URL` 环境变量设置为您的 SearXNG 实例地址：

```bash
export SEARXNG_URL=https://your-searxng-instance.com
```

或者您也可以在 Clawdbot 的配置文件中进行设置：
```json
{
  "env": {
    "SEARXNG_URL": "https://your-searxng-instance.com"
  }
}
```

默认值（未设置时）：`http://localhost:8080`

## 功能特点

- 🔒 注重隐私保护（使用您的本地实例）
- 🌐 多引擎聚合搜索结果
- 📰 多种搜索分类
- 🎨 丰富的格式化输出结果
- 🚀 快速的 JSON 模式，适用于程序化调用

## API

使用您本地的 SearXNG JSON API 端点进行搜索（默认情况下无需身份验证）。