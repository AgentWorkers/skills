---
name: webchat-voice-full-stack
description: >
  OpenClaw WebChat 的一站式全栈安装程序，支持本地语音转文本功能。该程序依次整合了三个核心组件：  
  1. **本地语音转文本（STT）后端**：实现更快速的语音转文本处理；  
  2. **HTTPS/WSS 反向代理**：确保 WebChat 通信的安全性和稳定性；  
  3. **语音用户界面（Voice UI）**：提供麦克风控制功能。  
  安装程序包含以下特性：  
  - **一键式部署**：用户可轻松完成整个系统的安装；  
  - **Push-to-Talk 功能**：支持一键开启/关闭语音通话；  
  - **连续录音快捷键**：方便用户进行长时间录音；  
  - **VU（Voice Activity Meter）**：实时显示语音活动状态；  
  - **多语言支持**：界面可切换为英文、德文或中文；  
  - **透明部署**：所有配置更改均可在用户层面进行，且可逆；  
  - **系统级管理**：通过 systemd 管理用户服务；  
  - **安全机制**：支持 HTTPS 和 WSS 协议；  
  - **无额外费用**：初次模型下载后无需支付任何额外 API 费用。  
  **关键词**：  
  语音输入、麦克风、WebChat、语音转文本（STT）、本地转录、一键部署、语音按钮、Push-to-Talk（PTT）、键盘快捷键、国际化（i18n）、HTTPS、WSS。
---
# WebChat 语音全栈

这是一个元安装程序（meta-installer），它按照正确的顺序协调三个独立的技能（skills）的安装：

1. **`faster-whisper-local-service`** — 本地语音转文本（STT）后端服务（运行在 127.0.0.1:18790 上）
2. **`webchat-https-proxy`** — 用于控制界面的 HTTPS/WSS 反向代理服务，支持 WebSocket 和语音转文本功能
3. **`webchat-voice-gui`** — 提供麦克风按钮、音量显示、键盘快捷键以及多语言支持（i18n）的 WebChat 用户界面

## 先决条件

在运行此元安装程序之前，必须先安装以下三个技能：

```bash
npx clawhub install faster-whisper-local-service
npx clawhub install webchat-https-proxy
npx clawhub install webchat-voice-gui
```

系统还必须满足以下要求：
- Python 3.10 或更高版本
- 安装了 `gst-launch-1.0`（来自操作系统包的 GStreamer 工具）
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

该元安装程序本身不包含部署逻辑，而是会调用每个子技能对应的 `deploy.sh` 脚本来执行部署任务：

### 第一步：faster-whisper-local-service
- 创建 Python 虚拟环境（venv），并安装 `faster-whisper==1.1.1` 版本
- 编写 `transcribe-server.py` 脚本，实现输入验证（包括特殊字符检测和文件大小限制）
- 创建 systemd 用户服务 `openclaw-transcribe.service`
- 首次运行时下载模型文件（模型文件大小约为 1.5 GB）

### 第二步：webchat-https-proxy
- 将 `https-server.py` 脚本复制到工作目录
- 将该服务的 HTTPS 地址添加到 `gateway.controlUi.allowedOrigins` 配置中
- 创建 systemd 用户服务 `openclaw-voice-https.service`
- 自动生成自签名 TLS 证书（支持 TLS 1.2 协议）

### 第三步：webchat-voice-gui
- 将 `voice-input.js` 脚本复制到控制界面中，并在界面中插入 `<script>` 标签
- 为确保更新的安全性，设置启动时的钩子（hook）
- 提供可选的语言选择功能

有关详细信息、安全注意事项和卸载说明，请参阅每个技能对应的 SKILL.md 文件。

## 安全性设计

由于这是一个元安装程序，它仅负责协调各个子技能的安装，并执行最低限度的本地配置更改：
- **持久性**：通过创建用户级别的 systemd 服务，确保 STT 和代理服务在系统重启后仍然可用（`openclaw-transcribe`、`openclaw-voice-https`）
- **用户界面**：在控制界面中插入 `<script>` 标签以启用语音输入功能
- **网关兼容性**：将新的 HTTPS 地址添加到 `gateway_controlUi.allowedOrigins` 配置中

安全性特点：
- 所有更改都有文档记录，并且可以通过卸载脚本进行恢复
- 无需 root 或 sudo 权限（仅限普通用户操作）
- 除了已记录的服务外，没有隐藏的后台任务或数据泄露行为
- 不存在任何数据输出或泄露的风险

## 验证

```bash
bash scripts/status.sh
```

## 卸载

请按相反的顺序分别卸载每个技能：

```bash
# 1. Voice GUI (hook, UI injection, workspace files)
bash skills/webchat-voice-gui/scripts/uninstall.sh

# 2. HTTPS Proxy (service, gateway config, certs)
bash skills/webchat-https-proxy/scripts/uninstall.sh

# 3. STT Backend (service, venv)
systemctl --user stop openclaw-transcribe.service
systemctl --user disable openclaw-transcribe.service
rm -f ~/.config/systemd/user/openclaw-transcribe.service
systemctl --user daemon-reload
```

## 注意事项：
- 该元安装程序只是一个便捷的封装工具，所有实际的功能都由三个子技能实现。
- 在运行之前，请仔细阅读每个子技能的脚本和安全说明。
- `WORKSPACE` 和 `SKILLS_DIR` 的路径可以通过环境变量进行配置。