---
name: ga4
description: 通过 Analytics Data API 查询 Google Analytics 4 (GA4) 的数据。当您需要获取网站分析信息（如热门页面、流量来源、用户数量、会话数、转化次数或任何 GA4 指标/维度）时，可以使用此方法。支持自定义日期范围和过滤条件。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"]}}}
---

# GA4 - Google Analytics 4 数据 API

通过 GA4 数据 API 查询各种分析数据，如页面浏览量、会话数、用户信息、流量来源、转化次数等。

## 设置（一次性操作）

1. 启用 Google Analytics Data API：https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com
2. 创建 OAuth 凭据或使用现有的 Google Cloud 项目
3. 设置环境变量：
   - `GA4_PROPERTY_ID` - 你的 GA4 属性 ID（数字格式，例如 "123456789")
   - `GOOGLE_CLIENT_ID` - OAuth 客户端 ID
   - `GOOGLE_CLIENT_SECRET` - OAuth 客户端密钥
   - `GOOGLE_REFRESH_TOKEN` - OAuth 刷新令牌（来自初次身份验证流程）

## 常见查询

### 浏览量最高的页面
```bash
python3 scripts/ga4_query.py --metric screenPageViews --dimension pagePath --limit 30
```

### 含有最多会话和用户的页面
```bash
python3 scripts/ga4_query.py --metrics screenPageViews,sessions,totalUsers --dimension pagePath --limit 20
```

### 流量来源
```bash
python3 scripts/ga4_query.py --metric sessions --dimension sessionSource --limit 20
```

### 着陆页
```bash
python3 scripts/ga4_query.py --metric sessions --dimension landingPage --limit 30
```

### 自定义日期范围
```bash
python3 scripts/ga4_query.py --metric sessions --dimension pagePath --start 2026-01-01 --end 2026-01-15
```

### 按页面路径过滤
```bash
python3 scripts/ga4_query.py --metric screenPageViews --dimension pagePath --filter "pagePath=~/blog/"
```

## 可用的指标

常见指标：`screenPageViews`（页面浏览量）、`sessions`（会话数）、`totalUsers`（总用户数）、`newUsers`（新用户数）、`activeUsers`（活跃用户数）、`bounceRate`（跳出率）、`averageSessionDuration`（平均会话时长）、`conversions`（转化次数）、`eventCount`（事件计数）

## 可用的维度

常见维度：`pagePath`（页面路径）、`pageTitle`（页面标题）、`landingPage`（着陆页）、`sessionSource`（会话来源）、`sessionMedium`（会话媒介）、`sessionCampaignName`（会话活动名称）、`country`（国家）、`city`（城市）、`deviceCategory`（设备类别）、`browser`（浏览器类型）、`date`（日期）

## 输出格式

默认格式：表格格式
使用 `--json` 选项可获取 JSON 格式输出
使用 `--csv` 选项可获取 CSV 格式输出