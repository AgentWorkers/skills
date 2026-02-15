---
name: stream-of-consciousness
description: 将整个对话上下文导出为 Open-Token 格式（包括工具和可选的内部跟踪信息），以便于代理之间的协作、审计以及问题的重现。
version: 0.1.0
---

# Open-Token 导出（SKILL）

## 目标

当被调用时，以 Open-Token 格式输出当前对话的 **全部内容**，作为一个单独的导出文件，适用于以下场景：
- 代理在运行时和提供者之间的交接/延续
- 审计和事件审查
- 可复现性和调试
- 来源追踪和差异分析

输出必须能够被机器解析，并且根据所选模式保持完整性。

## 调用方式

将 `$ARGUMENTS` 解析为以空格分隔的 `key=value` 对。

支持的选项：

- `mode=json|ndjson`  
  默认值：`json`

- `pretty=true|false`  
  默认值：`json` 时为 `true`；`ndjson` 时为 `false`

- `include=visible-only|include-internal`  
  默认值：`visible-only`

- `internal=redacted|summary|full`  
  默认值：`redacted`  
  含义：
  - `redacted`：仅包含内部事件的占位符（无实际内容）
  - `summary`：包含内部追踪的简要摘要（如果可用）
  - `full`：包含内部追踪的原始内容（仅在可用且被允许的情况下）

- `redact=none|secrets|pii|strict`  
  默认值：`secrets`

- `max_bytes=<int>`（可选）  
  如果存在，应用以下定义的截断规则。

### 内部追踪的可用性规则

如果请求了 `include=include-internal`，但在当前运行时环境中无法获取内部追踪（隐藏的推理过程、隐藏的系统路由、隐藏的中间令牌），则不要伪造这些数据。

在这种情况下：
- 设置 `conversation.internal_availability="unavailable"`
- 省略内部追踪内容事件，或将其作为占位符输出（与 `internal=redacted` 一致）
- 仍然输出工具调用/结果（如果可用）

## 不可协商的规则

1. 仅导出当前对话环境中实际存在的数据；切勿虚构缺失的对话内容。
2. 保持事件的因果顺序；不得重新排序事件。
3. 保持归属信息：正确的参与者、角色和事件类型。
4. 工具输出必须单独放在 `tool_result` 事件中。
5. 根据 `redact` 选项应用隐藏规则（除非 `redact=none`）。
6. 如果输出被截断，必须明确标注截断原因（参见截断部分）。
7. 确保最终输出是有效的 JSON（或每行有效的 NDJSON），且没有额外的注释。

## Open-Token 架构 v0.1

### 顶层对象（mode=json）

输出一个 JSON 对象：

```json
{
  "open_token_version": "0.1",
  "exported_at": "RFC3339 timestamp in UTC if available, else omit",
  "conversation": {},
  "participants": [],
  "events": [],
  "integrity": {}
}
```

约束：
- 除了列出的键之外，不允许添加其他顶层键（无法填充的键请省略）。
- `events` 必须按严格递增的顺序排列。

### 流式导出（mode=ndjson）

输出以换行符分隔的 JSON 记录：

1. 标头行：
{ "type": "header", "open_token_version": "0.1", "exported_at": "..." }

2. 然后每个事件占一行：
{ "type": "event", ...event object... }

3. 可选的页脚行：
{ "type": "footer", "integrity": { ... } }

约束：
- 每行都必须是有效的 JSON。
- 不要将 NDJSON 放入数组中。

## conversation 对象

`conversation` 字段：

- `id`（必需）：如果由运行时提供，则使用稳定的标识符；否则生成 `conv_<YYYYMMDD>_<hash8>`
- `title`（可选）
- `started_at`（可选；遵循 RFC3339 格式；不要猜测）
- `timezone`（可选）
- `source_runtime`（可选）：`cli`|"web"|"api"|"ide"|"other"
- `provider`（可选）：`openai"|"anthropic"|"google"|"meta"|"other"
- `internal_availability`（可选）：`available"|"unavailable"|"unknown"
- `redaction`（如果 `redact` 不为 `none` 则必需）：
  - `mode`：`none`|`secrets`|`pii`|`strict`
  - `strategy`：`mask`|`drop`|`hash`
  - `notes`：高级别注释数组（不包含敏感信息）

## participants 数组

每个参与者：

