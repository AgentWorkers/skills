---
name: search1api
description: 强大的网络搜索、内容爬取、新闻获取、站点地图生成、热门话题分析以及通过 `search1api` CLI（s1）进行的深度数据分析功能。该工具远超基本的 fetch 或搜索工具——它支持 13 种以上的搜索引擎（Google、Bing、DuckDuckGo、Reddit、GitHub、YouTube、arXiv、Baidu、X 等），能够适应多种网站以高效提取内容，并提供来自多个来源的新闻聚合服务。无论用户需要搜索网页、查找信息、研究某个主题、阅读或总结某个 URL 的内容、查看新闻、探索网站的链接、了解热门话题、进行深度数据分析，还是检查 API 的使用情况，都可以使用此功能。只需使用诸如“搜索”、“查找”、“了解详情”、“最近有什么新闻”、“这个链接的内容是什么”、“阅读这个页面”、“总结这个 URL 的内容”、“GitHub 上的热门内容”等指令即可触发该功能。即使用户没有明确使用“搜索”这个词，只要他们明显需要网络信息，也可以使用此工具。
metadata: {"openclaw": {"requires": {"env": ["SEARCH1API_KEY"], "bins": ["s1"]}, "primaryEnv": "SEARCH1API_KEY"}}
---
# Search1API CLI

通过 `s1` 命令行工具（`search1api-cli`）进行网页搜索和内容检索。

## 先决条件

在使用任何命令之前，请检查 `s1` 是否可用。如果不可用，请指导用户进行安装：

```bash
npm install -g search1api-cli
```

此外，还需要一个 API 密钥。请在 https://search1api.com 获取密钥，然后进行配置：

```bash
s1 config set-key <your-api-key>
```

或者设置环境变量 `SEARCH1API_KEY`。

如果命令出现“命令未找到”或身份验证错误，请提醒用户在重试前完成这些设置步骤。

## 使用场景

| 用户意图 | 命令 |
|---|---|
| 分享 URL/链接 → 读取并总结内容 | `s1 crawl <url>` |
| 搜索网页 | `s1 search "<query>"` |
| 查看新闻 | `s1 news "<query>"` |
| 探索网站的链接 | `s1 sitemap <url>` |
| 查看热门话题 | `s1 trending <service>` |
| 对问题进行深入分析 | `s1 reasoning "<content>"` |
| 查看剩余的 API 信用额度 | `s1 balance` |

## 动态调整

根据用户意图调整参数，不要仅使用默认值：

- **快速查询**（“搜索 X”，“X 是什么”）→ 使用 `-n 5`，不进行爬取
- **深入研究**（“彻底研究 X”，“全面分析”）→ 使用 `-n 15`，然后通过多次 `s1 crawl` 获取前 3–5 个结果
- **用户指定数量**（“查找 10 篇文章”）→ 使用 `-n` 参数匹配
- **时间范围**（“最新”，“最近”，“本周”）→ 使用 `-t day` 或 `-t month`
- **特定域名**（“在 Reddit 上搜索”，“查找 GitHub 仓库”）→ 使用 `-s reddit`，`-s github` 等
- **限定来源**（“仅从 arxiv.org 获取内容”）→ 使用 `--include arxiv.org`
- **中文查询** → 使用 `-s baidu` 可获得更好的结果

## 命令说明

### search

```bash
s1 search "<query>" [options]
```

| 选项 | 描述 | 默认值 |
|---|---|---|
| `-n, --max-results <N>` | 结果数量（1–50） | 10 |
| `-s, --service <engine>` | 搜索引擎 | google |
| `-c, --crawl <N>` | 爬取 N 个结果以获取完整内容 | 0 |
| `--include <sites...>` | 仅包含这些网站 | |
| `--exclude <sites...>` | 排除这些网站 | |
| `-t, --time <range>` | 时间范围（天，月，年） | |
| `--json` | 原始 JSON 输出 | |

支持的搜索引擎：google, bing, duckduckgo, yahoo, x, reddit, github, youtube, arxiv, wechat, bilibili, imdb, wikipedia

### news

```bash
s1 news "<query>" [options]
```

与 `search` 命令选项相同。支持的新闻服务：google, bing, duckduckgo, yahoo, hackernews。默认搜索引擎：bing。

当用户请求最新新闻时，务必添加 `-t day` 参数。

### crawl

```bash
s1 crawl <url>
```

从 URL 中提取干净的内容。当用户分享链接时可以使用此命令。

### sitemap

```bash
s1 sitemap <url>
```

返回某个 URL/域名下的所有链接。

### reasoning

```bash
s1 reasoning "<content>"
# or
s1 reason "<content>"
```

利用 DeepSeek R1 进行深入分析，适用于复杂的问题解答。

### trending

```bash
s1 trending <service> [-n <N>]
```

支持的服务：github, hackernews。

### balance

```bash
s1 balance
```

显示剩余的 API 信用额度。

## 工作流程

### 深入研究

1. `s1 search "<topic>" -n 15` → 获取广泛的结果
2. `s1 crawl <url>` → 爬取结果中的前 3–5 个相关 URL
3. 将收集到的所有内容整合成连贯的答案，并附上来源引用

### URL 摘要

1. `s1 crawl <url>` → 获取页面内容
2. 根据内容进行总结或回答问题

### 热门话题分析

1. `s1 trending github -n 10` → 发现热门话题
2. `s1 search "<interesting topic>" -t day` → 查找详细信息
3. `s1 crawl <url>` → 如有需要，阅读完整文章

## 输出处理

- 默认情况下，命令会生成易于阅读的格式化输出
- 对任何命令添加 `--json` 可获得原始 JSON 格式的数据（适用于程序化处理）
- 在获取结果后，务必为用户总结和整理信息，而不仅仅是直接输出原始数据

## 参考资料

- [使用示例](reference/examples.md) — 了解更多使用模式