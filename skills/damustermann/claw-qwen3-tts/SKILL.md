---
name: qwen3-tts
description: >
  使用 Qwen3-TTS 实现高质量的语音合成服务：  
  - 内置 10 种语音合成引擎，支持情感控制功能；  
  - 支持语音克隆（可生成长达 3 秒的语音片段）；  
  - 提供自然语言风格的语音设计选项；  
  - 支持 10 多种语言；  
  - 支持为语音设置自定义名称；  
  - 可通过 Telegram/WhatsApp 以原生语音消息的形式发送音频文件；  
  - 能自动检测并适配不同的 GPU 硬件（CUDA、ROCm、Intel XPU、CPU）。
version: "1.0"
author: daMustermann
repository: https://github.com/daMustermann/claw-qwen3-tts
license: MIT
requires:
  - python>=3.10
  - ffmpeg
  - sox
  - git
tags:
  - tts
  - audio
  - voice
  - speech
  - voice-cloning
  - voice-design
  - telegram
  - whatsapp
  - clawhub
---
# Qwen3-TTS 技能

您可以使用这个强大的文本转语音（TTS）系统，该系统支持 10 种内置语音，能够生成高质量的语音；可以根据描述创建新语音；可以从音频样本克隆现有语音；并通过 Telegram/WhatsApp 以原生语音消息的形式发送音频。

## 首次设置

如果该技能尚未安装（`~/clawd/skills/qwen3-tts` 目录不存在），请运行以下命令：

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/daMustermann/claw-qwen3-tts/main/install.sh)
```

或者，如果已经克隆了该技能但尚未进行设置（`.venv/` 目录不存在），请运行以下命令：

```bash
bash ~/clawd/skills/qwen3-tts/install.sh
```

此命令会自动检测您的 GPU（CUDA、ROCm、Intel XPU 或仅支持 CPU 的系统），创建一个 Python 虚拟环境（venv），并安装所有依赖项。首次运行可能需要 5–15 分钟。

## 启动和停止服务器

在进行任何 TTS 操作之前，请确保服务器正在运行：

```bash
# Start (idempotent — won't restart if already running)
bash ~/clawd/skills/qwen3-tts/scripts/start_server.sh

# Check health
bash ~/clawd/skills/qwen3-tts/scripts/health_check.sh

# Stop (when done)
bash ~/clawd/skills/qwen3-tts/scripts/stop_server.sh
```

服务器的运行地址为 `http://localhost:8880`。

---

## 可用的模型

| 模型 ID | 使用场景 | 备注 |
|----------|----------|-------|
| `custom-voice-1.7b` | 高质量的 TTS，支持内置语音 — **默认** | 最佳音质，需要约 5 GB 的显存（VRAM） |
| `custom-voice-0.6b` | 快速的 TTS，支持内置语音 | 体积较小，需要约 2 GB 的显存 |
| `voice-design` | 根据自然语言描述创建新语音 | 使用 VoiceDesign 模型 |
| `base-1.7b` | 基本的 TTS（会自动转换为 `custom-voice-1.7b`） | 请使用 `custom-voice-*` 代替 |
| `base-0.6b` | 基本的 TTS（会自动转换为 `custom-voice-0.6b`） | 请使用 `custom-voice-*` 代替 |

> **重要提示：** 在 `/v1/audio/speech` 端点上，`base-*` 和 `voice-design` 模型会自动转换为相应的 `custom-voice-*` 模型。建议始终使用 `custom-voice-1.7b` 或 `custom-voice-0.6b` 进行语音生成。

## 内置语音

`custom-voice-*` 模型包含 10 种内置语音：

> **Chelsie** · **Ethan** · **Aidan** · **Serena** · **Ryan** · **Vivian** · **Claire** · **Lucas** · **Eleanor** · **Benjamin**

您可以通过以下命令动态查看所有可用的语音：`curl http://localhost:8880/v1/speakers`

---

## 功能

### 1. 从文本生成语音

**使用场景：** 用户要求将文本读出来、生成音频、进行旁白或进行叙述等。

**参数：**

| 参数 | 是否必填 | 默认值 | 说明 |
|-----------|----------|---------|-------------|
| `model` | 否 | `custom-voice-1.7b` | 要使用的 TTS 模型 |
| `input` | 是 | — | 需要合成的文本 |
| `voice` | 否 | `default` | 内置语音的名称（例如 `"Angie"`） |
| `speaker` | 否 | `Chelsie` | 当 `voice` 为 `"default"` 时的内置语音名称 |
| `language` | 否 | `en` | 语言代码：en, zh, ja, ko, de, fr, ru, pt, es, it |
| `instruct` | 否 | `""` | 情感/风格指令（见下文） |
| `response_format` | 否 | `wav` | 输出格式：wav, mp3, ogg, flac |
| `speed` | 否 | `1.0` | 语音速度倍数 |

