---
name: copilotkit-agent-patterns
description: 用于构建与 CopilotKit 集成的 AI 代理的模式。这些模式适用于设计代理架构、实现 AG-UI 事件流、管理代理与 UI 之间的共享状态、添加人工干预检查点，或从代理中生成用户界面（UI）。这些模式会在涉及 CopilotKit 运行时、BuiltInAgent 或 AG-UI 协议的代理实现任务中被触发。
license: MIT
metadata:
  author: copilotkit
  version: "2.0.0"
---
# CopilotKit 代理模式

这些模式涵盖了构建与 CopilotKit 连接的 AI 代理的架构和实现方法。文件中包含了 20 条规则，分为 5 个类别，并根据规则的重要性进行了排序。

## 适用场景

在以下情况下请参考这些指南：
- 设计用于 CopilotKit 集成的代理架构
- 实现 AG-UI 协议的事件流处理
- 管理代理与前端之间的状态同步
- 在代理工作流程中添加人工干预的检查点
- 发送用于在前端渲染生成式用户界面的工具调用

## 规则类别及优先级

| 优先级 | 类别 | 重要性 | 前缀 |
|--------|--------|---------|--------|
| 1      | 代理架构 | 关键      | `architecture-` |
| 2      | AG-UI 协议 | 高        | `agui-`   |
| 3      | 状态管理 | 高        | `state-`   |
| 4      | 人工干预   | 中等      | `hitl-`   |
| 5      | 生成式 UI   | 中等      | `genui-`   |

## 快速参考

### 1. 代理架构（关键）

- `architecture-built-in-agent`：对于简单的代理，使用来自 @copilotkit/runtime/v2 的 BuiltInAgent。
- `architecture-model-resolution`：使用提供者/模型字符串格式来选择模型。
- `architecture-max-steps`：设置 maxSteps 以防止工具调用陷入无限循环。
- `architecture-mcp-servers`：配置 MCP 端点以访问外部工具。

### 2. AG-UI 协议（高）

- `agui-event-ordering`：按正确的顺序发送事件（开始 -> 内容 -> 结束）。
- `agui-text-streaming`：逐步发送文本，而不是一次性发送完整内容。
- `agui-tool-call-lifecycle`：遵循完整的工具调用事件生命周期。
- `agui-state-snapshot`：发送 STATE_SNAPSHOT 事件以进行前端同步。
- `agui-error-events`：在发生错误时始终发送错误事件。

### 3. 状态管理（高）

- `state-snapshot-frequency`：在有意义的检查点发送状态快照。
- `state-minimal-payload`：保持状态快照的简洁性和可序列化性。
- `state-conflict-resolution`：优雅地处理双向状态冲突。
- `state-thread-isolation`：按线程隔离状态，而不是按代理隔离。

### 4. 人工干预（中等）

- `hitl-approval-gates`：使用工具调用来实现审批流程，而不是自定义事件。
- `hitl-timeout-fallback`：始终设置超时并配置回退行为。
- `hitl-context-in-prompt`：在提示中提供足够的上下文信息供用户决策。
- `hitl-resume-state`：在获得批准后恢复时保留完整的状态。

### 5. 生成式 UI（中等）

- `genui-tool-call-render`：发送与前端 useRenderTool 对应的工具调用。
- `genui-streaming-args`：逐步发送工具参数以实现实时 UI 更新。
- `genui-activity-messages`：使用文本消息进行非工具相关的状态更新。

## 使用方法

有关详细说明和代码示例，请阅读相应的规则文件：

```
rules/architecture-built-in-agent.md
rules/agui-event-ordering.md
```

## 完整文档

如需查看包含所有规则的完整指南，请参阅 `AGENTS.md`。