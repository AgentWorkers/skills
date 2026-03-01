---
name: step-asr
description: 通过 Step ASR 流媒体 API（HTTP SSE）将音频文件转录为文本。支持中文和英文，支持多种音频格式（PCM、WAV、MP3、OGG/OPUS），提供实时流式输出功能，并支持术语更正提示。
version: 1.0.0
metadata:
  openclaw:
    emoji: "\U0001F399"
    requires:
      bins:
        - python3
      env:
        - STEPFUN_API_KEY
    primaryEnv: STEPFUN_API_KEY
    homepage: https://platform.stepfun.com/docs/zh/api-reference/audio/asr-stream
---
# Step ASR - 流式语音转文本

使用 Step (StepFun) 的 ASR API 通过 HTTP SSE 流式传输来转录音频文件。

## 快速入门

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.wav
```

## 使用示例

- 基本转录（中文，流式输出）：

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.wav
```

- 指定语言并保存到文件：

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.mp3 --language en --out /tmp/transcript.txt
```

- 使用提示语进行术语校正：

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.pcm --prompt "Related terms: OpenClaw, StepFun, ASR"
```

- 以 JSON 格式输出（包含使用统计信息）：

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.ogg --json
```

- 非流式模式（仅打印最终结果）：

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/audio.wav --no-stream
```

- 明确指定音频格式（针对没有扩展名的原始 PCM 文件）：

```bash
python3 {baseDir}/scripts/transcribe.py /path/to/raw_audio --format-type pcm --sample-rate 16000
```

## 支持的音频格式

| 格式 | 扩展名 | 备注 |
|--------|-----------|-------|
| PCM    | `.pcm`, `.raw` | 原始 PCM 格式，默认编码为 `pcm_s16le` |
| WAV    | `.wav`    | WAV 容器格式 |
| MP3    | `.mp3`    | |
| OGG/OPUS | `.ogg`, `.opus` | |

## 所有选项

| 标志 | 默认值 | 说明 |
|------|---------|-------------|
| `--language` | `zh` | 语言代码（`zh` 或 `en`） |
| `--model` | `step-asr` | ASR 模型名称 |
| `--out` | *(stdout)* | 将转录结果保存到文件 |
| `--prompt` | *(none)* | 用于提高特定领域术语准确性的提示文本 |
| `--format-type` | *(auto)* | 音频格式：`pcm`, `mp3`, `ogg`（根据扩展名自动检测） |
| `--sample-rate` | `16000` | 音频采样率（单位：Hz） |
| `--no-stream` | `false` | 仅打印最终完整结果 |
| `--json` | `false` | 以 JSON 格式输出并包含使用统计信息 |
| `--no-itn` | `false` | 禁用逆向文本规范化 |
| `--no-rerun` | `false` | 禁用二次错误校正 |

## API 密钥

设置 `STEPFUN_API_KEY` 环境变量，或在 `~/.openclaw/openclaw.json` 中进行配置：

```json5
{
  skills: {
    "step-asr": {
      apiKey: "YOUR_STEPFUN_API_KEY"
    }
  }
}
```

请从 [Step Platform](https://platform.stepfun.com/) 获取您的 API 密钥。