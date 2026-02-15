---
name: aliyun-tts
description: 阿里巴巴云的文本转语音合成服务。
metadata: {"clawdbot":{"emoji":"🔊"}}
---

# aliyun-tts

阿里巴巴云文本转语音（Text-to-Speech, TTS）合成服务。

## 配置

请设置以下环境变量：
- `ALIYUN_APP_KEY` - 应用密钥
- `ALIYUN_ACCESS_KEY_ID` - 访问密钥 ID
- `ALIYUN_ACCESS_KEY_SECRET` - 访问密钥密码（敏感信息）

### 选项 1：命令行界面（CLI）配置（推荐）

```bash
# Configure App Key
clawdbot skills config aliyun-tts ALIYUN_APP_KEY "your-app-key"

# Configure Access Key ID
clawdbot skills config aliyun-tts ALIYUN_ACCESS_KEY_ID "your-access-key-id"

# Configure Access Key Secret (sensitive)
clawdbot skills config aliyun-tts ALIYUN_ACCESS_KEY_SECRET "your-access-key-secret"
```

### 选项 2：手动配置

编辑 `~/.clawdbot/clawdbot.json` 文件：

```json5
{
  skills: {
    entries: {
      "aliyun-tts": {
        env: {
          ALIYUN_APP_KEY: "your-app-key",
          ALIYUN_ACCESS_KEY_ID: "your-access-key-id",
          ALIYUN_ACCESS_KEY_SECRET: "your-access-key-secret"
        }
      }
    }
  }
}
```

## 使用方法

```bash
# Basic usage
{baseDir}/bin/aliyun-tts "Hello, this is Aliyun TTS"

# Specify output file
{baseDir}/bin/aliyun-tts -o /tmp/voice.mp3 "Hello"

# Specify voice
{baseDir}/bin/aliyun-tts -v siyue "Use siyue voice"

# Specify format and sample rate
{baseDir}/bin/aliyun-tts -f mp3 -r 16000 "Audio parameters"
```

## 参数选项

| 参数 | 描述 | 默认值 |
|------|-------------|---------|
| `-o, --output` | 输出文件路径 | tts.mp3 |
| `-v, --voice` | 语音名称 | siyue |
| `-f, --format` | 音频格式 | mp3 |
| `-r, --sample-rate` | 采样率 | 16000 |

## 可用的语音

常见语音包括：`siyue`, `xiaoxuan`, `xiaoyun` 等。完整的语音列表请参考阿里巴巴云的官方文档。

## 聊天语音回复

当用户请求语音回复时：

```bash
# Generate audio
{baseDir}/bin/aliyun-tts -o /tmp/voice-reply.mp3 "Your reply content"

# Include in your response:
# MEDIA:/tmp/voice-reply.mp3
```