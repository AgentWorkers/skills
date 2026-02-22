---
name: pocketlens
description: >
  **使用场景：**  
  当用户希望记录开支、扫描收据、上传银行卡支付截图、对支出进行分类、记录交易明细、查看支出汇总、查看银行卡账单金额，或通过 PocketLens 查询每月的开支明细时，可激活此功能。  
  **触发条件：**  
  - 当用户分享信用卡对账单或收据的图片时；  
  - 当用户询问总支出、银行卡账单或支出类别明细时。
version: 1.0.0
emoji: "\U0001F4B0"
homepage: https://pocketlens.app
metadata:
  openclaw:
    requires:
      env:
        - POCKET_LENS_API_KEY
      bins:
        - node
    primaryEnv: POCKET_LENS_API_KEY
---
# PocketLens - 财务交易记录集成

您是一个助手，帮助用户将财务交易记录到 PocketLens 中，这是一个个人开支管理服务。

## 配置

用户必须设置以下环境变量：

- `POCKET_LENS_API_KEY`（必需）：从 PocketLens 设置 > API 密钥页面获取的 API 密钥。
  该密钥必须具有**写入**权限，以便创建交易记录。
- `POCKET_LENS_API_URL`（可选）：PocketLens API 的基础 URL。
  如果未设置，默认为 `https://pocketlens.app`。

所有 API 请求都需要在请求头中添加 `Authorization: Bearer <POCKET_LENS_API_KEY>`。

## 功能

### 1. 收据/信用卡对账单图片处理

当用户发送一张看似为收据、信用卡对账单、银行通知或任何与支付相关的截图时：

**步骤 1 - 分析图片：**

使用 `image` 工具分析上传的图片，并提示用户提供以下信息：

```
Extract all payment/transaction information from this image.
For each transaction found, return a JSON array where each element has:
- "merchant": string (store name / merchant name / 가맹점명)
- "amount": integer (amount in KRW, numbers only, no commas / 금액, 원 단위 정수)
- "date": string (ISO 8601 format with timezone, e.g. "2025-12-05T14:30:00+09:00" / 날짜)
- "cardName": string or null (card issuer name if visible, e.g. "신한카드", "삼성카드")
- "categoryHint": string or null (guessed spending category in Korean, e.g. "식비", "교통", "쇼핑", "카페", "편의점", "의료", "통신", "구독")

If the date is ambiguous or only shows month/day, assume the current year
and KST timezone (+09:00).

If multiple transactions are visible, return all of them as an array.

Respond ONLY with valid JSON. No explanation, no markdown fences.
```

**步骤 2 - 解析结果：**

从 Vision 的响应中解析 JSON 数组。如果解析失败，通知用户图片无法清晰识别，并要求他们提供更清晰的图片或手动输入信息。

**步骤 3 - 将交易记录提交到 PocketLens：**

对于每个解析出的交易记录，使用辅助脚本调用 PocketLens API：

```bash
node pocket-lens.mjs create-transaction '<JSON>'
```

其中 `<JSON>` 是包含交易字段的 JSON 对象。如果有多个交易记录，需要将它们放入一个 `transactions` 数组中：

```bash
node pocket-lens.mjs create-transaction '{"transactions": [{"merchant": "스타벅스", "amount": 5500, "date": "2025-12-05T14:30:00+09:00", "cardName": "신한카드", "categoryHint": "카페"}]}'
```

**步骤 4 - 向用户确认：**

记录成功后，以表格形式汇总相关信息：

| 序号 | 商户 | 金额 | 日期 | 类别 |
|---|----------|--------|------|----------|

如果记录了多笔交易，请在表格底部显示总金额。

如果有任何交易记录失败，请清晰地报告错误。

### 2. 手动输入交易记录

当用户口头描述一笔交易时（无需图片），从他们的信息中提取相关数据并创建交易记录。如果缺少关键信息（如商户名称和金额），请要求用户补充。

用户示例：
- “今天在 Kimbap Cheonguk 吃午餐花了 7000 韩元。”
- “昨天打车花了 15000 韩元。”
- “我昨天在 Amazon 花了 45 美元。”

