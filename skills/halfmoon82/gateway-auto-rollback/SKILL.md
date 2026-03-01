---
name: gateway-auto-rollback
description: >
  OpenClaw Gateway的自动配置回滚机制  
  该机制提供三层保护：修改前的备份、修改后的验证以及故障发生时的自动回滚。它包括一个文件监控守护进程、JSON格式的验证功能、Gateway健康检查以及基于SHA256哈希值的文件备份。在修改`openclaw.json`或其他关键配置文件时，使用该机制可以防止意外导致的系统故障，并确保配置更改过程中不会出现任何服务中断（零停机时间）。
---
# 开放式Claw网关自动回滚机制

**开放式Claw网关的三层配置保护机制**——确保您的配置设置永远不会出错。

## 功能概述

该机制通过以下方式自动保护您的开放式Claw配置文件：
1. **修改前备份**：在每次修改之前，会生成基于SHA256哈希值的文件内容地址快照。
2. **修改后验证**：检查JSON语法是否正确，并对网关状态进行检测。
3. **自动回滚**：如果验证失败，会立即恢复到之前的配置状态。

## 使用场景

- 在修改`openclaw.json`、`exec-approvals.json`或`skills.json`文件之前。
- 在执行自动化配置更改时（例如通过cron作业或脚本）。
- 在开发过程中作为安全保障机制。
- 当您希望确保错误的配置不会导致代理程序崩溃时。

## 快速入门

### 一次性检查（手动编辑前）

```bash
python3 gateway-auto-rollback.py
```

此步骤会初始化备份目录，验证当前配置，并记录状态。

### 监控模式（后台守护进程）

```bash
python3 gateway-auto-rollback.py --watch &
```

每隔3分钟监控一次关键配置文件。如果连续3次检测到配置正常，守护进程将自动退出。

## 工作原理

```
Before Modification        During              After Modification
       ↓                    ↓                        ↓
  Backup + Hash  ───→  Execute Change  ───→  JSON Validate + Health Check
       │                                          │
       └──────────────────────────────────────→ Auto-rollback on failure
```

### 受保护的文件

| 文件名 | 说明 |
|------|-------------|
| `openclaw.json` | 主网关配置文件 |
| `exec-approvals.json` | 命令执行权限配置文件 |
| `skills.json` | 技能注册表文件 |

### 备份命名规则

备份文件存储在`~/.openclaw/backup/`目录下，文件名采用基于SHA256哈希值的唯一格式。

```
openclaw.json.20260301_053612.a1b2c3d4.bak
                 ↑ timestamp    ↑ SHA256 prefix (dedup)
```

## API参考

### Python函数

```python
from gateway_auto_rollback import (
    pre_modification_check,   # Call before modifying config
    post_modification_verify, # Call after modifying config
    create_backup,            # Manual backup creation
    validate_json,            # JSON syntax validation
    check_gateway_health,     # Gateway health probe
    rollback_to_backup,       # Manual rollback
    watch_config_files,       # Start watch daemon
)
```

### 修改前流程

```python
from pathlib import Path

config = Path.home() / ".openclaw" / "openclaw.json"

# Returns backup path on success, False on failure
backup = pre_modification_check(config)

# ... make your changes ...

# Validates and auto-rolls back if needed
success = post_modification_verify(config, backup)
```

### 监控模式详细信息

- 守护进程每3分钟轮询一次配置文件。
- 通过SHA256哈希值比较来检测文件是否被修改。
- 检测到修改后自动创建备份。
- 每次修改后都会验证JSON格式并检查网关状态。
- 如果连续3次检测到配置正常，守护进程将自动退出。
- 所有事件都会被记录到`~/.openclaw/logs/config-modification.log`日志文件中。

## 与Cron集成

您可以使用Cron定期检查配置文件的完整性：

```bash
# Cron job example: check every hour
0 * * * * python3 /path/to/gateway-auto-rollback.py
```

或者直接使用开放式Claw内置的Cron任务来执行这些检查。

## 手动回滚

如果您需要手动恢复配置，请按照以下步骤操作：

```bash
# List available backups (newest first)
ls -lt ~/.openclaw/backup/ | head -10

# Restore a specific backup
cp ~/.openclaw/backup/openclaw.json.20260301_053612.a1b2c3d4.bak \
   ~/.openclaw/openclaw.json

# Restart Gateway
openclaw gateway restart

# Verify
curl -s http://127.0.0.1:18789/api/health
```

## 测试

运行附带的测试套件以验证该机制是否正常工作：

```bash
bash test-rollback-mechanism.sh
```

测试内容包括：
- 备份目录的存在性。
- JSON格式的验证。
- SHA256哈希值的计算。
- 备份文件的创建与恢复过程。
- 监控守护进程的状态。
- 日志文件的完整性。
- 脚本执行的权限设置。

## 日志记录

所有操作事件都会被记录到`~/.openclaw/logs/config-modification.log`文件中：

```
[2026-03-01 05:37:00] INFO: ✅ 备份创建: openclaw.json.20260301_053612.a1b2c3d4.bak
[2026-03-01 05:37:01] INFO: ✅ 修改验证通过
[2026-03-01 05:40:00] WARN: ⚠️ 检测到修改: openclaw.json
[2026-03-01 05:40:01] ERROR: JSON 验证失败 — 触发回滚
```

## 系统要求

- Python 3.8及以上版本。
- 开放式Claw网关必须正在运行（用于进行状态检测）。
- 无需安装额外的Python包（仅需要标准库）。

## 文件结构

```
gateway-auto-rollback/
├── SKILL.md                      # This file
├── _meta.json                    # ClawHub metadata
├── gateway-auto-rollback.py      # Main script (backup/validate/rollback/watch)
└── test-rollback-mechanism.sh    # Test suite
```