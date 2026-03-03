---
name: ansible-skills-admin
description: Manage ansible skill lifecycle across gateways: source-of-truth edits, mirror sync, deployment verification, and drift cleanup.
---

# Ansible 技能管理

当用户需要创建、更新或部署 Ansible 技能，或者解决规范仓库（canonical repo）与运行时技能镜像（runtime skill mirrors）之间的不一致问题时，请使用此功能。

## 原则与标准

- 规范仓库（位于 `~/code`）是所有更改的黄金来源。
- 运行时镜像（位于 `~/.openclaw/workspace/skills/*`）是部署的目标。
- 除非用户明确要求，否则切勿将仅针对运行时的更改推送到规范仓库。

## 标准工作流程

1. 首先编辑规范仓库中的技能内容。
2. 提交并推送更改到规范仓库。
3. 将更改拉取到运行时镜像（包括本地环境和 VPS）。
4. 验证运行时镜像中的技能内容。
5. 仅当运行时环境需要重新加载时，才重启相关服务。

## 必需的检查项

- 规范仓库的状态：
  `git -C ~/code/openclaw-skill-ansible status -b --short`
- 运行时镜像的完整性：
  `git -C ~/.openclaw/workspace/skills/ansible rev-parse --short HEAD`
- VPS 镜像的完整性：
  `ssh jane-vps "docker exec jane-gateway sh -lc 'git -C /home/node/.openclaw/workspace/skills/ansible rev-parse --short HEAD'"`

## 异常处理（Drift Triage）

如果运行时镜像与规范仓库存在差异：

- 如果更改是故意且有益的，将其合并到规范仓库并提交。
- 如果更改是意外的，将运行时镜像重置为规范仓库的最新版本（HEAD）。
- 修复问题后，重新验证本地和 VPS 镜像的完整性。

## 信息通知要求

在部署技能更改时，需向用户发送状态更新：

- 部署开始时发送 `ACK` 消息。
- 每次服务更新时发送 `IN_PROGRESS` 消息。
- 完成或遇到问题时发送 `DONE/BLOCKED` 消息，并附上验证结果。

请使用 `conversation_id` 来标识所有更新，以便用户能够跟踪整个流程。