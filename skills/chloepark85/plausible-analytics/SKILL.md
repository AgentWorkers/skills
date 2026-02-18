---
name: plausible-analytics
description: 查询并分析来自 Plausible Analytics 的网站分析数据。当您需要查看实时访客数量、获取特定时间段的页面浏览量和访客统计数据、分析流量来源或热门页面、检查地理位置分布，或者为使用 Plausible Analytics 追踪的网站生成分析报告和洞察时，可以使用该功能。
metadata:
  openclaw:
    requires:
      env:
        - PLAUSIBLE_API_KEY
      bins:
        - node
    primaryEnv: PLAUSIBLE_API_KEY
---
# Plausible Analytics

## 概述

Plausible Analytics 提供了一种从其 API 中检索和分析网站分析数据的功能。该服务支持实时访客追踪、历史统计数据、流量来源分析，以及按页面、来源或国家进行的详细数据细分。

## 快速入门

所有脚本都需要 `PLAUSIBLE_API_KEY` 环境变量。站点 ID 可以通过 `PLAUSIBLE_SITE_ID` 环境变量提供，或者作为脚本参数传递。

```bash
# Set API key
export PLAUSIBLE_API_KEY="your-api-key"

# Quick example: Get today's stats
node scripts/stats.mjs example.com --period day
```

## 实时访客

查看当前有多少人正在访问您的网站：

```bash
node scripts/realtime.mjs <site-id>
```

示例输出：
```json
{
  "visitors": 42
}
```

## 统计数据

获取指定时间段的页面浏览量、访客数量、跳出率和访问时长：

```bash
node scripts/stats.mjs <site-id> [--period day|7d|30d|month|6mo|12mo] [--date YYYY-MM-DD]
```

参数：
- `period` - 要查询的时间段（默认：`day`）
- `date` - 该时间段内的具体日期（默认：今天）

示例：
```bash
# Get today's stats
node scripts/stats.mjs example.com

# Get last 7 days
node scripts/stats.mjs example.com --period 7d

# Get stats for a specific month
node scripts/stats.mjs example.com --period month --date 2026-02-01
```

示例输出：
```json
{
  "results": {
    "visitors": {
      "value": 1234
    },
    "pageviews": {
      "value": 5678
    },
    "bounce_rate": {
      "value": 45
    },
    "visit_duration": {
      "value": 180
    }
  }
}
```

## 详细数据细分

按特定维度（页面、来源、国家等）分析流量：

```bash
node scripts/breakdown.mjs <site-id> <property> [--period day|7d|30d] [--limit N]
```

属性：
- `visit:source` - 流量来源（Google、Twitter、直接访问等）
- `visit:referrer` - 引荐 URL
- `visit:utm_medium` / `visit:utm_source` / `visit:utm_campaign` - UTM 参数
- `visit:device` - 桌面设备 vs 移动设备
- `visit:browser` - 浏览器类型
- `visit:os` - 操作系统
- `visit:country` - 国家
- `event:page` - 最热门页面

示例：
```bash
# Top 10 pages in the last 7 days
node scripts/breakdown.mjs example.com event:page --period 7d --limit 10

# Traffic sources today
node scripts/breakdown.mjs example.com visit:source

# Countries in the last 30 days
node scripts/breakdown.mjs example.com visit:country --period 30d
```

示例输出：
```json
{
  "results": [
    {
      "page": "/",
      "visitors": 542,
      "pageviews": 1024
    },
    {
      "page": "/about",
      "visitors": 123,
      "pageviews": 145
    }
  ]
}
```

## 环境变量

- `PLAUSIBLE_API_KEY`（必填）- 您的 Plausible Analytics API 密钥
- `PLAUSIBLE_SITE_ID`（可选）- 要使用的默认站点 ID

## 资源

### 脚本：
- `stats.mjs` - 按时间段汇总统计数据
- `realtime.mjs` - 实时访客数量
- `breakdown.mjs` - 按维度进行详细数据细分