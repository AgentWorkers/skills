---
name: agent-lifecycle-manager
description: "在节点上管理完整的 OpenClaw 代理生命周期操作：创建/注册代理、配置通道绑定、继承凭据、批准配对、归档和删除代理、刷新状态仪表板以及记录生命周期变更日志。适用于用户需要新接入代理、重新配置现有代理、退役/归档/删除代理，或维护代理状态信息及生命周期审计记录的场景。"
---
# 代理生命周期管理器

使用此技能可对 OpenClaw 代理执行可重复、错误率较低的生命周期操作。

## 工作流程

1. 收集所需输入参数
2. 运行相应的生命周期操作（创建、配置、归档、删除或检查代理状态）
3. 验证代理的运行状态（使用 `openclaw status` 和 `openclaw agents list` 命令）
4. 刷新仪表板数据
5. 记录生命周期操作的日志

在删除代理之前，务必先将其归档，并获取用户的明确确认。

## 各操作所需的输入参数

- **创建代理并绑定到 Telegram 账号：**
  - `AGENT_ID`
  - `TELEGRAM_TOKEN`
  - 可选参数：`WORKSPACE`（默认值：`~/.openclaw/workspace-<AGENT_ID>`）

- **配对确认（单独的步骤）：**
  - `AGENT_ID`
  - `PAIRING_CODE`（仅在用户向机器人发送 `/start` 命令后获取）

- **重新配置代理：**
  - `AGENT_ID`
  - 需要更改的字段（如模型、路由或频道令牌等）

- **归档/删除代理：**
  - `AGENT_ID`
  - 归档路径（默认为 `state/archive/<AGENT_ID>/`）

## 命令脚本

在执行特殊操作之前，请先阅读 `references/openclaw-agent-lifecycle-playbook.md` 文件。

为确保操作的确定性，请使用以下脚本：

- `scripts/create-telegram-agent.sh`：创建新的 Telegram 代理绑定
- `scripts/approve-telegram-pairing.sh`：批准代理配对请求
- `scripts/archive-agent.sh`：归档代理
- `scripts/delete-agent-safe.sh`：安全地删除代理
- `scripts/refresh-dashboard.sh`：刷新仪表板数据
- `scripts/lifecycle-log.sh`：记录生命周期操作日志

## 执行规则

- 尽量使用 OpenClaw 的命令行界面（CLI）进行操作，而非直接修改文件。
- 通过 `openclaw config get/set` 命令来配置代理绑定信息（避免盲目覆盖现有配置）。
- 默认情况下，绑定或配置更改后不会自动重启代理网关。
- 使用 `openclaw pairing approve <PAIRING_CODE> --channel telegram` 命令进行配对确认。
- 在成功归档代理之前，切勿直接删除代理。
- 对于删除操作，优先使用 `scripts/delete-agent-safe.sh` 脚本（包括归档验证、用户确认、资源清理及日志记录）。
- 每次完成生命周期操作后，务必刷新仪表板数据并记录操作日志。

## 最基本的操作后验证步骤

执行以下命令进行验证：

```bash
openclaw agents list --json
openclaw status --json
openclaw gateway status --json
```

确认以下内容：
- 目标代理是否存在（或已被成功删除）
- 配置的绑定信息及路由是否正确
- 代理网关是否正常运行，且 RPC 请求是否能够正常响应