---
name: config-guardian
description: 安全的 OpenClaw 配置更新功能，支持自动备份、验证和回滚操作。专为代理（agent）使用而设计，可防止无效的配置更新导致系统故障。
---
# 配置守护器（Config Guardian）

## 概述
**仅限代理（Agent）使用。** 提供安全的配置更新功能，包括自动备份、验证和回滚机制。可防止代理更新不存在的配置键或无效的值。

## 使用场景
每次需要更新 `openclaw.json` 时都应使用此工具。它能防止以下问题：
- 更新不存在的配置键
- 使用无效的值
- 因错误的配置导致系统故障

## 工作流程：原子性应用（Atomic Apply，默认设置）

所有配置更改均通过一个命令完成：

```bash
./scripts/atomic_apply.sh <config_path> <new_value>
# Example: ./scripts/atomic_apply.sh "agents.defaults.model.primary" "minimax-portal/MiniMax-M2.5"
```

**具体功能：**
1. 自动创建带有时间戳的备份文件
2. 通过 `openclaw config set <路径> <值>` 命令应用配置更改
3. 使用 `openclaw doctor --non-interactive` 进行验证
4. 如果验证失败，系统会自动回滚配置
5. 即使系统崩溃，该机制也能确保配置能够被正确回滚

**备份位置：**
```
~/.openclaw/config-guardian-backups/
```

## 使用注意事项：
- **严禁** 在未经用户明确批准的情况下重启系统或应用配置更改
- **务必** 使用 `atomic_apply.sh` 脚本
- 如果验证失败，系统会自动回滚配置，切勿强行继续操作

## 相关脚本：
| 脚本 | 功能 |
|--------|---------|
| `atomic_apply.sh` | 默认脚本，用于安全地应用配置更改 |
| `validate_config.sh` | 通过 `openclaw doctor` 进行配置验证 |
| `restore_config.sh` | 从备份文件中手动恢复配置 |