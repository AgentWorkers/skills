# OpenClaw 的 Zoho API 技能

这是一项用于认证和与 Zoho API（包括 CRM、Books、Desk、Creator 等）进行交互的全面技能。

## 概述

Zoho 是一个商业 SaaS 平台，提供以下服务：
- **Zoho CRM**：销售和联系人管理
- **Zoho Books**：会计和发票管理
- **Zoho Desk**：客户支持工单管理
- **Zoho Creator**：低代码应用程序开发
- **Zoho Campaigns**：电子邮件营销
- **Zoho Inventory**：库存管理
- **Zoho Projects**：项目管理
- 以及 50 多个其他商业应用程序！

该技能支持使用安全的 OAuth2 进行认证，并能与所有 Zoho 产品进行 API 交互。

## 设置

### 1. 创建 Zoho API 客户端

**步骤 1：** 访问 Zoho 开发者控制台
🔗 https://api-console.zoho.com/

**步骤 2：** 创建新客户端
- 点击“添加客户端”
- 选择“基于服务器的应用程序”（推荐）
- 填写以下信息：
  - 客户端名称：OpenClaw-Zoho
  - 主页 URL：https://openclaw.ai
  - 授权重定向 URI：https://openclaw.ai/callback

**步骤 3：** 复制您的凭据
- **客户端 ID：** `xxxxxx`
- **客户端密钥：** `xxxxxx`

---

### 2. 生成刷新令牌

**步骤 1：** 构建 OAuth URL
```bash
# Replace values in brackets []
https://accounts.zoho.com/oauth/v2/auth?
scope=ZohoCRM.modules.ALL&
client_id=[YOUR_CLIENT_ID]&
response_type=code&
access_type=offline&
redirect_uri=[YOUR_REDIRECT_URI]
```

**步骤 2：** 在浏览器中打开该 URL
- 您将被重定向到 Zoho 登录页面
- 点击“接受”以授权

**步骤 3：** 从重定向 URL 中复制授权代码

**步骤 4：** 将代码兑换为令牌
```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=authorization_code" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "redirect_uri=$ZOHO_REDIRECT_URI" \
  -d "code=[AUTHORIZATION_CODE]"
```

**响应：**
```json
{
  "access_token": "1000.xxxxxx",
  "expires_in": 3600,
  "refresh_token": "1000.xxxxxx"
}
```

**步骤 5：** 安全地保存刷新令牌！

---

### 3. 设置环境变量

创建一个 `.env` 文件或在系统中设置以下变量：

```bash
# Required
export ZOHO_CLIENT_ID="your-client-id"
export ZOHO_CLIENT_SECRET="your-client-secret"
export ZOHO_REFRESH_TOKEN="your-refresh-token"

# Optional (defaults shown)
export ZOHO_DATA_CENTER="com"  # com, eu, cn, au, in, jp
export ZOHO_REDIRECT_URI="https://openclaw.ai/callback"
```

**数据中心：**
| 代码 | 地区 |
|------|--------|
| com | 美国（默认） |
| eu | 欧洲 |
| cn | 中国 |
| au | 澳大利亚 |
| in | 印度 |
| jp | 日本 |

---

### 4. 生成访问令牌

Zoho 访问令牌的有效期为 **1 小时**。请始终使用刷新令牌：

```bash
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=refresh_token" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "refresh_token=$ZOHO_REFRESH_TOKEN"
```

**响应：**
```json
{
  "access_token": "1000.xxxxxx",
  "expires_in": 3600
}
```

---

## Zoho CRM API

### 基础 URL

| 数据中心 | 基础 URL |
|-------------|----------|
| 美国 | `https://www.zohoapis.com/crm/v2` |
| 欧洲 | `https://www.zohoapis.eu/crm/v2` |
| 澳大利亚 | `https://www.zohoapis.com.au/crm/v2` |
| 印度 | `https://www.zohoapis.in/crm/v2` |

---

### 🔍 获取所有模块

```bash
curl -X GET "[BASE_URL]/settings/modules" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

### 👥 CRM 营销线索管理

#### 获取所有营销线索

```bash
curl -X GET "[BASE_URL]/Leads" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

