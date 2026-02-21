---
name: atoship
description: 使用 AI 功能来包裹寄送：可以比较 USPS、FedEx 和 UPS 的运费，购买打折的包装标签，追踪包裹状态，并管理订单。在任何购买操作或影响用户钱包的操作之前，都需要用户的确认。
user-invokable: true
license: MIT
metadata: {"openclaw": {"emoji": "📦", "primaryEnv": "ATOSHIP_API_KEY", "requiredEnv": ["ATOSHIP_API_KEY"], "homepage": "https://atoship.com"}}
---
# atoship — 您的智能物流管理工具

想象一下，有一个永远不会犯错、永远不会输入数据错误的物流经理，能够立即找到将包裹从A地送到B地的最便宜方式。这就是atoship为您的智能助手带来的功能。

安装了这个技能后，您的智能助手就变成了一个功能齐全的物流经理。只需用简单的语言告诉它您的需求，它就会自动处理承运商的选择、价格比较、标签购买和追踪更新。以前需要花费10分钟在各个承运商的网站上操作的工作，现在只需一句话就能完成。

**使用atoship之前：** 打开承运商网站 → 输入地址 → 在不同标签页间比较价格 → 复制并粘贴追踪号码 → 手动更新订单状态。

**使用atoship之后：** “将这个订单寄给奥斯汀的约翰，选择3天内的最便宜方案。” 完成。

## 功能介绍

- **比较运费**：几秒钟内即可同时获取USPS、FedEx和UPS的实时折扣运费。
- **购买运输标签**：在结账时立即购买标签；支持PDF、PNG或ZPL格式。
- **追踪货物**：实时追踪包裹的运输情况，并提供所有承运商的完整事件历史记录。
- **管理标签**：查看、撤销或重新打印过去的运输标签。
- **检查钱包余额**：监控您的邮资信用和运输费用。
- **验证地址**：在购买前验证收货地址，以避免额外费用。

## 开始使用

这个技能仅需要指令，不需要任何命令行工具或额外的软件。您的智能助手会直接使用您的API密钥调用atoship的API。

**步骤1：创建一个免费的atoship账户**

在https://atoship.com注册（免费，无需信用卡）。

**步骤2：获取您的API密钥**

前往“仪表盘” → “设置” → “API密钥”，然后创建一个新的密钥。

**步骤3：设置您的API密钥**

```bash
export ATOSHIP_API_KEY=ak_live_your_key_here
```

或者您可以在智能助手的环境设置中配置它。

**步骤4：为钱包充值**

前往“仪表盘” → “账单”，为钱包充值邮资。标签费用将从您的钱包余额中扣除——您只需支付实际使用的费用。

> **关于权限的说明：** 您的API密钥用于授权标签购买和钱包扣费。我们建议：
- 在测试期间使用较小的钱包余额（例如20美元）。
- 开发阶段使用测试密钥（如`ak_test_...`），因为测试标签是免费的，不会实际发货。
- 在“仪表盘” → “账单” → “通知”中设置消费提醒。
- 随时在“仪表盘” → “设置” → “API密钥”中撤销或更换密钥。

## 使用方法

输入`/atoship`并描述您的需求。例如：

- “从洛杉矶寄一个2磅重的包裹到纽约需要多少钱？”
- “购买一张从90001寄往10001的USPS优先邮件标签（1磅重）”
- “追踪我的包裹：9400111899223456789012”
- “显示我最近的运输标签”
- “我的账户余额是多少？”

## 物流工作流程

### 第1步 — 比较运费

我将调用atoship API来获取所有承运商的实时运费：

```
From: ZIP code or "City, State"
To:   ZIP code or "City, State"
Weight: e.g. 2oz, 1lb, 500g
Dimensions (optional): length × width × height in inches
```

结果会显示每个承运商的服务、价格和预计送达时间。包括USPS、FedEx Ground、FedEx Express、UPS Ground、UPS 2-Day等。

### 第2步 — 购买标签

