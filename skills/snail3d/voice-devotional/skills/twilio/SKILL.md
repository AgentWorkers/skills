# Twilio 技能 - 语音通话、短信及双向消息传递

本技能实现了与 Twilio 的全面集成，支持发起语音通话、发送短信以及接收并自动回复短信。

## 快速链接

- **发送短信：** `sms.py`  
- **发起语音通话：** `call.py`  
- **Webhook 服务器：** `webhook_server.py`  
- **回复短信：** `respond_sms.py`  
- **设置指南：** 请参阅下方的“设置”部分  
- **故障排除：** 请参阅本文档末尾  

---

## 设置

### 1. 先决条件

- Python 3.8 或更高版本  
- 拥有启用了短信和语音通话功能的 Twilio 账户  
- （可选）使用 ngrok 或 Tailscale 将 webhook 暴露到互联网  

### 2. 安装依赖项  

```bash
cd ~/clawd/skills/twilio
pip install -r requirements.txt
```  

验证安装结果：  
```bash
python -c "from twilio.rest import Client; from flask import Flask; print('✓ All dependencies installed')"
```  

### 3. 设置环境变量  

在使用任何脚本之前，请先导出这些环境变量：  
```bash
export TWILIO_ACCOUNT_SID="AC35fce9f5069e4a19358da26286380ca9"
export TWILIO_AUTH_TOKEN="a7700999dcff89b738f62c78bd1e33c1"
export TWILIO_PHONE_NUMBER="+19152237302"
export ELEVENLABS_API_KEY="sk_98316c1321b6263ab8d3fc46b8439c23b9fc076691d85c1a"
```  

或者创建一个 `.env` 文件：  
```bash
# .env
TWILIO_ACCOUNT_SID=AC35fce9f5069e4a19358da26286380ca9
TWILIO_AUTH_TOKEN=a7700999dcff89b738f62c78bd1e33c1
TWILIO_PHONE_NUMBER=+19152237302
ELEVENLABS_API_KEY=sk_98316c1321b6263ab8d3fc46b8439c23b9fc076691d85c1a
```  

然后加载该文件：  
```bash
set -a; source .env; set +a
```  

**⚠️ 重要提示：** **切勿将包含真实凭据的 `.env` 文件提交到代码仓库。** 应将其添加到 `.gitignore` 文件中：  
```
.env
.env.local
*.log
```  

### 4. 验证凭据  

```bash
# Check that variables are set
echo "Account SID: $TWILIO_ACCOUNT_SID"
echo "Phone: $TWILIO_PHONE_NUMBER"

# Test with a simple SMS
python sms.py --phone "+19152134309" --message "Hello from Twilio skill!"
```  

---

## 功能  

### 1. 发送短信  

向任意电话号码发送短信。  

```bash
python sms.py --phone "+19152134309" --message "Hello!"
```  

**选项：**  
- `--phone`（必选）：接收方电话号码（E.164 格式，例如：`+19152134309`）  
- `--message`（必选）：短信内容  
- `--json`：以 JSON 格式输出响应  

**响应：**  
```json
{
  "status": "success",
  "message_sid": "SM1234567890abcdef",
  "phone": "+19152134309",
  "message": "Hello!",
  "from_number": "+1 (915) 223-7302",
  "segments": 1
}
```  

### 2. 发起语音通话  

使用文本转语音（TTS）功能发起语音通话。  

```bash
python call.py --phone "+19152134309" --message "Hello, this is a test call"
```  

**选项：**  
- `--phone`（必选）：接收方电话号码（E.164 格式）  
- `--message`（必选）：要播放的语音内容  
- `--voice`（可选）：ElevenLabs 提供的语音 ID（默认：Rachel）  
- `--json`：以 JSON 格式输出响应  

**响应：**  
```json
{
  "status": "success",
  "call_sid": "CA1234567890abcdef",
  "phone": "+19152134309",
  "message": "Hello, this is a test call",
  "from_number": "+1 (915) 223-7302"
}
```  

### 3. 接收短信（Webhook 服务器）  

启动 webhook 服务器以自动接收短信：  
```bash
python webhook_server.py
```  

该服务器：  
- ✅ 监听来自 Twilio 的 POST 请求（默认端口为 5000）  
- ✅ 将对话记录存储为 JSON 格式  
- ✅ 将短信转发至 Clawdbot 网关  
- ✅ 验证 Twilio 签名以确保安全性  
- ✅ 为每个电话号码维护对话状态  

