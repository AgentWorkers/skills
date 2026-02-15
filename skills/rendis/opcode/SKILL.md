---
name: opcode
description: >
  Zero-token execution layer for AI agents. Define workflows once, run them
  free forever — persistent, scheduled, deterministic. 6 MCP tools over SSE.
  Supports DAG-based execution, 6 step types (action, condition, loop,
  parallel, wait, reasoning), 26 built-in actions, ${{}} interpolation,
  reasoning nodes for human-in-the-loop decisions, and secret vault.
  Use when defining workflows, running templates, checking status,
  sending signals, querying workflow history, or visualizing DAGs.
license: MIT
compatibility: >
  Requires Go 1.25+, CGO_ENABLED=1, and gcc or clang.
  Runs as SSE daemon on macOS and Linux.
  Linux: cgroups v2 for process isolation. macOS: timeout-only fallback.
metadata:
  version: "1.2.1"
  transport: "sse"
  author: "rendis"
  repository: "https://github.com/rendis/opcode"
  primary-env: "OPCODE_VAULT_KEY"
  platforms: "darwin linux"
  requires-bins: "go gcc|clang"
  openclaw-emoji: "⚙️"
  openclaw-os: "darwin linux"
  openclaw-user-invocable: "true"
  openclaw-install-type: "go"
  openclaw-install-package: "github.com/rendis/opcode/cmd/opcode"
---

# OPCODE

OPCODE 是用于管理 AI 代理执行流程的工具。它负责执行代理的推理逻辑，在首次定义工作流程后，每次运行都不会消耗任何令牌（token）。工作流程可以在会话之间持续存在，并根据预定时间表执行，同时还能协调多个代理的运作。系统依赖于一个持久的 SSE（Simple State Engine）守护进程：1 个服务器、N 个代理以及 1 个数据库。工作流程的逻辑通过 JSON 定义，支持逐级执行和自动并行处理。OPCODE 通过 JSON-RPC 协议与 MCP（Master Control Panel）进行通信。

**为什么使用 OPCODE 而不是手动逐步执行推理？** 因为重复执行相同的工作流程会浪费已经做出的决策所消耗的令牌。OPCODE 会一次性将推理逻辑模板化，然后以确定性的方式执行它——这样每次运行的推理成本为 0，输出结果始终一致，并且能够跨上下文重置保持不变。

## 使用哪种工具？

| 功能需求 | 工具名称       |
| -------- | -------------- |
| 创建/更新工作流程模板 | opcode.define   |
| 执行工作流程 | opcode.run    |
| 检查状态或待定决策 | opcode.status   |
| 解决决策/取消/重试 | opcode.signal   |
| 列出工作流程、事件或模板 | opcode.query    |
| 可视化工作流程图 | opcode.diagram |

## 快速入门

**安装：**
```bash
go install github.com/rendis/opcode/cmd/opcode@latest
```

**首次设置（配置并启动守护进程：**
```bash
opcode install --listen-addr :4100 --vault-key "my-passphrase"
```

**停止后重启：`OPCODE_VAULT_KEY="my-passphrase" opcode`

**MCP 客户端配置：**
```json
{
  "mcpServers": {
  "mcpServers": {
    "opcode": {
      "type": "sse",
      "url": "http://localhost:4100/sse"
    }
  }
}
```

每个代理都会在调用工具时通过 `agent_id` 自动识别自身。建议为每个代理选择一个唯一的 ID（例如：“content-writer”或“deploy-bot”）。

工作流程在重启后仍能保持状态。启动时，处于“active”状态但被暂停的工作流程会变为“suspended”状态。可以通过 `opcode.query({ "resource": "workflows", "filter": { "status": "suspended" } )` 来查询这些工作流程，然后使用 `opcode.signal` 来恢复或取消它们。

有关完整的配置信息、子命令、热加载机制、安全模型、Web 面板以及性能测试，请参阅 [operations.md](references/operations.md)。

## MCP 工具

### opcode.define

