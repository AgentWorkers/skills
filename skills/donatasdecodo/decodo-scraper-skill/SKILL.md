---
name: decodo-scraper
description: 使用 Decodo Scraper OpenClaw 技能，您可以搜索 Google、抓取网页内容、亚马逊产品页面、YouTube 字幕，或者 Reddit 上的帖子和子版块（post/subreddit）的数据。
homepage: https://decodo.com
credentials:
  - DECODO_AUTH_TOKEN
env:
  required:
    - DECODO_AUTH_TOKEN
---
# Decodo Scraper OpenClaw 技能

使用这些技能可以通过 [Decodo Web Scraping API](https://help.decodo.com/docs/web-scraping-api/google-search) 在 Google 上进行搜索、抓取任何 URL 的内容，或获取 YouTube 的字幕。  
- **Search**：返回一个包含搜索结果的 JSON 对象；  
- **Scrape URL**：返回纯 Markdown 格式的网页内容；  
- **Amazon** 和 **Amazon search**：返回解析后的产品页面或搜索结果（JSON 格式）；  
- **YouTube subtitles**：返回视频的字幕或文本；  
- **Reddit post** 和 **Reddit subreddit**：返回 Reddit 帖子的内容（JSON 格式）。

**身份验证：**  
在您的环境变量中设置 `DECODO_AUTH_TOKEN`（从 Decodo 控制台 → Scraping APIs 获取的基本认证令牌），或者将其保存在仓库根目录下的 `.env` 文件中。

**错误处理：**  
如果执行失败，脚本会将错误信息写入标准错误输出（stderr），并以代码 1 退出。

---

## 工具

### 1. 在 Google 上搜索  
用于查找 URL、答案或结构化的搜索结果。API 返回的 JSON 对象中包含多个部分（并非每个查询都会包含所有部分）：  
| 部分        | 描述                    |
|--------------|-------------------------|
| `organic`     | 主要搜索结果（标题、链接、片段）        |
| `ai_overviews` | Google 显示的人工智能生成的概要或摘要 |
| `paid`       | 广告/付费搜索结果             |
| `related_questions` | “人们也问”类型的问答             |
| `related_searches` | 建议的相关搜索查询             |
| `discussions_and_forums` | 论坛或讨论区的结果             |

脚本仅输出 `results` 部分；分页信息（`page`、`last_visible_page`、`parse_status_code`）不会被包含。

**命令：**  
```bash
python3 tools/scrape.py --target google_search --query "your search query"
```

**示例：**  
```bash
python3 tools/scrape.py --target google_search --query "best laptops 2025"
python3 tools/scrape.py --target google_search --query "python requests tutorial"
```

**可选参数：**  
`--geo us` 或 `--locale en` 用于指定地理位置或语言。

---

### 2. 抓取 URL 内容  
用于获取特定网页的内容。默认情况下，API 以 Markdown 格式返回内容（这种格式更易于处理，且所需的 API 请求次数较少）。

**命令：**  
```bash
python3 tools/scrape.py --target universal --url "https://example.com"
```

**示例：**  
```bash
python3 tools/scrape.py --target universal --url "https://example.com"
python3 tools/scrape.py --target universal --url "https://news.ycombinator.com/"
```

---

### 3. Amazon 产品页面  
用于获取 Amazon 产品页面的解析数据。将产品页面的 URL 作为参数传递。脚本会发送 `parse: true` 参数，并输出 `results` 部分的内容（例如广告、产品详情等）。

**命令：**  
```bash
python3 tools/scrape.py --target amazon --url "https://www.amazon.com/dp/PRODUCT_ID"
```

**示例：**  
```bash
python3 tools/scrape.py --target amazon --url "https://www.amazon.com/dp/B09H74FXNW"
```

---

### 4. Amazon 搜索  
用于在 Amazon 上进行搜索并获取解析后的结果（搜索结果列表、配送邮政编码等）。将搜索查询作为参数传递。

**命令：**  
```bash
python3 tools/scrape.py --target amazon_search --query "your search query"
```

**示例：**  
```bash
python3 tools/scrape.py --target amazon_search --query "laptop"
```

---

### 5. YouTube 字幕  
用于获取 YouTube 视频的字幕或文本。将视频 ID（例如 `youtube.com/watch?v=VIDEO_ID`）作为参数传递。

**命令：**  
```bash
python3 tools/scrape.py --target youtube_subtitles --query "VIDEO_ID"
```

**示例：**  
```bash
python3 tools/scrape.py --target youtube_subtitles --query "dFu9aKJoqGg"
```

---

### 6. Reddit 帖子  
用于获取 Reddit 帖子的内容。将帖子的完整 URL 作为参数传递。

**命令：**  
```bash
python3 tools/scrape.py --target reddit_post --url "https://www.reddit.com/r/SUBREDDIT/comments/ID/..."
```

**示例：**  
```bash
python3 tools/scrape.py --target reddit_post --url "https://www.reddit.com/r/nba/comments/17jrqc5/serious_next_day_thread_postgame_discussion/"
```

---

### 7. Reddit 子版块  
用于获取 Reddit 子版块中的帖子列表。将子版块的 URL 作为参数传递。

**命令：**  
```bash
python3 tools/scrape.py --target reddit_subreddit --url "https://www.reddit.com/r/SUBREDDIT/"
```

**示例：**  
```bash
python3 tools/scrape.py --target reddit_subreddit --url "https://www.reddit.com/r/nba/"
```

---

## 总结  

| 功能                | 目标                    | 参数                | 示例命令                |
|------------------|------------------|------------------|----------------------|
| 在 Google 上搜索       | `google_search`         | `--query`            | `python3 tools/scrape.py --target google_search --query "laptop"` |
| 抓取网页内容       | `universal`          | `--url`            | `python3 tools/scrape.py --target universal --url "https://example.com"` |
| 获取 Amazon 产品信息   | `amazon`            | `--url`            | `python3 tools/scrape.py --target amazon --url "https://www.amazon.com/dp/B09H74FXNW"` |
| 在 Amazon 上搜索       | `amazon_search`         | `--query`            | `python3 tools/scrape.py --target amazon_search --query "laptop"` |
| 获取 YouTube 字幕       | `youtube_subtitles`      | `--query`            | `python3 tools/scrape.py --target youtube_subtitles --query "dFu9aKJoqGg"` |
| 获取 Reddit 帖子内容     | `reddit_post`          | `--url`            | `python3 tools/scrape.py --target reddit_post --url "https://www.reddit.com/r/nba/comments/17jrqc5/..."` |
| 获取 Reddit 子版块内容     | `reddit_subreddit`         | `--url`            | `python3 tools/scrape.py --target reddit_subreddit --url "https://www.reddit.com/r/nba/"` |

**输出格式：**  
- **Search**：返回 JSON 格式的搜索结果；  
- **Scrape URL**：返回 Markdown 格式的网页内容；  
- **Amazon / Amazon search**：返回 JSON 格式的产品信息或搜索结果；  
- **YouTube**：返回视频的字幕或文本；  
- **Reddit**：返回 JSON 格式的帖子内容。