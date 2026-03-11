---
name: New Zealand
slug: new-zealand
version: 1.0.0
homepage: https://clawic.com/skills/new-zealand
changelog: "Initial release with island-aware routing, practical transport guidance, and deep New Zealand travel playbooks."
description: 通过了解各岛屿的交通情况、实用的公路旅行攻略、户外安全知识，以及当地美食和地区的特色信息，来探索新西兰吧。
metadata: {"clawdbot":{"emoji":"🇳🇿","requires":{"bins":[],"config":["~/new-zealand/"]},"os":["linux","darwin","win32"]}}
---
## 设置

如果 `~/new-zealand/` 不存在或为空，请阅读 `setup.md` 并按照说明进行设置。

## 使用场景

适用于计划前往新西兰的游客，或需要了解当地信息的用户：需要了解应优先游览哪个岛屿、选择在哪里住宿、如何安全驾驶、提前预订什么、以及如何应对天气、餐饮、费用和户外活动相关的问题。

## 架构

所有与新西兰旅行相关的资料都存储在 `~/new-zealand/` 目录下。具体文件结构请参考 `memory-template.md`。

```text
~/new-zealand/
└── memory.md     # Trip context
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| **主要枢纽与地区** | |
| 奥克兰完整攻略 | `auckland.md` |
| 威灵顿完整攻略 | `wellington.md` |
| 罗托鲁瓦与陶波完整攻略 | `rotorua-taupo.md` |
| 皇后镇完整攻略 | `queenstown.md` |
| 基督城完整攻略 | `christchurch.md` |
| 尼尔森、阿贝尔塔斯曼与马尔堡地区 | `nelson-marlborough.md` |
| 菲奥德兰与南地地区攻略 | `fiordland-southland.md` |
| **旅行规划** | |
| 核心行程安排 | `itineraries.md` |
| 各岛屿及地区的特点 | `regions.md` |
| 根据个人喜好选择住宿方式 | `accommodation.md` |
| 入境与生物安全规划 | `entry-and-biosecurity.md` |
| 有用的应用程序 | `apps.md` |
| **餐饮** | |
| 地方美食与餐厅推荐 | `food-guide.md` |
| 葡萄酒产区与品酒指南 | `wine.md` |
| **体验活动** | |
| 独特体验活动 | `experiences.md` |
| 海滩与沿海活动规划 | `beaches.md` |
| 徒步旅行与安全指南 | `hiking.md` |
| 不同城市类型的夜生活 | `nightlife.md` |
| **参考资料** | |
| 新西兰文化、礼仪与旅行建议 | `culture.md` |
| 季节性因素与旅行策略 | `seasonality.md` |
| 带孩子旅行 | `with-kids.md` |
| 野生动物与户外安全 | `wildlife-safety.md` |
| 官方地图资源 | `sources.md` |
| **实用信息** | |
| 航班、渡轮、火车与驾车出行 | `transport.md` |
| 手机与网络使用 | `telecoms.md` |
| 支付与费用规划 | `payment-and-costs.md` |
| 应急情况与安全措施 | `emergencies.md` |

## 核心规则

### 1. 按岛屿或交通走廊规划行程
不要像规划欧洲旅行那样规划新西兰的行程。对于短途旅行，建议选择单个岛屿或一条主要的交通走廊：
- 北岛北部地区
- 威灵顿及中部高原
- 基督城至麦肯齐和皇后镇
- 尼尔森与阿贝尔塔斯曼地区
- 菲奥德兰与南地地区

### 2. 在确定行程前至少提前一个月了解当地情况
新西兰的旅行计划会随季节变化而调整：
- 夏季：白昼较长，需求量大，道路拥堵
- 冬季：适合滑雪，但日照时间短，山区风险较高
- 非旺季：许多地区的旅行性价比更高
- 菲奥德兰与西海岸的天气可能随时发生变化，影响整个行程计划

### 3. 实际驾驶情况可能与地图显示不同
新西兰的道路状况可能比游客预期的要慢：
- 双车道道路占主导
- 单车道桥梁很常见
- 夜间驾驶较为疲劳
- 山区、雨天或碎石路段会迅速影响行驶时间
- 在乘坐渡轮、飞机或进行米尔福德峡湾一日游前，请预留足够的时间

### 4. 生物安全与安全是必须考虑的因素
在出发前请务必阅读 `entry-and-biosecurity.md`：
- 面包鞋、食物、徒步装备和药品在边境可能会被检查
- 在进行户外活动前，请关注天气预报、冲浪旗信号以及新西兰环境保护部的安全提醒
- 一些热门的徒步路线和露营地可能会提前售罄

### 5. 具体化而非泛化
不要只是简单地说“游览峡湾和葡萄酒庄”。例如：“在菲奥德兰地区，建议将基地设在蒂阿瑙（Te Anau），预订米尔福德峡湾的早晨游轮，并在皇后镇的另一天安排品酒活动。”

### 6. 根据旅行风格选择相关内容
| 旅行类型 | 重点关注内容 |
|----------|----------|
| 美食爱好者 | `food-guide.md`, `wine.md`, `wellington.md` |
| 驾车旅行 | `transport.md`, `regions.md`, `itineraries.md` |
| 徒步与户外活动 | `hiking.md`, `wildlife-safety.md`, `fiordland-southland.md` |
| 家庭旅行 | `with-kids.md`, `accommodation.md`, `rotorua-taupo.md` |
| 城市与自然结合的旅行 | `auckland.md`, `wellington.md`, `christchurch.md` |
| 冒险旅行 | `queenstown.md`, `experiences.md`, `seasonality.md` |

## 常见误区

- 试图在一周内游览两个岛屿。
- 将4小时的驾车行程误认为是无需停留的半天行程。
- 在夏季末期预订皇后镇或菲奥德兰的行程。
- 从长途航班直接驱车前往目的地。
- 仅因为天气看起来平静就认为海滩总是安全的。
- 在没有考虑降雨、风力或徒步路线关闭等意外情况的情况下安排户外活动。
- 忘记了小城镇的营业时间通常比大城市更早结束。

## 安全与隐私

**数据存储位置**：旅行相关偏好信息存储在 `~/new-zealand/` 目录下。

**本技能的限制**：不会访问 `~/new-zealand/` 之外的文件，也不会发起网络请求。

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install travel`：用于旅行规划与行程安排
- `clawhub install booking`：用于预订与时间管理
- `clawhub install car-rental`：用于更好的自驾旅行规划与后勤协调
- `clawhub install food`：用于提供更详细的餐饮推荐
- `clawhub install english`：用于提升沟通效率和预订准确性

## 反馈建议

- 如果觉得本文档有用，请给 `new-zealand` 项目打星评价。
- 如需获取最新信息，请使用 `clawhub sync` 命令更新文档内容。