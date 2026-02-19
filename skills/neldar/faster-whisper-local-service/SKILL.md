---
name: faster-whisper-local-service
description: Local speech-to-text (STT) transcription service for OpenClaw using faster-whisper. Runs as HTTP microservice on localhost for voice input, microphone transcription, and speech recognition. No recurring API costs — after initial model download, runs fully local. Supports WebChat voice input, Telegram voice messages, and any OpenClaw voice workflow. Keywords: STT, speech to text, voice transcription, local transcription, whisper, faster-whisper, offline, microphone, speech recognition, voice input.
---

# 更快的Whisper本地服务

该服务提供了一个用于语音技能的本地STT（Speech-to-Text）后端。

## 功能说明

- 为`faster-whisper`项目创建一个Python虚拟环境（`venv`）。
- 配置`transcribe-server.py` HTTP端点，地址为`http://127.0.0.1:18790/transcribe`。
- 创建一个Systemd用户服务：`openclaw-transcribe.service`。

## 重要提示：首次运行时需要下载模型

在首次启动时，`faster-whisper`会从Hugging Face下载模型权重文件（`medium`模型大小约为1.5GB）。此过程需要网络连接和足够的磁盘空间。下载完成后，模型会被缓存到本地，之后服务即可完全离线运行。

| 模型类型 | 下载大小 | 内存占用 |
|---|---|---|
| tiny | 约75 MB | 约400 MB |
| base | 约150 MB | 约500 MB |
| small | 约500 MB | 约800 MB |
| medium | 约1.5 GB | 约1.4 GB |
| large-v3 | 约3.0 GB | 约3.5 GB |

若希望在无网络连接的环境中预下载模型，请参考[`faster-whisper`的文档](https://github.com/SYSTRAN/faster-whisper#model-download)。

## 安全注意事项

- **gst-launch-1.0**：该服务使用GStreamer的`decodebin`将输入音频转换为WAV格式。虽然参数是通过列表传递的（避免了shell注入风险），但处理不可信或格式错误的音频文件仍存在风险（这些风险来自GStreamer的媒体解析器）。请确保使用操作系统官方提供的`gst-launch-1.0`版本。
- **绑定地址**：该服务仅绑定到`127.0.0.1`（不对外公开）。
- **CORS**：默认情况下仅允许来自`https://127.0.0.1:8443`的请求。
- **无需凭证**：该服务不请求任何API密钥或敏感信息。

## 默认的安全和可复现性设置

- 固定安装的软件包版本：`faster-whisper==1.1.1`（可通过环境变量进行修改）。
- 显式检查对`gst-launch-1.0`的依赖关系。
- CORS默认仅允许来自`https://127.0.0.1:8443`的请求（可通过环境变量进行修改）。
- 工作空间和服务路径可配置（无需硬编码用户路径）。

## 部署方式

```bash
bash scripts/deploy.sh
```

### 自定义配置方法

```bash
WORKSPACE=~/.openclaw/workspace \
TRANSCRIBE_PORT=18790 \
WHISPER_MODEL_SIZE=medium \
WHISPER_LANGUAGE=auto \
TRANSCRIBE_ALLOWED_ORIGIN=https://10.0.0.42:8443 \
bash scripts/deploy.sh
```

### 语言设置

默认设置为`auto`（自动检测语言）。若需要仅支持德语，请将`WHISPER_LANGUAGE`设置为`de`；仅支持英语则设置为`en`等。如果只使用一种语言，固定语言设置可以提高处理速度和准确性。

该服务可以重复运行而不会产生副作用。

## 该服务会修改的文件和目录

| 修改内容 | 目录路径 | 操作内容 |
|---|---|---|
| Python虚拟环境 | `$WORKSPACE/.venv-faster-whisper/` | 创建虚拟环境并通过pip安装`faster-whisper` |
| 语音转录服务器脚本 | `$WORKSPACE/voice-input/transcribe-server.py` | 编写服务器脚本 |
| Systemd服务配置文件 | `~/.config/systemd/user/openclaw-transcribe.service` | 创建并启用系统服务 |
| 模型缓存目录 | `~/.cache/huggingface/` | 首次运行时下载模型权重文件 |

## 卸载方法

```bash
systemctl --user stop openclaw-transcribe.service
systemctl --user disable openclaw-transcribe.service
rm -f ~/.config/systemd/user/openclaw-transcribe.service
systemctl --user daemon-reload
```

### 可选的完整清理操作

```bash
rm -rf ~/.openclaw/workspace/.venv-faster-whisper
rm -f ~/.openclaw/workspace/voice-input/transcribe-server.py
```

## 验证方法

- 确认服务已启动。
- 测试端点是否响应（对于无效的音频样本，HTTP响应状态码200或500均为正常结果）。

## 其他说明

- 该服务仅提供语音转录功能。
- 需要与`webchat-voice-proxy`配合使用，以实现浏览器麦克风与HTTPS/WSS的集成。
- 如需一步完成部署，请使用`webchat-voice-full-stack`（依次部署后端服务和代理）。