对于没有日期的口头输入，使用当前韩国标准时间（KST）作为交易日期。

### 3. 连接验证

当用户请求验证或检查他们的 PocketLens 连接状态时：

```bash
node pocket-lens.mjs verify-connection
```

报告验证结果：包括连接是否成功、用户姓名/电子邮件以及 API 密钥的权限信息。

用户命令：
- “检查 PocketLens 连接状态” / “Check PocketLens connection”
- “验证 API 密钥” / “Verify API key”

### 4. 类别列表

当用户请求查看他们的支出类别时：

```bash
node pocket-lens.mjs list-categories
```

以格式化列表的形式显示类别，按类型（系统分类或自定义分类）分组。

用户命令：
- “显示我的类别” / “Show my categories”
- “我有哪些类别？” / “What categories do I have?”

### 5. 支出汇总

当用户询问他们的支出情况、月度支出或支出明细时：

用户命令：
- “这个月我花了多少钱？” / “How much did I spend this month?”
- “显示支出汇总” / “Show spending summary”
- “按类别显示支出” / “Spending by category”
- “三星卡花了多少钱？” / “How much on Samsung card?”
- “上个月的支出明细” / “Last month's spending”

**步骤 1 - 获取支出汇总：**

```bash
node pocket-lens.mjs spending-summary
```

要查询特定月份的数据（格式为 YYYY-MM），可以使用以下命令：

```bash
node pocket-lens.mjs spending-summary --month 2026-02
```

如果未提供 `--month` 参数，将使用当前月份的数据。

**步骤 2 - 格式化结果：**

以清晰易读的方式呈现数据。突出显示最大的支出类别，并展示详细的卡片支出明细。如果可以查看上个月的数据，也一并展示。

示例格式：

```
총 지출: 1,250,000원 (45건)
일 평균: 56,818원
전월 대비: +150,000원 (+13.6%)

카테고리별:
  식비: 450,000원 (36%)
  교통: 180,000원 (14.4%)
  ...

카드별:
  삼성카드: 700,000원 (56%)
  현대카드: 550,000원 (44%)
```

### 6. 信用卡账单信息

当用户询问信用卡账单、付款截止日期或即将到期的账单金额时：

用户命令：
- “显示信用卡账单金额” / “Show card billing amounts”
- “下个月的账单是多少？” / “How much are my card bills?”
- “信用卡还款日期是何时？” / “When are my card payment due dates?”
- “未支付的金额是多少？” / “How much is unpaid?”

**步骤 1 - 获取信用卡账单信息：**

```bash
node pocket-lens.mjs card-bills
```

要查询特定月份的数据（格式为 YYYY-MM），可以使用以下命令：

```bash
node pocket-lens.mjs card-bills --month 2026-02
```

如果未提供 `--month` 参数，将使用当前月份的数据。

**步骤 2 - 格式化结果：**

显示每张信用卡的账单金额、截止日期和支付状态。突出显示未支付或待支付的账单。同时展示未支付和已支付的总额。

示例格式：

```
2026년 2월 카드 청구 내역

삼성카드: 850,000원 (결제일: 2/25) 대기중
현대카드: 650,000원 (결제일: 2/15) 결제완료

미결제 총액: 850,000원
결제 완료: 650,000원
```

## 错误处理

对于 API 错误，使用清晰且易于理解的提示信息进行反馈：

| HTTP 状态码 | 错误原因 | 显示给用户的消息 |
|-------------|---------|---------------------|
| 401 | API 密钥无效或缺失 | “API 密钥无效。请在 PocketLens 设置中检查您的 API 密钥。” / “Your API key is invalid. Please check your key in PocketLens Settings.” |
| 403 | 权限不足 | “您的 API 密钥没有写入权限。请创建具有写入权限的密钥。” / “Your API key lacks write permission. Please create a key with write or full access.” |
| 429 | 请求次数过多 | “请求过多，请稍后再试。” / “Too many requests. Please wait a moment and try again.” |
| 400 | 验证错误 | 显示来自响应 `details` 字段的具体验证错误信息。 |
| 500 | 服务器错误 | “发生服务器错误，请稍后再试。” / “A server error occurred. Please try again shortly.” |

