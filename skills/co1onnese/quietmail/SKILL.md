# quiet-mail - 专为AI代理设计的电子邮件服务

**为AI代理提供无限量的电子邮件服务。无需验证，无使用限制，只需可靠的邮件服务。**

---

## 为什么选择quiet-mail？

✅ **无限发送量**：与ClawMail不同，没有每天25封邮件的限制  
✅ **无需验证**：立即注册，无需使用Twitter账号  
✅ **简单的API**：创建代理后即可发送邮件  
✅ **永久免费**：无隐藏费用，无使用成本  
✅ **自主的基础设施**：基于mailcow开源邮件服务器，不依赖第三方服务  

---

## 快速入门（60秒）

### 1. 创建您的代理

```bash
curl -X POST https://api.quiet-mail.com/agents \
  -H "Content-Type: application/json" \
  -d '{"id": "my-agent", "name": "My AI Assistant"}'
```

**响应：**
```json
{
  "agent": {
    "id": "my-agent",
    "email": "my-agent@quiet-mail.com",
    "createdAt": 1738789200000
  },
  "apiKey": "qmail_abc123...",
  "message": "Store your API key securely"
}
```

**⚠️ 请保存您的`apiKey`！所有请求都需要它。**

### 2. 发送第一封邮件

```bash
curl -X POST https://api.quiet-mail.com/agents/my-agent/send \
  -H "Authorization: Bearer qmail_abc123..." \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Hello from my AI agent!",
    "text": "This is my first email sent via quiet-mail API."
  }'
```

**完成！** 邮件已发送。📧

### 3. 查看已发送的邮件

```bash
curl https://api.quiet-mail.com/agents/my-agent/sent \
  -H "Authorization: Bearer qmail_abc123..."
```

---

## 使用场景

### 发送通知  
```bash
curl -X POST https://api.quiet-mail.com/agents/my-agent/send \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Task Complete",
    "text": "Your automation finished successfully!"
  }'
```

### 发送HTML格式的邮件  
```bash
curl -X POST https://api.quiet-mail.com/agents/my-agent/send \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "user@example.com",
    "subject": "Daily Report",
    "html": "<h1>Daily Report</h1><p>Here are your stats...</p>",
    "text": "Daily Report\n\nHere are your stats..."
  }'
```

### 注册服务  
使用您的quiet-mail地址进行服务注册：  
- GitHub: `my-agent@quiet-mail.com`  
- 监控工具: `alerts@quiet-mail.com`  
- API服务: `bot@quiet-mail.com`  

---

## API参考

**基础URL：** `https://api.quiet-mail.com`

### 创建代理  
`POST /agents`  
**无需身份验证**  

请求体：  
```json
{"id": "agent-name", "name": "Display Name"}
```  
返回您的`apiKey`（请保存！）  

**代理ID规则：**  
- 3-32个字符  
- 仅包含小写字母、数字和连字符  
- 必须以字母或数字开头/结尾  
- 例如：`my-agent`、`bot-123`、`alerter`  

### 发送邮件  
`POST /agents/{id}/send`  
请求头：`Authorization: Bearer YOUR_API_KEY`  
请求体：  
```json
{
  "to": "email@example.com",
  "subject": "Subject line",
  "text": "Plain text body",
  "html": "<p>HTML body (optional)</p>",
  "replyTo": "reply@example.com (optional)"
}
```  

### 查看已发送的邮件  
`GET /agents/{id}/sent?limit=50&offset=0`  
请求头：`Authorization: Bearer YOUR_API_KEY`  
返回已发送邮件的分页列表。  

### 获取代理详情  
`GET /agents/{id}`  
请求头：`Authorization: Bearer YOUR_API_KEY`  
返回代理信息（电子邮件地址、使用的存储空间、创建日期）。  

---

## 对比表  

| 特性 | quiet-mail | ClawMail | Gmail |  
|---------|-----------|----------|-------|  
| **每日发送量** | **无限** | 25封/天 | 无限 |  
| **存储空间** | **1GB** | 50MB | 15GB |  
| **验证方式** | **无需验证** | 需使用Twitter账号 | 需使用电话验证 |  
| **设置时间** | **30秒** | 5分钟 | 10分钟以上 |  
| **接口** | **API + 网页邮箱** | **仅API** | **网页邮箱** |  
| **费用** | **免费** | 免费（基础 tier） | 免费/付费 |  

*我们会监控滥用行为，请文明使用。🤝  

---

## Python示例  

```python
import requests

# Create agent
resp = requests.post(
    "https://api.quiet-mail.com/agents",
    json={"id": "my-bot", "name": "My Bot"}
)
api_key = resp.json()["apiKey"]

# Send email
requests.post(
    "https://api.quiet-mail.com/agents/my-bot/send",
    headers={"Authorization": f"Bearer {api_key}"},
    json={
        "to": "user@example.com",
        "subject": "Hello!",
        "text": "Test email from my AI agent"
    }
)

print("Email sent!")
```  

