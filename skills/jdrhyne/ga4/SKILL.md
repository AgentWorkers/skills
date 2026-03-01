---
name: ga4
description: 通过 Analytics Data API 查询 Google Analytics 4 (GA4) 数据。当您需要获取网站分析数据（如热门页面、流量来源、用户数量、会话数、转化率或任何 GA4 指标/维度）时，可以使用此方法。支持自定义日期范围和过滤条件。
homepage: https://developers.google.com/analytics
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires":
          {
            "anyBins": ["python3", "python"],
            "env": ["GA4_PROPERTY_ID", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "GOOGLE_REFRESH_TOKEN"],
          },
      },
  }
---
# GA4 - Google Analytics 4 数据 API

通过此 API 可以查询 Google Analytics 4（GA4）中的各种属性数据，包括页面浏览量、会话数、用户信息、流量来源、转化事件等。

## 设置（仅需一次）

1. 启用 Google Analytics Data API：https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com
2. 创建 OAuth 凭据或使用现有的 Google Cloud 项目
3. 设置环境变量：
   - `GA4_PROPERTY_ID`：您的 GA4 属性 ID（数字格式，例如 "123456789")
   - `GOOGLE_CLIENT_ID`：OAuth 客户端 ID
   - `GOOGLE_CLIENT_SECRET`：OAuth 客户端密钥
   - `GOOGLE_REFRESH_TOKEN`：OAuth 刷新令牌（在初次认证后生成）

## 安全限制

- 该功能仅用于连接 Google Analytics Data API 的相关端点。
- 该功能仅用于读取数据，不会写入或修改您的 GA4 属性。
- 该功能不会存储或传输凭证，数据仅在当前会话期间有效。
- 使用此功能需要将 OAuth 凭据（客户端 ID、客户端密钥、刷新令牌）设置为环境变量。

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

常见指标：`screenPageViews`（页面浏览量）、`sessions`（会话数）、`totalUsers`（总用户数）、`newUsers`（新用户数）、`activeUsers`（活跃用户数）、`bounceRate`（跳出率）、`averageSessionDuration`（平均会话时长）、`conversions`（转化事件数）、`eventCount`（事件总数）

## 可用的维度

常见维度：`pagePath`（页面路径）、`pageTitle`（页面标题）、`landingPage`（着陆页）、`sessionSource`（流量来源）、`sessionMedium`（会话媒介）、`sessionCampaignName`（会话活动名称）、`country`（国家/地区）、`city`（城市）、`deviceCategory`（设备类型）、`browser`（浏览器类型）、`date`（日期）

## 输出格式

默认格式：表格格式
- 使用 `--json` 选项可获取 JSON 格式输出
- 使用 `--csv` 选项可获取 CSV 格式输出