---
name: obverse-payments
description: 端到端的稳定币支付服务——包括链接、发票、收据以及监控仪表板——支持 Telegram、WhatsApp 和 Discord 平台。
homepage: https://www.obverse.cc
user-invocable: true
metadata:
  openclaw:
    requires:
      env: ["OBVERSE_API_KEY"]
    primaryEnv: "OBVERSE_API_KEY"
---
# Obverse – 用于AI代理的稳定币支付服务

**一个通用的支付链接，多种使用场景。**

在Solana和Monad区块链上接受USDC（稳定币）支付，适用于各种用途：销售产品、筹款、开具发票或简单支付。

## 该功能的主要作用：

✅ **创建支付链接**：一个适用于所有场景的灵活支付链接  
✅ **收集客户信息**：收集客户的电子邮件、姓名、电话号码或您需要的任何自定义字段  
✅ **仪表盘分析**：获取详细的支付统计数据、客户列表和图表  
✅ **接受USDC支付**：支持Solana和Monad区块链  
✅ **全面追踪**：销售分析、筹款进度、支付历史  
✅ **多平台支持**：可通过Telegram、WhatsApp、Discord等平台使用  
✅ **低费用**：每笔交易0.5-1.5%（相比之下，Stripe的费用为2.9%）  
✅ **即时结算**：资金几分钟内即可到账您的钱包  

---

## 快速设置：

### 1. 注册并获取API密钥  

```bash
# Register from any platform (no Telegram required!)
curl -X POST https://obverse.onrender.com/api-keys/register \
  -H "Content-Type: application/json" \
  -d '{"username": "your-agent-name"}'

# With your own wallet:
curl -X POST https://obverse.onrender.com/api-keys/register \
  -H "Content-Type: application/json" \
  -d '{"username": "your-agent-name", "walletAddress": "YOUR_WALLET", "chain": "solana"}'
```  
响应中会包含您的API密钥（`obv_sk_...`）和钱包地址。**请保存该密钥——它只会显示一次！**  

### 2. 设置环境变量  

```bash
export OBVERSE_API_KEY="obv_sk_your_key_here"
export OBVERSE_API_URL="https://obverse.onrender.com"  # optional, this is the default
```  

### 3. 开始使用  

```bash
# Create a payment link
obverse-cli create-link 50 USDC solana "My first payment"
```  

---

## 三种主要使用场景：  

### 1. **产品/服务销售**（商家销售）  

使用支付链接向任何人销售产品或服务。**系统会自动收集客户的电子邮件和姓名，用于构建邮件列表！**  
**示例：销售跑鞋**  

```bash
# Create product payment link (auto-collects email & name)
obverse-cli create-product-link "Premium Running Shoes" 120 USDC solana "High-performance shoes"

# Returns:
{
  "paymentUrl": "https://www.obverse.cc/pay/shoe-xyz",
  "linkCode": "shoe-xyz",
  "type": "product_sale",
  "title": "Premium Running Shoes",
  "amount": 120,
  "token": "USDC",
  "customFields": [
    { "fieldName": "email", "fieldType": "email", "required": true },
    { "fieldName": "name", "fieldType": "text", "required": true }
  ],
  "message": "Collects customer email and name!"
}

# Generate dashboard link to view all customer data
obverse-cli generate-dashboard shoe-xyz

# Returns:
{
  "dashboardUrl": "https://www.obverse.cc/dashboard",
  "credentials": {
    "username": "@yourname",
    "password": "AbC123XyZ456"
  },
  "instructions": [
    "1. Open dashboard: https://www.obverse.cc/dashboard",
    "2. Login with your credentials",
    "3. View customer emails, names, and payment details!"
  ]
}

# Check sales analytics
obverse-cli get-analytics shoe-xyz

# List all customers with their data
obverse-cli list-contributors shoe-xyz 50
```  
**适用场景：**  
- 实体产品（服装、小工具、周边商品）  
- 数字产品（电子书、课程、模板）  
- 服务（咨询、开发、设计）  
- 活动门票、订阅服务、预购  

---

### 2. **众筹/筹款**  

从多个捐助者那里筹集资金，实现共同目标。  
**示例：为AI开发项目筹款**  

