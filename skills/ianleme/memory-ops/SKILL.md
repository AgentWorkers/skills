---
name: memory-ops
description: Consulta e persistência obrigatória da memória principal no PostgreSQL (Memory_openclaw + pgvector). Use quando for responder, delegar tarefas, consolidar contexto do usuário, registrar handoffs (ex.: Alfred, Prompt Improver), ou manter histórico operacional com auditoria.
---

# 内存操作（Memory Operations）

## 强制执行的协议（Always mandatory）：
1. 在响应或委托任务之前，必须先查询主内存（main memory）。
2. 在响应或委托任务时，必须携带已获取的上下文信息。
3. 必须保存用户的输入提示（prompt）的上下文。
4. 必须保存发送给代理（agents）的每个委托任务的上下文信息。
5. 必须记录内存操作的审计信息（包括读写状态）。

## 目标数据库（Target Database）：
- 数据库名称：`Memory_openclaw`
- 数据库扩展名：`vector`
- 使用的表：`memories` 和 `memory_audit`

## 写入规则（Writing Rules）：
- 除非有明确需要，否则不得保存敏感信息。
- 优先记录操作相关的事实，包括目标（goal）、决策（decision）、限制（restriction）、偏好（preference）以及下一步行动（next step）。
- 必须包含以下最低限度的元数据：`source`、`scope`、`agent`、`timestamp`、`kind`。

## SQL 和数据库模式（SQL and Database Schema）：
- 数据库模式的创建/更新操作在文件 `references/schema.sql` 中进行。
- 查询操作在文件 `references/queries.sql` 中进行。

## 强制执行的审计记录（Mandatory Auditing）：
- 每个操作周期（turn cycle）必须在 `memory_audit` 中记录一次事件，记录内容包括：
  - `event_type`：操作类型（如 `turn_cycle`）
  - `read_ok`：读取操作是否成功（true/false）
  - `write_ok`：写入操作是否成功（true/false）
  - `details`：包含计数数据和相关 ID 的 JSON 数据

## 与代理的交互（Interaction with Agents）：
- 当将任务委托给 Alfred 或 Prompt Improver 时：
  - 首先保存类型为 `kind=delegation_prompt` 的记录，其中包含用户输入的提示内容。
  - 任务返回后，保存类型为 `kind=delegation_result` 的记录，其中包含任务执行的总结结果。
- 只有在完成这些步骤后，才能向用户提供最终响应。

## 参考实现（Reference Implementation）：
- 可用的脚本模板：`scripts/memory_ops_template.sql`
- 如果需要调整嵌入数据的维度，需根据实际模型修改 `vector(1536)` 这一列的宽度。