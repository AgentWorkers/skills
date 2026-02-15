---
name: Scrappa MCP
description: 您可以通过 Model Context Protocol 访问 Scrappa 的 MCP 服务器，以获取来自 Google、YouTube、Amazon、LinkedIn、Trustpilot 等平台的数据，包括航班信息、酒店预订等。
---

# Scrappa MCP 技能

通过 Scrappa 模型上下文协议（MCP）服务器，可以访问 80 多种工具，用于搜索 Google、YouTube、Amazon、LinkedIn、Trustpilot、商业评论、航班、酒店、房地产等信息。

## 设置

### 1. 获取 Scrappa API 密钥

在 [scrappa.co](https://scrappa.co/dashboard/register) 注册一个免费账户，并从控制面板中获取 API 密钥。

### 2. 在 Clawdbot 中配置

将 Scrappa 添加到您的 mcporter 配置中：

```bash
mcporter config add scrappa --url "https://scrappa.co/mcp" --headers "X-API-KEY=YOUR_API_KEY"
```

或者手动编辑 `~/clawd/config/mcporter.json`：

```json
{
  "mcpServers": {
    "scrappa": {
      "baseUrl": "https://scrappa.co/mcp",
      "headers": {
        "X-API-KEY": "your_api_key_here"
      }
    }
  }
}
```

### 3. 重启 Clawdbot

```bash
clawdbot gateway restart
```

## 可用的所有工具（80 多种）

### Google 搜索与翻译

| 工具 | 描述 |
|------|-------------|
| `search` | 使用高级过滤器抓取 Google 搜索结果 |
| `google-search-light` | 轻量级的 Google 网页搜索 |
| `google-search-autocomplete` | Google 搜索建议 |
| `google-translate-api` | 在不同语言之间翻译文本 |
| `google-images` | 搜索 Google 图片 |
| `google-videos` | 搜索 Google 视频 |
| `google-news` | 搜索 Google 新闻文章 |
| `google-jobs` | 搜索 Google 上索引的职位 |
| `brave-search` | 注重隐私的 Brave 网页搜索 |

### YouTube

| 工具 | 描述 |
|------|-------------|
| `youtube-external-search` | 搜索视频 |
| `youtube-external-video` | 获取视频的完整信息 |
| `youtube-external-info` | 基本视频元数据 |
| `youtube-external-channel` | 频道信息和统计 |
| `youtube-external-comments` | 获取视频评论 |
| `youtube-external-related` | 获取相关视频 |
| `youtube-external-chapters` | 提取视频章节 |
| `youtube-external-trending` | 按类别搜索热门视频 |
| `youtube-external-suggestions` | 搜索建议 |
| `youtube-external-channel-videos` | 频道上传的视频 |
| `youtube-external-channel-playlists` | 频道播放列表 |
| `youtube-external-community` | 频道社区帖子 |
| `youtube-external-playlist` | 获取播放列表中的视频 |
| `youtube-external-health` | 检查 API 状态 |
| `youtube-external-proxies` | YouTube 代理 API |
| `youtube-external-locales` | YouTube 地区信息 API |

### Amazon

| 工具 | 描述 |
|------|-------------|
| `amazon-search` | 在 22 个市场平台上搜索产品 |
| `amazon-product` | 根据 ASIN 获取产品详细信息 |

### LinkedIn

| 工具 | 描述 |
|------|-------------|
| `linkedin-profile` | 获取 LinkedIn 个人资料信息 |
| `linkedin-company` | 获取公司页面信息 |
| `linkedin-post` | 获取帖子详细信息 |
| `linkedin-search` | 搜索 LinkedIn 个人资料 |

### Trustpilot

| 工具 | 描述 |
|------|-------------|
| `trustpilot-categories` | 列出商业类别 |
| `trustpilot-businesses` | 搜索企业 |
| `trustpilot-countries` | 列出支持的国家 |
| `trustpilot-company-search` | 搜索公司 |
| `trustpilot-company-details` | 获取公司信息 |
| `trustpilot-company-reviews` | 获取公司评论 |

### Kununu（德国评论）

| 工具 | 描述 |
|------|-------------|
| `kununu-search` | 在 Kununu 上搜索公司 |
| `kununu-reviews` | 获取公司评论 |
| `kununu-profiles` | 获取公司资料 |
| `kununu-industries` | 列出可用行业 |
| `kununu-company-details` | 公司详细信息 |

### TrustedShops（欧洲评论）

| 工具 | 描述 |
|------|-------------|
| `trustedshops-markets` | 获取所有可用市场 |
| `trustedshops-search` | 搜索店铺 |
| `trustedshops-reviews` | 获取店铺评论 |
| `trustedshops-shop` | 获取店铺详细信息 |

### Google 地图与地点

| 工具 | 描述 |
|------|-------------|
| `simple-search` | 根据查询快速搜索地点 |
| `advanced-search` | 使用过滤器进行搜索并分页 |
| `autocomplete` | 输入时获取地点建议 |
| `google-reviews` | 获取 Google 地点评论 |
| `google-single-review` | 获取单条评论详细信息 |
| `google-business-details` | 从地图中获取完整企业信息 |
| `google-maps-photos` | 从地点下载照片 |
| `google-maps-directions` | 获取地点间的路线信息 |

### Google 航班

| 工具 | 描述 |
|------|-------------|
| `google-flights-one-way` | 搜索单程航班 |
| `google-flights-round-trip` | 搜索往返航班 |
| `google-flights-date-range` | 查找最便宜的飞行日期 |
| `google-flights-airlines` | 获取支持的航空公司（免费） |
| `google-flights-airports` | 获取支持的机场（免费） |
| `google-flights-booking-details` | 获取航班预订信息 |

### Google 酒店

| 工具 | 描述 |
|------|-------------|
| `google-hotels-search` | 根据位置搜索酒店 |
| `google-hotels-autocomplete` | 酒店位置自动完成 |

### ImmobilienScout24（德国房地产）

| 工具 | 描述 |
|------|-------------|
| `immobilienscout24-search` | 搜索房产列表 |
| `immobilienscout24-property` | 获取房产详细信息 |
| `immobilienscout24-locations` | 地点自动完成 |
| `immobilienscout24-price-insights` | 每平方米的平均价格 |

### Vinted（二手交易平台）

| 工具 | 描述 |
|------|-------------|
| `vinted-search` | 在 Vinted 上搜索商品 |
| `vinted-filters` | 获取可用过滤器 |
| `vinted-suggestions` | 搜索建议 |
| `vinted-item-details` | 获取商品信息 |
| `vinted-item-shipping` | 获取运输信息 |
| `vinted-similar-items` | 获取相似商品 |
| `vinted-user-profile` | 获取用户资料 |
| `vinted-user-items` | 获取用户列出的商品 |
| `vinted-categories` | 获取所有商品类别 |

### Indeed（求职）

| 工具 | 描述 |
|------|-------------|
| `indeed-jobs` | 在 Indeed 上搜索职位 |

## 使用示例

### Google 搜索
```
Search for "best coffee shops in New York"
```

### YouTube
```
Get details for video: dQw4w9WgXcQ
Search for "latest AI news 2024"
```

### 翻译
```
Translate "Hello world" from English to Spanish
Translate "Good morning" from English to German
```

### Amazon
```
Search for "wireless headphones" on Amazon US
Get product details for B09V3KXJPB
```

### LinkedIn
```
Get profile: https://www.linkedin.com/in/someone
Search for "software engineer" in San Francisco
```

### Trustpilot
```
Search for company "bestbuy"
Get reviews for amazon.com
```

### Google 地图
```
Search for "coffee shops" near "Times Square"
Get directions from "Central Park" to "Brooklyn Bridge"
```

### 航班
```
Search one-way flights from JFK to LHR on 2025-03-15
Find cheapest dates to fly from NYC to Paris in April
```

### 酒店
```
Search hotels in Paris for check-in 2025-04-01, check-out 2025-04-05
```

### 房地产（德国）
```
Search apartments for rent in Berlin, max €1500
Get property details for listing ID 123456
```

### Vinted
```
Search for "Nike shoes" on Vinted France
Get item details for item ID 12345
```

## 注意事项

- 需要从 [scrappa.co](https://scrappa.co) 获取 API 密钥 |
- 使用频率受 Scrappa 计划的限制 |
- 一些工具需要特定的市场/国家参数 |
- Google 搜索结果可能存在缓存延迟 |
- 航班/酒店搜索支持多种过滤器和排序选项

## 链接

- [Scrappa 控制面板](https://scrappa.co/dashboard)
- [Scrappa 文档](https://scrappa.co/docs)
- [MCP 集成指南](https://scrappa.co/docs/mcp-integration)
- [GitHub 仓库](https://github.com/Scrappa-co/scrappa-skill)