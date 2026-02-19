---
name: agent-ui
description: "Batteries-included agent component for React/Next.js from ui.inference.sh. One component with runtime, tools, streaming, approvals, and widgets built in. Capabilities: drop-in agent, human-in-the-loop, client-side tools, form filling. Use for: building AI chat interfaces, agentic UIs, SaaS copilots, assistants. Triggers: agent component, agent ui, chat agent, shadcn agent, react agent,"  agentic ui, ai assistant ui, copilot ui, inference ui, human in the loop
---

# 代理组件（Agent Component）

该代理组件包含电池，源自 [ui.inference.sh](https://ui.inference.sh)。

![代理组件](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgvftp7hb8wby7z66fvs9asd.jpeg)

## 快速入门

```bash
# Install the agent component
npx shadcn@latest add https://ui.inference.sh/r/agent.json

# Add the SDK for the proxy route
npm install @inferencesh/sdk
```

## 设置（Setup）

### 1. API 代理路由（API Proxy Route）（Next.js）

```typescript
// app/api/inference/proxy/route.ts
import { route } from '@inferencesh/sdk/proxy/nextjs';
export const { GET, POST, PUT } = route;
```

### 2. 环境变量（Environment Variables）

```bash
# .env.local
INFERENCE_API_KEY=inf_...
```

### 3. 使用该组件（Using the Component）

```tsx
import { Agent } from "@/registry/blocks/agent/agent"

export default function Page() {
  return (
    <Agent
      proxyUrl="/api/inference/proxy"
      agentConfig={{
        core_app: { ref: 'openrouter/claude-haiku-45@0fkg6xwb' },
        description: 'a helpful ai assistant',
        system_prompt: 'you are helpful.',
      }}
    />
  )
}
```

## 功能特性（Features）

| 功能 | 描述 |
|---------|-------------|
| 内置运行时环境（Runtime Included） | 无需后端逻辑 |
| 工具生命周期管理（Tool Lifecycle Management） | 正在开发中，包括进度跟踪、审批流程及结果展示 |
| 人工干预机制（Human-in-the-Loop） | 内置的审批流程 |
| 小部件（Widgets） | 从代理响应中生成的 JSON 格式用户界面 |
| 流式数据传输（Streaming） | 实时数据流传输 |
| 客户端工具（Client-side Tools） | 可在浏览器中运行的工具 |

## 客户端工具示例（Client-Side Tools Example）

```tsx
import { Agent } from "@/registry/blocks/agent/agent"
import { createScopedTools } from "./blocks/agent/lib/client-tools"

const formRef = useRef<HTMLFormElement>(null)
const scopedTools = createScopedTools(formRef)

<Agent
  proxyUrl="/api/inference/proxy"
  config={{
    core_app: { ref: 'openrouter/claude-haiku-45@0fkg6xwb' },
    tools: scopedTools,
    system_prompt: 'You can fill forms using scan_ui and fill_field tools.',
  }}
/>
```

## 属性（Props）

| 属性 | 类型 | 描述 |
|------|------|-------------|
| `proxyUrl` | string | API 代理端点 |
| `name` | string | 代理名称（可选） |
| `config` | AgentConfig | 代理配置信息 |
| `allowFiles` | boolean | 是否允许上传文件 |
| `allowImages` | boolean | 是否允许上传图片 |

## 相关技能（Related Skills）

```bash
# Chat UI building blocks
npx skills add inference-sh/skills@chat-ui

# Declarative widgets from JSON
npx skills add inference-sh/skills@widgets-ui

# Tool lifecycle UI
npx skills add inference-sh/skills@tools-ui
```

## 文档资料（Documentation）

- [代理组件概述](https://inference.sh/docs/agents/overview) - 了解 AI 代理的构建方式 |
- [代理 SDK](https://inference.sh/docs/api/agent/overview) - 程序化控制代理的方法 |
- [人工干预机制](https://inference.sh/docs/runtime/human-in-the-loop) - 代理的审批流程 |
- [生成式用户界面](https://inference.sh/blog/ux/generative-ui) - 如何构建生成式用户界面 |
- [代理用户体验最佳实践](https://inference.sh/blog/ux/agent-ux-patterns) - 用户体验设计指南 |

组件详细文档：[ui.inference.sh/blocks/agent](https://ui.inference.sh/blocks/agent)