**服务器选项：**  
- `--host`：绑定地址（默认：127.0.0.1）  
- `--port`：端口号（默认：5000）  
- `--debug`：启用调试模式  
- `--gateway-url`：Clawdbot 网关 URL（默认：`http://localhost:18789`）  
- `--gateway-token`：网关认证令牌  

**示例：**  
```bash
python webhook_server.py --port 5000 --debug
```  

**服务器端点：**  
```
POST   /sms                          - Receive Twilio webhook
GET    /health                        - Health check
GET    /conversations                 - List all conversations
GET    /conversations/<phone>         - Get specific conversation
```  

### 4. 回复短信  

使用 `respond_sms.py` 回复收到的短信：  
```bash
# Send a reply
python respond_sms.py --to "+19152134309" --message "Thanks for texting!"

# View conversation history
python respond_sms.py --to "+19152134309" --view

# List all active conversations
python respond_sms.py --list-conversations
```  

**选项：**  
- `--to`：接收短信的电话号码  
- `--message`：回复内容  
- `--view`：查看与该号码的对话记录  
- `--list-conversations`：显示所有活跃对话  
- `--json`：以 JSON 格式输出  

**示例响应：**  
```bash
# Send reply
$ python respond_sms.py --to "+19152134309" --message "Got it!"
✓ SMS sent to +19152134309
  SID: SM1234567890abcdef
  Message: Got it!

# View conversation
$ python respond_sms.py --to "+19152134309" --view
Conversation with +19152134309
Started: 2024-02-03T10:30:00
Total messages: 5

Recent messages:
[10:31] ← Them: Hey, how are you?
[10:32] → You: Doing well!
[10:35] ← Them: Great, when are we meeting?
[10:36] → You: Tomorrow at 2pm
[10:37] ← Them: Perfect!

# List conversations
$ python respond_sms.py --list-conversations
Phone Number    Messages   Last Message
+19152134309    5          2024-02-03
+19154567890    3          2024-02-02
Total: 2 conversations
```  

---

## 双向短信工作流程  

系统处理短信发送和接收的流程如下：  
```
Incoming SMS from User
         ↓
    [Twilio Cloud]
         ↓
webhook_server.py (POST /sms)
         ├→ Validate signature
         ├→ Store in conversation_db.json
         ├→ Forward to Clawdbot gateway
         └→ Return 200 OK to Twilio
         ↓
Clawdbot Gateway
         ├→ Notify user in Telegram/chat
         └→ (User crafts reply)
         ↓
User runs: respond_sms.py --to +1234567890 --message "Reply text"
         ↓
respond_sms.py
         ├→ Create Twilio client
         ├→ Send SMS
         ├→ Record in conversation_db.json
         └→ Return success/error
         ↓
    [Twilio Cloud]
         ↓
   Outgoing SMS to User
```  

---

## 公共 URL 设置（Webhook 所需）  

Webhook 服务器运行在本地。为了接收 Twilio 发来的短信，需要一个公共 URL。可以选择以下方式之一：  

### 选项 A：ngrok（简单且临时）  

最适合测试使用。  

```bash
# Install ngrok (one-time)
brew install ngrok  # macOS
# or visit https://ngrok.com/download

# Start ngrok tunnel
ngrok http 5000

# Output:
# Forwarding  https://1a2b3c4d5e6f.ngrok.io -> http://localhost:5000
```  

你的公共 URL 为 `https://1a2b3c4d5e6f.ngrok.io/sms`（注意：`/sms` 是端点地址）  

**在 Twilio 控制台：**  
1. 转到“电话号码” → “活跃号码”  
2. 点击你的号码  
3. 设置“来电时” → “Webhooks” → “消息传递”  
4. 粘贴：`https://1a2b3c4d5e6f.ngrok.io/sms`  
5. 保存设置  

### 选项 B：Tailscale Funnel（长期使用）  

最适合在生产环境中使用。  

```bash
# Install Tailscale (one-time)
brew install tailscale
tailscale up

# Enable funnel on port 5000
tailscale funnel 5000

# Output:
# Access point: https://your-machine.tail12345.ts.net
```  

你的公共 URL 为 `https://your-machine.tail12345.ts.net/sms`  

**在 Twilio 控制台：**  
1. 转到“电话号码” → “活跃号码”  
2. 将消息传递设置为：`https://your-machine.tail12345.ts.net/sms`  
3. 保存设置  

### 选项 C：静态 IP/端口转发（高级配置）  

如果你拥有静态公共 IP 和路由器访问权限：  
1. 将端口 5000 转发到本地机器  
2. 使用：`https://your-public-ip:5000/sms`  
3. 建议使用域名和 SSL 证书以增强安全性  

