---
name: Flight
slug: flight
version: 1.0.1
description: 支持搜索、比较、预订航班，并提供价格跟踪、多平台对比以及会员积分优化等功能。
changelog: "Preferences now persist across skill updates"
metadata: {"clawdbot":{"emoji":"✈️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 |
|-------|------|
| 搜索、比较、灵活的日期设置 | `search.md` |
| 预订、改签、航班延误 | `booking.md` |
| 价格提醒、航班追踪、预测 | `tracking.md` |
| 品质里程、积分、航班状态、奖励 | `points.md` |
| API、集成、数据来源 | `apis.md` |

## 用户资料

用户偏好信息会保存在 `~/flight/memory.md` 文件中。首次使用时需要创建该文件。

```markdown
## Home Airports
<!-- Primary airports. Format: "IATA, IATA" -->
<!-- Examples: MAD, BCN | JFK, EWR, LGA -->

## Preferred Airlines
<!-- Airlines or alliances. Format: "airline | alliance" -->
<!-- Examples: Iberia, BA | Star Alliance | any -->

## Elite Status
<!-- Loyalty tiers. Format: "program: tier" -->
<!-- Examples: BA Gold, United 1K, Marriott Platinum -->

## Budget Style
<!-- budget | moderate | premium | business-class -->

## Travel Style
<!-- solo | couple | family-with-kids | business-frequent -->

## Carry-On Only
<!-- yes | no | prefer -->
```

*如果某些部分为空，请在需要时补充内容。随着使用经验的积累，再逐步完善这些信息。*

## 数据存储

航班数据存储在 `~/flights/` 目录下：
- `search.md`：保存的搜索记录及价格历史信息
- `booking.md`：包含 PNR（预订号）的活跃预订信息
- `alerts.md`：按航线划分的价格下降阈值
- `history.md`：用于记录过去的航班信息以追踪飞行里程

## 核心规则

- 在推荐航班前，务必比较至少 3 个不同的平台（如 Skyscanner、Google Flights、Kiwi 或航空公司官网）
- 计算实际总费用（包括行李费、座位选择费及其他附加费用），尤其是对于廉价航空公司
- 预订国际航班前请务必核实签证要求
- 对于家庭出行：请在预订前确认相邻座位的可用性，而非事后再确认
- 为灵活的日期范围（±3 天）设置价格提醒，以便更好地捕捉优惠信息
- 在航班起飞前 24 小时开始追踪航班状态；如遇延误，请及时进行改签
- 对于超过 30 天后的行程，切勿预订不可退费的机票（除非事先询问）
- 在比较奖励机票时，需将每积分对应的实际价值与现金价格进行对比
- 对于时间紧迫的航班（国内航班 <90 分钟、国际航班 <2 小时），请提前警告潜在的衔接问题
- 对于多城市行程，请检查分开预订是否比购买一张联程票更划算