---
version: 3.1.0
name: aerobase-travel-concierge
description: 全方位的AI旅行管家服务——涵盖航班预订、酒店预订、休息室使用、里程兑换、活动安排以及优惠信息等。由Aerobase提供技术支持。
metadata:
  openclaw:
    requires:
      env:
        - AEROBASE_API_KEY
        - SCRAPLING_URL
    primaryEnv: AEROBASE_API_KEY
    user-invocable: true
    homepage: https://aerobase.app
    source: https://github.com/jetlag-revweb/jetlag-revweb
---
### ⚠️ **透明度声明**

此技能会在您的用户主目录下生成一个用于限制使用频率的JSON文件：
- `~/aerobase-browser-searches.json` - 浏览器搜索次数（每天最多10次）

这些文件仅包含以下内容：
- 操作的日期和次数
- 被查询的网站（针对浏览器搜索）

**数据处理：**
- 仅当用户明确请求时，才会扫描Gmail邮件。
- 除必要信息外，不会向任何外部服务发送个人数据。

**外部服务：**

| 服务 | 发送的数据 | 不发送的数据 |
|---------|-----------|---------------|
| Aerobase API | 带有AEROBASE_API_KEY的API请求 | 无 |
| Scrapling (SCRAPLING_URL) | 用于价格验证的URL | Gmail内容、支付信息、存储的凭证 |

**Scrapling** 是一种用于价格验证和发现优惠信息的隐蔽浏览服务。它可以绕过反机器人系统，从Google Flights、Kayak等网站获取实时价格。

---

# Aerobase旅行管家 ⭐ 一站式服务

您的个人AI旅行助手，永远在线。**这是完整的套餐**——所有Aerobase技能都集成在一个安装包中。

## **优先使用API的原则**

在任何浏览器自动化操作之前，**务必先使用Aerobase API**。API更快、更可靠，且不会触发反机器人系统。

浏览器/爬虫功能仅用于：
- 实时价格验证
- API无法覆盖的网站
- 登机自动化（测试阶段）
- 用户明确请求访问外部网站

---

# ✈️ 航班搜索与预订

## **API端点**

**GET /api/v1/flights/search** — 带时差评分的航班搜索
**POST /api/v1/flights/score** — 为航班选项评分（0-100分）
**POST /api/v1/flights/compare** — 比较多个航班选项

查询参数：`origin`（起点）、`destination`（目的地）、`departure`（出发时间）、`return`（返回时间）、`cabin`（舱位）、`maxPrice`（最高价格）、`limit`（限制数量）

## **示例**
```
POST /api/v1/flights/search
{ "origin": "JFK", "destination": "NRT", "departure": "2026-03-15", "cabin": "business" }
```

返回带有时差评分、恢复建议及相关信息的航班列表。

---

# 🏆 奖励计划搜索

## **API端点**

**POST /api/v1/awards/search** — 搜索24家以上航空公司的会员计划
**GET /api/transfer-bonuses** — 当前的转机奖励信息

查询参数：`origin`（起点）、`destination`（目的地）、`departure`（出发时间）、`return`（返回时间）、`cabin`（舱位）、`maxMiles`（最高里程）

**支持的航空公司：**
Aeromexico、Air Canada、Alaska、Alitalia、All Nippon、American Airlines、Avianca、British Airways、Cathay Pacific、Delta Air Lines、Emirates、Etihad Airways、Flying Blue、Iberia、Japan Airlines、JetBlue、Korean Air、Lufthansa、Qantas、Qatar Airways、Singapore Airlines、Southwest Airlines、United Airlines、Virgin Atlantic

## **CPP计算**