---

## 运行系统  

### 开发环境设置（一步完成）  

终端 1：启动 webhook 服务器：  
```bash
cd ~/clawd/skills/twilio
source .env  # Load credentials
python webhook_server.py --port 5000 --debug
```  

终端 2：启动 ngrok 隧道：  
```bash
ngrok http 5000
```  

终端 3：测试发送回复：  
```bash
cd ~/clawd/skills/twilio
source .env
python respond_sms.py --to "+19152134309" --message "Test reply"
```  

### 生产环境设置（使用 Tailscale）  

终端 1：确保 Tailscale 正在运行：  
```bash
tailscale up
tailscale funnel 5000
```  

终端 2：启动 webhook 服务器：  
```bash
cd ~/clawd/skills/twilio
source .env
python webhook_server.py --port 5000
```  

完成设置后，你可以通过 `https://your-machine.tail12345.ts.net/sms` 访问服务器。  

---

## 对话记录  

所有对话记录存储在 `~/.clawd/twilio_conversations.json` 文件中。  

**格式：**  
```json
{
  "+19152134309": {
    "phone": "+19152134309",
    "created_at": "2024-02-03T10:30:00",
    "last_message_at": "2024-02-03T11:45:00",
    "message_count": 5,
    "messages": [
      {
        "timestamp": "2024-02-03T10:30:00",
        "direction": "inbound",
        "body": "Hey!",
        "sid": "SM1234567890abcdef"
      },
      {
        "timestamp": "2024-02-03T10:31:00",
        "direction": "outbound",
        "body": "Hi there!",
        "sid": "SM1234567890abcdef"
      }
    ]
  }
}
```  

**查看对话记录：**  
```bash
python respond_sms.py --to "+19152134309" --view
```  

**备份对话记录：**  
```bash
cp ~/.clawd/twilio_conversations.json ~/Desktop/twilio_backup.json
```  

**清除对话记录（请谨慎操作！）：**  
```bash
rm ~/.clawd/twilio_conversations.json
```  

## 日志  

服务器日志存储在 `~/.clawd/twilio_webhook.log` 文件中。  

**查看实时日志：**  
```bash
tail -f ~/.clawd/twilio_webhook.log
```  

**解析日志：**  
```bash
grep "ERROR" ~/.clawd/twilio_webhook.log
grep "SMS sent" ~/.clawd/twilio_webhook.log
```  

## 安全性与最佳实践  

### 已实施的安全措施：  
- ✅ 在 webhook 中验证 Twilio 签名  
- ✅ 使用环境变量存储凭据（避免硬编码）  
- ✅ 处理请求超时  
- ✅ 记录错误日志（敏感数据已清洗）  
- ✅ 验证电话号码格式（E.164 格式）  

### 额外建议：  

1. **保密凭据：**  
   - 绝不分享账户 SID 或认证令牌  
   - 定期更新令牌  
   - 使用 `.env` 文件并将其添加到 `.gitignore` 文件中  

2. **监控使用情况：**  
   - 设置 Twilio 账户提醒，以便及时发现异常活动  
   - 定期查看日志：https://www.twilio.com/console/logs  

3. **保护 webhook：**  
   - 如果使用静态 IP，限制访问范围仅限于 Twilio 的 IP 范围  
   - 在路由器上设置 IP 过滤  
   - 仅启用 HTTPS（ngrok/Tailscale 会自动处理）  

4. **限制请求频率：**  
   - 如果多个用户同时使用 `respond_sms.py`，请实施请求频率限制  
   - 注意 Twilio 的 API 使用量限制及相关费用  

5. **数据保护：**  
   - 对话记录存储在本地（未加密）  
   - 如对话内容敏感，建议对 `~/.clawd/twilio_conversations.json` 进行加密  
   - 定期备份重要对话记录  

---

## 示例  

### 示例 1：自动状态检查  

```bash
#!/bin/bash
# Check server health
curl http://localhost:5000/health | jq .

# Output:
# {
#   "status": "healthy",
#   "timestamp": "2024-02-03T11:00:00",
#   "gateway": "http://localhost:18789",
#   "conversation_db": "/Users/ericwoodard/.clawd/twilio_conversations.json"
# }
```  

### 示例 2：批量回复脚本  

```bash
#!/bin/bash
# Reply to multiple numbers
for phone in "+19152134309" "+19154567890" "+19158901234"; do
  python respond_sms.py --to "$phone" --message "Hello from bulk script!"
  sleep 2  # Avoid rate limiting
done
```  

### 示例 3：与 Clawdbot 集成  

