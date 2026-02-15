---
name: ai-sdk-ui
description: |
  Build React chat interfaces with Vercel AI SDK v6. Covers useChat/useCompletion/useObject hooks, message parts structure, tool approval workflows, and 18 UI error solutions. Prevents documented issues with React Strict Mode, concurrent requests, stale closures, and tool approval edge cases.

  Use when: implementing AI chat UIs, migrating v5→v6, troubleshooting "useChat failed to parse stream", "stale body values", "React maximum update depth", "Cannot read properties of undefined (reading 'state')", or tool approval workflow errors.
user-invocable: true
---

# AI SDK UI - 前端 React Hooks

这些 React Hooks 用于基于 Vercel AI SDK v6 的 AI 驱动用户界面。

**版本**: AI SDK v6.0.42（稳定版）
**框架**: React 18+/19, Next.js 14+/15+
**最后更新**: 2026-01-20

---

## AI SDK v6 稳定版（2026年1月）

**状态**: 稳定发布
**最新版本**: ai@6.0.42, @ai-sdk/react@3.0.44, @ai-sdk/openai@3.0.7
**迁移**: 从 v5 升级到 v6 的改动较小

### v6 的新 UI 功能

**1. 消息部分结构（重大变更）**
在 v6 中，消息内容现在通过 `.parts` 数组访问，而不是 `.content`：

```tsx
// ❌ v5 (OLD)
{messages.map(m => (
  <div key={m.id}>{m.content}</div>
))}

// ✅ v6 (NEW)
{messages.map(m => (
  <div key={m.id}>
    {m.parts.map((part, i) => {
      if (part.type === 'text') return <span key={i}>{part.text}</span>;
      if (part.type === 'tool-invocation') return <ToolCall key={i} tool={part} />;
      if (part.type === 'file') return <FilePreview key={i} file={part} />;
      return null;
    })}
  </div>
))}
```

**部分类型**：
- `text` - 包含 `.text` 属性的文本内容
- `tool-invocation` - 包含 `.toolName`, `.args`, `.result` 的工具调用
- `file` - 包含 `.mimeType`, `.data` 的文件附件
- `reasoning` - 模型推理结果（如果可用）
- `source` - 来源引用

**3. 代理集成**
使用 `InferAgentUIMessage<typename agent>` 进行类型安全的代理消息传递：

```tsx
import { useChat } from '@ai-sdk/react';
import type { InferAgentUIMessage } from 'ai';
import { myAgent } from './agent';

export default function AgentChat() {
  const { messages, sendMessage } = useChat<InferAgentUIMessage<typeof myAgent>>({
    api: '/api/chat',
  });
  // messages are now type-checked against agent schema
}
```

**4. 工具审批工作流程（人工干预）**
在执行工具之前请求用户确认：

```tsx
import { useChat } from '@ai-sdk/react';
import { useState } from 'react';

export default function ChatWithApproval() {
  const { messages, sendMessage, addToolApprovalResponse } = useChat({
    api: '/api/chat',
  });

  const handleApprove = (toolCallId: string) => {
    addToolApprovalResponse({
      toolCallId,
      approved: true,  // or false to deny
    });
  };

  return (
    <div>
      {messages.map(message => (
        <div key={message.id}>
          {message.toolInvocations?.map(tool => (
            tool.state === 'awaiting-approval' && (
              <div key={tool.toolCallId}>
                <p>Approve tool call: {tool.toolName}?</p>
                <button onClick={() => handleApprove(tool.toolCallId)}>
                  Approve
                </button>
                <button onClick={() => addToolApprovalResponse({
                  toolCallId: tool.toolCallId,
                  approved: false
                })}>
                  Deny
                </button>
              </div>
            )
          ))}
        </div>
      ))}
    </div>
  );
}
```

**5. 自动提交功能**
处理审批后自动继续对话：

```tsx
import { useChat, lastAssistantMessageIsCompleteWithApprovalResponses } from '@ai-sdk/react';

export default function AutoSubmitChat() {
  const { messages, sendMessage } = useChat({
    api: '/api/chat',
    sendAutomaticallyWhen: lastAssistantMessageIsCompleteWithApprovalResponses,
    // Automatically resubmit after all approval responses provided
  });
}
```

**6. 聊天中的结构化输出**
在调用工具时生成结构化数据（之前仅在 `useObject` 中可用）：

