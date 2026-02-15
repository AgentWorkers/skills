---
name: memory-keeper
description: 将所有重要的代理上下文文件（如 MEMORY.md、memory/*.md、AGENTS.md、SOUL.md 等）复制并创建快照，存放到一个专门的归档目录或代码仓库中。当您需要备份代理的配置文件、上下文数据或内存信息时，可以使用此方法，以便在维护、数据恢复或迁移至其他主机时使用这些备份文件。
---

# Memory Keeper

Memory Keeper 是一个简单的命令行工具（CLI），它将 OpenClaw 的关键配置文件（每日内存日志、DESCRIPTION.md 文件、用户信息文档以及心跳提醒文件）复制到安全的存档目录中，并可选择性地将这些文件提交到配置好的 Git 仓库中。该工具保持文件原有的结构，因此您可以轻松地恢复或查看文件的历史记录，而无需下载整个工作区的数据。

## 主要功能

- **快照功能**：将 `memory/*.md`、`MEMORY.md`、`AGENTS.md`、`SOUL.md`、`USER.md`、`TOOLS.md`、`HEARTBEAT.md` 及其他可选文件复制到存档路径中，同时保留目录结构。
- **兼容 Git**：如果目标存档是一个 Git 仓库，Memory Keeper 可以初始化该仓库、创建提交记录，并将更改推送到远程分支（可通过 CLI 参数进行配置）。
- **便携性**：适用于任何平台；只需将 `--workspace` 参数指向包含这些文件的目录根目录即可使用该工具。

## 开始使用

```bash
python3 skills/memory-keeper/scripts/memory_sync.py --target ~/clawdy-memories --commit --message "Sync up" --remote https://github.com/your-org/clawdy-memories.git --push
```

有关配置技巧、自动化方案和故障排除指南，请参阅 `references/usage.md`。

## 资源链接

- **GitHub 仓库**：https://github.com/CrimsonDevil333333/memory-keeper
- **ClawHub 文档**：https://www.clawhub.ai/skills/memory-keeper