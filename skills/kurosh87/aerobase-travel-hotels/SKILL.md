---
name: aerobase-hotels
description: >
  酒店搜索功能：  
  - 兼顾时差影响的搜索结果  
  - 支持日间使用的酒店选择  
  - 提供价格比较功能  
  （注：翻译内容根据用户提供的文件内容进行了简化处理，保留了核心功能描述，同时确保了技术术语的准确性。）
metadata: {"openclaw": {"emoji": "🏨", "primaryEnv": "AEROBASE_API_KEY", "user-invocable": true}}
---
# 酒店预订与中途停留住宿

在推荐酒店时，应考虑旅客的疲劳恢复情况：“您的中途停留时间为9小时。乘坐8分钟的班车前往希尔顿酒店后，您可以在凌晨2点时休息5个小时。该酒店的价格为89美元，这有助于缓解您在下一趟航班中的时差反应。”

## 搜索（v1 API - 推荐使用）

**GET /api/v1/hotels** — 使用过滤器搜索酒店  
查询参数：`airport`（机场）、`city`（城市）、`country`（国家）、`chain`（酒店品牌）、`tier`（酒店等级）、`stars`（星级）、`jetlagFriendly`（是否适合缓解时差）、`search`（搜索关键词）、`limit`（结果数量）、`offset`（结果偏移量）  
返回内容：包含酒店信息、设施及价格的数据  

示例：`GET /api/v1/hotels?airport=JFK&jetlagFriendly=true`  

## 搜索（旧版API）

**POST /api/hotels/search** — 提供以下参数：`destination`（目的地）、`checkin`（入住时间）、`checkout`（退房时间）、`guests`（客人数量）  

**房价信息**：`GET /api/hotels/rates/{hotelId}` — 获取酒店房间信息及取消政策  
**预订**：`POST /api/hotels/prebook` — 预订酒店（价格可能会变动）  
**确认预订**：`POST /api/hotels/book` — 提供`prebookId`（预订ID）  
**管理预订**：`GET /api/hotels/bookings`（查看预订信息）；`DELETE /api/hotels/bookings/{id}`（取消预订）  

## 特殊服务  

- **GET /api/dayuse?airport={code}` — 专为中途停留旅客提供的日租酒店（仅允许当天使用，不允许过夜）  
- **GET /api/hotels?dayuse=true** — 过滤出仅提供日租服务的酒店  
- **GET /api/hotels/near-airport/{code}` — 位于机场附近的酒店  

## 常规建议  

- 预订前务必查看酒店的取消政策  
- 中途停留时间超过8小时的旅客，建议选择日租酒店  
- 长途旅行的旅客应考虑酒店是否提供有助于缓解时差的设施（如遮光窗帘、健身房、游泳池等）  

## 请求频率限制  

- 搜索请求：每小时最多20次  
- 房价查询：每小时最多10次  
- 预订请求：每小时最多5次（预订后价格可能变动）  
- 机场附近酒店的预订请求：每小时最多10次  

## 数据来源 — 酒店信息  

### 主要数据来源：LiteAPI（免费，优先使用）  
- 首先使用LiteAPI查询酒店的可用性、价格及详细信息  
- 返回结构化的JSON数据：酒店名称、价格、评分、设施及照片  
- 当前使用过程中无需担心请求频率限制  
- 响应速度快，且不会增加浏览器负担  

### 辅助数据来源：浏览器  
- 同时使用浏览器进行搜索，以获取以下额外信息：  
  - 酒店的实际外观（截图）  
  - Booking.com上的用户评价和评分  
  - 不同在线旅行平台（如Booking.com、Google Hotels、LiteAPI）的价格对比  
  - 酒店周边环境（Google地图街景）  

### 工作流程  
1. 用户请求：“查找3月15日至20日在东京的酒店”  
2. 立即发起两个并发请求：  
   a. 使用LiteAPI查询（数据结构化，响应速度快）  
   b. 使用浏览器访问Booking.com进行搜索（获取更多信息，但响应速度较慢）  
3. 先显示LiteAPI的结果（响应更快）  
4. 根据浏览器获取的信息进行补充说明：“我在Booking.com上也找到了这些酒店，供您参考……”  
5. 强调价格差异：“LiteAPI显示的价格为每晚120美元，而Booking.com上的价格是135美元。”  

### 数据抓取——Booking.com酒店搜索  

使用`/search`接口抓取酒店信息：  
参考文档：[Scrapling Documentation](https://scrapling.readthedocs.io/en/latest/overview.html)  

**返回格式示例**：`{"results": [{"name":"..","price":"..","rating":"..","location":".."}], "count": N}`  

**注意**：Booking.com属于“挑战级”数据源——部分酒店可能设置隐私政策，导致某些查询参数无法使用。如果`challenge`字段的值为`"pass"`且查询结果为空，则需通过代理浏览器进行查询。  

### 使用Google Hotels的流程（直接访问，无需代理）  
1. 访问https://www.google.com/travel/hotels  
2. 如果出现隐私政策提示，同意相关设置  
3. 输入目的地，等待搜索结果  
4. 结果会显示多个预订平台的综合价格  

**何时完全放弃使用浏览器**  
- 用户仅需要快速查询酒店可用性时，直接使用LiteAPI  
- 用户需要查询特定酒店名称时，直接使用LiteAPI  
- 预算有限或查询简单的需求时，LiteAPI即可满足  
- 仅当用户需要价格对比、查看评论或查看酒店外观时，才使用浏览器