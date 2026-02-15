---
name: minimax-tts
description: 管理 MiniMax Speech 2.8 的文本转语音（T2A）功能以及语音目录的查询操作。当您需要获取特定的 MiniMax 语音 ID、发起 Speech 2.8 的文本转语音（TTS）请求，或列出所有可用的 MiniMax 系统生成的语音时，可以使用这些功能。
---

# MiniMax Speech 2.8 辅助工具

1. **安装依赖项。** 在执行脚本的环境中运行 `pip install requests`。该 CLI 需要与 MiniMax 的 REST API 进行通信，因此除了 Python 3.11+ 之外，还需要 `requests` 库。
2. **设置您的 MiniMax 认证信息。** 将 `MINIMAX_API_KEY` 设置为用户提供的 API 密钥。如果没有这个密钥，脚本将无法运行。
3. **使用内置的 CLI。** `scripts/minimax_tts.py` 提供了两个子命令：
   - `tts`：发送 `POST` 请求到 `https://api.minimax.io/v1/t2a_v2`（Speech 2.8 的 T2A API），传入所需的语音 ID（voice_id）、语音设置、音频配置以及可选的语音效果。示例：
     ```bash
     python scripts/minimax_tts.py tts \
       --text "Tonight in Shenzhen the skies are clear." \
       --voice-id "Sweet_Girl_2" \
       --model speech-2.8-hd \
       --audio-format mp3 \
       --output minimax-weather.mp3
     ```
     该脚本会解码传入的十六进制或 Base64 格式的数据，将其保存为文件，并打印元数据。如果需要使用其他端点（如 `https://api-uw.minimax.io/v1/t2a_v2`），可以使用 `--endpoint` 参数进行修改。
   - `voices`：发送 `POST` 请求到 `https://api.minimax.io/v1/get_voice`，以获取系统（system）、语音克隆（voice_cloning）、语音生成（voice_generation）或所有（all）类别的语音信息。示例：
     ```bash
     python scripts/minimax_tts.py voices --voice-type all --print-response
     ```
4. **通过 CLI 参数自定义 TTS 配置。** 使用 `--speed`、`--vol`、`--pitch` 和 `--language-boost` 来调整语音效果。通过 `--sample-rate`、`--bitrate`、`--audio-format` 和 `--channel` 控制音频质量。还可以添加发音自定义选项（如 `--pronunciation "emoji=ee-moh-jee"`）或调整音色（如 `--timbre-weight "Sweet_Girl_2=0.8"`）。`--voice-modify-*` 参数可用于调整音高、音量或音色，或者添加音效（例如 `"spacious_echo"`）。`--output-format` 参数用于指定 API 返回音频的格式（`hex`、`base64` 或下载链接）。
5. **处理 JSON 数据。** 默认情况下，脚本会输出 `extra_info` 字段，以便您可以查看比特率、采样率和音频长度。在任一子命令中添加 `--print-response` 选项可以输出完整的 API 响应内容以方便调试。如果需要将语音信息保存到磁盘，可以使用 `--output <path>` 参数。

每当需要使用 MiniMax 的特定语音或精确的语音设置时，请确保该辅助工具已加载。该 CLI 允许您对语音 ID、模型和音频质量进行精确控制，从而确保始终获得预期的音效（例如 `Sweet_Girl_2`）。如果需要从其他工具中自动化执行这些请求，可以直接复制 `scripts/minimax_tts.py` 中的 `requests.post` 逻辑。