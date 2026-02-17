---
name: x-tweet-fetcher
description: 无需登录或使用 API 密钥即可从 X/Twitter 获取推文。支持普通推文、长推文、引用推文以及完整的 X 文章。完全无需依赖任何外部库或进行任何配置。
---
# X（Twitter）推文获取工具

无需认证即可从X/Twitter获取推文，该工具使用FxTwitter API。

## 支持获取的内容类型

| 内容类型 | 是否支持 |
|-------------|---------|
| 普通推文       | ✅ 全文 + 统计信息 |
| 长推文（Twitter Blue） | ✅ 全文 |
| X平台上的长篇文章 | ✅ 完整文章内容 |
| 引用推文     | ✅ 包含引用内容 |
| 推文统计信息（点赞/转发/浏览量） | ✅ 包含 |

## 使用方法

### 命令行界面（CLI）

```bash
# JSON output
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123456"

# Pretty JSON
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123456" --pretty

# Text only (human readable)
python3 scripts/fetch_tweet.py --url "https://x.com/user/status/123456" --text-only
```

### 从代理代码中使用

```python
from scripts.fetch_tweet import fetch_tweet

result = fetch_tweet("https://x.com/user/status/123456")
tweet = result["tweet"]

# Regular tweet
print(tweet["text"])

# X Article (long-form)
if tweet["is_article"]:
    print(tweet["article"]["title"])
    print(tweet["article"]["full_text"])  # Complete article
    print(tweet["article"]["word_count"])
```

## 输出格式

```json
{
  "url": "https://x.com/user/status/123",
  "username": "user",
  "tweet_id": "123",
  "tweet": {
    "text": "Tweet content...",
    "author": "Display Name",
    "screen_name": "username",
    "likes": 100,
    "retweets": 50,
    "bookmarks": 25,
    "views": 10000,
    "replies_count": 30,
    "created_at": "Mon Jan 01 12:00:00 +0000 2026",
    "is_note_tweet": false,
    "is_article": true,
    "article": {
      "title": "Article Title",
      "full_text": "Complete article content...",
      "word_count": 4847,
      "char_count": 27705
    }
  }
}
```

## 系统要求

- Python 3.7及以上版本
- 无需安装任何外部包（仅使用标准库）
- 无需API密钥
- 无需登录

## 工作原理

该工具使用[FxTwitter](https://github.com/FxEmbed/FxEmbed)的公共API（`api.fxtwitter.com`）来代理X/Twitter的内容。获取到的文章会以结构化的数据块形式返回，随后被重新组合成完整的文本。

## 限制

- 无法获取回复推文（仅能通过`replies_count`字段获取回复数量）  
  - 获取回复内容需要依赖浏览器自动化工具（如Camofox/Nitter）  
  - 为保持零依赖架构，这些功能已被移除  
  - 虽然提供了`--replies`参数，但会返回提示性错误信息  
- 无法获取已删除或私有的推文  
- 数据获取频率受FxTwitter服务可用性的影响  
- 如果FxTwitter服务中断，该工具将无法正常使用（无备用方案）

## 文件结构

```
skills/x-tweet-fetcher/
├── SKILL.md              (this file)
└── scripts/
    └── fetch_tweet.py    (single file, zero deps)
```