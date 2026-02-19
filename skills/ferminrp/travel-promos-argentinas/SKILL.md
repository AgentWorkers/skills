---
name: travel-promos-argentina
description: 使用 Anduin Promos API 查询来自阿根廷的旅行优惠信息。当用户请求阿根廷的旅行优惠、航班优惠、酒店优惠或旅行套餐信息时，可以使用该 API；同时也可以查询巴西/美国/欧洲地区的最佳优惠信息，或者按照评分对优惠进行排序，以及最新的航空优惠信息。
---
# 阿根廷旅游促销活动

您可以查看旅游促销信息（包括航班、酒店和旅游套餐），并能够对其进行本地过滤和排序。

## API概述

- **基础URL**: `https://anduin.ferminrp.workers.dev`
- **身份验证**: 无需身份验证
- **响应格式**: JSON
- **主要端点**: `/api/v1/promos`
- **上游数据源**: `data.source`
- **相关时间戳**:
  - `data.lastUpdated`（促销信息更新时间）
  - `timestamp`（服务响应时间）
- **注意**：已测试的查询参数（`category`、`destinationCountry`、`limit`、`q`）在API层面不提供过滤功能；需使用`jq`进行本地过滤。

## 端点

- `GET /api/v1/promos`

**使用示例**:

```bash
curl -s "https://anduin.ferminrp.workers.dev/api/v1/promos" | jq '.'
curl -s "https://anduin.ferminrp.workers.dev/api/v1/promos" | jq '.data.promos[0:5]'
curl -s "https://anduin.ferminrp.workers.dev/api/v1/promos" | jq '.data.promos | map(select(.category == "vuelos"))'
curl -s "https://anduin.ferminrp.workers.dev/api/v1/promos" | jq '.data.promos | map(select(.destinationCountry == "brazil"))'
curl -s "https://anduin.ferminrp.workers.dev/api/v1/promos" | jq '.data.promos | sort_by(-.score) | .[0:10]'
```

## 关键字段

- **顶级字段**:
  - `success`（布尔值，表示请求是否成功）
  - `timestamp`（ISO格式的日期时间）
- **data**:
  - `lastUpdated`（ISO格式的日期时间）
  - `source`（数据来源URL）
  - `totalPromos`（促销活动总数）
  - `promos`（促销活动数组）
- `promos[]`:
  - `id`、`date`、`title`、`link`、`permalink`、`thumbnailUrl`
  - `destinationCountry`（目的地国家，可能为`null`）
  - `category`（促销类型）
  - `score`（排名分数）
- **今日动态字段（示例，非固定列表）**:
  - `category`：`vuelos`（航班）、`hoteles`（酒店）、`paquetes`（旅游套餐）、`otros`（其他）
  - `destinationCountry`：`brazil`（巴西）、`united_states`（美国）、`spain`（西班牙）、`dominican_republic`（多米尼加共和国）、`aruba`（阿鲁巴岛）、`south_africa`（南非）、`null`（无特定目的地）

## 工作流程

1. **识别用户需求**:
   - 显示所有促销活动列表
   - 按类别或国家筛选
   - 按排名分数排序
   - 显示最新促销活动
2. 使用`curl -s`请求该端点
3. 确保`success`为`true`且`data.promos`存在
4. 使用`jq`进行本地过滤和排序：
   - 按类别
   - 按目的地国家
   - 按日期或排名分数
5. 首先返回以下信息：
   - 总促销活动数量（`totalPromos`）
   - 最后更新时间（`lastUpdated`）
   - 按排名或相关性排序的前3个促销活动
6. 然后显示简要信息表（前5/10个促销活动）：
   - `date` | `category` | `destinationCountry` | `score` | `title`
7. 仅对显示的促销活动提供链接（`link`或`permalink`）
8. 响应内容应仅包含基本信息，不包含财务建议或可用性保证。

## 错误处理

- **HTTP请求失败**:
  - 显示HTTP错误代码和请求的端点
- **`success`为`false`时**:
  - 如果有错误信息，则显示错误内容
- **JSON格式异常**:
  - 显示基本的错误信息并说明不一致之处
- **网络问题或超时**:
  - 重试2次，每次等待较短的时间间隔
- **`promos`为空**:
  - 显示“当前没有可用的促销活动”

## 结果展示方式

- **默认格式**:
  - 概要信息 + 简要信息表
- **优先考虑因素**:
  - 最新性（`date`）
  - 相关性（`score`）
  - 目的地和类别的清晰度
- 明确显示时间戳（`lastUpdated`和/或`timestamp`）以及数据来源（`data.source`）
- 仅提供促销活动信息，不提供购买建议

## 不在范围内的操作

- 在v1版本中禁止以下操作：
- 直接从外部网站抓取数据
- 自动化预订或购买流程
- 发送推送通知或跟踪变化
- 使用除`/api/v1/promos`之外的其他端点