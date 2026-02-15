---
name: ai-sdk-core
description: |
  Build backend AI with Vercel AI SDK v6 stable. Covers Output API (replaces generateObject/streamObject), speech synthesis, transcription, embeddings, MCP tools with security guidance. Includes v4→v5 migration and 15 error solutions with workarounds.

  Use when: implementing AI SDK v5/v6, migrating versions, troubleshooting AI_APICallError, Workers startup issues, Output API errors, Gemini caching issues, Anthropic tool errors, MCP tools, or stream resumption failures.
user-invocable: true
---

# AI SDK 核心

后端 AI 功能基于 Vercel AI SDK v5 和 v6 构建。

**安装：**
```bash
npm install ai @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google zod
```

---

## AI SDK 6（稳定版 - 2026年1月）

**状态：** 稳定
**最新版本：** ai@6.0.26（2026年1月）

### 注意事项：** Output API 替代了 generateObject/streamObject

⚠️ **重要提示**：`generateObject()` 和 `streamObject()` 已被弃用，并将在未来版本中移除。请使用新的 Output API。

**旧版本（v5 - 已弃用）：**
```typescript
// ❌ DEPRECATED - will be removed
import { generateObject } from 'ai';

const result = await generateObject({
  model: openai('gpt-5'),
  schema: z.object({ name: z.string(), age: z.number() }),
  prompt: 'Generate a person',
});
```

**新版本（v6 - 推荐使用）：**
```typescript
// ✅ NEW OUTPUT API
import { generateText, Output } from 'ai';

const result = await generateText({
  model: openai('gpt-5'),
  output: Output.object({ schema: z.object({ name: z.string(), age: z.number() }) }),
  prompt: 'Generate a person',
});

// Access the typed object
console.log(result.object); // { name: "Alice", age: 30 }
```

### 输出类型
```typescript
import { generateText, Output } from 'ai';

// Object with Zod schema
output: Output.object({ schema: myZodSchema })

// Array of typed objects
output: Output.array({ schema: personSchema })

// Enum/choice from options
output: Output.choice({ choices: ['positive', 'negative', 'neutral'] })

// Plain text (explicit)
output: Output.text()

// Unstructured JSON (no schema validation)
output: Output.json()
```

### 使用 Output API 进行流式处理
```typescript
import { streamText, Output } from 'ai';

const result = streamText({
  model: openai('gpt-5'),
  output: Output.object({ schema: personSchema }),
  prompt: 'Generate a person',
});

// Stream partial objects
for await (const partialObject of result.objectStream) {
  console.log(partialObject); // { name: "Ali..." } -> { name: "Alice", age: ... }
}

// Get final object
const finalObject = await result.object;
```

### v6 的新功能

**1. **代理抽象**：
- 使用 `ToolLoopAgent` 类统一构建代理：
  - 完全控制执行流程、工具循环和状态管理
  - 替代了手动调用工具的编排方式

**2. **工具执行审批（人工干预）**：
  - 通过选择性审批提升用户体验。并非所有工具调用都需要审批。

```typescript
tools: {
  payment: tool({
    // Dynamic approval based on input
    needsApproval: async ({ amount }) => amount > 1000,
    inputSchema: z.object({ amount: z.number() }),
    execute: async ({ amount }) => { /* process payment */ },
  }),

  readFile: tool({
    needsApproval: false, // Safe operations don't need approval
    inputSchema: z.object({ path: z.string() }),
    execute: async ({ path }) => fs.readFile(path),
  }),

  deleteFile: tool({
    needsApproval: true, // Destructive operations always need approval
    inputSchema: z.object({ path: z.string() }),
    execute: async ({ path }) => fs.unlink(path),
  }),
}
```

**最佳实践**：
- 对于风险取决于参数的操作（例如支付金额），使用动态审批机制
- 对于具有破坏性的操作（删除、修改、购买等），始终需要审批
- 对于安全的读取操作，无需审批
- 添加系统提示：“如果工具执行未获批准，请不要重试”
- 为重复操作设置超时机制
- 保存用户偏好设置

