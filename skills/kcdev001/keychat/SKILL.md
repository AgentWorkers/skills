---
name: keychat
description: "安装 Keychat：这是一个专为 OpenClaw 代理设计的、基于 Signal 协议的、具有自主 E2E 加密功能的消息传递工具。该工具通过 Nostr 中继进行通信。当用户需要为他们的 OpenClaw 代理添加 Keychat 功能或设置加密通信机制时，可以使用该工具。"
metadata: {"openclaw":{"emoji":"🔐","homepage":"https://github.com/keychat-io/keychat-openclaw"}}
---
# 安装 Keychat

```bash
openclaw plugins install @keychat-io/keychat
openclaw gateway restart
```

支持的平台：macOS（ARM/x64）、Linux（x64/ARM64）。

该插件会自动下载桥接程序（bridge binary），配置 `openclaw.json` 文件中的 `channels.keychat` 配置，并在首次启动时生成一个新的 Nostr 身份标识。

首次安装后，代理会将其 Keychat ID（格式为 `npub1...`）、联系信息链接以及 QR 码发送到用户的活跃聊天窗口中。

## 安全提示

在安装过程中，系统可能会显示两条警告信息，这两条警告都是正常的：

- **bridge-client.ts**：该文件用于生成用于 Signal 协议和 MLS 协议加密的 Rust 侧车程序（Keychat 的加密逻辑是用 Rust 实现的，需要通过桥接程序与 Node.js 进行交互）。
- **keychain.ts**：该文件将用户的身份标识信息存储在操作系统的密钥链中（macOS 的 Keychain 或 Linux 的 libsecret）以保障安全性。

## 升级

您可以在任何聊天窗口中向代理发送 “upgrade keychat” 命令，或者手动执行升级操作：

```bash
openclaw plugins install @keychat-io/keychat@latest
openclaw gateway restart
```

## 连接

安装完成后，用户可以将该代理添加为 Keychat 的联系人：

1. 打开 [Keychat 应用程序](https://keychat.io) → 点击 **添加联系人**。
2. 扫描代理的 QR 码，或输入代理的 npub（Public Key）。
3. 代理会自动接受请求并建立加密会话。

用户也可以随时向代理询问 “我的 Keychat ID 是什么”，以获取自己的 npub、联系信息链接以及 QR 码。

更多信息：[github.com/keychat-io/keychat-openclaw](https://github.com/keychat-io/keychat-openclaw)