{
  "actor_id": "act_###",
  "kind": "human"|`model`|`tool`|`system",
  "name": "string",
  "provider": "string (可选)",
  "model": "string (可选)",
  "instance_id": "string (可选)"
}

规则：
- 每个不同的说话者/代理/工具发起者创建一个 `participants` 条目。
- 对于系统/开发者提示的发起者，使用 `kind="system"`。
- 对于外部工具/功能，使用 `kind="tool"`。
- 对于模型/代理的输出，使用 `kind="model"`。

## events 数组

### 事件结构

每个 `events[]` 条目必须遵循以下格式：

{
  "id": "evt_000001",
  "seq": 1,
  "ts": "RFC3339 UTC 时间戳（如果未知则可选）",
  "type": "message"|`tool_use`|`tool_result`|`span_start`|`span_end`|`annotation`,
  "actor_id": "act_###",
  "visibility": "public"|`internal`|`metadata`,
  "role": "system"|`developer`|`user`|`assistant`|`assistant_thought`|`tool`,
  "content": {
    "mime": "text/plain"|`application/json`,
    "text": "string (可选)",
    "data": {}
  },
  "links": {
    "parent_id": "evt_###### (可选)",
    "replies_to": "evt_###### (可选)",
    "call_id": "call_###### (可选)",
    "span_id": "span_###### (可选)"
  },
  "usage": {
    "input_tokens": 0,
    "output_tokens": 0,
    "reasoning_tokens": 0
  }
}

规则：
- `id` 是必需的；`seq` 是必需的，并且必须是连续的（1..N）。
- `ts` 是可选的；不要猜测时间戳。
- `usage` 是可选的；仅在可用时包含。
- 如果使用了 `content.text`，则 `contentmime` 应为 `text/plain`。
- 如果使用了 `content.data`，则 `contentmime` 应为 `application/json`。

### 角色映射指南

将提供者概念映射到 `role` 和 `visibility`：

- 系统提示 → `role="system"`，`visibility="internal"`（或如果明确显示则为 `public`）
- 开发者指令 → `role="developer"`，`visibility="internal"`
- 用户消息 → `role="user"`，`visibility="public"`
- 助手最终答案 → `role="assistant"`，`visibility="public"`
- 隐藏的推理过程：
  - 如果可用且 `include=include-internal`：
    - `role="assistant_thought"`，`visibility="internal"`
    - `content` 的处理方式取决于 `internal`：
      - `full`：包含原始的思考内容
      - `summary`：包含简短的摘要字符串
      - `redacted`：包含没有思考内容的占位符
  - 否则：
    - 省略思考内容；在这种情况下设置 `conversation.internal_availability="unavailable"`
- 工具调用请求 → `type="tool_use"`，`role="assistant"`，`visibility="internal"`
- 工具输出 → `type="tool_result"`，`role="tool"`，`visibility="internal"`

### 工具事件要求

对于每个工具调用：
- 输出一个 `tool_use` 事件和一个 `tool_result` 事件。
- 两者必须共享相同的 `links.call_id`。
- `tool_use.content.data` 必须包含：
  - `tool_name`（字符串）
  - `arguments`（对象/数组）
- `tool_result.content` 必须仅包含工具的输出。
  - 如果是结构化的：`contentmime="application/json"` 并将输出放在 `content.data` 中
  - 如果是文本：`contentmime="text/plain"` 并将输出放在 `content.text` 中

如果工具调用被发起但上下文中没有结果：
- 仍然输出 `tool_use` 事件。
- 输出一个 `tool_result` 事件，其中包含：
  - `contentmime="application/json"`
  - `content.data={"missing_result":true}``
  - 并根据需要包含 `conversation.redaction.notes` 或事件级别的注释。

## 嵌套的代理和子代理

如果存在子代理：
- 将每个子代理表示为独立的参与者（`kind="model"`）。
- 将子代理的活动包装在一个时间跨度中：
  - `span_start` 事件开始时间跨度（`links.span_id`）
  - 子代理事件包含 `links.span_id`
  - `span_end` 事件结束时间跨度

如果有关于子代理的元数据，将其放在 `span_start.content.data` 中：
- `spawn_reason`
- `requested_capabilities`
- `tooling_scope`
- `model`（如果指定）

## 隐藏规则

根据 `redact` 选项应用隐藏规则：

- `none`：不进行隐藏（但如果政策要求，仍需避免输出已知的私密键）
- `secrets`：隐藏 API 密钥、认证令牌、密码、会话 cookie、私钥
- `pii`：额外隐藏电子邮件、电话号码、街道地址、直接的个人标识符
- `strict`：隐藏敏感信息、个人身份信息（PII）以及任何可能包含敏感数据的内部配置字符串

机制：
- 用 `[REDACTED:<type>:<hash8>]` 替换敏感子字符串
- 除非必要，否则不要更改周围的标点符号。
- 在 `conversation.redaction.notes` 中记录高级别注释（不包含敏感值）。

## 截断

如果设置了 `max_bytes` 且输出超过限制：
1. 优先截断较大的 `content.text` 字段：
   - 保留前 1024 个字符和最后 256 个字符，然后插入 `…`
2. 标记被截断的内容：
   - 如果 `contentmime="text/plain"`：
     - 在 JSON 结构中添加 `content.data={"truncated":true,"original_length":<int if known>}` 并保留截断后的文本
   - 如果 `contentmime="application/json"`：
     - 在 JSON 结构中添加 `{"truncated":true}`

3. 除非明确要求，否则不要删除事件；如果必须删除，请先删除最旧的事件，并添加一个描述删除情况的注释事件。

## 完整性（可选）

如果可行，包括以下内容：

"integrity": {
  "hash_alg": "sha256",
  "canonicalization": "json-c14n-like",
  "events_hash": "hex string"
}

如果不可行，则省略 `integrity`。

## 输出检查清单（必须满足）

- 输出是有效的 JSON（或每行有效的 NDJSON）。
- `seq` 是连续且严格递增的。
- 没有伪造的时间戳或缺失的对话内容。
- 工具调用：`tool_use` 通过 `call_id` 与 `tool_result` 配对（或使用明确的缺失结果标记）。
- 根据 `redact` 选项应用了隐藏规则。
- 内部追踪仅在可用时包含；否则标记为不可用且不伪造。
- 输出内容中不包含额外的文本。

## 最小示例（json）

```json
{
  "open_token_version": "0.1",
  "exported_at": "2026-01-31T00:00:00Z",
  "conversation": {
    "id": "conv_20260131_ab12cd34",
    "provider": "unknown",
    "source_runtime": "unknown",
    "internal_availability": "unavailable",
    "redaction": {
      "mode": "secrets",
      "strategy": "mask",
      "notes": ["masked api keys"]
    }
  },
  "participants": [
    { "actor_id": "act_001", "kind": "system", "name": "system" },
    { "actor_id": "act_002", "kind": "human", "name": "user" },
    { "actor_id": "act_003", "kind": "model", "name": "assistant", "provider": "unknown", "model": "unknown" },
    { "actor_id": "act_004", "kind": "tool", "name": "CalculatorAPI" }
  ],
  "events": [
    {
      "id": "evt_000001",
      "seq": 1,
      "type": "message",
      "actor_id": "act_001",
      "visibility": "internal",
      "role": "system",
      "content": { "mime": "text/plain", "text": "You are a math tutor." }
    },
    {
      "id": "evt_000002",
      "seq": 2,
      "type": "message",
      "actor_id": "act_002",
      "visibility": "public",
      "role": "user",
      "content": { "mime": "text/plain", "text": "What is 5 factorial?" }
    },
    {
      "id": "evt_000003",
      "seq": 3,
      "type": "tool_use",
      "actor_id": "act_003",
      "visibility": "internal",
      "role": "assistant",
      "content": {
        "mime": "application/json",
        "data": { "tool_name": "CalculatorAPI", "arguments": { "op": "factorial", "n": 5 } }
      },
      "links": { "call_id": "call_000001" }
    },
    {
      "id": "evt_000004",
      "seq": 4,
      "type": "tool_result",
      "actor_id": "act_004",
      "visibility": "internal",
      "role": "tool",
      "content": { "mime": "text/plain", "text": "120" },
      "links": { "call_id": "call_000001" }
    },
    {
      "id": "evt_000005",
      "seq": 5,
      "type": "message",
      "actor_id": "act_003",
      "visibility": "public",
      "role": "assistant",
      "content": { "mime": "text/plain", "text": "5! equals 120." }
    }
  ]
}
```