**参考资料**：
- [Next.js 人工干预指南](https://ai-sdk.dev/cookbook/next/human-in-the-loop)
- [Cloudflare 代理人工干预指南](https://developers.cloudflare.com/agents/guides/human-in-the-loop/)
- [Permit.io 最佳实践](https://www.permit.io/blog/human-in-the-loop-for-ai-agents-best-practices-frameworks-use-cases-and-demo)

**3. **RAG 重新排序**：
```typescript
import { rerank } from 'ai';

const result = await rerank({
  model: cohere.reranker('rerank-v3.5'),
  query: 'user question',
  documents: searchResults,
  topK: 5,
});
```

**4. **MCP 工具（模型上下文协议）**：
⚠️ **安全警告**：MCP 工具存在重大生产风险。请参阅以下安全说明。

```typescript
import { experimental_createMCPClient } from 'ai';

const mcpClient = await experimental_createMCPClient({
  transport: { type: 'stdio', command: 'npx', args: ['-y', '@modelcontextprotocol/server-filesystem'] },
});

const tools = await mcpClient.tools();

const result = await generateText({
  model: openai('gpt-5'),
  tools,
  prompt: 'List files in the current directory',
});
```

**已知问题**：MCP 工具可能在流式模式下无法正常执行（[Vercel 社区讨论](https://community.vercel.com/t/question-how-to-properly-pass-mcp-tools-to-backend-using-ai-sdk-uis-usechat/29714)）。对于 MCP 工具，请使用 `generateText()` 而不是 `streamText()`。

**MCP 安全注意事项**：
⚠️ **严重警告**：在生产环境中使用动态 MCP 工具存在安全风险：
- 工具定义可能成为代理提示的一部分
- 可能在没有预警的情况下发生意外变化
- 被入侵的 MCP 服务器可能注入恶意提示
- 新工具可能会提升用户权限（例如，将读取权限提升为删除权限）

**解决方案：使用静态工具生成**：
```typescript
// ❌ RISKY: Dynamic tools change without your control
const mcpClient = await experimental_createMCPClient({ /* ... */ });
const tools = await mcpClient.tools(); // Can change anytime!

// ✅ SAFE: Generate static, versioned tool definitions
// Step 1: Install mcp-to-ai-sdk
npm install -g mcp-to-ai-sdk

// Step 2: Generate static tools (one-time, version controlled)
npx mcp-to-ai-sdk generate stdio 'npx -y @modelcontextprotocol/server-filesystem'

// Step 3: Import static tools
import { tools } from './generated-mcp-tools';

const result = await generateText({
  model: openai('gpt-5'),
  tools, // Static, reviewed, versioned
  prompt: 'Use tools',
});
```

**最佳实践**：生成静态工具，进行审查后提交到版本控制，并仅在必要时进行更新。

**参考来源**：[Vercel 博文：MCP 安全性](https://vercel.com/blog/generate-static-ai-sdk-tools-from-mcp-servers-with-mcp-to-ai-sdk)

**5. **语言模型中间件**：
```typescript
import { wrapLanguageModel, extractReasoningMiddleware } from 'ai';

const wrappedModel = wrapLanguageModel({
  model: anthropic('claude-sonnet-4-5-20250929'),
  middleware: extractReasoningMiddleware({ tagName: 'think' }),
});

// Reasoning extracted automatically from <think>...</think> tags
```

**6. **遥测（OpenTelemetry）**：
```typescript
const result = await generateText({
  model: openai('gpt-5'),
  prompt: 'Hello',
  experimental_telemetry: {
    isEnabled: true,
    functionId: 'my-chat-function',
    metadata: { userId: '123' },
    recordInputs: true,
    recordOutputs: true,
  },
});
```

**官方文档：** https://ai-sdk.dev/docs

---

## 最新的 AI 模型（2025-2026）

### OpenAI

**GPT-5.2**（2025年12月）：
- 上下文窗口 400k，输出token数 128k
- 增强的推理能力
- 可通过 API 平台使用

**GPT-5.1**（2025年11月）：
- 比 GPT-5 更快、更高效
- 回答更加自然和智能

**GPT-5**（2025年8月）：
- 幻觉现象减少了 45%
- 在数学、编码和视觉感知方面处于领先水平

**o3 推理模型**（2025年12月）：
- o3、o3-pro、o3-mini - 高级推理能力
- o4-mini - 快速推理

```typescript
import { openai } from '@ai-sdk/openai';
const gpt52 = openai('gpt-5.2');
const gpt51 = openai('gpt-5.1');
const gpt5 = openai('gpt-5');
const o3 = openai('o3');
const o3mini = openai('o3-mini');
```

### Anthropic

**Claude 4 系列**（2025年5月-10月）：
- **Opus 4**（5月22日）：最适合复杂推理，每百万token费用 15/75 美元
- **Sonnet 4**（5月22日）：性能均衡，每百万token费用 3/15 美元
- **Opus 4.1**（8月5日）：在代理任务和实际编码方面表现更出色
- **Haiku 4.5**（9月29日）：在编码和计算机使用方面能力最强

```typescript
import { anthropic } from '@ai-sdk/anthropic';
const sonnet45 = anthropic('claude-sonnet-4-5-20250929');  // Latest
const opus41 = anthropic('claude-opus-4-1-20250805');
const haiku45 = anthropic('claude-haiku-4-5-20251015');
```

### Google

**Gemini 2.5 系列**（2025年3月-9月）：
- **Pro**（2025年3月）：启动时在 LMArena 中排名第一
- **Pro Deep Think**（2025年5月）：增强了推理功能
- **Flash**（2025年5月）：速度快且成本效益高
- **Flash-Lite**（2025年9月）：效率得到提升

```typescript
import { google } from '@ai-sdk/google';
const pro = google('gemini-2.5-pro');
const flash = google('gemini-2.5-flash');
const lite = google('gemini-2.5-flash-lite');
```

---

## 核心功能

### 文本生成

**generateText()** - 使用工具完成文本生成
**streamText()** - 实时流式输出

### 结构化输出（v6 Output API）

**Output.object()** - 使用 Zod 架构生成结构化对象（替代 generateObject）
**Output.array()** - 生成结构化数组
**Output.choice()** - 从枚举中选择输出
**Output.json()** - 生成非结构化 JSON 数据

有关使用示例，请参阅上述“AI SDK 6”部分。

### 多模态功能

#### 语音合成（文本转语音）
```typescript
import { experimental_generateSpeech as generateSpeech } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateSpeech({
  model: openai.speech('tts-1-hd'),
  voice: 'alloy',
  text: 'Hello, how can I help you today?',
});

// result.audio is an ArrayBuffer containing the audio
const audioBuffer = result.audio;
```

**支持的提供者：**
- OpenAI：tts-1, tts-1-hd, gpt-4o-mini-tts
- ElevenLabs：eleven_multilingual_v2, eleven_turbo_v2
- LMNT, Hume

#### 语音转文本（Transcription）
```typescript
import { experimental_transcribe as transcribe } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await transcribe({
  model: openai.transcription('whisper-1'),
  audio: audioFile, // File, Blob, ArrayBuffer, or URL
});

console.log(result.text); // Transcribed text
console.log(result.segments); // Timestamped segments
```

**支持的提供者：**
- OpenAI：whisper-1
- ElevenLabs, Deepgram, AssemblyAI, Groq, Rev.ai

#### 图像生成
```typescript
import { generateImage } from 'ai';
import { openai } from '@ai-sdk/openai';

const result = await generateImage({
  model: openai.image('dall-e-3'),
  prompt: 'A futuristic city at sunset',
  size: '1024x1024',
  n: 1,
});

// result.images is an array of generated images
const imageUrl = result.images[0].url;
const imageBase64 = result.images[0].base64;
```

**支持的提供者：**
- OpenAI：dall-e-2, dall-e-3
- Google：imagen-3.0
- Fal AI, Black Forest Labs (Flux), Luma AI, Replicate

#### 嵌入式功能（Embeddings）
```typescript
import { embed, embedMany, cosineSimilarity } from 'ai';
import { openai } from '@ai-sdk/openai';

// Single embedding
const result = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: 'Hello world',
});
console.log(result.embedding); // number[]

// Multiple embeddings (parallel processing)
const results = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: ['Hello', 'World', 'AI'],
  maxParallelCalls: 5, // Parallel processing
});

// Compare similarity
const similarity = cosineSimilarity(
  results.embeddings[0],
  results.embeddings[1]
);
console.log(`Similarity: ${similarity}`); // 0.0 to 1.0
```

**支持的提供者：**
- OpenAI：text-embedding-3-small, text-embedding-3-large
- Google：text-embedding-004
- Cohere, Voyage AI, Mistral, Amazon Bedrock

#### 多模态提示（文件、图像、PDF）
```typescript
import { generateText } from 'ai';
import { google } from '@ai-sdk/google';

const result = await generateText({
  model: google('gemini-2.5-pro'),
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Summarize this document' },
      { type: 'file', data: pdfBuffer, mimeType: 'application/pdf' },
    ],
  }],
});

// Or with images
const result = await generateText({
  model: openai('gpt-5'),
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'What is in this image?' },
      { type: 'image', image: imageBuffer },
    ],
  }],
});
```

更多 API 详情请参阅官方文档：https://ai-sdk.dev/docs/ai-sdk-core

---

## v5 流式响应方法

当通过 API 返回流式响应时，请使用正确的方法：

| 方法 | 输出格式 | 使用场景 |
|--------|---------------|----------|
| `toTextStreamResponse()` | 纯文本块 | 简单文本流式输出 |
| `toUIMessageStreamResponse()` | 带有 JSON 事件的 SSE 格式 | **聊天 UI**（text-start, text-delta, text-end, finish） |

**对于聊天插件和 UI，始终使用 `toUIMessageStreamResponse()`：**

```typescript
const result = streamText({
  model: workersai('@cf/qwen/qwen3-30b-a3b-fp8'),
  messages,
  system: 'You are helpful.',
});

// ✅ For chat UIs - returns SSE with JSON events
return result.toUIMessageStreamResponse({
  headers: { 'Access-Control-Allow-Origin': '*' },
});

// ❌ For simple text - returns plain text chunks only
return result.toTextStreamResponse();
```

**注意：** `toDataStreamResponse()` 在 AI SDK v5 中并不存在（这是一个常见的误解）。**

---

## workers-ai-provider 版本兼容性

**重要提示：** `workers-ai-provider@2.x` 需要 AI SDK v5，不兼容 v4。

```bash
# ✅ Correct - AI SDK v5 with workers-ai-provider v2
npm install ai@^5.0.0 workers-ai-provider@^2.0.0 zod@^3.25.0

# ❌ Wrong - AI SDK v4 causes error
npm install ai@^4.0.0 workers-ai-provider@^2.0.0
# Error: "AI SDK 4 only supports models that implement specification version v1"
```

**Zod 版本：** AI SDK v5 需要 `zod@^3.25.0` 或更高版本的 Zod，以支持 `zod/v3` 和 `zod/v4` 导出。较低版本（3.22.x）会导致构建错误：“无法解析 zod/v4”。

---

## Cloudflare Workers 启动问题修复

**问题：** AI SDK v5 与 Zod 结合使用时，启动时间超过 270ms（超过了 Workers 的 400ms 限制）。

**解决方案：**
```typescript
// ❌ BAD: Top-level imports cause startup overhead
import { createWorkersAI } from 'workers-ai-provider';
const workersai = createWorkersAI({ binding: env.AI });

// ✅ GOOD: Lazy initialization inside handler
app.post('/chat', async (c) => {
  const { createWorkersAI } = await import('workers-ai-provider');
  const workersai = createWorkersAI({ binding: c.env.AI });
  // ...
});
```

**其他建议：**
- 减少顶层 Zod 模式的使用
- 将复杂模式移至路由处理函数中
- 使用 Wrangler 监控启动时间

---

## v5 中的工具调用变化

**重要变更：**
- `parameters` → `inputSchema`（Zod 架构）
- 工具属性：`args` → `input`，`result` → `output`
- `ToolExecutionError` 被移除（现在错误信息存储在 `tool-error` 中）
- `maxSteps` 参数被移除 → 使用 `stopWhen(stepCountIs(n)` 替代

**v5 的新功能：**
- 动态工具（根据上下文在运行时添加工具）
- 代理类（支持多步骤工具执行）

---

## 从 v4 迁移到 v5 的关键步骤

AI SDK v5 引入了许多重大变更。如果需要从 v4 迁移，请遵循以下指南。

### 变更概述：

1. **参数重命名**
   - `maxTokens` → `maxOutputTokens`
   - `providerMetadata` → `providerOptions`

2. **工具定义**
   - `parameters` → `inputSchema`
   - 工具属性：`args` → `input`，`result` → `output`

3. **消息类型**
   - `CoreMessage` → `ModelMessage`
   - `Message` → `UIMessage`
   - `convertToCoreMessages` → `convertToModelMessages`

4. **错误处理**
   - `ToolExecutionError` 类被移除
   - 错误信息现在存储在 `tool-error` 中
   - 支持自动重试

5. **多步骤执行**
   - `maxSteps` → `stopWhen`
   - 使用 `stepCountIs()` 或 `hasToolCall()` 进行控制

6. **消息结构**
   - 简单的 `content` 字符串 → `parts` 数组
   - `parts` 包含文本、文件、推理结果、工具调用结果

7. **流式架构**
   - 单个数据块 → 分为开始/更新/结束三个阶段
   - 并发流具有唯一标识

8. **工具流式处理**
   - 默认启用
   - `toolCallStreaming` 选项被移除

9. **包重组**
   - `ai/rsc` → `@ai-sdk/rsc`
   - `ai/react` → `@ai-sdk/react`
   - `LangChainAdapter` → `@ai-sdk/langchain`

### 迁移示例

**旧版本（v4）：**
```typescript
import { generateText } from 'ai';

const result = await generateText({
  model: openai.chat('gpt-4-turbo'),
  maxTokens: 500,
  providerMetadata: { openai: { user: 'user-123' } },
  tools: {
    weather: {
      description: 'Get weather',
      parameters: z.object({ location: z.string() }),
      execute: async (args) => { /* args.location */ },
    },
  },
  maxSteps: 5,
});
```

**新版本（v5）：**
```typescript
import { generateText, tool, stopWhen, stepCountIs } from 'ai';

const result = await generateText({
  model: openai('gpt-4-turbo'),
  maxOutputTokens: 500,
  providerOptions: { openai: { user: 'user-123' } },
  tools: {
    weather: tool({
      description: 'Get weather',
      inputSchema: z.object({ location: z.string() }),
      execute: async ({ location }) => { /* input.location */ },
    }),
  },
  stopWhen: stepCountIs(5),
});
```

### 迁移检查清单：
- 将所有 `maxTokens` 更改为 `maxOutputTokens`
- 将 `providerMetadata` 更改为 `providerOptions`
- 将工具参数 `parameters` 更改为 `inputSchema`
- 更新工具执行函数：`args` → `input`
- 将 `maxSteps` 替换为 `stopWhen(stepCountIs(n)`
- 更新消息类型：`CoreMessage` → `ModelMessage`
- 移除 `ToolExecutionError` 处理逻辑
- 更新包导入（`ai/rsc` → `@ai-sdk/rsc`）
- 测试流式行为（架构已更改）
- 更新 TypeScript 类型定义

### 自动迁移工具

AI SDK 提供了迁移工具：
```bash
npx ai migrate
```

该工具将自动应用大部分变更。请仔细审查这些更改。

**官方迁移指南：**
https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0

---

## 常见问题及解决方案

### 1. **AI_APICallError**

**原因：** API 请求失败（网络问题、认证问题或速率限制）。

**解决方案：**
```typescript
import { AI_APICallError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_APICallError) {
    console.error('API call failed:', error.message);
    console.error('Status code:', error.statusCode);
    console.error('Response:', error.responseBody);

    // Check common causes
    if (error.statusCode === 401) {
      // Invalid API key
    } else if (error.statusCode === 429) {
      // Rate limit - implement backoff
    } else if (error.statusCode >= 500) {
      // Provider issue - retry
    }
  }
}
```

**预防措施：**
- 启动时验证 API 密钥
- 实现带有指数退避机制的重试逻辑
- 监控速率限制
- 优雅地处理网络错误

---

### 2. **AI_NoObjectGeneratedError**

**原因：** 模型未生成符合要求的结构化输出。

**解决方案：**
```typescript
import { AI_NoObjectGeneratedError } from 'ai';

try {
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: z.object({ /* complex schema */ }),
    prompt: 'Generate data',
  });
} catch (error) {
  if (error instanceof AI_NoObjectGeneratedError) {
    console.error('No valid object generated');

    // Solutions:
    // 1. Simplify schema
    // 2. Add more context to prompt
    // 3. Provide examples in prompt
    // 4. Try different model (gpt-5 or claude-sonnet-4-5 for complex objects)
  }
}
```

**预防措施：**
- 从简单模式开始，逐步增加复杂性
- 在提示中包含示例：“生成一个如下信息的人：{ name: 'Alice', age: 30 }”
- 对于复杂结构化输出，使用 GPT-4
- 先用样本数据测试模式

---

### 3. **Worker 启动时间过长（超过 270ms）**

**原因：** AI SDK v5 与 Zod 在 Cloudflare Workers 中的初始化开销超过了启动限制。

**解决方案：**
```typescript
// BAD: Top-level imports cause startup overhead
import { createWorkersAI } from 'workers-ai-provider';
import { complexSchema } from './schemas';

const workersai = createWorkersAI({ binding: env.AI });

// GOOD: Lazy initialization inside handler
export default {
  async fetch(request, env) {
    const { createWorkersAI } = await import('workers-ai-provider');
    const workersai = createWorkersAI({ binding: env.AI });

    // Use workersai here
  }
}
```

**预防措施：**
- 将 AI SDK 的导入代码移至路由处理函数中
- 减少顶层 Zod 模式的使用
- 监控 Worker 的启动时间（必须低于 400ms）
- 使用 Wrangler 监控启动时间

**GitHub 问题：** 在 Vercel AI SDK 的问题中搜索“Workers 启动时间限制”

---

### 4. **streamText 无法正常工作**

**原因：** 流式错误可能被 `createDataStreamResponse` 方法忽略。

**状态：** ✅ **已解决** - 在 ai@4.1.22（2025年2月）中修复

**推荐解决方案：**
```typescript
// Use the onError callback (added in v4.1.22)
const stream = streamText({
  model: openai('gpt-4-turbo'),
  prompt: 'Hello',
  onError({ error }) {
    console.error('Stream error:', error);
    // Custom error logging and handling
  },
});

// Stream safely
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}
```

**替代方案（手动处理）：**
```typescript
// Fallback if not using onError callback
try {
  const stream = streamText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });

  for await (const chunk of stream.textStream) {
    process.stdout.write(chunk);
  }
} catch (error) {
  console.error('Stream error:', error);
}
```

**预防措施：**
- **使用 `onError` 回调** 来正确捕获错误
- 实现服务器端的错误监控
- 明确测试流式错误的处理逻辑
- 在生产环境中始终在服务器端记录错误

**GitHub 问题：** #4726（已解决）

---

### 5. **AI_LoadAPIKeyError**

**原因：** API 密钥缺失或无效。

**解决方案：**
```typescript
import { AI_LoadAPIKeyError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
  });
} catch (error) {
  if (error instanceof AI_LoadAPIKeyError) {
    console.error('API key error:', error.message);

    // Check:
    // 1. .env file exists and loaded
    // 2. Correct env variable name (OPENAI_API_KEY)
    // 3. Key format is valid (starts with sk-)
  }
}
```

**预防措施：**
- 在应用程序启动时验证 API 密钥
- 使用环境变量进行验证
- 在开发阶段提供清晰的错误信息
- 文档中明确说明所需的环境变量

---

### 6. **AI_NoContentGeneratedError**

**原因：** 模型未生成任何内容。

**解决方案：**
```typescript
import { AI_NoContentGeneratedError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Some prompt',
  });
} catch (error) {
  if (error instanceof AI_NoContentGeneratedError) {
    console.error('No content generated');

    // Possible causes:
    // 1. Safety filters blocked output
    // 2. Prompt triggered content policy
    // 3. Model configuration issue

    // Handle gracefully:
    return { text: 'Unable to generate response. Please try different input.' };
  }
}
```

**预防措施：**
- 对用户输入进行清洗
- 避免使用可能触发安全过滤器的提示
- 提供备用提示信息
- 记录错误发生情况以供分析

---

### 7. **AI_TypeValidationError**

**原因：** 生成的输出不符合 Zod 架构要求。

**解决方案：**
```typescript
import { AI_TypeValidationError } from 'ai';

try {
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: z.object({
      age: z.number().min(0).max(120),  // Strict validation
    }),
    prompt: 'Generate person',
  });
} catch (error) {
  if (error instanceof AI_TypeValidationError) {
    console.error('Validation failed:', error.message);

    // Solutions:
    // 1. Relax schema constraints
    // 2. Add more guidance in prompt
    // 3. Use .optional() for unreliable fields
  }
}
```

**预防措施：**
- 从简单的模式开始，逐步增加复杂性
- 对可能不存在的字段使用 `.optional()` 标注
- 在字段描述中添加验证提示
- 用多种提示进行测试

---

### 8. **AI_RetryError**

**原因：** 所有重试尝试都失败了。

**解决方案：**
```typescript
import { AI_RetryError } from 'ai';

try {
  const result = await generateText({
    model: openai('gpt-4-turbo'),
    prompt: 'Hello',
    maxRetries: 3,  // Default is 2
  });
} catch (error) {
  if (error instanceof AI_RetryError) {
    console.error('All retries failed');
    console.error('Last error:', error.lastError);

    // Check root cause:
    // - Persistent network issue
    // - Provider outage
    // - Invalid configuration
  }
}
```

**预防措施：**
- 调查失败的根本原因
- 根据需要调整重试策略
- 为提供商故障实现断路器机制
- 准备备用提供商

---

### 9. **速率限制错误**

**原因：** 超过了提供商的速率限制（RPM/TPM）。

**解决方案：**
```typescript
// Implement exponential backoff
async function generateWithBackoff(prompt: string, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await generateText({
        model: openai('gpt-4-turbo'),
        prompt,
      });
    } catch (error) {
      if (error instanceof AI_APICallError && error.statusCode === 429) {
        const delay = Math.pow(2, i) * 1000;  // Exponential backoff
        console.log(`Rate limited, waiting ${delay}ms`);
        await new Promise(resolve => setTimeout(resolve, delay));
      } else {
        throw error;
      }
    }
  }
  throw new Error('Rate limit retries exhausted');
}
```

**预防措施：**
- 监控速率限制
- 队列请求以确保不超过限制
- 如有必要，升级提供商等级
- 实现请求节流

---

### 10. **TypeScript 与 Zod 的性能问题**

**原因：** 复杂的 Zod 模式会减慢 TypeScript 的类型检查速度。

**解决方案：**
```typescript
// Instead of deeply nested schemas at top level:
// const complexSchema = z.object({ /* 100+ fields */ });

// Define inside functions or use type assertions:
function generateData() {
  const schema = z.object({ /* complex schema */ });
  return generateObject({ model: openai('gpt-4-turbo'), schema, prompt: '...' });
}

// Or use z.lazy() for recursive schemas:
type Category = { name: string; subcategories?: Category[] };
const CategorySchema: z.ZodType<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(CategorySchema).optional(),
  })
);
```

**预防措施：**
- 避免使用顶层复杂的 Zod 模式
- 对于递归类型使用 `z.lazy()` 方法
- 将大型模式拆分为较小的部分
- 在适当的地方使用类型断言

**官方文档：** https://ai-sdk.dev/docs/troubleshooting/common-issues/slow-type-checking

---

### 11. **无效的 JSON 响应（特定于提供商）**

**原因：** 某些模型偶尔返回无效的 JSON 数据。

**解决方案：**
```typescript
// Use built-in retry and mode selection
const result = await generateObject({
  model: openai('gpt-4-turbo'),
  schema: mySchema,
  prompt: 'Generate data',
  mode: 'json',  // Force JSON mode (supported by GPT-4)
  maxRetries: 3,  // Retry on invalid JSON
});

// Or catch and retry manually:
try {
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: mySchema,
    prompt: 'Generate data',
  });
} catch (error) {
  // Retry with different model
  const result = await generateObject({
    model: openai('gpt-4-turbo'),
    schema: mySchema,
    prompt: 'Generate data',
  });
}
```

**预防措施：**
- 可使用时使用 `mode: 'json'` 参数
- 对于结构化输出，优先选择 GPT-4
- 实现重试逻辑
- 验证响应内容

**GitHub 问题：** #4302（Imagen 3.0 的无效 JSON 响应）

---

### 13. **Gemini 的隐式缓存问题**

**问题：** 当定义了工具时，即使未使用这些工具，Gemini 3 的缓存功能也会导致 API 成本增加。

**原因：** Google Gemini 3 的缓存功能在某些情况下会失效。

**解决方案：**
```typescript
// Conditionally add tools only when needed
const needsTools = await analyzePrompt(userInput);

const result = await generateText({
  model: google('gemini-3-flash'),
  tools: needsTools ? { weather: weatherTool } : undefined,
  prompt: userInput,
});
```

**影响：** 对于重复请求，可能会导致 API 成本显著增加

---

### 14. **Anthropic 工具错误导致 JSON 解析失败**

**问题：** `SyntaxError: "[object Object]"` 是无效的 JSON

**原因：** Anthropic 的内置工具（如 web_fetch）返回错误对象，AI SDK 试图将其解析为 JSON。

**解决方案：**
```typescript
try {
  const result = await generateText({
    model: anthropic('claude-sonnet-4-5-20250929'),
    tools: { web_fetch: { type: 'anthropic_defined', name: 'web_fetch' } },
    prompt: userPrompt,
  });
} catch (error) {
  if (error.message.includes('is not valid JSON')) {
    // Tool returned error result, handle gracefully
    console.error('Tool execution failed - likely blocked URL or permission issue');
    // Retry without tool or use custom tool
  }
  throw error;
}
```

**影响：** 在使用 Anthropic 的内置工具时可能导致应用程序崩溃

**解决方案：**
```typescript
// Workaround: Filter messages before sending
const filteredMessages = messages.map(msg => {
  if (msg.role === 'assistant') {
    return {
      ...msg,
      content: msg.content.filter(part => part.type !== 'tool-result'),
    };
  }
  return msg;
});

const result = await generateText({
  model: anthropic('claude-sonnet-4-5-20250929'),
  tools: { database: databaseTool },
  messages: filteredMessages,
  prompt: 'Get user data',
});
```

**预防措施：**
**影响：** 在使用 Anthropic 的内置工具时可能导致应用程序崩溃

**已知问题：** PR #11854 已提交

---

**更多错误：** https://ai-sdk.dev/docs/reference/ai-sdk-errors（共 31 个错误）

---

## 已知问题与限制

### 使用 `useChat` 时，带有记忆化选项的回调函数失效

**问题：** 当使用 `useChat` 并启用记忆化选项时（为了提高性能），`onData` 和 `onFinish` 回调函数会使用过时的数据，无法获取更新后的状态变量。

**来源：** [GitHub 问题 #11686](https://github.com/vercel/ai/issues/11686)

**重现步骤：**
```typescript
const [count, setCount] = useState(0);

const chatOptions = useMemo(() => ({
  onFinish: (message) => {
    console.log('Count:', count); // ALWAYS 0, never updates!
  },
}), []); // Empty deps = stale closure

const { messages, append } = useChat(chatOptions);
```

**解决方法 1：** 不要使用记忆化回调函数**
```typescript
const { messages, append } = useChat({
  onFinish: (message) => {
    console.log('Count:', count); // Now sees current count
  },
});
```

**解决方法 2：** 使用 `useRef`**
```typescript
const countRef = useRef(count);
useEffect(() => { countRef.current = count; }, [count]);

const chatOptions = useMemo(() => ({
  onFinish: (message) => {
    console.log('Count:', countRef.current); // Always current
  },
}), []);
```

**完整重现代码：** https://github.com/alechoey/ai-sdk-stale-ondata-repro

---

### 切换浏览器标签页时流式处理无法恢复

**问题：** 当用户在 AI 流式处理过程中切换浏览器标签页或使应用程序后台化时，流式处理无法恢复。连接会丢失，且不会自动重新建立。

**来源：** [GitHub 问题 #11865](https://github.com/vercel/ai/issues/11865)

**影响：** 对于长时间运行的流式处理来说，这是一个严重的用户体验问题

**解决方法 1：** 实现错误处理机制**
```typescript
const { messages, append, reload } = useChat({
  api: '/api/chat',
  onError: (error) => {
    if (error.message.includes('stream') || error.message.includes('aborted')) {
      // Attempt to reload last message
      reload();
    }
  },
});
```

**解决方法 2：** 检测窗口可见性变化**
```typescript
useEffect(() => {
  const handleVisibilityChange = () => {
    if (document.visibilityState === 'visible') {
      // Check if stream was interrupted
      const lastMessage = messages[messages.length - 1];
      if (lastMessage?.role === 'assistant' && !lastMessage.content) {
        reload();
      }
    }
  };

  document.addEventListener('visibilitychange', handleVisibilityChange);
  return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
}, [messages, reload]);
```

**现状：** 这是一个已知的问题，目前没有内置的自动恢复功能

---

## 何时使用此技能

### 在以下情况下使用 `ai-sdk-core`：
- 构建后端 AI 功能（服务器端文本生成）
- 实现服务器端文本生成（Node.js、Workers、Next.js）
- 创建结构化 AI 输出（JSON、表单、数据提取）
- 使用工具构建 AI 代理（多步骤工作流程）
- 集成多个 AI 提供者（OpenAI、Anthropic、Google、Cloudflare）
- 从 AI SDK v4 迁移到 v5
- 遇到 AI SDK 相关错误（如 AI_APICallError、AI_NoObjectGeneratedError 等）
- 在 Cloudflare Workers 中使用 AI（使用 workers-ai-provider）
- 在 Next.js 服务器组件/动作中使用 AI
- 需要在不同的 LLM 提供者之间保持 API 一致性

### 何时不使用此技能：

- 构建 React 聊天 UI 时（请使用 **ai-sdk-ui**）
- 需要前端钩子（如 useChat）时（请使用 **ai-sdk-ui**）
- 需要高级功能（如嵌入式处理或图像生成）时（请参阅官方文档）
- 构建不使用多个提供商的 Cloudflare Workers AI 应用程序时（请使用 **cloudflare-workers-ai**）
- 需要生成式 UI 或 RSC 功能时（请参阅 https://ai-sdk.dev/docs/ai-sdk-rsc）

---

## 版本信息

**AI SDK：**
- 稳定版本：ai@6.0.26（2026年1月）
- ⚠️ **请跳过 v6.0.40** - 因流式处理功能存在问题（已在 v6.0.41 中修复）
- 旧版本 v5：ai@5.0.117（使用 ai-v5 标签）
- 支持 Zod 3.x/4.x

**最新模型（2026年）：**
- OpenAI：GPT-5.2、GPT-5.1、GPT-5、o3、o3-mini、o4-mini
- Anthropic：Claude Sonnet 4.5、Opus 4.1、Haiku 4.5
- Google：Gemini 2.5 Pro/Flash/Lite

**查看最新版本：**
```bash
npm view ai version
npm view ai dist-tags
```

## 官方文档**

**核心功能：**
- AI SDK v6：https://ai-sdk.dev/docs
- AI SDK 核心：https://ai-sdk.dev/docs/ai-sdk-core/overview
- Output API：https://ai-sdk.dev/docs/ai-sdk-core/generating-structured-data
- 从 v4 迁移到 v5 的指南：https://ai-sdk.dev/docs/migration-guides/migration-guide-5-0
- 所有错误信息：https://ai-sdk.dev/docs/reference/ai-sdk-errors
- 提供者列表：https://ai-sdk.dev/providers/overview

**多模态功能：**
- 语音合成：https://ai-sdk.dev/docs/ai-sdk-core/speech
- 语音转文本：https://ai-sdk.dev/docs/ai-sdk-core/transcription
- 图像生成：https://ai-sdk.dev/docs/ai-sdk-core/image-generation
- 嵌入式功能：https://ai-sdk.dev/docs/ai-sdk-core/embeddings

**GitHub：**
- 仓库：https://github.com/vercel/ai
- 问题报告：https://github.com/vercel/ai/issues

---

**最后更新时间：** 2026年1月20日
**技能版本：** 2.1.0
**更新内容：** 添加了 3 个新的错误信息（Gemini 缓存问题、Anthropic 工具错误、工具结果的处理方式）、MCP 安全指南、React 钩子的使用场景、流式处理的解决方法
**AI SDK：** v6.0.26 稳定版本（请避免使用 v6.0.40）