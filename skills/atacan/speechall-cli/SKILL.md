---
name: speechall-cli
description: "安装并使用 `speechall` CLI 工具进行语音转文本的转录。该工具适用于以下场景：  
1. 将音频或视频文件转录为文本；  
2. 在 macOS 或 Linux 系统上安装 `speechall`；  
3. 查看可用的语音转文本（STT）模型及其功能；  
4. 通过终端使用语音识别功能、字幕生成或其他转录功能。  

该工具会在命令行中检测到与 `speechall`、`audio transcription CLI` 或 `speech-to-text` 相关的指令时自动执行相应操作。"
---

# speechall-cli

这是一个用于通过 Speechall API 将语音转换为文本的命令行工具（CLI）。支持多种语音转文本服务提供商（OpenAI、Deepgram、AssemblyAI、Google、Gemini、Groq、ElevenLabs、Cloudflare 等）。

## 安装

### Homebrew（macOS 和 Linux）

```bash
brew install Speechall/tap/speechall
```

**不使用 Homebrew 的情况**：从 [https://github.com/Speechall/speechall-cli/releases](https://github.com/Speechall/speechall-cli/releases) 下载适用于您平台的二进制文件，并将其添加到您的 `PATH` 环境变量中。

### 验证安装

```bash
speechall --version
```

## 认证

需要一个 API 密钥。可以通过环境变量（推荐）或命令行参数来提供该密钥：

```bash
export SPEECHALL_API_KEY="your-key-here"
# or
speechall --api-key "your-key-here" audio.wav
```

用户可以在 [https://speechall.com/console/api-keys](https://speechall.com/console/api-keys) 上创建 API 密钥。

## 命令

### transcribe（默认命令）

用于将音频或视频文件转换为文本。这是默认的子命令，例如：`speechall audio.wav` 等同于 `speechall transcribe audio.wav`。

```bash
speechall <file> [options]
```

**选项：**

| 参数 | 描述 | 默认值 |
| --- | --- | --- |
| `--model <provider.model>` | 语音转文本模型标识符 | `openai.gpt-4o-mini-transcribe` |
| `--language <code>` | 语言代码（例如 `en`、`tr`、`de`） | 由 API 自动检测 |
| `--output-format <format>` | 输出格式（`text`、`json`、`verbose_json`、`srt`、`vtt`） | 由 API 自动检测 |
| `--diarization` | 是否启用说话者标注功能 | 关闭（默认） |
| `--speakers-expected <n>` | 预期的说话者数量（与 `--diarization` 一起使用） | — |
| `--no-punctuation` | 禁用自动添加标点符号 | — |
| `--temperature <0.0-1.0>` | 模型的“温度”参数（影响生成结果的质量） | — |
| `--initial-prompt <text>` | 用于引导模型生成的文本提示 | — |
| `--custom-vocabulary <term>` | 用于提高识别准确性的自定义词汇 | — |
| `--ruleset-id <uuid>` | 替换规则集的 UUID | — |
| `--api-key <key>` | API 密钥（覆盖 `SPEECHALL_API_KEY` 环境变量） | — |

**示例：**

```bash
# Basic transcription
speechall interview.mp3

# Specific model and language
speechall call.wav --model deepgram.nova-2 --language en

# Speaker diarization with SRT output
speechall meeting.wav --diarization --speakers-expected 3 --output-format srt

# Custom vocabulary for domain-specific terms
speechall medical.wav --custom-vocabulary "myocardial" --custom-vocabulary "infarction"

# Transcribe a video file (macOS extracts audio automatically)
speechall presentation.mp4
```

### models

列出所有可用的语音转文本模型。输出结果为 JSON 格式到标准输出（stdout）。

```bash
speechall models [options]
```

**过滤参数：**

| 参数 | 描述 |
| --- | --- |
| `--provider <name>` | 按提供商过滤（例如 `openai`、`deepgram`） |
| `--language <code>` | 按支持的语言过滤（例如 `tr` 表示土耳其语） |
| `--diarization` | 仅显示支持说话者标注功能的模型 | — |
| `--srt` | 仅显示支持 SRT 格式输出的模型 | — |
| `--vtt` | 仅显示支持 VTT 格式输出的模型 | — |
| `--punctuation` | 仅显示支持自动添加标点符号的模型 | — |
| `--streamable` | 仅显示支持实时流处理的模型 | — |
| `--vocabulary` | 仅显示支持自定义词汇的模型 | — |

**示例：**

```bash
# List all available models
speechall models

# Models from a specific provider
speechall models --provider deepgram

# Models that support Turkish and diarization
speechall models --language tr --diarization

# Pipe to jq for specific fields
speechall models --provider openai | jq '.[].identifier'
```

## 提示：

- 在 macOS 上，视频文件（如 `.mp4`、`.mov` 等）在上传前会自动转换为音频格式。
- 在 Linux 上，可以直接传递音频文件（如 `.wav`、`.mp3`、`.m4a`、`.flac` 等）。
- 输出结果会显示在标准输出（stdout）中。若需保存结果，可以使用 `speechall audio.wav > transcript.txt`。
- 错误信息会显示在标准错误输出（stderr）中，因此直接将标准输出重定向到文件是安全的。
- 运行 `speechall --help`、`speechall transcribe --help` 或 `speechall models --help` 可以查看所有有效的模型标识符、语言代码和输出格式的选项。