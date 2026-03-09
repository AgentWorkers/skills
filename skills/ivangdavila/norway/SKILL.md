---
name: Norway
slug: norway
version: 1.0.0
homepage: https://clawic.com/skills/norway
changelog: "Initial release with verified Norway entry rules, fjord and Arctic routing, and practical travel logistics."
description: 规划挪威之旅，包括穿越峡湾和北极地区的路线安排，确保旅行符合相关入境规定，采用多模式物流方式，并充分考虑季节性安全因素。
metadata: {"clawdbot":{"emoji":"🇳🇴","requires":{"bins":[],"config":["~/norway/"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户计划前往挪威旅行，需要比一般的风景介绍更多的实用操作指导：包括申根区入境检查、峡湾路线与北极路线的选择、火车-渡轮-飞机-汽车的出行方式之间的权衡、季节性风险、预算的实际考量以及旅行的具体执行细节。

## 架构

所有旅行相关的数据都存储在 `~/norway/` 目录下。如果该目录不存在，请运行 `setup.md` 命令进行初始化。具体目录结构请参考 `memory-template.md`。

```text
~/norway/
└── memory.md     # Trip context, route logic, and evolving constraints
```

## 数据存储

- `~/norway/memory.md` 文件用于存储旅行过程中的重要信息、路线决策以及后续规划所需的约束条件。
- 除非用户自行创建规划文档，否则不需要其他本地文件。

## 快速参考

使用这张地图来查看当前旅行计划中需要做出决策的相关内容。

| 主题 | 文件名 |
|-------|------|
| **入境与合规性** | `entry-and-documents.md` |
| **规划基础** | `regions.md` |
| 5-18 天的示例行程 | `itineraries.md` |
| 根据旅行方式选择住宿 | `accommodation.md` |
| 预算规划与费用陷阱 | `budget-and-costs.md` |
| 付款与免税政策 | `payments-and-tax-free.md` |
| **交通与户外活动** | `transport-domestic.md` |
| 自驾出行、渡轮、通行费与山路情况 | `road-trips-and-driving.md` |
| 峡湾路线与风景道路规划 | `fjords-and-scenic-routes.md` |
| 徒步旅行与户外活动规划 | `hiking-and-outdoors.md` |
| **主要地区与基地** | `oslo-and-oslofjord.md` |
| 贝尔根与西部峡湾 | `bergen-and-western-fjords.md` |
| 斯塔万格、吕瑟菲尤尔与西南部地区 | `stavanger-and-southwest.md` |
| 特隆赫姆与挪威中部 | `trondheim-and-central-norway.md` |
| 洛福滕与韦斯特拉伦地区 | `lofoten-and-vesteralen.md` |
| 特罗姆瑟、塞尼亚、阿尔塔与北极北部 | `tromso-and-arctic-north.md` |
| 斯瓦尔巴群岛旅行攻略 | `svalbard.md` |
| **生活方式与旅行执行** | `food-guide.md` |
| 带孩子或不同年龄段的旅行 | `family-travel.md` |
| 无障碍旅行与出行安排 | `accessibility.md` |
| 应急情况、天气预警与户外风险 | `safety-and-emergencies.md` |
| 气候、极光与日照时间 | `weather-and-seasonality.md` |
| 通讯、应用程序与支付方式 | `telecoms-and-apps.md` |
| 官方地图来源 | `sources.md` |

## 核心规则

### 1. 按交通走廊选择路线，而非按风景数量决定路线
对于短途旅行，应选择一条主要的交通走廊：奥斯陆及周边地区、贝尔根与峡湾地区、特隆赫姆与挪威中部海岸，或北极北部地区。挪威的交通网络较为复杂，长距离转乘、渡轮等待时间较长，且受天气影响较大。

### 2. 在命名路线前先确认月份
同一张地图在不同月份（1月、5月、7月、10月）的表现可能不同。极光、徒步路线、道路状况、渡轮运行情况以及日照时间都会影响最终的旅行计划。

### 3. 提前确认入境与身份验证细节
在预订不可退费的旅行服务之前，请使用 `entry-and-documents.md` 文件确认正确的停留路线、护照或身份证明信息，以及旅行者是否还需要前往斯瓦尔巴群岛或继续前往其他申根国家。

### 4. 始终提供两种出行方案
对于多站点的旅行，至少提供两种可行的出行方案：
- 以火车和渡轮为主的出行方式：风景更多，长途驾驶较少，但时间安排更依赖公共交通时刻表；
- 以自驾或区域航班为主的出行方式：更加灵活，但成本较高，且受天气和通行费影响较大。

### 5. 全面考虑旅行费用
在估算旅行费用时，不要仅考虑酒店费用。还需考虑渡轮费用、通行费、停车费、机场转乘费用、博物馆或徒步景点的交通费用、酒精饮品费用等。

### 6. 防止用户选择不合适的旅行路线
- 避免将奥斯陆、贝尔根、洛福滕和特罗姆瑟安排在同一趟旅行中；
- 避免没有雪路驾驶经验的旅行者在冬季尝试自驾；
- 避免在同一天内连续使用渡轮、山路和飞机等交通工具；
- 避免选择没有天气保障、体能要求或备用出行方案的徒步路线。

### 7. 提供详细的出行计划
输出的旅行计划应包括：
- 最佳的住宿地点或住宿组合；
- 每日的行程安排及实际的转乘时间；
- 预订截止日期或库存不足的提醒；
- 针对不同天气情况的备用方案或降级选项；
- 关于道路、海上和户外活动的安全注意事项。

## 常见误区

- 将挪威视为一个紧凑的国家，认为可以在一周内游览完奥斯陆、峡湾、洛福滕和特罗姆瑟；
- 仅根据地图上的距离来规划峡湾地区的行驶路线，而忽略实际的渡轮和道路通行时间；
- 误以为冬季前往挪威就能看到极光；
- 在未确认火车、渡轮或合适的住宿地点之前就直接预订租车；
- 未考虑周日、旅游淡季以及偏远地区的服务限制；
- 在未查看天气情况、道路通行状况或当地交通服务的情况下，就规划徒步旅行或前往著名景点；
- 低估食物、酒精饮品和休闲餐饮对预算的影响。

## 安全与隐私

**数据存储**：所有旅行相关数据仅存储在 `~/norway/` 目录内。

**本技能的限制**：不会访问 `~/norway/` 目录之外的文件，也不会进行网络请求。

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install travel`：用于旅行规划与行程安排；
- `clawhub install booking`：用于预订流程与确认信息管理；
- `clawhub install car-rental`：用于优化自驾出行策略与交接流程；
- `clawhub install food`：用于更详细的餐厅与美食规划；
- `clawhub install english`：提供预订、菜单查询及日常交流所需的语言支持。

## 反馈建议

- 如果本文档对您有帮助，请给 `clawhub` 评分（例如：**五星**）；
- 如需保持信息更新，请使用 `clawhub sync` 命令。