> **重要提示**：在调用购买API之前，务必向用户显示承运商、服务、价格和完整地址，并请求明确确认（例如：“确认购买吗？”）。未经用户同意，切勿购买标签——否则会从用户的钱包中扣费。

选择服务后，我会收集完整的地址并购买标签：

```
Sender:    Name, Street, City, State, ZIP
Recipient: Name, Street, City, State, ZIP
```

您将收到：
- ✅ 追踪号码
- ✅ 标签下载链接（PDF或PNG格式）
- ✅ 从钱包中扣除的费用

如果在承运商规定的有效期内未使用标签，可以撤销标签以获得退款（USPS通常为28天，FedEx/UPS为1天）。

### 第3步 — 追踪包裹

提供追踪号码，我将显示完整的运输事件历史记录：

```
Status:    IN TRANSIT
Location:  Memphis, TN
ETA:       Feb 19, 2026
Events:    Feb 17 10:42 — Departed facility, Memphis TN
           Feb 17 06:15 — Arrived at USPS facility
           Feb 16 18:30 — Accepted at origin post office
```

## 支持的承运商

| 承运商 | 运费 | 标签 | 追踪 |
|---------|-------|--------|---------|
| USPS    | ✅    | ✅     | ✅      |
| FedEx   | ✅    | ✅     | ✅      |
| UPS     | ✅    | ✅     | ✅      |

## 常见用途

- **电子商务订单处理**：无需切换标签页，即可处理Shopify、eBay、Etsy或Amazon的订单，自动为每个订单选择最便宜的承运商。
- **小型企业物流**：比较USPS First Class、Priority Mail、FedEx Ground和UPS Ground的费用，适用于任何尺寸和重量的包裹，节省运输成本。
- **代发货和第三方物流**：将atoship的API集成到您的物流流程中，批量生成标签并进行追踪。
- **国际运输**：atoship支持通过USPS International、FedEx International和UPS Worldwide进行跨境运输，覆盖加拿大、英国、澳大利亚等200多个国家。
- **退货管理**：通过单一命令生成客户退货的预付退货标签。
- **批量运输**：使用https://atoship.com的仪表盘进行CSV导入和批量标签生成。

## 提示

- **最便宜的运输方式**：询问“将X件物品从A地运到B地最便宜的方法是什么？”
- **重量单位**：支持盎司（oz）、磅（lb）、克（g）和千克（kg）。
- **标签格式**：默认为PDF，支持PNG和ZPL格式（适用于热敏打印机）。
- **是否需要签名**：购买时可以选择“需要签名确认”。
- **保险选项**：购买时可以选择“添加100美元的保险”。
- **参考编号**：可以在标签上添加“参考编号：ORDER-123”以便追踪。

## API端点参考

基础URL：`https://atoship.com`

所有请求都需要包含`Authorization: Bearer YOUR_API_KEY`头部。

| 功能 | 方法 | 端点 | 说明 |
|--------|--------|----------|-------------|
| 获取运费 | POST | `/api/v1/rates` | 比较多个承运商的运费 |
| 创建标签 | POST | `/api/v1/labels` | 创建运输标签草稿 |
| 购买标签 | POST | `/api/v1/labels/{id}/purchase` | 购买标签 |
| 获取标签详情 | GET | `/api/v1/labels/{id}` | 通过ID获取标签详情 |
| 列出标签 | GET | `/api/v1/labels` | 列出标签（可选过滤条件） |
- 撤销标签 | DELETE | `/api/v1/labels/{id}` | 撤销/取消未使用的标签 |
- 追踪包裹 | GET | `/api/v1/tracking/{tracking_number}` | 通过追踪号码追踪包裹 |
- 验证地址 | POST | `/api/v1/addresses/validate` | 验证运输地址 |
- 创建订单 | POST | `/api/v1/orders` | 创建新订单 |
- 获取订单详情 | GET | `/api/v1/orders/{id}` | 通过ID获取订单详情 |
- 列出订单 | GET | `/api/v1/orders` | 列出订单（可选过滤条件） |
- 获取账户信息 | GET | `/api/v1/account` | 获取账户信息和余额 |
- 列出承运商 | GET | `/api/v1/carrier-accounts` | 列出已配置的承运商账户 |

