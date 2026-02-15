---
name: ringbot
description: 执行出站人工智能电话呼叫。适用于需要拨打企业电话、通过电话订购食物、安排预约或任何需要语音通话的任务。触发词包括 "call"（呼叫）、"phone"（电话）、"dial"（拨号）、"ring"（响铃）、"order pizza"（订购披萨）、"make reservation"（预订）和 "schedule appointment"（安排预约）。
---

# RingBot - 人工智能电话服务

使用人工智能语音代理发起外拨电话，实现自然流畅的对话。

## 💰 为什么选择 RingBot？（语音AI成本降低99%）

**传统语音AI服务费用：** 每分钟0.10-0.50美元（例如ElevenLabs、PlayHT等）
**RingBot费用：** 每分钟约0.01美元（仅收取Twilio的电话费用！）

| 组件        | 提供商        | 费用        |
|------------|-------------|------------|
| STT（语音转文本）   | Groq Whisper   | **免费**       |
| LLM（人工智能模型） | Groq Llama 3.3 70B | **免费**       |
| TTS（文本转语音）   | Groq Orpheus    | **免费**       |
| 语音基础设施 | LiveKit Cloud   | **免费 tier**     |
| 电话服务     | Twilio       | 每分钟约0.01美元   |

**您只需支付通过Twilio产生的实际通话费用。**

## 📦 使用RingBot的两种方式

### 选项1：自行搭建（免费 - 需自行购买相关服务）

您可以完全免费搭建自己的基础设施，只需支付Twilio的电话费用。

**所需账户：**

1. **Twilio** - https://twilio.com
   - 电话号码（每月约1美元）+ 通话费用（每分钟约0.01美元）
   - 获取：`TWILIO_ACCOUNT_SID`、`TWILIO_AUTH_TOKEN`、`TWILIO_PHONE_NUMBER`

2. **LiveKit Cloud** - https://cloud.livekit.io（免费 tier）
   - 创建项目并配置SIP trunk连接到Twilio
   - 获取：`LIVEKIT_URL`、`LIVEKIT_API_KEY`、`LIVEKIT_API_SECRET`、`LIVEKIT_SIP_TRUNK_ID`

3. **Groq** - https://console.groq.com（完全免费）
   - 获取API密钥，并同意TTS服务条款：https://console.groq.com/playground?model=canopylabs%2Forpheus-v1-english
   - 获取：`GROQ_API_KEY`

```bash
# .env for DIY setup
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_key
LIVEKIT_API_SECRET=your_secret
LIVEKIT_SIP_TRUNK_ID=your_trunk_id
GROQ_API_KEY=your_groq_key
```

### 选项2：托管服务（付费 - 仅需连接Twilio）

如果您不想自行搭建LiveKit和Groq，可以选择我们的托管服务：

- ✅ 无需配置LiveKit和Groq
- ✅ 无需自行设置任何服务
- ✅ 只需连接您的Twilio账户
- 💰 按分钟计费，且存在通话量限制

**即将推出** - 如需提前试用，请联系我们：https://talkforceai.com

## 🚀 使用场景

### 1. 电话订餐
> “拨打DeLuca's Pizza的电话，点一份大份pepperoni披萨，选择取餐。”

### 2. 预订服务
> “致电餐厅，为4人预订周六晚上7点的位置。”

### 3. 预约就诊
> “致电Smith医生的办公室，预约下周早上的体检。”

### 4. 客户服务
> “致电Comcast，咨询关于升级互联网套餐的事宜。”

### 5. 个人通话
> “给妈妈打电话，告诉她我爱她，并询问她今天过得怎么样。”

### 6. 潜在客户跟进
> “拨打这个潜在客户的电话，询问他们是否对我们的停车解决方案感兴趣。”

### 7. 自动化日常电话
> “每天早上9点，致电仓库，检查库存情况。”

### 8. 预约提醒
> “致电患者，提醒他们明天的预约时间。”

## 发起电话

**参数：**
- `to` - 电话号码（E.164格式，例如+1XXXXXXXXXX）
- `purpose` - 通话目的（指导人工智能的行为）
- `context` - 背景信息、具体请求以及需要收集的数据

## 示例：订披萨

**步骤1：查找餐厅**
```bash
goplaces search "pizza" --lat 41.36 --lng="-72.56" --limit 3
```

**步骤2：获取餐厅电话号码**
```bash
goplaces details ChIJRdQwYs4v5okRY2gp8pgskJ0
# Phone: (860) 663-3999
```

**步骤3：发起电话**
```bash
curl -X POST http://localhost:8000/ringbot/call \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+18606633999",
    "purpose": "Order a pizza for pickup",
    "context": "Order: 1 large pepperoni pizza. Customer name: Greg. Ask for pickup time and total."
  }'
```

## 提高通话效果的小贴士

**通话目的**：保持语句简洁明了：
- ✅ “订购一份披萨，选择取餐方式。”
- ✅ “预约一次牙齿清洁服务。”
- ❌ “打电话只是为了询问或下单。”

**通话背景信息**：提供详细信息：
- 客户/来电者的姓名
- 具体的订单或请求内容
- 客户的偏好和特殊要求
- 需要收集的回复信息

## 服务管理

**启动语音代理：**
```bash
cd /path/to/ringbot/src && python agent.py start
```

**启动API服务：**
```bash
cd /path/to/ringbot && python main.py
```

**查看通话状态：**
```bash
curl http://localhost:8000/ringbot/call/{call_id}
```