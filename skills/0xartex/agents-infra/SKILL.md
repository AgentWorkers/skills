---
name: agents-infra
description: AI代理的基础设施：包括电话、电子邮件、社交媒体账户、计算资源、域名以及语音通话功能。支持使用Solana或Base平台上的USDC进行支付，支付方式通过x402实现。
---**基础URL:** `https://agntos.dev`  
**来源:** https://github.com/0xArtex/AgentOS  

## 快速参考  

| 服务 | 端点          | 费用（USDC） |
|---------|--------------|-----------|
| 注册代理    | `POST /agents/register` | 免费       |
| **电话**     |                |            |
| 搜索号码    | `GET /phone/numbers/search?country=US` | 免费       |
| 预配号码    | `POST /phone/numbers`     | 2.00 USDC     |
| 发送短信    | `POST /phone/numbers/:id/send` | 0.05 USDC     |
| 读取消息    | `GET /phone/numbers/:id/messages` | 0.01 USDC     |
| **语音通话**   |                |            |
| 发出通话    | `POST /phone/numbers/:id/call` | 0.10 USDC     |
| 语音合成（TTS） | `POST /phone/calls/:callControlId/speak` | 0.05 USDC     |
| 播放音频    | `POST /phone/calls/:callControlId/play` | 0.05 USDC     |
| 发送DTMF信号 | `POST /phone/calls/:callControlId/dtmf` | 0.02 USDC     |
| 收集输入    | `POST /phone/calls/:callControlId/gather` | 0.05 USDC     |
| 录制通话    | `POST /phone/calls/:callControlId/record` | 0.05 USDC     |
| 挂断通话    | `POST /phone/calls/:callControlId/hangup` | 0.01 USDC     |
| 接听来电    | `POST /phone/calls/:callControlId/answer` | 0.01 USDC     |
| 转接通话    | `POST /phone/calls/:callControlId/transfer` | 0.10 USDC     |
| 列出通话记录 | `GET /phone/numbers/:id/calls` | 0.01 USDC     |
| 通话详情    | `GET /phone/calls/:id`     | 0.01 USDC     |
| **电子邮件**   |                |            |
| 预配收件箱   | `POST /email/inboxes`    | 1.00 USDC     |
| 读取收件箱   | `GET /email/inboxes/:id/messages` | 0.01 USDC     |
| 发送电子邮件 | `POST /email/inboxes/:id/send` | 0.05 USDC     |
| **计算**     |                |            |
| 列出计划    | `GET /compute/plans`    | 免费       |
| 上传SSH密钥   | `POST /compute/ssh-keys`    | 0.10 USDC     |
| 创建服务器    | `POST /compute/servers`    | 5.00–95.00 USDC   |
| 列出服务器    | `GET /compute/servers`    | 0.01 USDC     |
| 服务器状态    | `GET /compute/servers/:id`    | 0.01 USDC     |
| 服务器操作    | `POST /compute/servers/:id/actions` | 0.05 USDC     |
| 调整服务器大小 | `POST /compute/servers/:id/resize` | 0.10 USDC     |
| 删除服务器    | `DELETE /compute/servers/:id`    | 0.05 USDC     |
| **域名**     |                |            |
| 检查可用性   | `GET /domains/check?domain=example.com` | 免费       |
| 域名价格    | `GET /domains/pricing?domain=example` | 免费       |
| 注册域名    | `POST /domains/register`    | 14–88 USDC     |
| DNS记录    | `GET /domains/:domain/dns`    | 免费       |
| 更新DNS记录 | `POST /domains/:domain/dns`    | 免费       |
| 价格信息    | `GET /pricing`      | 免费       |

所有付费端点均使用 **x402** 授权机制：发送请求后收到402响应，使用USDC支付即可完成交易。  

## 认证  

**选项A：代理令牌**（只需注册一次）  
```  
Authorization: Bearer aos_xxxxx  
```  

**选项B：x402支付**（无需注册）  
直接调用任意端点。402响应会提示您需要支付的金额。支付即完成认证。  

## x402工作原理  

1. 调用任何付费端点 → 收到“402 Payment Required”响应。  
2. 将USDC转账至指定地址。  
3. 在请求头中添加`Payment-Signature`字段。  
4. 服务器验证并完成链上支付，然后返回响应。  

**支持的网络：** Solana主网 + Base（EVM）  

---

