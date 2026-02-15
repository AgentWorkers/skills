---
name: technews
description: 从 TechMeme 获取热门新闻，汇总相关文章的内容，并展示社交媒体上的用户反应。当用户请求科技新闻（例如输入 “/technews”）时，可以使用该功能。
metadata: {"openclaw":{"emoji":"📰"}}
---

# TechNews 技能

该技能从 TechMeme 获取热门新闻，总结相关文章的内容，并展示社交媒体上的讨论热点。

## 使用方法

**命令:** `/technews`

该命令会从 TechMeme 获取前十条热门新闻，提供每篇文章的摘要以及社交媒体上的重要反馈。

## 配置要求

该技能需要以下环境：
- Python 3.9 或更高版本
- `requests` 和 `beautifulsoup4` 库
- 可选：`tiktoken` 库（用于根据令牌进行内容截断）

安装所需依赖包：
```bash
pip install requests beautifulsoup4
```

## 架构

该技能的工作流程分为三个阶段：
1. **抓取 TechMeme 的热门新闻** — `scripts/techmeme_scraper.py` 负责获取并解析 TechMeme 的热门新闻。
2. **获取文章内容** — `scripts/article_fetcher.py` 并行获取文章的详细内容。
3. **生成摘要** — `scripts/summarizer.py` 生成文章的摘要并分析社交媒体上的反馈。

## 命令说明

### `/technews`

该命令用于获取并展示最新的科技新闻。

**输出内容包括：**
- 新闻标题和原始链接
- 由 AI 生成的摘要
- 社交媒体上的热门评论（例如 Twitter 上的反馈）
- 根据用户偏好计算出的新闻相关性得分

## 工作原理

1. 从 TechMeme 的首页抓取热门新闻（默认显示前十条）。
2. 对于每条新闻，获取其链接对应的文章内容。
3. 生成简短的摘要（2-3 句）。
4. 检查社交媒体上的相关反馈。
5. 以清晰易读的格式展示结果。

## 数据存储

- `<workspace>/memory/technews_history.json`：用于存储最近获取的新闻信息，以避免重复展示。

## 使用示例

- 输入 `/technews`，即可获取最新的科技新闻摘要。

## 未来扩展性

该技能支持扩展到其他新闻来源：
- Hacker News（`/hn`）
- Reddit（`/reddit`）
- 其他科技新闻聚合平台

由于其模块化的设计，只需添加新的处理程序，即可轻松支持新的数据源，而无需修改核心功能。