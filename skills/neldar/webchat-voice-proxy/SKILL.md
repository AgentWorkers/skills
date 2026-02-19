---
name: webchat-voice-proxy
description: Voice input and microphone button for OpenClaw WebChat Control UI. Adds a mic button to chat, records audio via browser MediaRecorder, transcribes locally via faster-whisper, and injects text into the conversation. Includes HTTPS/WSS reverse proxy, TLS cert management, and gateway hook for update safety. Fully local speech-to-text, no API costs. Keywords: voice input, microphone, WebChat, Control UI, speech to text, STT, local transcription, MediaRecorder, HTTPS proxy, voice button, mic button.
---

# WebChat语音代理

为OpenClaw WebChat设置一个可在重启后仍保持正常运行的语音处理栈（包括当前完善的麦克风/停止/计时器UI功能）：

- 在端口8443上提供HTTPS控制界面。
- 将 `/transcribe` 请求代理到本地的faster-whisper服务。
- 通过WebSocket将请求转发到网关（`ws://127.0.0.1:18789`）。
- 将语音按钮相关的JavaScript脚本注入到控制界面中。

## 先决条件（必需）

此功能需要一个本地的faster-whisper HTTP服务。

**默认配置：**
- URL：`http://127.0.0.1:18790/transcribe`
- systemd用户服务：`openclaw-transcribe.service`

**部署前请验证：**

```bash
systemctl --user is-active openclaw-transcribe.service
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18790/transcribe -X POST -H 'Content-Type: application/octet-stream' --data-binary 'x'
```

如果缺少此依赖项，请先安装faster-whisper服务（包括模型加载和HTTP端点配置），然后再执行此功能。

**相关功能：**
- `faster-whisper-local-service`（后端依赖项）
- `webchat-voice-full-stack`（用于部署后端和代理服务的元安装工具）

## 工作流程：
1. 确保转录服务已安装并正在运行（`openclaw-transcribe.service`）。
2. 将 `voice-input.js` 文件部署到控制界面的资源文件夹中，并将其JavaScript脚本注入到 `index.html` 文件中。
3. 配置网关以允许来自外部HTTPS接口的请求。
4. 以持久化用户服务的形式运行HTTPS+WSS代理（`openclaw-voice-https.service`）。
5. 检查并解决配对、令牌和来源地址相关的错误。

## 部署：
（自动检测主机IP地址的部署方式：）

```bash
bash scripts/deploy.sh
```

**或手动设置主机地址和端口：**

```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 bash scripts/deploy.sh
```

此脚本是幂等的（多次执行不会产生不同结果）。

## 快速验证：
运行以下命令：

```bash
bash scripts/status.sh
```

**预期结果：**
- 两个服务均处于活跃状态。
- JavaScript脚本已成功注入到控制界面中。
- 浏览器返回状态码 `https:200`。

## 常见问题及解决方法：
- **404 /chat?...**：可能是HTTPS代理中的单页应用（SPA）回退机制未正确配置。
- **“origin not allowed”**：确保在部署时使用了正确的 `VOICE_HOST` 值，并在网关配置中添加了相应的HTTPS来源地址。
- **令牌缺失**：尝试通过 `openclaw devices approve <requestId> --token <gateway-token>` 命令批准待配对的设备。
- 重启后麦克风功能失效：证书路径必须保持持久化（不能使用临时文件夹 `/tmp`）。
- 无转录结果：首先检查本地的faster-whisper服务是否正常工作。

**详细操作指南请参阅：`references/troubleshooting.md`**

## 该功能会修改的系统文件：
在安装此功能之前，请注意 `deploy.sh` 脚本会对系统进行的以下更改：

| 修改内容 | 修改路径 | 所作操作 |
|---|---|---|
| 控制界面HTML | `<npm-global>/openclaw/dist/control-ui/index.html` | 添加用于加载 `voice-input.js` 的 `<script>` 标签 |
| 控制界面资源文件 | `<npm-global>/openclaw/dist/control-ui/assets/voice-input.js` | 复制麦克风按钮相关的JavaScript文件 |
| 网关配置 | `~/.openclaw/openclaw.json` | 在 `gateway.controlUi.allowedOrigins` 中添加允许的HTTPS来源地址 |
| systemd服务 | `~/.config/systemd/user/openclaw-voice-https.service` | 创建并启用持久的HTTPS代理服务 |
| 网关启动钩子 | `~/.openclaw/hooks/voice-input-inject/` | 安装启动钩子，以便在系统更新后重新注入JavaScript脚本 |
| 工作区文件 | `~/.openclaw/workspace/voice-input/` | 复制 `voice-input.js` 和 `https-server.py` 文件 |
| TLS证书 | `~/.openclaw/workspace/voice-input/certs/` | 在首次运行时自动生成自签名证书 |

**注意：** 被注入的 `voice-input.js` 脚本会在控制界面中运行，并与聊天输入功能进行交互。在部署前请仔细审查该脚本的源代码。

## 卸载：
要完全恢复系统到安装前的状态，请执行以下操作：

```bash
bash scripts/uninstall.sh
```

执行此命令后：
1. 停止并删除 `openclaw-voice-https.service` 服务。
2. 删除网关的启动钩子。
3. 从控制界面中移除 `voice-input.js` 文件，并恢复 `index.html` 文件中的脚本注入内容。
4. 从网关配置中删除允许的HTTPS来源地址。
5. 重启网关。

工作区文件（`voice-input/` 目录）和TLS证书默认会被保留。如需同时删除这些文件，请执行相应的命令：

```bash
rm -rf ~/.openclaw/workspace/voice-input
```

请注意：卸载此功能不会影响faster-whisper后端服务——如需卸载该服务，请单独使用 `faster-whisper-local-service` 命令进行操作。