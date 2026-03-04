---
name: ansible-skills-admin
description: "管理 Ansible 技能的生命周期，涵盖各个环节：源代码的编辑与更新、镜像同步、部署验证以及潜在差异的清理工作。"
---
# Ansible 技能管理

当用户需要创建、更新、部署或同步 Ansible 技能内容（包括其规范版本和运行时版本）时，请使用此流程。

## 原始数据来源政策

- 规范版本存储在 `~/code` 目录下的仓库中，是所有更改的权威来源。
- 运行时版本的镜像存储在 `~/.openclaw/workspace/skills/*` 目录中，用于部署。
- 除非用户明确要求，否则切勿将仅针对运行时的更改推送到规范版本仓库。

## 标准工作流程

1. 首先编辑规范版本的 Ansible 技能仓库。
2. 提交并推送更改。
3. 将更改拉取到运行时版本的镜像中（包括本地环境和 VPS）。
4. 验证所有镜像之间的数据一致性。
5. 仅在运行时环境需要重新加载时重启相关服务。

## 必需的检查项

- 规范版本的仓库状态：
  `git -C ~/code/openclaw-skill-ansible status -b --short`
- 运行时版本的镜像状态：
  `git -C ~/.openclaw/workspace/skills/ansible rev-parse --short HEAD`
- VPS 上的镜像状态：
  `ssh jane-vps "docker exec jane-gateway sh -lc 'git -C /home/node/.openclaw/workspace/skills/ansible rev-parse --short HEAD'"`

## 异常处理机制

如果运行时版本的镜像与规范版本不一致：

- 如果更改是有意且有益的，将其合并到规范版本仓库中并提交。
- 如果更改是意外的，将运行时版本的镜像重置为规范版本的最新状态。
- 在问题解决后，重新验证所有镜像的一致性。

## 信息通知要求

在部署技能更改时，需向相关人员发送以下状态更新：

- `ACK`：表示部署开始。
- `IN_PROGRESS`：表示部署正在进行中。
- `DONE` 或 `BLOCKED`：表示部署已完成或遇到问题，并附上相应的验证证据。

所有相关更新都应使用 `conversation_id` 进行标识。