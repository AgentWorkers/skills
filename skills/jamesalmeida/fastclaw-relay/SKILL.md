---
name: fastclaw-relay
description: 将您的 OpenClaw 与 FastClaw iOS 应用程序连接起来。通过 Convex 云同步功能，在您的本地网关（Gateway）和 FastClaw 之间传递消息。无需进行端口转发或使用 VPN——只需完成配对即可开始使用。
---

# FastClaw 中继

通过 Convex 实时同步功能，将您的本地 OpenClaw Gateway 与 FastClaw iOS 应用程序连接起来。

## 工作原理

```
OpenClaw Gateway (local)  ←WebSocket→  fastclaw-relay  ←Convex→  FastClaw App (iOS)
```

1. 中继作为操作员客户端连接到您的本地 Gateway 的 WebSocket。
2. 消息通过 Convex（云端）实现双向同步。
3. FastClaw iOS 应用程序订阅 Convex 数据——无论用户身处何地均可使用该功能。

无需进行任何网络配置，双方均可主动发起连接。

## 设置

### 1. 安装该功能

```bash
clawhub install fastclaw-relay
```

### 2. 开始配对

```bash
openclaw fastclaw pair
```

系统会生成一个 QR 码，其中包含您的 Convex 部署 URL 和一次性的配对令牌。

### 3. 从 FastClaw 应用程序中扫描 QR 码

打开 FastClaw 应用程序 → 点击“连接” → 扫描 QR 码。配对完成。

## 配置

中继会从环境变量或 OpenClaw 配置文件中读取以下信息：

- `FASTCLAW_convEX_URL`：您的 Convex 部署 URL（在设置过程中提供）。
- `FASTCLAW_INSTANCE_ID`：该 OpenClaw 实例的唯一 ID（自动生成）。

这些配置信息会在首次配对后保存在 `~/.openclaw/fastclaw/config.json` 文件中。

## 架构

### Convex 数据结构

中继使用以下 Convex 数据表：

- **instances**：已注册的 OpenClaw 实例（包含 ID、名称、状态、最后访问时间）。
- **sessions**：从 Gateway 同步的聊天会话。
- **messages**：实现双向同步的单条消息。
- **pairingCodes**：用于 QR 配对的一次性代码（有效期为 5 分钟）。

### Gateway 连接

中继使用配置好的 gateway 令牌，通过 `ws://127.0.0.1:18789` 连接到本地 Gateway 的 WebSocket。中继以“操作员”（operator）角色的身份进行通信，具备 `operator.read` 和 `operator.write` 的操作权限。

### 消息传输流程

**用户通过 FastClaw 应用程序发送消息：**
1. 应用程序将消息写入 Convex 的 `messages` 表。
2. 中继通过 Convex 订阅功能实时接收更新。
3. 中继将消息转发到 Gateway 的 WebSocket。
4. Gateway 处理消息并返回响应。
5. 中继捕获响应并将其写入 Convex。
6. 应用程序实时接收响应。

**接收到的消息（来自 WhatsApp、Telegram 等渠道）：**
1. Gateway 在任何通道上接收消息。
2. 中继通过 Gateway 的 WebSocket 监测会话更新。
3. 中继将新消息同步到 Convex。
4. 应用程序实时显示这些消息。

## 安全性

- 配对令牌在 5 分钟后失效。
- 所有 Convex 通信均通过 TLS 协议进行加密。
- 实例令牌存储在本地文件 `~/.openclaw/fastclaw/` 中。
- 中继仅同步消息内容，不传输 API 密钥、令牌或配置信息。
- Gateway 令牌不会离开本地机器。
- 该功能采用开源代码，便于全面审计。

## 故障排除

### 中继无法连接
- 检查 Gateway 是否正在运行：`openclaw gateway status`。
- 确认 gateway 令牌是否正确：查看 `~/.openclaw/config.yaml` 文件。

### 消息无法同步
- 检查中继进程是否正常运行：`openclaw fastclaw status`。
- 确认 Convex 部署是否正常：`npx convex dashboard`。

### 重新配对
- 运行 `openclaw fastclaw pair --reset` 命令生成新的配对令牌。