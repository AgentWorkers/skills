---
name: cta
description: 芝加哥CTA公共交通系统——提供L线列车的实时到站信息、公交车到站预测、服务公告以及路线详情。当用户询问有关芝加哥公共交通系统、L线列车时刻表、CTA公交车时刻、服务公告或附近车站的信息时，可以使用该资源。
homepage: "https://github.com/brianleach/cta-skill"
license: MIT
metadata:
  clawhub:
    emoji: "🚇"
    tags: [transit, chicago, cta, transportation, bus, train, l-train, schedule]
    requires:
      bins: ["node", "unzip"]
      env: ["CTA_TRAIN_API_KEY", "CTA_BUS_API_KEY"]
    files: ["scripts/cta.mjs"]
    install:
      - id: npm-deps
        kind: shell
        command: "npm install --prefix $SKILL_DIR"
        label: "Install Node.js dependencies"
---
# CTA芝加哥交通（CTA Chicago Transit）

实时芝加哥CTA交通信息——L线列车到站时间、公交车预测、服务提醒以及路线信息。获取列车和公交车数据需要免费的API密钥；服务提醒功能无需密钥即可使用。

## 使用场景

- 用户咨询关于CTA、L线列车、蓝线（Blue Line）、红线（Red Line）、棕线（Brown Line）或任何芝加哥地铁线路的信息
- 用户询问芝加哥公交路线、公交追踪器或列车追踪器的使用方法
- 用户询问“下一班列车何时到站”或“红线是否在运行”
- 用户提到具体的CTA车站（如奥黑尔（O'Hare）、米德韦（Midway）、克拉克/莱克（Clark/Lake）、贝尔蒙特（Belmont）等
- 用户询问CTA票价、Ventra支付方式或如何乘坐芝加哥公共交通工具
- 用户询问CTA的服务提醒、延误情况或绕行信息
- 用户询问芝加哥附近的公交车站或路线信息

## 数据来源

CTA使用3个专有的REST API。列车追踪器（Train Tracker）和公交车追踪器（Bus Tracker）需要免费的API密钥，而服务提醒功能（Customer Alerts）则无需密钥即可访问。

### 列车追踪器API（需要`CTA_TRAIN_API_KEY`）

免费获取API密钥的链接：https://www.transitchicago.com/developers/traintrackerapply/

| API端点 | 功能描述 |
|----------|-------------|
| 按车站查询列车到站时间 (`mapid`) | 查看指定车站的列车到站信息 |
| 按车站查询列车到站时间 (`stpid`) | 查看特定车站的列车到站信息 |
| 列车实时位置 (`rt`) | 获取线路上所有列车的实时位置 |
| 跟踪特定列车行程 (`runnumber`) | 跟踪特定列车的运行情况 |

数据更新频率约为每分钟一次。每个密钥的每日请求限制为50,000次。

### 公交车追踪器API v2（需要`CTA_BUS_API_KEY`）

免费获取API密钥的链接：https://www.transitchicago.com/developers/bustracker/

| API端点 | 功能描述 |
|----------|-------------|
| 按车站预测公交车到站时间 | 预测公交车在特定车站的到站时间 |
| 预测特定公交车的行驶情况 | 预测特定公交车的行驶情况 |
| 公交车实时位置 | 获取公交车的实时位置 |
| 路线列表 | 所有运营中的公交路线 |
| 路线方向 | 提供路线的行驶方向信息 |
| 路线上的车站 | 列线上的所有车站信息 |

公交车数据更新频率约为每30秒一次。

### 服务提醒API（无需密钥）

| API端点 | 功能描述 |
|----------|-------------|
| 路线状态 | 查看所有路线的当前状态 |
| 所有服务提醒 | 查看所有有效的服务提醒 |
| 按路线筛选提醒 | 根据路线筛选服务提醒 |
| 按车站筛选提醒 | 根据车站筛选服务提醒 |

### GTFS静态数据源

| 数据源 | 格式 | 链接 |
|------|--------|-----|
| GTFS静态数据（ZIP格式） | ZIP | `https://www.transitchicago.com/downloads/sch_data/google_transit.zip` |

