---
name: say
description: 通过 macOS 的 `say` 命令和 Siri 的自然语音功能实现文本转语音（Text-to-Speech, TTS）。该功能可用于生成语音音频、TTS 视频片段，或在 macOS 上朗读文本。
metadata: {"openclaw":{"emoji":"🔊","os":["darwin"],"requires":{"bins":["say","ffmpeg"]}}}
---

# say

在 macOS 上，可以使用 `say` 命令来实现设备上的文本转语音功能。

## Siri 自然语音（推荐）

Siri 的语音效果是 macOS 上最好的文本转语音选项，但无法通过 `-v` 参数来选择特定语音。只需直接运行 `say` 命令即可（不带 `-v` 参数），系统会使用默认的语音。若需切换语言，可以使用 `defaults write` 命令进行设置：

```bash
# Switch to German
defaults write com.apple.speech.voice.prefs SystemTTSLanguage -string "de"
say "Hallo, wie geht's?" -o output_de.aiff

# Switch to Chinese (Mandarin)
defaults write com.apple.speech.voice.prefs SystemTTSLanguage -string "cmn"
say "你好，世界" -o output_zh.aiff
```

无需重启系统，下次再次使用 `say` 命令时，系统会自动使用新设置的语言。

### 先决条件

首先，在 **系统设置 > 辅助功能 > 语音内容** 中下载所需的语音文件，并将其设置为每种语言的系统默认语音。

查看当前已配置的语音列表：

```bash
defaults read com.apple.Accessibility SpokenContentDefaultVoiceSelectionsByLanguage
```

## 备用方案：通过 `-v` 参数选择语音

对于非 Siri 提供的语音，可以直接使用 `-v` 参数来指定语音：

```bash
say -v 'Tingting (Enhanced)' "你好，世界"
say -v '?'  # list all installed voices (Siri voices not listed)
```

## 将语音内容输出到文件

可以使用 `say` 命令将语音内容保存为音频文件。例如：

```bash
say -o output.aiff "Hello world"
ffmpeg -y -i output.aiff -ar 22050 -ac 1 output.wav  # convert to WAV
```

## 常用选项

- `-v <语音名称>`：选择特定的非 Siri 语音
- `-r <语速>`：指定语音的朗读速度（单位：每分钟单词数，例如 `-r 150`）
- `-o <文件路径>`：将输出文件保存为 AIFF 格式

## 注意事项

- `say` 会自动在标点符号处添加适当的停顿，无需手动分割句子
- AIFF 是系统的原生输出格式；如需转换为 WAV 或 MP3 格式，可以使用 ffmpeg 工具
- 对于批量生成语音文件的情况，建议先设置好语言，一次性生成所有音频文件后再进行语言切换，这样可以减少对 `defaults write` 命令的调用次数