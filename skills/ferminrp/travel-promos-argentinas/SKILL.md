---
name: travel-promos-argentina
description: 使用 Anduin Promos API 查询来自阿根廷的旅行优惠信息。当用户查询阿根廷的旅行优惠、航班优惠、酒店优惠或旅行套餐时，可以使用此 API；同时也可以查询巴西/美国/欧洲的优惠信息，以及按评分排名的优惠活动或最新的航空优惠信息。
---
# 阿根廷旅游促销活动

您可以查看旅游促销活动（包括航班、酒店和旅行套餐），并能够对其进行本地过滤和排序。

## API概述

- **基础URL**：`https://anduin.ferminrp.com`
- **认证**：无需认证
- **响应格式**：JSON
- **主要端点**：`/api/v1/promos`
- **OpenAPI文档**：`https://anduin.ferminrp.com/docs/openapi.json`
- **数据来源**：`data.source`
- **相关时间戳**：
  - `data.lastUpdated`（促销活动更新时间）
  - `timestamp`（服务响应时间）
- **`/api/v1/promos`的文档化查询参数**：无
- **注意**：虽然测试过`category`、`destinationCountry`、`limit`、`q`等查询参数，但它们在API层面并不具备过滤功能；请使用`jq`进行本地过滤（已在当前端点响应中验证）。

## 端点

- `GET /api/v1/promos`

**使用示例**：

```bash
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos[0:5]'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | map(select(.category == "vuelos"))'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | map(select(.category == "autos"))'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | map(select(.destinationCountry == "brazil"))'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | sort_by(.date) | reverse | .[0:10]'
curl -s "https://anduin.ferminrp.com/api/v1/promos" | jq '.data.promos | sort_by(-.score) | .[0:10]'
```

## 关键字段

- **顶级字段**：
  - `success`（布尔值，表示请求是否成功）
  - `timestamp`（ISO格式的日期时间）
- **data**：
  - `lastUpdated`（ISO格式的日期时间）
  - `source`（数据来源URL）
  - `totalPromos`（促销活动总数）
  - `promos`（促销活动数组）
- **promos[]**：
  - `id`（促销活动ID）
  - `date`（活动日期）
  - `title`（活动标题）
  - `permalink`（活动链接）
  - `thumbnailUrl`（活动缩略图URL）
  - `destinationCountry`（目的地国家，可能为`null`）
  - `category`（促销活动类别）
  - `score`（排名分数，若AI分类失败则可能不显示）

- **今日可用的动态字段（示例，非固定列表）**：
  - `category`：`vuelos`（航班）、`hoteles`（酒店）、`autos`（汽车）、`paquetes`（旅行套餐）、`asistencia`（辅助服务）、`otros`（其他）
  - `destinationCountry`：`brazil`（巴西）、`united_states`（美国）、`spain`（西班牙）、`dominican_republic`（多米尼加共和国）、`aruba`（阿鲁巴）、`mexico`（墨西哥）、`japan`（日本）、`portugal`（葡萄牙）、`europa`（欧洲）、`null`（无特定国家）
- **其他语义信息**：
  - `permalink`会根据请求主机动态生成，格式为`/links/viajes/:id`

## 工作流程

1. **识别用户需求**：
  - 显示所有促销活动列表
  - 按类别或国家筛选
  - 按排名顺序显示活动
  - 显示最新促销活动
2. 使用`curl -s`请求该端点
3. 确保`success`为`true`且`data.promos`存在
4. 使用`jq`进行本地过滤和排序：
  - 按类别
  - 按目的地国家
  - 根据`title`或`id`中的文本
  - 根据日期或评分
5. 首先返回以下信息：
  - 总促销活动数量（`totalPromos`）
  - 最后更新时间（`lastUpdated`）
  - 按评分或相关性排序的前3个促销活动
6. 然后显示简要列表（前5/10个活动）：
  - `date` | `category` | `destinationCountry` | `score` | `title`
7. 仅显示被选中的促销活动的链接（`permalink`）
8. 响应内容应仅包含促销信息，不提供财务建议或可用性保证。

## 错误处理

- **HTTP请求失败**：
  - 显示HTTP错误代码及请求的端点
- **404（`No promos data available`）**：
  - 说明当前没有缓存的促销数据
- **`success: false`**：
  - 如果存在错误，显示错误信息
- **JSON格式错误**：
  - 显示基本的错误信息并说明数据不一致的问题
- **网络问题或超时**：
  - 重试2次，每次间隔较短的时间
- **`promos`为空**：
  - 显示“当前没有可用的促销活动”

## 结果展示

- **默认格式**：
  - 活动概要 + 简要列表
- **优先考虑因素**：
  - 活动日期（最新性）
  - 活动相关性（评分）
  - 目地和类别的明确性
- 明确显示时间戳（`lastUpdated`和/或`timestamp`）以及数据来源（`data.source`）
- 仅提供促销活动信息，不提供购买建议

## 不在范围内的操作

- **V1版本禁止的操作**：
  - 直接从外部网站抓取数据
  - 自动预订或购买功能
  - 推送通知或跟踪活动变化
- 使用除`/api/v1/promos`之外的其他API端点