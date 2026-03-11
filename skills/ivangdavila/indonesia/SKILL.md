---
name: Indonesia
slug: indonesia
version: 1.0.0
homepage: https://clawic.com/skills/indonesia
changelog: "Initial release with Indonesia entry guidance, island-routing playbooks, and practical travel logistics."
description: 使用岛屿导航逻辑规划印度尼西亚的旅行路线，提供经过验证的入境指南，考虑天气因素的物流安排，以及实用的当地执行方案。
metadata: {"clawdbot":{"emoji":"🇮🇩","requires":{"bins":[],"config":["~/indonesia/"]},"os":["linux","darwin","win32"]}}
---
## 设置（Setup）

如果 `~/indonesia/` 目录不存在或为空，请先阅读 `setup.md` 文件，然后按照其中的指导进行操作。

## 适用场景（When to Use）

当用户计划前往印度尼西亚旅行时，本文档提供了超出常规旅行信息的实用指导，包括签证申请流程、岛屿选择、路线规划、适合冲浪和天气的条件、交通方式的选择，以及在广阔群岛中的实际出行建议。

## 架构（Architecture）

所有与印度尼西亚旅行相关的数据和文件都存储在 `~/indonesia/` 目录下。具体激活流程请参考 `setup.md`，文件结构请参见 `memory-template.md`。

```text
~/indonesia/
└── memory.md     # Trip context and evolving constraints
```

## 快速参考（Quick Reference）

使用以下表格来快速查找与当前旅行决策相关的印度尼西亚旅行信息：

| 旅行主题 | 对应文件 |
|---------|---------|
| **入境与到达** | `entry-and-documents.md` |
| 签证、VOA（签证豁免）、后续出行证明、停留限制 | <br>《入境与文件准备》（Entry and Documents） |
| 海关、电子护照（e-CD）、机场抵达、首日安排 | `customs-and-arrival.md` |
| **旅行规划基础** | <br>《地区与路线策略》（Regions and Route Strategies） |
| 样例行程安排 | `itineraries.md` |
| 根据旅行路线选择住宿地点 | `accommodation.md` |
| 预算规划 | `budget-and-costs.md` |
| 信用卡、现金及支付方式 | `payments-and-money.md` |
| **交通方式** | <br>《国内交通指南》（Transport Domestic） |
| 驾车或使用摩托车出行时的风险 | `road-trips-and-driving.md` |
| **目的地攻略** | <br>《巴厘岛、乌鲁瓦图、乌布德、仓古岛》（Bali and Nusa Islands） |
| 《雅加达、万隆及西爪哇地区》（Jakarta and West Java） |
| 《日惹、婆罗浮屠与普兰巴南》（Yogyakarta and Central Java） |
| 《东爪哇、布罗莫岛与伊真火山》（East Java and Bromo-Ijen） |
| 《龙目岛、吉利群岛及宁静的海滩》（Lombok and Gili Islands） |
| 《科莫多岛、弗洛雷斯岛与拉布安巴霍》（Komodo and Flores） |
| 《苏门答腊岛与猩猩或火山景点》（Sumatra and Volcanoes） |
| **生活方式与旅行准备** | <br>《各岛屿的食物与餐饮文化》（Food Guide） |
| 不同目的地的夜生活体验 | `nightlife.md` |
| 带着儿童或年长亲属旅行 | `family-travel.md` |
| 旅行中的无障碍出行与适应性策略 | `accessibility.md` |
| **安全与旅行注意事项** | <br>《紧急情况处理、健康风险、诈骗防范、火山与海洋安全》（Safety and Emergencies） |
| 气候、季风时间与季节性因素 | `weather-and-seasonality.md` |
| **旅行工具** | <br>《通讯与实用应用程序》（Telecoms and Apps） |
| 官方旅行地图资源 | `sources.md` |

## 核心规则（Core Rules）

