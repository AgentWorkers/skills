---
name: phone-agent
description: "使用 Twilio、Deepgram 和 ElevenLabs 运行一个实时 AI 电话代理。该代理可以处理来电，转录音频内容，通过大型语言模型（LLM）生成响应，并通过流式文本转语音（TTS）技术将生成的回答播报出来。适用于以下场景：  
(1) 测试语音 AI 的功能；  
(2) 以编程方式处理电话呼叫；  
(3) 构建对话式语音机器人。"
---

# 电话代理技能

该技能运行一个本地的 FastAPI 服务器，作为实时语音桥梁。

## 架构

```
Twilio (Phone) <--> WebSocket (Audio) <--> [Local Server] <--> Deepgram (STT)
                                                  |
                                                  +--> OpenAI (LLM)
                                                  +--> ElevenLabs (TTS)
```

## 先决条件

1. **Twilio 账户**：电话号码 + TwiML 应用程序。
2. **Deepgram API 密钥**：用于快速的语音转文本功能。
3. **OpenAI API 密钥**：用于对话逻辑处理。
4. **ElevenLabs API 密钥**：用于实现逼真的文本转语音功能。
5. **Ngrok**（或类似工具）：用于将本地的 8080 端口暴露给 Twilio。

## 设置步骤

1. **安装依赖项**：
    ```bash
    pip install -r scripts/requirements.txt
    ```

2. **设置环境变量**（在 `~/.moltbot/.env`、`~/.clawdbot/.env` 中设置，或通过 `export` 命令设置）：
    ```bash
    export DEEPGRAM_API_KEY="your_key"
    export OPENAI_API_KEY="your_key"
    export ELEVENLABS_API_KEY="your_key"
    export TWILIO_ACCOUNT_SID="your_sid"
    export TWILIO_AUTH_TOKEN="your_token"
    export PORT=8080
    ```

3. **启动服务器**：
    ```bash
    python3 scripts/server.py
    ```

4. **将服务器暴露到互联网**：
    ```bash
    ngrok http 8080
    ```

5. **配置 Twilio**：
    - 进入您的电话号码设置。
    - 在“语音与传真”选项中，将“来电处理”方式设置为 **Webhook**。
    - URL：`https://<your-ngrok-url>.ngrok.io/incoming`
    - 方法：`POST`

## 使用方法

拨打您的 Twilio 号码。代理会接听电话，将您的语音内容转录后，经过处理后以自然的语音回复您。

## 自定义设置

- **系统提示语**：编辑 `scripts/server.py` 文件中的 `SYSTEM_PROMPT` 以更改对话角色的提示语。
- **语音**：更改 `ELEVENLABS_VOICE_ID` 以使用不同的语音效果。
- **模型**：将 `gpt-4o-mini` 更改为 `gpt-4`，以获得更智能（但响应速度较慢）的回复效果。