**语言代码：** `en`, `zh`, `ja`, `ko`, `de`, `fr`, `ru`, `pt`, `es`, `it` — 或全称（如 `English`, `Chinese`, `German` 等）。

**情感/风格指令示例：**
- `"用快乐而兴奋的语气说话"`
- `"像低声诉说秘密一样轻声说"`
- `"以冷静、专业的新闻播音员的语气朗读"`
- `"用愤怒的语气说"`（也会以目标语言生成）
- `""`（空字符串表示中性默认值）

**当 `voice` 是保存的名称时：** 如果您传递 `"voice": "Angie"` 且存在名为 "Angie" 的语音，系统会使用保存的音频进行克隆，而不会使用内置语音。在这种情况下，`speaker` 字段将被忽略。**

### 2. 创建新语音

**使用场景：** 用户希望创建自定义语音，描述角色的声音特征。

**参数：**

| 参数 | 是否必填 | 默认值 | 说明 |
|-----------|----------|---------|-------------|
| `model` | 否 | `voice-design` | 必须设置为 `voice-design` |
| `input` | 是 | — | 需要使用该语音合成的文本 |
| `voice_description` | 是 | — | 对所需语音的自然语言描述 |
| `language` | 否 | `en` | 目标语言 |
| `response_format` | 否 | `wav` | 输出格式 |

**示例描述：**
- `"一个温暖、低沉的男性声音，带有轻微的英式口音，冷静而权威，像 40 多岁的 BBC 播音员"`
- `"一个年轻、充满活力的女性声音，明亮而欢快，带有轻微的沙哑感"`
- `"一个声音缓慢、神秘的老巫师的声音"`

响应中会包含一个 `X-Voice-Id` 标头——请保存该 ID 以保存新创建的语音（详见 §4）。

### 3. 克隆语音

**使用场景：** 用户提供参考音频片段，并希望用该语音生成新的语音。

**参数：**

| 参数 | 是否必填 | 默认值 | 说明 |
|-----------|----------|---------|-------------|
| `reference_audio` | 是 | — | 用于克隆语音的音频文件 |
| `input` | 是 | — | 使用该语音合成的新文本 |
| `reference_text` | 否 | `""` | 参考音频的文字记录（可提高质量） |
| `language` | 否 | `en` | 目标语言 |
| `response_format` | 否 | `wav` | 输出格式 |

**注意事项：**
- 参考音频长度至少为 3 秒
- 建议长度为 10–30 秒以获得最佳效果
- 提供准确的 `reference_text` 文本记录可以显著提高克隆效果
- 支持跨语言克隆（例如从英语克隆到日语）
- 如果 `reference_text` 为空，系统将仅使用音频特征进行克隆

响应中会包含一个 `X-Voice-Id` 标头——请保存该 ID 以保存新创建的语音（详见 §4）。

### 4. ⭐ 重要规则：语音保存提示

**您必须遵守以下规则：**

1. **在每次使用 `voice-design` 或 `voice-clone` 功能后**，请询问用户：
   > “您是否希望保存这个语音以供将来使用？应该给它起什么名字？”

2. **如果用户同意保存**，请从响应头中获取 `X-Voice-Id` 并保存它：
   ```bash
   curl -X POST http://localhost:8880/v1/voices \
     -H "Content-Type: application/json" \
     -d '{
       "name": "USER_CHOSEN_NAME",
       "source_voice_id": "VOICE_ID_FROM_X_VOICE_ID_HEADER",
       "description": "Description of the voice",
       "tags": ["tag1", "tag2"],
       "language": "en"
     }'
   ```

3. **当用户要求使用特定名称的语音进行 TTS 时**（例如：“用 Angie 的声音说这句话”）：
   - 在 `/v1/audio/speech` 请求中使用 `"voice": "Angie"` 
   - 系统会自动加载保存的参考音频并使用克隆功能
   - 如果名称不存在，应告知用户并提供创建或克隆新语音的服务

4. **当用户请求查看所有可用语音时**：
   ```bash
   curl http://localhost:8880/v1/voices
   ```
   以格式化列表的形式展示语音信息，包括名称、描述、来源、语言、标签和使用次数。语音按使用次数排序（使用次数最多的排在最前面）。