```bash
# Create fundraising campaign
obverse-cli create-fundraiser "AI Development Fund" 5000 USDC monad "Building advanced AI agents"

# Returns:
{
  "paymentUrl": "https://www.obverse.cc/pay/fund-xyz",
  "linkCode": "fund-xyz",
  "type": "crowdfunding",
  "goalAmount": 5000
}

# Check fundraising progress
obverse-cli check-progress fund-xyz 5000

# Returns:
{
  "fundraising": {
    "goalAmount": 5000,
    "raisedAmount": 3450,
    "remainingAmount": 1550,
    "progressPercent": "69.0",
    "contributors": 23
  }
}

# List all contributors
obverse-cli list-contributors fund-xyz
```  
**适用场景：**  
- 代理开发资金  
- 产品发布  
- 社区项目  
- 研究经费  
- 开源项目  
- 奖金计划  

---

### 3. **简单支付与开票**  

接受一次性付款或为客户开具发票。  
**示例：咨询服务发票**  

```bash
# Generic payment link (one-time use)
obverse-cli create-link 750 USDC solana "Consulting Services - 5 hours"

# Check if paid
obverse-cli check-payment xyz123

# List all payments
obverse-cli list-payments xyz123
```  
**或使用正式的发票系统：**  
```bash
# Create invoice with recipient details
obverse-cli create-invoice john@example.com 750 USDC monad
```  
**适用场景：**  
- 自由职业工作  
- 专业服务  
- 一次性付款  
- 小费与捐赠  

---

## 新功能：数据收集与仪表盘  

### 通过支付链接收集客户信息  

**现在每个支付链接都可以收集客户的自定义数据！**非常适合用于构建邮件列表、收集客户信息及开具发票。  
**可收集的自定义字段：**  
- 电子邮件地址（`fieldType: "email"`）  
- 姓名（`fieldType: "text"`）  
- 电话号码（`fieldType: "tel"`）  
- 信息（`fieldType: "textarea"`）  
- 公司名称、地址或您需要的任何文本字段！  

### 仪表盘分析  

**查看全面的支付统计数据和客户信息！**  
**仪表盘内容包括：**  
- 支付统计（总收入、交易数量、成功率）  
- 客户信息（电子邮件、姓名、所有收集的字段）  
- 随时间变化的图表和趋势  
- 可搜索的支付历史记录  
- 可导出的客户列表  

---

## 核心命令：  

### 创建支付链接  

```bash
# Generic payment link with optional custom fields
obverse-cli create-link <amount> [currency] [chain] [description] [customFieldsJson] [isReusable]

# Example: Simple payment
obverse-cli create-link 50 USDC solana "Payment for services"

# Example: With data collection
obverse-cli create-link 100 USDC monad "Consultation" '[{"fieldName":"email","fieldType":"email","required":true}]' true
```  

### 便捷功能（自动收集客户信息）  

```bash
# For product/service sales (auto-collects email & name)
obverse-cli create-product-link <title> <price> [currency] [chain] [description] [customFieldsJson]

# For crowdfunding (auto-collects optional email & name)
obverse-cli create-fundraiser <title> <goalAmount> [currency] [chain] [description] [customFieldsJson]

# For invoicing (formal)
obverse-cli create-invoice <recipient> <amount> [currency] [chain] [dueDate]
```  

### 仪表盘与分析  

```bash
# Generate dashboard credentials
obverse-cli generate-dashboard <linkCode>

# Get analytics (sales/fundraising stats)
obverse-cli get-analytics <linkCode>

# Check payment link status
obverse-cli check-payment <linkCode>

# List all payments for a link
obverse-cli list-payments <linkCode> [limit]

# Check fundraising progress toward goal
obverse-cli check-progress <linkCode> <goalAmount>

# List all contributors/customers
obverse-cli list-contributors <linkCode> [limit]

# Check wallet balance
obverse-cli balance <userId> [chain]
```  

---

## 完整的工作流程示例：  

### 工作流程1：销售数字产品（包含客户信息收集）  

```bash
# Step 1: Create product link (auto-collects email & name)
obverse-cli create-product-link "AI Course Bundle" 299 USDC solana

# Step 2: Share the link
# https://www.obverse.cc/pay/course-xyz
# Customers pay AND provide their email/name automatically!

# Step 3: Generate dashboard to view all customer data
obverse-cli generate-dashboard course-xyz
# Returns: Login credentials for full analytics dashboard

# Step 4: Check sales analytics
obverse-cli get-analytics course-xyz

# Step 5: Export customer email list for marketing
obverse-cli list-contributors course-xyz 100
# Now you have customer emails to send course access links!
```  

### 工作流程2：开展筹款活动  

```bash
# Step 1: Create fundraiser
obverse-cli create-fundraiser "Open Source AI Project" 10000 USDC monad

# Step 2: Share campaign link
# https://www.obverse.cc/pay/project-xyz

# Step 3: Track progress
obverse-cli check-progress project-xyz 10000

# Step 4: Thank top contributors
obverse-cli list-contributors project-xyz
```  

