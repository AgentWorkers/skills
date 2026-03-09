---
name: Switzerland
slug: switzerland
version: 1.0.0
homepage: https://clawic.com/skills/switzerland
changelog: "Initial release with verified Switzerland entry rules, scenic rail and mountain logistics, and practical regional playbooks."
description: 规划瑞士之旅时，需考虑阿尔卑斯山铁路和山区交通物流、经核实的入境规定、风景优美的旅行路线，以及当地的实际情况和执行细节。
metadata: {"clawdbot":{"emoji":"🇨🇭","requires":{"bins":[],"config":["~/switzerland/"]},"os":["linux","darwin","win32"]}}
---
## 设置（Setup）

如果 `~/switzerland/` 文件不存在或为空，请先阅读 `setup.md`，然后按照说明进行操作。

## 使用场景（When to Use）

当用户计划前往瑞士旅行，并需要超出常规旅行建议的实用指导时（例如：申根区入境检查、瑞士法郎的实际花费、火车与汽车的出行方式选择、风景列车与山区旅行的时间安排、地区选择以及实际旅行执行细节等），请参考本文档。

## 架构（Architecture）

所有与瑞士旅行相关的信息都存储在 `~/switzerland/` 文件夹中。具体文件结构请参阅 `memory-template.md`。

```text
~/switzerland/
└── memory.md     # Trip context, routing logic, and evolving constraints
```

## 快速参考（Quick Reference）

使用以下表格来快速查找与当前旅行计划相关的信息：

| 主题 | 对应文件 |
|-------|------|
| **入境与合规性** | `entry-and-documents.md` |
| 游客入境、申根区规定、护照检查 | <br>《入境与文件指南》（Entry and Documents） |
| 海关、免税政策、边境通行规则 | `customs-and-border.md` |
| **旅行规划基础** | <br>宏观区域与路线规划 | `regions.md` |
| 4-14天行程示例 | `itineraries.md` |
| 根据旅行风格选择住宿 | `accommodation.md` |
| 预算制定与隐性费用 | `budget-and-costs.md` |
| 付款方式与免税政策 | `payments-and-tax-free.md` |
| **交通与户外活动** | <br>国内交通方式 | `transport-domestic.md` |
| 驾车旅行相关事项 | `road-trips-and-driving.md` |
| 风景列车、缆车、湖泊、徒步旅行 | `alps-lakes-and-scenic-trains.md` |
| 滑雪、冬季旅行 | `winter-ski-and-snow.md` |
| **主要地区与旅行基地** | <br>苏黎世及周边地区 | `zurich.md` |
| 卢塞恩与中瑞士 | `lucerne-and-central-switzerland.md` |
| 伯尔尼及周边地区 | `bern-and-fribourg.md` |
| 因特拉肯、少女峰、劳特布伦嫩、格林德瓦尔德 | `bernese-oberland.md` |
| 日内瓦、洛桑、蒙特勒与日内瓦湖 | `geneva-lausanne-and-lake-geneva.md` |
| 泽马特、瓦莱州、马特洪峰 | `valais-and-zermatt.md` |
| 格劳宾登州、恩加丁、达沃斯与风景铁路线 | `graubunden-and-engadin.md` |
| 提契诺州与意大利语地区 | `ticino.md` |
| 巴塞尔与侏罗山区 | `basel-and-northwest.md` |
| **生活方式与旅行执行** | <br>饮食指南与当地特色 | `food-guide.md` |
| 带孩子或不同年龄段的家庭旅行 | `family-travel.md` |
| 无障碍旅行与出行安排 | `accessibility.md` |
| 紧急情况处理、天气变化、山区安全 | `safety-and-emergencies.md` |
| 气候、海拔与季节性因素 | `weather-and-seasonality.md` |
| 通讯服务与应用程序 | `telecoms-and-apps.md` |
| 官方旅行地图 | `sources.md` |

## 核心规则（Core Rules）