5. **当用户请求删除语音时**：先确认用户的意愿，然后执行删除操作：
   ```bash
   curl -X DELETE http://localhost:8880/v1/voices/VOICE_NAME
   ```

6. **当用户请求更改语音名称时**：
   ```bash
   curl -X PATCH http://localhost:8880/v1/voices/OLD_NAME \
     -H "Content-Type: application/json" \
     -d '{"name": "NEW_NAME"}'
   ```

7. **当用户请求更新语音的元数据（描述、标签、语言）时**：
   ```bash
   curl -X PATCH http://localhost:8880/v1/voices/VOICE_NAME \
     -H "Content-Type: application/json" \
     -d '{"description": "Updated description", "tags": ["new", "tags"]}'
   ```

8. **语音名称不区分大小写**，但会按照用户提供的大小写进行存储。
   - 如果名称已经存在，保存操作将会失败（返回 409 错误）。请用户提供另一个名称或选择删除现有语音。

9. **语音文件存储在本地目录 `~/clawd/skills/qwen3-tts/voices/` 中**，并在服务器重启后保持不变。每个语音文件包含以下文件：
    - `<name>.json` — 元数据
    - `<name>.pt` — 嵌入张量
    - `<name>_sample.wav` — 参考音频样本（用于克隆）

### 5. 转换音频格式

**使用场景：** 用户需要特定格式的音频，或者您需要将音频格式转换为适合发送的形式。

**支持的格式：** `wav`, `mp3`, `ogg` (Opus), `flac`

您也可以直接使用 shell 脚本进行转换：
```bash
bash ~/clawd/skills/qwen3-tts/scripts/convert_to_ogg_opus.sh input.wav output.ogg
```

### 6. 通过 Telegram 发送语音消息

**使用场景：** 用户通过 Telegram 进行交互，或明确要求通过 Telegram 发送音频。

**操作步骤：**
- `bot_token` 如果已在 `config.json` 中配置，则可选
- 音频会自动转换为 OGG/Opus 格式，并通过 Telegram 的 `sendVoice` API 发送
- 在聊天中显示为原生的语音消息

### 7. 通过 WhatsApp 发送语音消息

**使用场景：** 用户通过 WhatsApp 进行交互，或明确要求通过 WhatsApp 发送音频。

**操作步骤：**
- `phone_number_id` 和 `access_token` 如果已在 `config.json` 中配置，则可选
- 音频会自动转换为 OGG/Opus 格式，并通过 WhatsApp 的 `sendVoice` 功能发送

### 8. 发现可用模型和语音的端点

使用以下端点动态获取可用的模型和语音信息：

```bash
# List all available TTS models
curl http://localhost:8880/v1/models

# List built-in speakers
curl http://localhost:8880/v1/speakers

# Server health check (device info, voice count, version)
curl http://localhost:8880/health
```

---

## 响应用户请求的步骤

**生成语音后：**
1. 告知用户语音已生成
2. 提供输出文件的路径
3. 如果是使用 `voice-design` 或 `voice-clone` 功能，**务必询问用户是否希望保存该语音**（遵循规则 §4.1）
4. 如果用户使用 Telegram/WhatsApp，建议将语音文件作为语音消息发送

**保存语音后：**
- 确认语音名称，并告知用户可以随时使用该名称
- 例如：“语音已保存为‘Captain Hook’！您可以通过 `voice: Captain Hook` 来调用它。”

**通过 Telegram/WhatsApp 发送音频后：**
- 确认音频已成功发送

**选择语音时：** 如果用户未指定语音，系统默认使用 `"Chelsie"`；如果用户描述了所需的语音特征（但未进行完整的自定义语音设计），系统会选择最合适的内置语音。
**选择模型时：** 默认使用 `custom-voice-1.7b`；如果用户要求加快语音速度或系统显存不足，可以使用 `custom-voice-0.6b`。

---

## 配置

您可以通过更新 `~/clawd/skills/qwen3-tts/config.json` 文件来设置以下参数：
- **Telegram：** bot token 和默认聊天 ID
- **WhatsApp：** phone number ID 和 access token
- **默认模型：** `custom-voice-1.7b` 或 `custom-voice-0.6b`
- **默认音频格式：** wav, mp3, ogg, flac
- **设备优先级：** auto, cuda:0, xpu:0, cpu

如果 `config.json` 文件不存在，可以使用以下模板进行配置：
```bash
cp ~/clawd/skills/qwen3-tts/config.json.template ~/clawd/skills/qwen3-tts/config.json
```