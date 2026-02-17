---
name: openclaw-update
description: 检查 OpenClaw 的更新情况，执行更新操作，并管理版本状态。该功能支持自动检查更新、版本对比以及 OpenClaw 代理平台的无缝更新。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["openclaw"] },
        "install":
          [
            {
              "id": "openclaw-update-skill",
              "kind": "skill",
              "path": "skills/openclaw-update",
              "label": "OpenClaw Update Skill",
            },
          ],
      },
  }
---
# OpenClaw 更新技能

这是一个用于检查和应用 OpenClaw 更新的技能。

## 命令

### 检查状态

查看当前的 OpenClaw 版本及可用的更新：

```bash
openclaw update status
openclaw update status --json
```

### 运行更新

将 OpenClaw 更新到最新版本：

```bash
openclaw update run
```

### 查看配置

查看当前的更新配置：

```bash
openclaw update config
```

## 使用场景

- **自动更新检查**：配置 cron 作业以定期检查更新
- **版本监控**：监控是否有新版本可用
- **安全更新**：在更新前检查以确保兼容性
- **更新历史**：追踪更新的应用时间

## 环境变量

- `OPENCLAW_UPDATE_CHECK_URL`：覆盖更新检查的 URL（可选）

## 示例工作流程

```bash
# Check for updates (human-readable output)
openclaw update status

# Check for updates (JSON output for automation)
openclaw update status --json

# If update available, apply it
openclaw update run
```

## 注意事项

- 需要安装 OpenClaw
- 支持语义版本控制以便进行版本比较
- 更新时提供详细的变更日志
- 如有需要，支持回滚（请参阅文档）