# Instagram 个人资料抓取工具

这是一个基于浏览器的 Instagram 个人资料发现和抓取工具。

> 该工具属于 **[ScrapeClaw](https://www.scrapeclaw.cc/)** 系列——这是一套专为 Instagram、YouTube、X/Twitter 和 Facebook 设计的、可用于生产环境的社交媒体抓取工具，完全基于 Python 和 Playwright 开发，无需使用 API 密钥。

```yaml
---
name: instagram-scraper
description: Discover and scrape Instagram profiles from your browser.
emoji: 📸
version: 1.0.3
author: influenza
tags:
  - instagram
  - scraping
  - social-media
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

该工具提供了两阶段的 Instagram 抓取流程：

1. **个人资料发现**  
2. **浏览器抓取**  

## 主要功能

- 🔍  - 根据地理位置和类别发现 Instagram 个人资料  
- 🌐  - 全面模拟浏览器行为，确保抓取数据的准确性  
- 🛡️  - 通过浏览器指纹识别技术模拟人类行为，并使用隐蔽脚本  
- 📊  - 获取个人资料信息、统计数据、图片以及互动数据  
- 💾  - 可将数据导出为 JSON 或 CSV 格式，并附上下载的缩略图  
- 🔄  - 恢复中断的抓取会话  
- ⚡  - 自动跳过私密账户、粉丝数过少的账户或空账户  
- 🌍  - 内置住宅代理支持，支持 4 家代理服务提供商  

#### 获取 Google API 凭据（可选）

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)  
2. 创建新项目或选择现有项目  
3. 启用“自定义搜索 API”  
4. 创建 API 凭据（API Key）  
5. 访问 [Programmable Search Engine](https://programmablesearchengine.google.com/)  
6. 创建一个以 `instagram.com` 为搜索目标的搜索引擎  
7. 复制搜索引擎 ID  

## 使用方法

### 代理工具接口

对于 OpenClaw 代理的集成，该工具会输出 JSON 数据：

```bash
# Discover profiles (returns JSON)
discover --location "Miami" --category "fitness" --output json

# Scrape single profile (returns JSON)
scrape --username influencer123 --output json
```

## 输出数据

### 个人资料数据结构

```json
{
  "username": "example_user",
  "full_name": "Example User",
  "bio": "Fashion blogger | NYC",
  "followers": 125000,
  "following": 1500,
  "posts_count": 450,
  "is_verified": false,
  "is_private": false,
  "influencer_tier": "mid",
  "category": "fashion",
  "location": "New York",
  "profile_pic_local": "thumbnails/example_user/profile_abc123.jpg",
  "content_thumbnails": [
    "thumbnails/example_user/content_1_def456.jpg",
    "thumbnails/example_user/content_2_ghi789.jpg"
  ],
  "post_engagement": [
    {"post_url": "https://instagram.com/p/ABC123/", "likes": 5420, "comments": 89}
  ],
  "scrape_timestamp": "2025-02-09T14:30:00"
}
```

### 博主等级划分

| 等级 | 粉丝数量范围 |
|-------|-------------------|
| nano  | < 1,000           |
| micro | 1,000 - 10,000    |
| mid   | 10,000 - 100,000  |
| macro | 100,000 - 1,000,000  |
| mega  | > 1,000,000       |

### 文件输出路径

- **队列文件**：`data/queue/{location}_{category}_{timestamp}.json`  
- **抓取数据**：`data/output/{username}.json`  
- **缩略图**：`thumbnails/{username}/profile_*.jpg`, `thumbnails/{username}/content_*.jpg`  
- **导出文件**：`data/export_{timestamp}.json`, `data/export_{timestamp}.csv`  

## 配置

编辑 `config/scraper_config.json` 文件以进行配置：

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
    "min_followers": 1000,
    "download_thumbnails": true,
    "max_thumbnails": 6
  },
  "cities": ["New York", "Los Angeles", "Miami", "Chicago"],
  "categories": ["fashion", "beauty", "fitness", "food", "travel", "tech"]
}
```

## 应用过滤规则

该工具会自动过滤以下类型的账户：

- ❌ 私密账户  
- ❌ 粉丝数少于 1,000 的账户（可配置）  
- ❌ 没有发布内容的账户  
- ❌ 不存在或已被删除的账户  
- ❌ 已经被抓取过的账户（避免重复抓取）  

## 故障排除

### 登录问题

- 确保使用正确的凭据  
- 在提示时处理验证码  
- 如果遇到速率限制，请稍后重试  

### 未发现个人资料

- 检查 Google API 密钥和配额  
- 确认已为 `instagram.com` 配置正确的搜索引擎 ID  
- 尝试不同的地理位置或类别组合  

### 速率限制

- 降低抓取速度（通过配置增加延迟）  
- 在非高峰时段运行抓取任务  
- **使用住宅代理**（详见下文）  

---

## 🌐 住宅代理支持

### 为什么使用住宅代理？

在没有使用住宅代理的情况下大规模运行抓取工具时，您的 IP 地址很可能会被 Instagram 封禁。以下是使用代理的几个关键原因：

| 优势 | 说明 |
|-----------|-------------|
| **避免 IP 被封禁** | 住宅代理的 IP 地址看起来像真实用户的地址，而非数据中心的机器人地址，因此更不容易被 Instagram 标记为可疑。 |
| **自动 IP 轮换** | 每次请求都会使用一个新的 IP 地址，从而避免同一个 IP 地址被多次使用导致速率限制。 |
| **地理定位** | 将流量路由到特定国家/城市，使抓取的内容符合目标受众的语言环境。 |
| **保持会话连续性** | 可以在指定时间内（例如 10 分钟）使用相同的 IP 地址，确保浏览会话的连续性。 |
| **更高的成功率** | 使用住宅代理的抓取成功率可达到 95% 以上，而使用数据中心代理的成功率约为 30%。 |
| **长时间抓取** | 可以连续数小时或数天无间断地抓取大量个人资料。 |
| **并发抓取** | 可以同时使用多个浏览器实例在不同的 IP 地址上进行抓取。 |

### 推荐的代理服务提供商

我们与多家领先的住宅代理服务提供商有合作关系。使用以下链接可以帮助我们持续改进该工具：

| 服务提供商 | 适用场景 | 注册链接 |
|----------|----------|---------|
| **Bright Data** | 全球最大的代理网络，拥有 7,200 万多个 IP 地址，企业级服务 | 👉 [**注册 Bright Data**](https://get.brightdata.com/o1kpd2da8iv4) |
| **IProyal** | 按需付费，支持 195 个国家，无流量使用期限限制 | 👉 [**注册 IProyal**](https://iproyal.com/?r=ScrapeClaw) |
| **Storm Proxies** | 快速且可靠的代理服务，提供易于使用的 API，价格合理 | 👉 [**注册 Storm Proxies**](https://stormproxies.com/clients/aff/go/scrapeclaw) |
| **NetNut** | 提供 ISP 级别的代理服务，拥有 5,200 万多个 IP 地址，直接连接 | 👉 [**注册 NetNut**](https://netnut.io?ref=mwrlzwv) |  

### 设置步骤

#### 1. 获取代理凭据

在以上任一提供商处注册，然后获取以下信息：  
- **用户名**（来自提供商的控制面板）  
- **密码**（来自提供商的控制面板）  
- **主机地址** 和 **端口号**（由提供商预先配置，或自行设置）  

#### 2. 通过环境变量配置代理

```bash
export PROXY_ENABLED=true
export PROXY_PROVIDER=brightdata    # brightdata | iproyal | stormproxies | netnut | custom
export PROXY_USERNAME=your_user
export PROXY_PASSWORD=your_pass
export PROXY_COUNTRY=us             # optional: two-letter country code
export PROXY_STICKY=true            # optional: keep same IP per session
```

#### 3. 各服务提供商的默认主机/端口号

当您设置 `provider` 时，这些值会自动配置：

| 服务提供商 | 主机地址 | 端口号 |
|----------|------|------|
| Bright Data | `brd.superproxy.io` | `22225` |
| IProyal | `proxy.iproyal.com` | `12321` |
| Storm Proxies | `rotating.stormproxies.com` | `9999` |
| NetNut | `gw-resi.netnut.io` | `5959` |

如果您的计划使用其他代理服务，请通过 `PROXY_HOST` / `PROXY_PORT` 环境变量进行自定义配置。  

#### 4. 自定义代理服务提供商

对于其他代理服务，请将 `provider` 设置为 `custom`，并手动输入主机地址和端口号：

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
python main.py discover --location "Miami" --category "fitness"
python main.py scrape --username influencer123

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

1. **启用会话连续性** — Instagram 要求在浏览会话期间使用相同的 IP 地址，请将 `"sticky": true` 设置为 `true`。  
2. **选择正确的目标国家** — 设置 `"country": "us"`（或目标地区），以确保 Instagram 显示正确的语言内容。  
3. **结合其他反检测措施** — 该工具已具备浏览器指纹识别、隐蔽脚本和人类行为模拟功能；代理是最后的防护层。  
4. **在批量抓取之间轮换会话** — 在处理大量个人资料时，调用 `pm.rotate_session()` 以获取新的 IP 地址。  
5. **设置延迟** — 即使使用代理，也要遵守配置中的 `delay_between_profiles` 设置，以避免被 Instagram 视为恶意行为。  
6. **监控代理使用情况** | 所有代理服务提供商都提供带宽使用情况和成功率统计界面。