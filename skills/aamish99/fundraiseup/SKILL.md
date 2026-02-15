---
name: fundraiseup
description: 与 FundraiseUp 的 REST API 进行交互，以管理捐赠、定期捐赠计划、支持者信息、筹款活动以及捐赠者门户的访问权限。处理线上和线下的捐赠请求，获取筹款数据分析结果，并与非营利组织的 CRM 系统进行集成。
compatibility: 
  - bash_tool
  - web_search
  - web_fetch
metadata:
  author: Amish
  version: 1.0.0
  api_version: v1
  tags:
    - fundraising
    - donations
    - nonprofit
    - payments
    - crm-integration
    - stripe
---

# FundraiseUp API 技能

## 概述
该技能使 Claude 能够与 FundraiseUp 的 REST API 进行交互，以处理捐款、管理定期付款计划、检索支持者信息以及访问筹款分析数据。FundraiseUp 是一个数字筹款平台，允许非营利组织从各种渠道接收捐款。

## 配置
所需的环境变量：


```FUNDRAISEUP_API_KEY ```


- API 密钥（例如：`ABEDDDD_XSSSHwzZc98KR53CWQeWeclA`）

## 基本 URL
```
https://api.fundraiseup.com/v1
```

## 认证

### API 密钥生成
1. 转到“仪表板”>“设置”>“API 密钥”
2. 单击“创建 API 密钥”
3. 输入一个描述性名称
4. 选择数据模式：
   - **实时数据**：用于生产环境
   - **测试数据**：用于测试（密钥前缀为 `test_`）
5. 选择权限：
   - 检索捐款数据
   - 创建新的捐款
   - 生成捐赠者门户访问链接
6. 安全保存 API 密钥（仅显示一次）

### 认证头
所有 API 请求都必须包含带有 Bearer 令牌的 `Authorization` 头：

```bash
Authorization: Bearer YOUR_API_KEY
```

### 重要说明
- API 密钥是针对特定账户/子账户设置的
- 父账户的 API 密钥无法为子账户创建捐款
- 只有组织管理员才能创建 API 密钥
- 严禁公开 API 密钥

## 速率限制
- **每秒 8 次请求**
- **每分钟 128 次请求**
- 实现指数退避算法来处理速率限制

## 必需的头部信息
```bash
Content-Type: application/json
Accept: application/json
Authorization: Bearer YOUR_API_KEY
```

---

## API 端点

### 1. 捐款

#### 列出捐款
**端点：**`GET /donations`

**描述：**检索所有捐款，并支持基于游标的分页。

**查询参数：**
- `limit`（可选）：每页记录数（1-100，默认：10）
- `starting_after`（可选）：分页的游标（捐款 ID）
- `ending_before`（可选）：反向分页的游标（捐款 ID）
- 注意：`starting_after` 和 `ending_before` 是互斥的

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/donations?limit=50' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

**响应字段：**
- `id`：捐款标识符
- `created_at`：ISO 8601 时间戳
- `livemode`：布尔值（true 表示实时数据，false 表示测试数据）
- `amount`：捐款金额（以选定货币表示）
- `amount_in_default_currency`：以组织默认货币表示的金额
- `currency`：三位字母的 ISO 代码（小写）
- `status`：捐款状态（例如：成功、待处理、失败）
- `campaign`：活动详情（ID、代码、名称）
- `supporter`：支持者信息
- `recurring_plan`：定期付款计划详情（如适用）
- `designation`：捐款用途
- `tribute`：致敬信息（如果提供）
- `custom_fields`：自定义字段值数组
- `processing_fee`：处理费用详情
- `platform_fee`：平台费用详情
- `fees_covered`：捐赠者支付的费用金额

---

#### 获取单个捐款
**端点：**`GET /donations/{id}`

**描述：**检索特定捐款的详细信息。

**路径参数：**
- `id`（必需）：捐款 ID

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/donations/DFQLCFEP' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

---

#### 创建捐款
**端点：**`POST /donations`

**描述：**创建一次性或定期捐款。通过 API 创建的捐款将显示“API”作为捐款来源。

**前提条件：**
- 已将 Stripe 账户连接到 FundraiseUp 并激活
- 活动已启用基于货币的支付方式
- 拥有“创建新的捐款”权限的 API 密钥
- 拥有 Stripe 支付方式 ID（通过 Stripe API 创建）
- 符合 PCI 合规要求

