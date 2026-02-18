---
name: gumroad
description: 从 Gumroad API 中获取分析数据。跟踪产品信息、销售情况、收入以及转化率。这些数据可用于生成每日统计报告、进行趋势分析，并将营销活动与销售结果进行关联。
---
# Gumroad 分析

通过 Gumroad 的 API 获取产品和销售数据，以便进行跟踪和分析。

## 设置

**凭据：** `~/.config/gumroad/credentials.json`
```json
{
  "access_token": "YOUR_GUMROAD_ACCESS_TOKEN",
  "created_at": "YYYY-MM-DD"
}
```

获取令牌：Gumroad → 设置 → 高级 → 应用程序 → 创建应用程序

## 快速命令

### 获取当前统计数据
```bash
./scripts/gumroad-stats.sh
```

### 获取并记录每日指标
```bash
./scripts/gumroad-daily.sh
```

### 导出销售数据
```bash
./scripts/gumroad-sales.sh [--after YYYY-MM-DD] [--product PRODUCT_ID]
```

## API 参考

**基础 URL：** `https://api.gumroad.com/v2`

**认证：** `Authorization: Bearer ACCESS_TOKEN`

### 主要接口

| 接口 | 功能 |
|----------|---------|
| `GET /products` | 所有产品及其销售数量 |
| `GET /sales` | 带分页功能的销售列表 |
| `GET /sales/:id` | 单个销售的详细信息 |

### 产品响应字段
- `name`, `id`, `short_url`
- `sales_count`, `sales_usd_cents`
- `price`, `formatted_price`
- `published`, `deleted`

### 销售响应字段
- `id`, `email`, `product_name`
- `price`, `gumroad_fee`
- `created_at`, `country`
- `variants`, `custom_fields`

## 指标记录

每日数据快照：`memory/metrics/gumroad/YYYY-MM-DD.json`

```json
{
  "date": "2026-02-17",
  "products_count": 31,
  "published_count": 19,
  "top_products": [
    {"name": "Product", "sales": 9, "revenue_cents": 3300}
  ],
  "totals": {
    "sales": 100,
    "revenue_cents": 8100
  }
}
```

## 分析模式

### 转化率
```
conversion_rate = paid_sales / total_downloads
avg_sale_value = revenue_cents / sales_count
```

### 趋势检测
比较每日 `revenue_cents` 的变化。在以下情况下触发警报：
- 新销售（任何收入增加）
- 收入激增（超过日均值的 2 倍）
- 产品的首次销售

### 相关性追踪
记录用户互动事件（如 Moltbook 帖子、社交媒体活动）及其时间戳，并与销售时间进行对比，以确定转化的驱动因素。

## 限制

- **API 不支持显示流量来源** — 仅在仪表板上可见
- **没有漏斗数据分析** — 不提供页面浏览量/点击量数据
- **请求限制：** 每小时约 500 次请求（较为宽松的限制）