---
name: openai-tts
description: 通过 OpenAI 的 Audio Speech API 实现文本转语音功能。
homepage: https://platform.openai.com/docs/guides/text-to-speech
metadata: {"clawdbot":{"emoji":"🔊","requires":{"bins":["curl"],"env":["OPENAI_API_KEY"]},"primaryEnv":"OPENAI_API_KEY"}}
---

# OpenAI TTS（使用curl）

通过OpenAI的 `/v1/audio/speech` 端点将文本转换为语音。

## 快速入门

```bash
{baseDir}/scripts/speak.sh "Hello, world!"
{baseDir}/scripts/speak.sh "Hello, world!" --out /tmp/hello.mp3
```

默认参数：
- 模型：`tts-1`（快速）或 `tts-1-hd`（高质量）
- 语音：`alloy`（中性），其他可选语音：`echo`、`fable`、`onyx`、`nova`、`shimmer`
- 格式：`mp3`

## 可用语音

| 语音 | 描述 |
|-------|-------------|
| alloy | 中性、平衡的语音 |
| echo | 男性、温暖的语音 |
| fable | 英国口音、富有表现力 |
| onyx | 深沉、权威的语音 |
| nova | 女性、友好的语音 |
| shimmer | 女性、柔和的语音 |

## 命令行参数

```bash
{baseDir}/scripts/speak.sh "Text" --voice nova --model tts-1-hd --out speech.mp3
{baseDir}/scripts/speak.sh "Text" --format opus --speed 1.2
```

可选参数：
- `--voice <名称>`：alloy|echo|fable|onyx|nova|shimmer （默认：alloy）
- `--model <名称>`：tts-1|tts-1-hd （默认：tts-1）
- `--format <格式>`：mp3|opus|aac|flac|wav|pcm （默认：mp3）
- `--speed <速度>`：0.25-4.0 （默认：1.0）
- `--out <输出路径>`：输出文件（默认：标准输出或自动生成的文件名）

## API密钥

请设置 `OPENAI_API_KEY`，或在其配置文件 `~/.clawdbot/clawdbot.json` 中进行配置：

```json5
{
  skills: {
    entries: {
      "openai-tts": {
        apiKey: "sk-..."
      }
    }
  }
}
```

## 价格

- `tts-1`：每1000个字符约0.015美元
- `tts-1-hd`：每1000个字符约0.030美元

非常适合生成简短的语音内容！