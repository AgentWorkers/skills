---
name: elevenlabs-transcribe
description: 使用 ElevenLabs Scribe 将音频转录为文本。支持批量转录、从 URL 实时流式转录、麦克风输入以及本地文件转录。
homepage: https://elevenlabs.io/speech-to-text
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["ffmpeg","python3"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# ElevenLabs 语音转文本服务

> ** ElevenLabs官方提供的语音转文本功能。**

该服务能够以极高的准确率将音频转换为文本，支持90多种语言、语音识别功能以及实时流处理。

## 前提条件

- 已安装`ffmpeg`（在macOS上使用`brew install ffmpeg`命令安装）
- 确保`ELEVENLABS_API_KEY`环境变量已设置
- 确保使用Python 3.8或更高版本（依赖项会在首次运行时自动安装）

## 使用方法

```bash
{baseDir}/scripts/transcribe.sh <audio_file> [options]
{baseDir}/scripts/transcribe.sh --url <stream_url> [options]
{baseDir}/scripts/transcribe.sh --mic [options]
```

## 示例

### 批量转录

转录本地音频文件：

```bash
{baseDir}/scripts/transcribe.sh recording.mp3
```

### 带有语音识别的转录

```bash
{baseDir}/scripts/transcribe.sh meeting.mp3 --diarize
```

### 获取包含时间戳的完整JSON响应

```bash
{baseDir}/scripts/transcribe.sh interview.wav --diarize --json
```

### 实时流处理

从URL（例如：直播电台、播客）获取音频流并进行转录：

```bash
{baseDir}/scripts/transcribe.sh --url https://npr-ice.streamguys1.com/live.mp3
```

### 通过麦克风进行转录

```bash
{baseDir}/scripts/transcribe.sh --mic
```

### 实时转录本地文件（适用于测试）

```bash
{baseDir}/scripts/transcribe.sh audio.mp3 --realtime
```

### 为代理程序启用静音模式

抑制标准错误输出中的状态信息：

```bash
{baseDir}/scripts/transcribe.sh --mic --quiet
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `--diarize` | 识别音频中的不同说话者 |
| `--lang CODE` | ISO语言代码（例如：`en`、`pt`、`es`、`fr`） |
| `--json` | 输出包含时间戳和元数据的完整JSON格式 |
| `--events` | 标记音频中的事件（如笑声、音乐、掌声等） |
| `--realtime` | 实时处理音频流而非批量处理 |
| `--partials` | 在实时模式下显示中间转录结果 |
| `-q, --quiet` | 抑制状态信息（推荐用于代理程序） |

## 输出格式

### 文本模式（默认）

纯文本格式的转录结果：

```
The quick brown fox jumps over the lazy dog.
```

### JSON模式（使用`--json`选项）

```json
{
  "text": "The quick brown fox jumps over the lazy dog.",
  "language_code": "eng",
  "language_probability": 0.98,
  "words": [
    {"text": "The", "start": 0.0, "end": 0.15, "type": "word", "speaker_id": "speaker_0"}
  ]
}
```

### 实时模式

转录结果会在生成后立即输出。使用`--partials`选项时，会显示中间转录结果：

```
[partial] The quick
[partial] The quick brown fox
The quick brown fox jumps over the lazy dog.
```

## 支持的文件格式

**音频格式：** MP3、WAV、M4A、FLAC、OGG、WebM、AAC、AIFF、Opus
**视频格式：** MP4、AVI、MKV、MOV、WMV、FLV、WebM、MPEG、3GPP

**限制：** 文件大小不超过3GB，音频时长不超过10小时

## 错误处理

遇到错误时，脚本会以非零状态码退出：

- **API密钥缺失：** 请设置`ELEVENLABS_API_KEY`环境变量
- **文件未找到：** 请检查文件路径是否正确
- **未安装ffmpeg：** 请使用包管理器安装该工具
- **API错误：** 请检查API密钥的有效性及使用频率限制

## 各种模式的适用场景

| 场景 | 命令示例 |
|----------|---------|
| 转录录音文件 | `./transcribe.sh file.mp3` |
| 多人参与的会议录音 | `./transcribe.sh meeting.mp3 --diarize` |
| 直播电台/播客流 | `./transcribe.sh --url <url>` |
| 通过麦克风输入语音 | `./transcribe.sh --mic --quiet` |
| 需要标注单词的时间戳 | `./transcribe.sh file.mp3 --json` |