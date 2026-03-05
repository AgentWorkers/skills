---
name: clawpulse
description: 配置并维护 OpenClaw 的 ClawPulse 集成，包括使用令牌保护的通信机制、确保访问安全（符合 Tailscale 的安全标准）、设置 iOS 终端的相关默认参数（如令牌信息），以及解决与 ATS（Authentication, Tracking, and Sync）相关的故障问题。此操作适用于新机器的设置、令牌的定期更新、ClawPulse 连接问题的排查，以及启用状态响应中的辅助信息（如助手名称、令牌信息及用户思维数据）等功能。
---
# ClawPulse

## 概述
通过 OpenClaw 和 ClawPulse 构建一个安全的状态通信桥梁，并以最少的手动操作来维持其正常运行。

## 依赖项
- 必需：`openclaw`, `python3`
- 可选（仅用于远程访问）：`tailscale`

## 快速工作流程
1. 运行 `scripts/setup_clawpulse_bridge.sh`（默认为干运行模式），生成/确认令牌并打印端点设置。
2. 只有在准备就绪时才启动/重启桥梁：`scripts/setup_clawpulse_bridge.sh --apply`。
3. 默认情况下，绑定地址为 `0.0.0.0`，适用于通过 Tailscale 或局域网连接的移动设备。
4. 设置脚本会默认生成 QR 码（在 macOS 上会显示 PNG 图片）。
5. 向用户提供 ClawPulse 应用程序所需的端点和令牌。
6. 如果同步失败，请参考故障排除指南。

## 第一步 — 启动桥梁
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
桥梁的响应应至少包含以下信息：

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
在 ClawPulse 中使用以下信息进行连接：
- URL：`http://<tailscale-or-lan-ip>:8787/health`
- 令牌：从设置脚本中获得的承载令牌
- 默认轮询间隔：10 秒

## 故障排除
- 在 iOS 设备上遇到 HTTP 阻拦问题：请确保应用程序的 `Info.plist` 中包含用于开发的 ATS 异常处理设置，或使用 HTTPS 协议。
- 401 错误：令牌不匹配；请重新生成令牌并重新应用。
- 403 禁止访问：源 IP 地址不是本地或 Tailscale 的地址；请确认设备已连接到 Tailscale。
- 超时问题：检查桥梁进程和网络连接情况。
- 显示名称错误：请更新 `workspace/IDENTITY.md` 文件中的名称字段。

## 令牌更新
使用 `ROTATE_TOKEN=1` 重新运行设置脚本：

```bash
ROTATE_TOKEN=1 bash scripts/setup_clawpulse_bridge.sh
```

立即在 ClawPulse 中更新令牌。