用于获取车站名称、路线信息和时刻表。所有API使用相同的车站ID。

## 实现方式

### 快速入门：使用辅助脚本

位于`scripts/`目录中的脚本负责获取、解析和展示CTA数据。

### 脚本：`scripts/cta.mjs`

该脚本是主要入口文件，支持以下命令：

```bash
# L train arrivals
node scripts/cta.mjs arrivals --station "Clark/Lake"
node scripts/cta.mjs arrivals --mapid 40380
node scripts/cta.mjs arrivals --stop 30070
node scripts/cta.mjs arrivals --stop-search "ohare"
node scripts/cta.mjs arrivals --stop-search "belmont" --route Red

# Bus predictions
node scripts/cta.mjs bus-arrivals --stop 456
node scripts/cta.mjs bus-arrivals --stop 456 --route 22
node scripts/cta.mjs bus-arrivals --stop-search "michigan"

# Vehicle tracking
node scripts/cta.mjs vehicles --route Red
node scripts/cta.mjs bus-vehicles --route 22

# Service alerts
node scripts/cta.mjs alerts
node scripts/cta.mjs alerts --route Red

# Routes and stops
node scripts/cta.mjs routes
node scripts/cta.mjs bus-routes
node scripts/cta.mjs stops --search "belmont"
node scripts/cta.mjs stops --near 41.8781,-87.6298 --radius 0.3
node scripts/cta.mjs route-info --route Red
node scripts/cta.mjs route-info --route 22

# Maintenance
node scripts/cta.mjs refresh-gtfs
```

### 设置：API密钥

列车和公交车相关的命令需要免费的API密钥：

1. **列车追踪器密钥：** 在https://www.transitchicago.com/developers/traintrackerapply/申请
2. **公交车追踪器密钥：** 在https://www.transitchicago.com/developers/bustracker/申请
3. 设置环境变量：`CTA_TRAIN_API_KEY` 和 `CTA_BUS_API_KEY`

服务提醒相关的命令无需密钥即可使用。

### 设置：GTFS静态数据

首次使用时，运行`node scripts/cta.mjs refresh-gtfs`命令以下载并提取GTFS静态数据（路线、车站、时刻表），并将其保存到`~/.cta/gtfs/`目录。只需在CTA更新时刻表时重新下载这些数据。

### L线列车路线参考

| 路线代码 | 路线名称 | 起止站点 |
|-----------|------|-----------|
| Red | 红线 | 奥黑尔（O'Hare） ↔ 第95街/丹·瑞安（95th/Dan Ryan） |
| Blue | 蓝线 | 奥黑尔（O'Hare） ↔ 森林公园（Forest Park） |
| Brn | 棕线 | 金博尔（Kimball） ↔ 环线（Loop） |
| G | 绿线 | 哈莱姆/莱克（Harlem/Lake） ↔ 阿什兰/第63街或科蒂奇格罗夫（Ashland/63rd or Cottage Grove） |
| Org | 橙线 | 米德韦（Midway） ↔ 环线（Loop） |
| P | 紫线 | 林登（Linden） ↔ 奥黑尔（Howard）（工作日快线） |
| Pink | 粉线 | 第54街/瑟马克（54th/Cermak） ↔ 环线（Pink Line） |
| Y | 黄线 | 登普斯特-斯科基（Dempster-Skokie） ↔ 奥黑尔（Yellow Line） |

### 主要公交路线参考

| 路线代码 | 路线名称 | 说明 |
|-------|------|-------|
| 22 | 克拉克（Clark） | 主要的南北向公交线路 |
| 36 | 百老汇（Broadway） | 北区湖滨线路 |
| 77 | 贝尔蒙特（Belmont） | 主要的东西向公交线路 |
| 151 | 谢里登（Sheridan） | 湖滨快线 |
| 146 | 内环大道/密歇根快线（Inner Drive/Michigan Express） | 环线至北湖滨 |
| 8 | 哈尔斯特德（Halsted） | 长距离的南北向公交线路 |
| 9 | 阿什兰（Ashland） | 主要的南北向公交线路 |
| 49 | 西部（Western） | 系统中最长的公交线路 |
| 66 | 芝加哥（Chicago） | 主要的东西向公交线路 |
| 79 | 第79街（79th） | 南区的东西向公交线路 |