**响应：**
```json
{
  "data": [
    {
      "id": "1234567890",
      "Company": "South Indian AB",
      "Last_Name": "Ravi",
      "First_Name": "Customer",
      "Email": "customer@example.com",
      "Phone": "+46700000000",
      "Status": "Not Contacted"
    }
  ],
  "info": {
    "page": 1,
    "per_page": 200,
    "total_count": 50
  }
}
```

---

#### 创建新营销线索

```bash
curl -X POST "[BASE_URL]/Leads" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "Company": "South Indian AB",
        "Last_Name": "Ravi",
        "First_Name": "Customer",
        "Email": "customer@example.com",
        "Phone": "+46700000000",
        "Lead_Source": "Website",
        "Industry": "Technology"
      }
    ]
  }'
```

---

#### 更新营销线索

```bash
curl -X PUT "[BASE_URL]/Leads/[LEAD_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "Phone": "+46709999999",
        "Status": "Contacted"
      }
    ]
  }'
```

---

#### 删除营销线索

```bash
curl -X DELETE "[BASE_URL]/Leads/[LEAD_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

### 💼 CRM 交易管理

#### 创建交易

```bash
curl -X POST "[BASE_URL]/Deals" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "Deal_Name": "Annual Software License - South Indian AB",
        "Amount": 50000,
        "Closing_Date": "2026-03-31",
        "Stage": "Needs Analysis",
        "Pipeline": "Standard",
        "Account_Name": "1234567890"
      }
    ]
  }'
```

---

#### 按阶段获取交易

```bash
curl -X GET "[BASE_URL]/Deals?stage=Closed Won" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

### 👤 CRM 联系人管理

#### 创建联系人

```bash
curl -X POST "[BASE_URL]/Contacts" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "First_Name": "Ravi",
        "Last_Name": "Senthazal",
        "Email": "ravi@example.com",
        "Phone": "+46701234567",
        "Mailing_Street": "Drottninggatan 1",
        "Mailing_City": "Stockholm",
        "Mailing_Country": "Sweden"
      }
    ]
  }'
```

---

### 🏢 CRM 客户/公司管理

#### 创建客户

```bash
curl -X POST "[BASE_URL]/Accounts" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "Name": "South Indian Restaurant AB",
        "Phone": "+4681234567",
        "Website": "https://southindian.se",
        "Industry": "Restaurant",
        "Billing_City": "Stockholm",
        "Billing_Country": "Sweden",
        "Type": "Customer"
      }
    ]
  }'
```

---

### 📝 CRM 备注和活动

#### 为记录添加备注

```bash
curl -X POST "[BASE_URL]/Notes" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "Note_Title": "Follow-up Call Scheduled",
        "Note_Content": "Customer requested follow-up call next week.",
        "Parent_Id": "[LEAD_ID]",
        "Parent_Name": "Leads"
      }
    ]
  }'
```

---

## Zoho Books API

### 基础 URL

| 数据中心 | 基础 URL |
|-------------|----------|
| 美国 | `https://www.zohoapis.com/books/v3` |
| 欧洲 | `https://www.zohoapis.eu/books/v3` |
| 澳大利亚 | `https://www.zohoapis.com.au/books/v3` |

**注意：** 所有请求都需要 `organization_id` 参数！

---

### 🔐 Books 的认证

使用相同的 OAuth 令牌。Books 默认使用 CRM 令牌！

---

### 👤 Books - 客户管理

#### 获取所有客户

```bash
curl -X GET "https://www.zohoapis.com/books/v3/contacts?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

#### 创建客户

```bash
curl -X POST "https://www.zohoapis.com/books/v3/contacts?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_name": "South Indian AB",
    "company_name": "South Indian Restaurant AB",
    "email": "billing@southindian.se",
    "phone": "+4681234567",
    "billing_address": {
      "street": "Drottninggatan 1",
      "city": "Stockholm",
      "state": "Stockholm County",
      "zip": "11123",
      "country": "Sweden"
    }
  }'