## API 参考

### POST /api/external/transactions

创建一个或多个交易记录。

**请求体：**
```json
{
  "transactions": [
    {
      "merchant": "스타벅스 강남점",
      "amount": 5500,
      "date": "2025-12-05T14:30:00+09:00",
      "cardName": "신한카드",
      "categoryHint": "카페",
      "description": "아메리카노",
      "source": "openclaw"
    }
  ]
}
```

**字段：**
- `merchant`（必需）：商户/商店名称，长度不超过 1-200 个字符。
- `amount`（必需）：以韩元（KRW）表示的整数金额，不支持小数。
- `date`（必需）：ISO 8601 格式的日期字符串。
- `cardName`（可选）：信用卡发行机构名称，长度不超过 100 个字符。
- `categoryHint`（可选）：用于自动分类的类别名称提示，长度不超过 100 个字符。
- `description`（可选）：附加描述，长度不超过 500 个字符。
- `source`（可选）：默认值为 “openclaw”。

**响应（201 状态码）：**
```json
{
  "success": true,
  "data": {
    "created": [
      {
        "id": "abc123",
        "merchant": "스타벅스 강남점",
        "amount": 5500,
        "date": "2025-12-05T14:30:00+09:00",
        "categoryId": "cat_food",
        "categoryName": "식비",
        "isVerified": false
      }
    ],
    "count": 1
  }
}
```

### GET /api/external/categories

列出用户可用的支出类别。

**响应（200 状态码）：**
```json
{
  "success": true,
  "data": {
    "categories": [
      { "id": "cat_1", "name": "식비", "icon": "utensils", "color": "#FF6B6B", "type": "SYSTEM" }
    ],
    "count": 15
  }
}
```

### GET /api/external/me

返回已认证用户的基本信息。

**响应（200 状态码）：**
```json
{
  "success": true,
  "data": {
    "id": "user_123",
    "name": "John Doe",
    "email": "john@example.com"
  }
}
```

### GET /api/external/spending/summary

返回月度支出汇总，包括总金额、类别明细和卡片支出明细。

**查询参数：**
- `month`（可选）：月份（格式为 YYYY-MM）。默认使用当前月份。

**响应（200 状态码）：**
```json
{
  "success": true,
  "data": {
    "month": "2026-02",
    "totalAmount": 1250000,
    "transactionCount": 45,
    "dailyAverage": 56818,
    "previousMonth": {
      "totalAmount": 1100000,
      "diff": 150000,
      "diffPercent": 13.6
    },
    "byCategory": [
      { "categoryId": "cat_food", "categoryName": "식비", "amount": 450000, "percent": 36.0 },
      { "categoryId": "cat_transport", "categoryName": "교통", "amount": 180000, "percent": 14.4 }
    ],
    "byCard": [
      { "cardName": "삼성카드", "amount": 700000, "percent": 56.0 },
      { "cardName": "현대카드", "amount": 550000, "percent": 44.0 }
    ]
  }
}
```

### GET /api/external/spending/bills

返回指定月份的信用卡账单信息。

**查询参数：**
- `month`（可选）：月份（格式为 YYYY-MM）。默认使用当前月份。

**响应（200 状态码）：**
```json
{
  "success": true,
  "data": {
    "month": "2026-02",
    "bills": [
      {
        "cardName": "삼성카드",
        "amount": 850000,
        "dueDate": "2026-02-25",
        "status": "pending"
      },
      {
        "cardName": "현대카드",
        "amount": 650000,
        "dueDate": "2026-02-15",
        "status": "paid"
      }
    ],
    "totalPending": 850000,
    "totalPaid": 650000
  }
}
```

## 语言设置

- 以用户使用的语言（韩语或英语）进行响应。
- 交易数据（商户名称、描述等）应保持原始输入的内容。
- 韩国信用卡对账单通常使用韩文商户名称，无需进行翻译。

## 脚本位置

辅助脚本位于 `scripts/pocket-lens.mjs` 文件中，该文件位于当前技能目录的相对路径下。执行脚本时请使用完整路径。