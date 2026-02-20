---
name: atoship
description: 将您的人工智能助手转变为一个完全自主的物流管理工具。只需简单描述您的需求，即可购买打折的物流标签、比较 USPS、FedEx 和 UPS 的运费、追踪包裹以及管理运输过程。无需使用任何门户网站或复杂的界面，也无需进行任何手动操作。
user-invokable: true
license: MIT
metadata: {"openclaw": {"emoji": "📦", "primaryEnv": "ATOSHIP_API_KEY", "homepage": "https://atoship.com"}}
---
# atoship — 您的AI物流管理助手

想象一下，有一个永远不会犯错、永远不会输入错误数据、并且能够立即找到从A地到B地运输包裹的最便宜方式的物流管理助手。atoship正是为您的AI助手提供的这样的功能。

安装了这个技能后，您的AI就能成为一位全能的物流管理专家。只需用简单的语言告诉它您的需求，它就会自动处理承运商的选择、价格比较、标签购买以及物流追踪更新。过去需要花费10分钟在各个承运商网站上操作的任务，现在只需一句话就能完成。

**使用atoship之前的流程：**  
- 打开承运商网站  
- 输入收件人和寄件人地址  
- 在不同标签页间比较运费  
- 复制并粘贴追踪号码  
- 手动更新订单状态  

**使用atoship之后的流程：**  
*“将这个包裹寄给奥斯汀的约翰，选择3天内的最便宜方案。”* 完成！

## 主要功能：  
- **比较运费**：  
  在几秒钟内同时获取USPS、FedEx和UPS的实时折扣运费信息。  

- **购买物流标签**：  
  在结账时立即购买物流标签，支持PDF、PNG或ZPL格式。  

- **追踪包裹**：  
  实时追踪包裹的运输情况，并提供完整的事件记录（适用于所有承运商）。  

- **管理标签**：  
  查看、撤销或重新打印之前的物流标签。  

- **查看钱包余额**：  
  监控您的邮资余额和物流费用支出。  

- **验证地址**：  
  在购买前验证收件地址，以避免额外费用。  

## 开始使用方法：  
这个技能无需任何命令行工具（CLI）或额外软件。您的AI助手会直接使用您的API密钥调用atoship的API。  

**步骤1：创建一个免费的atoship账户**  
在https://atoship.com注册（免费，无需信用卡）。  

**步骤2：获取API密钥**  
进入“仪表盘”→“设置”→“API密钥”，然后创建一个新的密钥。  

**步骤3：设置API密钥**  
（具体代码请参考```bash
export ATOSHIP_API_KEY=ak_live_your_key_here
```）  
或者您也可以在AI助手的环境设置中配置API密钥。  

**步骤4：为钱包充值**  
进入“仪表盘”→“账单”，为物流服务充值。标签费用将从您的钱包余额中扣除——您只需支付实际使用的费用。  

> **关于权限的说明：**  
您的API密钥用于授权标签购买和钱包扣费。我们建议：  
- 在测试阶段使用较小的钱包余额（例如20美元）。  
- 开发时使用测试密钥（如`ak_test_...`），测试标签是免费的且不会实际发送。  
- 在“仪表盘”→“账单”→“通知”中设置费用提醒。  
- 随时可以通过“仪表盘”→“设置”→“API密钥”撤销或更换密钥。  

## 使用方法：  
输入`/atoship`，然后描述您的需求。例如：  
- “从洛杉矶寄一个2磅重的包裹到纽约需要多少钱？”  
- “购买一张从90001寄往10001的USPS优先邮件标签（1磅重）。”  
- “追踪我的包裹：9400111899223456789012。”  
- “显示我最近的物流标签。”  
- “我的账户余额是多少？”  

## 物流工作流程：  
### 第1步：比较运费  
我会调用atoship API来获取所有承运商的实时运费信息：  
（具体代码请参考```
From: ZIP code or "City, State"
To:   ZIP code or "City, State"
Weight: e.g. 2oz, 1lb, 500g
Dimensions (optional): length × width × height in inches
```）  
结果会显示每个承运商的服务、价格和预计送达时间（包括USPS、FedEx Ground、FedEx Express、UPS Ground、UPS 2-Day等）。  

