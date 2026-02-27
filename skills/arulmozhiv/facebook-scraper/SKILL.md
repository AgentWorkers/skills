# Facebook页面与群组抓取工具

> 该工具属于**[ScrapeClaw](https://www.scrapeclaw.cc/)**系列——一套专为Instagram、YouTube、X/Twitter和Facebook设计的、可投入生产的社交媒体抓取工具，基于Python和Playwright开发，无需使用API密钥。

这是一个基于浏览器的Facebook页面与群组发现及抓取工具。

```yaml
---
name: facebook-scraper
description: Discover and scrape Facebook pages and public groups from your browser.
emoji: 📘
version: 1.0.0
author: influenza
tags:
  - facebook
  - scraping
  - social-media
  - page-discovery
  - group-discovery
  - business-pages
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

该工具提供了两阶段的Facebook抓取流程：
1. **页面/群组发现**
2. **浏览器抓取**

## 主要功能：
- 🔍  根据地理位置和类别发现Facebook页面和群组
- 🌐  全模拟浏览器环境，确保抓取数据的准确性
- 🛡️  通过模拟人类行为和使用隐蔽脚本来规避限制
- 📊  获取页面/群组信息、统计数据、图片及互动数据
- 💾  支持将数据导出为JSON或CSV格式，并附带下载的缩略图
- 🔄  可恢复中断的抓取会话
- ⚡  自动跳过私人群组、点赞数过低的页面或空账户
- 📂  通过`--type`参数支持抓取页面、群组和公开个人资料

#### 获取Google API凭证（可选）

1. 访问[Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用“自定义搜索API”
4. 生成API密钥
5. 访问[Programmable Search Engine](https://programmablesearchengine.google.com/)，设置搜索目标为`facebook.com`
6. 复制搜索引擎ID

## 使用方法

### 代理工具接口

对于OpenClaw代理的集成，该工具会输出JSON格式的数据：

```bash
# Discover Facebook pages (returns JSON)
discover --location "Miami" --category "restaurant" --type page --output json

# Discover Facebook groups (returns JSON)
discover --location "New York" --category "fitness" --type group --output json

# Scrape single page (returns JSON)
scrape --page-name examplebusiness --output json

# Scrape single group (returns JSON)
scrape --page-name examplegroup --type group --output json
```

## 输出数据格式

### 页面/群组数据结构

```json
{
  "page_name": "example_business",
  "display_name": "Example Business",
  "entity_type": "page",
  "category": "Restaurant",
  "subcategory": "Italian Restaurant",
  "about": "Family-owned Italian restaurant since 1985",
  "followers": 45000,
  "page_likes": 42000,
  "location": "Miami, FL",
  "address": "123 Main St, Miami, FL 33101",
  "phone": "+1-555-0123",
  "email": "info@example.com",
  "website": "https://example.com",
  "hours": "Mon-Sat 11AM-10PM",
  "is_verified": false,
  "page_tier": "mid",
  "profile_pic_local": "thumbnails/example_business/profile_abc123.jpg",
  "cover_photo_local": "thumbnails/example_business/cover_def456.jpg",
  "recent_posts": [
    {"post_url": "https://facebook.com/example_business/posts/123", "reactions": 320, "comments": 45, "shares": 12}
  ],
  "scrape_timestamp": "2026-02-20T14:30:00"
}
```

### 群组数据结构

```json
{
  "page_name": "example_group",
  "display_name": "Miami Fitness Community",
  "entity_type": "group",
  "about": "A community for fitness enthusiasts in Miami",
  "members": 15000,
  "privacy": "Public",
  "posts_per_day": 25,
  "location": "Miami",
  "page_tier": "mid",
  "profile_pic_local": "thumbnails/example_group/profile_abc123.jpg",
  "cover_photo_local": "thumbnails/example_group/cover_def456.jpg",
  "scrape_timestamp": "2026-02-20T14:30:00"
}
```

### 页面分类

| 分类 | 点赞数/成员数范围 |
|-------|---------------------|
| nano  | < 1,000             |
| micro | 1,000 - 10,000      |
| mid   | 10,000 - 100,000    |
| macro | 100,000 - 1,000,000    |
| mega  | > 1,000,000         |

### 文件输出路径：
- **队列文件**：`data/queue/{location}_{category}_{type}_{timestamp}.json`
- **抓取数据**：`data/output/{page_name}.json`
- **缩略图**：`thumbnails/{page_name}/profile_*.jpg`, `thumbnails/{page_name}/cover_*.jpg`
- **导出文件**：`data/export_{timestamp}.json`, `data/export_{timestamp}.csv`

## 配置

编辑`config/scraper_config.json`文件进行配置：

```json
{
  "google_search": {
    "enabled": true,
    "api_key": "",
    "search_engine_id": "",
    "queries_per_location": 3
  },
  "scraper": {
    "headless": false,
    "min_likes": 1000,
    "download_thumbnails": true,
    "max_thumbnails": 6
  },
  "cities": ["New York", "Los Angeles", "Miami", "Chicago"],
  "categories": ["restaurant", "retail", "fitness", "real-estate", "healthcare", "beauty"]
}
```

## 过滤规则：
- ❌ 私人群组
- ❌ 点赞数少于1,000的页面（可配置）
- ❌ 已禁用或已删除的页面/群组
- ❌ 不存在的页面/群组
- ❌ 已经抓取过的内容（避免重复）

## 故障排除：
- **登录问题**：确保凭证正确；处理提示的验证码；遇到速率限制时等待脚本自动重试
- **未发现页面**：检查Google API密钥和配额；确认搜索引擎ID配置正确
- **速率限制**：降低抓取速度；使用多个Facebook账户；选择非高峰时段抓取；**使用住宅代理**（详见下文）

---

## 🌐 住宅代理支持

### 为何使用住宅代理？

在没有住宅代理的情况下大规模运行抓取工具会导致IP被快速封禁。以下是使用代理的必要性：
- **避免IP封禁**：住宅代理的IP地址看起来像真实用户的IP，Facebook更难识别为机器人。
- **自动IP轮换**：每次请求都会使用新的IP地址，避免同一IP地址频繁被封禁。
- **地理定位**：将流量导向特定国家/城市，确保抓取内容符合目标受众的语言设置。
- **保持会话稳定性**：在指定时间内（例如10分钟）使用同一IP地址，维持Facebook登录会话。
- **更高的成功率**：使用住宅代理的抓取成功率可达到95%以上，而数据中心代理的成功率约为30%。
- **长时间抓取**：能够连续抓取数千个页面/群组。
- **并发抓取**：允许在多个IP地址上同时运行多个浏览器实例。

### 推荐的代理服务提供商：
我们与多家领先的住宅代理服务提供商有合作关系。使用这些链接有助于持续改进该工具：
| 提供商 | 适用场景 | 注册链接 |
|----------|----------|---------|
| **Bright Data** | 全球最大的住宅代理网络，7200万IP地址，企业级服务 | 👉 [**注册Bright Data**](https://get.brightdata.com/o1kpd2da8iv4) |
| **IProyal** | 高端住宅代理服务，按需付费，支持195个国家 | 👉 [**注册IProyal**](https://iproyal.com/?r=ScrapeClaw) |
| **Storm Proxies** | 快速可靠的住宅代理服务，提供易于使用的API | 👉 [**注册Storm Proxies**](https://stormproxies.com/clients/aff/go/scrapeclaw) |
| **NetNut** | 优质住宅代理服务，5200万IP地址，直接连接 | 👉 [**注册NetNut**](https://netnut.io?ref=mwrlzwv) |

### 设置步骤：
1. **获取代理凭证**：在上述提供商中注册，获取用户名、密码以及主机地址和端口信息。
2. **通过环境变量进行配置**：将相关配置信息添加到环境变量中。
3. **特定提供商的默认配置**：根据提供商设置相应的主机地址和端口。
4. **自定义代理服务**：对于其他代理服务，将提供商设置为“custom”，并手动输入主机地址和端口。

### 使用代理进行抓取：
配置完成后，工具会自动使用代理进行抓取，无需额外设置。

### 长时间抓取的最佳实践：
- **启用会话保持功能**：设置`"sticky": true`以确保登录会话的稳定性。
- **选择正确的目标国家**：设置`"country": "us"`（或其他目标地区）以获取正确的语言内容。
- **结合反检测机制**：该工具已具备IP指纹识别、隐蔽脚本和模拟人类行为的功能；代理作为额外的安全层。
- **在多个账户间轮换会话**：切换Facebook账户时调用`pm.rotate_session()`以获取新IP。
- **设置延迟**：即使使用代理，也要遵守配置中的`delay_between_profiles`（默认5-10秒），避免触发Facebook的检测机制。
- **监控代理使用情况**：所有代理服务提供商（Bright Data、IProyal、Storm Proxies、NetNut）都提供带宽使用情况和成功率监控界面。