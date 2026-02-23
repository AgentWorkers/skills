---
name: tfl
description: 伦敦交通局（TfL）的公共交通服务——提供伦敦地铁（London Underground）、DLR（District Line Railway）、地面公交（Overground）、伊丽莎白线（Elizabeth Line）以及公交车的实时到站信息、线路状态、服务中断情况、出行规划及路线详情。当用户咨询伦敦公共交通、地铁时刻表、公交车到站时间或TfL的服务状态时，可参考该信息。
homepage: "https://github.com/brianleach/tfl-skill"
license: MIT
metadata:
  openclaw:
    emoji: "\U0001F1EC\U0001F1E7"
    tags: [transit, london, tfl, transportation, tube, underground, bus, train, schedule]
    primaryEnv: TFL_API_KEY
    requires:
      bins: ["node"]
    files: ["scripts/tfl.mjs"]
---
# 伦敦交通（TfL）实时信息

提供伦敦交通系统的实时数据，包括地铁到站时间、公交车预测、线路状态、交通延误以及出行规划信息。所有数据均通过TfL统一的REST API获取。API密钥为可选（免费提供，但建议使用以提升请求速率限制）。

## 使用场景

- 当用户询问关于地铁（London Underground）、TfL或伦敦公共交通系统的相关信息时
- 当用户提及具体的地铁线路（如Bakerloo、Central、Circle、District、Hammersmith & City、Jubilee、Metropolitan、Northern、Piccadilly、Victoria、Waterloo & City等）
- 当用户询问“Northern线路是否正常运行”或“下一班地铁何时到达”时
- 当用户提到伦敦的地铁站（如King's Cross、Oxford Circus、Waterloo、Victoria、Paddington等）
- 当用户询问关于伦敦公交车、DLR（Docklands Light Railway）、Overground、Elizabeth线路或电车的相关信息时
- 当用户询问TfL的服务状态、延误情况或计划中的线路关闭信息时
- 当用户询问关于Oyster卡、非接触式支付方式或TfL票价的信息时
- 当用户需要规划在伦敦的出行路线时

## 数据来源

TfL提供了一个**统一的REST API**（`api.tfl.gov.uk`），该API可为所有交通方式返回JSON格式的数据（包括地铁、公交车、DLR、Overground、Elizabeth线路、电车等）。该API不支持protobuf格式，也不提供SIRI接口或多种数据格式选项，仅提供简洁一致的JSON响应。

