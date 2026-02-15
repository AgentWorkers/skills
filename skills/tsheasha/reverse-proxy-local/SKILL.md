---
name: ecto-connection
version: 1.0.0
description: 通过 Tailscale Funnel 将 OpenClaw 连接到互联网。当用户输入“connect with ecto”、“setup ecto connection”、“expose openclaw publicly”或“enable external access”时，请使用此功能。
metadata:
  openclaw:
    emoji: "🔌"
    author: "OpenClaw"
    commands:
      - connect
      - status
      - disconnect
---

# Ecto 连接功能

通过一个命令即可完成设置，使 OpenClaw 通过 Tailscale Funnel 接入互联网，并实现安全认证。

## 功能概述

1. **安装 Tailscale**（如果尚未安装）。
2. **使用您的 Tailscale 账户进行身份验证**。
3. **以适当的权限启动 Tailscale 服务**。
4. **启用 Funnel 功能，将端口 18789 公开暴露**。
5. **使用安全认证令牌配置 OpenClaw，并启用其 API 端点**。
6. **使用新的配置重新启动网关**。

## 使用方法

当用户输入 “connect with ecto” 或类似指令时，脚本将执行以下操作：

```bash
~/.openclaw/workspace/skills/ecto-connection/scripts/connect.sh
```

### 命令

**完整连接设置：**
```bash
./scripts/connect.sh
```

**检查状态：**
```bash
./scripts/status.sh
```

**断开连接（禁用 Funnel 功能）：**
```bash
./scripts/disconnect.sh
```

## 输出结果

成功连接后，脚本会输出以下信息：
- 公共访问地址：`https://<machine>.tail<xxxxx>.ts.net/v1/chat/completions`
- API 访问所需的认证令牌
- 一个示例 curl 命令

## 系统要求

- 安装了 Homebrew 的 macOS 系统
- 拥有 Tailscale 账户（可在 tailscale.com 免费注册）
- 具有 sudo 权限（用于启动 Tailscale 服务）

## 安全性

- 生成一个 32 字节的随机认证令牌。
- 所有 API 请求都需要使用该认证令牌。
- Funnel 功能使用 Tailscale 自动提供的 TLS 证书进行加密传输。
- 网关仅通过 Funnel 可以访问。

## 设置完成后

您可以使用与 OpenAI 兼容的 API 进行交互：

```bash
curl https://<your-url>/v1/chat/completions \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello!"}]}'
```

## 故障排除

**Funnel 功能无法使用？**
- 确保在您的 Tailscale 系统中启用了 Funnel 功能：https://login.tailscale.com/admin/machines
- 检查：`tailscale funnel status`

**认证错误？**
- 认证令牌存储在：`~/.openclaw/ecto-credentials.json` 文件中
- 重新生成令牌：`./scripts/connect.sh --regenerate-token`

**网关无响应？**
- 查看日志文件：`cat /tmp/openclaw-gateway.log`
- 重新启动网关：`./scripts/connect.sh --restart`