### 1. 根据岛屿和交通便利性选择行程路线，而非仅凭风景图片决定
印度尼西亚的交通网络较为复杂，建议用户每周集中游览一个主要岛屿群：
- 巴厘岛 + 尼萨群岛或巴厘岛 + 龙目岛
- 爪哇岛（包括日惹和东爪哇地区）
- 弗洛雷斯岛与科莫多岛
- 苏门答腊岛的野生动物与火山景点

### 2. 先确保入境流程畅通
在推荐不可退费的航班之前，请务必阅读 `entry-and-documents.md` 文件。免签政策、VOA（签证豁免）、后续出行证明的要求、护照有效期以及巴厘岛的相关费用等因素都可能影响旅行的安全性。

### 3. 根据用户需求选择合适的岛屿，而非盲目跟风
了解用户的真实需求：
- 首次旅行或希望行程简单便利
- 希望有充足的冲浪和海滩时间
- 对潜水或乘船旅行感兴趣
- 对当地文化和寺庙感兴趣
- 希望探索火山与徒步旅行
- 考虑家庭旅行的需求
- 偏好低摩擦度、舒适的旅行体验或偏远自然风光

### 4. 在制定计划时考虑季节因素
在确定旅行岛屿、乘船日期、潜水行程或火山游览时间之前，请务必参考 `weather-and-seasonality.md` 文件。印度尼西亚的天气因地区而异，海况与降雨情况同样重要。

### 5. 正视乘船、摩托车出行及高海拔地区的风险
不要过分依赖快速船只或摩托车：
- 当天连续乘坐船只和航班的行程安排较为脆弱
- 对初学者的摩托车使用建议往往并不合适
- 高温、脱水、高海拔、崎岖的道路以及医疗设施的缺乏都可能影响旅行体验

### 6. 根据实际群岛情况制定预算
在制定预算时，应考虑整个行程的总体费用，而不仅仅是别墅的价格：
- 国内航班的行李费用
- 船票及港口转乘费用
- 驾驶员的劳务费用及机场相关费用
- 旅游税、签证费、公园门票及向导费用
- 在主要交通枢纽以外的地区仅使用现金的必要性

### 7. 提供详细的操作性计划
所有旅行计划应包含以下内容：
- 基本旅行逻辑及需要跳过的环节
- 每日的行程安排及实际的交通时间窗口
- 需要提前预订的物品或服务
- 针对不同天气或海况的备用方案
- 选定路线的安全、支付及出行注意事项

## 常见误区（Common Traps）

- 将印度尼西亚简化为“只有巴厘岛或其他几个地方”，而忽略了其复杂的地理和交通条件。
- 尝试在同一趟旅行中同时游览巴厘岛、日惹、科莫多岛、吉利群岛和苏门答腊岛。
- 误以为所有地方的信用卡、ATM机、网络服务、人行道和英语交流都同样适用。
- 在没有预留缓冲时间的情况下预订快速船只或航班。
- 未提前考虑楼梯、道路状况、高温环境或医疗支持，便安排家庭或年长旅客前往尼萨佩尼达岛、布罗莫岛或科莫多岛。
- 对整个印度尼西亚的天气情况一概而论。
- 为疲劳、缺乏经验的旅客或雨季旅行者默认推荐使用摩托车。

## 安全与隐私（Security & Privacy）

**数据存储位置**：所有旅行相关数据仅存储在 `~/indonesia/` 目录内。

**本技能的限制**：**仅允许在 `~/indonesia/` 目录内访问文件，且不进行任何网络请求。**

## 相关技能（Related Skills）

如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：用于安装旅行规划、预订流程、餐厅推荐、数据设置及语言支持等工具：
  - `travel`：通用旅行规划与行程安排
  - `booking`：预订流程与确认机制
  - `food`：餐厅与美食信息
  - `esim`：抵达前的移动数据准备
  - `indonesian`：旅行过程中的语言支持

## 反馈建议（Feedback）

- 如果本文档对您有帮助，请给 `clawhub` 评分（例如：`clawhub star indonesia`）。
- 为了获取最新信息，请定期执行 `clawhub sync` 命令。