```tsx
import { useChat } from '@ai-sdk/react';
import { z } from 'zod';

const schema = z.object({
  summary: z.string(),
  sentiment: z.enum(['positive', 'neutral', 'negative']),
});

export default function StructuredChat() {
  const { messages, sendMessage } = useChat({
    api: '/api/chat',
    // Server can now stream structured output with chat messages
  });
}
```

---

## useChat Hook - 从 v4 升级到 v5 的重大变更

**重要提示**: 在 v5 中，`useChat` 不再管理输入状态！

**v4（旧版本 - 请勿使用）**:
```tsx
const { messages, input, handleInputChange, handleSubmit, append } = useChat();

<form onSubmit={handleSubmit}>
  <input value={input} onChange={handleInputChange} />
</form>
```

**v5（新版本）**:
```tsx
const { messages, sendMessage } = useChat();
const [input, setInput] = useState('');

<form onSubmit={(e) => {
  e.preventDefault();
  sendMessage({ content: input });
  setInput('');
}}>
  <input value={input} onChange={(e) => setInput(e.target.value)} />
</form>
```

**v5 的变更总结**：
1. **移除了输入管理**：`input`, `handleInputChange`, `handleSubmit` 不再存在
2. **`append()` → `sendMessage()`：新的消息发送方法
3. **`onResponse` 被移除**：改用 `onFinish`
4. **`initialMessages` → 转为 `messages` 属性进行完全控制
5. **`maxSteps` 被移除**：仅在服务器端处理

请参阅 `references/use-chat-migration.md` 以获取完整的迁移指南。

---

## useAssistant Hook（已弃用）

> **⚠️ 已弃用通知**：`useAssistant` 自 AI SDK v5 开始已弃用。OpenAI Assistants API v2 将在 2026 年 8 月 26 日停止支持。对于新项目，请改用带有自定义后端逻辑的 `useChat`。
> 有关迁移指南，请参阅 **openai-assistants** 技能文档。

该 Hook 可用于与兼容 OpenAI 的助手 API 进行交互，并自动管理 UI 状态。

**导入方式**:
```tsx
import { useAssistant } from '@ai-sdk/react';
```

**基本用法**:
```tsx
'use client';
import { useAssistant } from '@ai-sdk/react';
import { useState, FormEvent } from 'react';

export default function AssistantChat() {
  const { messages, sendMessage, isLoading, error } = useAssistant({
    api: '/api/assistant',
  });
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    sendMessage({ content: input });
    setInput('');
  };

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          <strong>{m.role}:</strong> {m.content}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
        />
      </form>
      {error && <div>{error.message}</div>}
    </div>
  );
}
```

**使用场景**：
- 构建基于 OpenAI Assistant 的 UI
- 管理助手线程和运行
- 流式显示助手响应并管理 UI 状态
- 集成文件搜索和代码解释功能

有关完整的 API 参考，请参阅官方文档：https://ai-sdk.dev/docs/reference/ai-sdk-ui/use-assistant

---

## 常见 UI 错误及解决方法

请参阅 `references/top-ui-errors.md` 以获取完整文档。以下是部分常见错误及其解决方法：

### 1. useChat 无法解析流数据

**错误**: `SyntaxError: JSON 中在位置 X 处出现意外字符`

**原因**: API 路由返回的流数据格式不正确。

**解决方法**:
```typescript
// ✅ CORRECT
return result.toDataStreamResponse();

// ❌ WRONG
return new Response(result.textStream);
```

### 2. useChat 无响应

**原因**: API 路由无法正确传输数据流。

**解决方法**:
```typescript
// App Router - use toDataStreamResponse()
export async function POST(req: Request) {
  const result = streamText({ /* ... */ });
  return result.toDataStreamResponse(); // ✅
}

// Pages Router - use pipeDataStreamToResponse()
export default async function handler(req, res) {
  const result = streamText({ /* ... */ });
  return result.pipeDataStreamToResponse(res); // ✅
}
```

### 3. 部署后流数据传输失败

**原因**: 部署平台对响应进行了缓冲。

**解决方法**: Vercel 会自动检测流数据传输。其他平台可能需要额外配置。

### 4. useChat 显示的文本内容过时

**原因**: `body` 选项仅在首次渲染时被捕获。

