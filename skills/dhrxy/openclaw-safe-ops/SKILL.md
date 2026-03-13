---
name: openclaw-safe-ops
description: 通过执行飞行前备份（preflight backups）、变更后的健康检查（post-change health checks）以及提供回滚指导（rollback guidance）来保护高风险的 OpenClaw 操作。这些措施适用于以下场景：重启/启动/停止网关（gateway restart/start/stop）、设置/取消设置配置（config set/unset）、安装/更新/卸载插件（plugin install/update/uninstall），以及编辑 openclaw.json 文件。
---
# OpenClaw 安全操作指南

## 适用场景

在执行任何高风险的 OpenClaw 操作之前，请使用本指南：

- `openclaw gateway restart|start|stop|install|uninstall|run|status`
- `openclaw config set|unset`
- `openclaw plugins install|update|uninstall|enable|disable`
- 手动编辑 `~/.openclaw/openclaw.json` 文件

## 安全工作流程

1. 在进行更改之前，先创建备份：
   - `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json/manual.$(date +%Y%m%d-%H%M%S).bak`
2. 运行所需的命令。
3. 立即进行验证：
   - `openclaw channels status --probe`
   - `openclaw status --deep`
4. 如果验证失败，立即回滚：
   - `cp ~/.openclaw/openclaw.json.bak ~/.openclaw/openclaw.json`
   - `openclaw gateway restart`
   - `openclaw status --deep`

## 推荐的命令封装工具

对于本地终端操作，建议使用以下脚本：

- `./scripts/openclaw-safe.sh <openclaw args...>`

该脚本会自动为高风险操作备份配置文件，执行健康检查，并在操作失败时进行回滚。

## 操作结果记录要求

在完成高风险操作后，需记录以下信息：

- 执行的命令
- 使用的备份路径
- 健康检查的结果
- 是否需要回滚