**API密钥：**请访问[https://api-portal.tfl.gov.uk/](https://api-portal.tfl.gov.uk/)注册免费的`app_key`，并在请求中添加`?app_key={KEY}`。虽然不使用API密钥也可以进行基本操作，但会受到请求速率限制；使用密钥后，每分钟可发送500个请求。

### 主要API端点

| 端点          | 描述                                      |
|-----------------|-----------------------------------------|
| `/Line/Mode/tube/Status`   | 所有地铁线路的状态                        |
| `/Line/{lineId}/Status`    | 特定地铁线路的状态                        |
| `/StopPoint/{naptanId}/Arrivals` | 某地铁站的到站信息                        |
| `/Line/{lineId}/Arrivals/{stopPointId}` | 按线路筛选的到站信息                        |
| `/StopPoint/Search/{query}`   | 按名称搜索地铁站                          |
| `/StopPoint?lat=&lon=&radius=` | 根据地理位置搜索地铁站                        |
| `/Line/{lineId}/StopPoints`    | 某地铁线路上的所有地铁站                        |
| `/Line/{lineId}/Route/Sequence/{dir}` | 某地铁线路的站点顺序                        |
| `/Line/{lineId}/Disruption`   | 某地铁线路的交通延误情况                        |
| `/Journey/JourneyResults/{from}/to/{to}` | 出行规划服务                          |
| `/Line/Mode/bus`     | 所有公交线路的信息                        |

所有端点返回的均为JSON格式的数据。如需认证请求，请在URL后添加`?app_key={KEY}`。

## 实现方式

### 快速入门：使用辅助脚本

本技能中的`scripts/`目录包含用于获取、解析和展示TfL数据的辅助脚本。

### 脚本：`scripts/tfl.mjs`

该脚本是主要的数据处理入口，支持以下功能：

```bash
# Tube line status
node scripts/tfl.mjs status
node scripts/tfl.mjs status --all
node scripts/tfl.mjs status --line victoria

# Arrivals at a station
node scripts/tfl.mjs arrivals --station "Oxford Circus"
node scripts/tfl.mjs arrivals --stop 940GZZLUOXC
node scripts/tfl.mjs arrivals --stop-search "kings cross"
node scripts/tfl.mjs arrivals --stop-search "kings cross" --line piccadilly

# Bus arrivals
node scripts/tfl.mjs bus-arrivals --stop 490005183E
node scripts/tfl.mjs bus-arrivals --stop-search "oxford circus"
node scripts/tfl.mjs bus-arrivals --stop-search "oxford circus" --route 24

# Disruptions
node scripts/tfl.mjs disruptions
node scripts/tfl.mjs disruptions --line northern

# Routes and stops
node scripts/tfl.mjs routes
node scripts/tfl.mjs routes --all
node scripts/tfl.mjs bus-routes
node scripts/tfl.mjs stops --search "waterloo"
node scripts/tfl.mjs stops --near 51.5074,-0.1278 --radius 500
node scripts/tfl.mjs stops --line victoria
node scripts/tfl.mjs route-info --line bakerloo
node scripts/tfl.mjs route-info --route 24

# Journey planning
node scripts/tfl.mjs journey --from "waterloo" --to "kings cross"
node scripts/tfl.mjs journey --from "51.5031,-0.1132" --to "51.5308,-0.1238"
```

### 设置：API密钥（可选，推荐使用）

即使不使用API密钥，基本功能也能正常使用（但会受到速率限制）。如需每分钟发送500个请求，请按照以下步骤操作：
1. 在[https://api-portal.tfl.gov.uk/](https://api-portal.tfl.gov.uk/)注册并获取`app_key`。
2. 将`TFL_API_KEY`设置为环境变量。

### 地铁线路参考

| 线路ID | 线路名称 | 表示符号 | 起终点站                          |
|---------|---------|---------|-----------------------------------------|
| bakerloo | Bakerloo   | brown     | Harrow & Wealdstone ↔ Elephant & Castle         |
| central | Central | red     | Epping / Ealing Broadway ↔ West Ruislip         |
| circle | Circle   | yellow     | Hammersmith (环线，途经Liverpool Street)       |
| district | District | green     | Richmond / Ealing Broadway ↔ Upminster         |
| hammersmith-city | Hammersmith & City | pink     | Hammersmith ↔ Barking                   |
| jubilee | Jubilee | silver    | Stanmore ↔ Stratford                   |
| metropolitan | Metropolitan | magenta   | Chesham / Amersham / Uxbridge ↔ Aldgate        |
| northern | Northern | black     | Edgware / High Barnet ↔ Morden / Battersea         |
| piccadilly | Piccadilly | dark blue  | Heathrow T5 / Uxbridge ↔ Cockfosters         |
| victoria | Victoria | light blue  | Walthamstow Central ↔ Brixton                |
| waterloo-city | Waterloo & City | teal     | Waterloo ↔ Bank                        |

### 其他TfL铁路线路

| 线路ID | 线路名称 | 类型                          |
|---------|---------|-----------------------------------------|
| dlr     | DLR     | Docklands Light Railway                 |
| liberty   | Liberty   | Overground (Romford — Upminster)             |
| lioness   | Lioness   | Overground (Watford — Euston)                 |
| mildmay   | Mildmay   | Overground (Stratford — Richmond/Clapham)         |
| suffragette | Suffragette | Overground (Gospel Oak — Barking)             |
| weaver   | Weaver   | Overground (Liverpool St — Enfield/Chingford)         |
| windrush  | Windrush  | Overground (Highbury — Crystal Palace/Clapham/W Croydon)     |
| elizabeth | Elizabeth | Crossrail                         |
| tram     | London Trams | Croydon Tramlink                     |

### TfL票价参考（自2025年3月起）

| 票价类型 | 价格                          |
|---------|-----------------------------------------|
| 地铁1区（Oyster/非接触式支付，高峰时段） | £2.80                          |
| 地铁1区（Oyster/非接触式支付，非高峰时段） | £2.70                          |
| 地铁1-2区（高峰时段） | £2.80                          |
| 地铁1-2区（非高峰时段） | £2.70                          |
| 地铁1-3区（高峰时段） | £3.50                          |
| 地铁1-3区（非高峰时段） | £2.80                          |
| 公交车/电车（任意路线） | £1.75                          |
| 1小时内无限次公交/电车票       | 总价£1.75                          |
| 1-2区每日票价上限     | £8.90                          |
| 1-2区每周票价上限     | £44.70                          |
| 现金单程票（自动售货机） | £6.70（仅限1区）                        |

**高峰时段**：周一至周五的早上6:30-9:30及下午4:00-7:00（公共假期除外）。

### 用户使用提示

- **NaPTAN ID**是地铁站的唯一标识符，采用`940GZZLU{code}`格式。
- 使用`--station`或`--stop-search`可按名称查询地铁站；使用`--stop`可查询具体的NaPTAN ID。
- 时间采用24小时制显示（符合伦敦的惯例）。
- `arrivals`命令会使用TfL API提供的`timeToStation`函数（以秒为单位）来计算预计到站时间。
- 公交车站有自己的NaPTAN ID，格式为`490{code}`。
- 出行规划功能会提供票价估算（如数据可用）。

### 错误处理

- 如果未设置`TFL_API_KEY`，请求仍可执行，但会受到速率限制，并会显示提示信息。
- 当遇到429错误（表示请求速率限制）时，系统会提供注册API密钥的链接。
- 对无效的地铁站/车站查询，系统会显示“未找到匹配的站点”并给出建议。
- 网络错误或API错误会显示友好的提示信息。
- 如果车站关闭或暂停服务，系统会显示相应的提示信息。

### 数据展示方式

在向用户展示交通信息时：
- 首先提供最实用的信息（如下一班车的到站时间、线路状态）。
- 使用颜色符号表示线路名称（例如：“🔴 Central：服务正常”）。
- 时间采用24小时制显示（符合伦敦的惯例）。
- 对于到站信息，会显示线路名称、目的地及预计到站时间（通过`timeToStation / 60`计算）。
- 如有平台信息，也会一并显示。
- 对于出行规划，会详细列出出行方式、线路、行驶时间及票价。
- 对于查询的线路，会明确标注是否存在交通延误。

## 外部API接口

| 端点          | 发送的数据                   | 接收的数据                         |
|-----------------|-----------------------------|-----------------------------------------|
| `api.tfl.gov.uk/Line/*/Status` | API密钥（可选参数） | 线路状态（JSON格式）                     |
| `api.tfl.gov.uk/StopPoint/*/Arrivals` | API密钥（可选参数） | 地铁站到站信息（JSON格式）                   |
| `api.tfl.gov.uk/StopPoint/Search/*` | API密钥（可选参数） | 地铁站搜索结果（JSON格式）                   |
| `api.tfl.gov.uk/StopPoint?lat=&lon=` | API密钥（可选参数） | 附近地铁站信息（JSON格式）                   |
| `api.tfl.gov.uk/Line/*/StopPoints` | API密钥（可选参数） | 某地铁线路上的所有地铁站信息（JSON格式）             |
| `api.tfl.gov.uk/Line/*/Route/Sequence/*` | API密钥（可选参数） | 某地铁线路的站点顺序（JSON格式）                 |
| `api.tfl.gov.uk/Line/*/Disruption` | API密钥（可选参数） | 某地铁线路的交通延误情况（JSON格式）                 |
| `api.tfl.gov.uk/Journey/JourneyResults/*` | API密钥（可选参数） | 出行规划结果（JSON格式）                     |
| `api.tfl.gov.uk/Line/Mode/bus` | API密钥（可选参数） | 公交线路信息（JSON格式）                     |

API密钥作为查询参数传递给TfL的官方API。不会传输任何用户个人信息。

## 安全与隐私声明

- **API密钥为可选**：TfL的统一API支持无需密钥的使用（但会有速率限制）；使用免费密钥后，每分钟可发送500个请求。
- **不传输用户数据**：请求内容仅包含API密钥以及线路/车站标识符，不包含任何个人信息。
- **无本地数据存储**：该技能不会在磁盘上保存任何文件（无需GTFS缓存，所有数据均来自实时API）。
- **无数据传输**：该技能不会向第三方发送任何数据。
- **输入处理**：用户输入的站点名称和线路ID会在API请求中经过URL编码，不会被用于其他用途。

## 信任声明

本技能从TfL的官方统一API中获取公开可用的交通数据。API密钥仅用于验证请求权限，不会访问、存储或传输用户的任何个人信息。