```python
# In a Clawdbot skill
import subprocess
import json

def send_sms(phone, message):
    result = subprocess.run([
        'python', '/path/to/respond_sms.py',
        '--to', phone,
        '--message', message,
        '--json'
    ], capture_output=True, text=True)
    
    return json.loads(result.stdout)

# Use it
response = send_sms("+19152134309", "Hello from Python!")
print(response['message_sid'])
```  

---

## 故障排除  

### “模块未找到：twilio”  

**原因：** 可能未正确安装 Twilio 相关模块。  

### “认证失败”  

1. 确认凭据已正确设置：  
   ```bash
   echo $TWILIO_ACCOUNT_SID
   echo $TWILIO_AUTH_TOKEN
   ```  

2. 在 Twilio 控制台检查凭据：  
   - https://www.twilio.com/console/project/settings  

3. 确认认证令牌未过期  

### “连接被拒绝”（可能是因为 Clawdbot 网关未运行）  

**解决方法：**  
检查 Clawdbot 网关是否正在运行。  

### “Twilio 签名无效”  

**原因：**  
- 请求可能并非来自 Twilio（安全问题）  
- `.env` 文件中的 `TWILIO_AUTH_TOKEN` 有误  
- 或者你使用的是 curl 进行测试（Twilio 签名是按请求生成的）  

**临时禁用签名验证（仅限测试）：**  
```bash
# In webhook_server.py, change:
if not validate_twilio_signature(request):
    return Response("Unauthorized", status=401)

# To:
# Temporarily disabled for testing
# if not validate_twilio_signature(request):
#     return Response("Unauthorized", status=401)
```  

### “短信发送失败”  

**原因：**  
1. 检查接收方电话号码格式（例如：`+19152134309`）  
2. 确认 Twilio 账户已启用短信功能  
3. 检查账户余额  
4. 查看 Twilio 日志：https://www.twilio.com/console/logs  

### “未找到对话记录”  

**原因：**  
Webhook 服务器尚未收到任何短信。  
1. 确认 webhook 服务器正在运行  
2. 检查 ngrok/Tailscale 隧道是否正常工作  
3. 确认 Twilio 配置中的电话号码指向正确的 webhook URL  
4. 用手机尝试发送测试短信  

### “Webhook 服务器无法启动”  

**原因：**  
端口 5000 被其他程序占用。  

**解决方法：**  
检查端口 5000 是否已被占用。  

### 需要帮助？**  
1. 查看日志：`tail -f ~/.clawd/twilio_webhook.log`  
2. 启用调试模式：`python webhook_server.py --debug`  
3. 使用 curl 进行测试：  
   ```bash
   curl -X POST http://localhost:5000/health
   ```  
4. 查阅 Twilio 文档：https://www.twilio.com/docs/sms/quickstart  

---

## 费用  

- **短信：** 每条短信 0.0075 美元  
- **语音通话：** 每分钟 0.013 至 0.025 美元  
- **ElevenLabs TTS：** 每 100 万字符 0.15 美元  

**费用控制建议：**  
- 保持短信内容简短  
- 避免不必要的 API 请求  
- 定期监控 Twilio 账户使用情况  
- 设置账户使用量提醒  

---

## 电话号码格式  

所有电话号码均采用 **E.164** 格式：  

**示例：**  
- 美国：`+1 915 223 7302` → `+19152237302`  
- 英国：`+44 20 7122 3467` → `+442071223467`  
- 加拿大：`+1 416 555 1234` → `+14165551234`  

**脚本支持以下格式：**  
- E.164 格式：`+19152134309`  
- 美国 10 位数字格式：`9152134309`（会自动转换为 `+19152134309`）  
- 带空格/破折号的格式：`(915) 213-4309`（也会被自动转换）  
- 不正确的格式：`1-915-213-4309`（无效）  

---

## 相关技能  

- **Universal Voice Agent**：支持实时语音的通用通话功能  
- **Jami Skill**：点对点语音通信  
- **Sentry Mode**：结合摄像头监控和语音警报的功能  

---

## 许可证  

本技能基于 MIT 许可协议，可自由用于你的项目中。  

---

## 支持资源  

**Twilio 文档：**  
- 短信：https://www.twilio.com/docs/sms  
- 语音通话：https://www.twilio.com/docs/voice  
- Webhook：https://www.twilio.com/docs/usage/webhooks  

**Twilio 控制台：**  
- https://www.twilio.com/console  

**ElevenLabs 文档：**  
- https://elevenlabs.io/docs/  

最后更新时间：2024-02-03