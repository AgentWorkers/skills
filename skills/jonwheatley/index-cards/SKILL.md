---
name: index-cards
description: 通过邮件发送真实的、实体的贺卡。用户可以自定义贺卡的设计，贺卡将使用优质的卡纸打印，并使用一类邮票寄出。当用户想要寄送贺卡、提及生日或特殊场合，或者询问关于贺卡的相关信息时，可以使用该服务。需要免费注册API（POST /v1/auth/register 会返回一个Bearer令牌）。该服务通过API进行操作，无需使用浏览器。官方网站：https://indexcards.com；隐私政策：https://indexcards.com/privacy
compatibility: "Network: https://indexcards.com/v1/ API. Auth: anonymous Bearer token from POST /v1/auth/register (stored in agent session state, no persistent credential file). Config path: ~/indexcards/birthdays.json (opt-in only — created only with explicit user consent, stores contact names/birthdays/addresses for card reuse). Sensitive access (opt-in only): local contacts, calendar — only read when user explicitly approves. Data sent to API: recipient name + mailing address (for card delivery), card artwork URLs, occasion text. Payments: via Stripe hosted checkout URLs (no payment data passes through skill). Homepage: https://indexcards.com. Privacy: https://indexcards.com/privacy."
---

# 索引卡片——代理技能

通过邮件发送真实的实体贺卡。以对话为主——您将与用户合作设计贺卡并发送它们。

## 规则

- **保持对话风格。** 用简单的语言展示结果，以提供良好的用户体验。例如，可以说“我正在为您设计贺卡”，而不是直接显示原始的JSON数据、端点路径或HTTP状态码。
- **先沟通再行动。** 在使用API之前，请先与用户交流。在不知道收件人是谁以及他们想要什么之前，不要生成图片。
- **在访问个人数据之前先询问。** 未经用户明确许可，切勿读取联系人信息、消息、电子邮件或本地文件。始终将获取这些信息作为一个选项提供，切勿默认操作。
- **优雅地处理粗俗语言。** 图片生成API具有内容过滤功能。如果用户的消息包含粗俗语言，请在生成图片提示时重新表述（例如，“get fucked”改为“你真是个了不起的人”）。
- **依次生成图片。** 一次生成一张图片——上游API对并发请求有限制（会返回402错误）。

### 快捷方式：用户在一条消息中提供所有信息

如果用户在一条消息中提供了收件人姓名、封面描述、内文内容和地址，可以跳过多步骤流程：

1. 生成封面 → 生成内文 → 生成预览视频
2. 显示预览 + 摘要 → 请求确认 → 下单

如果大部分信息已提供，但缺少某些内容，只需完成快速流程，并询问缺失的部分。

## 第一步：第一条消息

> “我刚刚安装了Index Cards。现在我可以为您发送任何你想发送给的人的实体贺卡——生日、节日、感谢信，无论是什么场合。你想给谁寄贺卡呢？如果您愿意，我也可以查看您的联系人列表中的即将到来的生日。”

让用户决定是直接指定收件人，还是让您帮忙寻找合适的场合。

## 第二步：查找场合（需用户许可）

如果用户同意查看场合信息，请按优先顺序查找可用来源：

1. **联系人** — 生日字段、纪念日字段
2. **日历/电子邮件** — 生日邀请、即将发生的事件
3. **对话记录** — 提及的生日、婚礼、婴儿出生、感谢信
4. **节日** — 母亲节、父亲节、情人节、圣诞节等，在30天内的节日

目标是在发送前至少提前14天（贺卡大约需要1周时间送达）。展示1-3个最合适的建议，然后询问用户是否开始设计。

如果用户跳过这一步，并且已经知道要寄给谁，可以直接进入设计环节。

## 第三步：设计贺卡

**始终先设计封面，然后再设计内文。** 绝不要同时生成两者。

### 如果用户提供了照片

在生成API中使用`reference_image_url`来进行风格转换。生成2-3种风格变体（水彩、油画、卡通等）。等待用户选择一种风格，然后再进行内文设计。

