# 🛡️ MaclawPro 安全工具

**专为 OpenClaw 设计的全面 macOS 安全监控工具**

## 该工具的功能是什么？

该工具提供了 52 多项专业的 macOS 安全监控功能，包括：

- 📹 **摄像头监控**：实时查看哪些应用程序正在使用您的摄像头
- 🎤 **麦克风监控**：实时监控麦克风的使用情况
- 🔥 **防火墙状态**：确认您的 Mac 是否启用了防火墙
- 🔐 **VPN 检查器**：检测 VPN 连接状态
- 📡 **WiFi 扫描器**：分析 WiFi 安全性（WPA2/WPA3）
- 🔌 **端口扫描器**：列出所有开放的网络端口
- 🛑 **应用拦截器**：立即拦截可疑应用程序（仅限 Pro 版本）

## 何时使用该工具？

当您需要执行以下操作时，请使用该工具：
- 检查是否有应用程序在秘密使用您的摄像头或麦克风
- 核实 Mac 的安全设置（防火墙、VPN）
- 扫描开放的端口或 WiFi 漏洞
- 实时监控系统安全状况

## 示例命令

```
User: Check if anyone is using my camera
Skill: ✅ CAMERA INACTIVE - No apps currently using your camera

User: Is my firewall on?
Skill: ✅ FIREWALL ENABLED - Your Mac is protected!

User: Check VPN status
Skill: ⚠️ VPN INACTIVE - Your traffic is NOT protected
```

## 使用要求

- **仅支持 macOS**（使用 macOS 特有的命令）
- **所需权限**：exec、fs.read、network
- **基本功能无需 API 密钥**

## 安装方法

```bash
npm install openclaw-macos-security
```

或者通过 OpenClaw 安装：
```bash
openclaw skills install openclaw-macos-security
```

## 可用命令

- `camera-status`：检查摄像头使用情况
- `microphone-status`：检查麦克风使用情况
- `firewall-status`：查看防火墙配置
- `vpn-checker`：检测 VPN 连接状态
- `open-ports`：列出所有监听端口
- `wifi-scanner`：分析 WiFi 安全性
- `block-app <name>`：拦截可疑应用程序

## 隐私与安全保障

✅ **所有监控数据仅存储在您的 Mac 上**，不会发送到外部服务器
✅ **开源项目**：代码托管在 GitHub 上
✅ **由认证的安全专家开发**

## 升级至 MaclawPro Pro

Pro 版本提供更高级的功能：
- 实时警报（通过 Telegram、Email 或 Slack 发送）
- 带有分析功能的 Web 控制面板
- 自动威胁拦截
- 24/7 全天候后台监控

👉 [maclawpro.com/pricing](https://maclawpro.com/pricing)

## 技术支持

- **npm 包**：[openclaw-macos-security](https://www.npmjs.com/package/openclaw-macos-security)
- **GitHub 仓库**：[drg3nz0/maclaw-openclaw-skill](https://github.com/drg3nz0/maclaw-openclaw-skill)
- **官方网站**：[maclawpro.com](https://maclawpro.com)

---

**专业的 macOS 安全监控工具**