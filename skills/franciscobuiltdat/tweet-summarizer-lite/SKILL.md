---
name: tweet-summarizer-lite
description: 从 Twitter/X 获取并汇总单条推文。支持基本搜索和单条推文的获取功能。这是一个轻量级工具，非常适合快速查找推文。
requiredEnv:
  - AUTH_TOKEN
  - CT0
requiredBins:
  - bird
permissions:
  - network: Contact X/Twitter API via bird CLI (uses session cookies)
  - filesystem: Write tweets to ~/.openclaw/workspace/data/tweets/
---
# Tweet Summarizer Lite

这是一个用于从 Twitter/X 获取并总结单条推文的轻量级工具，适合快速查看推文内容。

## 特点

- 🐦 **获取单条推文**：通过推文链接获取具体的推文内容。
- 🔍 **基本搜索**：根据查询条件搜索推文。
- 📊 **自动总结**：获取推文后自动生成摘要。
- 📁 **简单存储**：推文会存储在结构化的文件中。

## 前提条件

需要安装 `bird` CLI 并设置有效的 cookie 认证。请确保环境变量 `AUTH_TOKEN` 和 `CT0` 已设置。

## 快速入门

```bash
# Fetch a single tweet
python3 scripts/tweet.py https://x.com/user/status/123

# Search for tweets
python3 scripts/search_tweets.py --text "AI agents"

# Skip summary
python3 scripts/tweet.py https://x.com/user/status/123 -ns
```

## 使用方法

### 获取单条推文

```bash
python3 scripts/tweet.py <URL>
```

选项：
- `-ns` 或 `--no-summary`：跳过自动总结功能。

### 搜索已存储的推文

```bash
# By text content
python3 scripts/search_tweets.py --text "artificial intelligence"

# By source
python3 scripts/search_tweets.py --source elonmusk

# By date
python3 scripts/search_tweets.py --since 2026-02-01

# List all sources
python3 scripts/search_tweets.py --list-sources

# Storage stats
python3 scripts/search_tweets.py --stats
```

### 生成推文摘要

```bash
# From stored file
python3 scripts/summarize.py <file_path>

# From source
python3 scripts/summarize.py elonmusk
```

## 存储结构

```
~/.openclaw/workspace/data/tweets/
├── index.json           # Master search index
└── single/
    └── <tweet-id>/      # Individual tweets
        └── single_*.json
```

## 配置

请编辑 `config.json` 文件以配置工具的行为：

```json
{
  "defaults": {
    "show_summary": true,
    "auto_detect_urls": true,
    "default_mode": "single"
  }
}
```

## 直接使用 `bird` 命令

如果只需要快速查看推文内容而不需要存储，可以直接使用以下命令：

```bash
# Read tweet (plain text)
bird read <url-or-id> --plain

# Search
bird search "query" -n 20 --plain
```

## 升级到 Pro 版本

如需更多功能，可以尝试 [tweet-summarizer-pro](https://github.com/openclaw/openclaw-tweet-summarizer-pro)：
- 🧵 **获取完整对话线程**：获取整个推文对话串。
- 📂 **创建收藏夹**：将推文分类到自定义的收藏夹中。
- 👤 **用户时间线**：获取指定用户的推文。
- 🏠 **主时间线**：获取自己的主时间线或关注者的时间线。
- 🏷️ **添加标签**：为推文添加标签以便管理。
- 📦 **归档**：对推文进行归档和恢复。

## 脚本

| 脚本 | 描述 |
|--------|-------------|
| `tweet.py` | 获取单条推文并生成摘要。|
| `fetch_tweets.py` | 低级推文获取接口（仅支持获取单条推文）。|
| `search_tweets.py` | 搜索已存储的推文。|
| `summarize.py` | 生成推文摘要。|
| `config.py` | 管理工具的配置设置。|

## 文件结构

- `config.json`：默认配置文件。
- `config.example.json`：配置示例文件。
- `scripts/`：所有脚本文件存放目录。