```

---

### 💰 Books - 发票管理

#### 创建发票

```bash
curl -X POST "https://www.zohoapis.com/books/v3/invoices?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "1234567890",
    "date": "2026-02-05",
    "due_date": "2026-03-05",
    "line_items": [
      {
        "name": "South Indian Dinner Buffet",
        "description": "2 Adults, Weekend Package",
        "rate": 399,
        "quantity": 2,
        "item_id": "1234567890"
      },
      {
        "name": "Welcome Drinks",
        "rate": 49,
        "quantity": 2,
        "item_id": "1234567891"
      }
    ],
    "notes": "Thank you for dining with us!",
    "terms": "Payment due within 30 days."
  }'
```

---

#### 获取发票状态

```bash
curl -X GET "https://www.zohoapis.com/books/v3/invoices/[INVOICE_ID]?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

#### 向客户发送发票

```bash
curl -X POST "https://www.zohoapis.com/books/v3/invoices/[INVOICE_ID]/actions/send?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_mail_ids": ["customer@example.com"]
  }'
```

---

### 📊 Books - 开支跟踪

#### 创建支出记录

```bash
curl -X POST "https://www.zohoapis.com/books/v3/expenses?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-02-05",
    "amount": 1500,
    "account_id": "1234567890",
    "description": "Weekly ingredient supply - spices",
    "vendor_id": "1234567890",
    "tax_id": "1234567890"
  }'
```

---

### 📈 Books - 报告

#### 获取损益报告

```bash
curl -X GET "https://www.zohoapis.com/books/v3/reports/profitandloss?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

## Zoho Desk API

### 基础 URL

| 数据中心 | 基础 URL |
|-------------|----------|
| 美国 | `https://desk.zoho.com/api/v1` |
| 欧洲 | `https://desk.zoho.eu/api/v1` |
| 澳大利亚 | `https://desk.zoho.com.au/api/v1` |

---

### 🎫 工单管理

#### 获取所有工单

```bash
curl -X GET "https://desk.zoho.com/api/v1/tickets?departmentId=[DEPT_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

#### 创建工单

```bash
curl -X POST "https://desk.zoho.com/api/v1/tickets" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Table Reservation Issue",
    "departmentId": "1234567890",
    "contact": {
      "lastName": "Ravi",
      "email": "customer@example.com"
    },
    "description": "Customer reported that their online table reservation was not found in the system.",
    "priority": "High",
    "status": "Open"
  }'
```

---

#### 更新工单

```bash
curl -X PUT "https://desk.zoho.com/api/v1/tickets/[TICKET_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress",
    "priority": "High",
    "assigneeId": "1234567890"
  }'
```

---

#### 为工单添加评论

```bash
curl -X POST "https://desk.zoho.com/api/v1/tickets/[TICKET_ID]/comments" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Contacted customer, issue resolved. Reservation updated in system.",
    "isPublic": true
  }'
```

---

## Zoho Creator API

### 基础 URL

| 数据中心 | 基础 URL |
|-------------|----------|
| 美国 | `https://creator.zoho.com/api/v2` |
| 欧洲 | `https://creator.zoho.eu/api/v2` |

---

### 📝 提交表单数据

```bash
curl -X POST "https://creator.zoho.com/api/v2/[APP_LINK_NAME]/[FORM_LINK_NAME]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "Name": "Employee Onboarding",
      "Employee_Name": "John Doe",
      "Department": "Engineering",
      "Start_Date": "2026-03-01",
      "Manager": "Jane Smith"
    }
  }'
```

---

### 📊 获取表单记录

```bash
curl -X GET "https://creator.zoho.com/api/v2/[APP_LINK_NAME]/[FORM_LINK_NAME]?MaxRows=100" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

## Zoho Campaigns API

### 基础 URL
`https://campaigns.zoho.com/api/v1`

---

### 📧 创建营销活动

```bash
curl -X POST "https://campaigns.zoho.com/api/v1/campaigns" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name": "February Restaurant Promotion",
    "subject": "🍛 Special Offer: 20% Off South Indian Thali!",
    "from_name": "South Indian Restaurant",
    "from_email": "marketing@southindian.se",
    "reply_to": "info@southindian.se"
  }'
```

---

### 👥 管理列表

```bash
# Get all mailing lists
curl -X GET "https://campaigns.zoho.com/api/v1/lists" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

---

## 高级功能

### 🔄 自动令牌刷新脚本

创建一个辅助脚本 `refresh-zoho-token.sh`：

```bash
#!/bin/bash

