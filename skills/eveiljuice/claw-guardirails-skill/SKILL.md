---
name: guardrails-safe-tools
description: 通过 `safe_exec`、`safe_send` 和 `safe_action` 来强制执行受保护的执行操作。当任务可能需要运行 shell 命令、发送通道消息，或调用可能修改数据或状态的外部 API/操作时，应使用这些函数。
---
# Guardrails 安全工具

## 使用场景

在以下情况下应使用这些安全工具：
- 当请求可以执行 shell 命令或系统命令时；
- 当请求需要向外部渠道发送消息或帖子时；
- 当请求需要触发外部操作（如发送电子邮件、访问数据库、调用网关或执行自动化任务时）。

## 硬性规则
1. 必须使用 `safe_exec` 而不是原始的 `exec` 命令。
2. 必须使用 `safe_send` 而不是直接使用渠道发送工具。
3. 对于需要触发外部系统或 API 动作的场景，必须使用 `safe_action`。
4. 禁止使用任何可能破坏系统安全的工具来绕过安全防护机制。
5. 如果某个操作需要审批，请立即停止并等待明确的审批结果。

## 输入规范
- 在调用 `safe_exec` 时，必须提供尽可能精确的当前工作目录（`cwd`）。
- 如果可能，必须提供发送者、渠道或代理的相关信息。
- 命令参数必须明确列出，不要在 shell 命令中隐藏任何可能带来风险的参数。
- 对于 `safe_action`，如果可能的话，必须提供所需的资源信息。

## 工具接口规范

### `safe_exec`
仅在被授权后才能用于执行 shell 命令。

**预期输入格式：**
```json
{
  "command": "git",
  "args": ["status"],
  "cwd": "/workspace/project"
}
```

### `safe_send`
用于向外部渠道发送消息。

**预期输入格式：**
```json
{
  "channel": "telegram:ops-room",
  "message": "Deployment done",
  "channelType": "telegram"
}
```

### `safe_action`
用于执行那些既不是简单的 shell 命令也不是简单的聊天消息发送的操作。

**预期输入格式：**
```json
{
  "action": "gmail.delete_message",
  "payload": { "messageId": "..." },
  "resources": [
    { "kind": "unknown", "value": "email-api", "operation": "delete" }
  ]
}
```

## 错误处理机制
- `allow`：允许操作继续执行，并返回运行结果。
- `deny`：拒绝操作，并附带错误代码；禁止使用其他可能带来风险的工具重试。
- `require_approval`：提示需要审批，并等待用户通过 `/approve <id>` 或 RPC 请求进行审批。

## 建议的默认行为
- 在可能的情况下，优先选择只读操作（如 `git status`、`rg`、`ls`）而非可修改系统状态的命令。
- 首先尝试可逆的操作。
- 即使技术上允许执行破坏性操作，也必须先获取用户的确认。