---
name: slybroadcast-voicemail
description: 使用 OpenClaw 或 LLM（大型语言模型），通过 CLI（命令行接口）或 MCP（管理控制面板）发送无铃声的语音邮件（voicemail）营销活动。这些活动支持 AI 语音生成（如 ElevenLabs 或通用的 HTTP 语音 API），并且具备完善的营销活动控制功能。
---
# Slybroadcast 语音邮件服务

当用户需要使用 Slybroadcast 发送一条或多条语音邮件，并且可以选择将文本转换为语音录音时，可以使用此功能。

## 前提条件

所需的环境变量：

- `SLYBROADCAST_UID`（或备用选项 `SLYBROADCAST_EMAIL`）
- `SLYBROADCAST_PASSWORD`
- `SLYBROADCAST_DEFAULT_CALLER_ID`（或明确指定呼叫者 ID）

对于本地文件或 AI 生成的语音文件，还需设置以下变量：

- `SLYBROADCAST_PUBLIC_AUDIO_BASE_URL`
- `SLYBROADCAST_AUDIO_STAGING_DIR`

若使用 ElevenLabs 的语音生成服务，还需设置：

- `ELEVENLABS_API_KEY`
- `ELEVENLABS_TTS_VOICE_ID`

## 命令行接口（CLI）命令

可以直接运行以下命令：

```bash
npm --workspace @fub/slybroadcast-voicemail run dev:cli -- send --help
```

**常见示例：**

1. 使用现有账户的录音作为语音邮件内容：
```bash
npm --workspace @fub/slybroadcast-voicemail run dev:cli -- send \
  --to "16173999981,16173999982" \
  --record-audio "My First Voice Message" \
  --caller-id "16173999980" \
  --campaign-name "Follow-up" \
  --schedule-at "now"
```

2. 使用公共音频文件作为语音邮件内容：
```bash
npm --workspace @fub/slybroadcast-voicemail run dev:cli -- send \
  --to "16173999981" \
  --audio-url "https://example.com/voicemail.mp3" \
  --audio-type mp3 \
  --caller-id "16173999980"
```

3. 使用 ElevenLabs 的文本转语音服务并发送语音邮件：
```bash
npm --workspace @fub/slybroadcast-voicemail run dev:cli -- send \
  --to "16173999981" \
  --ai-text "Hi, this is your appointment reminder for tomorrow at 3 PM." \
  --ai-provider elevenlabs \
  --caller-id "16173999980"
```

4. 从 Slybroadcast 平台上传语音邮件文件列表：
```bash
npm --workspace @fub/slybroadcast-voicemail run dev:cli -- send \
  --list-id 94454 \
  --record-audio "My First Voice Message" \
  --caller-id "16173999980"
```

## MCP 工具

启动 MCP 服务器：

```bash
npm --workspace @fub/slybroadcast-voicemail run dev:mcp
```

**可用的工具：**

- `slybroadcast_voicemail_send`
- `slybroadcast_audio_list`
- `slybroadcast_phone_list`
- `slybroadcast_campaign_status`
- `slybroadcast_campaign_results`
- `slybroadcast_campaign_control`
- `slybroadcast_voice_generate`

## 注意事项：

- Slybroadcast 的 API 响应时间以东部时间（Eastern Time）计算，采用 24 小时格式（`YYYY-MM-DD HH:MM:SS`）。
- 每次请求只能使用一种音频来源：账户录音、系统生成的音频文件、公共音频 URL、本地文件或 AI 生成的文本。
- 本地文件和 AI 生成的语音文件需要先被存储到指定的临时目录（`SLYBROADCAST_AUDIO_STAGING_DIR`），并且必须能够被 Slybroadcast 访问到才能使用。