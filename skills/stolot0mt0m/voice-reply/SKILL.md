---
name: voice-reply
version: 1.0.0
description: |
  Local text-to-speech using Piper voices via sherpa-onnx. 100% offline, no API keys required.
  Use when user asks for a voice reply, audio response, spoken answer, or wants to hear something read aloud.
  Supports multiple languages including German (thorsten) and English (ryan) voices.
  Outputs Telegram-compatible voice notes with [[audio_as_voice]] tag.
metadata:
  openclaw:
    emoji: "🎤"
    os: ["linux"]
    requires:
      bins: ["ffmpeg"]
      env: ["SHERPA_ONNX_DIR", "PIPER_VOICES_DIR"]
---

# 语音回复

使用 `sherpa-onnx` 和本地的 Piper TTS 生成语音音频回复，完全离线，无需使用任何云 API。

## 特点

- **100% 本地化**：设置完成后无需网络连接
- **无需 API 密钥**：免费使用，无需注册账户
- **多语言支持**：提供德语和英语语音
- **兼容 Telegram**：生成的语音消息会以气泡形式显示在 Telegram 中
- **自动检测语言**：根据输入文本自动选择相应的语音

## 先决条件

1. 已安装 `sherpa-onnx` 运行时环境
2. 已下载 Piper 语音模型
3. 安装了 `ffmpeg` 用于音频转换

## 安装

### 快速安装

```bash
cd scripts
sudo ./install.sh
```

### 手动安装

#### 1. 安装 `sherpa-onnx`

```bash
sudo mkdir -p /opt/sherpa-onnx
cd /opt/sherpa-onnx
curl -L -o sherpa.tar.bz2 "https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.12.23/sherpa-onnx-v1.12.23-linux-x64-shared.tar.bz2"
sudo tar -xjf sherpa.tar.bz2 --strip-components=1
rm sherpa.tar.bz2
```

#### 2. 下载语音模型

```bash
sudo mkdir -p /opt/piper-voices
cd /opt/piper-voices

# German - thorsten (medium quality, natural male voice)
curl -L -o thorsten.tar.bz2 "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-de_DE-thorsten-medium.tar.bz2"
sudo tar -xjf thorsten.tar.bz2 && rm thorsten.tar.bz2

# English - ryan (high quality, clear US male voice)
curl -L -o ryan.tar.bz2 "https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-en_US-ryan-high.tar.bz2"
sudo tar -xjf ryan.tar.bz2 && rm ryan.tar.bz2
```

#### 3. 安装 `ffmpeg`

```bash
sudo apt install -y ffmpeg
```

#### 4. 设置环境变量

将相关路径添加到 OpenClaw 服务或 shell 环境变量中：

```bash
export SHERPA_ONNX_DIR="/opt/sherpa-onnx"
export PIPER_VOICES_DIR="/opt/piper-voices"
```

## 使用方法

```bash
{baseDir}/bin/voice-reply "Text to speak" [language]
```

### 参数

| 参数 | 说明 | 默认值 |
|---------|-------------|---------|
| text | 需要转换成语音的文本 | （必填） |
| language | `de` 表示德语，`en` 表示英语 | 自动检测 |

### 示例

```bash
# German (explicit)
{baseDir}/bin/voice-reply "Hallo, ich bin dein Assistent!" de

# English (explicit)
{baseDir}/bin/voice-reply "Hello, I am your assistant!" en

# Auto-detect (detects German from umlauts and common words)
{baseDir}/bin/voice-reply "Guten Tag, wie geht es dir?"

# Auto-detect (defaults to English)
{baseDir}/bin/voice-reply "The weather is nice today."
```

## 输出格式

脚本会输出两行内容，OpenClaw 会将其处理后发送到 Telegram：

```
[[audio_as_voice]]
MEDIA:/tmp/voice-reply-output.ogg
```

- `[[audio_as_voice]]`：标记，用于指示 Telegram 将音频显示为气泡形式
- `MEDIA:path`：生成的 OGG Opus 音频文件的路径

## 可用的语音

| 语言 | 语音来源 | 音质 | 说明 |
|-------|---------|---------|-------------|
| 德语 (de) | thorsten | 中等 | 自然男性声音，发音清晰 |
| 英语 (en) | ryan | 高音质 | 清晰的美国男性声音，专业语气 |

## 添加更多语音

可在以下链接浏览可用的 Piper 语音模型：
- https://rhasspy.github.io/piper-samples/
- https://github.com/k2-fsa/sherpa-onnx/releases/tag/tts-models

下载语音模型并将其解压到 `$PIPER_VOICES_DIR` 目录中，然后修改脚本以使用新语音。

## 常见问题解决方法

### “找不到 TTS 可执行文件”
确保 `SHERPA_ONNX_DIR` 环境变量已正确设置，并且其中包含 `bin/sherpa-onnx-offline-tts` 文件。

### “无法生成音频”
检查语音模型文件（`.onnx`、`tokens.txt`、`espeak-ng-data/`）是否齐全。

### 音频以文件形式显示而非气泡形式
确保输出内容中 `[[audio_as_voice]]` 标签位于 `MEDIA:` 行之前。

## 致谢

- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)：离线语音处理工具
- [Piper](https://github.com/rhasspy/piper)：快速的本地 TTS 语音库
- [Thorsten Voice](https://github.com/thorstenMueller/Thorsten-Voice)：德语语音数据集