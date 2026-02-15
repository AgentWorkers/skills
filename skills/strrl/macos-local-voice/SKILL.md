---
name: macos-local-voice
description: "在 macOS 上，可以利用 Apple 的原生功能实现本地的语音转文本（STT）和文本转语音（TTS）功能。语音转文本通过 `yap`（Apple Speech.framework）完成，文本转语音则通过 `say` 和 `ffmpeg` 来实现。整个过程完全离线进行，无需使用任何 API 密钥。系统还提供了语音质量检测和智能语音选择的功能。"
metadata: { "openclaw": { "emoji": "🎙️", "requires": { "bins": ["yap", "say", "osascript"], "os": ["darwin"] } } }
---

# macOS 本地语音功能

在 macOS 上，支持完全本地的文字转语音（STT）和语音转文字（TTS）功能。无需使用 API 密钥，也不依赖网络或云端服务，所有处理都在设备上完成。

## 系统要求

- macOS（推荐使用 Apple Silicon 处理器，Intel 处理器也可使用）
- 系统路径（PATH）中包含 `yap` 命令行工具——可通过 `brew install finnvoor/tools/yap` 安装
- 系统路径中包含 `ffmpeg` 工具（可选，用于生成 ogg/opus 格式的音频文件）——可通过 `brew install ffmpeg` 安装
- `say` 和 `osascript` 是 macOS 的内置工具

## 文字转语音（STT）

使用苹果设备的自动语音识别功能将音频文件转换为文本。

```bash
node {baseDir}/scripts/stt.mjs <audio_file> [locale]
```

- `audio_file`：音频文件的路径（支持格式：ogg, m4a, mp3, wav 等）
- `locale`：可选，例如 `zh_CN`, `en_US`, `ja_JP`。如果省略，则使用系统默认设置。
- 将转录后的文本输出到标准输出（stdout）。

### 支持的 STT 语言设置

使用命令 `node {baseDir}/scripts/stt.mjs --locales` 可查看所有支持的语言设置。

支持的语言包括：`en_US`, `en_GB`, `zh_CN`, `zh_TW`, `zh_HK`, `ja_JP`, `ko_KR`, `fr_FR`, `de_DE`, `es_ES`, `pt_BR`, `ru_RU`, `vi_VN`, `th_TH`。

### 语言检测建议

- 如果用户的最新消息是中文，使用 `zh_CN` 语言设置；
- 如果是英文，使用 `en_US`；
- 如果消息内容混合或难以识别，可以尝试不设置语言设置（使用系统默认语言）。

## 语音转文字（TTS）

使用 macOS 的原生语音合成功能将文本转换为音频文件。

```bash
node {baseDir}/scripts/tts.mjs "<text>" [voice_name] [output_path]
```

- `text`：要转换成语音的文本
- `voice_name`：可选，例如 `Yue (Premium)`, `Tingting`, `Ava (Premium)`。如果省略，系统会自动选择最适合当前文本的语言的语音。
- `output_path`：可选，默认输出路径为 `~/.openclaw/media/outbound/` 目录下的文件（文件名包含时间戳）。
- 将生成的音频文件路径输出到标准输出（stdout）。
- 如果系统安装了 `ffmpeg`，输出格式为 ogg/opus（适合消息平台）；否则输出格式为 aiff。

### 以语音消息的形式发送音频文件

生成音频文件后，可以使用 `message` 工具将其发送出去：

```
message action=send media=<path_from_tts.sh> asVoice=true
```

## 语音管理

- 查看可用的语音选项，检查语音的可用性，或根据需要选择适合某种语言的语音。

```bash
node {baseDir}/scripts/voices.mjs list [locale]     # List voices, optionally filter by locale
node {baseDir}/scripts/voices.mjs check "<name>"     # Check if a specific voice is downloaded and ready
node {baseDir}/scripts/voices.mjs best <locale>       # Get the highest quality voice for a locale
```

### 语音质量设置

- 1：压缩格式（质量较低，始终可用）
- 2：增强型格式（质量中等，可能需要下载）
- 3：高级格式（最高质量，需要从系统设置中下载）

### 如果某个语音无法使用

向用户提示：“语音 X 未下载。请前往 **系统设置 → 辅助功能 → 语音内容 → 系统语音 → 管理语音** 进行下载。”

## 注意事项

- 如果请求的语音无法使用，`say` 命令会自动切换到默认语音（退出代码为 0，不会显示错误）。在使用 `tts.mjs` 时，请务必先使用 `voices.mjs check` 命令检查所需语音是否可用。
- 高级语音（如 `Yue (Premium)`, `Ava (Premium)` 的音质更好，但需要用户手动下载。
- Siri 的语音无法通过语音合成 API 使用。