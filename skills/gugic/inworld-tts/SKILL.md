---
name: inworld-tts
description: 通过 Inworld.ai API 实现文本转语音功能。适用于将文本转换为语音音频、生成语音回应或将文本转换为 MP3/音频文件。支持多种语音、不同的语速，并且能够流畅地处理长文本。
---

# Inworld TTS

使用 Inworld.ai 的 TTS API 从文本生成语音音频。

## 设置

1. 从 https://platform.inworld.ai 获取 API 密钥。
2. 申请具有 “Voices: Read” 权限的 API 密钥。
3. 复制 “Basic (Base64)” 格式的 API 密钥。
4. 设置环境变量：

```bash
export INWORLD_API_KEY="your-base64-key-here"
```

为确保设置持久生效，请将环境变量添加到 `~/.bashrc` 或 `~/.clawdbot/.env` 文件中。

## 安装

```bash
# Copy skill to your skills directory
cp -r inworld-tts /path/to/your/skills/

# Make script executable
chmod +x /path/to/your/skills/inworld-tts/scripts/tts.sh

# Optional: symlink for global access
ln -sf /path/to/your/skills/inworld-tts/scripts/tts.sh /usr/local/bin/inworld-tts
```

## 使用方法

```bash
# Basic
./scripts/tts.sh "Hello world" output.mp3

# With options
./scripts/tts.sh "Hello world" output.mp3 --voice Dennis --rate 1.2

# Streaming (for text >4000 chars)
./scripts/tts.sh "Very long text..." output.mp3 --stream
```

## 选项

| 选项          | 默认值     | 描述                          |
|----------------|-----------|--------------------------------------------|
| `--voice`       | Dennis     | 语音 ID                          |
| `--rate`       | 1.0       | 说话速度（0.5-2.0）                     |
| `--temp`       | 1.1       | 语调（0.1-2.0）                     |
| `--model`       | inworld-tts-1.5-max | 模型 ID                         |
| `--stream`       | false      | 是否使用流式传输功能                    |

## API 参考

| API 端点        | 使用方法                          |
|----------------|--------------------------------------------|
| `POST https://api.inworld.ai/tts/v1/voice` | 标准语音合成                      |
| `POST https://api.inworld.ai/tts/v1/voice:stream` | 长文本的流式传输                    |

## 所需工具

- `curl`：用于发送 HTTP 请求
- `jq`：用于处理 JSON 数据
- `base64`：用于解码音频文件

## 示例

```bash
# Quick test
export INWORLD_API_KEY="aXM2..."
./scripts/tts.sh "Testing one two three" test.mp3
mpv test.mp3  # or any audio player

# Different voice and speed
./scripts/tts.sh "Slow and steady" slow.mp3 --rate 0.8

# Fast-paced narration
./scripts/tts.sh "Breaking news!" fast.mp3 --rate 1.5
```

## 故障排除

- **“INWORLD_API_KEY 未设置”**：运行程序前请确保已设置环境变量。
- **输出文件为空**：检查 API 密钥是否有效，并且是否具有 “Voices: Read” 权限。
- **流式传输问题**：确认 `jq` 工具支持 `--unbuffered` 标志。

## 链接

- Inworld 平台：https://platform.inworld.ai
- API 示例：https://github.com/inworld-ai/inworld-api-examples