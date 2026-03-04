---
name: ansible-skills-admin
description: "管理 Ansible 技能的生命周期，涵盖各个环节：源代码的编辑与更新、镜像同步、部署验证以及潜在差异的清理工作。"
---
# Ansible 技能管理

当用户需要创建、更新、部署或同步 Ansible 技能内容（包括其在规范仓库（canonical repo）和运行时环境（runtime）中的版本时，请使用此技能。

## 基本原则

- 规范仓库（`~/code`）是所有更改的权威来源。
- 运行时环境的镜像（位于 `~/.openclaw/workspace/skills/*`）是部署目标。
- 除非用户明确要求，否则切勿将仅针对运行时的更改推送到规范仓库。

## 标准工作流程

1. 首先编辑规范仓库中的代码。
2. 提交并推送更改。
3. 将更改拉取到运行时环境的镜像中（包括本地和虚拟专用服务器（VPS）。
4. 验证各个镜像之间的内容是否一致。
5. 仅当运行时环境需要重新加载时，才重启相关服务。

## 必需的检查项

- 规范仓库的状态：
  `git -C ~/code/openclaw-skill-ansible status -b --short`
- 运行时环境的镜像状态：
  `git -C ~/.openclaw/workspace/skills/ansible rev-parse --short HEAD`
- VPS 镜像的状态：
  `ssh jane-vps "docker exec jane-gateway sh -lc 'git -C /home/node/.openclaw/workspace/skills/ansible rev-parse --short HEAD'"`

## 异常处理机制

如果运行时环境中的镜像与规范仓库中的内容不一致：

- 如果更改是故意进行的且具有实际意义，请将更改合并到规范仓库并提交。
- 如果更改是意外发生的，请将运行时环境的镜像恢复到规范仓库的最新版本。
- 在问题解决后，重新验证本地和 VPS 镜像的状态。

## 信息通知要求

在部署技能更改时，需要向相关人员发送以下状态更新：

- `ACK`：部署开始时
- `IN_PROGRESS`：每次更新运行时环境时
- `DONE` 或 `BLOCKED`：更新完成后，并附上验证结果

所有相关更新都应使用 `conversation_id` 进行标识。