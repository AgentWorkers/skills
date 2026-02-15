---
name: ops-dashboard
description: 收集运行状态相关的信息（如磁盘使用情况、Git仓库的状态、最近的提交记录以及系统资源使用情况），这样你就可以在不需要手动执行多项检查的情况下，直接回答“Clawdy基础设施的运行状况如何？”这个问题。
---

# 运维仪表盘 (Ops Dashboard)

## 概述

`ops-dashboard` 提供了一个命令行工具（`scripts/ops_dashboard.py`），用于显示以下信息的快照：
- 工作区的磁盘使用情况（总容量与可用空间）以及存储可用性。
- 当前分支的 Git 状态和最新提交记录。
- 系统负载平均值以及顶级目录的大小，帮助您了解数据集中的热点区域。

在部署前检查系统健康状况、推送更新或帮助遇到工作区运行缓慢问题的团队成员时，可随时使用此工具。

## 命令行用法

- `python3 skills/ops-dashboard/scripts/ops_dashboard.py --show summary`：显示磁盘使用情况、Git 状态和顶级目录信息。
- `--show resources`：添加系统负载平均值以及最近 Git 提交的详细信息（包括作者和提交内容）。
- `--workspace /path/to/workspace`：允许您将工具指向另一个克隆的仓库或项目。
- `--output json`：以 JSON 格式输出报告，以便其他脚本使用。

## 各指标说明

- **磁盘使用情况**：显示 `/`, `/mnt/ramdisk` 以及工作区内其他已挂载分区的 `df` 结果。
- **Git 状态**：判断当前分支是否干净，列出已暂存/未暂存的文件，并显示最近三次提交的哈希值和作者信息。
- **系统负载平均值**：记录 1 分钟、5 分钟和 15 分钟的系统负载情况，帮助您将系统性能下降与资源消耗高峰关联起来。
- **目录大小**：突出显示工作区根目录下的三个最大文件目录，以便您发现数据增长的趋势。

## 示例命令

```bash
python3 skills/ops-dashboard/scripts/ops_dashboard.py --show summary --workspace /path/to/workspace (or omit to use the current directory)
```

此命令在开始高风险操作之前，会显示当前仓库的基本运行状况，包括 Git 状态和磁盘使用情况。

## 参考资料

- `references/ops-dashboard.md`：解释了各指标的含义以及如何解读诸如高磁盘使用率或过时分支等警报信息。

## 资源链接

- **GitHub**：https://github.com/CrimsonDevil333333/ops-dashboard
- **ClawHub**：https://www.clawhub.ai/skills/ops-dashboard