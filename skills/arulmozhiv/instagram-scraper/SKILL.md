# Instagram个人资料抓取工具

这是一个基于浏览器的Instagram个人资料发现和抓取工具。

> 该工具属于**[ScrapeClaw](https://www.scrapeclaw.cc/)**系列——这是一套专为Instagram、YouTube、X/Twitter和Facebook设计的、可投入生产的社交媒体抓取工具，使用Python和Playwright开发，无需API密钥。

```yaml
---
name: instagram-scraper
description: Discover and scrape Instagram profiles from your browser.
emoji: 📸
version: 1.0.6
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

该工具提供了一个两阶段的Instagram抓取系统：

1. **个人资料发现**
2. **浏览器抓取**

## 特点

- 🔍  - 按地理位置和类别发现Instagram个人资料
- 🌐  - 全浏览器模拟，确保抓取数据的准确性
- 🛡️  - 浏览器指纹识别、模拟人类行为以及使用隐蔽脚本
- 📊  - 个人资料信息、统计数据、图片和互动数据
- 💾  - 可导出JSON/CSV格式的数据，并包含下载的缩略图
- 🔄  - 恢复中断的抓取会话
- ⚡  - 自动跳过私密账户、粉丝数较少的账户或空账户
- 🌍  - 内置住宅代理支持，支持4家代理服务提供商

#### 获取Google API凭证（可选）

1. 访问[Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用“自定义搜索API”
4. 创建API凭证 → API密钥
5. 访问[Programmable Search Engine](https://programmablesearchengine.google.com/)
6. 创建一个以`instagram.com`为搜索目标的搜索引擎
7. 复制搜索引擎ID

## 使用方法

### 代理工具接口

对于OpenClaw代理的集成，该工具提供JSON格式的输出数据：

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

### 影响者等级

| 等级 | 粉丝数量范围 |
|-------|-------------------|
| nano  | < 1,000           |
| micro | 1,000 - 10,000    |
| mid   | 10,000 - 100,000  |
| macro | 100,000 - 1,000,000  |
| mega  | > 1,000,000       |

### 文件输出

- **队列文件**：`data/queue/{location}_{category}_{timestamp}.json`
- **抓取数据**：`data/output/{username}.json`
- **缩略图**：`thumbnails/{username}/profile_*.jpg`, `thumbnails/{username}/content_*.jpg`
- **导出文件**：`data/export_{timestamp}.json`, `data/export_{timestamp}.csv`

## 配置

编辑`config/scraper_config.json`文件：

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

## 应用过滤器

该工具会自动过滤以下类型的账户：

- ❌ 私密账户
- ❌ 粉丝数少于1,000的账户（可配置）
- ❌ 没有帖子的账户
- ❌ 不存在或已被删除的账户
- ❌ 已经被抓取过的账户（避免重复抓取）

## 故障排除

### 登录问题

- 确保凭证正确
- 在提示时处理验证码
- 如果遇到速率限制，请等待，脚本会自动重试

### 未发现个人资料

- 检查Google API密钥和配额
- 确认搜索引擎ID已正确配置为`instagram.com`
- 尝试不同的地理位置/类别组合

### 速率限制

- 降低抓取速度（在配置中增加延迟）
- 在非高峰时段运行
- **使用住宅代理**（见下文）

---

## 🌐 住宅代理支持

### 为什么使用住宅代理？

在没有使用住宅代理的情况下大规模运行抓取工具会导致IP被迅速封禁。以下是使用代理的必要性：

| 优势 | 说明 |
|-----------|-------------|
| **避免IP封禁** | 住宅代理的IP看起来像是真实用户的IP，而不是数据中心的机器人IP，因此Instagram不太可能将其标记为异常。 |
| **自动IP轮换** | 每个请求（或会话）都会使用一个新的IP地址，从而避免同一地址的速率限制问题。 |
| **地理定位** | 将流量路由到特定国家/城市，使抓取的内容符合目标受众的地域设置。 |
| **保持会话稳定性** | 可以在指定时间内（例如10分钟）使用相同的IP地址，这对于维持稳定的浏览会话至关重要。 |
| **更高的成功率** | 与数据中心代理相比，使用住宅代理的抓取成功率可达到95%以上。 |
| **长时间运行** | 可以连续数小时或数天无间断地抓取大量个人资料。 |
| **并发抓取** | 可以同时使用多个浏览器实例在不同的IP地址上运行抓取任务。 |

### 推荐的代理服务提供商

我们与多家领先的住宅代理服务提供商有合作关系。使用这些链接可以支持该工具的持续开发：

| 提供商 | 适用场景 | 注册链接 |
|----------|----------|---------|
| **Bright Data** | 全球最大的代理网络，拥有7200万+个IP地址，企业级服务 | 👉 [**注册Bright Data**](https://get.brightdata.com/o1kpd2da8iv4) |
| **IProyal** | 按需付费，支持195多个国家，无流量过期限制 | 👉 [**注册IProyal**](https://iproyal.com/?r=ScrapeClaw) |
| **Storm Proxies** | 快速且可靠的代理服务，提供易于使用的API接口，价格合理 | 👉 [**注册Storm Proxies**](https://stormproxies.com/clients/aff/go/scrapeclaw) |
| **NetNut** | 提供ISP级别的代理服务，拥有5200万+个IP地址，直接连接 | 👉 [**注册NetNut**](https://netnut.io?ref=mwrlzwv) |

### 设置步骤

#### 1. 获取代理凭证

在上述提供商中注册，然后获取以下信息：
- **用户名**（来自提供商的控制面板）
- **密码**（来自提供商的控制面板）
- **主机地址**和**端口**由提供商预先配置（或自定义）

#### 2. 通过环境变量进行配置

```bash
export PROXY_ENABLED=true
export PROXY_PROVIDER=brightdata    # brightdata | iproyal | stormproxies | netnut | custom
export PROXY_USERNAME=your_user
export PROXY_PASSWORD=your_pass
export PROXY_COUNTRY=us             # optional: two-letter country code
export PROXY_STICKY=true            # optional: keep same IP per session
```

#### 3. 各提供商的默认主机/端口设置

当您设置`provider`名称时，这些值会自动配置：

| 提供商 | 主机地址 | 端口 |
|----------|------|------|
| Bright Data | `brd.superproxy.io` | `22225` |
| IProyal | `proxy.iproyal.com` | `12321` |
| Storm Proxies | `rotating.stormproxies.com` | `9999` |
| NetNut | `gw-resi.netnut.io` | `5959` |

如果您的计划使用其他代理服务，请通过`PROXY_HOST` / `PROXY_PORT`环境变量进行自定义配置。

#### 4. 自定义代理服务

对于其他代理服务，将`provider`设置为`custom`，并手动输入主机地址和端口：

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

配置完成后，工具会自动使用代理进行抓取——无需额外设置：

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

### 长时间运行抓取的最佳实践

1. **使用“sticky”设置** — Instagram要求在浏览会话期间使用相同的IP地址。请将`"sticky": true`设置为True。
2. **选择正确的目标国家** — 设置`"country": "us"`（或您的目标地区），以确保Instagram返回符合预期语言设置的内容。
3. **结合其他反检测措施** — 该工具已经具备指纹识别、隐蔽脚本和模拟人类行为的功能，代理是最后的防护层。
4. **在批量抓取之间轮换会话** — 在处理大量个人资料时，调用`pm.rotate_session()`以获取新的IP地址。
5. **设置延迟** — 即使使用代理，也要遵守配置中的`delay_between_profiles`设置，以避免频繁的请求模式。
6. **监控代理服务提供商的仪表板** | 所有提供商的仪表板都会显示带宽使用情况和抓取成功率。