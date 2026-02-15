---
name: meta-ad-creatives
version: 1.0.0
description: **Track Meta (Facebook/Instagram) 广告创意的表现及点击率**  
该工具可用于追踪多个账户中的广告创意效果及点击率。适用于需要了解广告创意的成功率、哪些广告达到了预期效果、进行 CPT（每次点击费用）、CPI（每千次展示费用）或 ROAS（投资回报率）分析，以及比较不同账户或时间段内的广告创意表现的情况。支持多种评估指标（CPT、CPI、IPM、ROAS），并支持货币转换功能。
---

# Meta Ad 创意内容管理

该功能用于跟踪多个 Meta Ad 账户的创意内容表现和点击率。

## 功能概述

- 计算创意内容的**点击率**（即达到性能基准的创意内容所占的比例）
- 收集多种指标数据：**CPT**（每次尝试的成本）、**CPI**（每次安装的成本）、**IPM**（每千次展示的安装次数）、**ROAS**（投资回报率）
- 比较多个账户之间的表现
- 保存**历史数据**以供趋势分析
- 识别表现优异的创意内容与表现不佳的创意内容
- 支持国际账户的**货币转换**

## 设置

### 1. 环境变量

```bash
FACEBOOK_ACCESS_TOKEN=your_token_here
FACEBOOK_APP_ID=your_app_id
FACEBOOK_APP_SECRET=your_app_secret
```

### 2. 账户配置

创建 `accounts_config.json` 文件：

```json
{
  "accounts": {
    "ClientName": {
      "account_id": "123456789",
      "filter": "CampaignNameFilter",
      "geo_filter": "US",
      "benchmark_value": 100,
      "benchmark_display": "CPT < $100",
      "active": true
    }
  }
}
```

配置字段：
- `account_id`：Meta Ad 账户 ID（不含 `act_` 前缀）
- `filter`：活动名称过滤器（可选）
- `geo_filter`：地理过滤器（例如 “US”）（可选）
- `benchmark_value`：表现优异的创意内容的 CPT 阈值
- `benchmark_display`：人类可读的基准描述

## 使用方法

### 获取当月的点击率

```python
from scripts.meta_ad_creatives import get_all_hit_rates

data = get_all_hit_rates(month_offset=0)
print(f"Overall hit rate: {data['totals']['hit_rate']}%")
for account in data['accounts']:
    print(f"  {account['account_name']}: {account['hit_rate']}%")
```

### 获取上个月的点击率

```python
# Last month
data = get_all_hit_rates(month_offset=-1)

# Two months ago
data = get_all_hit_rates(month_offset=-2)
```

### 获取历史累计数据

```python
data = get_all_hit_rates(all_time=True)
```

### 获取单个广告的表现数据

```python
from scripts.meta_ad_creatives import get_individual_ads

# All ads for an account
ads = get_individual_ads(account_name="ClientName", month_key="2026-01")

# Only winning ads
winners = get_individual_ads(account_name="ClientName", hit_only=True)

# Sort by CPT
ads = get_individual_ads(sort_by="cpt")
```

### 进行月度比较

```python
from scripts.meta_ad_creatives import get_monthly_comparison

# Compare last 3 months
months = get_monthly_comparison(num_months=3)
for month in months:
    print(f"{month['month_label']}: {month['totals']['hit_rate']}%")
```

## 主要指标

| 指标 | 描述 |
|--------|-------------|
| Total Ads | 该期间创建的广告数量 |
| Ads with Spend | 收到预算的广告数量 |
| Ads Hitting Benchmark | 达到 CPT 阈值的广告数量 |
| Hit Rate | 达到基准的广告所占比例 |
| CPT | 每次尝试的成本（花费 / 尝试次数） |

## 点击率计算规则

当创意内容满足以下条件时，即被视为“达到基准”：
1. 花费大于 $0$
2. 尝试次数大于 0$
3. CPT 低于 `benchmark_value`（例如 $100$

点击率 = （达到基准的广告数量 / 收到预算的广告数量）× 100%

## 数据存储

该功能会将历史数据存储在以下数据库中以供趋势分析：
- **Firestore**（云部署的默认选择）
- **SQLite**（本地备份选项）

若需在本地使用 SQLite，请将 `USE_fireSTORE=false` 设置为 `true`。

## 常见问题解答

- “我们这个月的创意内容点击率是多少？”
- “哪些创意内容对 [客户] 来说表现优异？”
- “这个月与上个月相比如何？”
- “请显示所有达到基准的广告。”
- “我们的历史点击率是多少？”