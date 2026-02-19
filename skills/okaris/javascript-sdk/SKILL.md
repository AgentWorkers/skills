---
name: javascript-sdk
description: "JavaScript/TypeScript SDK for inference.sh – 用于运行AI应用程序、构建代理程序以及集成150多种模型。  
包名：@inferencesh/sdk（可通过 `npm install` 安装）。  
支持完整的TypeScript语法、数据流处理以及文件上传功能；支持使用模板或自定义方式构建代理程序；提供工具构建API以及人工审批机制。  
适用场景：JavaScript集成、TypeScript开发、Node.js应用、React框架、Next.js项目以及前端应用程序。  
相关触发命令：`javascript sdk`、`typescript sdk`、`npm install`、`node.js api`、`js client`、`react ai`、`next.js ai`、`frontend sdk`、`@inferencesh/sdk`、`typescript agent`、`browser sdk`、`js integration`。"
allowed-tools: Bash(npm *), Bash(npx *), Bash(node *), Bash(pnpm *), Bash(yarn *)
---
# JavaScript SDK

使用 [inference.sh](https://inference.sh) JavaScript/TypeScript SDK 构建 AI 应用程序。

![JavaScript SDK](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgvftjwhby36trvaj66bwzcf.jpeg)

## 快速入门

```bash
npm install @inferencesh/sdk
```

```typescript
import { inference } from '@inferencesh/sdk';

const client = inference({ apiKey: 'inf_your_key' });

// Run an AI app
const result = await client.run({
  app: 'infsh/flux-schnell',
  input: { prompt: 'A sunset over mountains' }
});
console.log(result.output);
```

## 安装

```bash
npm install @inferencesh/sdk
# or
yarn add @inferencesh/sdk
# or
pnpm add @inferencesh/sdk
```

**要求：** Node.js 18.0.0+（或支持 `fetch` 方法的现代浏览器）

## 认证

```typescript
import { inference } from '@inferencesh/sdk';

// Direct API key
const client = inference({ apiKey: 'inf_your_key' });

// From environment variable (recommended)
const client = inference({ apiKey: process.env.INFERENCE_API_KEY });

// For frontend apps (use proxy)
const client = inference({ proxyUrl: '/api/inference/proxy' });
```

获取您的 API 密钥：设置 → API 密钥 → 创建 API 密钥

## 运行应用程序

### 基本执行

```typescript
const result = await client.run({
  app: 'infsh/flux-schnell',
  input: { prompt: 'A cat astronaut' }
});

console.log(result.status);  // "completed"
console.log(result.output);  // Output data
```

### 一次性执行（无需后续管理）

```typescript
const task = await client.run({
  app: 'google/veo-3-1-fast',
  input: { prompt: 'Drone flying over mountains' }
}, { wait: false });

console.log(`Task ID: ${task.id}`);
// Check later with client.getTask(task.id)
```

### 流式处理进度

```typescript
const stream = await client.run({
  app: 'google/veo-3-1-fast',
  input: { prompt: 'Ocean waves at sunset' }
}, { stream: true });

for await (const update of stream) {
  console.log(`Status: ${update.status}`);
  if (update.logs?.length) {
    console.log(update.logs.at(-1));
  }
}
```

### 运行参数

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `app` | 字符串 | 应用程序 ID（格式：namespace/name@version） |
| `input` | 对象 | 符合应用程序模式的输入数据 |
| `setup` | 对象 | 隐藏的配置信息 |
| `infra` | 字符串 | 运行模式：`cloud` 或 `private` |
| `session` | 字符串 | 用于保持会话状态的会话 ID |
| `session_timeout` | 数字 | 空闲超时时间（1-3600 秒） |

## 文件处理

### 自动上传

```typescript
const result = await client.run({
  app: 'image-processor',
  input: {
    image: '/path/to/image.png'  // Auto-uploaded
  }
});
```

### 手动上传

```typescript
// Basic upload
const file = await client.uploadFile('/path/to/image.png');

// With options
const file = await client.uploadFile('/path/to/image.png', {
  filename: 'custom_name.png',
  contentType: 'image/png',
  public: true
});

const result = await client.run({
  app: 'image-processor',
  input: { image: file.uri }
});
```

### 浏览器文件上传

```typescript
const input = document.querySelector('input[type="file"]');
const file = await client.uploadFile(input.files[0]);
```

## 会话（保持状态的执行）

在多次调用中保持工作进程的活跃状态：

```typescript
// Start new session
const result = await client.run({
  app: 'my-app',
  input: { action: 'init' },
  session: 'new',
  session_timeout: 300  // 5 minutes
});
const sessionId = result.session_id;

// Continue in same session
const result2 = await client.run({
  app: 'my-app',
  input: { action: 'process' },
  session: sessionId
});
```

## 代理 SDK

### 模板代理

使用工作区中预构建的代理：

```typescript
const agent = client.agent('my-team/support-agent@latest');

// Send message
const response = await agent.sendMessage('Hello!');
console.log(response.text);

// Multi-turn conversation
const response2 = await agent.sendMessage('Tell me more');

// Reset conversation
agent.reset();

// Get chat history
const chat = await agent.getChat();
```

### 自定义代理

通过编程方式创建自定义代理：

```typescript
import { tool, string, number, appTool } from '@inferencesh/sdk';

// Define tools
const calculator = tool('calculate')
  .describe('Perform a calculation')
  .param('expression', string('Math expression'))
  .build();

const imageGen = appTool('generate_image', 'infsh/flux-schnell@latest')
  .describe('Generate an image')
  .param('prompt', string('Image description'))
  .build();

// Create agent
const agent = client.agent({
  core_app: { ref: 'infsh/claude-sonnet-4@latest' },
  system_prompt: 'You are a helpful assistant.',
  tools: [calculator, imageGen],
  temperature: 0.7,
  max_tokens: 4096
});

const response = await agent.sendMessage('What is 25 * 4?');
```

### 可用的核心应用程序

| 模型 | 应用程序参考 |
|-------|---------------|
| Claude Sonnet 4 | `infsh/claude-sonnet-4@latest` |
| Claude 3.5 Haiku | `infsh/claude-haiku-35@latest` |
| GPT-4o | `infsh/gpt-4o@latest` |
| GPT-4o Mini | `infsh/gpt-4o-mini@latest` |

## 工具构建器 API

### 参数类型

```typescript
import {
  string, number, integer, boolean,
  enumOf, array, obj, optional
} from '@inferencesh/sdk';

const name = string('User\'s name');
const age = integer('Age in years');
const score = number('Score 0-1');
const active = boolean('Is active');
const priority = enumOf(['low', 'medium', 'high'], 'Priority');
const tags = array(string('Tag'), 'List of tags');
const address = obj({
  street: string('Street'),
  city: string('City'),
  zip: optional(string('ZIP'))
}, 'Address');
```

### 客户端工具（在您的代码中运行）

```typescript
const greet = tool('greet')
  .display('Greet User')
  .describe('Greets a user by name')
  .param('name', string('Name to greet'))
  .requireApproval()
  .build();
```

### 应用程序工具（调用 AI 应用程序）

```typescript
const generate = appTool('generate_image', 'infsh/flux-schnell@latest')
  .describe('Generate an image from text')
  .param('prompt', string('Image description'))
  .setup({ model: 'schnell' })
  .input({ steps: 20 })
  .requireApproval()
  .build();
```

### 代理工具（委托给子代理）

```typescript
import { agentTool } from '@inferencesh/sdk';

const researcher = agentTool('research', 'my-org/researcher@v1')
  .describe('Research a topic')
  .param('topic', string('Topic to research'))
  .build();
```

### Webhook 工具（调用外部 API）

```typescript
import { webhookTool } from '@inferencesh/sdk';

const notify = webhookTool('slack', 'https://hooks.slack.com/...')
  .describe('Send Slack notification')
  .secret('SLACK_SECRET')
  .param('channel', string('Channel'))
  .param('message', string('Message'))
  .build();
```

### 内部工具（内置功能）

```typescript
import { internalTools } from '@inferencesh/sdk';

const config = internalTools()
  .plan()
  .memory()
  .webSearch(true)
  .codeExecution(true)
  .imageGeneration({
    enabled: true,
    appRef: 'infsh/flux@latest'
  })
  .build();

const agent = client.agent({
  core_app: { ref: 'infsh/claude-sonnet-4@latest' },
  internal_tools: config
});
```

## 流式代理响应

```typescript
const response = await agent.sendMessage('Explain quantum computing', {
  onMessage: (msg) => {
    if (msg.content) {
      process.stdout.write(msg.content);
    }
  },
  onToolCall: async (call) => {
    console.log(`\n[Tool: ${call.name}]`);
    const result = await executeTool(call.name, call.args);
    agent.submitToolResult(call.id, result);
  }
});
```

## 文件附件

```typescript
// From file path (Node.js)
import { readFileSync } from 'fs';
const response = await agent.sendMessage('What\'s in this image?', {
  files: [readFileSync('image.png')]
});

// From base64
const response = await agent.sendMessage('Analyze this', {
  files: ['data:image/png;base64,iVBORw0KGgo...']
});

// From browser File object
const input = document.querySelector('input[type="file"]');
const response = await agent.sendMessage('Describe this', {
  files: [input.files[0]]
});
```

## 技能（可重用的上下文数据）

```typescript
const agent = client.agent({
  core_app: { ref: 'infsh/claude-sonnet-4@latest' },
  skills: [
    {
      name: 'code-review',
      description: 'Code review guidelines',
      content: '# Code Review\n\n1. Check security\n2. Check performance...'
    },
    {
      name: 'api-docs',
      description: 'API documentation',
      url: 'https://example.com/skills/api-docs.md'
    }
  ]
});
```

## 服务器代理（前端应用程序）

对于浏览器应用程序，通过代理将请求转发到后端以保护 API 密钥的安全：

### 客户端配置

```typescript
const client = inference({
  proxyUrl: '/api/inference/proxy'
  // No apiKey needed on frontend
});
```

### Next.js 代理（应用程序路由）

```typescript
// app/api/inference/proxy/route.ts
import { createRouteHandler } from '@inferencesh/sdk/proxy/nextjs';

const route = createRouteHandler({
  apiKey: process.env.INFERENCE_API_KEY
});

export const POST = route.POST;
```

### Express 代理

```typescript
import express from 'express';
import { createProxyMiddleware } from '@inferencesh/sdk/proxy/express';

const app = express();
app.use('/api/inference/proxy', createProxyMiddleware({
  apiKey: process.env.INFERENCE_API_KEY
}));
```

### 支持的框架

- Next.js（应用程序路由和页面路由）
- Express
- Hono
- Remix
- SvelteKit

## TypeScript 支持

包含完整的类型定义：

```typescript
import type {
  TaskDTO,
  ChatDTO,
  ChatMessageDTO,
  AgentTool,
  TaskStatusCompleted,
  TaskStatusFailed
} from '@inferencesh/sdk';

if (result.status === TaskStatusCompleted) {
  console.log('Done!');
} else if (result.status === TaskStatusFailed) {
  console.log('Failed:', result.error);
}
```

## 错误处理

```typescript
import { RequirementsNotMetException, InferenceError } from '@inferencesh/sdk';

try {
  const result = await client.run({ app: 'my-app', input: {...} });
} catch (e) {
  if (e instanceof RequirementsNotMetException) {
    console.log('Missing requirements:');
    for (const err of e.errors) {
      console.log(`  - ${err.type}: ${err.key}`);
    }
  } else if (e instanceof InferenceError) {
    console.log('API error:', e.message);
  }
}
```

## 人工审批工作流程

```typescript
const response = await agent.sendMessage('Delete all temp files', {
  onToolCall: async (call) => {
    if (call.requiresApproval) {
      const approved = await promptUser(`Allow ${call.name}?`);
      if (approved) {
        const result = await executeTool(call.name, call.args);
        agent.submitToolResult(call.id, result);
      } else {
        agent.submitToolResult(call.id, { error: 'Denied by user' });
      }
    }
  }
});
```

## CommonJS 支持

```javascript
const { inference, tool, string } = require('@inferencesh/sdk');

const client = inference({ apiKey: 'inf_...' });
const result = await client.run({...});
```

## 参考文件

- [代理模式](references/agent-patterns.md) - 多代理、RAG、批量处理模式
- [工具构建器](references/tool-builder.md) - 完整的工具构建器 API 参考
- [服务器代理](references/server-proxy.md) - Next.js、Express、Hono、Remix、SvelteKit 的设置指南
- [流式处理](references/streaming.md) - 实时进度更新和 SSE 处理
- [文件处理](references/files.md) - 文件上传、下载和管理
- [会话](references/sessions.md) - 保持状态的执行及工作进程的持续运行
- [TypeScript](references/typescript.md) - 类型定义和类型安全模式
- [React 集成](references/react-integration.md) - Hooks、组件和集成方案

## 相关技能

```bash
# Python SDK
npx skills add inference-sh/skills@python-sdk

# Full platform skill (all 150+ apps via CLI)
npx skills add inference-sh/skills@inference-sh

# LLM models
npx skills add inference-sh/skills@llm-models

# Image generation
npx skills add inference-sh/skills@ai-image-generation
```

## 文档

- [JavaScript SDK 参考](https://inference.sh/docs/api/sdk-javascript) - 完整的 API 文档
- [代理 SDK 概述](https://inference.sh/docs/api/agent-sdk) - 代理程序的构建方法
- [工具构建器参考](https://inference.sh/docs/api/agent-tools) - 工具的创建方法
- [服务器代理设置](https://inference.sh/docs/api/sdk/server-proxy) - 前端应用程序的集成指南
- [认证](https://inference.sh/docs/api/authentication) - API 密钥的设置方法
- [流式处理](https://inference.sh/docs/api/sdk/streaming) - 实时更新功能
- [文件上传](https://inference.sh/docs/api/sdk/files) - 文件处理相关内容