## 注册代理（免费）  
```bash  
curl -X POST https://agntos.dev/agents/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "walletAddress": "YOUR_SOLANA_PUBKEY"}  
```  
返回代理令牌，保存后用于后续请求：`Authorization: Bearer aos_xxxxx`  

---

## 📱 电话与短信  

### 搜索可用号码（免费）  
```bash  
curl "https://agntos.dev/phone/numbers/search?country=US&limit=5"  
```  

### 预配号码（2.00 USDC）  
```bash  
curl -X POST https://agntos.dev/phone/numbers \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"country": "US"}  
```  
响应示例：  
```json  
{  
  "id": "uuid",  
  "phoneNumber": "+14782058302",  
  "country": "US",  
  "owner": "your-agent",  
  "active": true  
}  
```  

### 发送短信（0.05 USDC）  
```bash  
curl -X POST https://agntos.dev/phone/numbers/PHONE_ID/send \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"to": "+15551234567", "body": "Hello from my agent!"}  
```  

### 读取消息（0.01 USDC）  
```bash  
curl https://agntos.dev/phone/numbers/PHONE_ID/messages \
  -H "Authorization: Bearer aos_xxxxx"  
```  

---

## 📞 语音通话  

### 发出通话（0.10 USDC）  
```bash  
curl -X POST https://agntos.dev/phone/numbers/PHONE_ID/call \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{  
    "to": "+15551234567",  
    "tts": "Hello! I am an AI agent calling you.",  
    "ttsVoice": "female",  
    "record": true  
  }  
```  
响应示例：  
```json  
{  
  "id": "uuid",  
  "callControlId": "v3:xxxxx",  
  "from": "+14782058302",  
  "to": "+15551234567",  
  "status": "initiated",  
  "message": "Calling +15551234567 from +14782058302",  
  "hint": "TTS will play when the call is answered"  
}  
```  
参数说明：  
- `to`：目标电话号码（E.164格式）  
- `tts`：接听时播放的文本转语音内容  
- `ttsVoice`：语音类型（`male`或`female`）  
- `audioUrl`：接听时播放的音频文件URL  
- `record`：是否录制通话（`true`表示录制）  
- `timeoutSecs`：通话超时时间（默认30秒）  

### 通话中的操作  

通话建立后，使用`callControlId`执行以下操作：  

**语音合成（TTS）**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/speak \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"text": "Please press 1 for sales or 2 for support", "voice": "female", "language": "en-US"}  
```  

**播放音频文件**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/play \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"audioUrl": "https://example.com/greeting.mp3"}  
```  

**发送DTMF信号**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/dtmf \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"digits": "1234#"}  
```  

**收集DTMF输入**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/gather \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"maxDigits": 4, "terminatingDigit": "#", "prompt": "Please enter your PIN followed by the pound sign"}'  
```  

**开始录制**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/record \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"format": "mp3"}  
```  

**停止录制**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/record/stop \
  -H "Authorization: Bearer aos_xxxxx"  
```  

**转接通话**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/transfer \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"to": "+15559876543"}  
```  

**接听来电**：  
```bash  
curl -X POST https://agntos.dev/phone/calls/CALL_CONTROL_ID/answer \
  -H "Authorization: Bearer aos_xxxxx"  
```  

### 通话记录  

**列出某个号码的通话记录**：  
```bash  
curl https://agntos.dev/phone/numbers/PHONE_ID/calls \
  -H "Authorization: Bearer aos_xxxxx"  
```  

**获取通话详情**：  
```bash  
curl https://agntos.dev/phone/calls/CALL_ID \
  -H "Authorization: Bearer aos_xxxxx"  
```  

**示例：** 代理拨打餐厅电话：  
1. `POST /phone/numbers/PHONE_ID/call` → 设置通话参数  
2. 等待对方接听  
3. `POST /phone/calls/CTRL_ID/gather` → 收集用户输入（如PIN码）  
4. `POST /phone/calls/CTRL_ID/dtmf` → 发送DTMF信号  
5. `POST /phone/calls/CTRL_ID/speak` → 传达订单信息  
6. `POST /phone/calls/CTRL_ID/hangup` → 结束通话  

---

## 📧 电子邮件  

### 预配收件箱（1.00 USDC）  
```bash  
curl -X POST https://agntos.dev/email/inboxes \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "walletAddress": "YOUR_SOLANA_PUBKEY"}  
```  
返回邮箱地址：`my-agent@agntos.dev`  

### 读取收件箱（0.01 USDC）  
```bash  
curl https://agntos.dev/email/inboxes/INBOX_ID/messages  
```  

### 发送电子邮件（0.05 USDC）  
```bash  
curl -X POST https://agntos.dev/email/inboxes/INBOX_ID/send \
  -H "Content-Type: application/json" \
  -d '{"to": "user@example.com", "subject": "Hello", "body": "Message from my agent"}`  