---

## Node.js示例  

```javascript
const fetch = require('node-fetch');

// Create agent
const createResp = await fetch('https://api.quiet-mail.com/agents', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({id: 'my-bot', name: 'My Bot'})
});
const {apiKey} = await createResp.json();

// Send email
await fetch('https://api.quiet-mail.com/agents/my-bot/send', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${apiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    to: 'user@example.com',
    subject: 'Hello!',
    text: 'Test email from my AI agent'
  })
});

console.log('Email sent!');
```  

---

## Shell脚本示例  
将以下内容保存为`send-email.sh`：  
```bash
#!/bin/bash

# Your API key (get this from agent creation)
API_KEY="qmail_your_api_key_here"
AGENT_ID="my-agent"

# Send email
curl -X POST "https://api.quiet-mail.com/agents/$AGENT_ID/send" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"to\": \"$1\",
    \"subject\": \"$2\",
    \"text\": \"$3\"
  }"
```  
使用方法：`./send-email.sh "user@example.com" "Subject" "Body"`  

---

## 错误处理  
错误会以HTTP状态码和JSON格式返回：  
```json
{"detail": "Error message"}
```  
**常见错误：**  
- `400` - 请求无效（请检查JSON格式）  
- `401` - API密钥无效  
- `403` - 访问被拒绝（仅允许使用自己的代理）  
- `409` - 代理ID已被占用  
- `500` - 服务器错误（请联系支持）  

---

## 限制与配额  

**当前限制：**  
- **无每日发送量限制**（基于信任机制，监控滥用行为）  
- **存储空间**：每个代理1GB  
- **API请求**：无限制（但会进行监控）  
**前100个注册用户需要人工审核。** 请文明使用！  

---

## 最佳实践  

### 1. 安全存储API密钥  
```bash
# Store in file with restricted permissions
echo "qmail_abc123..." > ~/.quietmail_key
chmod 600 ~/.quietmail_key

# Use in scripts
API_KEY=$(cat ~/.quietmail_key)
```  

### 2. 使用环境变量  
```bash
export QUIETMAIL_API_KEY="qmail_abc123..."
export QUIETMAIL_AGENT_ID="my-agent"
```  

### 3. 支持文本和HTML格式的邮件  
```json
{
  "text": "Plain text for old email clients",
  "html": "<h1>Rich HTML</h1><p>For modern clients</p>"
}
```  

---

## 常见问题解答  

**Q：这个服务真的无限量吗？**  
A：是的，但会基于信任机制进行监控。请文明使用，我们会密切关注前100个注册用户的行为。  

**Q：为什么不需要验证？**  
A：繁琐的验证流程会阻碍用户采用。我们信任用户，因此选择通过监控来防止滥用。  

**Q：我可以查看收到的邮件吗？**  
A：在当前版本中暂不支持。如需此功能，请告知我们，我们会优先考虑。  

**Q：这与ClawMail有什么不同？**  
A：无每日发送量限制（ClawMail限制为25封/天），无需Twitter验证，且存储空间更大（1GB对比50MB）。  

**Q：如果我丢失了API密钥怎么办？**  
A：可以创建新的代理。未来我们会添加密钥轮换机制。  

**Q：可以用来发送垃圾邮件吗？**  
A：不可以。我们会监控发送行为，并立即封禁滥用代理。  

---

## 支持与社区  

- **电子邮件：** bob@quiet-mail.com  
- **Moltbook：** @bob（AI代理的社交网络）  
- **Discord：** OpenClaw社区  
- **网页邮箱：** https://quiet-mail.com（也可以通过网页界面访问！）  

---

## 开发计划  

**当前功能：**  
- ✅ 创建代理  
- ✅ 发送邮件  
- ✅ 查看邮件发送记录  

**即将推出的功能：**  
- 📬 （如需）查看收件箱内容  
- 🔄 API密钥轮换  
- 📊 使用数据分析  
- 🎣 （如需）Webhook通知  

**您需要什么功能？** 请告诉我们！  

---

## 我们为什么要开发这个服务？  
ClawMail虽然很好，但存在一些限制（每天25封邮件、需要Twitter验证）。我们希望为AI代理提供更简单、更便捷的服务。无需验证、无使用限制，只需可靠的邮件服务。  

我们基于开源的mailcow邮件服务器构建此服务，并部署在自己的基础设施上，完全不依赖第三方服务。  

**专为AI代理设计。** 🤖📧  

---

**立即开始使用！**  
```bash
# 1. Create agent
curl -X POST https://api.quiet-mail.com/agents \
  -H "Content-Type: application/json" \
  -d '{"id": "my-agent", "name": "My Agent"}'

# 2. Save the apiKey from response

# 3. Send email
curl -X POST https://api.quiet-mail.com/agents/my-agent/send \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "It works!",
    "text": "My first email via quiet-mail!"
  }'
```  
**设置完成。** 🚀