---
name: cerberus-agent-foundry
description: "适用于 OpenClaw 的生产级多代理架构套件。该套件提供了隔离的代理工作空间、控制平面编排功能、结构化的任务生命周期管理、经过校验和（checksum）验证的邮件通信机制以及可审计的事件日志记录。适用于需要实现具有安全边界、异步协作和操作治理机制的团队领导（Team Leader）与专业代理（specialist agents）协同工作的场景。"
---
# Cerberus 多代理控制平面

这是一个用于构建、管理和运营 OpenClaw 中本地多代理团队的专业蓝图。它提供了一套经过优化的协议栈，以实现角色隔离、任务编排、异步任务传递以及审计功能。

## 快速启动

1. 将蓝图安装到目标路径：
   - `bash scripts/install_blueprint.sh /path/to/your/system`
2. 验证任务板：
   - `python3 /path/to/your/system/scripts/taskctl.py list`
3. 验证邮件箱：
   - 发送消息：`python3 /path/to/your/system/scripts/mailboxctl.py send --task-id TSK-000 --sender team-lead --receiver coder --correlation-id CORR-001 --body "ACK protocol"`
   - 回复消息：`python3 /path/to/your/system/scripts/mailboxctl.py status --message-id MSG-0001 --to ACK --actor coder`

## 该蓝图提供的功能

- 为每个代理提供严格的工作区隔离（`agents/*/workspace`）
- 统一的控制平面（`control-plane/tasks`、`control-plane/mailbox`、`control-plane/logs`）
- 任务状态机工具（`taskctl.py`）
- 带有校验和功能的邮件箱协议（`mailboxctl.py`）
- 控制平面下的共享内存层（`control-plane/shared-memory`）

## 核心规则（必须遵守）

1. 禁止使用共享的代理工作区。
2. 仅使用 `control-plane/mailbox` 进行代理间的通信。
3. 团队负责人是邮件箱内容的唯一清理权限。
4. 部署任何操作都需要明确的人类审批。

## 参考资料

- 请阅读 `references/operations-checklist.md` 以了解部署和审计检查的相关信息。
- 请阅读 `assets/blueprint/docs/protocol-v1.md` 以了解协议细节。