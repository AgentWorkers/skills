---
name: chat-ui
description: |
  Chat UI building blocks for React/Next.js from ui.inference.sh.
  Components: container, messages, input, typing indicators, avatars.
  Capabilities: chat interfaces, message lists, input handling, streaming.
  Use for: building custom chat UIs, messaging interfaces, AI assistants.
  Triggers: chat ui, chat component, message list, chat input, shadcn chat,
  react chat, chat interface, messaging ui, conversation ui, chat building blocks
---

# 聊天用户界面组件

这些聊天组件来自 [ui.inference.sh](https://ui.inference.sh)。

## 快速入门

```bash
# Install chat components
npx shadcn@latest add https://ui.inference.sh/r/chat.json
```

## 组件

### 聊天容器

```tsx
import { ChatContainer } from "@/registry/blocks/chat/chat-container"

<ChatContainer>
  {/* messages go here */}
</ChatContainer>
```

### 消息

```tsx
import { ChatMessage } from "@/registry/blocks/chat/chat-message"

<ChatMessage
  role="user"
  content="Hello, how can you help me?"
/>

<ChatMessage
  role="assistant"
  content="I can help you with many things!"
/>
```

### 聊天输入框

```tsx
import { ChatInput } from "@/registry/blocks/chat/chat-input"

<ChatInput
  onSubmit={(message) => handleSend(message)}
  placeholder="Type a message..."
  disabled={isLoading}
/>
```

### 输入状态指示器

```tsx
import { TypingIndicator } from "@/registry/blocks/chat/typing-indicator"

{isTyping && <TypingIndicator />}
```

## 完整示例

```tsx
import {
  ChatContainer,
  ChatMessage,
  ChatInput,
  TypingIndicator,
} from "@/registry/blocks/chat"

export function Chat() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = async (content: string) => {
    setMessages(prev => [...prev, { role: 'user', content }])
    setIsLoading(true)
    // Send to API...
    setIsLoading(false)
  }

  return (
    <ChatContainer>
      {messages.map((msg, i) => (
        <ChatMessage key={i} role={msg.role} content={msg.content} />
      ))}
      {isLoading && <TypingIndicator />}
      <ChatInput onSubmit={handleSend} disabled={isLoading} />
    </ChatContainer>
  )
}
```

## 消息类型

| 类型 | 说明 |
|------|-------------|
| `user` | 用户发送的消息（右对齐显示） |
| `assistant` | 人工智能生成的回复（左对齐显示） |
| `system` | 系统发送的消息（居中显示） |

## 样式设计

这些组件使用了 Tailwind CSS 和 shadcn/ui 的设计规范：

```tsx
<ChatMessage
  role="assistant"
  content="Hello!"
  className="bg-muted"
/>
```

## 相关技能

```bash
# Full agent component (recommended)
npx skills add inference-sh/agent-skills@agent-ui

# Declarative widgets
npx skills add inference-sh/agent-skills@widgets-ui

# Markdown rendering
npx skills add inference-sh/agent-skills@markdown-ui
```

## 文档资料

- [与智能助手进行聊天](https://inference.sh/docs/agents/chatting) - 如何构建聊天界面 |
- [智能助手的用户体验设计模式](https://inference.sh/blog/ux/agent-ux-patterns) - 聊天界面的最佳实践 |
- [实时流式响应](https://inference.sh/blog/observability/streaming) - 实时流式消息传递技术

组件文档：[ui.inference.sh/blocks/chat](https://ui.inference.sh/blocks/chat)