### 第2步：购买标签  
选择服务后，我会收集完整的地址信息并购买标签：  
（具体代码请参考```
Sender:    Name, Street, City, State, ZIP
Recipient: Name, Street, City, State, ZIP
```）  
您将收到：  
- ✅ 追踪号码  
- ✅ 标签下载链接（PDF或PNG格式）  
- ✅ 费用将从您的钱包中扣除。  
如果标签在承运商规定的有效期内未被使用，您可以申请退款。  

### 第3步：追踪包裹  
提供追踪号码，我将显示完整的物流事件记录：  
（具体代码请参考```
Status:    IN TRANSIT
Location:  Memphis, TN
ETA:       Feb 19, 2026
Events:    Feb 17 10:42 — Departed facility, Memphis TN
           Feb 17 06:15 — Arrived at USPS facility
           Feb 16 18:30 — Accepted at origin post office
```）  

## 支持的承运商：  
| 承运商 | 运费 | 标签 | 追踪服务 |  
|--------|-------|--------|---------|  
| USPS    | ✅    | ✅     | ✅      |  
| FedEx   | ✅    | ✅     | ✅      |  
| UPS     | ✅    | ✅     | ✅      |  

## 常见用途：  
- **电子商务订单处理**：  
  无需切换页面，即可为Shopify、eBay、Etsy或Amazon的订单处理物流。自动为每个订单选择最便宜的承运商。  

- **小型企业物流**：  
  比较USPS First Class、Priority Mail、FedEx Ground和UPS Ground的运费，适用于任何包裹大小和重量，节省每一笔运输费用。  

- **代发货和第三方物流**：  
  将atoship的API集成到您的物流系统中，批量生成和追踪包裹。  

- **国际运输**：  
  支持通过USPS International、FedEx International和UPS Worldwide进行跨境运输（涵盖加拿大、英国、澳大利亚等200多个国家）。  

- **退货管理**：  
  通过单一命令生成预付退货标签。  

## 使用技巧：  
- **查询最便宜的运输方式**：  
  询问“从X地寄到Y地的最便宜方式是什么？”  

- **支持的单位**：  
  支持盎司（oz）、磅（lb）、克（g）和千克（kg）。  

- **标签格式**：  
  默认为PDF格式，也支持PNG和ZPL格式（适用于热敏打印机）。  

- **是否需要签名**：  
  购买标签时可以选择“需要签名确认”。  

- **是否需要保险**：  
  可以选择“购买时包含100美元的保险”。  

## API端点参考：  
基础URL：`https://atoship.com`  
所有请求都需要添加`Authorization: Bearer YOUR_API_KEY`头部。  

| 功能 | 方法 | API端点 | 说明 |  
|--------|--------|----------|-------------|  
| 获取运费 | POST | `/api/v1/rates` | 比较多个承运商的运费 |  
| 创建标签 | POST | `/api/v1/labels` | 创建物流标签草稿 |  
| 购买标签 | POST | `/api/v1/labels/{id}/purchase` | 购买标签 |  
| 查看标签详情 | GET | `/api/v1/labels/{id}` | 根据ID查看标签详情 |  
| 列出标签 | GET | `/api/v1/labels` | 列出所有标签（可选过滤条件） |  
| 撤销标签 | DELETE | `/api/v1/labels/{id}` | 撤销未使用的标签 |  
| 追踪包裹 | GET | `/api/v1/tracking/{tracking_number}` | 根据追踪号码追踪包裹 |  
| 验证地址 | POST | `/api/v1/addresses/validate` | 验证收件地址 |  
| 创建订单 | POST | `/api/v1/orders` | 创建新订单 |  
| 查看订单详情 | GET | `/api/v1/orders/{id}` | 根据ID查看订单详情 |  
| 列出订单 | GET | `/api/v1/orders` | 列出所有订单（可选过滤条件） |  
| 查看账户信息 | GET | `/api/v1/account` | 查看账户信息和余额 |  
| 列出承运商信息 | GET | `/api/v1/carrier-accounts` | 查看配置的承运商账户 |  

