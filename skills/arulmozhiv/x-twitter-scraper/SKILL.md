# Twitter/X 账号抓取工具

这是一个基于浏览器的 Twitter/X 账号发现与抓取工具。

> 该工具属于 **[ScrapeClaw](https://www.scrapeclaw.cc/)** 系列，该系列是一套专为 Instagram、YouTube、Twitter 和 Facebook 设计的、可投入生产的社交媒体抓取工具，使用 Python 和 Playwright 开发，无需 API 密钥。

```yaml
---
name: twitter-scraper
description: Discover and scrape Twitter/X public profiles from your browser.
emoji: 🐦
version: 1.0.2
author: influenza
tags:
  - twitter
  - x
  - scraping
  - social-media
  - profile-discovery
  - influencer-discovery
metadata:
  clawdbot:
    requires:
      bins:
        - python3
        - chromium

    config:
      stateDirs:
        - data/output
        - data/queue
        - thumbnails
      outputFormats:
        - json
        - csv
---
```

## 概述

该工具提供两阶段的 Twitter/X 账号抓取流程：

1. **账号发现**：通过 Google 自定义搜索 API 或 DuckDuckGo 找到 Twitter 账号。
2. **浏览器抓取**：使用 Playwright 进行公开账号的抓取，并具备反检测机制（无需登录）。

## 主要功能

- 🔍  - 按地理位置和类别查找 Twitter/X 账号
- 🌐  - 完整的浏览器模拟环境，确保抓取数据的准确性
- 🛡️  - 浏览器指纹识别、模拟人类行为以及使用隐蔽脚本
- 📊  - 获取账号信息、关注者、推文、互动数据及媒体内容
- 💾  - 支持将数据导出为 JSON 或 CSV 格式，并附带下载的缩略图
- 🔄  - 可恢复中断的抓取会话
- ⚡  - 自动跳过私密账号、关注者数量较少的账号以及被暂停使用的账号
- 🌍  - 内置住宅代理支持，支持 4 家代理服务提供商

#### 获取 Google API 凭据（可选）

1. 访问 [Google Cloud 控制台](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用“自定义搜索 API”
4. 创建 API 凭据（API 密钥）
5. 访问 [可编程搜索引擎](https://programmablesearchengine.google.com/)
6. 创建一个搜索引擎，设置搜索目标为 `x.com` 和 `twitter.com`
7. 复制搜索引擎 ID

如果未配置 Google API，系统将自动切换到 DuckDuckGo（无需 API 密钥）。

## 使用方法

### 代理工具接口

对于 OpenClaw 代理的集成，该工具提供 JSON 格式的输出数据：

```bash
# Discover Twitter profiles (returns JSON)
discover --location "Miami" --category "tech" --output json

# Discover profiles in a specific category (returns JSON)
discover --location "New York" --category "crypto" --output json

# Scrape single profile (returns JSON)
scrape --username elonmusk --output json

# Scrape from a queue file
scrape data/queue/Miami_tech_20260220_120000.json
```

## 输出数据结构

### 账号数据结构

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

### 队列文件结构

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

### 账号影响力分级

| 分级 | 关注者数量范围 |
|-------|---------------------|
| nano  | < 1,000             |
| micro | 1,000 - 10,000      |
| mid   | 10,000 - 100,000    |
| macro | 100,000 - 1,000,000    |
| mega  | > 1,000,000         |

### 文件输出路径

- **队列文件**：`data/queue/{location}_{category}_{timestamp}.json`
- **抓取数据**：`data/output/{username}.json`
- **缩略图**：`thumbnails/{username}/profile_*.jpg`, `thumbnails/{username}/tweet_media_*.jpg`
- **导出文件**：`data/export_{timestamp}.json`, `data/export_{timestamp}.csv`

## 配置

编辑 `config/scraper_config.json` 文件进行配置：

```json
{
  "proxy": {
    "enabled": false,
    "provider": "brightdata",
    "country": "",
    "sticky": true,
    "sticky_ttl_minutes": 10
  },
  "google_search": {
    "enabled": true,
    "api_key": "",
    "search_engine_id": "",
    "queries_per_location": 3
  },
  "scraper": {
    "headless": false,
    "min_followers": 500,
    "max_tweets": 20,
    "download_thumbnails": true,
    "max_thumbnails": 6,
    "delay_between_profiles": [4, 8],
    "timeout": 60000
  },
  "cities": ["New York", "Los Angeles", "Miami", "Chicago"],
  "categories": ["tech", "politics", "sports", "entertainment", "news", "crypto"]
}
```

## 过滤规则

该工具会自动过滤以下类型的账号：

- ❌ 被暂停或停用的账号
- ❌ 被保护的（私密）账号
- ❌ 关注者数量少于 500 的账号（可配置）
- ❌ 不存在的账号
- ❌ 已经被抓取过的账号（避免重复抓取）

## 反检测机制

该工具采用多种反检测技术：

- **浏览器指纹识别**：使用 4 种不同的浏览器配置（视口、用户代理、时区、WebGL 等）
- **隐蔽 JavaScript**：隐藏 `navigator.webdriver`，伪造插件/语言设置、硬件信息，生成随机 canvas 图像
- **模拟人类行为**：随机延迟、鼠标移动、滚动模式
- **网络请求随机化**：请求之间随机调整时间间隔
- **处理登录提示**：自动关闭 Twitter 的登录提示界面

## 常见问题解决方法

### 未发现账号

- 检查 Google API 密钥和配额是否有效
- 确保已正确配置用于搜索 `x.com` 和 `twitter.com` 的搜索引擎 ID
- 尝试不同的地理位置或类别组合
- 如果 Google API 使用失败，系统会自动切换到 DuckDuckGo

### 速率限制

- 降低抓取速度（通过配置文件调整延迟时间）
- 在非高峰时段运行抓取任务
- **使用住宅代理**（详见下文）

### 登录提示问题

- 该工具会自动关闭登录提示界面
- 如果内容被屏蔽，可以尝试禁用 `--headless` 参数以进行可视化调试

---

## 🌐 住宅代理支持

### 为什么需要使用住宅代理？

在没有使用住宅代理的情况下大规模运行抓取任务时，很容易导致 IP 被 Twitter 封禁。以下是使用代理的必要性：

| 优势 | 说明 |
|-----------|-------------|
| **避免 IP 被封禁** | 住宅代理的 IP 地址看起来像真实用户的地址，而非数据中心的机器人地址，因此更难被 Twitter 标记为异常行为。 |
| **自动 IP 旋转**：每次请求都会使用新的 IP 地址，避免同一 IP 被多次使用导致速率限制。 |
| **地理定位**：将流量路由到目标国家/地区，确保抓取的内容符合目标用户的地域设置。 |
| **保持会话稳定性**：在指定时间内（例如 10 分钟）使用相同的 IP 地址，有助于维持稳定的浏览会话。 |
| **更高的抓取成功率**：使用住宅代理的抓取成功率可达到 95% 以上，而使用数据中心代理的成功率约为 30%。 |
| **长时间抓取**：可以连续数小时或数天无间断地抓取大量账号信息。 |
| **并发抓取**：可以在不同 IP 地址上同时运行多个浏览器实例。

### 推荐的代理服务提供商

我们与多家领先的住宅代理服务提供商有合作关系。使用这些链接可以帮助我们持续改进该工具：

| 服务提供商 | 适用场景 | 注册链接 |
|----------|----------|---------|
| **Bright Data** | 全球最大的代理网络，拥有 7,200 万多个 IP 地址，企业级服务 | 👉 [**注册 Bright Data**](https://get.brightdata.com/o1kpd2da8iv4) |
| **IProyal** | 按需付费，支持 195 个国家，无流量使用期限限制 | 👉 [**注册 IProyal**](https://iproyal.com/?r=ScrapeClaw) |
| **Storm Proxies** | 快速且可靠的代理服务，提供易于使用的 API，价格合理 | 👉 [**注册 Storm Proxies**](https://stormproxies.com/clients/aff/go/scrapeclaw) |
| **NetNut** | 提供 ISP 级别的代理服务，拥有 5,200 万多个 IP 地址，直接连接 | 👉 [**注册 NetNut**](https://netnut.io?ref=mwrlzwv) |

### 设置步骤

#### 1. 获取代理服务提供商的凭据

在以上提供商中注册，然后获取以下信息：
- **用户名**（来自提供商的控制面板）
- **密码**（来自提供商的控制面板）
- **主机地址** 和 **端口号**（由提供商预先配置，或根据需要自定义）

#### 2. 通过环境变量进行配置

```bash
export PROXY_ENABLED=true
export PROXY_PROVIDER=brightdata    # brightdata | iproyal | stormproxies | netnut | custom
export PROXY_USERNAME=your_user
export PROXY_PASSWORD=your_pass
export PROXY_COUNTRY=us             # optional: two-letter country code
export PROXY_STICKY=true            # optional: keep same IP per session
```

#### 3. 各服务提供商的默认主机/端口号

设置 `provider` 时，系统会自动配置以下参数：

| 服务提供商 | 主机地址 | 端口号 |
|----------|------|------|
| Bright Data | `brd.superproxy.io` | `22225` |
| IProyal | `proxy.iproyal.com` | `12321` |
| Storm Proxies | `rotating.stormproxies.com` | `9999` |
| NetNut | `gw-resi.netnut.io` | `5959` |

如果你的代理服务提供商使用不同的配置，请通过 `PROXY_HOST` 和 `PROXY_PORT` 环境变量进行自定义设置。

#### 4. 自定义代理服务提供商

对于其他代理服务，将 `provider` 设置为 `custom`，并手动输入主机地址和端口号：

```json
{
  "proxy": {
    "enabled": true,
    "provider": "custom",
    "host": "your.proxy.host",
    "port": 8080,
    "username": "user",
    "password": "pass"
  }
}
```

### 使用代理运行抓取工具

配置完成后，工具会自动使用代理进行抓取，无需额外设置：

```bash
# Discover and scrape as usual — proxy is applied automatically
python main.py discover --location "Miami" --category "tech"
python main.py scrape --username elonmusk

# The log will confirm proxy is active:
# INFO - Proxy enabled: <ProxyManager provider=brightdata enabled host=brd.superproxy.io:22225>
# INFO - Browser using proxy: brightdata → brd.superproxy.io:22225
```

### 程序化使用代理管理器

```python
from proxy_manager import ProxyManager

# From config (auto-reads config/scraper_config.json)
pm = ProxyManager.from_config()

# From environment variables
pm = ProxyManager.from_env()

# Manual construction
pm = ProxyManager(
    provider="brightdata",
    username="your_user",
    password="your_pass",
    country="us",
    sticky=True
)

# For Playwright browser context
proxy = pm.get_playwright_proxy()
# → {"server": "http://brd.superproxy.io:22225", "username": "user-country-us-session-abc123", "password": "pass"}

# For requests / aiohttp
proxies = pm.get_requests_proxy()
# → {"http": "http://user:pass@host:port", "https": "http://user:pass@host:port"}

# Force new IP (rotates session ID)
pm.rotate_session()

# Debug info
print(pm.info())
```

### 长时间抓取的最佳实践

1. **使用稳定的 IP 地址**：Twitter 要求在浏览会话期间使用相同的 IP 地址，因此请设置 `"sticky": true`。
2. **选择正确的目标国家**：设置 `"country": "us"`（或目标地区），以确保 Twitter 显示正确的本地化内容。
3. **结合反检测机制**：该工具已具备指纹识别、隐蔽脚本和模拟人类行为的功能，代理作为最后的防护层。
4. **在批量抓取之间轮换会话**：在处理大量账号时，调用 `pm.rotate_session()` 以获取新的 IP 地址。
5. **设置适当的延迟**：即使使用了代理，也要遵守配置文件中的 `delay_between_profiles` 设置（默认为 4-8 秒），以避免被识别为恶意行为。
6. **监控代理服务提供商的监控面板**：所有提供商都会提供带宽使用情况和抓取成功率的数据。

## 注意事项

- **无需登录**：仅抓取公开可见的内容。
- **进度跟踪与恢复**：队列文件会记录抓取进度，可以使用 `--resume` 命令恢复中断的抓取任务。
- **速率限制**：遇到速率限制时，系统会等待 60 秒；达到每日限制时则会停止抓取。
- **Twitter 账号识别**：使用 `data[TestId` 属性进行识别（该属性在界面更新后依然有效），同时备选方案包括使用 `aria-label` 和结构化选择器。