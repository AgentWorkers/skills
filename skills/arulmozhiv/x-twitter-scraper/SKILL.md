# Twitter/X 数据抓取工具

**名称：** `twitter-scraper`  
**版本：** `1.0.0`  
**运行环境：** `python3`  
**浏览器：** `chromium`（通过 Playwright 实现）

## 概述

这是一个用于抓取 Twitter/X 公开用户资料的抓取工具，分为两个阶段：

1. **用户资料发现**：通过 Google 自定义搜索 API 或 DuckDuckGo（搜索 `x.com` 和 `twitter.com`）来查找 Twitter 账号。  
2. **浏览器抓取**：使用 Playwright 进行抓取，具备反检测机制（无需登录）。

## 设置

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### Google 自定义搜索 API（可选）

**通过 Google 发现用户资料：**
1. 在 [Google Cloud Console](https://console.cloud.google.com/) 创建 API 密钥。  
2. 在 [cse.google.com](https://cse.google.com/) 创建一个可编程搜索引擎，并将其范围设置为 `x.com` 和 `twitter.com`。  
3. 在 `config/scraper_config.json` 文件中配置相关参数：  
   ```json
   {
     "google_search": {
       "enabled": true,
       "api_key": "YOUR_API_KEY",
       "search_engine_id": "YOUR_CX_ID"
     }
   }
   ```

**如果未配置 Google 自定义搜索 API，则工具会使用 DuckDuckGo 进行用户资料发现（无需 API 密钥）。**

## 命令

### 发现用户资料  
```bash
# Interactive mode
python main.py discover

# Specific location + category
python main.py discover --location "New York" --category tech --count 15

# Batch mode (multiple cities x categories)
python main.py discover --batch

# JSON output (for agent integration)
python main.py discover --location "Miami" --category crypto --output json
```

### 抓取用户资料  
```bash
# Scrape from a queue file
python main.py scrape data/queue/New_York_tech_20260217_120000.json

# Scrape a single profile
python main.py scrape --username elonmusk

# Scrape multiple usernames (manual list)
python main.py scrape --usernames user1,user2,user3 --category tech

# Headless mode
python main.py scrape --username nasa --headless

# JSON output
python main.py scrape --username elonmusk --output json
```

### 列出待抓取的文件  
```bash
python main.py list
```

### 导出数据  
```bash
# Export to both JSON and CSV
python main.py export --format both

# JSON only
python main.py export --format json

# CSV only (produces profiles CSV + tweets CSV)
python main.py export --format csv
```

## 目录结构  

| 目录          | 内容                |
|---------------|-------------------|
| `data/queue/`     | 待抓取的文件：`{location}_{category}_{timestamp}.json` |
| `data/output/`    | 抓取到的用户资料：`{username}.json` |
| `thumbnails/`     | 下载的图片：`{username}/profile_*.jpg`, `{username}/tweet_media_*.jpg` |

## 输出格式

### 用户资料 JSON 文件（`data/output/{username}.json`）  
```json
{
  "username": "elonmusk",
  "display_name": "Elon Musk",
  "bio": "...",
  "followers": 180000000,
  "following": 800,
  "tweets_count": 45000,
  "is_verified": true,
  "profile_pic_url": "https://...",
  "profile_pic_local": "thumbnails/elonmusk/profile_abc123.jpg",
  "user_location": "Mars & Earth",
  "join_date": "June 2009",
  "website": "https://x.ai",
  "influencer_tier": "mega",
  "category": "tech",
  "scrape_location": "New York",
  "scraped_at": "2026-02-17T12:00:00",
  "recent_tweets": [
    {
      "id": "1234567890",
      "text": "Tweet content...",
      "timestamp": "2026-02-17T10:30:00.000Z",
      "likes": 50000,
      "retweets": 12000,
      "replies": 3000,
      "views": "5.2M",
      "media_urls": ["https://..."],
      "media_local": ["thumbnails/elonmusk/tweet_media_0_def456.jpg"],
      "is_retweet": false,
      "is_reply": false,
      "url": "https://x.com/elonmusk/status/1234567890"
    }
  ]
}
```

### 待抓取文件（`data/queue/{location}_{category}_{timestamp}.json`）  
```json
{
  "location": "New York",
  "category": "tech",
  "total": 15,
  "usernames": ["user1", "user2", "..."],
  "completed": ["user1"],
  "failed": {"user3": "not_found"},
  "current_index": 2,
  "created_at": "2026-02-17T12:00:00",
  "source": "google_api"
}
```

## 用户影响力分级  

| 分级        | 关注者数量           |
|--------------|----------------------|
| nano          | < 1,000               |
| micro          | 1,000 – 10,000             |
| mid           | 10,000 – 100,000             |
| macro          | 100,000 – 1,000,000           |
| mega          | > 1,000,000               |

## 配置文件（`config/scraper_config.json`）

| 参数          | 默认值            | 说明                          |
|---------------|-----------------------------|
| `scraper.headless` | `false`          | 以无界面模式运行浏览器                 |
| `scraper.min_followers` | `500`            | 跳过关注者数量低于此值的用户资料           |
| `scraper.max_tweets` | `20`            | 每个用户资料最多抓取 20 条推文             |
| `scraper.max_thumbnails` | `6`            | 每个用户资料最多下载 6 张图片             |
| `scraper.download_thumbnails` | `true`          | 下载用户资料的图片和媒体文件               |
| `scraper.delay_between_profiles` | `[4, 8]`          | 抓取请求之间的随机延迟时间（秒）             |
| `scraper.timeout` | `60000`          | 页面加载超时时间（毫秒）                 |

## 反检测机制

该工具采用了多种反检测技术：
- **浏览器指纹识别**：通过轮换不同的浏览器配置（视口、用户代理、时区、WebGL 等）来避免被识别。  
- **隐藏 JavaScript 功能**：隐藏 `navigator.webdriver`，伪造插件/语言/硬件信息，并添加随机噪声到页面内容中。  
- **模拟人类行为**：设置随机延迟、鼠标移动和滚动模式。  
- **网络请求随机化**：调整请求之间的时间间隔。  
- **处理登录提示**：自动关闭 Twitter 的登录提示和覆盖层。

## 过滤条件

如果满足以下条件，用户资料将被自动跳过：
- 账号不存在或被暂停。  
- 账号设置为私密状态。  
- 关注者数量低于配置的 `min_followers` 值。

## 注意事项：
- **无需登录**：仅抓取公开可见的内容。  
- **进度跟踪**：待抓取的文件用于记录抓取进度；可以使用 `--resume` 命令恢复中断的抓取任务。  
- **速率限制**：遇到速率限制时等待 60 秒；达到每日抓取上限时停止抓取。  
- **用户资料选择**：使用 `data-testid` 属性进行选择（该属性在用户界面更改后仍然有效）；如果 `data-testid` 无效，则使用 `aria-label` 和结构化选择器作为备用方式。