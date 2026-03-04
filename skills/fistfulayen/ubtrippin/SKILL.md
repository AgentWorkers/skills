---
name: ubtrippin
version: 2.0.0
description: 通过 UBTRIPPIN 为您的用户管理旅行相关事务，包括行程安排、旅行用品、会员积分计划、家庭旅行信息、城市指南、活动信息、音乐会门票预订以及通知等。当用户询问他们的旅行安排、即将到来的旅行计划、航班信息、酒店预订、音乐会门票、活动门票、会员积分，或者希望管理自己的旅行记录时，可以使用该功能。使用该功能需要从 ubtrippin.xyz/settings 获取 UBTRIPPIN API 密钥。
---
# UBTRIPPIN 技能简介

**UBTRIPPIN** 是一个个人旅行追踪工具，它可以解析预订确认邮件，并将这些信息整理成旅行记录。同时，它还能处理来自 Ticketmaster、AXS、Eventbrite 等平台的音乐会、剧院演出、体育赛事、节日活动等活动的门票信息。作为代理，您可以通过 REST API 查看和管理用户的旅行信息（包括航班、酒店、火车票、门票/活动等）、忠诚度积分、家庭成员信息以及城市指南等。

---

## 设置（首次使用）

1. 请用户访问 **ubtrippin.xyz/settings** 生成一个 API 密钥。该密钥的格式为：`ubt_k1_<40 个十六进制字符>`。请妥善保管该密钥。
2. 获取用户的 **注册发送邮箱地址**——即他们用于转发预订邮件的邮箱地址。这个地址是用户在 UBTRIPPIN 中被允许使用的发送邮箱。
3. 操作该工具需要这两个信息：API 密钥用于读写数据，邮箱地址用于通过转发添加新的预订记录。
4. 设置完成后，调用 `GET /api/v1/me/profile`，并通过 `PATCH /api/v1/me/profile` 设置用户的默认机场、货币偏好和座位偏好。

---

## 认证

所有 API 请求都需要使用 Bearer 令牌：

```
Authorization: Bearer ubt_k1_<your_key>
```

基础 URL：`https://www.ubtrippin.xyz`

**请求限制**：每个 API 密钥每分钟最多 100 次请求。超出限制会导致 429 错误，需要等待 60 秒后再试。

---

## API 端点

### 旅行记录

#### 列出所有旅行记录
```
GET /api/v1/trips
```

查询参数：`?status=upcoming`（可选过滤条件）

响应：
```json
{
  "data": [
    {
      "id": "uuid",
      "title": "Tokyo Spring 2026",
      "start_date": "2026-04-01",
      "end_date": "2026-04-14",
      "primary_location": "Tokyo, Japan",
      "travelers": ["Ian Rogers"],
      "notes": null,
      "cover_image_url": "https://...",
      "share_enabled": false,
      "created_at": "2026-02-15T10:00:00Z",
      "updated_at": "2026-02-15T10:00:00Z"
    }
  ],
  "meta": { "count": 1 }
}
```

结果按 `start_date` 降序排列（最近的旅行记录排在最前面）。

#### 获取包含所有行程信息的旅行记录
```
GET /api/v1/trips/:id
```

响应中包含完整的旅行记录对象，其中包含嵌套的 `items` 数组。每个旅行记录项包含以下字段：
- `id`
- `trip_id`
- `kind`（类型）
- `provider`（预订平台）
- `traveler_names`（旅行者姓名）
- `start_ts`（开始时间）
- `end_ts`（结束时间）
- `start_date`（开始日期）
- `end_date`（结束日期）
- `start_location`（出发地）
- `end_location`（目的地）
- `summary`（简要描述）
- `details_json`（详细信息）
- `status`（状态）
- `confidence`（解析准确性）
- `needs_review`（是否需要审核）
- `timestamps`（时间戳）

**行程类型**：`flight`（航班）、`hotel`（酒店）、`train`（火车）、`car`（租车）、`ferry`（渡轮）、`activity`（活动）、`ticket`（门票）、`other`（其他类型）

#### 创建旅行记录
```
POST /api/v1/trips
Content-Type: application/json

{ "title": "Summer in Provence", "start_date": "2026-07-01", "end_date": "2026-07-14" }
```

