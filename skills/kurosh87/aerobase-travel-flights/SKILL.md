---
version: 3.1.0
name: aerobase-travel-flights
description: 搜索、比较航班，并根据时差因素对航班进行评分。支持通过 Kiwi 和 Duffel API 进行预订。
metadata: {"openclaw": {"emoji": "🛫", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true, "homepage": "https://aerobase.app"}}
---
# Aerobase 旅行航班 🛫

## 搜索

**POST /api/v1/flights/search** — 使用 Kiwi 搜索引擎进行实时搜索；若 Kiwi 无法使用，则使用数据库作为备用方案  
请求体：`{ from: "JFK", to: "LHR", date: "2026-03-15", returnDate?: "2026-03-22", cabinClass?: "economy" }`  
免费 tier：返回 5 条结果；Concierge tier：返回 50 条结果。结果按时差综合得分（jetlag composite）降序排列，再按价格升序排列。  

**POST /api/flights/search/agent** — 同时使用多个供应商（Kiwi 和 Duffel）进行搜索  
请求体与 `/api/v1/flights/search` 相同。返回一个包含航班信息（UnifiedFlight[]）的数组，其中包含供应商信息、价格、时差得分（jetlagScore）以及航班段（segments）。  
每个供应商的搜索请求有 15 秒的超时限制；结果会根据航班编号和出发时间进行去重（允许 5 分钟的时间差异，价格差异不超过 5%）。  

## 预订（推荐使用 API）  

**POST /api/flights/validate** — 预订前检查价格  
请求体：`{ flightId, provider, offerId }`  
返回值：`{ valid, currentPrice, priceChanged }`  

**POST /api/flights/book** — 通过 AgentBookingService 进行预订  
请求体：`{ flightId, provider, offerId, passengers: [...], payment: { stripePaymentMethodId } }`  
- 使用 Kiwi 时，预订流程分为三个阶段：`check_flights → save_booking → confirm_payment`；价格允许有 5% 的差异。  
- 使用 Duffel 时，订单为即时生效，需使用余额支付。  
- 如果这两种方式均不可用，系统会返回一个 deepLink，供用户通过浏览器手动完成预订。  

**请务必在用户明确同意后才能提交支付。**  

## 预订（浏览器方式——备用方案）  

仅当 API 返回 deepLink 或相关服务不可用时才使用浏览器进行预订：  
1. 通过浏览器打开航空公司官网。  
2. 从用户个人资料中填写乘客信息。  
3. 截取预付款页面的截图并发送给用户审批。  
4. 只有在用户明确表示“同意”后才能提交预订。  

## 比较与评分  

**POST /api/v1/flights/compare** — 比较 2 至 10 条航班，并提供推荐结果及价格差异。  
**POST /api/v1/flights/score** — 计算航班的时差得分（jetlag score，范围 0-100），并提供恢复所需的天数（recoveryDays）及相应的出行策略。  
**GET /api/v1/flights/lookup/{carrier}/{number}** — 实时查询航班信息；若 Kiwi 或 Duffel 服务不可用，会使用 Amadeus 数据库作为备用方案。  
**GET /api/flightsproviders/status** — 查看 Kiwi 和 Duffel 服务的运行状态（预订前请先检查）。  

## 速率限制  

- 搜索：Kiwi 每小时最多 20 次请求；使用多个供应商进行搜索时，每小时最多 10 次请求。  
- 预订验证：每个预订请求每小时最多 5 次。  
- 评分/比较：每小时最多 50 次请求。  
- 航班信息查询：每小时最多 30 次请求（受 Amadeus 许可限制）。  

## 使用爬虫获取航班搜索结果（优先于直接使用浏览器）  

建议使用 `/search` 端点进行数据抓取。该端点会返回结构化 JSON 数据，无需手动操作浏览器（如截图或点击链接）。Helsinki 服务器返回的价格单位为欧元（EUR）。  
参考文档：[Scrapling 文档](https://scrapling.readthedocs.io/en/latest/overview.html)  

### Google Flights  
```
POST {SCRAPLING_URL}/search
{"site":"google-flights","origin":"LAX","destination":"NRT","departure":"2026-03-15","return":"2026-03-22"}
```  
返回格式：`{"results": [{"airline":"..","price":"€1,216","duration":"11 hr 50 min","stops":"Nonstop"}], "count": N}`  

### Kayak（可能会遇到验证码——此时可使用代理）  
```
POST {SCRAPLING_URL}/search
{"site":"kayak","origin":"LAX","destination":"NRT","departure":"2026-03-15","return":"2026-03-22"}
```  

### 结合 API 和爬虫的数据获取方式  
1. 立即通过 API（Kiwi/Duffel）进行搜索并向用户展示结果。  
2. 同时使用爬虫 `/search` 端点获取对比数据。  
3. 如果发现 Google Flights 也显示相同路线的航班价格（例如 €1,216 且为直飞），则进行进一步核对。  
4. 强调 API 数据与浏览器数据显示的差异。  

### 备用方案：使用原生浏览器  
如果爬虫请求返回 `challenge != "pass"` 或未找到任何结果：  
1. 尝试使用带有代理的浏览器进行搜索。  
2. 按照 aerobase-browser 的操作流程手动填写乘客信息。  
3. 每个网站每个会话最多尝试 2 次。  

### 重要注意事项：  
- Helsinki 服务器默认返回欧元价格；如用户需要美元价格，请进行转换。  
- Google Flights 每次搜索通常返回 15 至 50 条结果。  
- Kayak 服务经常需要用户输入验证码；此时使用爬虫获取数据更为可靠。  
- Skyscanner 服务可能完全无法使用，应跳过该服务。