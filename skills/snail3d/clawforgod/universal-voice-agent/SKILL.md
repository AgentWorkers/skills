---
name: universal-voice-agent
description: 实时目标导向的语音呼叫代理。适用于需要通过电话实现特定目标的场景：下订单、预订服务、提供客户服务、进行鼓励性通话，或进行任何以对话为目的的沟通。Haiku 使用您的声音实时控制通话过程（由 ElevenLabs 提供技术支持），自动转录对方的回答（由 Groq Whisper 负责），智能地适应对话的节奏，处理通话中的沉默或暂停情况，并在通话结束后向您发送短信总结。完全无需编写脚本，实现纯实时的智能交互。
---

# Universal Voice Agent

该语音助手能够通过电话实现各种目标。Haiku能够自然地进行对话、实时适应对话内容，并自主处理整个通话流程。

## 快速入门

### 打电话

```bash
universal-voice-agent call \
  --goal "Order 2 large pepperonis for pickup at 6pm" \
  --phone "+1-555-123-4567" \
  --notify-to "+1-555-730-8926"
```

Haiku的运作流程：
1. 通过Twilio拨打电话
2. 听取对方的回答（使用Groq的Whisper技术进行语音转录）
3. 根据当前对话内容进行实时推理（利用Claude的推理引擎）
4. 用你的声音进行回答（通过ElevenLabs的TTS技术）
5. 重复上述步骤，直到目标达成或超时
6. 向你发送短信总结通话内容

### 示例

**下单示例：**
```bash
universal-voice-agent call \
  --goal "Order 2 large pepperonis for pickup at 6pm" \
  --phone "+1-555-123-4567"
```

**客户服务示例：**
```bash
universal-voice-agent call \
  --goal "Find out the cancellation policy and confirm my appointment" \
  --phone "+1-555-987-6543"
```

**鼓励他人示例：**
```bash
universal-voice-agent call \
  --goal "Call John and encourage him about his recent wins" \
  --phone "+1-555-555-5555"
```

**寻求支持示例：**
```bash
universal-voice-agent call \
  --goal "Get a refund for order #12345" \
  --phone "+1-800-123-4567"
```

## 工作原理

### 实时语音交互循环

```
Goal: "Order 2 large pepperonis"
Phone: 555-123-4567

[DIAL]
  ↓
[LISTEN] (Groq Whisper) → "Hi, Mario's Pizza!"
  ↓
[THINK] (Haiku) → "They answered, now I'll state my order"
  ↓
[SPEAK] (ElevenLabs) → "Hi! I'd like to order 2 large pepperonis..."
  ↓
[LISTEN] (Groq Whisper) → "Sure, what else?"
  ↓
[THINK] (Haiku) → "They're ready. I should give toppings and details."
  ↓
[SPEAK] (ElevenLabs) → "No onions, and pickup at 6pm"
  ↓
[LISTEN] (Groq Whisper) → "$35, see you at 6."
  ↓
[THINK] (Haiku) → "Goal achieved! Order confirmed."
  ↓
[SEND SMS] → "✅ Order placed: 2 large pepperoni, pickup 6pm, $35"
  ↓
[HANGUP]
```

### 主要特性

- **实时推理**：
  - Haiku会记录完整的对话历史
  - 根据对话情境而非预设脚本来决定下一步的回应内容
  - 能够自然地应对意外的对话情况

- **静音处理**：
  - 检测对方是否处于静音状态（例如挂断电话等）
  - 静默5秒后：等待对方回应
  - 静默10秒后：询问“你好吗？你还在吗？”
  - 静默5分钟后：智能地挂断电话

- **自然的对话节奏**：
  - 回应延迟小于2秒
  - 说话速度与人类相似（使用ElevenLabs的TTS技术）
  - 会自然地暂停以倾听对方的声音

- **智能超时机制**：
  - 总通话时间最长为20分钟
  - 挂断等待时间最长为5分钟
  - 在放弃尝试前会询问“有人吗？”

- **短信总结**：
  - 通话结束后，会向你发送短信，内容包括：
    - 通话状态（✅ 成功完成，❌ 失败）
    - 通话简要回顾
    - 重要确认信息/细节
    - 通话时长

## 配置

### 目标设定

可以使用任何自然语言语句来设定目标，例如：
- “订购2个大号意大利辣香肠，下午6点取货”
- “查询取消政策”
- “给John打电话并鼓励他”
- “为订单#12345申请退款”

Haiku会解析你的目标并调整对话内容以实现该目标。

### 电话号码

电话号码格式为E.164：`+1-555-123-4567` 或 `555-123-4567`

### 可选配置项

```bash
universal-voice-agent call \
  --goal "Order 2 large pepperonis" \
  --phone "555-123-4567" \
  --context "Restaurant: Mario's Pizza, Budget: $40, Dietary: no onions" \
  --notify-to "555-730-8926"
```

## 相关脚本

- **agent.js**：主要控制脚本，负责管理Twilio通话和发送短信总结
- **transcriber.js**：负责语音转录的Groq Whisper服务
- **thinker.js**：Haiku的推理引擎
- **speaker.js**：负责语音输出的ElevenLabs TTS服务
- **silence-handler.js**：用于检测通话中的静音、挂断等异常情况

## 参考资料

- **ARCHITECTURE.md**：实时语音交互循环的设计方案
- **LATENCY.md**：优化响应时间（确保小于2秒）

## 所需凭证

- **Twilio**：账户SID、认证令牌、电话号码
- **ElevenLabs**：API密钥及你的语音识别ID
- **Groq**：用于语音转录的API密钥
- **Claude API** 或 **Clawdbot Gateway**：用于Haiku的推理功能

相关配置信息请保存在`ENVIRONMENT.md`或`TOOLS.md`文件中。