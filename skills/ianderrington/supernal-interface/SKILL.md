---
name: supernal-interface
description: 通用AI接口框架，用于实现应用程序的可AI控制功能。适用于添加AI工具装饰器、配置聊天适配器、创建可被AI调用的函数，或集成CopilotKit等场景。
---

# Supernal Interface - 人工智能可控性框架

## 安装

```bash
npm install @supernal/interface
```

## 核心概念

通过装饰函数，人工智能能够以完全类型安全的方式调用这些函数。

## 快速入门

### 1. 装饰函数

```typescript
import { Tool } from '@supernal/interface';

class TodoApp {
  @Tool({
    name: 'add_todo',
    description: 'Add a new todo item',
    category: 'productivity'
  })
  async addTodo(text: string): Promise<Todo> {
    return this.db.create({ text, done: false });
  }

  @Tool({
    name: 'complete_todo',
    description: 'Mark a todo as complete'
  })
  async completeTodo(id: string): Promise<void> {
    await this.db.update(id, { done: true });
  }
}
```

### 2. 设置适配器

```typescript
import { createCopilotKitAdapter, ChatUIProvider } from '@supernal/interface';

const adapter = createCopilotKitAdapter({
  autoRegisterTools: true,
  autoRegisterReadables: true
});

function App() {
  return (
    <ChatUIProvider adapter={adapter}>
      <YourApp />
    </ChatUIProvider>
  );
}
```

### 3. 安装完成

现在，人工智能助手可以发现并调用你装饰过的函数了。

## 装饰器

| 装饰器 | 用途 |
|-----------|---------|
| `@Tool` | 将函数暴露为可供人工智能调用的工具 |
| `@ToolProvider` | 包含多个工具的类 |
| `@Component` | 具备人工智能上下文的 React 组件 |

## 适配器

### CopilotKit（推荐使用）
```typescript
import { createCopilotKitAdapter } from '@supernal/interface';

const adapter = createCopilotKitAdapter({
  autoRegisterTools: true
});
```

### 自定义适配器
```typescript
import { ChatUIAdapter } from '@supernal/interface';

class MyAdapter implements ChatUIAdapter {
  name = 'my-adapter';
  registerTools(tools) { /* convert to your format */ }
  render(props) { return <MyChat {...props} />; }
}
```

## React Hooks

```typescript
import { useToolBinding, usePersistedState, useChatWithContext } from '@supernal/interface';

// Bind a tool to component state
const [todos, setTodos] = useToolBinding('todos', []);

// Persist state across sessions
const [prefs, setPrefs] = usePersistedState('user-prefs', defaults);

// Chat with app context
const { messages, send } = useChatWithContext();
```

## 存储适配器

```typescript
import { StateManager, LocalStorageAdapter } from '@supernal/interface/storage';

const storage = StateManager.getInstance('myapp', new LocalStorageAdapter());
await storage.setState('user', { name: 'Alice' });
```

## 测试

```typescript
import { GherkinParser, TestRunner } from '@supernal/interface/testing';

const feature = GherkinParser.parseFeature(gherkinText);
const tests = await TestRunner.generateTests({ framework: 'jest' });
```

## 企业级功能

在 supernal.ai/enterprise 上可享受以下企业级功能：
- 通过装饰器自动生成测试用例
- 故事系统（性能提升 50-80%）
- 架构可视化
- 多模型路由
- 审计与合规性日志记录