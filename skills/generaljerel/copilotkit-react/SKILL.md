---
name: copilotkit-react-patterns
description: >
  **CopilotKit React最佳实践：适用于使用CopilotKit钩子（useAgent、useFrontendTool、useRenderTool、useCopilotAction、useCopilotReadable）以及相关组件（CopilotChat、CopilotSidebar、CopilotPopup）的应用程序。**  
  这些最佳实践适用于编写、审查或重构React代码的场景，尤其是在涉及代理集成（agent integration）、工具渲染（tool rendering）、共享状态（shared state）或生成式用户界面（generative UI）的任务中。
license: MIT
metadata:
  author: copilotkit
  version: "2.0.0"
---
# CopilotKit React 模式

使用 CopilotKit 构建智能型 React 应用程序的最佳实践。包含 25 条规则，分为 6 个类别，根据规则对代码生成和重构的影响进行优先级排序。涵盖了 v1 (`@copilotkit/react-core`) 和 v2 (`@copilotkit/react-core/v2`) API。

## 适用场景

在以下情况下请参考这些指南：
- 在 React 应用程序中设置 `CopilotKit` 提供者
- 使用代理钩子（`useAgent`、`useFrontendTool`、`useCopilotAction`）
- 从代理端渲染工具调用或自定义消息
- 通过 `useCopilotReadable` 或 `useCoAgent` 管理 UI 与代理之间的共享状态
- 使用 `CopilotChat`、`CopilotSidebar` 或 `CopilotPopup` 构建聊天界面
- 配置主动代理辅助的建议

## 规则类别及优先级

| 优先级 | 类别 | 影响 | 前缀 |
|----------|----------|--------|--------|
| 1 | 提供者设置 | 关键 | `provider-` |
| 2 | 代理钩子 | 高 | `agent-` |
| 3 | 工具渲染 | 高 | `tool-` |
| 4 | 上下文与状态 | 中等 | `state-` |
| 5 | 聊天界面 | 中等 | `ui-` |
| 6 | 建议 | 低 | `suggestions-` |

## 快速参考

### 1. 提供者设置（关键）

- `provider-runtime-url` - 始终配置 `runtimeUrl` 以连接到代理后端
- `provider-single-endpoint` - 配置用于 CoAgent 路由的代理属性
- `provider-nested-providers` - 通过嵌套的 CopilotKit 提供者来管理代理配置
- `provider-tool-registration` - 尽可能通过钩子在提供者内部注册工具，而不是作为属性

### 2. 代理钩子（高）

- `agent-use-agent-updates` - 指定更新订阅以避免不必要的重新渲染
- `agent-agent-id` - 在运行多个代理时始终传递 `agentId`
- `agent-context-description` - 为 `useCopilotReadable` 编写描述性的上下文值
- `agent-frontend-tool-deps` - 声明 `useFrontendTool` 的依赖数组
- `agent-stable-tool-handlers` - 对工具处理函数使用 ` useCallback`

### 3. 工具渲染（高）

- `tool-typed-args` - 为 `useRenderTool` 参数定义 Zod 模式（v2）
- `tool-status-handling` - 处理所有三种工具调用状态（进行中、执行中、已完成）
- `tool-wildcard-fallback` - 为未知工具注册通配符渲染器作为备用方案
- `tool-render-vs-frontend` - 使用 `useRenderTool` 仅用于显示，使用 `useFrontendTool` 用于副作用
- `tool-component-hook` - 使用 `useFrontendTool` 的 `render` 属性进行简单组件渲染

### 4. 上下文与状态（中等）

- `state-minimal-context` - 仅向代理提供相关上下文，而不是整个应用的状态
- `state-structured-values` - 在 `useCopilotReadable` 中使用结构化对象，而不是序列化字符串
- `state-context-granularity` - 按领域将上下文分割为多个 `useCopilotReadable` 调用
- `state-avoid-stale-closures` - 在工具处理函数中使用函数式状态更新

### 5. 聊天界面（中等）

- `ui-chat-layout` - 选择 `CopilotSidebar` 用于持久聊天，`CopilotPopup` 用于按需聊天
- `ui-custom-labels` - 始终自定义标签，而不是使用默认值
- `ui-welcome-screen` - 提供带有建议提示的欢迎界面
- `ui-input-mode` - 根据您的使用场景选择合适的 `inputMode`

### 6. 建议（低）

- `suggestions-configure` - 使用 `useConfigureSuggestions`（v2）或 `useCopilotChatSuggestions`（v1）
- `suggestions-context-driven` - 提供丰富的上下文以确保建议的相关性
- `suggestions-loading-state` - 通过 `useSuggestions`（v2）处理建议的加载状态

## 使用方法

请阅读各个规则文件以获取详细说明和代码示例：

```
rules/provider-runtime-url.md
rules/agent-use-agent-updates.md
rules/tool-typed-args.md
```

每个规则文件包含：
- 该规则重要性的简要说明
- 错误的代码示例及其解释
- 正确的代码示例及其解释
- 额外的上下文和参考资料

## 完整编译文档

有关所有规则的完整指南：`AGENTS.md`