#### 更新旅行记录
```
PATCH /api/v1/trips/:id
Content-Type: application/json

{ "title": "Updated Title", "notes": "Remember sunscreen" }
```

#### 删除旅行记录
```
DELETE /api/v1/trips/:id
```

#### 重命名旅行记录
```
POST /api/v1/trips/:id/rename
Content-Type: application/json

{ "title": "New Trip Name" }
```

#### 合并旅行记录
```
POST /api/v1/trips/:id/merge
Content-Type: application/json

{ "source_trip_id": "uuid-of-trip-to-merge-in" }
```

将源旅行记录中的项目合并到目标旅行记录中。

#### 旅行记录状态
```
GET /api/v1/trips/:id/status
```

返回旅行记录的处理状态。

#### 示例旅行记录
```
GET /api/v1/trips/demo
```

返回一个示例旅行记录（无需认证即可查看）。

---

### 旅行记录项

#### 获取单个旅行记录项
```
GET /api/v1/items/:id
```

响应格式：`{"data": <旅行记录项>`，其中 `details_json` 包含确认编号、座位分配等信息。

#### 更新旅行记录项
```
PATCH /api/v1/items/:id
Content-Type: application/json

{ "summary": "Updated summary", "start_location": "Paris CDG" }
```

#### 删除旅行记录项
```
DELETE /api/v1/items/:id
```

#### 向旅行记录中添加项目
```
POST /api/v1/trips/:id/items
Content-Type: application/json
```

**必填字段**：`kind`、`start_date`

**所有字段**：
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `kind` | string | 必填。值可以是 `flight`、`hotel`、`car_rental`、`train`、`activity`、`restaurant`、`ticket`、`other` |
| `start_date` | string | ISO 格式日期（格式：`YYYY-MM-DD`） |
| `end_date` | string | ISO 格式日期（酒店：退房日期；航班：到达日期） |
| `start_ts` | string | ISO 8601 格式的时间戳（包含时区，例如：`2026-04-01T08:30:00Z`） |
| `end_ts` | string | ISO 8601 格式的时间戳（包含时区） |
| `start_location` | string | 出发地/起点（最多 300 个字符） |
| `end_location` | string | 目的地（最多 300 个字符） |
| `summary` | string | 简要描述（例如：AF276 CDG→NRT） |
| `provider` | string | 预订平台（例如：Air France） |
| `confirmation_code` | string | 预订参考编号（最多 200 个字符） |
| `traveler_names` | string[] | 旅行者姓名数组（每个姓名最多 200 个字符） |
| `details_json` | object | 自由格式的元数据（例如：登机口、座位信息等，最大 10KB） |
| `notes` | string | 用户备注 |
| `status` | string | 项目状态 |

**示例 — 航班记录**：
```json
{
  "kind": "flight",
  "start_date": "2026-04-01",
  "start_ts": "2026-04-01T08:30:00+01:00",
  "end_ts": "2026-04-01T15:45:00+09:00",
  "start_location": "Paris CDG",
  "end_location": "Tokyo NRT",
  "summary": "AF276 CDG→NRT",
  "provider": "Air France",
  "confirmation_code": "XK7J3M",
  "traveler_names": ["Ian Rogers"],
  "details_json": { "flight_number": "AF276", "seat": "14A", "class": "Economy" }
}
```

**示例 — 酒店记录**：
```json
{
  "kind": "hotel",
  "start_date": "2026-04-01",
  "end_date": "2026-04-05",
  "start_location": "Tokyo, Japan",
  "summary": "Park Hyatt Tokyo",
  "provider": "Hyatt",
  "confirmation_code": "HY-889923",
  "traveler_names": ["Ian Rogers", "Hedvig Rogers"],
  "details_json": { "room_type": "King Deluxe", "check_in": "15:00", "check_out": "11:00" }
}
```

**示例 — 火车记录**：
```json
{
  "kind": "train",
  "start_date": "2026-04-05",
  "start_ts": "2026-04-05T09:00:00+09:00",
  "end_ts": "2026-04-05T11:30:00+09:00",
  "start_location": "Tokyo Station",
  "end_location": "Kyoto Station",
  "summary": "Shinkansen Nozomi 7",
  "provider": "JR Central",
  "confirmation_code": "JR-44521",
  "details_json": { "car": "7", "seat": "3A", "class": "Green Car" }
}
```

