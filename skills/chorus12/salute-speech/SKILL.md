---
name: salute-speech
description: 使用 Sber Salute Speech 的异步 API 来转录音频文件。该 API 支持俄语（ru-RU）、英语（en-US）、哈萨克语（kk-KZ）和吉尔吉斯语（ky-KG）的语音转文本（STT）功能，优先处理俄语语音。
metadata: { "openclaw": { "requires": { "bins": ["uv"], "env": ["SALUTE_AUTH_DATA"] }, "primaryEnv": "SALUTE_AUTH_DATA" } }
---
# 使用 Sber Salute Speech 进行音频转录

通过 Sber Salute Speech 的异步 REST API，将音频/视频文件转录为带有时间戳的文本。

## 要求

- **API 密钥**：必须设置环境变量 `SALUTE_AUTH_DATA`（格式为 Base64 编码的 `client_id:client_secret`，或从 https://developers.sber.ru/studio/ 获取的原始授权密钥）。
- **SSL 说明**：由于 Sber 的证书链不符合标准，脚本默认禁用了 SSL 验证（`verify_ssl=False`）。这是预期的行为。

## 支持的格式与编码

| 音频编码 | 内容类型 | 常见扩展名 |
|---------------|-------------|--------------------|
| `MP3` | `audio/mpeg` | `.mp3` |
| `PCM_S16LE` | `audio/wav` | `.wav` |
| `OPUS` | `audio/ogg` | `.ogg`, `.opus` |
| `FLAC` | `audio/flac` | `.flac` |
| `ALAW` | `audio/alaw` | `.alaw` |
| `MULAW` | `audio/mulaw` | `.mulaw` |

## 支持的语言

`ru-RU`（俄语）、`en-US`（英语）、`kk-KZ`（哈萨克语）、`ky-KG`（吉尔吉斯语）、`uz-UZ`（乌兹别克语）。

## 工作流程

1. **识别输入文件** — 根据用户请求确定文件。
2. **读取 API 密钥** — 从主机环境中获取 API 密钥。
3. **执行转录** — 运行 `salute_transcribe.py` 并传递必要的参数。
4. **提供结果** — 将带有时间戳的转录文本呈现给用户，并提供文件的直接链接。

## 使用方法

```bash
uv run --with requests {baseDir}/salute_transcribe.py \
  --file /path/to/audio.mp3 \
  --output_dir ~/.openclaw/workspace/transcriptions \
  --lang ru-RU
```

### 参数

| 参数 | 是否必填 | 默认值 | 说明 |
|----------|----------|---------|-------------|
| `--file` | 是 | — | 音频/视频文件的路径 |
| `--output_dir` | 否 | `~/.openclaw/workspace/transcribations` | 结果的输出目录 |
| `--lang` | 否 | `ru-RU` | 语言代码：`ru-RU`、`en-US`、`kk-KZ`、`ky-KG`、`uz-UZ` |
| `--audio-encoding` | 否 | `MP3` | 编码格式：`MP3`、`PCM_S16LE`、`OPUS`、`FLAC`、`ALAW`、`MULAW` |
| `--model` | 否 | `general` | 识别模型：`general` 或 `callcenter` |
| `--hyp-count` | 否 | `1` | 替代假设的数量：`1` 或 `2` |
| `--max-wait-time` | 否 | `300` | 等待异步结果的最大时间（秒） |
| `--print` | 否 | 关闭 | 同时将转录结果输出到标准输出（stdout） |

### 内容类型映射

如果文件扩展名与 `audio/mpeg` 不匹配，请在脚本中调整 `content_type` 或添加相应的逻辑。当前默认值为 `audio/mpeg`（MP3）。对于 `.wav` 文件，应使用 `audio/wav` 等格式。

## 输出文件

对于输入文件 `meetingABC.mp3`，脚本会生成以下文件：

| 文件 | 说明 |
|------|-------------|
| `meetingABC_recognition_orig.json` | 原始 API 响应（包含所有假设、时间戳和置信度的完整 JSON 数据） |
| `meetingABC_pretty.txt` | 带有时间戳的格式化后的可读文本 |

## 输出文本格式

```
[00:01 - 00:20]:
Ну, даже если сосредоточиться на идее узкой щели.

[00:20 - 00:45]:
Следующий фрагмент текста здесь.
```

## 注意事项

- 令牌的有效期为约 30 分钟；脚本每次运行时会重新获取新的令牌。
- 大文件（超过 1 小时）可能需要将 `--max-wait-time` 增加到超过 300 秒。
- `callcenter` 模型针对电话音频（8kHz、单声道）进行了优化。
- 粗话过滤功能默认是关闭的（`enable_profanity_filter=False`）。
- 脚本默认使用**标准化文本**（数字以数字形式显示，缩写会展开显示）。原始文本也包含在 JSON 输出中。