### 1. 按旅行路线选择地区，而非按景点数量决定
对于短途旅行，建议选择某一主要旅行区域：苏黎世及周边地区、伯尔尼高地、日内瓦湖周边、瓦莱州、格劳宾登州、提契诺州或巴塞尔与侏罗山区。虽然这些地区的风景优美，但频繁更换酒店、乘坐缆车及转乘会增加旅行不便。

### 2. 在确定最佳旅行地区前，先了解当月的天气状况和海拔高度
同样的旅行计划在不同月份（2月、6月、9月、12月）可能会有很大差异。积雪线、湖泊美景、徒步路线、日照时间以及学校假期等因素都会影响旅行体验。

### 3. 原则上选择火车出行；只有在汽车出行更合适时才考虑使用汽车
经典的瑞士旅行路线通常更适合乘坐火车或船只。只有在需要穿越偏远乡村、湖泊地区或频繁穿越边境时，才建议使用汽车。

### 4. 将山区视为旅行中的重要因素，而不仅仅是背景
在规划旅行路线前，请务必参考 `alps-lakes-and-scenic-trains.md`、`winter-ski-and-snow.md` 和 `weather-and-seasonality.md` 等文档。云层、风力、降雪、雪崩风险以及缆车关闭等情况都可能影响旅行计划。

### 5. 根据瑞士的实际费用制定预算
在制定预算时，不要仅依据酒店价格估算。请考虑瑞士法郎的实际价值、度假村税费、缆车票价、停车费用、隧道或通行费、行李搬运费用以及山区食物的额外成本。

### 6. 防范边境相关问题
瑞士虽然属于申根区，但并不适用欧盟的关税和漫游政策。跨境购物、免税政策、周日的商业活动限制以及跨境交通方式都需要特别留意。

### 7. 提供详细的旅行计划
旅行计划应包括：
- 最佳的旅行基地或基地组合
- 每日的行程安排及实际的转乘时间
- 预订截止日期或房源紧张的预警信息
- 天气变化时的备用方案
- 安全、支付方式及紧急应对措施

## 常见误区（Common Traps）

- 将瑞士视为一个可以轻松游览的小国家，认为只需几次火车行程就能完成旅行。
- 将苏黎世、卢塞恩、少女峰、泽马特、圣莫里茨、日内瓦湖和提契诺州合并为一次旅行。
- 在未确认火车（SBB）加上当地巴士或船只是否更合适之前，就直接预订汽车。
- 误以为宣传照片中的山区天气就是实际旅行时的天气。
- 将风景列车行程视为简单的转乘，而忽略了它们通常需要一整天的时间。
- 低估夏季高峰期和滑雪季酒店价格的上涨幅度。
- 误以为瑞士自动适用欧盟的漫游政策、关税规则和欧元定价标准。

## 安全与隐私（Security & Privacy）

- **数据存放位置**：旅行偏好、路线选择及截止日期等信息均存储在 `~/switzerland/` 文件夹内。
- **使用限制**：本技能仅允许访问 `~/switzerland/` 文件夹内的文件，不允许进行网络请求。
- **数据保留规则**：仅在用户正在进行瑞士旅行规划或需要跨会话延续旅行信息时，才会保留本地旅行记录。对于一次性查询，仅提供必要的帮助，不会创建额外的旅行数据。

## 相关技能（Related Skills）
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：用于安装旅行规划相关的工具（如 `travel`、`europe`、`booking`、`car-rental`、`food` 等）：
  - `travel`：通用旅行规划与行程结构工具
  - `europe`：在瑞士属于更长旅行路线时提供更全面的欧洲背景信息
  - `booking`：预订流程与确认相关工具
  - `car-rental`：汽车租赁相关服务与协调流程
  - `food`：餐厅与美食规划工具

## 反馈建议（Feedback）
- 如果本文档对您有帮助，请给予好评（例如：`clawhub star switzerland`）。
- 为了获取最新信息，请使用 `clawhub sync` 命令同步数据。