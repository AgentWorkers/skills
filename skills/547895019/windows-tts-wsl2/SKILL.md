---
name: windows-tts
description: 在 Windows 11 中，可以通过 WSL2/TUI 使用 Windows 内置的 TTS（System.Speech）功能将文本朗读出来。当用户要求中文语音播放、希望助手在电脑上“直接播放声音”，或者 OpenClaw 的内置 TTS 功能不支持中文时，可以使用此方法。
---

# Windows TTS (WSL2)

通过 `powershell.exe` 使用 Windows 内置的 TTS 功能，这样音频将会通过 Windows 的声音设备播放（无需使用 WSLg PulseAudio）。

## 快速入门（中文发音）

在 WSL 中运行以下命令：

```bash
bash {baseDir}/scripts/saycn.sh "你好，我是你的助手。"
```

## 列出已安装的语音

```bash
bash {baseDir}/scripts/list_voices.sh
```

## 使用特定的语音进行发音

```bash
bash {baseDir}/scripts/saycn.sh --voice "VOICE_NAME" "你好，我以后会用这个声音说话。"
```

## 注意事项：

- 如果你直接在 bash 中使用 PowerShell，请记得对 `$` 进行转义处理，或者使用外部单引号；否则 bash 会解析 `$s` 并导致命令执行失败。
- 如果用户遇到诸如 `=New-Object` 或 `TypeName:` 等提示错误，建议使用提供的脚本，而不是自行编写引号。