**请求体：**
```json
{
  "campaign_id": "FUNCPJTZZQR",
  "amount": "25.00",
  "currency": "usd",
  "payment_method_id": "pm_1234567890abcdef",
  "supporter": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+1234567890",
    "mailing_address": {
      "line1": "123 Main St",
      "line2": "Apt 4B",
      "city": "New York",
      "region": "NY",
      "postal_code": "10001",
      "country": "us"
    }
  },
  "recurring_plan": {
    "frequency": "monthly"
  },
  "designation": [
    {
      "id": "EHHJ9R36"
    }
  ],
  "tribute": {
    "type": "in_honor_of",
    "honoree": "Jane Smith"
  },
  "comment": "Monthly donation for general fund",
  "anonymous": false,
  "custom_fields": [
    {
      "name": "referral_source",
      "value": "Email Campaign"
    }
  ]
}
```

**必填字段：**
- `campaign_id`：必须属于该账户并且是活动的活动
- `amount`：十进制字符串（例如：`9.99` 表示 USD，`200` 表示 JPY），最低金额为 $1 或等值
- `currency`：三位字母的 ISO 代码（小写）
- `payment_method_id`：Stripe 支付方式 ID
- `supporter.first_name`：最多 256 个字符
- `supporter.last_name`：最多 256 个字符
- `supporter.email`：有效的电子邮件地址（API 不进行验证）
- `supporter.phone`：最多 20 个字符（如果活动需要）
- `supporter.mailing_address`：如果活动需要，则必须提供

**可选字段：**
- `recurring_plan.frequency`：创建定期付款计划（“monthly”、“weekly”、“quarterly”、“yearly”、“daily”）
- `designation`：捐款用途 ID 数组
- `tribute.type`：`in_honor_of` 或 `in_memory_of`
- `tribute.honoree`：受尊敬的人的名字
- `comment`：捐款备注
- `anonymous`：布尔值（默认：false）
- `custom_fields`：自定义字段对象数组

**示例请求：**
```bash
curl --request POST \
  --url 'https://api.fundraiseup.com/v1/donations' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}' \
  --header 'Content-Type: application/json' \
  --data '{
    "campaign_id": "FUNCPJTZZQR",
    "amount": "50.00",
    "currency": "usd",
    "payment_method_id": "pm_1234567890",
    "supporter": {
      "first_name": "Jane",
      "last_name": "Smith",
      "email": "jane@example.com"
    }
  }'
```

**重要说明：**
- 所有字符串参数都会被截断；空字符串将转换为 null
- 地址和电子邮件地址不会被格式化或验证
- 目前仅支持信用卡支付
- 费用可能最初显示为 0，直到 Stripe 完成处理（使用 Events 端点获取最终费用）

---

#### 更新捐款
**端点：**`PATCH /donations/{id}`

**描述：**更新捐款。仅允许在创建后的 24 小时内更新，并且仅适用于通过 API 创建的捐款。

**路径参数：**
- `id`（必需）：捐款 ID

**限制：**
- 仅能更新通过 API 创建的捐款
- 更新必须在创建后的 24 小时内进行
- 不支持批量更新

---

### 2. 定期付款计划

#### 列出定期付款计划
**端点：**`GET /recurring_plans`

**描述：**检索所有定期付款计划。

**查询参数：**
- `limit`（可选）：每页记录数（1-100）
- `starting_after`（可选）：分页的游标
- `ending_before`（可选）：反向分页的游标

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/recurring_plans?limit=50' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

**响应字段：**
- `id`：定期付款计划标识符
- `created_at`：ISO 8601 时间戳
- `frequency`：“monthly”、“weekly”、“quarterly”、“yearly”或“daily”
- `amount`：定期付款金额
- `currency`：三位字母的 ISO 代码
- `status`：计划状态（活动、暂停、取消）
- `next_installment_at`：下一次预定捐款日期
- `ended_at`：结束日期（如果设置）
- `campaign`：关联的活动详情
- `supporter`：支持者信息

---

#### 获取单个定期付款计划
**端点：**`GET /recurring_plans/{id}`

**描述：**检索特定定期付款计划的详细信息。

**路径参数：**
- `id`（必需）：定期付款计划 ID

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/recurring_plans/RVSHJNPJ' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

