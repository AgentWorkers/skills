---
name: United States
slug: united-states
version: 1.0.0
homepage: https://clawic.com/skills/united-states
changelog: "Initial release with verified U.S. entry rules, region playbooks, and practical tourism logistics."
description: 规划前往美国的旅行时，请考虑地区特定的路线安排、经过验证的入境要求、交通物流信息以及实用的旅游安全建议。
metadata: {"clawdbot":{"emoji":"🇺🇸","requires":{"bins":[],"config":["~/united-states/"]},"os":["linux","darwin","win32"]}}
---
## 设置

如果 `~/united-states/` 不存在或为空，请阅读 `setup.md` 并按照说明进行设置。

## 适用场景

当用户计划前往美国旅行时，本文档提供了超出一般建议的实际指导，包括入境要求、地区选择、路线规划、交通方式、季节性风险以及旅行中的实际操作指南。

## 架构

所有旅行相关的数据和文档都存储在 `~/united-states/` 目录下。具体结构请参考 `memory-template.md`。

```
~/united-states/
└── memory.md     # Trip context and evolving constraints
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| **入境与边境** | `entry-and-documents.md` |
| 税务、ESTA、I-94、身份证明 | `customs-and-border.md` |
| **旅行规划基础** | `regions.md` |
| 样例行程（7-21天） | `itineraries.md` |
| 住宿安排 | `accommodation.md` |
| 预算与费用规划 | `budget-and-costs.md` |
| 小费与支付习惯 | `tipping-and-payments.md` |
| **交通方式** | `transport-domestic.md` |
| 驾车旅行 | `road-trips-and-driving.md` |
| **自然与公园** | `national-parks.md` |
| **主要地区与城市** | `new-york-city.md` | `washington-dc.md` | `california.md` | `florida.md` | `southwest-and-rockies.md` | `pacific-northwest.md` | `great-lakes-and-midwest.md` | `deep-south-and-louisiana.md` | `hawaii-and-alaska.md` |
| **生活方式与旅行执行** | `food-guide.md` | `nightlife.md` | `family-travel.md` | `accessibility.md` |
| **安全与旅行环境** | `safety-and-emergencies.md` | `weather-and-seasonality.md` |
| **工具与资源** | `telecoms-and-apps.md` | `sources.md` |

## 核心规则

### 1. 按地理区域规划行程，而非按愿望清单
建议每周围绕一个大的地理区域进行旅行规划。美国的地理距离和交通便利性比景点数量更为重要。

### 2. 入境与合规性优先
在制定行程之前，请确保所有旅行相关事项都符合规定（参见 `entry-and-documents.md`）：签证类型、ESTA 状态、护照有效期、I-94 表格填写要求以及国内身份证明的合法性。

### 3. 全面考虑季节因素
在制定户外活动计划前，请务必参考 `weather-and-seasonality.md` 和 `national-parks.md`。高温、风暴、野火烟雾、积雪以及公园的预约系统都可能影响行程的顺利进行。

### 4. 提供多种交通选择
对于每条路线，至少提供两种不同的交通方式，并说明各自的优缺点：
- 以飞机为主（速度较快，但机场相关费用较高）
- 以火车/汽车为主（速度较慢，但能欣赏更多风景，且交通方式不同）

### 5. 根据实际费用制定预算
在制定预算时，请充分考虑实际旅行成本：机场税费、小费、停车/通行费、度假村/目的地的额外费用以及交通转乘费用。

### 6. 提前警示常见陷阱
在用户做出旅行决策前，务必提醒他们可能遇到的问题：
- 从东海岸到西海岸的紧凑行程安排
- 没有提前预订的旺季公园门票
- 在停车费用较高的核心地区租车
- 选择没有人群缓冲或天气保障的主题城市周末旅行

### 7. 提供可执行的旅行计划
旅行计划应包括：
- 基础旅行策略
- 每日的行程安排及转乘时间
- 预订截止日期
- 应对天气或延误情况的备用方案
- 安全与紧急情况的注意事项

## 常见误区

- 将美国视为一个紧凑的国家，认为一次旅行可以游览五个城市。
- 直到最后一周才处理入境和行政手续。
- 不考虑季节或天气变化，固定使用同一份行程计划。
- 低估机场、酒店与目的地之间的交通时间。
- 仅根据夜间房价选择住宿，忽略交通成本和时间因素。
- 假设所有公园和景点在高峰时段都可以随时入场。

## 安全与隐私

**数据存储**：所有旅行相关数据仅存储在 `~/united-states/` 目录内。

**本技能的限制**：不会访问 `~/united-states/` 之外的文件，也不会发起网络请求。

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install travel`：通用旅行规划和行程管理
- `clawhub install car-rental`：更高效的租车策略与交接流程
- `clawhub install booking`：便捷的预订流程与确认机制
- `clawhub install food`：针对每个目的地的详细餐饮规划
- `clawhub install english`：提供语言支持（用于电话沟通、预订和服务交互）

## 反馈建议

- 如果本文档对你有帮助，请给 `clawhub` 评分（例如：给 `united-states` 评分）。
- 为了获取最新信息，请使用 `clawhub sync` 命令保持同步。