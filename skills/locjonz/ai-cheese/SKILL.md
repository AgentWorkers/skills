---
name: ai-cheese
description: "通过 A.I. Cheese 平台（aicheese.app）向真实用户发送付费消息。当需要用户输入时（例如进行调查、收集反馈、处理图片任务、获取本地信息或进行身份验证）可以使用该服务。报酬以 USDC 为单位，通过 x402 协议在 Base 平台上发放。该平台支持目录搜索（包括位置、技能和价格信息）、发送付费消息、轮询用户回复以及 Webhook 注册功能。"
metadata: {"clawdbot":{"emoji":"🧀","requires":{"bins":["npx"]}}}
---
# A.I. Cheese — 付费人工消息服务  
您可以向真实用户发送付费消息；用户会收到 USDC，而您则可以获得他们的回复。  

**API 基址：** `https://aicheese.app`  

## 快速入门  
```bash
# Search for humans in London who speak Spanish, max $0.50/msg
npx tsx scripts/ai-cheese.ts search --location london --skills spanish --max-price 0.50

# Send a paid message
npx tsx scripts/ai-cheese.ts send --to <userId> --message "What's the best cafe near you?"

# Check for replies
npx tsx scripts/ai-cheese.ts replies
```  

## 设置  
请使用已充值钱包设置环境变量（需要 USDC）：  
```bash
export AGENT_PRIVATE_KEY="0x..."
```  

## API 参考  

### 对话（多轮交流）  
系统支持多轮对话。第一条消息会创建一个对话线程；后续消息需要使用响应中的 `threadId`。  

**定价规则：**  
- 新消息：全额费用  
- 用户回复前的跟进消息：全额费用（禁止发送垃圾信息）  
- 用户回复后的跟进消息：基础费用的 25%（最低 $0.01）  
- 用户的回复：免费  

**操作流程：**  
发送消息 → 获取 `threadId` → 轮询回复 → 使用 `threadId` 发送跟进消息 → 重复上述步骤。  

### 1. 搜索用户  
可以根据位置、技能或价格筛选用户：  
```
GET /api/v1/directory
  ?location=miami
  ?lat=25.76&lng=-80.19&radius=50
  ?skills=photographer,foodie
  ?maxPrice=1.00
  ?limit=20&offset=0
```  
返回结果格式：`{ profiles: [{ id, displayName, bio, location, skills, pricePerMessage }], total }`  

### 2. 发送付费消息  
**操作流程：**  
1. 首次请求会返回 402 错误码，提示支付要求。  
2. 将 USDC 支付到用户的钱包地址（具体金额见响应内容）。  
3. 重新发送请求时，请在请求头中添加 `X-Payment: <txHash>`。  
4. 消息发送成功后，系统会返回 `{ ok: true, messageId, threadId }`。  
跟进消息时，请在消息正文中包含 `threadId`；如果用户已回复，费用将降至基础费用的 25%。  

### 3. 轮询回复  
**操作流程：**  
系统会返回回复信息：`{ replies: [{ messageId, replyContent, replyAttachments, replyAt, amountPaid }] }`。  
`replyAttachments` 参数包含上传的照片的 URL（例如：`/api/v1/files/abc.jpg`）。  

### 4. 注册 Webhook  
用户回复时，系统会立即发送通知：  
```
POST /api/v1/agent/webhook
Body: { agentId, url, secret }
```  
Webhook 的请求数据中包含 `X-Webhook-Signature`（使用密钥对消息内容进行 HMAC-SHA256 计算生成的签名）。  

## CLI 脚本  
随附的 `scripts/ai-cheese.ts` 脚本可自动处理整个付费流程：  
- `search`：根据条件搜索用户  
- `send --to <id> --message "..."`：发送消息  
- `replies`：轮询用户回复  
- `webhook --url <url>`：注册 Webhook  

**使用方法：**  
运行命令：`npx tsx <skill-path>/scripts/ai-cheese.ts <command> [options]`  

**应用场景：**  
- **调查**：询问用户的地区、意见或经验  
- **反馈**：收集用户对应用、想法或产品的真实反馈  
- **图片请求**：请求用户提供特定地点、产品或商场的照片  
- **本地信息**：查找附近的人以获取实地信息  
- **验证**：通过人工审核 AI 生成的内容  

**提示：**  
- 调查类任务：每条消息费用为 $0.10–$0.25  
- 需要专业知识的任务：每条消息费用为 $0.50–$5.00  
- 可按地理位置筛选用户  
- 可按用户技能筛选合适的回答者  
- 可每隔几分钟轮询一次回复，或使用 Webhook 实现实时通知  
- 回复内容可包含图片（查看 `replyAttachments` 参数）