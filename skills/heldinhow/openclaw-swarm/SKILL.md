# openclaw-swarm

使用 OpenClaw Swarm 的功能来实现高级的子代理（subagent）编排。

## 关于

此技能提供了对 **OpenClaw Swarm** 的访问权限——OpenClaw 的一个分支，它增强了子代理的编排能力：

- **分支地址：** https://github.com/Heldinhow/openclaw-swarm
- **文档：** [SWARM.md](https://github.com/Heldinhow/openclaw-swarm/blob/main/SWARM.md)

## 适用场景

在以下情况下使用此技能：
- 创建需要共享上下文的子代理
- 协调多个子代理的运行
- 在子代理之间共享状态
- 运行并行任务

## 可用工具

### 1. sessions_spawn（支持上下文共享）

将父会话的上下文共享给子代理：

```json
{
  "sessions_spawn": {
    "label": "my-task",
    "task": "Do something",
    "contextSharing": "recent"
  }
}
```

**可选参数：**
- `none` - 不共享任何上下文
- `summary` - 压缩后的会话摘要
- `recent` - 最新的消息
- `full` - 完整的会话历史记录

### 2. context_store

在子代理之间共享数据：

```json
// Write
{ "context_store": { "action": "set", "namespace": "project", "key": "data", "value": {...} } }

// Read
{ "context_store": { "action": "get", "namespace": "project", "key": "data" } }
```

**支持的操作：** `get`（获取）、`set`（设置）、`delete`（删除）、`list`（列出）、`subscribe`（订阅）、`broadcast`（广播）

### 3. context_publish

在子代理完成任务时发送通知：

```json
{ "context_publish": {
    "action": "publish",
    "eventType": "task_complete",
    "target": "orchestrator",
    "data": { "result": "..." }
  }
}
```

### 4. parallel_spawn

并行运行多个子代理：

```json
{ "parallel_spawn": {
    "tasks": [
      { "label": "task1", "task": "Do this" },
      { "label": "task2", "task": "Do that" }
    ],
    "wait": "all"
  }
}
```

**等待策略：**
- `all` - 等待所有子代理完成
- `any` - 一旦有一个子代理完成就立即返回结果，其他子代理继续运行
- `race` - 一旦有任何一个子代理完成就立即返回结果

## 使用模式

### 并行研究（Parallel Research）

```json
{
  "parallel_spawn": {
    "tasks": [
      { "label": "web-search", "task": "Search X" },
      { "label": "docs-search", "task": "Find docs about X" }
    ],
    "wait": "all"
  }
}
```

### 链式工作流程（Chain Workflow）
1. 第一个子代理将数据写入 `context_store`。
2. 第二个子代理从 `context_store` 中读取数据。
3. 两个子代理都通过 `context_publish` 发送完成通知。

### 上下文管道（Context Pipeline）

```json
{
  "sessions_spawn": {
    "label": "processor",
    "task": "Process data",
    "contextSharing": "recent"
  }
}
```

## 自动通知（Auto-Announce）

子代理完成任务后会自动发送完成通知：
```
✅ Sub-agent completed: label
   task: ...
   result: ...
   runtime: Xs
```

无需进行额外的轮询（polling）操作！