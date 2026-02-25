---
name: paypilot
description: 通过安全的支付网关代理来处理付款、发送发票、退款以及管理交易。当用户需要向他人收费、发送付款链接、查看销售数据、办理退款、创建定期付款计划或管理任何与支付相关的任务时，均可使用该功能。此外，该系统还适用于商户的注册流程及首次支付设置。
homepage: https://agms.com/paypilot/
source: https://github.com/agmsyumet/paypilot-skill
author: AGMS (Avant-Garde Marketing Solutions)
requires:
  tools: [curl, jq, mkdir, chmod]
  network: [paypilot.agms.com]
credentials:
  - name: PAYPILOT_EMAIL
    description: Your merchant email for the PayPilot API
  - name: PAYPILOT_PASSWORD
    description: Your merchant password (used only during login to obtain a JWT)
  - name: PAYPILOT_GATEWAY_KEY
    description: Your payment gateway security key (encrypted at rest on the server)
config:
  path: ~/.config/paypilot/config.json
  permissions: "600"
  contents: api_url, email, token (JWT)
---
# PayPilot — 为AI代理提供的支付处理服务

通过对话即可完成收款、发送发票、退款以及销售跟踪等操作。

## 设置

PayPilot连接到托管的API代理服务器（地址：`https://paypilot.agms.com`）。首次使用时，请验证用户的凭证：

```bash
cat ~/.config/paypilot/config.json
```

如果配置信息不存在，请指导用户完成以下设置步骤：
1. 在PayPilot代理平台上进行**注册**：
```bash
curl -s "https://paypilot.agms.com/v1/auth/register" -X POST \
  -H "Content-Type: application/json" \
  -d '{"name":"BUSINESS_NAME","email":"EMAIL","password":"PASSWORD"}'
```

2. **登录**以获取访问令牌：
```bash
curl -s "https://paypilot.agms.com/v1/auth/login" -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"EMAIL","password":"PASSWORD"}'
```

3. **配置支付网关密钥**：
```bash
curl -s "https://paypilot.agms.com/v1/auth/configure" -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"gateway_key":"YOUR_GATEWAY_KEY"}'
```

4. 将凭证信息保存到本地：
```bash
mkdir -p ~/.config/paypilot
cat > ~/.config/paypilot/config.json << 'EOF'
{
  "api_url": "https://paypilot.agms.com",
  "email": "merchant@example.com",
  "token": "jwt_token_here"
}
EOF
chmod 600 ~/.config/paypilot/config.json
```

如果用户尚未拥有支付网关账户，请引导用户完成以下入职流程：
1. 通过对话收集基本信息：
   - 公司名称
   - 联系人姓名
   - 电子邮件地址
   - 电话号码
   - 企业类型（零售、餐饮、电子商务、移动服务等）

2. 将用户信息保存到我们的系统中：
```bash
curl -s "https://paypilot.agms.com/v1/onboard" -X POST \
  -H "Content-Type: application/json" \
  -d '{"business_name":"Acme Corp","contact_name":"John Doe","email":"john@acme.com","phone":"555-1234","business_type":"retail"}'
```

3. 将完整的申请链接发送给用户，以便其完成填写并电子签名：
> “太好了！请点击以下链接完成申请：**https://agms.com/get-started/**  
> 完成申请大约需要5-10分钟。您需要提供公司地址、税务识别号（Tax ID）和银行信息。提交后，您将立即完成电子签名，通常会在24-48小时内获得审批结果。  
> 一旦获得批准，我会立即为您设置支付处理功能。”

**重要提示：** 代理人员**严禁**收集用户的社保号码（SSN）、税务识别号（Tax ID）、银行账户信息或其他敏感的个人信息（PII）。这些信息仅通过安全的AGMS表格进行传输。

## 认证

所有支付请求端点都需要使用JWT（JSON Web Token）进行身份验证。请加载配置文件并设置请求头：
```bash
CONFIG=$(cat ~/.config/paypilot/config.json)
API=$(echo $CONFIG | jq -r '.api_url')
TOKEN=$(echo $CONFIG | jq -r '.token')
AUTH="Authorization: Bearer $TOKEN"
```