---

#### 更新定期付款计划
**端点：**`PATCH /recurring_plans/{id}`

**描述：**更新定期付款计划。仅允许在创建后的 24 小时内更新，并且仅适用于通过 API 创建的计划。

---

### 3. 支持者

#### 列出支持者
**端点：**`GET /supporters`

**描述：**检索所有支持者/捐款人。

**查询参数：**
- `limit`（可选）：每页记录数（1-100）
- `starting_after`（可选）：分页的游标
- `ending_before`（可选）：反向分页的游标

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/supporters?limit=50' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

**响应字段：**
- `id`：支持者标识符
- `created_at`：ISO 8601 时间戳
- `email`：电子邮件地址
- `first_name`：名字
- `last_name`：姓氏
- `phone`：电话号码
- `mailing_address`：地址详情
- `mailing_list_subscribed`：布尔值
- `anonymous`：布尔值
- `employer`：雇主名称（如果提供）

---

#### 获取单个支持者
**端点：**`GET /supporters/{id}`

**描述：**检索特定支持者的详细信息。

**路径参数：**
- `id`（必需）：支持者 ID

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/supporters/SXXXXXXX' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

---

### 4. 事件
**端点：**`GET /events`

**描述：**检索捐款、定期付款计划和支持者的审计日志事件。

**查询参数：**
- `limit`（可选）：每页记录数（1-100）
- `starting_after`（可选）：分页的游标
- `ending_before`（可选）：反向分页的游标

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/events?limit=50' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

**用例：**
- 跟踪费用何时最终确定（查找 `donation.success` 事件）
- 监控状态变化
- 审计追踪以确保合规性
- 集成调试

---

### 5. 活动
**端点：**`GET /campaigns`

**描述：**检索所有活动。

**查询参数：**
- `limit`（可选）：每页记录数（1-100）
- `starting_after`（可选）：分页的游标
- `ending_before`（可选）：反向分页的游标

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/campaigns' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

**响应字段：**
- `id`：活动标识符
- `code`：活动代码
- `name`：活动名称
- `status`：活动状态

---

#### 获取单个活动
**端点：**`GET /campaigns/{id}`

**路径参数：**
- `id`（必需）：活动 ID

---

### 6. 捐款用途
**端点：**`GET /designations`

**描述：**检索所有捐款用途。

**示例请求：**
```bash
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/designations' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

---

### 7. 捐赠者门户访问

#### 生成支持者门户链接
**端点：**`POST /donor_portal/access_links/supporters/{id}`

**描述：**生成一个安全链接，让支持者无需登录即可访问他们的捐赠者门户。

**路径参数：**
- `id`（必需）：支持者 ID

**前提条件：**
- 拥有启用“生成捐赠者门户访问链接”权限的 API 密钥

**示例请求：**
```bash
curl --request POST \
  --url 'https://api.fundraiseup.com/v1/donor_portal/access_links/supporters/64b0ba9d9a19ea001fa3516a' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

**响应：**
```json
{
  "url": "https://yourorg.org/login/?auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**重要安全说明：**
- 链接仅有效期为 **1 分钟**
- 仅应在捐赠者门户内使用
- **严禁** 通过电子邮件、短信或公共渠道分享
- 提供对敏感数据（支付方式、捐款历史、收据）的访问权限
- 在生成链接之前验证支持者的身份
- 实现自动重定向（无需手动操作）

#### 生成定期付款计划门户链接
**端点：**`POST /donor_portal/access_links/recurring_plans/{id}`

**描述：**生成一个链接，让支持者可以访问特定的定期付款计划。

**路径参数：**
- `id`（必需）：定期付款计划 ID

**可选查询参数：**
- `return_url`（可选）：管理定期付款计划后返回的 URL

**示例请求：**
```bash
curl --request POST \
  --url 'https://api.fundraiseup.com/v1/donor_portal/access_links/recurring_plans/RVSHJNPJ' \
  --header 'Accept: application/json' \
  --header 'Authorization: Bearer {{FUNDRAISEUP_API_KEY}}'