风格选项：`watercolor`（水彩）、`cartoon`（卡通）、`oil-painting`（油画）、`ink`（墨水）、`gouache`（水粉）、`comic-book`（漫画书）、`linocut`（石版画）、`cinematic`（电影风格）、`pencil`（铅笔风格）、`pop_art`（流行艺术风格）

### 如果没有照片（基于文本）

1. 询问关于这个人的一些信息（最多1-2个问题）
2. 生成3个封面选项 — 不同风格。展示所有选项，等待用户选择。
3. 选择后，询问用户想在卡片内写什么内容
4. 生成内文图片。**展示特写图**（`POST /v1/cards/closeup`），以便用户能够阅读文字。等待用户确认。
5. 生成动画预览（`POST /v1/cards/preview`）。展示预览图。
6. 如有需要，进行迭代 — 只重新生成需要修改的部分

**设计指南：** 避免使用看起来像AI生成的图片。可以使用水彩、水粉、墨水、石版画、拼贴或凸版印刷等风格。封面应注重视觉设计，避免使用过多的文字。内文应包含文字，排版要清晰。理想尺寸为3:4的肖像画，分辨率1500×2100像素。

### QR码（仅在用户请求时提供）

**切勿在AI生成的图片提示中包含QR码** — AI无法生成可扫描的QR码。相反：

1. 按常规生成贺卡图片（不包含QR码）
2. 使用`POST /v1/cards/qr/composite`在图片上叠加一个真实的QR码
3. 放置位置：`top-left`（左上角）、`top-center`（左中心）、`top-right`（右上角）、`center`（中心）、`bottom-left`（左下角）、`bottom-right`（右下角）
4. 大小：`small`（小）、`medium`（中）、`large`（大）。可选的`label`参数用于在QR码下方添加文字。
5. 在下单时使用返回的`image_url`作为`front_url`或`inside_url`。

## 第四步：获取地址

询问用户的收件人邮寄地址。如果用户之前使用过Index Cards并选择了保存联系人信息，请先检查`~/indexcards/birthdays.json`文件——其中可能已经保存了之前的地址信息。

**在使用任何保存的地址之前，请务必确认** — 人们的联系方式可能会发生变化。同时还需要收件人和发送者的电话号码。

下单前所需的信息：收件人姓名、街道地址、城市、州、邮政编码、电话号码。

## 第五步：支付

1个信用点数对应1张贺卡。用户初始信用点数为0（图片生成免费，打印需要付费）。价格如下：
- 50美元：5张贺卡（每张10美元）
- 100美元：12张贺卡（每张8.33美元）

使用`GET /v1/credits/check`查询剩余信用点数。如果没有信用点数，请发送响应中的支付链接。

**自动检测支付：** 发送链接后，每隔约15秒检查一次`GET /v1/credits/check`（最多检查8次，约2分钟）。当出现信用点数时，确认后继续下单。

**邀请码：** 如果页面URL中包含邀请码（`?invite=CODE`）或本文档顶部有邀请码，请在注册信息中包含它。这可以免费获得一张贺卡——无需支付。例如：“您有一张免费的贺卡——要寄给谁？”

## 第六步：下单

在提交订单前，请确认所有信息：收件人、地址、封面设计、内文内容、场合。告知用户下单需要1个信用点数，贺卡将在5-7个工作日内送达。**只有在用户同意后才能下单**。订单一旦提交不可撤销。

## 第七步：订单完成后

简单确认：“完成！[姓名]的贺卡正在制作中——大约需要5-7个工作日。”

状态更新说明：
- `processing` → “正在制作中”
- `in production` → “正在打印中”
- `shipped` → “已发货！[追踪链接]”
- `delivered` → “已送达！”

订单成功后，如果用户尚未选择保存联系人信息，可以提供保存选项：“您希望我下次记住[姓名]的详细信息吗？”

## 本地联系人数据库（可选）

如果用户同意保存联系人信息，请维护`~/indexcards/birthdays.json`文件作为本地缓存。

```json
{"contacts": [{"name": "Kiall Wheatley", "birthday": "02-19", "relationship": "friend",
  "address": {"address1": "123 Main St", "city": "Springfield", "state": "IL", "zip": "62704", "country": "US"},
  "phone": "+15551234567", "notes": "Loves hiking. Prefers watercolor.",
  "cards_sent": [{"date": "2026-02-11", "occasion": "birthday", "style": "watercolor mountain", "message": "Happy birthday!", "order_id": "e5f67c35"}]}]}
```

