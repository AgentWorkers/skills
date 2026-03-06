---
name: whisper-tailnet-api
description: 通过 Tailnet 在 http://100.92.116.99:8765 上使用 OpenAI 兼容的音频转录端点 (/v1/audio/transcriptions) 来调用共享的 Whisper 语音转文本 API。当代理需要远程转录服务、请求示例、语言提示、时间测试或故障排除响应/输出时，可以使用该 API。
---
# 通过 Tailnet 使用 Whisper STT API（兼容 OpenAI）

请参考本指南来调用共享的 Whisper 服务器。

## 端点

- **基础 URL：** `http://100.92.116.99:8765`
- **健康检查：** `GET /health`
- **转录音频：** `POST /v1/audio/transcriptions` （发送原始二进制音频数据）

## 快速健康检查

```bash
curl -sS http://100.92.116.99:8765/health
```

## 转录音频（推荐使用）

```bash
curl -sS -X POST \
  --data-binary @/path/to/audio.wav \
  "http://100.92.116.99:8765/v1/audio/transcriptions?ext=.wav"
```

## 记录请求时间

```bash
time curl -sS -X POST \
  --data-binary @/path/to/audio.wav \
  "http://100.92.116.99:8765/v1/audio/transcriptions?ext=.wav"
```

## 注意事项

- 建议优先使用此兼容 OpenAI 的接口，而非该服务器上的 `/transcribe` 接口。
- 通过 `ext` 查询参数指定文件类型（例如：`.wav`、`.mp3`、`.m4a`）。
- 如果知道音频语言，请使用 `language` 查询参数以提高转录准确性。

## 预期响应格式

```json
{
  "text": "transcribed text...",
  "model": "turbo"
}
```