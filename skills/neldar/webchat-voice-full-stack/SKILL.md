---
name: webchat-voice-full-stack
description: OpenClaw WebChat 语音输入的一键式全栈安装程序，支持本地语音转文本功能。该安装程序可通过一个命令快速部署 faster-whisper STT 后端服务以及基于 HTTPS/WSS 协议的 WebChat 代理，并提供麦克风按钮。支持“按住说话”（Push-to-Talk）功能，并可通过键盘快捷键（Ctrl+Space 用于 PTT，Ctrl+Shift+M 用于连续录音）切换模式。具备实时音量指示器（VU meter），提供中英文、德文等多语言本地化界面，在安装过程中可交互式选择语言。无需支付额外的 API 使用费用，模型下载完成后（约 1.5GB 大小）即可实现完全本地化运行。该工具集成了 faster-whisper-local-service 和 webchat-voice-proxy 两大功能。关键词：语音输入、麦克风、WebChat、语音转文本（STT）、本地转录、按住说话（Push-to-Talk）、键盘快捷键、多语言支持（i18n）。
---
# WebChat Voice Full Stack

这是一个元安装器（meta-installer），它按照正确的顺序协调两个独立的技能（skills）的安装：

1. **`faster-whisper-local-service`** — 本地语音转文本（STT, Speech-to-Text）后端服务（运行在 `127.0.0.1:18790` 上，使用 HTTP 协议）
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
- 首次运行时需要网络连接（模型文件大小约为 1.5 GB）

## 部署

```bash
bash scripts/deploy.sh
```

可选的配置参数（会传递给下游脚本）：

```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 TRANSCRIBE_PORT=18790 WHISPER_LANGUAGE=auto bash scripts/deploy.sh
```

## 功能说明（通过下游脚本实现）

该元安装器本身不包含部署逻辑，而是会调用每个子技能对应的 `deploy.sh` 脚本。以下是这些脚本的具体功能：

### `faster-whisper-local-service` 的部署流程：
- 在 `$WORKSPACE/.venv-faster-whisper/` 目录下创建 Python 虚拟环境
- 通过 pip 安装 `faster-whisper` 库（版本为 1.1.1）
- 将 `transcribe-server.py` 文件写入 `$WORKSPACE/voice-input/` 目录
- 创建并启用 `openclaw-transcribe.service` 这个 systemd 用户服务
- 首次运行时从 Hugging Face 下载模型文件（模型文件大小约为 1.5 GB）

### `webchat-voice-proxy` 的部署流程：
- 将 `voice-input.js` 和 `https-server.py` 文件复制到 `$WORKSPACE/voice-input/` 目录
- 在 WebChat 控制界面的 `index.html` 文件中插入 `<script>` 标签
- 在 `openclaw.json` 文件中添加 `gateway.controlUi.allowedOrigins` 列表，以允许来自 `webchat-voice-proxy` 的 HTTPS 请求
- 创建并启用 `openclaw-voice-https.service` 这个 systemd 用户服务
- 在 `~/.openclaw/hooks/voice-input-inject/` 目录下添加启动钩子
- 首次运行时自动生成自签名 TLS 证书

有关详细信息、安全注意事项以及卸载说明，请参阅每个技能对应的 SKILL.md 文件。

## 验证部署结果

```bash
bash scripts/status.sh
```

## 卸载

需要分别卸载这两个技能：

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
- 该元安装器仅起到简化安装流程的作用，所有实际功能都由两个子技能实现。
- 如果尚未执行，请先仔细阅读这两个子技能对应的脚本。
- `WORKSPACE` 和 `SKILLS_DIR` 的路径可以通过环境变量进行配置（默认值分别为 `~/.openclaw/workspace` 和 `~/.openclaw/workspace/skills`）。