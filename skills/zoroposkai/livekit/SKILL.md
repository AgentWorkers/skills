---
name: livekit
description: 使用 LiveKit 构建语音 AI 代理。适用于开发实时语音应用、语音代理流程（STT-LLM-TTS）、WebRTC 通信或部署对话式 AI。内容包括 LiveKit 代理 SDK、提供商选择（Deepgram、OpenAI、ElevenLabs、Cartesia），以及云部署与自托管部署的差异。
---

# LiveKit 语音 AI 技能

使用 LiveKit 的开源平台构建生产级语音代理。

## 快速入门

```bash
# Install SDK
pip install livekit-agents livekit-plugins-openai livekit-plugins-deepgram livekit-plugins-cartesia

# Or Node.js
npm install @livekit/agents @livekit/agents-plugin-openai
```

## 最小化代理（Python）

```python
from livekit.agents import AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, openai, cartesia

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    session = AgentSession(
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4.1-mini"),
        tts=cartesia.TTS(),
    )
    
    session.start(ctx.room)
    await session.say("Hello! How can I help?")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
```

## 提供商选择

| 组件 | 预算 | 质量 | 低延迟 |
|-----------|--------|---------|-------------|
| **语音转文本（STT）** | Deepgram Nova-3 | AssemblyAI | Deepgram Keychain |
| **大型语言模型（LLM）** | GPT-4.1 mini | Claude Sonnet | GPT-4.1 mini |
| **文本转语音（TTS）** | Cartesia Sonic-3 | ElevenLabs | Cartesia Sonic-3 |

## 语音处理流程与实时交互

**语音转文本-大型语言模型-文本转语音（STT-LLM-TTS）流程：**
- 更高的控制灵活性，可混合使用不同提供商的服务
- 通常成本更低
- 更易于调试

**OpenAI 实时 API：**
- 支持语音转语音功能，表达能力更强
- 成本较高（约 0.10 美元/分钟）
- 控制灵活性较低

## 环境变量

```bash
LIVEKIT_URL=wss://your-app.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

# Provider keys (if not using LiveKit Inference)
OPENAI_API_KEY=
DEEPGRAM_API_KEY=
CARTESIA_API_KEY=
ELEVENLABS_API_KEY=
```

## 工具使用

```python
from livekit.agents import function_tool

@function_tool()
async def get_weather(location: str) -> str:
    """Get current weather for a location."""
    # Your implementation
    return f"Weather in {location}: 72°F, sunny"

session = AgentSession(
    stt=deepgram.STT(),
    llm=openai.LLM(),
    tts=cartesia.TTS(),
    tools=[get_weather],
)
```

## 电话通信（SIP）

```python
from livekit import api

# Outbound call
await lk_api.sip.create_sip_participant(
    api.CreateSIPParticipantRequest(
        sip_trunk_id="trunk-id",
        sip_call_to="+15551234567",
        room_name="my-room",
    )
)
```

## 部署

**LiveKit 云服务：** `livekit-server-cli deploy --project my-project`

**自托管：**
```bash
docker run -d \
  -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  -e LIVEKIT_KEYS="api-key: api-secret" \
  livekit/livekit-server
```

## 成本估算

| 场景 | 每月成本 |
|----------|--------------|
| 开发/测试 | 免费 tier |
| 每月 100 小时语音处理 | 约 150-250 美元 |
| 生产级 B2B 服务 | 约 300-500 美元 |
| 高流量场景 | 需要自托管 |

## 常见应用模式

### 语音指令检测
```python
session = AgentSession(
    turn_detection=openai.TurnDetection(
        threshold=0.5,
        silence_duration_ms=500,
    ),
    ...
)
```

### 中断处理
```python
@session.on("user_speech_started")
async def handle_interruption():
    session.stop_speaking()
```

### 多代理协同工作
```python
await session.transfer_to(specialist_agent)
```

## 参考资料

- 文档：https://docs.livekit.io/agents/
- 示例代码：https://github.com/livekit/agents/tree/main/examples
- 实验平台：https://agents-playground.livekit.io