**解决方法**:
```typescript
// ❌ WRONG - body captured once
const { userId } = useUser();
const { messages } = useChat({
  body: { userId },  // Stale!
});

// ✅ CORRECT - use controlled mode
const { userId } = useUser();
const { messages, sendMessage } = useChat();

sendMessage({
  content: input,
  data: { userId },  // Fresh on each send
});
```

### 5. React 最大更新深度限制

**原因**: `useEffect` 中出现了无限循环。

**解决方法**:
```typescript
// ❌ WRONG
useEffect(() => {
  saveMessages(messages);
}, [messages, saveMessages]); // saveMessages triggers re-render!

// ✅ CORRECT
useEffect(() => {
  saveMessages(messages);
}, [messages]); // Only depend on messages
```

有关其他 13 种常见错误的详细信息，请参阅 `references/top-ui-errors.md`（共记录了 18 种错误）。

---

## 流数据传输的最佳实践

### 性能优化

**始终使用流数据传输以提升用户体验**:
```tsx
// ✅ GOOD - Streaming (shows tokens as they arrive)
const { messages } = useChat({ api: '/api/chat' });

// ❌ BAD - Non-streaming (user waits for full response)
const response = await fetch('/api/chat', { method: 'POST' });
```

### 用户界面设计模式

**显示加载状态**:
```tsx
{isLoading && <div>AI is typing...</div>}
```

**提供停止按钮**:
```tsx
{isLoading && <button onClick={stop}>Stop</button>}
```

**自动滚动到最新消息**:
```tsx
useEffect(() => {
  messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
}, [messages]);
```

**加载时禁用输入**:
```tsx
<input disabled={isLoading} />
```

有关全面的最佳实践，请参阅 `references/streaming-patterns.md`。

---

## React 严格模式的注意事项

React 严格模式会故意重复执行某些效果（effects）以捕获错误。当在效果函数中使用 `useChat` 或 `useCompletion`（如自动恢复、初始消息处理）时，需要注意避免重复执行，以防止 API 调用重复和令牌浪费。

**问题**:
```tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { useEffect } from 'react';

export default function Chat() {
  const { messages, sendMessage, resumeStream } = useChat({
    api: '/api/chat',
    resume: true,
  });

  useEffect(() => {
    // ❌ Triggers twice in strict mode → two concurrent streams
    sendMessage({ content: 'Hello' });
    // or
    resumeStream();
  }, []);
}
```

**解决方法**:
```tsx
// ✅ Use ref to track execution
import { useRef } from 'react';

const hasSentRef = useRef(false);

useEffect(() => {
  if (hasSentRef.current) return;
  hasSentRef.current = true;

  sendMessage({ content: 'Hello' });
}, []);

// For resumeStream specifically:
const hasResumedRef = useRef(false);

useEffect(() => {
  if (!autoResume || hasResumedRef.current || status === 'streaming') return;
  hasResumedRef.current = true;
  resumeStream();
}, [autoResume, resumeStream, status]);
```

**原因**: React 严格模式会重复执行效果函数。由于 SDK 未对并发请求进行处理，因此两次调用会创建不同的数据流，导致状态更新冲突。

**影响**: 重复显示消息、令牌使用量增加、可能出现错误：“Cannot read properties of undefined (reading ‘state’)”。

