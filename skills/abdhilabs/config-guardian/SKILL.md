---
name: config-guardian
description: 验证并保护 OpenClaw 配置的更新（文件格式为 openclaw.json 或通过 openclaw config set/apply 命令进行配置）。在更改网关配置、模型、通道、代理、工具、会话或路由时，请务必使用此功能。系统会在重启前执行备份操作、验证配置文件的结构，并确保配置能够安全地回滚（即恢复到之前的有效状态）。
---

# 配置守护者（Config Guardian）

## 概述
每当编辑 `~/.openclaw/openclaw.json` 文件或运行 `openclaw config set/apply` 命令时，请使用此工作流程。该流程可防止配置错误、创建备份文件、验证配置是否符合规范，并支持配置回滚功能。

## 工作流程（每次操作均需执行）
1. **预检查**
   - 确认所需的更改内容及其范围。
   - 检查是否存在敏感信息（如令牌、凭据等）。

2. **备份**
   - 运行 `scripts/backup_config.sh` 命令以生成带有时间戳的配置备份文件。

3. **更改前验证**
   - 运行 `scripts/validate_config.sh` 命令验证配置。
   - 如果验证失败，立即停止操作并报告错误。

4. **应用更改**
   - 对于较小的更改，建议使用 `openclaw config set <路径> <值>` 命令。
   - 对于复杂的更改，请直接修改文件，并尽量减少文件内容的差异。

5. **更改后验证**
   - 再次运行 `scripts/validate_config.sh` 命令进行验证。
   - 如果验证失败，使用 `scripts/restore_config.sh` 命令从备份中恢复配置。

6. **重启系统（仅经明确批准后执行）**
   - 如果更改需要重启系统，请先获得批准。
   - 使用 `openclaw gateway restart` 命令重启系统。

## 规则限制
- **未经用户明确批准，严禁** 重启系统或应用配置更改。
- **严禁** 删除配置键或重新排列配置结构。
- **每次编辑前** 必须创建备份文件。
- 如果对配置规范不确定，请运行 `openclaw doctor --non-interactive` 命令；遇到错误时立即停止操作。

## 相关脚本
- `scripts/backup_config.sh` — 生成带有时间戳的配置备份文件。
- `scripts/validate_config.sh` — 通过 `openclaw doctor` 工具验证配置是否合法。
- `scripts/diff_config.sh` — 比较当前配置与备份文件的内容差异。
- `scripts/restore_config.sh` — 从备份文件中恢复配置。

## 配置验证
- 使用 `openclaw doctor --non-interactive` 命令进行配置规范验证。
- 该命令会检查配置是否符合 OpenClaw 系统实际使用的规范。
- 如果发现未知的配置键、无效的数据类型或安全问题，系统会发出警告。