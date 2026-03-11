---
name: volcengine-ata-subtitle
description: "使用 Volcengine 的 ATA API 生成具有自动时间对齐功能的字幕。适用于以下场景：  
(1) 为视频添加时间对齐的字幕；  
(2) 将文本和音频转换为 SRT/ASS 格式；  
(3) 自动化字幕制作流程。"
version: 1.0.0
category: media-processing
argument-hint: "[audio file] [text file] [output file]"
license: MIT
---
# Volcengine ATA字幕生成（自动时间对齐）

使用Volcengine的ATA（Automatic Time Alignment）API生成具有自动时间对齐功能的字幕。

## 先决条件

设置以下环境变量或创建配置文件：

### 选项A：环境变量

```bash
export VOLC_ATA_APP_ID="your-app-id"
export VOLC_ATA_TOKEN="your-access-token"
export VOLC_ATA_API_BASE="https://openspeech.bytedance.com"
```

### 选项B：配置文件

创建`~/.volcengine_ata.conf`文件：

```ini
[credentials]
appid = your-app-id
access_token = your-access-token
secret_key = your-secret-key

[api]
base_url = https://openspeech.bytedance.com
submit_path = /api/v1/vc/ata/submit
query_path = /api/v1/vc/ata/query
```

## 执行方式（Python CLI工具）

提供了一个名为`volc_ata.py`的Python CLI工具，位于`~/.openclaw/workspace/skills/volcengine-ata-subtitle`目录下。

### 快速示例

```bash
# Basic usage: audio + text → SRT subtitle
python3 ~/.openclaw/workspace/skills/volcengine-ata-subtitle/volc_ata.py \
  --audio storage/audio.wav \
  --text storage/subtitle.txt \
  --output storage/subtitles/final.srt

# Specify output format (srt or ass)
python3 ~/.openclaw/workspace/skills/volcengine-ata-subtitle/volc_ata.py \
  --audio storage/audio.wav \
  --text storage/subtitle.txt \
  --output storage/subtitles/final.ass \
  --format ass
```

## 输入要求

### 音频文件

- **格式**：WAV（PCM）
- **采样率**：16000 Hz（16kHz）
- **声道**：1（单声道）
- **编码**：16位PCM（`pcm_s16le`）

**从视频中提取音频**：
```bash
ffmpeg -i input.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
```

### 文本文件

- **格式**：纯文本（UTF-8）
- **结构**：每行一个句子
- **不含标点符号**：ATA会自动处理
- **不含时间戳**：仅包含纯文本

**示例**：
```
主人闹钟没响睡过头了
我们俩轮流用鼻子拱他脸
他以为地震了抱着枕头就跑
```

## 输出格式

### SRT（SubRip）

```srt
1
00:00:00,000 --> 00:00:02,500
第一句字幕

2
00:00:02,500 --> 00:00:05,000
第二句字幕
```

### ASS（Advanced Substation Alpha）

```ass
[Script Info]
Title: ATA Subtitles
ScriptType: v4.00+

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:02.50,Default,,0,0,0,,第一句字幕
```

## 规则

1. **在进行API调用之前，请务必检查配置是否正确。**
2. **音频必须是16kHz单声道PCM格式**——如有必要，请使用ffmpeg进行转换。
3. **文本应为纯文本**——不得包含时间戳或标点符号。
4. **默认输出格式**：SRT（兼容性最佳）。
5. **优雅地处理错误**——显示清晰的错误信息。

## 故障排除

### 无效的采样率

**错误**：`无效的采样率，预期值为16000Hz`

**解决方法**：
```bash
ffmpeg -i input.mp4 -ar 16000 -ac 1 audio.wav
```

### 授权失败

**错误**：`授权失败`

**解决方法**：检查令牌格式。令牌应为`Bearer; {token}`（以分号结尾）。

## 相关文档

- [Volcengine ATA文档](https://www.volcengine.com/docs/6561/163043?lang=zh)