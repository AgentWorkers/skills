---
name: voice-agent-builder
description: 使用 Vapi、Bland.ai 或 Retell 构建和管理语音 AI 代理。您可以创建代理、配置语音、设置提示语、发起外拨电话以及检索通话记录。文档中还提供了平台之间的比较指南。这些工具非常适合用于构建电话代理、交互式语音应答（IVR）系统或以语音为主要交互方式的客户服务系统。
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Vapi API key
metadata: {"openclaw": {"emoji": "\ud83d\udde3\ufe0f", "requires": {"env": ["VAPI_API_KEY"]}, "primaryEnv": "VAPI_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 语音代理构建器

用于构建、配置和管理语音AI代理。支持**Vapi**（主要平台）、**Bland.ai**和**Retell**平台。

## 快速入门

```bash
export VAPI_API_KEY="your-vapi-api-key"

# Create a voice agent
python3 {baseDir}/scripts/vapi_agent.py create-agent '{"name":"Sales Agent","firstMessage":"Hi! How can I help you today?","systemPrompt":"You are a helpful sales assistant for Acme Corp."}'

# Make an outbound call
python3 {baseDir}/scripts/vapi_agent.py call '{"assistantId":"asst_xxx","phoneNumberId":"pn_xxx","customer":{"number":"+15551234567"}}'

# List agents
python3 {baseDir}/scripts/vapi_agent.py list-agents

# List calls
python3 {baseDir}/scripts/vapi_agent.py list-calls
```

## 平台对比

| 特性 | Vapi | Bland.ai | Retell |
|---------|------|----------|--------|
| **最适合** | 定制代理、开发友好 | 简单的外发营销活动 | 企业级应用、低延迟 |
| **延迟** | 约800毫秒 | 约500毫秒 | 约500毫秒 |
| **支持的语言** | 100多种 | 30多种 | 30多种 |
| **自定义LLM** | ✅ 支持任何OpenAI兼容的模型 | ✅ 有限支持 | ✅ 通过API支持 |
| **电话号码** | 可购买/导入 | 可购买/导入 | 可购买/导入 |
| **定价** | 每分钟0.05美元 + 提供商费用 | 每分钟0.09美元（包含所有费用） | 每分钟0.07-0.15美元 |
| **WebSocket** | ✅ | ❌ | ✅ |
| **知识库** | ✅ 内置 | ✅ | ✅ |
| **电话转接** | ✅ | ✅ | ✅ |

**建议：** 首先尝试使用**Vapi**——功能最灵活，文档最完善，社区最活跃。对于简单的高量外发任务，可以选择**Bland**；对于企业级应用且对延迟要求较高的场景，建议使用**Retell**。

详细对比信息请参阅 `{baseDir}/scripts/voice_comparison.md`。

## 代理创建流程

### 1. 选择语音服务
Vapi支持多种TTS（文本转语音）服务提供商：
- **ElevenLabs**：音质最佳，自然度最高（推荐）
- **PlayHT**：音质不错，成本较低
- **Deepgram**：响应速度快，适合实时语音交互
- **Azure**：适用于企业级应用，支持多种语言

### 2. 配置代理
```json
{
  "name": "Appointment Setter",
  "firstMessage": "Hi! This is Sarah from Dr. Smith's office. I'm calling to help you schedule your appointment.",
  "systemPrompt": "You are Sarah, a friendly appointment scheduler...",
  "voice": {
    "provider": "11labs",
    "voiceId": "21m00Tcm4TlvDq8ikWAM"
  },
  "model": {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.7
  },
  "endCallFunctionEnabled": true,
  "maxDurationSeconds": 300,
  "silenceTimeoutSeconds": 30
}
```

### 3. 语音提示设计
语音提示与文本提示有所不同。关键原则如下：
- **保持回答简洁**：每次对话最多1-2句话
- **采用对话式语言**：自然地使用填充词（如“当然可以！”、“明白了！”）
- **处理中断**：考虑到语音代理可能会被中断，设计时要考虑到这一点
- **确认理解**：重复关键信息（如姓名、数字、日期）
- **提供备用选项**：如果听不清楚，可以询问“您能再说一遍吗？”

### 4. 电话号码设置
```bash
# List available phone numbers
python3 {baseDir}/scripts/vapi_agent.py list-phones

# Buy a number (via Vapi dashboard or API)
# Import existing number (Twilio, Vonage)
python3 {baseDir}/scripts/vapi_agent.py import-phone '{"provider":"twilio","number":"+15551234567","twilioAccountSid":"AC...","twilioAuthToken":"..."}'
```

### 5. 通话处理

**外发电话：**
```bash
python3 {baseDir}/scripts/vapi_agent.py call '{"assistantId":"asst_xxx","phoneNumberId":"pn_xxx","customer":{"number":"+15551234567"}}'
```

**来电处理：** 在Vapi控制台中为电话号码分配相应的代理，或通过API进行配置：
```bash
python3 {baseDir}/scripts/vapi_agent.py update-phone '{"id":"pn_xxx","assistantId":"asst_xxx"}'
```

## 集成方案

### 语音 + 客户关系管理（GHL）
1. 语音代理在通话中评估潜在客户的质量
2. 使用Vapi的`serverUrl` webhook捕获通话数据
3. 通话结束后，创建或更新GHL联系人信息
4. 将潜在客户转移到相应的处理流程中
5. 如有需要，安排后续跟进

### 语音 + 日历预订
1. 代理通过日历API查询可用时间
2. 使用相关功能预订约会
3. 通过语音确认日期和时间
4. 通话结束后发送短信确认

### 语音 + 知识库
将文档上传到Vapi的知识库中，以便快速查询相关信息：
```bash
python3 {baseDir}/scripts/vapi_agent.py create-kb '{"name":"Product FAQ","files":["faq.pdf"]}'
```

## 可用命令
```bash
python3 {baseDir}/scripts/vapi_agent.py create-agent '{...}'     # Create new agent
python3 {baseDir}/scripts/vapi_agent.py get-agent <id>            # Get agent details
python3 {baseDir}/scripts/vapi_agent.py list-agents               # List all agents
python3 {baseDir}/scripts/vapi_agent.py update-agent <id> '{...}' # Update agent
python3 {baseDir}/scripts/vapi_agent.py delete-agent <id>         # Delete agent
python3 {baseDir}/scripts/vapi_agent.py call '{...}'              # Make outbound call
python3 {baseDir}/scripts/vapi_agent.py get-call <id>             # Get call details
python3 {baseDir}/scripts/vapi_agent.py list-calls                # List all calls
python3 {baseDir}/scripts/vapi_agent.py list-phones               # List phone numbers
python3 {baseDir}/scripts/vapi_agent.py import-phone '{...}'      # Import phone number
python3 {baseDir}/scripts/vapi_agent.py update-phone '{...}'      # Update phone config
```

## 致谢
本工具由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi)和[agxntsix.ai](https://www.agxntsix.ai)开发。
[YouTube频道](https://youtube.com/@aiwithabidi) | [GitHub仓库](https://github.com/aiwithabidi)
本工具是**AgxntSix Skill Suite**的一部分，专为OpenClaw代理设计。

📅 **需要帮助为您的企业设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)