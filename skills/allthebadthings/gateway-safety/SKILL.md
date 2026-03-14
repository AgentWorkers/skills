---
name: gateway-safety
description: **安全地更新 OpenClaw 网关配置（openclaw.json）**：该功能支持自动验证、备份配置文件，并在配置错误时提供 30 秒的回滚机制。每当代理需要修改网关设置、端口、提供者凭据或网络绑定时，请使用此功能，以确保不会因配置错误而导致会话数据永久丢失。
license: MIT
---
# 网关安全

此安全机制确保对 OpenClaw 网关配置的任何修改都能安全地进行。它通过验证网关是否能够成功重启，来防止出现“死循环”和会话永久丢失的情况。

## 核心规则

1. **必须使用脚本**：切勿直接编辑 `~/.openclaw/openclaw.json` 文件。始终使用提供的 `safe-gateway-update.sh` 脚本。
2. **防循环策略**：如果脚本连续失败 3 次，它将创建一个 `GATEWAY_LOCKOUT` 文件。如果该文件存在，则**停止所有操作**并等待 Kevin 的指示。切勿尝试绕过锁定机制。
3. **备份意识**：脚本会自动备份配置文件，但对于关键更改，需要手动验证 `~/.openclaw/openclaw.json.known-good` 文件是否是最新的。

## 使用方法

要更新网关配置：

1. 准备新的配置 JSON 文件（例如，保存在 `/tmp/new_config.json` 中）。
2. 执行安全脚本：
   ```bash
   [SKILL_PATH]/scripts/safe-gateway-update.sh /tmp/new_config.json [timeout_seconds]
   ```
3. 脚本将执行以下操作：
   - 验证 JSON 语法是否正确。
   - 备份当前配置。
   - 应用新的配置并重启网关。
   - 检查是否收到“RPC probe: ok”的成功响应。
   - 如果健康检查失败或超时，则恢复到之前的配置。

## 作者信息
由 Kevin Smith 和 Rook (Orbit Smith) 于 2026 年 3 月编写。