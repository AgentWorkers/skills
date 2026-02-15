---
name: phone-voice
description: 通过 Twilio 将 ElevenLabs 的代理连接到您的 OpenClaw 系统。该解决方案支持来电显示（caller ID）认证、语音 PIN 安全机制、来电筛选功能、数据注入（memory injection）以及通话费用追踪。
version: 2.0.0
author: Fred (@FredMolty)
---

# 手机语音集成

将您的 OpenClaw 转变为可通过电话呼叫的助手，使用 ElevenLabs Agents 和 Twilio 实现。

**您将获得：**
- 📞 从任何电话拨打您的机器人
- 🔐 来电显示号码身份验证 + 语音 PIN 安全机制
- 🛡️ 呼叫筛选（基于白名单）
- 🧠 完整的记忆上下文（加载 MEMORY.md 和 USER.md 文件）
- 💰 每次通话的成本追踪
- 📝 带有摘要的通话记录
- ⏱️ 调用速率限制
- 🌐 永久隧道（Cloudflare）或临时隧道（ngrok）

## 架构

```
Phone → Twilio → ElevenLabs Agent → Your Bridge → Anthropic Claude → OpenClaw Tools
                                          ↓
                                    Memory Context
                                    (MEMORY.md, USER.md)
```

**流程：**
1. 来电者拨打您的 Twilio 号码
2. Twilio 将呼叫路由到 ElevenLabs Agent
3. Agent 将聊天结果发送到您的桥接服务器（模拟 OpenAI API）
4. 桥接服务器将结果翻译成 Anthropic 语言，并注入来自内存文件的上下文
5. Claude 生成响应 → ElevenLabs TTS 生成语音 → 来电者听到该语音

## 先决条件**

- OpenClaw 已安装并运行
- ElevenLabs 账户及 API 密钥
- Twilio 账户及电话号码
- Anthropic API 密钥
- Cloudflare 隧道 **或** ngrok（用于暴露本地服务器）

## 设置

### 1. 在 OpenClaw 中启用聊天结果功能

此功能无需启用——因为桥接服务器会直接调用 Claude，从而让您更好地控制内存注入和成本追踪。

### 2. 创建桥接服务器

桥接服务器是一个 FastAPI 服务器，用于：
- 接收来自 ElevenLabs 的 `/v1/chat/completions` 请求
- 注入记忆上下文（MEMORY.md、USER.md 和实时数据）
- 调用 Anthropic Claude API
- 以 OpenAI 格式返回响应
- 记录成本和通话记录

**关键文件：**
- `server.py` — 包含 /v1/chat/completions 端点的 FastAPI 应用程序
- `fred_prompt.py` — 系统提示生成器（加载内存文件）
- `.env` — 包含 API 密钥、令牌和白名单
- `contacts.json` — 用于筛选来电者的白名单

### 3. 设置 Cloudflare 隧道（推荐）

**永久且安全的替代方案：** 使用 Cloudflare 隧道：

在 Cloudflare DNS 中添加 CNAME 设置：
```
voice.yourdomain.com → <tunnel-id>.cfargotunnel.com
```

**或使用 ngrok（临时方案）：**
```bash
ngrok http 8013
```

### 4. 配置 ElevenLabs Agent

#### 选项 A：手动配置（通过界面）
1. 登录 ElevenLabs 仪表板 → 对话式 AI
2. 创建新代理
3. 在 LLM 设置中设置 URL：`https://voice.yourdomain.com/v1/chat/completions`
4. 添加请求头：`Authorization: Bearer <YOUR_BRIDGE_TOKEN>`

#### 选项 B：编程配置（通过 API）

```bash
# Step 1: Store your bridge auth token as a secret
curl -X POST https://api.elevenlabs.io/v1/convai/secrets \
  -H "xi-api-key: YOUR_ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "new",
    "name": "bridge_auth_token",
    "value": "YOUR_BRIDGE_AUTH_TOKEN"
  }'

# Response: {"secret_id": "abc123..."}

# Step 2: Create the agent
curl -X POST https://api.elevenlabs.io/v1/convai/agents/create \
  -H "xi-api-key: YOUR_ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_config": {
      "agent": {
        "language": "en",
        "prompt": {
          "llm": "custom-llm",
          "prompt": "You are a helpful voice assistant.",
          "custom_llm": {
            "url": "https://voice.yourdomain.com/v1/chat/completions",
            "api_key": {"secret_id": "abc123..."}
          }
        }
      }
    }
  }'
```

### 5. 连接 Twilio 电话号码

在 ElevenLabs 代理设置中：
1. 进入 **电话** 部分
2. 输入 Twilio 账户 SID 和认证令牌
3. 选择您的 Twilio 电话号码
4. 保存设置

完成！您的机器人现在可以通过该电话号码接听来电了。

## 安全特性

### 来电显示号码身份验证
自动识别白名单内的号码：
```json
// contacts.json
{
  "+12505551234": {
    "name": "Alice",
    "role": "family"
  }
}
```

