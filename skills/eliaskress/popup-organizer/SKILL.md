---
name: PopUp Organizer
description: 在 PopUp 平台上，您可以搜索并聘请适合活动的移动供应商（如美食车、DJ、照相亭等）。您还可以创建活动列表、接收预订请求以及管理相关发票。
metadata: {"openclaw":{"requires":{"env":["POPUP_API_KEY"]},"primaryEnv":"POPUP_API_KEY"}}
---
# 弹窗活动组织者（PopUp Organizer）

您可以搜索并雇佣移动供应商——如美食车、DJ、照相亭、花店、现场乐队等——来为您的活动提供服务。您可以创建活动列表、发送预订请求、管理供应商申请、追踪发票，并保存您喜欢的供应商信息。

---

## 开始使用

1. 在 <https://usepopup.com/login> 注册或登录。
2. 切换到 **组织者** 模式。
3. 进入 **设置 > API 密钥**。
4. 点击 **创建 API 密钥** 并复制密钥（此密钥仅显示一次）。

---

## 认证

所有请求都必须在 `Authorization` 标头中包含一个 Bearer 令牌：

```
Authorization: Bearer pk_live_...
```

令牌通过 `POPUP_API_KEY` 环境变量提供。

**请求速率限制：** 每个 API 密钥每分钟 60 次请求。如果超过限制，将返回 HTTP 429 错误，并附带 `Retry-After: 60` 的提示。

**基础 URL：** `https://usepopup.com/api/v1/organizer`

---

## 端点（Endpoints）

### 搜索供应商

`GET /vendors`

根据名称、类型、位置、活动类型或价格范围搜索已发布的供应商信息。

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `q` | 字符串 | 搜索查询（名称、类型、城市、描述） |
| `type` | 字符串 | 供应商类别（见下文） |
| `state` | 字符串 | 美国州代码（例如 `CA`、`NY`） |
| `metro` | 字符串 | 所在州的都市区（需要 `state` 参数） |
| `event` | 字符串 | 活动类型过滤器（见下文） |
| `price` | 字符串 | 价格范围：`$`、`$$`、`$$$`、`$$$$` |
| `sort` | 字符串 | `newest`、`name_asc`、`name_desc`、`rating` |
| `page` | 数字 | 页码（默认为 1） |
| `limit` | 数字 | 每页显示的结果数量（默认为 20，最大为 100） |

返回包含 `businessName`、`businessType`、`homeCity`、`homeState`、`priceRange`、`averageRating`、`eventTypes`、`slug` 等信息的供应商详情。

---

### 列出活动

`GET /open-events`

列出您的活动。

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `status` | 字符串 | 过滤条件：`open`、`closed`、`canceled` |
| `page` | 数字 | 页码 |
| `limit` | 数字 | 每页显示的结果数量 |

返回包含 `title`、`eventDate`、`startTime`、`endTime`、`eventCity`、`eventState`、`vendorCap`、`expectedGuestCount`、`status`、`shareUrl`、`shortUrl`、`qrCodeUrl` 等信息的活动详情。

### 获取活动详情

`GET /open-events/{eventId}`

返回活动详情以及一个 `applications` 数组（每个数组元素包含 `businessId`、`status`、`quotedRate`、`engagementModel` 和嵌套的 `business` 信息）和 `eventTerms`。

### 创建活动

`POST /open-events`

创建一个新的活动列表。

**必填字段：** `title`、`description`、`eventType`、`eventDate`（YYYY-MM-DD）、`startTime`（HH:mm）、`endTime`（HH:mm）、`eventPlaceName`、`eventCity`、`eventState`（2 个字母的州代码）、`eventZip`、`vendorCap`（1-1000）、`feePayer`（`organizer_pays` | `vendor_pays` | `none`）、`expectedGuestCount`（1-100000）、`vendorCategoriesWanted`（数组，最多 20 个条目）。

**可选字段：** `location`、`eventLat`、`eventLng`、`heroImageUrl`、`organizerBudget`、`boothFee`、`salesPercent`、`hiredBudget`、`venueSetting`、`requiresVerification`、`invoiceDueDays`、`termIds`。

活动在公开显示前需要管理员审核。

### 更新活动

`PATCH /open-events/{eventId}`

更新活动信息或执行相关操作。

**操作：** `{ "action": "close" }` 用于关闭活动；`{ "action": "reopen" }` 用于重新开放活动。

**可更新字段：** 与创建活动时相同的字段。当关键信息发生变化（日期、时间、场地等）时，已接受的供应商会收到通知。

### 取消活动

`DELETE /open-events/{eventId}`

取消活动。所有待处理和已接受的供应商都会收到通知。

