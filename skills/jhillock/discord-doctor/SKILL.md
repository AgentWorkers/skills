---
name: discord-doctor
description: 针对 Discord 机器人、Gateway、OAuth 令牌以及旧配置问题，提供快速诊断和修复方案。该方案会检查连接状态、令牌的有效期，并清理旧的 Clawdis 相关文件。
metadata: {"clawdbot":{"emoji":"🩺","os":["darwin","linux"],"requires":{"bins":["node","curl"]}}}
---

# Discord Doctor

这是一个用于快速诊断和修复 Discord/Gateway 可用性问题、OAuth 令牌问题以及旧版 Clawdis 配置冲突的工具。

## 使用方法

```bash
# Check status (diagnostic only)
discord-doctor

# Check and auto-fix issues
discord-doctor --fix
```

## 检查内容

1. **Discord 应用**：Discord 桌面应用是否正在运行（可选，用于监控）
2. **Gateway 进程**：Clawdbot 的 Gateway 守护进程是否正在运行
3. **Gateway HTTP**：Gateway 是否在端口 18789 上响应请求
4. **Discord 连接**：机器人是否已成功连接到 Discord（通过 `clawdbot health` 检查）
5. **Anthropic OAuth**：您的 OAuth 令牌是否有效或已过期
6. **旧版 Clawdis**：检测可能导致冲突的旧版启动服务（launchd）和配置文件
7. **最近的活动**：显示最近的 Discord 会话记录

## 自动修复功能

当使用 `--fix` 参数运行时，它可以执行以下操作：

- **启动 Gateway**（如果未运行）
- **安装缺失的 npm 包**（如 `discord.js`、`strip-ansi`）
- **修复依赖关系后重启 Gateway**
- **删除旧版的启动服务（`com.clawdis.gateway.plist`）
- **备份旧版配置文件**（将 `~/.clawdis` 文件夹移动到 `~/.clawdis-backup`）

## 常见问题及解决方法

| 问题 | 自动修复操作 |
|-------|-----------------|
| Gateway 未运行 | 在端口 18789 上启动 Gateway |
| 缺少 npm 包 | 运行 `npm install` 并安装所需包 |
| Discord 连接断开 | 重启 Gateway 以重新连接 |
| OAuth 令牌过期 | 显示重新认证的提示 |
| 旧版启动服务 | 删除旧的 `com.clawdis.gateway.plist` 文件 |
| 旧版配置文件 | 将旧配置文件移动到 `~/.clawdis-backup` |

## OAuth 令牌问题

如果出现“访问令牌已过期”的提示，请运行以下命令：
```bash
cd ~/Clawdis && npx clawdbot configure
```
然后选择“Anthropic OAuth (Claude Pro/Max)”进行重新认证。

## 旧版 Clawdis 迁移

如果您从 Clawdis 升级到了 Clawdbot，可能会遇到导致 OAuth 令牌冲突的旧版文件：

- **旧版启动服务**：`~/Library/LaunchAgents/com.clawdis.gateway.plist`
- **旧版配置目录**：`~/.clawdis/`

运行 `discord-doctor --fix` 可以自动清理这些旧文件。

## 示例输出

```
Discord Doctor
Checking Discord and Gateway health...

1. Discord App
   Running (6 processes)

2. Gateway Process
   Running (PID: 66156, uptime: 07:45)

3. Gateway HTTP
   Responding on port 18789

4. Discord Connection
   Discord: ok (@Clawdis) (321ms)

5. Anthropic OAuth
   Valid (expires in 0h 45m)

6. Legacy Clawdis
   No legacy launchd service
   No legacy config directory

7. Recent Discord Activity
   - discord:group:123456789012345678 (21h ago)

Summary
All checks passed! Discord is healthy.
```