---
name: faster-whisper-local-service
description: Local speech-to-text (STT) transcription service for OpenClaw using faster-whisper. Runs as HTTP microservice on localhost for voice input, microphone transcription, and speech recognition. No recurring API costs — after initial model download, runs fully local. Supports WebChat voice input, Telegram voice messages, and any OpenClaw voice workflow. Keywords: STT, speech to text, voice transcription, local transcription, whisper, faster-whisper, offline, microphone, speech recognition, voice input.
---

# 更快速的 Whisper 本地服务

该服务提供了一个用于语音技能的本地文本转语音（STT）后端。

## 功能介绍

- 为 `faster-whisper` 创建一个 Python 虚拟环境（`venv`）。
- 提供一个名为 `transcribe-server.py` 的 HTTP 服务端点，地址为 `http://127.0.0.1:18790/transcribe`。
- 配置一个 systemd 用户服务：`openclaw-transcribe.service`。

## 重要提示：首次运行时需要下载模型

在首次启动时，`faster-whisper` 会从 Hugging Face 下载模型权重文件（`medium` 模型的大小约为 1.5 GB）。此过程需要网络连接和足够的磁盘空间。下载完成后，模型会被缓存到本地，之后服务即可完全离线运行。

| 模型 | 下载大小 | 内存占用 |
|---|---|---|
| tiny | 约 75 MB | 约 400 MB |
| base | 约 150 MB | 约 500 MB |
| small | 约 500 MB | 约 800 MB |
| medium | 约 1.5 GB | 约 1.4 GB |
| large-v3 | 约 3.0 GB | 约 3.5 GB |

若希望在无网络连接的环境中预下载模型，请参阅 [faster-whisper 的文档](https://github.com/SYSTRAN/faster-whisper#model-download)。

## 安全注意事项

### 网络隔离
- 仅绑定到 `127.0.0.1` 地址——无法从外部网络访问该服务。
- 通过 CORS 限制请求来源，默认只允许来自 `https://127.0.0.1:8443` 的请求。
- 服务不使用或存储任何凭据、API 密钥或敏感信息。

### 输入验证
- **上传文件大小限制**：超出配置限制的请求会在处理前被拒绝（返回 HTTP 413 错误）。默认值为 50 MB，可通过 `MAX_UPLOAD_MB` 配置。
- **文件格式验证**：仅接受具有有效音频格式（WAV、OGG、FLAC、MP3、WebM、M4A）的文件；不支持的格式会在传递给 GStreamer 之前被拒绝（返回 HTTP 415 错误）。
- **子进程安全性**：所有传递给 `gst-launch-1.0` 的参数都以列表形式传递，防止 shell 扩展或注入攻击。

### 对 GStreamer 的依赖

该服务依赖 GStreamer 的 `decodebin` 模块进行音频格式转换。作为媒体处理库，GStreamer 的解析器需要保持最新状态。**建议措施**：从操作系统供应商提供的可信软件包中安装 `gst-launch-1.0`，并定期应用安全更新。上述的文件格式验证机制可以防止非音频数据被传递给 GStreamer。

### 数据安全
- 服务在首次下载模型后不再进行任何 outbound 网络请求。
- 服务不发送任何遥测数据或进行数据分析。
- 临时文件会生成在每个请求对应的 `TemporaryDirectory` 目录中，并在任务完成后立即清除。

## 可复现性配置

- 固定使用的软件包版本：`faster-whisper==1.1.1`（可通过环境变量覆盖）。
- 明确要求依赖 `gst-launch-1.0`。
- 默认情况下，CORS 仅允许来自一个源的请求。
- 工作空间和服务路径可配置（不会使用硬编码的用户路径）。

## 部署方式

```bash
bash scripts/deploy.sh
```

（部署相关代码块）

### 语言设置

默认语言为 `auto`（自动检测语言）。若需要指定语言，可设置 `WHISPER_LANGUAGE`，例如 `de` 表示德语，`en` 表示英语等。仅使用一种语言时，使用固定语言可以提高处理速度和准确性。

该服务具有幂等性（多次运行结果一致）。

## 该服务会修改的文件和目录

| 修改内容 | 修改路径 | 修改操作 |
|---|---|---|
| Python 虚拟环境 | `$WORKSPACE/.venv-faster-whisper/` | 创建虚拟环境并通过 pip 安装 `faster-whisper` |
| 语音转录服务器脚本 | `$WORKSPACE/voice-input/transcribe-server.py` | 生成并保存服务器脚本 |
| systemd 服务配置 | `~/.config/systemd/user/openclaw-transcribe.service` | 创建并启用服务 |
| 模型缓存目录 | `~/.cache/huggingface/` | 首次运行时下载模型文件 |

## 卸载方式

```bash
systemctl --user stop openclaw-transcribe.service
systemctl --user disable openclaw-transcribe.service
rm -f ~/.config/systemd/user/openclaw-transcribe.service
systemctl --user daemon-reload
```

（卸载相关代码块）

### 全面清理（可选）

```bash
rm -rf ~/.openclaw/workspace/.venv-faster-whisper
rm -f ~/.openclaw/workspace/voice-input/transcribe-server.py
```

## 验证方法

- 确认服务已启动（状态应为 `active`）。
- 测试服务端点是否响应（对于无效的输入数据，应返回 HTTP 200 或 500 状态码）。

## 其他说明

- 该服务仅提供文本转语音功能。
- 需要与 `webchat-voice-proxy` 服务配合使用，以实现浏览器麦克风与 HTTPS/WSS 协议的集成。
- 若希望一次性完成部署，可使用 `webchat-voice-full-stack`（依次部署后端和服务代理）。