### 语音 PIN 验证
对于未知来电者或需要高级安全性的操作：
```python
VOICE_PIN = "banana"  # Set in .env
```

来电者必须输入 PIN 码才能继续通话。

### 呼叫筛选
未知号码会听到接待员的提示：
> “我是 Fred 的助手。我可以留言或帮助您解答一般性问题。”

### 调用速率限制
可配置每小时调用次数限制：
```python
RATE_LIMIT_PER_HOUR = 10
```

防止滥用和成本失控。

## 内存注入

桥接服务器在每次通话前会自动加载以下内容：
- `MEMORY.md` — 关于用户、项目和偏好的长期信息
- `USER.md` — 用户信息（姓名、位置、时区）
- 最近的通话记录

**实时数据注入：**
- 当前时间/日期
- 天气信息（可选，通过 API 获取）
- 日历事件（可选，通过 gog CLI 获取）

所有这些数据都会在 Claude 开始对话之前被注入到系统提示中。

## 成本追踪

每次通话都会被记录到 `memory/voice-calls/costs.jsonl` 文件中：
```json
{
  "call_sid": "CA123...",
  "timestamp": "2026-02-03T10:30:00",
  "caller": "+12505551234",
  "duration_sec": 45,
  "total_cost_usd": 0.12,
  "breakdown": {
    "twilio": 0.02,
    "elevenlabs": 0.08,
    "anthropic": 0.02
  }
}
```

您可以分析这些 JSONL 文件以追踪每月的通话费用。

## 使用示例

**如何呼叫您的机器人：**
1. 拨打您的 Twilio 号码
2. 如果您在白名单内 → 开始正常对话
3. 如果您是未知号码 → 进入接待员模式
4. 询问机器人查看日历、发送消息、设置提醒等

** outbound calling（可选）：**
```bash
curl -X POST https://voice.yourdomain.com/call/outbound \
  -H "Authorization: Bearer <BRIDGE_TOKEN>" \
  -d '{"to": "+12505551234", "message": "Reminder: dentist at 3pm"}'
```

## 配置选项

**环境变量（.env）：**
```bash
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=sk_...
ELEVENLABS_AGENT_ID=agent_...
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_NUMBER=+1...
LLM_BRIDGE_TOKEN=<random-secure-token>
VOICE_PIN=<your-secret-word>
CLAWD_DIR=/path/to/clawd
```

**白名单（contacts.json）：**
```json
{
  "+12505551234": {"name": "Alice", "role": "family"},
  "+12505555678": {"name": "Bob", "role": "friend"}
}
```

## 高级功能：工作时间限制

仅在工作时间内允许通话：
```python
# In server.py
OFFICE_HOURS = {
    "enabled": True,
    "timezone": "America/Vancouver",
    "weekdays": {"start": "09:00", "end": "17:00"},
    "weekends": False
}
```

非工作时间 → 自动转接语音信箱。

## 调试

**直接测试桥接服务器：**
```bash
curl -X POST https://voice.yourdomain.com/v1/chat/completions \
  -H "Authorization: Bearer <BRIDGE_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

**查看日志：**
```bash
tail -f ~/clawd/memory/voice-calls/bridge.log
```

**验证 Twilio Webhook：**
1. 拨打您的电话号码
2. 查看 Twilio 控制台 → 呼叫日志 → Webhook 状态
3. 应能看到来自 ElevenLabs 的 200 状态码响应

## 成本估算

**每分钟费用明细：**
- Twilio：约 0.01 美元/分钟（ inbound 呼叫）+ 运营商费用
- ElevenLabs TTS：约 0.05 美元/分钟（取决于语音质量）
- Anthropic Claude：约 0.01 美元/分钟（取决于令牌使用量）
- **总计：约 0.07-0.10 美元/分钟**（每小时通话时间约 4-6 分钟）

请使用调用速率限制和呼叫筛选功能来控制成本。

## 对比：本教程与基础教程

**ElevenLabs 官方教程：**
- ✅ 提供基本集成功能
- ❌ 无安全机制
- ❌ 无内存持久化功能
- ❌ 无成本追踪功能
- ❌ 使用临时 ngrok 隧道

**本教程（Phone Voice v2.0）：**
- ✅ 具备上述所有功能
- ✅ 来电显示号码身份验证 + PIN 安全机制
- ✅ 跨通话记录共享
- ✅ 成本追踪与分析功能
- ✅ 永久隧道（Cloudflare）
- ✅ 调用速率限制
- ✅ 呼叫筛选
- ✅ 通话记录保存

## 链接**

- ElevenLabs Agents：https://elevenlabs.io/conversational-ai
- Twilio：https://www.twilio.com/
- Cloudflare 隧道：https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/
- 参考实现代码：（如有需要可联系 FredMolty）

## 许可证

MIT 许可证 — 可自由使用，如需致谢请注明来源。

---

**由 Fred (@FredMolty) 开发 — 自 2026 年起使用 OpenClaw 运行。**