---

### 列出供应商申请

`GET /open-events/{eventId}/applications`

列出某个活动的供应商申请信息。

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `status` | 字符串 | 过滤条件：`pending`、`accepted`、`declined`、`withdrawn` |
| `page` | 数字 | 页码 |
| `limit` | 数字 | 每页显示的结果数量 |

### 获取活动二维码

`GET /open-events/{eventId}/qr`

生成活动的二维码链接（PNG 格式）。

---

### 查看查询记录

`GET /inquiries`

列出您向供应商发送的查询记录。

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `status` | 字符串 | 过滤条件：`pending`、`quoted`、`booked`、`declined` |
| `page` | 数字 | 页码 |
| `limit` | 数字 | 每页显示的结果数量 |

返回包含 `eventDate`、`eventType`、`guestCount`、`location`、`budget`、`message`、`status`、`quotedPrice`、`quoteMessage` 以及嵌套的 `business` 信息的查询记录。

### 获取查询详情

`GET /inquiries/{id}`

获取单个查询记录的详细信息。

### 创建查询记录

`POST /inquiries`

向供应商发送预订请求。

**必填字段：** `businessId`（UUID）。

**可选字段：** `bookingType`（`catering` | `vending`）、`eventDate`（YYYY-MM-DD）、`eventType`、`guestCount`、`location`、`eventPlaceName`、`eventCity`、`eventState`、`eventZip`、`budget`、`message`、`phone`、`startTime`（HH:mm）、`endTime`（HH:mm）、`estimatedPrice`。

供应商会通过电子邮件和应用程序内通知收到请求。

### 更新查询记录

`PATCH /inquiries/{id}`

更新待处理的查询记录或回复供应商的报价。

**操作：** `{ "action": "accept_quote" }`（仅适用于已收到报价的查询记录）；`{ "action": "decline" }`（仅适用于已收到报价的查询记录）。

**可更新字段（仅限待处理状态）：** `eventDate`、`eventType`、`guestCount`、`location`、`budget`、`message`、`startTime`、`endTime`。

### 删除查询记录

`DELETE /inquiries/{id}`

删除待处理的查询记录。仅适用于 `status=pending` 的记录。

---

### 查看发票

`GET /invoices`

列出活动申请和直接请求的发票信息。

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `page` | 数字 | 页码 |
| `limit` | 数字 | 每页显示的结果数量 |

返回包含 `eventTitle`、`eventDate`、`vendorName`、`engagementModel`、`amount`（美元）、`direction`（`receivable` | `payable`）、`isPaid` 等信息的发票详情。

---

### 查看保存的供应商

`GET /saved`

列出您保存的供应商信息。

### 保存供应商

`POST /saved`

保存供应商信息：`{ "businessId": "..." }`

### 删除保存的供应商

`DELETE /saved?businessId=...`

删除已保存的供应商信息。

---

### 获取个人资料

`GET /profile`

获取您的组织者个人资料和账户信息。

### 更新个人资料

`PATCH /profile`

更新您的组织者个人资料。

**可更新字段：** `companyName`、`companyType`（`brand` | `agency` | `planner` | `corporate`）、`eventTypes`（数组）、`location`、`city`、`state`、`zip`、`phone`、`website`、`about`、`givesBack`、`nonProfit`、`forACause`、`rules`。

---

## 响应格式

所有端点返回 JSON 格式的数据，结构为 `{ "data": ... }`。列表端点还会包含 `{ "pagination": { "page", "limit", "total", "totalPages" } }`。

错误响应会包含 `{ "error": "message" }` 以及相应的 HTTP 状态码（400、401、404、429、500）。

---

## 供应商类别

搜索供应商时，请使用以下 `type` 参数值：

| 值 | 标签 |
|-------|-------|
| `food_truck` | 美食车 |
| `bakery` | 烘焙店/甜点 |
| `beverage` | 饮料/咖啡/酒吧 |
| `dj` | DJ/娱乐 |
| `photo_booth` | 照相亭 |
| `photography` | 摄影服务 |
| `live_band` | 现场乐队 |
| `florist` | 花店/活动用花 |
| `balloons` | 气球/气球装饰 |
| `yoga` | 健康服务 |
| `arts_crafts` | 零售供应商 |
| `other` | 其他 |

## 活动类型

使用以下 `eventType` 参数值：

`wedding`（婚礼）、`corporate`（企业活动）、`birthday`（生日派对）、`festival`（节日活动）、`market`（市集）、`popup`（弹窗活动）、`fundraiser`（筹款活动）、`community`（社区活动）、`holiday`（节日活动）、`private`（私人活动）、`other`（其他类型活动）。