```  

---

## 💻 计算（VPS）  

### 列出计划（免费）  
```bash  
curl https://agntos.dev/compute/plans  
```  
可用计划示例：  
| 类型 | vCPU | RAM | 磁盘 | 月费 |  
|------|------|-----|------|----------|  
| cx23 | 2 | 4GB | 40GB | $5 |  
| cx33 | 4 | 8GB | 80GB | $9 |  
| cx43 | 8 | 16GB | 160GB | $15 |  
| cx53 | 16 | 32GB | 320GB | $28 |  
| cpx11 | 2 | 2GB | 40GB | $7 |  
| cpx21 | 3 | 4GB | 80GB | $15 |  
| cpx31 | 4 | 8GB | 160GB | $26 |  
| cpx41 | 8 | 16GB | 240GB | $48 |  
| cpx51 | 16 | 32GB | 360GB | $95 |  
```  

### 上传SSH密钥（0.10 USDC）  
```bash  
curl -X POST https://agntos.dev/compute/ssh-keys \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-key", "publicKey": "ssh-ed25519 AAAA..."}`  
返回的`id`用于创建服务器。  

### 创建服务器（5.00–95.00 USDC）  
```bash  
curl -X POST https://agntos.dev/compute/servers \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-server", "serverType": "cx23", "sshKeyIds": [KEY_ID]}  
```  
响应示例：  
```json  
{  
  "id": "12345",  
  "name": "my-server",  
  "serverType": "cx23",  
  "status": "running",  
  "ipv4": "89.167.36.207",  
  "message": "Server created. SSH in with: ssh root@89.167.36.207"  
}  
```  

**安全设计：** 仅使用您的SSH公钥；我们不会访问您的私钥。  

### 服务器操作（0.05 USDC）  
```bash  
curl -X POST https://agntos.dev/compute/servers/SERVER_ID/actions \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"action": "reboot"}  
```  
可执行的操作：`reboot`、`poweron`、`poweroff`、`rebuild`、`reset`  

### 调整服务器大小（0.10 USDC）  
```bash  
curl -X POST https://agntos.dev/compute/servers/SERVER_ID/resize \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"serverType": "cx33"}  
**注意：** 服务器必须处于关闭状态才能调整大小。  

### 删除服务器（0.05 USDC）  
```bash  
curl -X DELETE https://agntos.dev/compute/servers/SERVER_ID \
  -H "Authorization: Bearer aos_xxxxx"  
```  

---

## 🌐 域名  

### 检查可用性（免费）  
```bash  
curl "https://agntos.dev/domains/check?domain=example.com"  
```  

### 获取价格信息（免费）  
```bash  
curl "https://agntos.dev/domains/pricing?domain=example"  
```  

### 注册域名（动态定价）  
```bash  
curl -X POST https://agntos.dev/domains/register \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"domain": "my-agent.dev"}  
```  

### DNS管理（仅限域名所有者）  

```bash  
# 获取DNS记录  
curl https://agntos.dev/domains/my-agent.dev/dns -H "Authorization: Bearer aos_xxxxx"  
# 设置DNS记录  
curl -X POST https://agntos.dev/domains/my-agent.dev/dns \
  -H "Authorization: Bearer aos_xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"records": [{"type": "A", "name": "@", "value": "1.2.3.4"}']  
```  

---

## 支付详情  

- **Solana**：USDC转账至 `B1YEboAH3ZDscqni7cyVnGkcDroB2kqLXCwLs3Ez8oX3`  
- **Base（EVM）**：USDC转账至 `0x7fA8aC4b42fd0C97ca983Bc73135EdbeA5bD6ab2`  
- **x402版本**：2  
- **支付处理方**：`4R67MWivvc52g9BSzQRvQyD8GshttW1QLbnj46usBrcQ`  

## Webhooks  

设置Webhooks以接收事件通知：  
- **短信来电**：通过Telnyx webhook接收短信，数据可 via API查询  
- **语音事件**：`call.initiated`、`call.answered`、`call.hangup`、`call.recording.saved`、`call.gather.ended`  
- **电子邮件**：发送至`*@agntos.dev`的邮件会通过Cloudflare处理并加密存储。