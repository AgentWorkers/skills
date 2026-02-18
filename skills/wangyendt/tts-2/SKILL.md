---
name: pywayne-tts
description: 文本转语音工具。用于将文本转换为语音音频文件（opus或mp3格式）。支持macOS内置的“say”命令以及通过ffmpeg进行音频转换的Google TTS（gTTS）服务。
---
# Pywayne TTS

这是一个文本转语音（TTS）工具，可以将文本转换为音频文件（opus 或 mp3 格式）。

## 功能

### text_to_speech_output_opus - 将文本转换为 Opus 格式

```python
from pywayne.tts import text_to_speech_output_opus

# Output: test.opus
text_to_speech_output_opus("你好，世界", "test.opus")
```

**参数：**
- `text` - 需要转换的文本
- `opus_filename` - 输出的 .opus 文件名
- `use_say` - 如果为 True，则使用 macOS 的 'say' 命令；否则使用 gTTS（默认值为 True）

**行为：**
- 在 macOS 上，当 `use_say` 为 True 时，优先使用原生的 'say' 命令
- 在其他平台上，使用 Google TTS 服务
- 使用 ffmpeg 将音频转换为 opus 格式（16kHz，单声道）
- 会自动清理临时文件

### text_to_speech_output_mp3 - 将文本转换为 MP3 格式

```python
from pywayne.tts import text_to_speech_output_mp3

# Output: test.mp3
text_to_speech_output_mp3("你好，世界", "test.mp3")
```

**参数：**
- `text` - 需要转换的文本
- `mp3_filename` - 输出的 .mp3 文件名
- `use_say` - 如果为 True，则使用 macOS 的 'say' 命令；否则使用 gTTS（默认值为 True）

**行为：**
- 在 macOS 上，当 `use_say` 为 True 时，优先使用原生的 'say' 命令
- 在其他平台上，使用 Google TTS 服务
- 使用 ffmpeg 将音频转换为 mp3 格式
- 会自动清理临时文件

## 快速入门

```bash
# Convert text to Opus format (default: macOS uses 'say')
text_to_speech_output_opus "你好，世界" "test.opus"

# Convert text to MP3 format
text_to_speech_output_mp3 "你好，世界" "test.mp3"

# Force use gTTS instead of macOS 'say'
text_to_speech_output_mp3 "你好，世界" "test.mp3" use_say=False
```

## 所需软件

- **ffmpeg**：用于音频转换
  - macOS：使用 `brew install ffmpeg` 安装
  - Windows：从 https://ffmpeg.org 下载并添加到 PATH 环境变量中
  - Linux：使用 `sudo apt install ffmpeg` 或通过包管理器安装
- **gtts**：用于调用 Google TTS 服务的 Python 库

## 平台检测

该工具会自动检测当前平台，并在缺少 ffmpeg 时提示用户进行安装。

## 音频格式

- **Opus**：音质更好，文件体积更小，适合语音通话
- **MP3**：兼容性更强，适合多媒体播放

## 注意事项

- 使用 gTTS 服务需要网络连接
- 临时文件会自动被清理
- 确保输出目录具有写入权限