---
name: seats-aero
description: 通过 `seats.aero` API 检查奖励航班的可用性。该功能适用于以下场景：奖励航班预订、里程兑换、寻找商务舱/头等舱的座位、以及航线可用性查询。
---

# Seats.aero 奖励航班搜索

使用 seats.aero 合作伙伴 API，在 24 个里程计划中搜索奖励航班的可用性。

## 设置

在搜索之前，您需要一个 seats.aero API 密钥：

1. 如果用户尚未提供 API 密钥，请提示他们：
   - “请提供您的 seats.aero API 密钥。您可以在 https://seats.aero/partner 获取一个。”
2. 将密钥存储在对话上下文中，以便后续请求使用。
3. 所有请求都需要添加以下头部信息：`Partner-Authorization: Bearer {api_key}`

## 核心功能

### 1. 搜索航线 (`/search`)
在所有里程计划中搜索特定起讫点对的航班可用性（已缓存的数据）。

### 2. 批量查询可用性 (`/availability`)
查询单个里程计划的全部航班可用性，可选择按地区过滤。

### 3. 航线查询 (`/routes`)
获取特定里程计划监控的所有航线信息。

### 4. 航班详情 (`/trips/{id}`)
获取特定航班的详细信息及预订链接。

## 快速参考

| 项目 | 值 |
|------|-------|
| 基础 URL | `https://seats.aero/partnerapi/` |
| 认证头部 | `Partner-Authorization: Bearer {key}` |
| 日期格式 | `YYYY-MM-DD` |

### 客舱代码
- `Y` = 经济舱
- `W` = 高级经济舱
- `J` = 商务舱
- `F` = 头等舱

### 地区
北美、南美、欧洲、非洲、中东、亚洲、大洋洲

## 支持的计划

```
aeroplan, alaska, american, aeromexico, azul, copa, delta, emirates,
ethiopian, etihad, finnair, flyingblue, gol, jetblue, lufthansa,
qantas, qatar, sas, saudia, singapore, turkish, united,
virginatlantic, virginaustralia
```

## 常见工作流程

### 查找特定航线的航班可用性
**用户**：“查找下个月从旧金山（SFO）到东京的商务舱航班”

1. 使用 `/search` 端点，输入：
   - `origin_airport=SFO`（出发机场）
   - `destination_airport=NRT,HND`（东京的两个机场）
   - `cabin=J`（客舱类型）
   - `start_date` 和 `end_date`（日期范围）

### 查询计划内的航班可用性
**用户**：“联合航空（United）在欧洲有哪些可用的奖励航班？”

1. 使用 `/availability` 端点，输入：
   - `source=united`（航空公司名称）
   - `origin_region=Europe`（出发地区）

### 获取预订详情
**用户**：“显示该航班的详细信息”

1. 使用 `/trips/{id}` 端点，并传入上一步搜索得到的航班 ID。
2. 响应中包含航班段、航班时间和预订链接。

### 查询某个计划覆盖的航线
**用户**：“Aeroplan 监控哪些航线？”

1. 使用 `/routes` 端点，输入 `source=aeroplan`（航空公司名称）。

## API 参数快速指南

### /search
| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| origin_airport | 是 | 3 位字母的 IATA 代码 |
| destination_airport | 是 | 3 位字母的 IATA 代码（用逗号分隔） |
| cabin | 否 | Y、W、J 或 F（多个选项用逗号分隔） |
| start_date | 否 | YYYY-MM-DD（开始日期） |
| end_date | 否 | YYYY-MM-DD（结束日期） |
| sources | 否 | 航空公司名称（用逗号分隔） |
| only_direct | 否 | 是否仅显示直飞航班 |
| take | 否 | 每页显示的结果数量（默认为 100 条） |
| cursor | 否 | 分页游标 |

### /availability
| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| source | 是 | 单个航空公司名称 |
| cabin | 否 | 单一客舱代码 |
| origin_region | 否 | 按出发地区过滤 |
| destination_region | 否 | 按目的地地区过滤 |
| start_date | 否 | YYYY-MM-DD（开始日期） |
| end_date | 否 | YYYY-MM-DD（结束日期） |
| take | 否 | 每页显示的结果数量 |

## 脚本使用

对于复杂或重复的搜索操作，可以使用 Python 辅助工具：

```python
from scripts.seats_api import search_availability, format_results

results = search_availability(
    api_key="your_key",
    origin="SFO",
    destination="NRT",
    start_date="2024-03-01",
    end_date="2024-03-31",
    cabins="J,F"
)
print(format_results(results["data"], cabin="J"))
```

请参阅 `scripts/seats_api.py` 以获取完整的 API 客户端实现。

## 响应处理

### 可用性对象字段
- `ID` - 用于通过 `/trips/{id}` 查找航班详情
- `Route` - 起讫点对
- `Date` - 航班日期
- `YAvailable`, `WAvailable`, `JAvailable`, `FAvailable` - 航班是否可用（布尔值）
- `YMileageCost` 等 - 各客舱所需的里程数
- `YDirects` 等 | 可用的直飞航班数量
- `Source` - 航空公司名称
- `ComputedLastSeen` - 数据更新时间戳

### 错误处理
- 401：API 密钥无效或缺失
- 429：请求次数限制，请稍后再试
- 404：没有结果或提供的可用性 ID 无效

## 提示

1. **日期范围**：建议使用 30-60 天内的航班以获得更快结果。
2. **多个客舱类型**：同时搜索 `J` 和 `F` 以获取更高级别的舱位选项。
3. **直飞航班**：使用 `only_direct=true` 过滤非直飞航班。
4. **分页**：使用响应中的 `cursor` 参数进行分页查询。
5. **数据更新**：检查 `ComputedLastSeen` 字段，较旧的数据可能已失效。

## 参考文档

有关完整的 API 规范（包括所有字段和响应格式），请参阅 `references/api-spec.md`。