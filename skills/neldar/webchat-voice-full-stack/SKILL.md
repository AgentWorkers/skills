---
name: webchat-voice-full-stack
description: One-step full-stack installer for OpenClaw WebChat voice input with local speech-to-text. Deploys faster-whisper STT backend plus HTTPS/WSS WebChat proxy with mic button in one command. Voice transcription, microphone input, speech recognition — no recurring API costs, runs locally after initial model download. Combines faster-whisper-local-service and webchat-voice-proxy. Keywords: voice input, microphone, WebChat, speech to text, STT, local transcription, whisper, full stack, one-click, voice button.
---

# WebChat 语音全栈

这是一个元安装器（meta-installer），它按照正确的顺序协调两个独立的技能（skills）的安装：

1. **`faster-whisper-local-service`** — 本地语音转文字（STT, Speech-to-Text）后端服务（运行在 127.0.0.1:18790 上）
2. **`webchat-voice-proxy`** — 用于 WebChat 控制界面的 HTTPS/WSS 代理服务以及麦克风按钮功能

## 先决条件

在运行此元安装器之前，必须先安装以下两个技能：

```bash
clawdhub install faster-whisper-local-service
clawdhub install webchat-voice-proxy
```

系统还必须满足以下要求：
- Python 3.10 或更高版本
- `gst-launch-1.0`（来自操作系统包的 GStreamer 工具）
- 首次运行时需要互联网连接（模型文件大小约为 1.5 GB）

## 部署

```bash
bash scripts/deploy.sh
```

可选的配置参数（会传递给下游脚本）：

```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 TRANSCRIBE_PORT=18790 WHISPER_LANGUAGE=auto bash scripts/deploy.sh
```

## 功能说明（通过下游脚本实现）

该元安装器本身不包含部署逻辑，而是会调用每个子技能对应的 `deploy.sh` 脚本。这些脚本的具体功能如下：

### `faster-whisper-local-service` 的部署步骤：
- 在 `$WORKSPACE/.venv-faster-whisper/` 目录下创建一个 Python 虚拟环境
- 使用 pip 安装 `faster-whisper` 库（版本 1.1.1）
- 将 `transcribe-server.py` 文件写入 `$WORKSPACE/voice-input/` 目录
- 创建并启用 `openclaw-transcribe.service` 这个 systemd 用户服务
- 首次运行时从 Hugging Face 下载模型文件（模型文件大小约为 1.5 GB）

### `webchat-voice-proxy` 的部署步骤：
- 将 `voice-input.js` 和 `https-server.py` 文件复制到 `$WORKSPACE/voice-input/` 目录
- 在 WebChat 控制界面的 `index.html` 文件中插入 `<script>` 标签
- 在 `openclaw.json` 文件中添加 `gateway_controlUi.allowedOrigins` 列表，以允许来自 `webchat-voice-proxy` 的 HTTPS 请求
- 创建并启用 `openclaw-voice-https.service` 这个 systemd 用户服务
- 在 `~/.openclaw/hooks/voice-input-inject/` 目录下设置启动钩子
- 首次运行时自动生成自签名 TLS 证书

有关详细信息、安全注意事项和卸载说明，请参阅每个技能对应的 SKILL.md 文件。

## 验证部署结果

```bash
bash scripts/status.sh
```

## 卸载

需要分别卸载每个技能：

```bash
# Proxy (service, hook, UI injection, gateway config)
bash skills/webchat-voice-proxy/scripts/uninstall.sh

# Backend (service, venv)
systemctl --user stop openclaw-transcribe.service
systemctl --user disable openclaw-transcribe.service
rm -f ~/.config/systemd/user/openclaw-transcribe.service
systemctl --user daemon-reload
```

## 注意事项：
- 该元安装器仅用于简化部署流程，实际的功能实现都包含在两个子技能中。
- 如果尚未执行，请先仔细阅读这两个子技能的脚本说明。
- `WORKSPACE` 和 `SKILLS_DIR` 的路径可以通过环境变量进行配置（默认值分别为 `~/.openclaw/workspace` 和 `~/.openclaw/workspace/skills`）。