**示例 — 餐厅记录**：
```json
{
  "kind": "restaurant",
  "start_date": "2026-04-03",
  "start_ts": "2026-04-03T19:00:00+09:00",
  "start_location": "Sukiyabashi Jiro, Ginza, Tokyo",
  "summary": "Dinner at Sukiyabashi Jiro",
  "details_json": { "party_size": 2, "reservation_name": "Rogers" }
}
```

**示例 — 门票/活动记录（音乐会、体育赛事、剧院演出、节日活动等）**：
```json
{
  "kind": "ticket",
  "summary": "David Byrne at Théâtre du Châtelet",
  "start_date": "2026-05-15",
  "start_ts": "2026-05-15T20:00:00+02:00",
  "start_location": "Paris",
  "provider": "Ticketmaster",
  "details_json": {
    "event_name": "David Byrne: American Utopia",
    "venue": "Théâtre du Châtelet",
    "venue_address": "1 Place du Châtelet, 75001 Paris",
    "performer": "David Byrne",
    "event_time": "20:00",
    "door_time": "19:00",
    "section": "Orchestre",
    "seat": "12",
    "row": "G",
    "ticket_count": 2,
    "ticket_type": "Reserved",
    "event_category": "concert"
  }
}
```

**门票详细信息**：
| 字段 | 类型 | 描述 |
|-------|------|-------------|
| event_name | string | 活动名称 |
| venue | string | 活动场所名称 |
| venue_address | string? | 完整地址 |
| event_time | HH:MM | 活动开始时间 |
| door_time | HH:MM? | 开场时间 |
| section | string? | 座位区域 |
| seat | string? | 座位编号 |
| row | string? | 座位排号 |
| ticket_count | number | 门票数量 |
| ticket_type | string? | 座位类型（例如：GA、Reserved、VIP 等） |
| performer | string? | 艺术家/表演者 |
| event_category | enum | 活动类型（音乐会、剧院演出、体育赛事、博物馆、节日活动等） |

**支持的门票预订平台**：Ticketmaster、AXS、Eventbrite、Dice、SeeTickets、StubHub、Viagogo、场馆直接销售。只需将预订确认邮件转发至 trips@ubtrippin.xyz，系统会自动提取门票信息。

**活动驱动的旅行记录**：当门票邮件创建新的旅行记录时（日期不重叠），旅行记录的名称会以活动或表演者命名，封面图片也会使用表演者的图片（而非城市名称）。

#### 批量添加旅行记录项
```
POST /api/v1/trips/:id/items/batch
Content-Type: application/json

{ "items": [ <item>, <item>, ... ] }
```

每次请求最多添加 50 个旅行记录项。字段与单个旅行记录的创建方式相同。

响应格式：`{"data": [...items], "meta": { "count": N }`

**给代理的建议**：当用户提供预订确认信息（电子邮件文本或截图）时，您需要自行解析这些信息，并使用相应的 API 端点添加到旅行记录中。UBTRIPPIN 负责数据的存储、分类和显示。

#### 更新旅行记录项的状态
```
GET /api/v1/items/:id/status
```

#### 刷新旅行记录项的状态
```
POST /api/v1/items/:id/status/refresh
```

重新检查旅行记录的实时状态（例如航班延误、登机口变更等）。

---

### 忠诚度积分

#### 列出我的忠诚度计划
```
GET /api/v1/me/loyalty
```

响应内容：
```json
{
  "data": [
    {
      "id": "uuid",
      "provider_key": "delta_skymiles",
      "provider_name": "Delta SkyMiles",
      "member_number": "1234567890",
      "tier": "Gold",
      "notes": null
    }
  ]
}
```

#### 按预订平台查找忠诚度计划
```
GET /api/v1/me/loyalty/lookup?provider_key=delta_skymiles
```

根据特定预订平台返回对应的忠诚度计划信息。

#### 添加忠诚度计划
```
POST /api/v1/me/loyalty
Content-Type: application/json

{ "provider_key": "delta_skymiles", "member_number": "1234567890", "tier": "Gold" }
```

#### 更新忠诚度计划
```
PATCH /api/v1/me/loyalty/:id
Content-Type: application/json

{ "member_number": "9876543210", "tier": "Platinum" }
```

