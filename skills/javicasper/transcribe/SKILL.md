---
name: transcribe
description: 使用本地的 Whisper 工具（基于 Docker）将音频文件转换为文本。适用于接收语音消息、处理音频文件（格式包括 .mp3、.m4a、.ogg、.wav、.webm）时，或需要将音频内容转录为文本的场景。
---

# 语音转录

使用 `faster-whisper` 在 Docker 中实现本地音频转录功能。

## 安装

```bash
cd /path/to/skills/transcribe/scripts
chmod +x install.sh
./install.sh
```

此步骤会构建 `whisper:local` Docker 镜像，并安装 `transcribe` 命令行工具（CLI）。

## 使用方法

```bash
transcribe /path/to/audio.mp3 [language]
```

- 默认语言：`es`（西班牙语）
- 使用 `auto` 选项进行自动语言检测
- 转录结果以纯文本形式输出到标准输出（stdout）

## 示例

```bash
transcribe /tmp/voice.ogg          # Spanish (default)
transcribe /tmp/meeting.mp3 en     # English
transcribe /tmp/audio.m4a auto     # Auto-detect
```

## 支持的音频格式

mp3、m4a、ogg、wav、webm、flac、aac

## 接收语音消息时的操作流程：

1. 将音频文件保存到临时文件夹中。
2. 运行 `transcribe <路径>` 命令进行转录。
3. 将转录结果包含在回复中。
4. 删除临时文件夹中的音频文件。

## 相关文件：

- `scripts/transcribe`：`transcribe` 命令行的封装脚本（基于 Bash）。
- `scripts/install.sh`：安装脚本（包含 Dockerfile）。

## 注意事项：

- 使用的模型为 `small`（转录速度较快，但准确性较低）；如需更高准确性，请修改 `install.sh` 文件以使用 `large-v3` 模型。
- 该工具完全基于本地处理，无需使用 API 密钥。