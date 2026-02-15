---
name: telegram-voice-to-voice-macos
description: "适用于 macOS 上搭载 Apple Silicon 处理器的 Telegram 应用：使用 `yap`（Speech.framework）库将接收到的 `.ogg` 格式的语音笔记转录为文本，然后通过 `say+ffmpeg` 工具将文本转换回语音笔记并通过 Telegram 发送。该功能不支持 Linux 和 Windows 系统。"
metadata: {"openclaw":{"os":["darwin"],"requires":{"bins":["yap","ffmpeg","say","defaults"]}}}
---

# Telegram语音转语音功能（仅支持macOS Apple Silicon系统）

这是一个由OpenClaw提供的技能（skill）。

## 使用要求

- 确保使用的是搭载Apple Silicon处理器的macOS系统。
- 确保`yap`命令行工具（用于语音转文本的转录功能）已添加到系统的`PATH`环境变量中（该工具来自Speech.framework）。
  - 项目链接：https://github.com/finnvoor/yap（由finnvoor开发）
- 确保`ffmpeg`命令行工具也已添加到`PATH`环境变量中。

## 兼容性说明（重要）

此功能仅适用于macOS系统（依赖`say`命令和Speech.framework）。由于技能注册系统无法强制用户遵守操作系统限制，因此在Linux或Windows系统上安装或运行此功能可能会导致运行时错误。

## 持久回复模式（语音或文本）

系统会在工作区中存储一个与用户相关联的配置文件：

- 配置文件路径：`voice_state/telegram.json`
- 文件内容：
  - `"voice"`：回复时使用Telegram的语音消息。
  - `"text"`：回复时使用纯文本消息。

如果该配置文件不存在或发送者的用户ID信息缺失，系统将默认使用“语音”模式进行回复。

### 切换模式命令

- 当收到纯文本消息时，执行以下命令：
  - `/audio off`：将回复模式切换为“文本”，并通过发送一条简短的文本消息进行确认。
  - `/audio on`：将回复模式切换为“语音”，并通过发送一条简短的文本消息进行确认。

## 获取传入的语音文件（.ogg格式）

Telegram的语音消息通常会以`<media:audio>`的形式嵌入在消息文本中。OpenClaw会将这些语音文件保存在以下路径：
  - `~/.openclaw/media/inbound/`

推荐的处理方式：
  1. 如果传入的消息中包含了语音文件的路径，直接使用该路径。
  2. 如果没有提供路径，系统会自动从`~/.openclaw/media/inbound/`目录中选取最新的`.ogg`格式语音文件。

## 转录功能

- 转录使用的默认语言环境为macOS系统的默认语言设置。
- 可选环境变量：`YAP_LOCALE`（用于覆盖语言设置，例如`it-IT`、`en-US`）。
- 推荐的转录命令：`yap transcribe --locale "${YAP_LOCALE:-<system>}" <path.ogg>`
  - 如果未设置`YAP_LOCALE`，系统会使用macOS系统的默认语言设置（通过`defaults read -g AppleLocale`获取）。
- 如果转录失败或转录结果为空，系统会提示用户重新发送语音或输入文本。

### 辅助脚本

用于处理语音文件转录的脚本：`scripts/transcribe_telegram_ogg.sh [path.ogg]`

## 回复行为

### 回复模式：语音（默认）

- 默认情况下，系统会使用macOS系统预设的语音效果进行回复。用户也可以通过传递特定的语音名称来自定义语音效果：
  1. 生成需要回复的文本。
  2. 使用`scripts/tts_telegram_voice.sh "<回复文本>" [SYSTEM|VoiceName]`命令将文本转换为`.ogg`格式的语音文件。
  3. 使用`message`工具将生成的`.ogg`文件作为语音消息发送回Telegram（注意设置`asVoice: true`选项），并指定`media`参数为语音文件的路径。
  - 可选地，可以通过设置`replyTo`参数将回复消息关联到原始对话线程中。

**提示：**建议始终使用系统预设的语音效果（`SYSTEM`）。

### 回复模式：文本

- 回复时直接发送纯文本消息，格式如下：
  - `Transcription: <...>`
  - `Reply: <...>`