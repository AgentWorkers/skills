---
name: tfl-journey-disruption
description: 根据出发/到达时间或特定时间点规划TfL（Transportation for Learning）行程；解析目的地地址（优先使用邮政编码）；在行程受阻时发出警告，并提供替代路线建议。
---

# TfL 旅程规划器 + 突发事件检测功能

当用户需要制定TfL（Transport for London）旅程计划并了解可能出现的交通延误情况时，可使用此功能。

参考文档：https://tfl.gov.uk/info-for/open-data-users/api-documentation

## 脚本辅助工具

使用 `scripts/tfl_journey_disruptions.py` 可快速完成旅程规划及突发事件检测。

**示例：**

```bash
python3 scripts/tfl_journey_disruptions.py \"940GZZLUSTD\" \"W1F 9LD\" --depart-at 0900
python3 scripts/tfl_journey_disruptions.py --from \"Stratford\" --to \"W1F 9LD\" --arrive-by 1800
```

**注意事项：**
- 如果API返回多个选项，请选择其中一个，并使用其 `parameterValue` 重新尝试请求。
- 如果您拥有TfL API密钥，请在环境变量中设置 `TFL_APP_ID` 和 `TFL_APP_KEY`。

## 需要收集的信息：
- **出发地**：邮政编码、车站名称、地点名称或经纬度坐标
- **目的地**：邮政编码、车站名称、地点名称或经纬度坐标
- **时间**：出发时间或到达时间（如未明确指定，则使用“当前时间”）
- **可选信息**：用户可能提及的出行方式或无障碍出行要求

如果这些信息有任何缺失或不明确的地方，请向用户询问详细信息。

## 地点解析：
- 尽量使用邮政编码作为出发/目的地信息。如果无法使用邮政编码，可尝试解析地点名称或车站名称：
  - 如果输入的是英国邮政编码，直接使用该编码作为出发/目的地。
  - 如果输入的是经纬度坐标，直接使用这些坐标。
  - 如果输入的是车站名称，可以尝试使用 `StopPoint/Search/{query}` 来查找相关车站，并选择对应的枢纽站点或NaPTAN ID。
  - 如果搜索结果有多个选项，请显示所有选项（包括常用名称和对应的 `parameterValue`），并让用户进行选择。
  - 如果不确定，请向用户确认相关信息，避免猜测。

## 旅程规划：
调用以下API接口：
`/Journey/JourneyResults/{from}/to/{to}?date=YYYYMMDD&time=HHMM&timeIs=Depart|Arrive`

**使用指南：**
- 如果用户指定“到达时间”，则使用 `timeIs=Arrive`；否则默认使用 `Depart`。
- 如果未提供日期，可询问用户。如果用户表示“现在出发”，则可以省略日期/时间参数。

## 提取候选路线：
从响应结果中选取前1-3条旅程信息：
- 旅程时长及预计到达时间
- 公共交通线路信息（出行方式、线路名称、行驶方向）
- 用于检查交通状况的线路ID（通常位于 `leg.routeOptions[]`.lineIdentifier.id` 或 `leg.line.id` 中）

**交通状况检测：**
对于每条旅程，收集所有涉及的线路ID，并调用以下API接口：
`/Line/{ids}/Status`

如果某条线路的状态不是“良好服务”（Good Service），或者有相关故障说明，则认为该线路处于故障状态。需要总结故障的严重程度和原因。

**可选操作：**
如需要检查特定车站的交通状况，可调用：
`/StopPoint/{id}/Disruption`

**响应策略：**
- 如果最优路线没有交通延误，直接推荐该路线，并说明未发现任何故障。
- 如果最优路线存在故障，首先提醒用户，并提供1-2条备用路线作为替代方案。
- 如果所有路线都处于故障状态，仍然推荐最优路线，但需同时列出故障信息及备用方案。
- 如果旅程安排在未来的时间（如当天晚些时候或另一天），请告知用户当前交通状况可能会发生变化（例如：“目前仅有轻微延误，但到出行时间时情况可能会有所改变”）。
- 始终邀请用户确认所选路线或提供进一步的信息。