#### 删除忠诚度计划
```
DELETE /api/v1/me/loyalty/:id
```

#### 导出忠诚度数据
```
GET /api/v1/me/loyalty/export
```

以可下载格式返回所有忠诚度计划数据。

#### 列出支持的预订平台
```
GET /api/v1/loyalty/providers
```

返回所有支持的预订平台列表（无需认证）。

---

### 个人资料

#### 查看我的个人资料
```
GET /api/v1/me/profile
```

响应内容包括姓名、邮箱地址、偏好设置和会员等级。

#### 更新我的个人资料
```
PUT /api/v1/me/profile
Content-Type: application/json

{ "display_name": "Ian Rogers", "timezone": "Europe/Paris" }
```

也可以使用 `POST` 请求进行更新。

---

### 家庭成员

#### 列出我的家庭成员
```
GET /api/v1/families
```

#### 创建家庭成员
```
POST /api/v1/families
Content-Type: application/json

{ "name": "The Rogers Family" }
```

#### 查看家庭成员信息
```
GET /api/v1/families/:id
```

#### 更新家庭成员信息
```
PATCH /api/v1/families/:id
Content-Type: application/json

{ "name": "Updated Family Name" }
```

#### 删除家庭成员
```
DELETE /api/v1/families/:id
```

#### 邀请家庭成员加入家庭
```
POST /api/v1/families/:id/members
Content-Type: application/json

{ "email": "partner@example.com", "role": "member" }
```

#### 删除家庭成员
```
DELETE /api/v1/families/:id/members/:uid
```

#### 查看家庭成员的个人资料
```
GET /api/v1/families/:id/profiles
```

#### 查看家庭成员的旅行记录
```
GET /api/v1/families/:id/trips
```

显示家庭成员可见的所有旅行记录。

#### 家庭忠诚度计划
```
GET /api/v1/families/:id/loyalty
```

#### 查找家庭成员的忠诚度计划信息
```
GET /api/v1/families/:id/loyalty/lookup?provider_key=delta_skymiles
```

查询所有家庭成员的忠诚度计划编号。

#### 家庭城市指南
```
GET /api/v1/families/:id/guides
```

#### 查看并接受家庭邀请链接
```
GET /api/v1/family-invites/:token
POST /api/v1/family-invites/:token/accept
```

---

### 合作者（旅行记录共享）

#### 列出合作者
```
GET /api/v1/trips/:id/collaborators
```

#### 邀请合作者
```
POST /api/v1/trips/:id/collaborators
Content-Type: application/json

{ "email": "friend@example.com", "role": "viewer" }
```

#### 更新合作者的角色
```
PATCH /api/v1/trips/:id/collaborators/:uid
Content-Type: application/json

{ "role": "editor" }
```

#### 删除合作者
```
DELETE /api/v1/trips/:id/collaborators/:uid
```

#### 查看和接受旅行记录共享邀请
```
GET /api/v1/invites/:token
POST /api/v1/invites/:token/accept
```

---

### 城市指南

#### 列出城市指南
```
GET /api/v1/guides
```

查询参数：`?family_id=uuid`（可选）

#### 创建城市指南
```
POST /api/v1/guides
Content-Type: application/json

{ "city": "Tokyo", "title": "Tokyo Eats" }
```

#### 查看城市指南信息
```
GET /api/v1/guides/:id
```

#### 更新城市指南信息
```
PATCH /api/v1/guides/:id
```

#### 删除城市指南
```
DELETE /api/v1/guides/:id
```

#### 列出城市指南条目
```
GET /api/v1/guides/:id/entries
```

#### 添加城市指南条目
```
POST /api/v1/guides/:id/entries
Content-Type: application/json

{ "name": "Tsukiji Outer Market", "category": "food", "notes": "Go early" }
```

#### 更新城市指南条目
```
PATCH /api/v1/guides/:id/entries/:eid
```

#### 删除城市指南条目
```
DELETE /api/v1/guides/:id/entries/:eid
```

#### 查找附近的城市指南
```
GET /api/v1/guides/nearby?lat=35.6762&lng=139.6503
```

查找指定位置附近的指南信息。

---

### 允许的发送邮箱地址

