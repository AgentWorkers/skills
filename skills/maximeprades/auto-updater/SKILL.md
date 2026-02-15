---
name: auto-updater
description: "每天自动更新 Clawdbot 及所有已安装的技能。该过程通过 cron 任务执行：系统会检查是否有更新，然后应用这些更新，并向用户发送更新内容的摘要信息。"
metadata: {"version":"1.0.0","clawdbot":{"emoji":"🔄","os":["darwin","linux"]}}
---

# 自动更新技能

通过每日自动检查，确保您的 Clawdbot 及其技能始终保持最新状态。

## 功能概述

该技能会设置一个每日运行的 cron 作业，用于：

1. 更新 Clawdbot 本身（通过 `clawdbot doctor` 或包管理器）
2. 更新所有已安装的技能（通过 `clawdhub update --all`）
3. 向您发送更新总结信息

## 设置方法

### 快速入门

让 Clawdbot 自动设置自动更新功能：

```
Set up daily auto-updates for yourself and all your skills.
```

或者手动添加 cron 作业：

```bash
clawdbot cron add \
  --name "Daily Auto-Update" \
  --cron "0 4 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Run daily auto-updates: check for Clawdbot updates and update all skills. Report what was updated."
```

### 配置选项

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| 更新时间 | 上午 4:00 | 更新运行的时间（使用 `--cron` 进行修改） |
| 时区 | 系统默认值 | 通过 `--tz` 设置 |
| 更新通知方式 | 主会话窗口 | 更新总结信息的发送位置 |

## 更新流程

### Clawdbot 的更新过程

对于通过 **npm/pnpm/bun** 安装的技能：
```bash
npm update -g clawdbot@latest
# or: pnpm update -g clawdbot@latest
# or: bun update -g clawdbot@latest
```

对于通过 **git checkout** 安装的技能：
```bash
clawdbot update
```

更新完成后，请务必运行 `clawdbot doctor` 以应用相应的迁移脚本。

### 技能的更新过程

该功能会检查所有已安装的技能，并在发现有新版本时进行更新。

## 更新总结格式

更新完成后，您将收到如下格式的消息：

```
🔄 Daily Auto-Update Complete

**Clawdbot**: Updated to v2026.1.10 (was v2026.1.9)

**Skills Updated (3)**:
- prd: 2.0.3 → 2.0.4
- browser: 1.2.0 → 1.2.1  
- nano-banana-pro: 3.1.0 → 3.1.2

**Skills Already Current (5)**:
gemini, sag, things-mac, himalaya, peekaboo

No issues encountered.
```

## 手动命令

- 检查更新情况（不执行任何操作）：
```bash
clawdhub update --all --dry-run
```

- 查看当前技能版本：
```bash
clawdhub list
```

- 查看 Clawdbot 的版本：
```bash
clawdbot --version
```

## 故障排除

### 更新失败的原因及解决方法

- **更新未运行**：确认 cron 作业是否已启用（检查配置文件中的 `cron.enabled`）；确认 Gateway 是否持续运行；检查 cron 作业是否存在（使用 `clawdbot cron list` 命令）。
- **更新失败**：更新总结中会包含失败原因。常见解决方法包括：
  - **权限问题**：确保 Gateway 用户具有写入技能目录的权限；
  - **网络问题**：检查网络连接是否正常；
  - **包冲突**：运行 `clawdbot doctor` 以诊断问题。

### 禁用自动更新

- 删除 cron 作业：
```bash
clawdbot cron remove "Daily Auto-Update"
```

- 或者在配置文件中临时禁用自动更新功能：
```json
{
  "cron": {
    "enabled": false
  }
}
```

## 参考资源

- [Clawdbot 更新指南](https://docs.clawd.bot/install/updating)
- [ClawdHub 命令行工具](https://docs.clawd.bot/tools/clawdhub)
- [Cron 作业相关文档](https://docs.clawd.bot/cron)