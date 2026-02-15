---
name: supermetrics
description: "官方 Supermetrics 技能：能够从 100 多个平台（包括 Google Analytics、Meta Ads、Google Ads 和 LinkedIn）查询营销数据。需要使用 API 密钥。"
version: 1.0.1
triggers:
  - marketing data
  - supermetrics
  - analytics
  - ads performance
  - campaign metrics
  - google analytics
  - meta ads
  - facebook ads
  - google ads
  - linkedin ads
  - marketing report
author: supermetrics
tags: [marketing, analytics, supermetrics, api, data]
requires:
  env:
    - SUPERMETRICS_API_KEY
---

# Supermetrics营销数据

从100多个平台（包括Google Analytics、Meta Ads、Google Ads和LinkedIn）查询营销数据。

## 使用方法

导入辅助模块：

```python
from supermetrics import (
    discover_sources,
    discover_accounts,
    discover_fields,
    query_data,
    get_results,
    get_today,
    search,
    health,
)
```

## 函数

### discover_sources()

列出所有可用的营销平台。

```python
result = discover_sources()
for src in result['data']['sources']:
    print(f"{src['id']}: {src['name']}")
```

### discover_accounts(ds_id)

获取数据源的关联账户。

**常见数据源ID：**
| ID | 平台 |
|----|----------|
| FA | Meta Ads（Facebook） |
| AW | Google Ads |
| GAWA | Google Analytics |
| GA4 | Google Analytics 4 |
| LI | LinkedIn Ads |
| AC | Microsoft Advertising（Bing） |

```python
result = discover_accounts("GAWA")
for acc in result['data']['accounts']:
    print(f"{acc['account_id']}: {acc['account_name']}")
```

### discover_fields(ds_id, field_type=None)

获取可用的指标和维度。

```python
# Get all fields
result = discover_fields("GAWA")

# Get only metrics
result = discover_fields("GAWA", "metric")

# Get only dimensions
result = discover_fields("GAWA", "dimension")
```

### query_data(...)

执行营销数据查询。返回异步查询的`schedule_id`。

**参数：**
- `ds_id`（必需）：数据源ID
- `ds_accounts`（必需）：通过`discover_accounts()`获取的账户ID
- `fields`（必需）：通过`discover_fields()`获取的字段ID
- `date_range_type`：`last_7_days`、`last_30_days`、`last_3_months`、`custom`
- `start_date`、`end_date`：自定义日期范围（格式为YYYY-MM-DD）
- `filters`：过滤条件（例如，`"country == United States"`）
- `timezone`：IANA时区（例如，`"America/New_York"`）

**过滤操作符：**
- `==`、`!=` - 等于、不等于
- `>`、`>=`、`<`、`<=` - 比较运算
- `=`、`!=` - 包含、不包含
- `=~`、`!=` - 正则表达式匹配

### get_results(schedule_id)

检索查询结果。

```python
result = get_results(schedule_id)
for row in result['data']['data']:
    print(row)
```

### get_today()

获取当前UTC日期，用于日期计算。

```python
result = get_today()
print(result['data']['date'])  # "2026-02-03"
```

### search(query)

在Supermetrics资源中搜索相关帮助和建议。

```python
result = search("facebook ads metrics")
print(result['data'])
```

### health()

检查Supermetrics服务器的健康状态。

```python
result = health()
print(result['data']['status'])  # "healthy"
```

## 工作流程示例

```python
from supermetrics import (
    discover_accounts,
    discover_fields,
    query_data,
    get_results,
)

# 1. Find accounts
accounts = discover_accounts("GAWA")
account_id = accounts['data']['accounts'][0]['account_id']

# 2. See available fields
fields = discover_fields("GAWA", "metric")
print([f['id'] for f in fields['data']['metrics'][:5]])

# 3. Query data
query = query_data(
    ds_id="GAWA",
    ds_accounts=account_id,
    fields=["date", "sessions", "users", "pageviews"],
    date_range_type="last_7_days"
)

# 4. Get results
data = get_results(query['data']['schedule_id'])
for row in data['data']['data']:
    print(row)
```

## 响应格式

所有函数返回的结果格式如下：

```python
{"success": True, "data": {...}}  # Success
{"success": False, "error": "..."}  # Error
```