### 示例：  
- **追踪包裹**：  
  （具体代码请参考```bash
curl -X GET "https://atoship.com/api/v1/tracking/9400111899223456789012" \
  -H "Authorization: Bearer ak_live_your_key_here"
```）  

- **获取运费**：  
  （具体代码请参考```bash
curl -X POST "https://atoship.com/api/v1/rates" \
  -H "Authorization: Bearer ak_live_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": {"name": "Sender", "street1": "123 Main St", "city": "Los Angeles", "state": "CA", "zip": "90001"},
    "to_address": {"name": "Recipient", "street1": "456 Oak Ave", "city": "New York", "state": "NY", "zip": "10001"},
    "parcel": {"weight": 16, "weight_unit": "oz"}
  }'
```）  

- **购买标签**：  
  （具体代码请参考```bash
# Step 1: Create draft
curl -X POST "https://atoship.com/api/v1/labels" \
  -H "Authorization: Bearer ak_live_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": {"name": "Sender", "street1": "123 Main St", "city": "Los Angeles", "state": "CA", "zip": "90001"},
    "to_address": {"name": "Recipient", "street1": "456 Oak Ave", "city": "New York", "state": "NY", "zip": "10001"},
    "parcel": {"weight": 16, "weight_unit": "oz"},
    "carrier": "USPS",
    "service": "Priority Mail"
  }'

# Step 2: Purchase the draft (use the id from step 1)
curl -X POST "https://atoship.com/api/v1/labels/{id}/purchase" \
  -H "Authorization: Bearer ak_live_your_key_here"
```）  

## 为什么选择atoship？  
物流是运营在线业务中最耗时的环节之一。每个订单都需要登录承运商网站、手动比较运费、复制地址、下载标签并逐一更新追踪信息。对于每天处理数十或数百个包裹的团队来说，这是个巨大的工作负担。  

atoship彻底解决了这些问题。通过将您的AI助手与atoship平台连接起来，您将拥有一个高效的物流管理助手：  
- **响应迅速**：瞬间完成所有承运商的运费比较；  
- **避免错误**：从对话到标签生成的全过程都是结构化的数据流，无需人工重新输入；  
- **记住上下文**：AI了解您要运输的物品、目的地及用途；  
- **灵活扩展**：无论每天运输1个还是1000个包裹，工作流程都相同；  
- **节省成本**：提供折扣运费，无最低运输量要求，也无需支付月费。  

atoship专为电子商务卖家、小型企业主、物流协调员和开发者设计，帮助他们自动化物流流程，无需复杂的合同或集成。  

**主要特点：**  
- USPS、FedEx和UPS的折扣运费；  
- 支持多承运商的统一API；  
- 实时追踪和配送事件通知；  
- 地址验证和标准化；  
- 基于钱包的计费方式，无需支付月费或订阅费。  

## 安全性与API密钥保护：  
此技能会代表您调用atoship的REST API（https://atoship.com/api/v1）。它不会在磁盘上存储任何数据，也不会访问您的系统，仅使用您提供的`ATOSHIP_API_KEY`。  

**影响钱包的操作：**  
- `purchase_label`：从您的钱包余额中扣除标签费用；  
- `void_label`：在承运商规定的有效期内退款。  

**仅读操作：**  
- `get_shipping_rates`、`track_package`、`list_labels`、`get_label`、`get_account`、`list_carrier_accounts`、`validate_address`。  

**风险控制：**  
您可以在“仪表盘”→“设置”→“API密钥”中创建只读API密钥，并限制其访问特定IP地址或设置使用次数限制。  

**支持与联系方式：**  
如有任何问题，请发送邮件至support@atoship.com，我们将在一个工作日内回复您。  
- **邮箱**：support@atoship.com  
- **官网**：https://atoship.com  
- **文档**：https://atoship.com/docs  
- **API参考**：https://atoship.com/docs/api  
- **仪表盘**：https://atoship.com/dashboard  

如有关于API密钥、账单问题或集成需求，请随时联系我们。