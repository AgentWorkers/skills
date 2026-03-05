---
name: clawpulse
description: 配置并维护 OpenClaw 的 ClawPulse 集成，包括使用令牌保护的状态桥接（token-protected status bridge）、Tailscale 安全访问（Tailscale-safe access）、iOS 终端/令牌的默认设置，以及解决 ATS（Authentication, Authorization, and Session）/认证/同步（auth/sync）相关问题。此配置适用于新机器的设置、令牌的轮换、ClawPulse 连接性的修复，以及启用状态响应中的助手名称（assistant name）、令牌（token）和元数据（metadata）功能。
---
# ClawPulse

## 概述
通过 OpenClaw 与 ClawPulse 建立一个安全的状态通信通道，并以最少的手动操作来维持其正常运行。

## 依赖项
- 必需：`openclaw`、`python3`
- 可选（仅限远程访问）：`tailscale`

## 快速工作流程
1. 运行 `scripts/setup_clawpulse_bridge.sh`（默认为 dry-run 模式），生成/确认令牌并打印端点设置。
2. 只有在准备就绪时才启动/重启通信通道：`scripts/setup_clawpulse_bridge.sh --apply`。
3. 默认情况下，通信通道的绑定地址为 `0.0.0.0`，适用于通过 Tailscale 或局域网连接的移动设备。
4. 设置脚本会默认生成 QR 码（在 macOS 上可用时会显示 PNG 图片）。
5. 向用户提供 ClawPulse 应用程序所需的端点和令牌。
6. 如果同步失败，请参考故障排查指南。

## 第一步 — 启动通信通道
运行：

```bash
# Dry-run: generate token/server file and print settings (no background process)
bash scripts/setup_clawpulse_bridge.sh

# Start service (remote-ready default + QR)
bash scripts/setup_clawpulse_bridge.sh --apply

# Optional local-only mode (hardened)
BIND_HOST=127.0.0.1 bash scripts/setup_clawpulse_bridge.sh --apply
```

预期输出：
- 端点地址（本地或 Tailscale 格式）
- 承载令牌
- 绑定主机/端口以及日志路径

## 第二步 — 验证响应内容
通信通道的响应应至少包含以下信息：

```json
{
  "online": true,
  "assistantName": "OpenClaw",
  "workStatus": "工作中",
  "tokenUsage": {"prompt": 1, "completion": 2, "total": 3},
  "thought": "..."
}
```

## 第三步 — 配置应用程序
在 ClawPulse 中使用以下信息：
- URL：`http://<tailscale-or-lan-ip>:8787/health`
- 令牌：从设置脚本中获得的承载令牌
- 默认轮询间隔：5 秒（更及时的响应）

## 监控模式（推荐）
将监控端点作为公共访问端点使用，将通信通道作为内部数据源。

```bash
# Start/restart monitor (reads bridge and applies anti-flap state machine)
bash scripts/setup_clawpulse_monitor.sh --apply
```

然后使用从脚本输出或 QR 码中获取的监控端点和令牌来配置应用程序，而不是使用通信通道的令牌。

## 故障排查
- 在 iOS 设备上遇到 HTTP 阻止问题：确保应用程序的 `Info.plist` 中设置了 ATS 异常处理（用于开发模式），或者使用 HTTPS 协议。
- 401 认证错误：令牌不匹配；请重新生成令牌并重新应用。
- 403 禁止访问错误：源 IP 地址不是本地的或不在 Tailscale 网络范围内；请确认设备已连接到 Tailscale。
- 超时问题：检查通信通道的运行状态以及网络连接情况。
- 显示名称错误：更新 `workspace/IDENTITY.md` 文件中的名称字段。

## 令牌更新
使用 `ROTATE_TOKEN=1` 重新运行设置脚本：

```bash
ROTATE_TOKEN=1 bash scripts/setup_clawpulse_bridge.sh
```

立即在 ClawPulse 中更新令牌。