#### 列出允许的发送邮箱地址
```
GET /api/v1/settings/senders
```

#### 添加新的发送邮箱地址
```
POST /api/v1/settings/senders
Content-Type: application/json

{ "email": "mywork@company.com" }
```

#### 删除发送邮箱地址
```
DELETE /api/v1/settings/senders/:id
```

---

### 日历

#### 获取日历令牌
```
GET /api/v1/calendar/token
```

返回用于将旅行记录同步到日历应用的 iCal 订阅链接。

#### 重新生成日历令牌
```
POST /api/v1/calendar/token
```

使旧令牌失效并生成新的令牌。

---

### 通知

#### 列出通知信息
```
GET /api/v1/notifications
```

查询参数：`?unread=true`（可选）

#### 标记通知为已读
```
PATCH /api/v1/notifications/:id
Content-Type: application/json

{ "read": true }
```

---

### Webhook

#### 列出 Webhook 信息
```
GET /api/v1/webhooks
```

#### 创建 Webhook
```
POST /api/v1/webhooks
Content-Type: application/json

{ "url": "https://example.com/hook", "events": ["trip.created", "item.added"] }
```

#### 获取 Webhook 信息
```
GET /api/v1/webhooks/:id
```

#### 更新 Webhook 信息
```
PATCH /api/v1/webhooks/:id
Content-Type: application/json

{ "url": "https://example.com/new-hook", "active": true }
```

#### 删除 Webhook
```
DELETE /api/v1/webhooks/:id
```

#### 测试 Webhook
```
POST /api/v1/webhooks/:id/test
```

发送测试数据以验证 Webhook 是否正常工作。

#### Webhook 发送记录
```
GET /api/v1/webhooks/:id/deliveries
```

列出最近的 Webhook 发送尝试记录及其状态码。

---

### 火车信息

#### 查看火车状态
```
GET /api/v1/trains/:trainNumber/status
```

根据火车编号查询火车的实时状态（例如延误情况、站台信息等）。

---

### 图片

#### 搜索图片
```
GET /api/v1/images/search?q=tokyo+tower
```

搜索目的地或活动现场的图片。

---

### 数据导入

#### 列出导入记录
```
GET /api/v1/imports
```

#### 创建导入任务
```
POST /api/v1/imports
```

上传预订数据以批量导入。

#### 获取导入记录
```
GET /api/v1/imports/:id
```

---

### 账务管理

#### 查看订阅信息
```
GET /api/v1/billing/subscription
```

返回当前的订阅计划、会员等级和计费周期。

#### 获取计费门户链接
```
GET /api/v1/billing/portal
```

返回用于管理订阅的 Stripe 计费门户链接。

#### 查看价格信息
```
GET /api/v1/billing/prices
```

查看可用的订阅计划和价格信息。

#### 进行订单结算
```
POST /api/v1/checkout
Content-Type: application/json

{ "price_id": "price_xxx" }
```

创建 Stripe 订购结算页面。

---

### 账户激活

#### 查看账户激活状态
```
GET /api/v1/activation/status
```

返回用户账户的激活状态。

---

## 添加新的预订记录（通过邮件转发）

添加预订记录的主要方法是 **邮件转发**。当用户收到预订确认邮件时，请按照以下步骤操作：
1. 将邮件转发至：`trips@ubtrippin.xyz`
2. 必须使用用户的注册发送邮箱地址进行转发；UBTRIPPIN 会拒绝来自未知发送地址的邮件。
3. UBTRIPPIN 的人工智能解析器会自动提取预订详情（通常在 30 秒内完成）。
4. 该预订记录会显示在相应的旅行记录中（或创建一个新的旅行记录）。

**作为代理的操作步骤**：
- 使用您的邮件发送功能，将邮件从用户的邮箱地址转发至 `trips@ubtrippin.xyz`。
- 或者指导用户直接从他们的邮箱进行转发。
- 支持 PDF 格式的附件（例如电子票），请确保将附件一起转发。

**支持的预订类型**：航班、酒店、火车（Eurostar、SNCF、Thalys 等）、租车、渡轮预订、音乐会/活动门票（Ticketmaster、AXS、Eventbrite、Dice、SeeTickets、StubHub、Viagogo）以及大多数主要的预订平台（Booking.com、Expedia、Kayak、Trainline 等）。

