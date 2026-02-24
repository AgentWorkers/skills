---
name: supabase-checkpointer
description: 通过 Supabase REST API（PostgREST）实现 LangGraph 的持久化检查点功能——无需直接连接 Postgres 数据库。适用于将 LangGraph 图谱部署到临时性平台（如 Railway、Fly、Cloud Run）的场景：在这些平台上，内存中的数据会在重新部署时丢失，因此需要使用该功能来实现任务的中断和恢复，以确保任务在系统崩溃后仍能继续执行。该功能适用于所有使用现有服务角色密钥的 Supabase 项目。
---
# Supabase REST Checkpointer for LangGraph

## 问题

LangGraph 的 `MemorySaver` 会在进程内部存储状态数据。在临时部署环境（如 Railway、Fly 等）中，重新部署时会终止进程，导致所有未完成的图状态数据丢失。`PostgresSaver` 需要直接连接到 Postgres 数据库，但这种连接可能无法建立。

## 解决方案

我们实现了一个名为 `BaseCheckpointSaver` 的组件，它通过 Supabase 的 PostgREST API 来存储检查点数据，无需直接连接到 Postgres 数据库。

## 设置步骤

### 1. 创建表格

在 Supabase 中运行 `scripts/create_tables.sql`（可以通过 SQL 编辑器或 `exec_sql` RPC 命令执行）：

```sql
CREATE TABLE langgraph_checkpoints (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    parent_checkpoint_id TEXT,
    type TEXT,
    checkpoint JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

CREATE TABLE langgraph_writes (
    thread_id TEXT NOT NULL,
    checkpoint_ns TEXT NOT NULL DEFAULT '',
    checkpoint_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    idx INTEGER NOT NULL,
    channel TEXT NOT NULL,
    type TEXT,
    blob JSONB,
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);
```

### 2. 使用 Checkpointer

```python
from supabase import create_client
from supabase_checkpointer import SupabaseCheckpointer

client = create_client(url, key)
checkpointer = SupabaseCheckpointer(client)
graph = builder.compile(checkpointer=checkpointer)
```

### 3. 备用方案（推荐）

```python
def _create_checkpointer():
    # 1. Try Supabase (durable across redeploys)
    try:
        from supabase_checkpointer import SupabaseCheckpointer
        client = get_supabase_client()
        if client:
            return SupabaseCheckpointer(client)
    except Exception:
        pass

    # 2. Try SQLite (survives process restarts within same deploy)
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
        import sqlite3
        return SqliteSaver(sqlite3.connect("checkpoints.db", check_same_thread=False))
    except Exception:
        pass

    # 3. Fallback: in-memory (lost on restart)
    from langgraph.checkpoint.memory import MemorySaver
    return MemorySaver()
```

## 实现细节

完整的实现代码位于 `scripts/supabase_checkpointer.py` 文件中，其中包含了 `BaseCheckpointSaver` 所需的所有方法：

- `put()`：将检查点数据插入 `langgraph_checkpoints` 表中。
- `put_writes()`：将待写入的数据插入 `langgraph_writes` 表中。
- `get_tuple()`：获取某个线程的最新检查点数据及待写入的数据。
- `list()`：遍历某个线程的所有检查点数据（实现时间回溯功能）。

所有数据都以 JSONB 格式进行序列化；对于无法序列化的类型，使用 `json.dumps(obj, default=str)` 进行处理。

## 关键细节：

- **线程隔离**：每个图处理任务在配置文件中使用唯一的 `thread_id` 进行标识。
- **检查点排序**：根据 `created_at` 字段的降序顺序来查找最新的检查点。
- **写入数据的去重**：通过复合主键机制防止重复写入。
- **错误处理**：所有操作都包含在 `try/except` 块中，遇到错误时仅记录日志而不会导致程序崩溃。
- **无需异步处理**：使用同步的 Supabase 客户端（通过 HTTP 协议访问 PostgREST API）。