使用Scrapling服务获取每积分的现金价格：
```
POST {SCRAPLING_URL}/search
{"site":"google-flights","origin":"JFK","destination":"LHR","departure":"2026-04-01","return":"2026-04-08"}
```
参考文档：[Scrapling文档](https://scrapling.readthedocs.io/en/latest/overview.html)

---

# 🏧 机场贵宾室

## **API端点**

**GET /api/v1/lounges** — 使用过滤器搜索：`airport`（机场）、`airline`（航空公司）、`network`（航空联盟）、`tier`（贵宾室等级）、`search`（搜索条件）
**GET /api/airports/{code}/lounges** — 某特定机场的贵宾室信息

数据来源于LR（LoungeReview）表格，包含详细信息。

## **与时差相关的字段：**
- **recoveryScore**：1-10分，分数越高，恢复效果越好
- **hasShowers**：布尔值 - 表示航班间可淋浴
- **hasSpa**：布尔值 - 表示提供高级休息设施
- **hasSleepPods**：布尔值 - 表示提供睡眠舱
- **quietZone**：布尔值 - 表示环境适合调整生物钟
- **naturalLight**：布尔值 - 表示环境有助于调整时差

## **Scrapling — Priority Pass使用时间**

用于实时验证Priority Pass的使用时间：
```
web_fetch {SCRAPLING_URL}/fetch?url=https://www.prioritypass.com/lounges/united-states/new-york-ny/jfk-john-f-kennedy-intl&json=1&extract=css&selector=.lounge-card
```
参考文档：[Scrapling文档](https://scrapling.readthedocs.io/en/latest/overview.html)

---

# 🏨 酒店搜索

## **API端点**

**GET /api/v1/hotels** — 使用过滤器搜索：`airport`（机场）、`city`（城市）、`country`（国家）、`chain`（酒店连锁）、`tier`（酒店等级）、`stars`（星级）、`jetlagFriendly`（是否适合时差调整）、`search`（搜索条件）
**GET /api/hotels/near-airport/{code}** — 位于机场附近的酒店

## **过境酒店**

**GET /api/dayuse?airport={code}** — 适用于过境乘客的日租酒店（按天预订，不提供过夜住宿）
**GET /api/hotels?dayuse=true** — 过滤仅适合日租的酒店

对于过境时间超过8小时的乘客，推荐日租酒店。

---

# 🎫 旅行团与活动

## **API端点**

**GET /api/v1/tours** — Viator提供的旅行团和景点信息
查询参数：`airport`（机场）、`destination`（目的地）、`category`（类型）、`duration`（时长）、`priceRange`（价格范围）

## **Scrapling — TripAdvisor发现**

用于补充发现旅行活动信息：
```
web_fetch {SCRAPLING_URL}/fetch?url=https://www.tripadvisor.com/Attractions-g294217-Activities-Tokyo_Tokyo_Prefecture_Kanto.html&json=1&extract=css&selector=.listing_title
```
参考文档：[Scrapling文档](https://scrapling.readthedocs.io/en/latest/overview.html)

---

# 💰 航班优惠

## **API端点**

**GET /api/v1/deals** — 精选航班优惠信息
查询参数：`origin`（起点）、`destination`（目的地）、`maxPrice`（最高价格）、`minScore`（最低评分）、`dateFrom`（开始日期）、`dateTo`（结束日期）、`cabin`（舱位）、`sort`（排序方式）、`limit`（限制数量）

最多返回50个结果（免费会员可查看3个）。

**数据来源：**
优惠信息来自以下网站：SecretFlying、TheFlightDeal、TravelPirates、Going.com

这些数据会定期抓取并存储在我们的数据库中。

## **Scrapling — 优惠验证**

仅用于验证或用户明确请求时使用：
```
POST {SCRAPLING_URL}/search
{"site":"secretflying"}
POST {SCRAPLING_URL}/search
{"site":"google-flights","origin":"JFK","destination":"NRT","departure":"2026-03-15","return":"2026-03-22"}
```
参考文档：[Scrapling文档](https://scrapling.readthedocs.io/en/latest/overview.html)

---

# 💳 积分与钱包

## **API端点**

**GET /api/v1/credit-cards** — 信用卡转账合作伙伴信息
**GET /api/v1/loyalty/balances** — （高级会员）需要扫描Gmail邮件

**Gmail积分扫描（高级会员）**

⚠️ **用户同意要求：** 仅在使用以下功能时才需要用户同意：
1. 用户明确请求“扫描我的Gmail以获取积分”或“显示我的积分余额”
2. 用户已通过Aerobase设置中的OAuth连接Gmail（由Aerobase处理，而非此技能）
3. 严禁主动扫描Gmail邮件——仅在用户请求后进行

**工作原理：**
- 用户通过Aerobase设置中的OAuth连接Gmail。仅提取积分/会员数据，不会共享邮件内容。
- 该技能会调用`GET /api/v1/loyalty/balances`——Aerobase服务器负责处理Gmail API请求
- 返回的仅是积分/会员数量，不会包含邮件内容

---

# 😴 **时差恢复计划（高级会员）**

## **API端点**

**POST /api/v1/recovery/plan** — 生成个性化的恢复计划

所需参数：`flight`（航班信息，包括起点、目的地、出发时间）、`chronotype`（生物钟类型，如earlyBird、nightOwl、neutral）、`tripDuration`（旅行时长）

返回内容：
- 旅行前的准备计划
- 航班中的应对策略
- 每日的恢复时间表
- 光照暴露建议
- 睡眠和饮食调整建议

---

# 🔧 浏览器自动化

**仅在以下情况下使用浏览器：**
- 用户明确要求查询Google Flights、Kayak或Skyscanner
- API搜索无结果且用户希望获取更全面的信息
- 需要价格比较
- 登机自动化（测试阶段）

## **浏览器命令（OpenClaw Playwright-on-CDP）**

- `browser snapshot` — 获取包含`[ref=eN]`元素的ARIA树结构
- `browser type [ref=eN] "value"` — 在输入框中输入内容
- `browser click [ref=eN]` — 点击指定元素
- `browser screenshot` — 截取当前页面截图

## **上下文选择**

| 类型 | 适用场景 |
|------|---------|
| DIRECT | Google Flights、Kayak、Booking.com、Google Hotels、Lufthansa |
| SCRAPLING | Delta Air Lines、British Airways、SecretFlying、seats.aero、Southwest Airlines、Hilton、Hyatt、TripAdvisor、TheFlightDeal、Going.com、SeatGuru、Google Travel |
| PROXY | United Airlines、American Airlines、Air Canada、KLM、TravelPirates |

## **Scrapling服务（反机器人机制）**

当浏览器自动化被反机器人系统（如Akamai、Cloudflare、Datadome）阻止时，使用通过`SCRAPLING_URL`环境变量配置的隐蔽爬虫服务。

参考文档：[Scrapling文档](https://scrapling.readthedocs.io/en/latest/overview.html)

### 获取页面内容
```
web_fetch {SCRAPLING_URL}/fetch?url=https://www.delta.com&json=1
```

### 运行JavaScript
```
POST {SCRAPLING_URL}/evaluate
Body: {"url": "https://seats.aero", "script": "document.title"}
```

### 多步骤交互（表单填写）
```
POST {SCRAPLING_URL}/interact
{
  "url": "https://www.example.com/form/",
  "steps": [
    {"action": "consent"},
    {"action": "fill", "selector": "#confirmationNumber", "value": "<PNR>"},
    {"action": "fill", "selector": "#passengerLastName", "value": "<LAST>"},
    {"action": "click", "selector": "button#form-mixin--submit-button"},
    {"action": "wait", "ms": 5000},
    {"action": "screenshot"}
  ]
}
```

### 数据聚合搜索
```
POST {SCRAPLING_URL}/search
{"site":"google-flights","origin":"LAX","destination":"NRT","departure":"2026-03-15","return":"2026-03-22"}
```

## **使用频率限制**

- 浏览器搜索：用户每天最多10次
- 爬虫：遵循5分钟缓存规则
- API：根据端点不同而有所差异（详见各章节）

---

# 📋 使用频率限制总结

**API调用总计：每天5次**（所有端点共享同一配额）

| 功能 | 说明 |
|---------|-------|
| API调用 | 每天5次（所有端点共享） |
| 浏览器搜索 | 每天10次（记录在`~/aerobase-browser-searches.json`文件中） |

---

# 📁 其他文件

## **辅助脚本（`scripts/`）**
- `browser-tracking.mjs` — 跟踪浏览器搜索次数

## **API参考文档（`references/`）**
- `aerobase-api.md` — 完整的Aerobase API端点参考
- `scrapling.md` — 爬虫服务的相关端点和参数

## **完整文档**
- OpenAPI规范：https://aerobase.app/api/v1/openapi
- Scrapling文档：https://scrapling.readthedocs.io/en/latest/overview.html

---

# 🔒 隐私、安全与凭证

## **所需的环境变量**

| 变量 | 用途 | 提供方式 |
|----------|---------|-------------|
| `AEROBASE_API_KEY` | 访问Aerobase API所需 | 用户从aerobase.app/settings获取 |
| `SCRAPLING_URL` | 隐蔽爬虫服务地址 | 由OpenClaw配置 |
| OAuth tokens | 访问Gmail邮件所需 | 用户通过Aerobase的OAuth连接（不会存储在技能中） |

**注意：** `SCRAPLING_URL`由OpenClaw配置——用户无需自行提供。

## **Gmail OAuth的工作原理**

1. 用户访问https://aerobase.app/settings
2. 点击“连接Gmail”进入Google的OAuth流程
3. 用户仅授权读取积分相关邮件内容
4. Aerobase接收OAuth令牌——令牌由Aerobase存储，不会被此技能使用
5. 该技能调用`GET /api/v1/loyalty/balances`——Aerobase服务器执行Gmail API请求
**注意：** 邮件内容不会离开Aerobase服务器，仅返回积分余额信息

**提取的数据包括：**
- 航空公司/酒店的会员账户信息
- 邮件中提到的积分余额
- 信用卡消费类别

**不会访问的数据：**
- 邮件正文/内容
- 个人消息
- 联系人信息
- 日历记录

## **本地文件存储**

该技能会在用户主目录下生成一个JSON文件来记录使用频率：
- `~/aerobase-browser-searches.json` — 浏览器搜索次数和历史记录

**存储内容：**
- 搜索的日期和次数
- 被查询的网站及时间戳

这些文件仅用于限制使用频率，不会存储任何个人数据。

**用户控制：**
- 用户可以随时通过Google账户设置撤销权限
- 用户断开连接后，Aerobase会删除相关令牌

更多信息请访问：https://aerobase.app/privacy

## **Scrapling服务**

`SCRAPLING_URL`服务由OpenClaw负责管理。它用于：
- 价格验证（如Google Flights、Kayak）
- 优惠信息查询（如SecretFlying、TheFlightDeal）

**发送给Scrapling服务的数据：**
- 该技能请求的URL（用于价格验证或优惠发现）
- 不会包含用户凭证或个人信息

**不用于：**
- 访问Gmail邮件
- 收集支付信息
- 存储用户数据

## **浏览器自动化**

- 用于实时价格验证：从旅行网站获取当前价格
- 不需要用户提供任何凭证

---

**安全与隐私说明：**
- Aerobase隐私政策：https://aerobase.app/privacy
- Aerobase服务条款：https://aerobase.app/terms
- OpenClaw安全政策：https://openclaw.ai/security

---

# 🚀 快速参考

## 常规操作：
1. 首先查询API——更快、更可靠、无限制
2. 立即将API结果展示给用户
3. 仅在执行验证或用户明确请求时使用浏览器/爬虫功能
4. 为结果添加时差评分信息

## **备用方案：**
1. 先尝试API
2. 使用Scrapling服务（无需代理）
3. 使用原生浏览器+代理
4. 如果所有方法均失败，截图并向用户说明情况