```

**响应：**
```json
{
  "url": "https://yourorg.org/login/?auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## 分页最佳实践
所有列表端点都使用基于游标的分页：

1. **初始请求：**设置 `limit` 参数（1-100）
2. **下一页：**使用上一个记录的 `id` 作为 `starting_after`
3. **上一页：**使用第一个记录的 `id` 作为 `ending_before`
4. **排序：**按创建日期（最新优先），然后按 ID（Z 到 A）排序

**示例分页流程：**
```bash
# Page 1
GET /donations?limit=50

# Page 2 (use last donation ID from page 1)
GET /donations?limit=50&starting_after=LAST_DONATION_ID

# Previous page
GET /donations?limit=50&ending_before=FIRST_DONATION_ID
```

## 错误处理

### 标准 HTTP 响应代码
- `200 OK`：GET 请求成功
- `201 Created`：POST 请求成功
- `400 Bad Request`：请求参数无效
- `401 Unauthorized`：缺少或无效的 API 密钥
- `403 Forbidden`：权限不足
- `404 Not Found`：资源未找到
- `429 Too Many Requests`：超出速率限制
- `500 Internal Server Error`：服务器错误

### 最佳实践
1. 实现指数退避算法来处理速率限制
2. 记录所有 API 错误及其请求详情
3. 在发送到 API 之前验证数据
4. 优雅地处理空值
5. 使用 Events 端点检查最终费用

---

## 代码示例

### Python 示例
```python
import requests
import os

API_KEY = os.environ.get('FUNDRAISEUP_API_KEY')
BASE_URL = 'https://api.fundraiseup.com/v1'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# List donations
def get_donations(limit=50):
    url = f'{BASE_URL}/donations'
    params = {'limit': limit}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# Create donation
def create_donation(campaign_id, amount, currency, payment_method_id, supporter):
    url = f'{BASE_URL}/donations'
    data = {
        'campaign_id': campaign_id,
        'amount': str(amount),
        'currency': currency,
        'payment_method_id': payment_method_id,
        'supporter': supporter
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

# Get single donation
def get_donation(donation_id):
    url = f'{BASE_URL}/donations/{donation_id}'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
```

### Node.js 示例
```javascript
const axios = require('axios');

const API_KEY = process.env.FUNDRAISEUP_API_KEY;
const BASE_URL = 'https://api.fundraiseup.com/v1';

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Accept': 'application/json',
  'Content-Type': 'application/json'
};

// List donations
async function getDonations(limit = 50) {
  const response = await axios.get(`${BASE_URL}/donations`, {
    headers,
    params: { limit }
  });
  return response.data;
}

// Create donation
async function createDonation(campaignId, amount, currency, paymentMethodId, supporter) {
  const response = await axios.post(`${BASE_URL}/donations`, {
    campaign_id: campaignId,
    amount: amount.toString(),
    currency,
    payment_method_id: paymentMethodId,
    supporter
  }, { headers });
  return response.data;
}

// Get single donation
async function getDonation(donationId) {
  const response = await axios.get(`${BASE_URL}/donations/${donationId}`, { headers });
  return response.data;
}
```

### 使用环境变量的 cURL 示例
```bash
# Set your API key as environment variable
export FUNDRAISEUP_API_KEY="your_api_key_here"

# List donations
curl --request GET \
  --url 'https://api.fundraiseup.com/v1/donations?limit=50' \
  --header "Accept: application/json" \
  --header "Authorization: Bearer $FUNDRAISEUP_API_KEY"

# Create donation
curl --request POST \
  --url 'https://api.fundraiseup.com/v1/donations' \
  --header "Accept: application/json" \
  --header "Authorization: Bearer $FUNDRAISEUP_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
    "campaign_id": "FUNCPJTZZQR",
    "amount": "25.00",
    "currency": "usd",
    "payment_method_id": "pm_1234567890",
    "supporter": {
      "first_name": "John",
      "last_name": "Doe",
      "email": "john@example.com"
    }
  }'

# Get single donation
curl --request GET \
  --url "https://api.fundraiseup.com/v1/donations/DFQLCFEP" \
  --header "Accept: application/json" \
  --header "Authorization: Bearer $FUNDRAISEUP_API_KEY"
```

## 测试

### 测试模式
- 使用“测试数据”模式生成 API 密钥
- 测试密钥前缀为 `test_`
- 测试模式数据不会影响实时数据或银行网络
- 使用测试 Stripe 支付方式创建测试捐款

### 测试用的 URL 参数
在任何 URL 中添加 `fundraiseupLivemode=no` 以进行测试，而不会处理实际捐款

## 集成模式

### 历史数据同步
1. 使用 `limit` 参数分批获取数据（建议：50-100）
2. 使用上一个记录的 ID 作为下一次批处理的 `starting_after`
3. 顺序处理批次数据
4. 实现错误处理和重试逻辑

### 实时轮询
1. 定期轮询 API（遵守速率限制）
2. 使用 Events 端点跟踪变化
3. 存储最后处理的记录 ID
4. 使用 `starting_after` 仅获取新记录

### 基于事件的集成
- 使用 Zapier 进行事件触发（FundraiseUp 不支持直接 Webhook）
- 配置 Zapier 以在 FundraiseUp 事件发生时触发
- 根据事件在系统中触发同步任务

## 常见用例

1. **处理离线捐款**
   - 面对面筹款
   - 直接邮件捐款
   - 慈善晚会捐款
   - 活动注册

2. **CRM 集成**
   - 将捐款数据同步到 CRM（Salesforce、HubSpot 等）
   - 更新支持者记录
   - 跟踪定期付款计划
   - 生成报告

3. **分析和报告**
   - 将捐款数据导出到 BI 工具
   - 跟踪活动表现
   - 分析捐赠者行为
   - 计算终身价值

4. **捐赠者门户集成**
   - 从自定义门户实现无缝认证
   - 直接访问定期付款计划管理
   - 单点登录体验

## 安全最佳实践

1. **API 密钥管理**
   - 将 API 密钥存储在环境变量中（切勿硬编码）
   - 为不同的集成使用不同的密钥
   - 定期轮换密钥
   - 立即撤销被泄露的密钥

2. **仅使用 HTTPS**
   - 所有请求都必须使用 HTTPS
   - HTTP 请求将被拒绝

3. **数据验证**
   - 在发送到 API 之前验证所有输入
   - 清理用户提供的数据
   - 在处理之前检查响应数据

4. **PCI 合规**
   - 不要在应用程序中处理原始卡数据
   - 使用 Stripe 支付方式 API 处理卡支付
   - 符合 PCI DSS 要求（对于直接 API 集成，请使用 SAQ D）
   - 考虑使用 Stripe Elements 以减少 PCI 范围

5. **捐赠者门户安全**
   - 在生成访问链接之前验证支持者的身份
   - 使用自动重定向（无需手动链接）
   **严禁** 通过电子邮件或公共渠道分享访问链接
   - 访问链接在 1 分钟后过期

## 限制和注意事项

1. **支付方式：**目前仅支持信用卡
2. **更新：**仅允许在创建后的 24 小时内进行，且仅适用于通过 API 创建的记录
3. **批量操作：**不支持批量更新
4. **Webhook：**不支持直接 Webhook（使用 Zapier 进行事件触发）
5. **子账户：**父账户的 API 密钥无法为子账户创建捐款
6. **费用计算：**费用可能最初显示为 0；使用 Events 端点获取最终费用
7. **地址验证：**API 不会格式化或验证地址
8. **电子邮件验证：**API 不会验证电子邮件地址
9. **迁移：**REST API 不是迁移机制（使用迁移服务）

## 其他资源

- 官方文档：https://fundraiseup.com/docs/rest-api/
- API 资源：https://fundraiseup.com/docs/rest-api-resources/
- 捐赠者门户集成：https://fundraiseup.com/docs/seamless-donor-portal/
- 支持：https://fundraiseup.com/support/

## 故障排除

### 常见问题

**401 Unauthorized**
- 检查 API 密钥是否正确且有效
- 验证 Authorization 头的格式
- 确保 API 密钥具有所需的权限

**429 超出速率限制**
- 实现指数退避算法
- 减少请求频率
- 尽可能进行批量操作

**400 Bad Request**
- 验证所有必需字段是否齐全
- 检查数据类型和格式
- 确保货币代码是小写
- 验证金额格式（十进制字符串）

**费用显示为 0**
- 费用是异步完成的
- 使用 Events 端点获取最终费用
- 查找 `donation.success` 事件

**无法更新捐款**
- 验证捐款是否是通过 API 创建的
- 确保更新在创建后的 24 小时内进行
- 检查 API 密钥权限

## 版本信息
- API 版本：v1
- 最后更新时间：2026 年 2 月
- 支持的支付方式：仅支持信用卡