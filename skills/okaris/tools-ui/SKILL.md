---
name: tools-ui
description: "Tool lifecycle UI components for React/Next.js from ui.inference.sh. Display tool calls: pending, progress, approval required, results. Capabilities: tool status, progress indicators, approval flows, results display. Use for: showing agent tool calls, human-in-the-loop approvals, tool output. Triggers: tool ui, tool calls, tool status, tool approval, tool results,"  agent tools, mcp tools ui, function calling ui, tool lifecycle, tool pending
---

# 工具用户界面组件

这些组件来自 [ui.inference.sh](https://ui.inference.sh)，用于管理工具的生命周期。

![工具用户界面组件](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgjw8atdxgkrsr8a2t5peq7b.jpeg)

## 快速入门

```bash
npx shadcn@latest add https://ui.inference.sh/r/tools.json
```

## 工具状态

| 状态 | 描述 |
|-------|-------------|
| `pending` | 请求调用工具，正在等待执行 |
| `running` | 工具正在执行中 |
| `approval` | 需要人工批准才能执行 |
| `success` | 工具执行成功 |
| `error` | 工具执行失败 |

## 组件

### 工具调用显示

```tsx
import { ToolCall } from "@/registry/blocks/tools/tool-call"

<ToolCall
  name="search_web"
  args={{ query: "latest AI news" }}
  status="running"
/>
```

### 工具结果

```tsx
import { ToolResult } from "@/registry/blocks/tools/tool-result"

<ToolResult
  name="search_web"
  result={{ results: [...] }}
  status="success"
/>
```

### 工具审批

```tsx
import { ToolApproval } from "@/registry/blocks/tools/tool-approval"

<ToolApproval
  name="send_email"
  args={{ to: "user@example.com", subject: "Hello" }}
  onApprove={() => executeTool()}
  onDeny={() => cancelTool()}
/>
```

## 完整示例

```tsx
import { ToolCall, ToolResult, ToolApproval } from "@/registry/blocks/tools"

function ToolDisplay({ tool }) {
  if (tool.status === 'approval') {
    return (
      <ToolApproval
        name={tool.name}
        args={tool.args}
        onApprove={tool.approve}
        onDeny={tool.deny}
      />
    )
  }

  if (tool.result) {
    return (
      <ToolResult
        name={tool.name}
        result={tool.result}
        status={tool.status}
      />
    )
  }

  return (
    <ToolCall
      name={tool.name}
      args={tool.args}
      status={tool.status}
    />
  )
}
```

## 工具卡片的样式设计

```tsx
<ToolCall
  name="read_file"
  args={{ path: "/src/index.ts" }}
  status="running"
  className="border-blue-500"
/>
```

## 工具图标

工具会根据其名称自动获取对应的图标：

| 图标模式 | 对应图标 |
|---------|------|
| `search*`, `find*` | 搜索 |
| `read*`, `get*` | 文件 |
| `write*`, `create*` | 铅笔 |
| `delete*`, `remove*` | 垃圾桶 |
| `send*`, `email*` | 邮件 |
| 默认 | 扳手 |

## 与 Agent 组件的集成

Agent 组件会自动管理工具的生命周期：

```tsx
import { Agent } from "@/registry/blocks/agent/agent"

<Agent
  proxyUrl="/api/inference/proxy"
  config={{
    core_app: { ref: 'openrouter/claude-sonnet-45@0fkg6xwb' },
    tools: [
      {
        name: 'search_web',
        description: 'Search the web',
        parameters: { query: { type: 'string' } },
        requiresApproval: true, // Enable approval flow
      },
    ],
  }}
/>
```

## 相关技能

```bash
# Full agent component (recommended)
npx skills add inference-sh/skills@agent-ui

# Chat UI blocks
npx skills add inference-sh/skills@chat-ui

# Widgets for tool results
npx skills add inference-sh/skills@widgets-ui
```

## 文档资料

- [向 Agent 添加工具](https://inference.sh/docs/agents/adding-tools) - 为 Agent 配置工具 |
- [人工参与流程](https://inference.sh/docs/runtime/human-in-the-loop) - 批准流程 |
- [工具审批机制](https://inference.sh/blog/tools/approval-gates) - 实现审批功能 |

组件文档：[ui.inference.sh/blocks/tools](https://ui.inference.sh/blocks/tools)