# Refresh Zoho access token
RESPONSE=$(curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=refresh_token" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "refresh_token=$ZOHO_REFRESH_TOKEN")

# Extract access token
ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access_token')

# Export for current session
export ZOHO_ACCESS_TOKEN=$ACCESS_TOKEN

echo "Token refreshed: $ACCESS_TOKEN"
```

运行该脚本：
```bash
chmod +x refresh-zoho-token.sh
./refresh-zoho-token.sh
```

---

### 📡 Webhook 设置

Zoho 可以将实时更新发送到您的端点：

**在 Zoho 中配置：**
1. 转到设置 → Webhook
2. 添加 webhook URL：`https://your-server.com/api/zoho-webhook`
3. 选择触发器（例如，`on_lead_create`、`on_deal_update`）

**在您的应用程序中处理 webhook：**
```javascript
// Express.js example
app.post('/api/zoho-webhook', (req, res) => {
  const { module, data, event } = req.body;
  
  console.log(`Zoho Webhook: ${event} on ${module}`);
  console.log('Data:', data);
  
  // Process the update
  if (module === 'Leads') {
    // Handle new lead
    handleNewLead(data);
  }
  
  res.status(200).send('OK');
});
```

---

### 🔗 多产品工作流

#### 示例：餐厅从客户到发票的工作流程

```bash
# 1. Customer books table (Zoho Creator form)
curl -X POST "https://creator.zoho.com/api/v2/restaurant/bookings" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "Customer_Name": "Ravi",
      "Email": "ravi@example.com",
      "Date": "2026-02-14",
      "Guests": 4,
      "Special_Requests": "Window seat preferred"
    }
  }'
```

```bash
# 2. Create CRM contact
curl -X POST "https://www.zohoapis.com/crm/v2/Contacts" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{
      "First_Name": "Ravi",
      "Email": "ravi@example.com",
      "Source": "Table Booking"
    }]
  }'
```

```bash
# 3. After dining, create invoice
curl -X POST "https://www.zohoapis.com/books/v3/invoices?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "[CUSTOMER_ID]",
    "date": "2026-02-14",
    "line_items": [{
      "name": "Valentine's Day Special Thali",
      "rate": 499,
      "quantity": 4
    }]
  }'
```

---

## 错误处理

### 常见错误代码

| 代码 | 含义 | 解决方案 |
|------|---------|----------|
| 401 | 无效令牌 | 请刷新您的访问令牌 |
| 400 | 请求错误 | 检查 JSON 语法 |
| 403 | 禁止访问 | 检查 API 权限 |
| 404 | 未找到 | 验证记录 ID |
| 429 | 超过请求频率限制 | 等待片刻后重试 |
| 500 | 服务器错误 | 稍后重试 |

---

### 重试逻辑示例

```bash
# Function to call Zoho API with retry
call_zoho_api() {
  local url=$1
  local method=$2
  local data=$3
  local max_attempts=3
  local attempt=1
  
  while [ $attempt -le $max_attempts ]; do
    response=$(curl -s -o /dev/null -w "%{http_code}" \
      -X $method "$url" \
      -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$data")
    
    if [ $response -eq 200 ] || [ $response -eq 201 ]; then
      echo "Success!"
      return 0
    elif [ $response -eq 429 ]; then
      echo "Rate limited, waiting 60s..."
      sleep 60
    else
      echo "Error: $response"
    fi
    
    attempt=$((attempt + 1))
    sleep 5
  done
  
  echo "Failed after $max_attempts attempts"
  return 1
}
```

---

## 环境变量参考

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `ZOHO_CLIENT_ID` | ✅ | OAuth 客户端 ID |
| `ZOHO_CLIENT_SECRET` | ✅ | OAuth 客户端密钥 |
| `ZOHO_REFRESH_TOKEN` | ✅ | 长期有效的刷新令牌 |
| `ZOHO_ACCESS_TOKEN` | ❌ | 短期有效的令牌（自动生成） |
| `ZOHO_DATACENTER` | ❌ | `com`（默认）、`eu`、`au`、`in` |
| `ZOHO_REDIRECT_URI` | ❌ | OAuth 重定向 URI |
| `ZOHO_ORG_ID` | ❌ | Books/Desk 组织 ID |

---

## 使用场景

### 🍽️ 餐厅业务

| 任务 | Zoho 产品 | 示例 |
|------|-------------|---------|
| 餐桌预订 | Creator | 在线预订表单 |
| 客户数据库 | CRM | 跟踪用餐偏好 |
| 发票管理 | Books | 月度账单 |
| 支持工单 | Desk | 预订问题 |
| 营销活动 | Campaigns | 新菜单公告 |

---

### 🛒 SaaS 业务

| 任务 | Zoho 产品 | 示例 |
|------|-------------|---------|
| 营销线索跟踪 | CRM | 销售流程 |
| 客户支持 | Desk | 技术问题 |
| 订阅账单 | Books/Subscriptions | 定期发票 |
| 功能请求 | Creator | 反馈门户 |
| 电子邮件营销 | Campaigns | 产品更新 |

---

### 🏢 通用业务

| 任务 | Zoho 产品 | 示例 |
|------|-------------|---------|
| 联系人管理 | CRM | 公司数据库 |
| 项目跟踪 | Projects | 任务分配 |
| 开支跟踪 | Books | 收据管理 |
| 人力资源入职 | Creator | 员工表格 |
| IT 帮助台 | Desk | 支持工单 |

---

## 安全最佳实践

### ✅ 应遵循的做法

- 将令牌存储在环境变量中
- 对所有 API 调用使用 HTTPS
- 定期轮换刷新令牌
- 设置 webhook 验证
- 使用最小权限的 API 范围

### ❌ 应避免的做法

- 切勿将令牌提交到 GitHub
- 不要在 URL 中暴露访问令牌
- 避免硬编码凭据
- 不要在用户之间共享令牌

---

## 测试

### 验证设置

```bash
# Test CRM connection
curl -X GET "https://www.zohoapis.com/crm/v2/settings/modules" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN"
```

应返回模块列表。如果返回 401 错误，请刷新您的令牌！

---

### 测试发票创建

```bash
# Create test invoice (amount: 1.00)
curl -X POST "https://www.zohoapis.com/books/v3/invoices?organization_id=[ORG_ID]" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "[TEST_CUSTOMER_ID]",
    "line_items": [{
      "name": "Test Item",
      "rate": 1,
      "quantity": 1
    }]
  }'
```

---

## 故障排除

### “无效令牌”错误

```bash
# Refresh your access token
curl -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "grant_type=refresh_token" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "refresh_token=$ZOHO_REFRESH_TOKEN"
```

---

### “请求频率超过限制”

- 等待 60 秒后重试
- 实施指数级退避策略
- 减少 API 调用频率
- 如需更高请求频率，请联系 Zoho 支持

---

### “模块未找到”

- 确认模块名称的拼写是否正确：
- ✅ `Leads`、`Contacts`、`Deals`、`Accounts`
- ❌ `Lead`、`Contact`、`Deal`、`Account`

---

### 权限被拒绝

- 检查您的 OAuth 权限范围：
- `ZohoCRM.modules.ALL` 以获取完整的 CRM 访问权限
- `ZohoBooks.fullaccess` 以获取 Books 的全部功能
- `ZohoDesk.fullaccess.all` 以获取 Desk 的全部功能

---

## 资源

### 官方文档
- **Zoho CRM API：** https://www.zoho.com/crm/developer/docs/api/v2/
- **Zoho Books API：** https://www.zoho.com/books/developer/docs/api/v3/
- **Zoho Desk API：** https://desk.zoho.com/developer/docs/api/v1/
- **Zoho Creator API：** https://www.zoho.com/creator/developer/docs/api/v2/

### 工具
- **API 控制台：** https://api-console.zoho.com/
- **开发者中心：** https://www.zoho.com/developer/

### 支持
- **Zoho 社区：** https://help.zoho.com/
- **开发者论坛：** https://forums.zoho.com/

---

## 版本

- **当前版本：** 1.0.0
- **创建日期：** 2026-02-05
- **作者：** OpenClaw 社区

---

**祝您 Zoho 自动化顺利！** 🚀📊

有问题？请查看故障排除部分或 Zoho 的官方文档！