---

## 常见的代理工作流程

### “我有哪些即将到来的旅行？”
1. `GET /api/v1/trips`
2. 根据 `start_date` 筛选（大于或等于今天）并格式化结果显示。

### “我在东京的行程安排是什么？”
1. `GET /api/v1/trips` — 查找东京的旅行记录 ID
2. `GET /api/v1/trips/:id` — 获取包含所有行程信息的完整行程记录
3. 根据 `start_ts` 按时间顺序显示行程记录。

### “我刚刚在东京预订了酒店，请添加到旅行记录中”
1. 请用户将预订确认邮件转发至 `trips@ubtrippin.xyz`
2. 或者如果您有访问用户邮箱的权限，可以自行转发邮件
3. 等待约 30 秒后，再次调用 `GET /api/v1/trips/:id` 确认记录是否已添加。

### “我的 Delta SkyMiles 会员编号是多少？”
1. `GET /api/v1/me/loyalty/lookup?provider_key=delta_skymiles`
2. 从响应中获取 `member_number`。

### “我为我的家庭添加 Marriott Bonvoy 会员资格”
1. 使用 `POST /api/v1/me/loyalty` 发送以下数据：`{"provider_key": "marriott_bonvoy", "member_number": "123456789"}`

### “我的家庭成员有哪些 Delta 忠诚度计划？”
1. 获取家庭成员 ID：`GET /api/v1/families`
2. `GET /api/v1/families/:id/loyalty/lookup?provider_key=delta_skymiles`
3. 获取所有家庭成员的 Delta 会员编号。

### “为我的家庭成员添加会员”
1. 使用 `POST /api/v1/families` 创建家庭成员组（如果尚不存在）
2. 对于每个家庭成员，使用 `POST /api/v1/families/:id/members` 发送以下数据：`{"email": "partner@example.com"}`。他们会收到邀请邮件以确认加入。
3. 家庭成员收到邀请后需要点击链接接受邀请。

### “与朋友共享我的旅行记录”
1. 使用 `POST /api/v1/trips/:id/collaborators` 发送以下数据：`{"email": "friend@example.com", "role": "viewer"}`

### “我的火车是否准点？”
1. `GET /api/v1/trains/:trainNumber/status`
2. 查看火车的实时状态（例如延误情况、站台变更等）。

### “显示我附近的城市指南”
1. `GET /api/v1/guides/nearby?lat=48.8566&lng=2.3522`

### “为新预订设置 Webhook”
1. 使用 `POST /api/v1/webhooks` 发送以下数据：`{"url": "https://...", "events": ["item.added"]`

### “获取我的旅行记录的日历链接”
1. `GET /api/v1/calender/token`
2. 将生成的 iCal 链接提供给用户，以便他们将其添加到日历应用中。

---

## 错误处理

| 状态码 | 错误信息 | 含义 |
|--------|------|---------|
| 401 | `unauthorized` | API 密钥缺失或无效 |
| 400 | `invalid_param` | 提供的 UUID 无效或缺少字段 |
| 404 | `not_found` | 未找到旅行记录或项目，或该记录属于其他用户 |
| 429 | _（错误信息可能因情况而异）| 请求次数超出限制，请等待 60 秒后再试 |
| 500 | `internal_error` | 服务器错误，请稍后再试 |

所有错误都会返回以下格式的响应：`{"error": { "code": "...", "message": "..." }`

---

## 给代理的注意事项

- 所有的 ID 都是 UUID 格式。
- 日期使用 ISO 8601 格式（日期：`YYYY-MM-DD`；时间戳：`YYYY-MM-DDTHH:MM:SSZ`）。
- `details_json` 包含原始的解析数据（例如预订编号、座位信息、忠诚度编号等）。
- `confidence`（0–1）表示人工智能解析的准确性；标记为 `needs_review` 的项目可能存在错误。
- API 密钥属于用户所有，切勿共享或存储（除非用户明确允许）。

---

## API 密钥管理

用户可以在 **ubtrippin.xyz/settings** 中管理自己的 API 密钥。每个密钥都有一个名称和预览信息。如果密钥被盗用，用户可以在设置页面撤销密钥并生成新的密钥。