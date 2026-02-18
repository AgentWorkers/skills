---
name: openclaw-update
description: 检查 OpenClaw 的更新情况，执行更新操作，并管理版本状态。该系统能够自动检测更新、进行版本对比，并实现 OpenClaw 代理平台的无缝升级。
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

这是一项用于检查和应用 OpenClaw 更新的技能。

## 命令

### 检查状态

查看当前的 OpenClaw 版本及可用的更新：

```bash
openclaw update status
openclaw update status --json
```

### 运行更新（使用 pnpm）

使用 pnpm 更新 OpenClaw（适用于通过 pnpm 安装的 OpenClaw）：

```bash
# Check current version
pnpm list -g openclaw

# Update to latest version
pnpm add -g openclaw

# Restart gateway after update
openclaw gateway restart
```

### 网关管理

更新完成后重启 OpenClaw 网关：

```bash
openclaw gateway restart
openclaw gateway status
```

## pnpm 升级工作流程

对于通过 pnpm 安装的 OpenClaw：

```bash
# 1. Check current version
pnpm list -g openclaw

# 2. Update to latest
pnpm add -g openclaw

# 3. Restart gateway
openclaw gateway restart

# 4. Verify update
openclaw update status
```

## 使用场景

- **自动更新检查**：配置 cron 作业以定期检查更新
- **版本监控**：监控是否有新版本可用
- **安全更新**：在更新前检查以确保兼容性
- **更新历史记录**：追踪更新的应用时间
- **pnpm 工作流程**：专为基于 pnpm 的安装环境设计的特殊命令

## 环境变量

- `OPENCLAW_UPDATE_CHECK_URL`：用于覆盖更新检查的 URL（可选）

## 示例工作流程

```bash
# Check for updates (human-readable output)
openclaw update status

# Check for updates (JSON output for automation)
openclaw update status --json

# For pnpm installations, use pnpm to update
pnpm add -g openclaw

# Restart gateway after update
openclaw gateway restart
```

## 注意事项

- 需要已安装 OpenClaw
- 支持语义版本控制以便进行版本比较
- 更新时提供详细的变更日志
- 如有需要，支持回滚操作（请参阅文档）
- pnpm 的安装路径：`/home/rothcold/.local/share/pnpm/pnpm`