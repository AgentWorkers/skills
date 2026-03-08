---
name: aerobase-lounges
description: 机场贵宾休息室使用指南及物品领取建议
metadata: {"openclaw": {"emoji": "🏧", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true}}
---
# 机场休息室的使用与选择

帮助用户找到适合缓解时差影响的机场休息室。推荐时差缓解相关的休息室时，需考虑以下因素：“Delta Sky Club 提供淋浴设施和安静区域——非常适合在夜间航班前进行3小时的休息。”

## 搜索功能（v1 API - 推荐使用）

**GET /api/v1/lounges** — 使用过滤器搜索机场休息室  
查询参数：`airport`（机场）、`airline`（航空公司）、`network`（航空联盟）、`tier`（休息室等级）、`search`（搜索条件）、`limit`（返回结果数量）、`offset`（结果偏移量）  
返回内容：包含时差缓解功能、设施信息及休息室评分的休息室列表  

示例：`GET /api/v1/lounges?airport=JFK&tier=1`  

## 旧版搜索方式  

**GET /api/lounges** — `{ airport?, airline?, network?, tier?, search? }`  
**GET /api/airports/{code}/lounges** — 某特定机场的休息室列表  

数据来源于包含详细休息室信息的 LR 表格。  

## 休息室信息  

数据库中包含以下与缓解时差相关的字段：  
- **recoveryScore**：1-10 分的评分，分数越高，缓解时差的效果越好  
- **hasShowers**：布尔值——适合在航班间隙清洁身体  
- **hasSpa**：布尔值——高级的时差缓解选项  
- **hasSleepPods**：布尔值——提供航班间隙的休息空间  
- **quietZone**：布尔值——有助于调整生物钟  
- **naturalLight**：布尔值——有助于缓解时差  
- **amenities**：数组——包含餐厅、酒吧、淋浴设施、水疗服务、休息舱等  

## 常规建议：  
- 始终在推荐休息室时提供其时差缓解评分  
- 对于长途航班，建议选择提供淋浴设施的休息室  
- 对于夜间航班，推荐设有安静区域的休息室  
- 提及休息室的入场方式（是否需要 Priority Pass）  
- 在推荐休息室或酒店时，需考虑中转时间  

## 使用限制：  
- 每小时最多可搜索 30 次  
- 每小时最多可查询 20 个特定机场的休息室信息  

## 浏览器自动化操作  

仅使用浏览器进行以下操作：  
- 休息室位置和质量的视觉确认  
- 实时检查休息室的开放时间  
- 确认入场要求（如是否需要 Priority Pass 等）  

### Priority Pass 休息室信息获取  

Priority Pass 的相关数据可通过 scraping 功能获取（无需使用代理）。该功能用于实时检查休息室的开放时间及入场要求：  
参考文档：[Scrapling 文档](https://scrapling.readthedocs.io/en/latest/overview.html)  

```
web_fetch {SCRAPLING_URL}/fetch?url=https://www.prioritypass.com/lounges/united-states/new-york-ny/jfk-john-f-kennedy-intl&json=1&extract=css&selector=.lounge-card
```  

请将 `country/city/airport` 替换为实际需要查询的地点名称。返回的休息室信息包括开放时间、入场方式及设施详情。  
关于休息室卡（LoungeCard）的渲染方式，请参阅 **aerobase-ui** 中的 LoungeCard 组件规范。  

### 何时无需使用浏览器：  
- 一般性的休息室搜索：API 提供了全面的信息  
- 入场信息验证：API 可显示是否需要 Priority Pass 等信息  
- 仅需要使用浏览器进行视觉确认或检查开放时间时