用于注册可重用的工作流程模板。模板版本会自动递增（v1、v2、v3 等）。

| 参数        | 类型       | 是否必填 | 描述                                                                                          |
| ------------ | -------- | -------- | ----------------------------------------------------------------------------------------------- |
| `name`      | 字符串     | 是       | 模板名称                                                                                         |
| `definition` | 对象       | 是       | 工作流程的定义                                                                                   |
| `agent_id`    | 字符串     | 是       | 定义该工作流程的代理 ID                                                                                   |
| `description` | 字符串     | 否       | 模板描述                                                                                         |
| `input_schema` | 对象       | 否       | 用于输入验证的 JSON 架构                                                                                   |
| `output_schema` | 对象       | 否       | 用于输出验证的 JSON 架构                                                                                   |
| `triggers`    | 对象       | 否       | 触发器配置（详见 [workflow-schema.md](references/workflow-schema.md#triggers-template-level) |

**返回值：`{ "name": "...", "version": "v1" }`

### opcode.run

根据注册的模板执行工作流程。

| 参数        | 类型       | 是否必填 | 描述                                                                                          |
| ------------ | -------- | ------------------------- |
| `template_name` | 字符串     | 是       | 要执行的工作流程模板名称                                                                                   |
| `agent_id`    | 字符串     | 是       | 启动该工作流程的代理 ID                                                                                   |
| `version`     | 字符串     | 否       | 使用的模板版本（默认为最新版本）                                                                                   |
| `params`      | 对象       | 否       | 输入参数                                                                                         |

**返回值：**
```json
{
  "workflow_id": "uuid",
  "status": "completed | suspended | failed",
  "output": { ... },
  "started_at": "RFC3339",
  "completed_at": "RFC3339",
  "steps": {
    "step-id": { "step_id": "...", "status": "completed", "output": {...}, "duration_ms": 42 }
  }
}
```

如果工作流程的状态为“suspended”，可以使用 `opcode.status` 来查看待定的决策。

### opcode.status

用于获取工作流程的执行状态。

| 参数        | 类型       | 是否必填 | 描述                                                                                          |
| ------------ | -------- | ------------------------- |
| `workflow_id` | 字符串     | 要查询的工作流程 ID                                                                                   |

**返回值：**
```json
{
  "workflow_id": "uuid",
  "status": "suspended",
  "steps": { "step-id": { "status": "...", "output": {...} } },
  "pending_decisions": [
    {
      "id": "uuid",
      "step_id": "reason-step",
      "context": { "prompt": "...", "data": {...} },
      "options": [ { "id": "approve", "description": "Proceed" } ],
      "timeout_at": "RFC3339",
      "fallback": "reject",
      "status": "pending"
    }
  ],
  "events": [ ... ]
}
```

工作流程的状态包括：`pending`（待定）、`active`（活动）、`suspended`（暂停）、`completed`（已完成）、`failed`（失败）和 `cancelled`（已取消）。

### opcode.signal

用于向被暂停的工作流程发送信号。

| 参数        | 类型       | 是否必填 | 描述                                                                                          |
| ------------ | -------- | ------------------------- |
| `workflow_id` | 字符串     | 目标工作流程 ID                                                                                   |
| `signal_type` | 枚举       | 是       | 信号类型（`decision`、`data`、`cancel`、`retry`、`skip`）         |
| `payload`     | 对象       | 是       | 信号携带的数据                                                                                         |
| `step_id`     | 字符串     | 目标执行步骤编号                                                                                   |
| `agent_id`    | 字符串     | 发送信号的代理 ID                                                                                   |
| `reasoning`   | 字符串     | 代理的推理结果                                                                                         |

**不同信号类型的有效载荷：**

| 信号类型    | 执行步骤编号 | 有效载荷                        | 行为                                                                                         |
| ---------- | -------------- | -------------------------------- | ----------------------------- |
| `decision`   | 必填       | `{ "choice": "<option_id>" }` | 解决决策，自动恢复工作流程                 |
| `data`     | 可选       | `{ "key": "value", ... }`     | 向工作流程注入数据                                   |
| `cancel`    | 可选       | `{}`                          | 取消工作流程                                   |
| `retry`     | 必填       | `{}`                          | 重试失败的步骤                                   |
| `skip`     | 必填       | `{}`                          | 跳过失败的步骤                                   |

**返回值：**
- 如果信号类型为 `decision`：`{ "ok": true, "resumed": true, "status": "completed" }`
- 其他情况：`{ "ok": true, "workflow_id": "...", "signal_type": "..." }`

### opcode.query

用于查询工作流程、事件或模板的信息。

| 参数        | 类型       | 是否必填 | 描述                                                                                          |
| ------------ | -------- | ------------------------------------ |
| `resource`     | 枚举       | 查询类型（`workflows`、`events` 或 `templates`）       |
| `filter`      | 对象       | 过滤条件                                                                                         |

**按资源类型过滤：**

| 资源类型    | 可过滤的字段                                      |
| ---------- | -------------------------------------------------------- |
| `workflows`   | `status`, `agent_id`, `since` (RFC3339), `limit`         |
| `events`    | `workflow_id`, `step_id`, `event_type`, `since`, `limit`     |
| `templates`   | `name`, `agent_id`, `limit`                              |

**注意：** 查询事件时，必须提供 `event_type` 或 `workflow_id` 作为过滤条件。

**返回值：`{ "<resource>": [...] }` —— 结果按资源类型进行分类返回。**

### opcode.diagram

根据模板或正在执行的工作流程生成可视化的有向无环图（DAG）。

| 参数        | 类型       | 是否必填 | 描述                                                                                          |
| ------------ | -------- | ------------------------- |
| `template_name` | 字符串     | 是否需要显示模板名称（用于预览结构）         |
| `version`     | 字符串     | 是否需要显示模板版本（默认为最新版本）         |
| `workflow_id`    | 字符串     | 是否需要显示工作流程 ID（包括运行状态）         |
| `format`      | 枚举       | 图表格式（`ascii`、`mermaid` 或 `image`）         |
| `include_status` | 布尔值     | 是否显示运行状态（默认为 `true`，如果提供了 `workflow_id`）     |

**注意：** 必须提供 `template_name` 或 `workflow_id` 中的一个。

- `template_name`：在执行前预览工作流程的结构。
- `workflow_id`：显示包含实时步骤状态的工作流程图。
- `format: "ascii"`：以文本格式显示图表（适合命令行界面）。
- `format: "mermaid"`：使用 Markdown 语法生成的流程图。
- `format: "image"`：以 Base64 编码的 PNG 图片格式显示图表。

**返回值：`{ "format": "ascii", "diagram": "..." }`

## 工作流程定义

```json
{
  "steps": [ ... ],
  "inputs": { "key": "value or ${{secrets.KEY}}" },
  "context": { "intent": "...", "notes": "..." },
  "timeout": "5m",
  "on_timeout": "fail | suspend | cancel",
  "on_complete": { /* step definition */ },
  "on_error": { /* step definition */ },
  "metadata": {}
}
```

| 参数        | 类型       | 是否必填 | 描述                                                                                          |
| ------------ | -------- | ------------------------- |
| `steps`      | StepDefinition[] | 是否需要定义工作流程的步骤                         |
| `inputs`     | 对象       | 是否需要输入参数                         |
| `context`     | 对象       | 工作流程的上下文（可通过 `${{context.*}` 访问）         |
| `timeout`     | 字符串     | 工作流程的超时时间（例如：“5m”或“1h”）         |
| `on_timeout`    | 字符串     | 失败时的处理方式（`fail`、`suspend` 或 `cancel`）     |
| `on_complete` | StepDefinition | 完成后的处理步骤                         |
| `on_error`    | StepDefinition | 工作流程失败时的处理步骤                         |
| `metadata`    | 对象       | 可选的元数据                                   |

### Step Definition（步骤定义）

`type` 的默认值为 `action`。详细配置信息请参阅 [workflow-schema.md](references/workflow-schema.md)。

## 步骤类型

### action（默认类型）

执行已注册的动作。通过设置 `action` 来指定动作名称，并通过 `params` 传递输入参数。

### condition

评估 CEL（Cellular Expression）表达式并根据结果进行分支处理。

```json
{
  "id": "route",
  "type": "condition",
  "config": {
    "expression": "inputs.env",
    "branches": { "prod": [...], "staging": [...] },
    "default": [...]
  }
}
```

### loop

遍历集合或条件。循环变量包括：`${{loop.item}}` 和 `{{loop.index}}`。

```json
{
  "id": "process-items",
  "type": "loop",
  "config": {
    "mode": "for_each",
    "over": "[\"a\",\"b\",\"c\"]",
    "body": [
      {
        "id": "hash",
        "action": "crypto.hash",
        "params": { "data": "${{loop.item}}" }
      }
    ],
    "max_iter": 100
  }
}
```

循环模式包括：`for_each`（遍历集合）、`while`（当条件为真时持续循环）和 `until`（当条件为真时停止循环）。

### parallel

并发执行多个分支。

```json
{
  "id": "fan-out",
  "type": "parallel",
  "config": {
    "mode": "all",
    "branches": [
      [{ "id": "a", "action": "http.get", "params": {...} }],
      [{ "id": "b", "action": "http.get", "params": {...} }]
    ]
  }
}
```

并行执行模式包括：`all`（等待所有分支完成）和 `race`（先完成的分支获胜）。

### wait

延迟执行或等待指定的信号。

```json
{ "id": "pause", "type": "wait", "config": { "duration": "5s" } }
```

### reasoning

当需要代理做出决策时，会暂停工作流程。如果未指定 `options`，则允许代理自由选择任何决策。

```json
{
  "id": "review",
  "type": "reasoning",
  "config": {
    "prompt_context": "Review data and decide",
    "options": [
      { "id": "approve", "description": "Proceed" },
      { "id": "reject", "description": "Stop" }
    ],
    "data_inject": { "analysis": "steps.analyze.output" },
    "timeout": "1h",
    "fallback": "reject",
    "target_agent": ""
  }
}
```

## 变量插值

语法：`${{namespace.path}}`

| 命名空间    | 可用的字段                                      |
| ---------- | ----------------------------------- | ----------------------------------------------------------------- |
| `steps`     | `${{steps.fetch.output.body}}`      | 获取步骤的输出结果                   |
| `inputs`    | `${{inputs.api_key}}`               | 从 `opcode.run` 中获取的参数键             |
| `workflow`    | `${{workflow.run_id}}`              | 工作流程的 ID、名称、版本和代理 ID             |
| `context`     | `${{context(intent}}`               | 工作流程定义中的上下文键                 |
| `secrets`    | `${{secrets.DB_PASS}}`              | 从安全存储库中获取的密钥                   |
| `loop`     | `${{loop.item}}`, `${{loop.index}}` | 当前循环项和循环索引                     |

变量插值的处理规则：首先获取非敏感数据，然后通过 AES-256-GCM 加密算法从安全存储库中获取敏感数据。

**关于 CEL 的注意事项：** `loop` 是 CEL 语言中的保留字。在 CEL 表达式中应使用 `iter.item` 或 `iter.index`。`{{loop.item}}` 的插值语法仍然有效。

有关 CEL 语言、GoJQ 库以及表达式引擎的详细信息，请参阅 [expressions.md](references/expressions.md)。

## 内置动作

| 动作类别       | 动作名称                                      |
| -------------- | --------------------------------------- |
| **HTTP**       | `http.request`, `http.get`, `http.post`                 |
| **文件系统**     | `fs.read`, `fs.write`, `fs.append`, `fs.delete`, `fs.list`, `fs.stat`, `fs.copy`, `fs.move` |
| **Shell**      | `shell.exec`                                    |
| **加密**     | `crypto.hash`, `crypto.hmac`, `crypto.uuid`                |
| **断言**     | `assert.equals`, `assert.contains`, `assert.matches`, `assert.schema`     |
| **表达式**     | `expr.eval`                                    |

**常用动作示例：**

- `http.get`：`url`（请求参数）、`headers`（请求头）、`timeout`（超时设置）、`fail_on_error_status`（错误处理）——返回值：`{ status_code, headers, body, duration_ms }`
- `shell.exec`：`command`（命令）、`args`（命令参数）、`stdin`（标准输入）、`timeout`（超时设置）、`env`（环境变量）、`workdir`（工作目录）——返回值：`{ stdout, stderr, exit_code, killed }`
- `fs.read`：`path`（文件路径）、`encoding`（编码方式）——返回值：`{ path, content, encoding, size }`
- `workflow.notify`：`message`（通知内容）、`data`（通知标志）——通过 MCP SSE 向代理发送实时通知（尽力通知）
- `expr.eval`：`expression`（表达式）、`data`（计算结果）——在工作流程的上下文中评估表达式

有关所有 26 个内置动作的详细参数说明，请参阅 [actions.md](references/actions.md)。

## 使用 `shell.exec` 进行脚本编写

`shell.exec` 会自动解析 JSON 格式的输入。默认参数分配规则为：`stdout` 用于输出 JSON 数据，`stderr` 用于输出错误信息，非零退出代码表示执行失败。如果需要原始的命令行输出，可以使用 `stdout_raw` 参数。

有关特定语言（Bash、Python、Node、Go）的脚本编写模板，请参阅 [patterns.md](references/patterns.md#10-scripting-with-shellexec)。

## 推理节点的生命周期

1. 工作流程到达需要推理的步骤。
2. 执行器创建一个 `PendingDecision` 对象，并触发 `decision_requested` 事件。
3. 工作流程的状态变为 `suspended`（暂停）。
4. 代理调用 `opcode.status` 来查看待定的决策及其相关选项。
5. 代理通过 `opcode.signal` 来执行相应的操作。

```json
   {
     "workflow_id": "...",
     "signal_type": "decision",
     "step_id": "reason-step",
     "payload": { "choice": "approve" }
   }
   ```

6. 接收到信号后，工作流程会自动恢复执行。
7. 如果超时时间到期，系统会自动选择备用方案；如果没有备用方案，则步骤会失败。

## 常见使用模式

有关工作流程的常见使用模式（如线性流程、条件分支、循环处理、并行执行、人工干预、错误恢复等），请参阅 [patterns.md](references/patterns.md)。

## 错误处理

| 错误处理策略 | 处理方式                                      |
| --------------- | ----------------------------------- |
| `ignore`     | 跳过当前步骤，继续执行剩余的工作流程           |
| `fail_workflow` | 整个工作流程失败                             |
| `fallback_step` | 执行备用步骤                             |
| `retry`      | 根据预设策略尝试重新执行                         |

错误处理策略包括：`none`（忽略错误）、`linear`（线性重试）、`exponential`（指数级重试）和 `constant`（固定次数重试）。对于无法重试的错误（如验证失败、权限问题或断言错误），系统不会尝试重新执行。

有关错误处理机制的详细信息，包括断路器设置和超时处理规则，请参阅 [error-handling.md](references/error-handling.md)。

## 性能表现

包含 10 个步骤的工作流程大约在 50 微秒内完成，包含 500 个步骤的工作流程大约在 2.4 毫秒内完成。事件存储系统每秒可以处理约 15,000 条新增记录，在同时有 100 个代理写入数据的情况下，系统性能下降幅度小于 12%。工作进程池的额外开销约为每个任务 0.85 微秒（在任何规模的进程池中，处理速度可超过每秒 100 万个任务）。

完整的性能测试图表、各场景下的详细数据以及测试方法论，请参阅 [`docs/benchmarks.md`](../../docs/benchmarks.md)。