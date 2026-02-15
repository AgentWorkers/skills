# shellphone-gateway

这是一个专用的 WebSocket 网关，用于将 iOS 设备连接到您的 AI 代理服务器。无需使用 Telegram 或 Discord，也无需任何中间件。

## 功能介绍

ShellPhone 与 OpenClaw Gateway 结合使用，可在您的 iPhone 和自托管的 AI 机器人之间建立一条直接、加密的通信通道：

- **隐私保护优先**：所有消息都不会传输到第三方服务器。
- **完全自托管**：该服务运行在您的本地硬件上。
- **自动识别 LLM（Large Language Model）**：如果您拥有本地 LLM，无需任何配置即可使用该服务。
- **免费的语音合成/语音识别功能**：通过 ScrappyLabs 提供（无需注册账户）。

## 快速入门

### 1. 运行网关

```bash
# Docker (recommended)
git clone https://github.com/loserbcc/openclaw-gateway.git
cd openclaw-gateway
docker compose up

# Or Python
pip install openclaw-gateway
openclaw-gateway
```

### 2. 下载 iOS 应用程序

加入 TestFlight 测试计划：https://testflight.apple.com/join/BnjD4BEf

### 3. 连接设备

扫描来自 `http://localhost:8770/setup` 的 QR 码，或手动输入连接信息：
- **URL**：`wss://your-server:8770/gateway`
- **Token**：在网关启动时会在屏幕上显示。

## 相关链接

- **TestFlight**：https://testflight.apple.com/join/BnjD4BEf
- **GitHub 仓库**：https://github.com/loserbcc/openclaw-gateway
- **ScrappyLabs**：https://scrappylabs.ai

## 许可证

采用 MIT 许可协议——您可以自由使用该软件，无需遵守任何额外限制。