### CTA票价参考（2026年）

| 车票类型 | 价格 |
|-----------|-------|
| 常规票（Ventra/非接触式支付） | $2.50 |
| 公交转乘 | $0.25 |
| 地铁转公交 | 2小时内免费转乘 |
| 优惠票 | $1.25 |
| 1天通票 | $5.00 |
| 3天通票 | $15.00 |
| 7天通票 | $20.00 |
| 30天通票 | $75.00 |

支持使用Ventra卡、Ventra应用程序或非接触式银行卡支付。转乘优惠有效期为2小时。

### 用户提示

- **车站ID** 以4xxxx开头（代表起始车站）；**车站名称** 以3xxxx开头（代表具体车站）
- 使用`--station`或`--stop-search`进行基于名称的查询；使用`--mapid`进行精确车站查询
- **服务提醒** 始终可用——无需API密钥——因此如果发现异常，请先查看服务提醒
- 列车数据更新频率约为每分钟一次；公交车数据更新频率约为每30秒
- 对于环线（Loop），列车可能显示为从不同方向到达

### 错误处理

- 如果未设置`CTA_TRAIN_API_KEY`，列车相关命令会显示注册链接以帮助用户获取密钥
- 如果未设置`CTA_BUS_API_KEY`，公交车相关命令会显示注册链接以帮助用户获取密钥
- 服务提醒相关命令始终可用（无需密钥）
- 如果输入的车站/车站名称无效，系统会显示“未找到匹配的车站”并给出建议
- 网络错误或API响应错误会显示友好的提示信息

### 响应格式

在向用户展示交通信息时：
- 首先提供最实用的信息（如下一班列车到站时间、当前服务提醒）
- 时间以12小时制显示（包含AM/PM）
- 显示线路颜色和目的地（例如：“红线前往第95街/丹·瑞安”）
- 对于列车：即将到站的列车显示“Due”，即将到达的列车显示预计到达时间（分钟）
- 对于公交车预测，显示预计到达时间（分钟）
- 如果查询的路线有服务提醒，务必提及这些提醒

## 外部API接口

| API接口 | 发送的数据 | 接收的数据 |
|----------|-----------|---------------|
| `https://lapi.transitchicago.com/api/1.0/ttarrivals.aspx` | API密钥（查询参数，HTTPS） | 列车到站信息（JSON） |
| `https://lapi.transitchicago.com/api/1.0/ttpositions.aspx` | API密钥（查询参数，HTTPS） | 列车实时位置（JSON） |
| `https://lapi.transitchicago.com/api/1.0/ttfollow.aspx` | API密钥（查询参数，HTTPS） | 列车行程详情（JSON） |
| `https://www.ctabustracker.com/bustime/api/v2/*` | API密钥（查询参数，HTTPS） | 公交车预测/实时位置（JSON） |
| `https://www.transitchicago.com/api/1.0/routes.aspx` | 无（仅GET请求） | 路线状态（JSON） |
| `https://www.transitchicago.com/api/1.0/alerts.aspx` | 无（仅GET请求） | 服务提醒（JSON） |
| `https://www.transitchicago.com/downloads/sch_data/google_transit.zip` | 无（仅GET请求） | GTFS静态数据（ZIP格式） |

所有API请求均使用HTTPS协议。API密钥作为查询参数传递给CTA的官方API，不会传输任何用户数据。

## 安全与隐私

- **需要API密钥**：列车和公交车追踪器API需要免费的开发者密钥作为URL查询参数
- **不传输用户数据**：请求仅包含API密钥和路线/车站标识符，不包含个人信息
- **仅本地缓存**：GTFS静态数据会缓存到`~/.cta/gtfs/`目录，不会写入其他地方
- **无数据传输**：该技能不会发送任何使用数据
- **输入处理**：用户输入的车站名称和路线ID仅用于本地过滤，不会用于执行shell命令

## 信任声明

该技能从CTA的官方API获取公开可用的交通数据。API密钥仅用于CTA API的认证。该技能不会访问、存储或传输用户配置的API密钥之外的任何个人信息。