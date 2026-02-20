---
name: discord-local-stt-tts-installer
description: （macOS）Discord语音助手安装程序。请从GitHub的发布版本中安装或更新`discord-local-stt-tts`（该工具集包含Discord语音功能、本地语音转文本（STT）以及本地文本转语音（TTS）功能）。
---
# discord-local-stt-tts-installer (macOS)

这是一个用于安装/更新 **discord-local-stt-tts** OpenClaw 插件的 ClawHub 工具。

- 插件仓库：https://github.com/vilmire/discord-local-stt-tts
- 安装路径：`~/.openclaw/openclaw-extensions/plugins/discord-local-stt-tts`

## 支持的平台
- **仅限 macOS**

## 必需软件
- `curl`  
- `python3`（安装程序所需；某些本地文本转语音（STT）引擎也需要）  
- `unzip`  
- `ffmpeg`（插件运行时必需）  
- 可选：`pnpm`（如果希望安装程序尝试构建插件）

## macOS 权限设置
如果您使用 Apple Speech（`apple-speech`）作为本地文本转语音服务，macOS 可能需要以下权限设置：
- 系统设置 → 隐私与安全 → **语音识别**  
- 系统设置 → 隐私与安全 → **麦克风**

## 安装 / 更新
```bash
bash bin/install.sh
openclaw gateway restart
```

## 安装程序的功能
1) 下载最新的 GitHub 仓库源代码压缩包  
2) 备份现有的插件文件夹  
3) 将插件安装到 OpenClaw 的扩展插件目录中  
4) 如果安装了 `pnpm`，则会尝试执行 `pnpm i && pnpm build`（仅尝试构建插件，不保证成功）

## 注意事项
- 该工具不会修改您的 `openclaw.json` 文件。您仍需要手动启用并配置该插件。