如果请求返回401错误，请让用户重新登录并更新保存的令牌。

如令牌过期，可执行以下操作来刷新令牌：
```bash
# Re-login
LOGIN=$(curl -s "$API/v1/auth/login" -X POST \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$(echo $CONFIG | jq -r '.email')\",\"password\":\"YOUR_PASSWORD\"}")
NEW_TOKEN=$(echo $LOGIN | jq -r '.access_token')

# Update config
jq --arg t "$NEW_TOKEN" '.token = $t' ~/.config/paypilot/config.json > /tmp/pp.json && mv /tmp/pp.json ~/.config/paypilot/config.json
chmod 600 ~/.config/paypilot/config.json
```

## 核心命令

### 收款/销售
使用已存储的卡片令牌来处理支付请求。**切勿直接处理原始卡片号码**。
```bash
curl -s "$API/v1/payments/charge" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"amount":500.00,"token":"VAULT_ID","description":"Consulting — January"}'
```

### 发送发票/支付链接
```bash
curl -s "$API/v1/payments/invoice" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"amount":500.00,"email":"john@example.com","description":"Consulting — January"}'
```

### 退款
```bash
# Full refund
curl -s "$API/v1/payments/refund" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"transaction_id":"TXN_ID"}'

# Partial refund
curl -s "$API/v1/payments/refund" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"transaction_id":"TXN_ID","amount":50.00}'
```

### 取消订单（当天有效）
```bash
curl -s "$API/v1/payments/void" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"transaction_id":"TXN_ID"}'
```

### 查看交易记录
```bash
curl -s "$API/v1/transactions" -H "$AUTH" | jq .
```

### 销售统计
```bash
curl -s "$API/v1/transactions/summary" -H "$AUTH" | jq .
```

### 客户信息存储（安全存储卡片信息）
安全地存储客户卡片信息——系统会返回一个存储令牌。客户通过安全表格输入卡片信息；原始卡片数据不会被代理人员获取。
```bash
curl -s "$API/v1/vault/add" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"first_name":"John","last_name":"Smith","email":"john@example.com"}'
```

### 从存储的卡片中扣款
```bash
curl -s "$API/v1/vault/charge" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"vault_id":"VAULT_ID","amount":99.00,"description":"Monthly service"}'
```

### 定期 billing（循环计费）
```bash
# Create subscription
curl -s "$API/v1/subscriptions" -X POST \
  -H "Content-Type: application/json" -H "$AUTH" \
  -d '{"vault_id":"VAULT_ID","plan_id":"monthly_99","amount":99.00,"interval":"monthly"}'

# Cancel subscription
curl -s "$API/v1/subscriptions/SUB_ID" -X DELETE -H "$AUTH"
```

## 安全规则
- **严禁**请求、记录或存储原始信用卡号码。
- **严禁**在对话记录或内存文件中保存信用卡号码。
- **始终**使用支付链接或客户存储的令牌来进行支付操作。
- **始终**使用HTTPS协议——代理服务器会强制使用TLS加密。
- API令牌和支付网关密钥必须保存在配置文件中，严禁在聊天记录中泄露。
- 代理服务器会对支付网关密钥进行加密处理（使用AES-256-GCM算法）。
- 每分钟全球请求上限为60次；认证端点的请求上限为5次。

## 响应格式

- 支付成功时：
> “✅ 已成功处理500.00美元的支付。交易ID：abc123。”

- 发送发票时：
> “📧 已将500.00美元的支付链接发送至john@example.com。”

- 支付失败时：
> “❌ 支付被拒绝。您是否想尝试其他支付方式或接收支付链接？”

- 查看销售记录时：
> “📊 本月共完成23笔交易，总销售额为4,750美元，其中2笔退款（150美元），净收入为4,600美元。”

## API参考

有关支付网关的详细文档，请参阅`references/gateway-api.md`。
支付流程图请参阅`references/payment-flows.md`。
有关PCI合规性指南，请参阅`references/pci-compliance.md`。