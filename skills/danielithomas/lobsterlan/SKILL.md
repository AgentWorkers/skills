---
name: lobsterlan
description: 在您的本地网络中与其他 OpenClaw 代理进行通信。当您需要向其他代理提问（同步操作）、委托任务（异步操作），或检查某个代理是否可用时，可以使用此功能。该功能支持同步聊天以及基于 Webhook 的异步任务委托。需要使用 `peers.json` 配置文件来指定代理的地址和令牌信息。
---
# LobsterLAN — 代理之间的通信

在您的局域网（LAN）中与其他 OpenClaw 代理进行通信。

## 设置

1. 将 `config/peers.example.json` 复制到 `config/peers.json`。
2. 填入对等节点的主机名、端口和令牌（token）。
3. 确保目标代理已启用所需的 API（详见下文）。
4. **设置安全的传输方式**（详见“网络传输”部分）。

## 目标代理所需的配置

- **同步请求**（用于聊天对话的完成）：
  ```jsonc
// Target agent's openclaw.json — keep bind as "loopback"!
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```

> ⚠️ **请勿将 `gateway.bind` 设置为 `"lan"`** — 如果网关暴露在非回环地址上且没有使用 TLS，OpenClaw 将拒绝启动。请改用安全的传输方式（详见下文）。

- **异步委托**（用于 Webhook）：
  ```jsonc
{
  "hooks": {
    "enabled": true,
    "token": "a-secure-shared-secret"
  }
}
```

## 网络传输

OpenClaw 网关默认设置为 `bind: loopback`，如果网关位于非回环地址上且未使用 TLS，将无法启动。因此，跨主机通信需要使用安全的传输层：

| 方法 | 复杂度 | 适用场景 |
|----------|-----------|----------|
| **SSH 隧道** ⭐ | 低 | 家用局域网、简单环境 |
| **反向代理（TLS）** | 中等 | 已安装 Caddy/nginx 的环境 |
| **Tailscale Serve** | 中等 | 多站点或远程代理 |

**对于简单的局域网环境，建议使用 SSH 隧道。** 两个网关都保持在回环地址上，SSH 隧道提供加密功能，且无需更改网关配置。

### SSH 隧道示例

将本地端口转发到远程代理的回环网关：
```bash
ssh -N -L 18790:127.0.0.1:18790 user@remote-agent-host
```

然后在 `peers.json` 中，将目标代理指向 `127.0.0.1:18790`（本地的隧道端点）。

为了实现持久化，可以使用带有 `Restart=always` 选项的 systemd 用户服务。完整的设置指南请参阅 `docs/setup.md`。

## 命令

### 请求（同步 — 等待回复）
```bash
scripts/lobsterlan.sh ask scotty "What is the CPU temperature?"
```
适用于需要立即获取答案的简单查询。

### 委托（异步 — 发送后无需关心后续流程）
```bash
scripts/lobsterlan.sh delegate scotty "Generate 5 zen wallpapers and push to the file share"
```
适用于需要长时间运行的任务。目标代理会独立执行任务。

### 状态检查
```bash
scripts/lobsterlan.sh status scotty
```

### 列出对等节点
```bash
scripts/lobsterlan.sh peers
```

## 代理使用方法（在 OpenClaw 中）

通过 `exec` 工具运行相关命令：
```bash
cd ~/.openclaw/workspace/skills/lobsterlan && scripts/lobsterlan.sh ask scotty "status report"
```

## 安全性

通信安全通过三层防护机制实现：
1. **网络层**：仅限局域网访问（防火墙阻止外部访问网关端口）。
2. **网关令牌**：每次请求时都需要进行身份验证。
3. **代理 ID 标头**（可选）：发送 `X-LobsterLAN-Agent` 以及代理的自身 ID。

网关令牌是真正的安全保障；代理 ID 标头则适用于需要明确身份验证的环境。

## 环境变量

- `LOBSTERLAN_CONFIG` — 对等节点配置文件的路径（默认值：`../config/peers.json`，相对于脚本文件的位置）