---
name: gemini-stt
description: 使用 Google 的 Gemini API 或 Vertex AI 来转录音频文件。
metadata: {"clawdbot":{"emoji":"🎤","os":["linux","darwin"]}}
---

# Gemini 语音转文本技能

使用 Google 的 Gemini API 或 Vertex AI 对音频文件进行转录。默认模型为 `gemini-2.0-flash-lite`，以实现最快的转录速度。

## 认证（请选择一种方式）

### 选项 1：使用应用默认凭据的 Vertex AI（推荐）

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

脚本会自动检测并使用 ADC（如果可用）。

### 选项 2：直接使用 Gemini API 密钥

在环境变量中设置 `GEMINI_API_KEY`（例如：`~/.env` 或 `~/.clawdbot/.env`）。

## 必备条件

- Python 3.10 或更高版本（无需外部依赖库）
- 需要 `GEMINI_API_KEY` 或已配置 ADC 的 gcloud CLI。

## 支持的文件格式

- `.ogg` / `.opus`（Telegram 语音消息）
- `.mp3`
- `.wav`
- `.m4a`

## 使用方法

```bash
# Auto-detect auth (tries ADC first, then GEMINI_API_KEY)
python ~/.claude/skills/gemini-stt/transcribe.py /path/to/audio.ogg

# Force Vertex AI
python ~/.claude/skills/gemini-stt/transcribe.py /path/to/audio.ogg --vertex

# With a specific model
python ~/.claude/skills/gemini-stt/transcribe.py /path/to/audio.ogg --model gemini-2.5-pro

# Vertex AI with specific project and region
python ~/.claude/skills/gemini-stt/transcribe.py /path/to/audio.ogg --vertex --project my-project --region us-central1

# With Clawdbot media
python ~/.claude/skills/gemini-stt/transcribe.py ~/.clawdbot/media/inbound/voice-message.ogg
```

## 参数说明

| 参数 | 说明 |
|--------|-------------|
| `<audio_file>` | 音频文件的路径（必填） |
| `--model`, `-m` | 要使用的 Gemini 模型（默认：`gemini-2.0-flash-lite`） |
| `--vertex`, `-v` | 强制使用带有 ADC 的 Vertex AI |
| `--project`, `-p` | GCP 项目 ID（针对 Vertex，默认使用 gcloud 配置） |
| `--region`, `-r` | GCP 地区（针对 Vertex，默认：`us-central1`） |

## 支持的模型

任何支持音频输入的 Gemini 模型均可使用。推荐模型如下：

| 模型 | 说明 |
|-------|-------|
| `gemini-2.0-flash-lite` | **默认模型**。转录速度最快。 |
| `gemini-2.0-flash` | 转录速度快且成本效益高。 |
| `gemini-2.5-flash-lite` | 轻量级模型。 |
| `gemini-2.5-flash` | 性能与质量平衡。 |
| `gemini-2.5-pro` | 转录质量更高，但速度稍慢。 |
| `gemini-3-flash-preview` | 最新的闪存模型。 |
| `gemini-3-pro-preview` | 最新的专业模型，质量最佳。 |

有关最新模型列表，请参阅 [Gemini API 模型文档](https://ai.google.dev/gemini-api/docs/models)。

## 工作原理

1. 读取音频文件并将其进行 Base64 编码。
2. 自动检测认证方式：
   - 如果 ADC 可用（通过 gcloud），则使用 Vertex AI 服务。
   - 否则，使用 `GEMINI_API_KEY` 直接调用 Gemini API。
3. 将编码后的音频数据发送到选定的 Gemini 模型，并提供转录提示。
4. 返回转录结果。

## 集成示例

用于 Clawdbot 的语音消息处理：

```bash
# Transcribe incoming voice message
TRANSCRIPT=$(python ~/.claude/skills/gemini-stt/transcribe.py "$AUDIO_PATH")
echo "User said: $TRANSCRIPT"
```

## 错误处理

在以下情况下，脚本会以代码 1 退出并将错误信息输出到标准错误流（stderr）：

- 无法进行认证（既没有 ADC 也没有 `GEMINI_API_KEY`）。
- 文件未找到。
- API 使用过程中出现错误。
- 使用 Vertex 时缺少 GCP 项目信息。

## 注意事项

- 默认使用 `gemini-2.0-flash-lite` 模型以实现最快转录速度。
- 无需外部 Python 依赖库（仅使用标准库）。
- 会根据文件扩展名自动检测文件的 MIME 类型。
- 如果 ADC 可用，优先使用 Vertex AI（无需管理 API 密钥）。