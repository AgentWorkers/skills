---
name: webchat-voice-proxy
description: Voice input and microphone button for OpenClaw WebChat Control UI. Adds a mic button to chat, records audio via browser MediaRecorder, transcribes locally via faster-whisper, and injects text into the conversation. Includes HTTPS/WSS reverse proxy, TLS cert management, and gateway hook for update safety. Fully local speech-to-text, no API costs. Keywords: voice input, microphone, WebChat, Control UI, speech to text, STT, local transcription, MediaRecorder, HTTPS proxy, voice button, mic button.
---

# WebChat语音代理

为OpenClaw WebChat设置一个可重启的语音处理堆栈（包括当前完善的麦克风/停止/计时器UI状态）：
- 在8443端口上提供HTTPS控制UI
- 将`/transcribe`请求代理到本地的faster-whisper服务
- 通过WebSocket将请求转发到网关（`ws://127.0.0.1:18789`）
- 将语音按钮相关的脚本注入到控制UI中

## 先决条件（必需）

此功能需要一个**本地的faster-whisper HTTP服务**。

默认配置：
- URL：`http://127.0.0.1:18790/transcribe`
- systemd用户服务：`openclaw-transcribe.service`

在部署前请进行验证：

```bash
systemctl --user is-active openclaw-transcribe.service
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:18790/transcribe -X POST -H 'Content-Type: application/octet-stream' --data-binary 'x'
```

如果缺少此依赖项，请先设置faster-whisper（包括模型加载和HTTP端点），然后再运行此功能。

相关功能：
- `faster-whisper-local-service`（后端必备功能）
- `webchat-voice-full-stack`（用于部署后端和代理的元安装工具）

## 工作流程

1. 确保转录服务存在并正在运行（`openclaw-transcribe.service`）。
2. 将`voice-input.js`文件部署到控制UI的资源目录中，并将相关脚本标签注入到`index.html`文件中。
3. 配置网关允许的请求来源地址。
4. 以持久化用户服务的方式运行HTTPS+WSS代理（`openclaw-voice-https.service`）。
5. 检查配对/令牌/来源地址相关的错误，并按顺序进行修复。

## 部署

自动检测主机IP地址并运行脚本：

```bash
bash scripts/deploy.sh
```

或者手动指定主机地址和端口：

```bash
VOICE_HOST=10.0.0.42 VOICE_HTTPS_PORT=8443 bash scripts/deploy.sh
```

此脚本是幂等的（多次运行不会产生不同结果）。

## 快速验证

运行以下命令进行验证：

```bash
bash scripts/status.sh
```

预期结果：
- 两个服务均处于活跃状态
- 脚本注入成功
- 响应状态码为`https:200`

## 常见问题解决方法

- 出现`404 /chat?...`错误：可能是HTTPS代理中的单页应用程序（SPA）回退逻辑缺失。
- 出现“origin not allowed”错误：请确保使用了正确的`VOICE_HOST`地址，并在`gateway.controlUi.allowedOrigins`配置中添加了相应的HTTPS来源地址。
- 出现“token missing”错误：尝试使用`?token=...`参数访问相关URL。
- 需要配对设备：通过`openclaw devices approve <requestId> --token <gateway-token>`命令批准待配对设备。
- 重启后麦克风功能失效：请确保证书路径是持久化的（不要使用`/tmp`目录）。
- 未收到转录结果：请先检查本地的faster-whisper服务是否正常运行。

有关详细命令，请参阅`references/troubleshooting.md`。