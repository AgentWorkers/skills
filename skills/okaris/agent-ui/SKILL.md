---
name: agent-ui
description: |
  Batteries-included agent component for React/Next.js from ui.inference.sh.
  One component with runtime, tools, streaming, approvals, and widgets built in.
  Capabilities: drop-in agent, human-in-the-loop, client-side tools, form filling.
  Use for: building AI chat interfaces, agentic UIs, SaaS copilots, assistants.
  Triggers: agent component, agent ui, chat agent, shadcn agent, react agent,
  agentic ui, ai assistant ui, copilot ui, inference ui, human in the loop
---

# 代理组件

该代理组件包含电池，源自 [ui.inference.sh](https://ui.inference.sh)。

## 快速入门

```bash
# Install the agent component
npx shadcn@latest add https://ui.inference.sh/r/agent.json

# Add the SDK for the proxy route
npm install @inferencesh/sdk
```

## 设置

### 1. API 代理路由（Next.js）

```typescript
// app/api/inference/proxy/route.ts
import { route } from '@inferencesh/sdk/proxy/nextjs';
export const { GET, POST, PUT } = route;
```

### 2. 环境变量

```bash
# .env.local
INFERENCE_API_KEY=inf_...
```

### 3. 使用该组件

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

## 功能

| 功能 | 描述 |
|---------|-------------|
| 内置运行时环境 | 无需后端逻辑 |
| 工具生命周期 | 待定：包括进度、审批、结果等环节 |
| 人工参与流程 | 内置审批流程 |
| 小部件 | 从代理响应中生成的声明式 JSON UI |
| 流式传输 | 实时令牌传输 |
| 客户端工具 | 在浏览器中运行的工具 |

## 客户端工具示例

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

## 属性

| 属性 | 类型 | 描述 |
|------|------|-------------|
| `proxyUrl` | string | API 代理端点 |
| `name` | string | 代理名称（可选） |
| `config` | AgentConfig | 代理配置 |
| `allowFiles` | boolean | 是否允许文件上传 |
| `allowImages` | boolean | 是否允许图片上传 |

## 相关技能

```bash
# Chat UI building blocks
npx skills add inference-sh/agent-skills@chat-ui

# Declarative widgets from JSON
npx skills add inference-sh/agent-skills@widgets-ui

# Tool lifecycle UI
npx skills add inference-sh/agent-skills@tools-ui
```

## 文档资料

- [代理概述](https://inference.sh/docs/agents/overview) - 构建 AI 代理 |
- [代理 SDK](https://inference.sh/docs/api/agent/overview) - 程序化代理控制 |
- [人工参与流程](https://inference.sh/docs/runtime/human-in-the-loop) - 审批流程 |
- [生成 UI 的代理](https://inference.sh/blog/ux/generative-ui) - 构建生成式 UI |
- [代理用户体验最佳实践](https://inference.sh/blog/ux/agent-ux-patterns) - 最佳使用方法 |

组件文档：[ui.inference.sh/blocks/agent](https://ui.inference.sh/blocks/agent)