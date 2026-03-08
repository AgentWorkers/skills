---
version: 3.1.0
name: aerobase-flight-awards
description: 搜索24家以上的航空公司忠诚度计划，查找可使用的里程数、座位可用性以及时差影响评分（jetlag scores）。
metadata: {"openclaw": {"emoji": "✈️", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---
# Aerobase 航班奖励 ✈️

## 搜索

**POST /api/v1/awards/search** — 查找 seats.aero 的航班奖励信息（缓存数据包含 286,000 多条记录，涵盖 24 家航空公司）  
请求参数：  
`{ origin?: ? (起始城市?), destination?: ? (目的地?), program?: ? (航空公司?), cabin?: ? (舱位类型?), dateFrom?: ? (出发日期?), dateTo?: ? (到达日期?), minScore?: ? (最低分数要求?) }`  
返回结果：  
`jetlagScore`（0-10 分，K2 奖励的分数需乘以 10），`k2CabinScore`，`k2BaseScore`，`milesCost`（里程费用），`remaining_seats`（剩余座位数），`transfer_options`（转机选项）。  
舱位类型包括：economy（经济舱）、business（商务舱）、premium（豪华舱）、first-class（头等舱）（返回的是舱位的全称，而非代码）。  

## 通知  

- **POST /api/awards/alerts** — 创建航班奖励通知  
- **GET /api/awards/alerts** — 查看用户的航班奖励通知列表  
- 持续接收通知需要使用 Pro 级账户。  

## 航空公司信息  

目前支持 24 家航空公司：Copa、Aeromexico、Ethiopian、United、Delta、American、BA、Lufthansa、AF/KLM 等。  
系统会自动将用户的信用卡信息与航空公司的转机合作伙伴信息进行匹配。  

## 常见提示：  

- 所有价格均以里程或积分的形式显示，而非现金价格。  
- 每个搜索结果都会附带时差评分（jetlag score）。  
- 对于 BA、LH、AF 等航空公司的奖励，系统会提醒乘客注意燃油附加费。  
- 计算每积分的现金价值示例：  
  “从商务舱飞往东京需要 75,000 Aeroplan 积分，现金价格为 3,200 美元，即每积分 0.9 美分——性价比极高。”  
- 在比较现金与积分时，系统会提示：  
  “经济舱虽然可节省 50,000 英里，但航班起飞时间为晚上 11 点，会导致四天的疲劳状态；而商务舱则能让你高效工作三天。”  

## 速率限制：  

- 每小时最多搜索 20 次航班奖励信息。  
- 每个用户最多可创建 10 条航班奖励通知。  
- 航班奖励信息更新频率为每 4 小时一次（建议批量查询航线信息）。  

## 数据抓取（用于计算每积分的现金价值）  

使用 `/search` 接口从 Google Flights 获取航班的现金价格，以计算每积分的现金价值：  
[参考文档：](https://scrapling.readthedocs.io/en/latest/overview.html)  

**返回示例：**  
`{"results": [{"price": "€488", "duration": "6 小时 50 分", "stops": "直飞"}], "count": 48}`  

### 每积分的现金价值（CPP）计算流程：  
1. 从 seats.aero API 获取航班奖励的现金价格（例如：60,000 Aeroplan 积分）。  
2. 使用 Scrapling 技术从 Google Flights 获取相同航线的现金价格（单位：欧元，必要时转换为美元）。  
3. 计算公式：`cash_price_usd / miles_required * 100 = cents_per_point`。  
4. 显示结果：  
  “从商务舱飞往伦敦需要 60,000 Aeroplan 积分，现金价格为 543 美元，即每积分 0.9 美分。”  

### seats.aero 的使用建议：  
- 首选使用 seats.aero API；浏览器访问需通过代理服务器（PROXY）。  
- seats.aero 采用 Cloudflare 保护机制，建议优先使用 API；仅限已登录用户通过浏览器访问。  

### 航空公司奖励信息的获取（需使用代理服务器）：  
- 访问航空公司的 FFP（Frequent Flyer Program）预订页面（需要登录）。  
- 用户必须提供自己的账户凭证，切勿存储或泄露这些凭证。  

## 何时完全放弃使用浏览器：  
- 一般航班奖励搜索：优先使用 seats.aero API 的缓存数据。  
- 航班奖励通知：API 会自动处理相关通知。  
- 航空公司信息比较：API 提供的数据已足够使用。  
- 仅在需要查看航班信息或查询现金价格时使用浏览器。