### 工作流程3：自由职业咨询  

```bash
# Step 1: Create payment link
obverse-cli create-link 1500 USDC solana "Smart Contract Development"

# Step 2: Send link to client
# https://www.obverse.cc/pay/work-xyz

# Step 3: Check if paid
obverse-cli check-payment work-xyz

# Step 4: Verify payment
obverse-cli list-payments work-xyz
```  

---

## 代理使用方式：  

### 通过Telegram  

```
User: "Create payment link to sell my AI course for $299"

Agent: ✅ Product Payment Link Created!
       Product: AI Course Bundle
       Price: $299 USDC
       Link: https://www.obverse.cc/pay/course-xyz

       Share this link to start selling!
```  

```
User: "How many courses have I sold?"

Agent: 📊 Sales Analytics
       Total Sales: 47
       Revenue: $14,053 USDC
       Customers: 47
       Average: $299.00
```  

### 通过WhatsApp  

```
User: "Start a fundraiser for $5000"

Agent: 🚀 Fundraising Campaign Created!
       Goal: $5,000 USDC
       Link: https://www.obverse.cc/pay/fund-xyz
```  

```
User: "How much have we raised?"

Agent: 💰 Fundraising Progress
       Goal: $5,000 USDC
       Raised: $3,450 (69%)
       Remaining: $1,550
       Contributors: 23
```  

### 通过Discord  

```
User: "Bill the client for $750"

Agent: 💳 Payment Link Created
       Amount: $750 USDC
       Link: https://www.obverse.cc/pay/work-xyz
```  

```
User: "Did they pay?"

Agent: ✅ PAYMENT RECEIVED!
       Amount: $750 USDC
       Transaction: 0x8a9b7c...
       Time: 15 minutes ago
```  

### 新功能：数据收集与仪表盘示例  

```
User: "Create a payment link for my course and collect customer emails"

Agent: ✅ Product Link Created with Data Collection!
       Product: Online Course
       Price: $299 USDC
       Link: https://www.obverse.cc/pay/course-xyz

       📧 Automatically collects:
       • Customer email
       • Customer name

       Share this link to sell and build your email list!
```  

```
User: "Show me who bought my course"

Agent: 📊 Generating Dashboard Access...

       🔐 Dashboard Credentials:
       URL: https://www.obverse.cc/dashboard
       Username: @yourname
       Password: AbC123XyZ456

       ⏰ Valid for: 2 hours

       View all customer emails, names, payments, and analytics!
```  

```
User: "I want to collect phone numbers too"

Agent: ✅ Custom Payment Link Created!
       Link: https://www.obverse.cc/pay/custom-xyz

       Collecting:
       • Email (required)
       • Name (required)
       • Phone (optional)

       Perfect for building your customer database!
```  

---

## 默认设置：  

- **默认区块链**：Solana  
- **默认货币**：USDC（最常用的稳定币）  
- **结算时间**：资金2-5分钟内到账  
- **费用**：每笔交易0.5-1.5%  

---

## 支持的区块链：  

| 区块链 | 货币 | 费用 |
|-------|-----------|------|
| **Solana** | USDC | 低费用 |
| Monad | USDC | 低费用 |

---

## 错误处理：  

**常见错误：**  
“无效的API密钥”  
```bash
# Check your API key
echo $OBVERSE_API_KEY
# Register for a new key:
curl -X POST https://obverse.onrender.com/api-keys/register \
  -H 'Content-Type: application/json' \
  -d '{"username": "your-agent-name"}'

**"Payment link not found"**
```bash  
# 检查链接代码是否正确  
`obverse-cli check-payment <linkCode>`  
```

**"Rate limit exceeded"**
```bash  
# 等待60秒后重试  

---

## API使用限制：  

| 计划类型 | 每分钟请求次数 | 每月交易次数 |
|------|--------------|--------------|
| 免费 | 10 | 100 |
| 初级 | 60 | 500 |
| 专业 | 300 | 2,000 |

---

## 帮助获取：  

- **API文档**：[obverse.onrender.com/api-docs](https://obverse.onrender.com/api-docs)  
- **支持邮箱**：obverse.ccc@gmail.com  

---

## 关键要点：  

**一个通用的支付链接，多种使用场景。**  
无论您是销售产品、筹款还是为客户开具发票，都可以使用这个灵活的支付系统。便捷的操作命令让使用更加简单。  
无需复杂的设置，无需多个接口，只需简单的支付功能即可满足需求。💙  

---

**由Obverse团队用心制作。**