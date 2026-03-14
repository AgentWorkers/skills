---
name: hotel
description: 这是一个以本地酒店资源为优先的决策引擎，用于处理旅行住宿的相关任务，包括酒店比较、候选酒店列表的生成、预订准备情况以及住宿计划的制定。无论用户何时提及酒店、住宿地点、酒店属性的比较、住宿天数、地理位置的权衡、预算、酒店设施、预订决策，或是为旅行选择最佳住宿方案，都可以使用该引擎。该引擎能够捕捉用户的酒店需求，存储旅行相关信息，对各种因素进行综合评估，并根据用户的预算、地理位置、酒店设施以及决策的可靠性，推荐最合适的酒店。
---
# 酒店：让住宿选择更加便捷。

## 核心理念
1. 将模糊的住宿计划转化为明确的酒店选择。
2. 清晰地权衡各种因素：价格、位置、设施、便利性、灵活性。
3. 在预订前先进行筛选。
4. 通过明确决策标准来减少预订后的后悔。

## 运行时要求
- 必须安装 Python 3，并将其设置为 `python3` 可执行路径。
- 不需要任何外部包。

## 数据存储
所有数据仅存储在本地，路径如下：
- `~/.openclaw/workspace/memory/hotel/trips.json`
- `~/.openclaw/workspace/memory/hotel/hotels.json`
- `~/.openclaw/workspace/memory/hotelpreferences.json`

无需外部同步，也不需要使用任何预订 API 或凭证。

## 核心数据结构
- `trip`：目的地、日期、预算、出行目的、约束条件
- `hotel`：酒店候选信息，包括价格、所在区域、设施、退款政策、备注
- `preference`：用户可复用的偏好设置，例如是否需要早餐、房间是否安静、是否支持灵活取消等

## 主要工作流程
- **创建旅行计划**：`add_trip.py` --destination "东京" --check_in 2026-04-10 --check_out 2026-04-13 --budget_total 450`
- **添加酒店信息**：`add_hotel.py` --trip_id TRP-XXXX --name "酒店A" --nightly_price 120 --area "新宿" --amenities wifi,breakfast`
- **比较酒店**：`compare_hotels.py` --trip_id TRP-XXXX`
- **筛选酒店**：`shortlist.py` --trip_id TRP-XXXX --top 3`
- **预订检查**：`book_ready.py` --hotel_id HOT-XXXX`
- **保存偏好设置**：`save_preference.py` --key 早餐 --value 必需

## 脚本说明
| 脚本 | 功能 |
|---|---|
| `init_storage.py` | 初始化本地存储 |
| `add_trip.py` | 创建新的旅行计划 |
| `add_hotel.py` | 添加酒店候选信息 |
| `compare_hotels.py` | 比较旅行计划的酒店选项 |
| `shortlist.py` | 筛选出最合适的酒店 |
| `book_ready.py` | 检查酒店是否适合预订 |
| `save_preference.py` | 保存用户的偏好设置 |