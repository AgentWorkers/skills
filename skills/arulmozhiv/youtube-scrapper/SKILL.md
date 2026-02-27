# YouTube频道抓取工具

这是一个基于浏览器的YouTube频道发现和抓取工具。

> 该工具属于**[ScrapeClaw](https://www.scrapeclaw.cc/)**系列——一套专为Instagram、YouTube、X/Twitter和Facebook开发的、可投入生产的社交媒体抓取工具，支持Python和Playwright框架，无需API密钥。

```yaml
---
name: youtube-scrapper
description: Discover and scrape YouTube channels from your browser.
emoji: 📺
version: 1.0.2
author: influenza
tags:
  - youtube
  - scraping
  - social-media
  - channel-discovery
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

该工具提供了两阶段的YouTube抓取流程：

1. **频道发现**——通过Google搜索查找YouTube频道（基于浏览器，无需API密钥）
2. **浏览器抓取**——使用Playwright进行抓取，具备反检测机制（无需登录）

## 特点

- 🔍  - 按地理位置和类别发现YouTube频道
- 🌐  - 完整的浏览器模拟功能，确保抓取数据的准确性
- 🛡️  - 浏览器指纹识别、模拟人类行为以及使用隐蔽脚本
- 📊  - 提供频道信息、订阅者数量、观看次数、视频内容、互动数据及媒体文件
- 💾  - 支持将数据导出为JSON格式，并附带下载的缩略图
- 🔄  - 可恢复中断的抓取任务
- ⚡  - 自动跳过无法访问的频道或订阅者较少的频道
- 🌍  - 内置住宅代理支持，支持4家代理服务提供商
- 🗺️  - 提供美国、英国、欧洲、印度、海湾地区和东亚的地域配置选项

## 使用方法

### 代理工具接口

对于OpenClaw代理的集成，该工具会输出JSON格式的数据：

```bash
# Discover YouTube channels (returns JSON queue)
python scripts/youtube_channel_discovery.py --categories tech --locations India

# Scrape from a queue file
python scripts/youtube_channel_scraper.py --queue data/queue/your_queue_file.json

# Full orchestration — discover + scrape in one go
python scripts/youtube_orchestrator.py --config resources/scraper_config_ind.json
```

## 输出数据

### 频道数据结构

```json
{
  "channel_name": "Marques Brownlee",
  "channel_url": "https://www.youtube.com/@mkbhd",
  "subscribers": 19200000,
  "total_views": 4500000000,
  "video_count": 1800,
  "description": "MKBHD: Quality Tech Videos...",
  "joined_date": "Mar 21, 2008",
  "country": "United States",
  "profile_pic_url": "https://...",
  "profile_pic_local": "thumbnails/mkbhd/profile_abc123.jpg",
  "banner_url": "https://...",
  "banner_local": "thumbnails/mkbhd/banner_def456.jpg",
  "influencer_tier": "mega",
  "category": "tech",
  "scrape_location": "New York",
  "scraped_at": "2026-02-17T12:00:00",
  "recent_videos": [
    {
      "title": "Galaxy S26 Ultra Review",
      "url": "https://www.youtube.com/watch?v=...",
      "views": 5200000,
      "published": "2 days ago",
      "duration": "14:32",
      "thumbnail_url": "https://...",
      "thumbnail_local": "thumbnails/mkbhd/video_0_ghi789.jpg"
    }
  ]
}
```

### 队列文件结构

```json
{
  "location": "India",
  "category": "tech",
  "total": 20,
  "channels": ["@channel1", "@channel2", "..."],
  "completed": ["@channel1"],
  "failed": {"@channel3": "not_found"},
  "current_index": 2,
  "created_at": "2026-02-17T12:00:00",
  "source": "google_search"
}
```

### 博主等级划分

| 等级 | 订阅者数量范围 |
|-------|---------------------|
| nano  | < 1,000             |
| micro | 1,000 – 10,000      |
| mid   | 10,000 – 100,000    |
| macro | 100,000 – 1,000,000    |
| mega  | > 1,000,000         |

### 文件输出路径

- **队列文件**: `data/queue/{region}/{location}_{category}_{timestamp}.json`
- **抓取数据**: `data/output_{region}/{channel_name}.json`
- **缩略图**: `thumbnails_{region}/{channel}/profile_*.jpg`, `thumbnails_{region}/{channel}/video_*.jpg`
- **进度文件**: `data/progress/discovery_progress_{region}.json`

## 配置

地域配置文件位于`resources/`目录下：

```
resources/scraper_config_us.json
resources/scraper_config_uk.json
resources/scraper_config_eur.json
resources/scraper_config_ind.json
resources/scraper_config_gulf.json
resources/scraper_config_east.json
```

示例配置文件（`resources/scraper_config_ind.json`）:

```json
{
  "proxy": {
    "enabled": false,
    "provider": "brightdata",
    "country": "",
    "sticky": true,
    "sticky_ttl_minutes": 10
  },
  "categories": [
    "gaming", "tech", "beauty", "fashion", "fitness",
    "food", "travel", "music", "education", "comedy",
    "lifestyle", "cooking", "diy", "art", "finance",
    "health", "entertainment"
  ],
  "locations": [
    "India", "Mumbai", "Delhi", "Bangalore", "Hyderabad",
    "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur"
  ],
  "max_videos_to_scrape": 6,
  "headless": false,
  "results_per_search": 20,
  "search_delay": [3, 7],
  "scrape_delay": [2, 5],
  "rate_limit_wait": 60,
  "max_retries": 3
}
```

## 过滤规则

该工具会自动过滤以下类型的频道：

- ❌ 无法访问或已被终止的频道
- ❌ 订阅者数量少于500的频道（可配置）
- ❌ 不存在的频道URL
- ❌ 已经被抓取过的频道（避免重复抓取）
- ❌ 遭遇速率限制的请求（自动重试）

## 反检测机制

该工具采用多种反检测技术：

- **浏览器指纹识别**——轮换浏览器配置（视口、用户代理、时区、WebGL等）
- **隐蔽JavaScript**——隐藏`navigator.webdriver`对象，伪造插件/语言/硬件信息，添加随机噪声到canvas元素，模拟真实的浏览器行为
- **模拟人类行为**——设置随机延迟、鼠标移动和滚动模式
- **网络随机化**——在请求之间随机调整发送时间
- **拦截检测脚本**——阻止常见的检测机制

## 常见问题解决方法

### 未发现任何频道

- 尝试不同的地理位置或频道类别组合
- 检查Google搜索结果是否包含验证码页面
- 使用`--headless false`参数以无界面模式运行工具进行调试

### 速率限制

- 降低抓取速度（通过配置文件调整延迟时间）
- 在非高峰时段执行抓取任务
- **使用住宅代理**（详见下文）

### 浏览器崩溃

- 系统会每抓取50个频道后自动重启浏览器
- 中断的抓取任务可以自动恢复——队列文件会记录抓取进度

---

## 🌐 住宅代理支持

### 为何使用住宅代理？

在没有住宅代理的情况下大规模运行抓取工具会导致IP地址被快速封禁。以下是使用代理的必要性：

| 优势 | 说明 |
|-----------|-------------|
| **避免IP封禁** | 住宅代理的IP地址看起来像真实用户的IP，YouTube不太可能将其识别为机器人 |
| **自动IP轮换** | 每次请求都会使用新的IP地址，避免同一IP地址被多次限制 |
| **地域定向** | 将流量路由到目标地区，确保抓取内容符合目标受众的语言设置 |
| **保持会话稳定性** | 可配置会话持续时间（例如10分钟），确保浏览会话的连续性 |
| **更高的成功率** | 使用住宅代理的抓取成功率可超过95%，而使用数据中心代理的成功率约为30% |
| **长时间抓取** | 可连续抓取数千个频道，而不会中断 |
| **并发抓取** | 可同时使用多个浏览器实例在多个IP地址上执行抓取任务 |

### 推荐的代理服务提供商

我们与多家领先的住宅代理服务提供商建立了合作关系。使用以下链接可以帮助我们持续改进该工具：

| 服务提供商 | 适用场景 | 注册链接 |
|----------|----------|---------|
| **Bright Data** | 全球最大的代理网络，拥有7200万以上IP地址，企业级服务 | 👉 [**注册Bright Data**](https://get.brightdata.com/o1kpd2da8iv4) |
| **IProyal** | 按需付费，支持195多个国家，无流量使用期限限制 | 👉 [**注册IProyal**](https://iproyal.com/?r=ScrapeClaw) |
| **Storm Proxies** | 快速且可靠的代理服务，提供易于使用的API，价格合理 | 👉 [**注册Storm Proxies**](https://stormproxies.com/clients/aff/go/scrapeclaw) |
| **NetNut** | 提供ISP级别的代理服务，拥有5200万以上IP地址，直接连接网络 | 👉 [**注册NetNut**](https://netnut.io?ref=mwrlzwv) |

### 设置步骤

#### 1. 获取代理凭证

在任一上述提供商处注册，然后获取以下信息：
- **用户名**（从提供商的控制面板获取）
- **密码**（从提供商的控制面板获取）
- **主机地址**和**端口**由提供商预先配置（或自行设置）

#### 2. 通过环境变量进行配置

```bash
export PROXY_ENABLED=true
export PROXY_PROVIDER=brightdata    # brightdata | iproyal | stormproxies | netnut | custom
export PROXY_USERNAME=your_user
export PROXY_PASSWORD=your_pass
export PROXY_COUNTRY=us             # optional: two-letter country code
export PROXY_STICKY=true            # optional: keep same IP per session
```

#### 3. 各服务提供商的默认主机/端口设置

当设置`provider`参数时，系统会自动配置相应的主机和端口：

| 服务提供商 | 主机地址 | 端口 |
|----------|------|------|
| Bright Data | `brd.superproxy.io` | `22225` |
| IProyal | `proxy.iproyal.com` | `12321` |
| Storm Proxies | `rotating.stormproxies.com` | `9999` |
| NetNut | `gw-resi.netnut.io` | `5959` |

如果您的代理服务提供商使用其他配置，请通过`PROXY_HOST`/`PROXY_PORT`环境变量进行自定义设置。

#### 4. 自定义代理服务提供商

对于其他代理服务，将`provider`参数设置为`custom`，并手动输入主机地址和端口：

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

### 使用代理运行工具

配置完成后，工具会自动使用代理进行抓取——无需额外设置：

```bash
# Discover and scrape as usual — proxy is applied automatically
python scripts/youtube_orchestrator.py --config resources/scraper_config_ind.json

# The log will confirm proxy is active:
# INFO - Proxy enabled: <ProxyManager provider=brightdata enabled host=brd.superproxy.io:22225>
# INFO - Browser using proxy: brightdata → brd.superproxy.io:22225
```

### 程序化使用代理管理器

```python
from proxy_manager import ProxyManager

# From config (auto-reads config from resources/)
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

1. **启用会话稳定性**——YouTube要求在浏览会话期间使用相同的IP地址。请设置`"sticky": true`。
2. **选择正确的目标地区**——设置`"country": "us"`（或目标地区），以确保YouTube返回符合当地语言设置的内容。
3. **结合多种反检测机制**——该工具已具备指纹识别、隐蔽脚本和模拟人类行为的功能；代理作为最后的防护层。
4. **在批量抓取之间轮换会话**——在处理大量频道时调用`pm.rotate_session()`函数以获取新的IP地址。
5. **设置适当的延迟**——即使使用了代理，也要遵守配置文件中的`scrape_delay`设置（默认为2-5秒），以避免被检测到异常行为。
6. **监控代理服务提供商的监控面板**——所有提供商都会提供带宽使用情况和抓取成功率的数据。

## 注意事项

- **无需登录**——仅抓取公开可见的内容
- **进度记录与恢复**——队列文件会记录抓取进度，中断的抓取任务可以自动恢复
- **速率限制**——遇到速率限制时等待60秒，连续失败时采用指数级重试策略
- **系统具有高稳定性**——浏览器会自动重启，失败频道会自动重试，收到SIGINT/SIGTERM信号时会优雅地关闭程序
- **地域配置**——提供覆盖全球200多个城市的预设配置选项