---
name: upgrade
description: >
  **安全可靠的 OpenClaw 升级方案，支持即时回滚功能**  
  适用于以下场景：  
  - 用户请求“升级 OpenClaw”  
  - 用户请求“更新 OpenClaw”  
  - 用户请求“检查更新”  
  **使用说明：**  
  仅用于 OpenClaw 安装的升级或更新操作，不适用于配置更改（请使用 `gateway config.patch`）或技能更新（请使用 `clawhub`）。  
  **注意事项：**  
  - 升级过程中会自动应用最新的功能和改进，但用户可以随时选择回滚到之前的版本。  
  - 请确保在升级前备份所有重要数据，以防万一。  
  **适用场景示例：**  
  - 当用户输入“upgrade openclaw”或“update openclaw”时，立即执行此脚本。  
  - 当用户询问“是否有更新可用”时，也请使用此脚本进行升级操作。  
  **总结：**  
  这是一个简单且可靠的 OpenClaw 升级工具，能够确保升级过程的稳定性和数据安全性，同时提供便捷的回滚机制。
---
# OpenClaw 安全升级

该升级过程通过一个原子命令完成。在遇到任何故障时，系统会自动执行回滚操作；即使网关重启，升级过程也能正常完成。

## 脚本内容

```bash
# From an agent session — ALWAYS set escape flag (ensures script survives gateway restart)
_UPGRADE_FORCE_ESCAPE=1 bash skills/upgrade/scripts/safe-upgrade.sh

# Force upgrade even if already on latest
_UPGRADE_FORCE_ESCAPE=1 bash skills/upgrade/scripts/safe-upgrade.sh --force

# Safe read-only checks (no escape needed)
bash skills/upgrade/scripts/safe-upgrade.sh --check      # Pre-flight only
bash skills/upgrade/scripts/safe-upgrade.sh --rollback    # Manual rollback
```

## 升级流程（一个命令，包含10个步骤）：

1. **Cgroup 逃逸**：通过 `systemd-run --user --scope` 重新执行脚本，以防止网关停止操作导致脚本终止。
2. 预升级检查：验证当前版本、检查磁盘空间以及是否存在可能破坏系统稳定性的更改。
3. 备份数据：备份 OpenClaw 安装包、配置文件、定时任务（cron jobs）以及 acpx 的自定义设置。
4. 使用 `npm i -g openclaw@latest` 安装最新版本的 OpenClaw。
5. 恢复 acpx 的配置设置（升级后，acpx 代理的自定义配置仍会保留）。
6. 重启网关（升级过程在独立的进程中执行，不会受到网关重启的影响）。
7. 等待网关恢复正常状态（可配置超时时间）；如果升级失败，系统会自动执行回滚操作。
8. 等待 WhatsApp 重新连接（超时时间非强制要求）。
9. 验证升级结果：确保版本正确且定时任务未受到影响；如果仍有问题，系统会自动执行回滚操作。
10. 记录升级结果（可选）；如果需要，还可以生成备份文件。

如果任何关键检查步骤失败，脚本会自动执行回滚操作，恢复系统的原始状态（包括安装包、配置文件和定时任务）。在关键操作阶段，系统会捕获并处理任何异常退出事件。

## 代理的工作流程：

1. 首先运行 `--check` 命令，并将输出结果展示给用户。
2. 通知用户：“正在启动升级过程，网关重启期间我将暂时离线。”
3. 执行升级操作（具体步骤见 **CODE_BLOCK_1___**；**请勿将升级过程的输出通过管道传输**，例如不要使用 `| tee` 或 `2>&1 | cat`）。升级脚本会将输出日志写入 `/tmp/upgrade-live.log` 文件。
4. 网关重启后，当前会话将结束，这是正常现象。
5. 重启后，新会话会检查以下内容：
   - `~/.openclaw/upgrade-result.json` 文件以获取升级状态。
   - `/tmp/upgrade-live.log` 文件以获取实时升级日志。
   - 如果升级成功，向用户报告结果并更新相关版本信息。
   - 如果升级失败，向用户说明问题原因（具体原因记录在 `upgrade-result.json` 文件中）。
   - 如果 `~/.openclaw/upgrade-backups/current/` 目录下没有备份文件，说明升级过程中脚本被意外终止，此时需要运行 `--rollback` 命令进行回滚。
6. 完整的升级日志记录在 `~/.openclaw/upgrade-last.log` 文件中。

## 备份内容：

- OpenClaw 安装包的压缩文件。
- 配置文件（`openclaw.json`）。
- 定时任务配置文件（`jobs.json`）。
- acpx 用户配置文件（`~/.acpx/config.json`，如果存在的话）。
- 与版本相关的元数据（包括版本信息、时间戳和定时任务记录）。

备份文件保存路径：`~/.openclaw/upgrade-backups/current/`。

## 结果文件：`~/.openclaw/upgrade-result.json`

```json
{
    "status": "success|rolled_back|rollback_failed|no_change|blocked",
    "from_version": "2026.3.2",
    "to_version": "2026.3.7",
    "message": "...",
    "timestamp": "...",
    "log": "~/.openclaw/upgrade-last.log"
}
```

## 为什么需要使用 Cgroup 逃逸机制？

OpenClaw 作为 systemd 服务运行。当代理执行升级脚本时，该脚本实际上是该服务所属 cgroup 内的一个子进程。`systemctl stop` 命令会向 cgroup 内的所有进程发送 SIGKILL 信号，这会导致升级脚本终止。由于无法捕获 SIGKILL 信号，因此需要使用 Cgroup 逃逸机制来确保脚本能够继续执行。

**重要提示：**
- **切勿直接运行 `gateway update.run` 命令**，请始终使用这个升级脚本。
- **从代理会话执行升级操作时，务必将 `_UPGRADE_FORCE_ESCAPE` 设置为 1**。
- acpx 的自定义设置会在升级过程中自动保留。
- 回滚操作会完全恢复系统的原始状态（包括安装包、配置文件、定时任务和 acpx 配置）。
- `--check` 命令可以随时安全地执行，不会对系统产生任何影响。
- 脚本会自动从配置文件中获取网关的端口信息（不会使用硬编码的默认值）。
- 如果工作区中存在 `golden-snapshot.sh` 或 `service-quick-check.py` 文件，系统会自动使用这些脚本；否则会忽略它们。