### 示例：追踪包裹

```bash
curl -X GET "https://atoship.com/api/v1/tracking/9400111899223456789012" \
  -H "Authorization: Bearer ak_live_your_key_here"
```

### 示例：获取运费

```bash
curl -X POST "https://atoship.com/api/v1/rates" \
  -H "Authorization: Bearer ak_live_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "from_address": {"name": "Sender", "street1": "123 Main St", "city": "Los Angeles", "state": "CA", "zip": "90001"},
    "to_address": {"name": "Recipient", "street1": "456 Oak Ave", "city": "New York", "state": "NY", "zip": "10001"},
    "parcel": {"weight": 16, "weight_unit": "oz"}
  }'
```

### 示例：购买标签

```bash
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
```

## 为什么选择atoship？

物流是经营在线业务中最耗时的部分之一。每个订单都需要登录承运商网站、手动比较运费、复制地址、下载标签并逐一更新追踪信息。对于每天处理数十或数百个包裹的团队来说，这是一个巨大的操作负担。

atoship彻底解决了这些问题。通过将您的智能助手连接到atoship平台，您将拥有一个能够：

- **瞬间完成价格比较** — 在几秒钟内完成所有承运商的运费比较。
- **避免地址输入错误** — 从对话到标签的整个流程都是结构化的，无需任何手动输入。
- **记住上下文** — 智能助手知道您要运输什么、去往哪里以及用途是什么。
- **随业务规模扩展** — 无论每天运输1个还是1000个包裹，工作流程都是一样的。
- **节省实际费用** — 提供折扣运费，没有最低运输量要求，也没有月费。

atoship专为电子商务卖家、小型企业主和物流协调员设计，帮助他们自动化物流操作，无需企业级合同或复杂的集成。

**主要特点：**
- USPS、FedEx和UPS的折扣运费——无需最低运输量要求。
- 统一的API，支持多承运商的自动化物流管理。
- 实时追踪和送达事件通知。
- 地址验证和标准化。
- 基于钱包的计费方式，无需月费或订阅费用。

## 安全性与API密钥保护

此技能会代表您调用atoship的REST API（`https://atoship.com/api/v1`）。它不会在磁盘上写入文件，不会访问您的文件系统，也不会读取其他环境变量，仅与`atoship.com`域名进行通信。

**必需的环境变量：**
- `ATOSHIP_API_KEY` — 您的atoship API密钥（生产环境使用`ak_live_...`，测试环境使用`ak_test_...`）。

**影响钱包的操作（执行前需要用户确认）：**
- `purchase_label` — 从钱包余额中扣除标签费用。
- `void_label` — 退款（在承运商规定的有效期内）。

> **对于智能助手的建议**：在调用`purchase_label`或`void_label`之前，必须获得用户的明确确认。显示操作详情（承运商、服务、价格、地址），并等待用户回复“是”或“确认”。切勿自动执行影响钱包的操作。

**无需确认即可安全调用的操作：**
- `get_shipping_rates`、`track_package`、`list_labels`、`get_label`、`get_account`、`list_carrier_accounts`、`validate_address`、`list_orders`、`get_order`、`create_order`。

**建议：**
- 在测试期间使用测试密钥（`ak_test_...`），因为测试标签是免费的，不会实际发货。
- 在测试期间使用较小的钱包余额（例如20美元）。
- 在“仪表盘” → “账单” → “通知”中设置消费提醒。
- 随时在“仪表盘” → “设置” → “API密钥”中撤销或更换密钥。

## 支持与联系

遇到问题？我们随时为您提供帮助。

- **电子邮件**：support@atoship.com
- **网站**：https://atoship.com
- **文档**：https://atoship.com/docs
- **API参考**：https://atoship.com/docs/api
- **仪表盘**：https://atoship.com/dashboard

如果您有关于API密钥、账单或承运商集成的问题，请发送电子邮件至support@atoship.com，我们将在一个工作日内回复您。