**来源**: [GitHub 问题 #7891](https://github.com/vercel/ai/issues/7891), [问题 #6166](https://github.com/vercel/ai/issues/6166)

---

## 何时使用此技能

### 适用场景**：
- 构建 React 聊天界面
- 在 UI 中实现 AI 完成功能
- 将 AI 响应以流数据形式传输到前端
- 开发基于 Next.js 的 AI 应用程序
- 管理聊天消息状态
- 在 UI 中显示工具调用结果
- 管理 AI 相关的文件附件
- 从 v4 升级到 v5（使用 UI Hooks）
- 遇到 `useChat` 或 `useCompletion` 相关错误

### 不适用场景**：
- 需要后端 AI 功能时，请使用 **ai-sdk-core**
- 构建非 React 前端（如 Svelte、Vue）时，请参阅官方文档
- 需要生成式 UI 或 RSC 功能时，请参阅 https://ai-sdk.dev/docs/ai-sdk-rsc
- 开发原生应用程序时，需要使用其他 SDK

### 相关技能**：
- **ai-sdk-core** - 提供后端文本生成、结构化输出、工具支持和代理功能
- 结合使用这两个技能可构建全栈 AI 应用程序

---

## 包版本

**推荐版本（v6）**:
```json
{
  "dependencies": {
    "ai": "^6.0.8",
    "@ai-sdk/react": "^3.0.6",
    "@ai-sdk/openai": "^3.0.2",
    "react": "^18.3.0",
    "zod": "^3.24.2"
  }
}
```

**旧版本（v5）**:
```json
{
  "dependencies": {
    "ai": "^5.0.99",
    "@ai-sdk/react": "^1.0.0",
    "@ai-sdk/openai": "^2.0.68"
  }
}
```

**版本说明**：
- AI SDK v6.0.6（稳定版，2026年1月发布） - 推荐用于新项目
- AI SDK v5.x（旧版本） - 仍受支持，但不再接收新功能
- 支持 React 18.3+ / React 19
- 推荐使用 Next.js 14+/15+
- 推荐使用 Zod 3.24.2+ 进行模式验证

---

## 官方文档链接

**核心 UI Hooks**：
- AI SDK UI 概述：https://ai-sdk.dev/docs/ai-sdk-ui/overview
- useChat：https://ai-sdk.dev/docs/ai-sdk-ui/chatbot
- useCompletion：https://ai-sdk.dev/docs/ai-sdk-ui/completion
- useObject：https://ai-sdk.dev/docs/ai-sdk-ui/object-generation

**高级主题（仅提供链接）**：
- 生成式 UI（RSC）：https://ai-sdk.dev/docs/ai-sdk-rsc/overview
- 流数据协议：https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocols
- 消息元数据：https://ai-sdk.dev/docs/ai-sdk-ui/message-metadata

**Next.js 集成**：
- Next.js 应用程序路由器：https://ai-sdk.dev/docs/getting-started/nextjs-app-router
- Next.js 页面路由器：https://ai-sdk.dev/docs/getting-started/nextjs-pages-router

**迁移与故障排除**：
- 从 v4 升级到 v5 的指南：https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0
- 故障排除：https://ai-sdk.dev/docs/troubleshooting
- 常见问题：https://ai-sdk.dev/docs/troubleshooting/common-issues

**Vercel 部署**：
- Vercel 函数：https://vercel.com/docs/functions
- 在 Vercel 上使用流数据传输：https://vercel.com/docs/functions/streaming

---

## 模板

该技能在 `templates/` 目录下包含以下模板：

1. **use-chat-basic.tsx** - 基本聊天功能（支持手动输入，v5 模式）
2. **use-chat-tools.tsx** - 带有工具调用功能的聊天界面
3. **use-chat-attachments.tsx** - 支持文件附件的聊天界面
4. **use-completion-basic.tsx** - 基本文本补全功能
5. **use-object-streaming.tsx** - 流式传输结构化数据
6. **nextjs-chat-app-router.tsx** - 完整的 Next.js 应用程序路由器示例
7. **nextjs-chat-pages-router.tsx** - 完整的 Next.js 页面路由器示例
8. **nextjs-api-route.ts** - 适用于应用程序和页面路由器的 API 路由配置
9. **message-persistence.tsx** - 保存/加载聊天历史记录
10. **custom-message-renderer.tsx** - 支持 Markdown 的自定义消息组件
11. **package.json** - 依赖项配置文件

## 参考文档

请参阅 `references/` 目录中的文档：

- **use-chat-migration.md** - 完整的从 v4 升级到 v5 的迁移指南
- **streaming-patterns.md** - UI 流数据传输的最佳实践
- **top-ui-errors.md** - 18 种常见 UI 错误及其解决方法
- **nextjs-integration.md** - Next.js 集成指南
- **links-to-official-docs.md** - 官方文档的链接集合

---

**生产环境测试**：已在 WordPress Auditor （https://wordpress-auditor.webfonts.workers.dev）上通过测试
**最后验证时间**: 2026-01-20 | **技能版本**: 3.1.0 | **更新内容**：升级到 AI SDK v6.0.42（包含 19 个修复补丁）。新增了关于 React 严格模式的章节，扩展了对问题 #7（过时数据问题）的解决方案，以及 6 个新问题的修复：`resume+onFinish` 导致的错误 (#13)、并发发送请求导致的状态损坏 (#14)、工具审批回调的边缘情况 (#15)、提前停止时出现的 ZodError (#16)、`convertToModelMessages` 工具审批错误 (#17)、`undefined id` 导致的无限循环 (#18)。错误总数从 12 个增加到 18 个。