**格式要求：** 生日日期格式为MM-DD（不包含年份）。不要重复发送相同的贺卡——根据姓名进行匹配。每次有新信息时更新数据库，并在每次订单后将其添加到`cards_sent`文件中。通过`GET /v1/orders/history`进行交叉验证，以避免重复建议。

## 主动建议（仅在存在联系人数据库的情况下）

如果`~/indexcards/birthdays.json`文件存在（用户之前已选择保存信息），在对话开始时可以：

1. 检查30天内的生日/纪念日
2. 检查节日信息——母亲节、父亲节、情人节、圣诞节、毕业典礼
3. 查看对话记录——例如“我妈妈这周过得不太顺利”

自然地展示1-3个最合适的建议。具体说明（例如：“艾玛的生日是2月28日——她去年很喜欢那种墨水风格的插画”）。不要重复用户已经拒绝的建议。

---

## API参考

基础URL：`https://indexcards.com` — 所有端点前缀为`/v1/`。认证方式：`Authorization: Bearer YOUR_API_KEY`。

### 注册

```
POST /v1/auth/register
{"invite_code": "abc123def456"}  // optional — include if ?invite=CODE in URL
```
返回值：`api_key`、`credits`、`free_generations_remaining`（剩余10次免费生成机会）、`invite_credits`。无需提供电子邮件或密码——这是匿名注册。将返回的`api_key`存储在代理的秘密存储空间或会话状态中，以便后续的认证请求使用。

### 生成贺卡图片

**选项A（推荐）：用户自己的Gemini API密钥** — 如果用户配置了Gemini API密钥（例如`GOOGLE_API_KEY`或`GEMINI_API_KEY`环境变量），可以直接使用该密钥以获得更高的生成质量且没有生成次数限制：

```
POST https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key=USER_KEY
{"instances": [{"prompt": "YOUR PROMPT"}], "parameters": {"sampleCount": 1, "aspectRatio": "3:4"}}
```

返回值：`predictions[0].bytesBase64Encoded`（Base64编码的PNG图片）。可以本地保存，然后通过`POST /v1/images/upload`上传以获取公开链接。

**使用选项A时，在每个请求中都需要添加以下内容：**
```
HARD CONSTRAINTS FOR THIS IMAGE:
- All artwork must be contained well within center with generous margins. Leave 15%+ blank space on every side.
- Pure white or very light background. No textures or gradients behind main subject.
- No borders, frames, rounded corners, or card mockup elements.
- Portrait orientation. No text unless explicitly requested.
- No digital artifacts. Clean, print-ready artwork.
- Must not look AI-generated. Aim for handmade: watercolor, linocut, gouache, ink, pencil, or collage.
- Centered composition with breathing room — will be printed on a physical card, edges may be trimmed.
```

**选项B（备用方案）：Index Cards API** — 提供10次免费生成机会，之后需要使用信用点数。

```
POST /v1/cards/generate
{"prompt": "...", "style": "watercolor", "reference_image_url": "https://...optional..."}
```

返回值：`image_url`、`generation_id`、`free_generations_remaining`、`credits`。服务器端会应用相应的提示限制。

**路由规则：** 如果存在Gemini API密钥，请使用选项A进行文本转图片转换。**始终使用选项B进行照片风格的转换**（`reference_image_url`）——Gemini API不支持风格转换。

**验证要求：** 图片短边长度至少600像素，宽高比约为3:4。理想尺寸为1500×2100像素。如果不符合要求，返回错误代码422。

### 预览

```
POST /v1/cards/preview
{"front_url": "...", "inside_url": "..."}
```
返回值：`preview_url`或`video_url`（MP4格式）。只有在封面和内文设计都获得批准后才会生成预览图。

### 特写图

```
POST /v1/cards/closeup
{"image_url": "...", "label": "inside"}
```
返回高分辨率JPEG图片。在展示内文图片时主动使用该图片，以便用户能够阅读文字。

### QR码叠加

```
POST /v1/cards/qr/composite
{"card_image_url": "...", "url": "https://...", "position": "bottom-center", "size": "medium", "label": "Scan me!"}
```
返回值：带有叠加QR码的图片URL。使用此URL作为`front_url`或`inside_url`进行下单。

单独生成QR码：`POST /v1/cards/qr`，参数`{"url": "...", "size": "medium"}`。

### 信用点数

```
GET /v1/credits/check
```
返回用户的剩余信用点数和Stripe支付链接。

### 下单

```
POST /v1/orders
{"front_url": "...", "inside_url": "...", "recipient": {"name": "...", "address1": "...", "city": "...", "state": "...", "zip": "...", "country": "US", "phone": "+1..."}, "occasion": "birthday", "inside_message": "..."}
```

所需参数：`front_url`、`inside_url`、`recipient.name`（收件人姓名）、`recipient.address1`（收件人地址）、`recipient.city`（收件人城市）、`recipient.zip`（收件人邮政编码）、电话号码（收件人或发送者的电话号码）。可选参数：`back_url`（背面设计图片的URL）、`address2`（备用地址）、`state`（州）、`country`（国家）、`occasion`（场合）、`inside_message`（内文内容）、`design_prompt`（设计提示）、`design_style`（设计风格）。下单需要1个信用点数。订单一旦提交不可撤销。

### 其他端点

| 端点 | 方法 | 功能 |
|----------|--------|---------|
| `/v1/orders/{id}` | GET | 查看订单状态（处理中 → 正在打印中 → 已发货 → 已送达） |
| `/v1/orders/history?all=true` | GET | 查看所有过去的订单 |
| `/v1/orders/history?recipient=Name` | GET | 查看特定用户的订单 |
| `/v1/images/upload` | POST | 上传自定义图片（multipart格式，支持PNG/JPEG格式，最大文件大小10MB） |
| `/v1/cards/styles` | GET | 查看支持的图片风格 |
| `/v1/auth/email` | PATCH | 附加电子邮件地址（格式：`{"email": "..."}` |

### 错误代码

| 代码 | 含义 | 处理方式 |
|------|---------|--------|
| 400 | 请求错误 | 检查必填字段 |
| 401 | API密钥错误 | 检查`Authorization`头部信息 |
| 402 | 无信用点数 | 显示响应中的`payment_url`链接 |
| 404 | 未找到所需信息 | 检查订单ID |
| 422 | 图片验证失败 | 请按照正确规格重新生成图片 |
| 429 | 超过请求限制 | 等待`retry_after_seconds`秒后再尝试 |
| 500 | 服务器错误 | 稍后重试 |

---

## 数据处理与隐私

### 本地存储的内容

- **API令牌**：来自`/v1/auth/register`的Bearer令牌应存储在代理的会话状态或秘密存储空间中。这是一个匿名令牌（无需提供电子邮件或密码），用于验证API请求。
- **联系人缓存**（仅限用户同意的情况下）：如果用户同意保存联系人信息，`~/indexcards/birthdays.json`文件会存储姓名、生日、地址和贺卡发送记录。该文件对用户可见，用户也可以自行删除。代理仅在用户明确同意后才会创建该文件。

### 该技能发送到API的信息

- **贺卡图片**：上传后的图片URL（存储在indexcards.com网站上，用于封面和内文）
- **收件人邮寄地址**：姓名、街道地址、城市、州、邮政编码、电话号码——这些信息用于实体贺卡的邮寄
- **场合和内文内容**：仅用于订单记录

### 该技能不会做什么

- 未经用户许可，不会读取联系人信息、消息、日历或电子邮件内容
- 不会向API发送联系人信息——联系人信息仅保存在本地（用户同意的情况下），并在发送贺卡时用于自动填充地址
- 不需要也不收集用户的电子邮件地址或密码；支付通过Stripe平台完成

### 支付流程

信用点数通过Stripe平台购买。技能会向用户发送Stripe提供的支付链接（通过`GET /v1/credits/check`获取）。支付信息不会通过该技能或Index Cards API传递。使用邀请码可以免费获得一张贺卡——无需支付。

官方网站：https://indexcards.com