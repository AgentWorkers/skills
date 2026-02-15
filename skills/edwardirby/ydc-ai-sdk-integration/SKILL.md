---
name: ydc-ai-sdk-integration
description: 将 Vercel AI SDK 应用程序与 You.com 工具（网络搜索、AI 代理、内容提取）集成。当开发者提到 AI SDK、Vercel AI SDK、generateText、streamText 或 You.com 与 AI SDK 的集成时，请使用此内容。
license: MIT
compatibility: Requires Node.js 18+ and npm/bun/yarn/pnpm
metadata:
  author: youdotcom-oss
  category: sdk-integration
  version: "1.0.0"
  keywords: vercel,vercel-ai-sdk,ai-sdk,you.com,integration,anthropic,openai,web-search,content-extraction,livecrawl,citations
---

# 将 AI SDK 与 You.com 工具集成

本文档提供了使用 `@youdotcom-oss/ai-sdk-plugin` 将 You.com 工具集成到您的 Vercel AI SDK 应用程序中的交互式工作流程。

## 工作流程

1. **询问：包管理器**
   * 使用哪种包管理器？（npm、bun、yarn、pnpm）
   * 使用所选的包管理器安装相应的包：
     ```bash
     npm install @youdotcom-oss/ai-sdk-plugin
     # or bun add @youdotcom-oss/ai-sdk-plugin
     # or yarn add @youdotcom-oss/ai-sdk-plugin
     # or pnpm add @youdotcom-oss/ai-sdk-plugin
     ```

2. **询问：环境变量名称**
   * 使用标准的 `YDC_API_KEY` 吗？
   * 或者使用自定义名称？（如果是自定义名称，请获取该名称）
   * 用户是否已在环境中设置了该变量？
   * 如果没有：指导用户从 https://you.com/platform/api-keys 获取 API 密钥。

3. **询问：需要使用哪些 AI SDK 函数？**
   * 是否使用 `generateText()` 函数？
   * 是否使用 `streamText()` 函数？
   * 两者都需要吗？

4. **询问：使用现有文件还是新建文件？**
   * 如果使用现有文件：询问需要编辑哪些文件。
   * 如果需要新建文件：询问文件的位置和名称。

5. **针对每个文件，进一步询问：**
   * 需要添加哪些 You.com 工具？
     - `youSearch`（网页搜索）
     - `youExpress`（AI 代理）
     - `youContents`（内容提取）
     - 需要同时使用多个工具吗？（选择合适的组合）
   * 在该文件中是否使用 `generateText()` 或 `streamText()` 函数？
   * 使用的是哪个 AI 提供商的模型？（这有助于确定是否需要设置 `stopWhen` 参数）。

6. **参考集成示例**
   请参阅下方的“集成示例”部分，了解完整的代码模式：
   - `generateText()`：使用这些工具进行基本文本生成。
   - `streamText()`：与 Web 框架（Next.js、Express、React）配合使用，实现流式响应。

7. **更新/创建文件**
   - 对于每个文件：
     - 参考相应的集成示例（根据用户的回答选择使用 `generateText` 或 `streamText`）。
     - 添加所选工具的导入语句。
     - 如果是现有文件：找到 `generateText` 或 `streamText` 的调用部分，并添加相应的工具配置。
     - 如果是新建文件：创建文件并使用示例结构。
     - 根据环境变量的名称配置工具的调用方式：
       - 使用标准 `YDC_API_KEY` 时：`youSearch()`
       - 使用自定义名称时：`youSearch({ apiKey: process.env.CUSTOM_NAME })`
     - 将所选的工具添加到 `tools` 对象中。
     - 如果同时使用 `streamText` 和 Anthropic，需要添加 `stopWhen` 参数。

## 集成示例

### `generateText()` - 基本文本生成
**环境变量设置：**
```typescript
import { anthropic } from '@ai-sdk/anthropic';
import { generateText } from 'ai';
import { youContents, youExpress, youSearch } from '@youdotcom-oss/ai-sdk-plugin';

// Reads YDC_API_KEY from environment automatically
const result = await generateText({
  model: anthropic('claude-sonnet-4-5-20250929'),
  tools: {
    search: youSearch(),
  },
  prompt: 'What are the latest developments in quantum computing?',
});

console.log(result.text);
```

**多个工具的集成示例：**
```typescript
const result = await generateText({
  model: anthropic('claude-sonnet-4-5-20250929'),
  tools: {
    search: youSearch(),      // Web search with citations
    agent: youExpress(),      // AI answers with web context
    extract: youContents(),   // Content extraction from URLs
  },
  prompt: 'Research quantum computing and summarize the key papers',
});
```

**自定义 API 密钥：**
```typescript
const result = await generateText({
  model: anthropic('claude-sonnet-4-5-20250929'),
  tools: {
    search: youSearch({ apiKey: 'your-custom-key' }),
  },
  prompt: 'Your prompt here',
});
```

**完整示例：**
```typescript
import { anthropic } from '@ai-sdk/anthropic';
import { generateText } from 'ai';
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

const main = async () => {
  try {
    const result = await generateText({
      model: anthropic('claude-sonnet-4-5-20250929'),
      tools: {
        search: youSearch(),
      },
      maxSteps: 5,
      prompt: 'What are the latest developments in quantum computing?',
    });

    console.log('Generated text:', result.text);
    console.log('\nTool calls:', result.steps.flatMap(s => s.toolCalls));
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
};

main();
```

### `streamText()` - 流式响应
**基本流式响应示例：**
```typescript
import { anthropic } from '@ai-sdk/anthropic';
import { streamText, type StepResult } from 'ai';
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

// CRITICAL: Always use stopWhen for Anthropic streaming
// Anthropic's SDK requires explicit stop conditions
const stepCountIs = (n: number) => (stepResult: StepResult<any>) =>
  stepResult.stepNumber >= n;

const result = streamText({
  model: anthropic('claude-sonnet-4-5-20250929'),
  tools: { search: youSearch() },
  stopWhen: stepCountIs(3),  // Required for Anthropic
  prompt: 'What are the latest AI developments?',
});

// Consume stream
for await (const chunk of result.textStream) {
  process.stdout.write(chunk);
}
```

**Next.js 集成（应用路由器）：**
```typescript
// app/api/chat/route.ts
import { anthropic } from '@ai-sdk/anthropic';
import { streamText, type StepResult } from 'ai';
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

const stepCountIs = (n: number) => (stepResult: StepResult<any>) =>
  stepResult.stepNumber >= n;

export async function POST(req: Request) {
  const { prompt } = await req.json();

  const result = streamText({
    model: anthropic('claude-sonnet-4-5-20250929'),
    tools: { search: youSearch() },
    stopWhen: stepCountIs(5),
    prompt,
  });

  return result.toDataStreamResponse();
}
```

**Express.js 集成：**
```typescript
// server.ts
import express from 'express';
import { anthropic } from '@ai-sdk/anthropic';
import { streamText, type StepResult } from 'ai';
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

const app = express();
app.use(express.json());

const stepCountIs = (n: number) => (stepResult: StepResult<any>) =>
  stepResult.stepNumber >= n;

app.post('/api/chat', async (req, res) => {
  const { prompt } = req.body;

  const result = streamText({
    model: anthropic('claude-sonnet-4-5-20250929'),
    tools: { search: youSearch() },
    stopWhen: stepCountIs(5),
    prompt,
  });

  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.setHeader('Transfer-Encoding', 'chunked');

  for await (const chunk of result.textStream) {
    res.write(chunk);
  }

  res.end();
});

app.listen(3000);
```

**React 客户端（与 Next.js 一起使用）：**
```typescript
// components/Chat.tsx
'use client';

import { useChat } from 'ai/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
  });

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          <strong>{m.role}:</strong> {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}
```

**完整的流式响应示例：**
```typescript
import { anthropic } from '@ai-sdk/anthropic';
import { streamText, type StepResult } from 'ai';
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

const stepCountIs = (n: number) => (stepResult: StepResult<any>) =>
  stepResult.stepNumber >= n;

const main = async () => {
  try {
    const result = streamText({
      model: anthropic('claude-sonnet-4-5-20250929'),
      tools: {
        search: youSearch(),
      },
      stopWhen: stepCountIs(3),
      prompt: 'What are the latest AI developments?',
    });

    // Stream to stdout
    console.log('Streaming response:\n');
    for await (const chunk of result.textStream) {
      process.stdout.write(chunk);
    }
    console.log('\n\nDone!');
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
};

main();
```

## 工具调用模式

根据第 2 步中的环境变量名称进行调用：

**使用标准 `YDC_API_KEY`：**
```typescript
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

tools: {
  search: youSearch(),
}
```

**使用自定义环境变量：**
```typescript
import { youSearch } from '@youdotcom-oss/ai-sdk-plugin';

const apiKey = process.env.THEIR_CUSTOM_NAME;

tools: {
  search: youSearch({ apiKey }),
}
```

**同时使用多个工具（使用标准环境变量）：**
```typescript
import { youSearch, youExpress, youContents } from '@youdotcom-oss/ai-sdk-plugin';

tools: {
  search: youSearch(),
  agent: youExpress(),
  extract: youContents(),
}
```

**同时使用多个工具（使用自定义环境变量）：**
```typescript
import { youSearch, youExpress, youContents } from '@youdotcom-oss/ai-sdk-plugin';

const apiKey = process.env.THEIR_CUSTOM_NAME;

tools: {
  search: youSearch({ apiKey }),
  agent: youExpress({ apiKey }),
  extract: youContents({ apiKey }),
}
```

## 可用的工具

- **youSearch**：网页和新闻搜索功能，具体参数由模型决定（如查询内容、数量、国家等）。
- **youExpress**：具有 Web 上下文支持的 AI 代理，具体参数由模型决定（如输入内容、使用的工具等）。
- **youContents**：用于提取网页内容，具体参数由模型决定（如 URL、格式等）。

## 关键集成模式

上述示例展示了以下内容：
- 如何导入 AI SDK、API 提供商以及 You.com 工具。
- 如何验证环境变量（对于新建文件可选）。
- 如何根据环境变量配置工具。
- 如何使用 `generateText` 或 `streamText` 函数。
- 如何处理返回结果（特别是对于 `streamText`，需要正确解构 `textStream` 数据）。
- 如何在使用 Anthropic 时设置 `stopWhen` 参数（例如 `stepCountIs(3)`）。
- 如何将工具集成到不同的 Web 框架中（Next.js、Express、React）。

## 实施检查清单

对于每个需要更新或新建的文件：
- [ ] 是否为所选工具添加了正确的导入语句？
- [ ] 如果使用了自定义环境变量，是否使用了正确的变量名称？
- [ ] 是否将工具配置添加到了 `generateText` 或 `streamText` 函数中？
- [ ] 每个工具是否被正确调用：
  - 使用标准环境变量时：`toolName()`
  - 使用自定义环境变量时：`toolName({ apiKey })`
- [ ] 如果使用了 `streamText`，是否正确解构了返回的数据（例如 `const { textStream } = ...`）？
- **如果同时使用了 Anthropic 和 `streamText`，是否添加了 `stopWhen: stepCountIs(3)` 参数？**

**全局检查清单：**
- [ ] 是否使用正确的包管理器安装了所有需要的包？
- [ ] 用户是否已在环境中设置了环境变量？
- [ ] 所有文件是否都已更新或创建完成？
- [ ] 是否已准备好进行测试？

## 常见问题及解决方法

- **问题**：“找不到 `@youdotcom-oss/ai-sdk-plugin` 模块。”
  **解决方法**：使用相应的包管理器进行安装。
- **问题**：“需要设置 `YDC_API_KEY`（或自定义名称）环境变量。”
  **解决方法**：在环境中设置该变量（密钥获取地址：https://you.com/platform/api-keys）。
- **问题**：“工具执行失败，提示 401 错误。”
  **解决方法**：确认 API 密钥有效。
- **问题**：“响应不完整或缺失。”
  **解决方法**：如果使用了 `streamText`，请增加迭代次数（建议从 3 开始，根据需要逐步增加）（详见 README 文件中的故障排除指南）。
- **问题**：“`textStream` 对象不可迭代。”
  **解决方法**：正确解构返回的数据：`const { textStream } = streamText(...)`。
- **问题**：“自定义环境变量不起作用。”
  **解决方法**：在调用工具时传递正确的参数，例如 `youSearch({ apiKey })`。

## 高级功能：自定义工具开发模式

对于开发自定义 AI SDK 工具或为 `@youdotcom-oss/ai-sdk-plugin` 贡献代码的开发者：

### 工具函数结构

所有工具函数都遵循以下结构：
```typescript
export const youToolName = (config: YouToolsConfig = {}) => {
  const apiKey = config.apiKey ?? process.env.YDC_API_KEY;

  return tool({
    description: 'Tool description for AI model',
    inputSchema: ZodSchema,
    execute: async (params) => {
      if (!apiKey) {
        throw new Error('YDC_API_KEY is required');
      }

      const response = await callApiUtility({
        params,
        YDC_API_KEY: apiKey,
        getUserAgent,
      });

      // Return raw API response for maximum flexibility
      return response;
    },
  });
};
```

### 输入模式：启用智能查询

始终使用来自 `@youdotcom-oss/mcp` 的输入模式：
```typescript
// ✅ Import from @youdotcom-oss/mcp
import { SearchQuerySchema } from '@youdotcom-oss/mcp';

export const youSearch = (config: YouToolsConfig = {}) => {
  return tool({
    description: '...',
    inputSchema: SearchQuerySchema,  // Enables AI to use all search parameters
    execute: async (params) => { ... },
  });
};

// ❌ Don't duplicate or simplify schemas
const MySearchSchema = z.object({ query: z.string() });  // Missing filters!
```

**这样做的重要性：**
- 丰富的输入模式允许 AI 使用更复杂的查询参数（如筛选条件、数据更新频率、国家等）。
- AI 可以根据用户意图构建更智能的查询。
- 避免在不同包中重复定义输入模式。
- 确保与 MCP 服务器的输入模式保持一致。

### API 密钥处理

在调用 API 之前，始终提供环境变量的备用值并进行验证：
```typescript
// ✅ Automatic environment variable fallback
const apiKey = config.apiKey ?? process.env.YDC_API_KEY;

// ✅ Check API key in execute function
execute: async (params) => {
  if (!apiKey) {
    throw new Error('YDC_API_KEY is required');
  }
  const response = await callApi(...);
}
```

### 响应格式

始终返回原始的 API 响应，以获得最大的灵活性：
```typescript
// ✅ Return raw API response
execute: async (params) => {
  const response = await fetchSearchResults({
    searchQuery: params,
    YDC_API_KEY: apiKey,
    getUserAgent,
  });

  return response;  // Raw response for maximum flexibility
}

// ❌ Don't format or transform responses
return {
  text: formatResponse(response),
  data: response,
};
```

**为什么使用原始响应？**
- 使 AI SDK 能够更灵活地处理返回的数据。
- 避免因格式转换导致的信息丢失。
- AI SDK 可以自行处理数据的展示方式。
- 更便于调试（可以直接查看实际的 API 响应内容）。

### 工具描述

为每个工具编写描述，以指导 AI 的行为：
```typescript
// ✅ Clear guidance for AI model
description: 'Search the web for current information, news, articles, and content using You.com. Returns web results with snippets and news articles. Use this when you need up-to-date information or facts from the internet.'

// ❌ Too brief
description: 'Search the web'
```

## 其他资源
- **包的 README 文档**：https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/ai-sdk-plugin
- **Vercel AI SDK 文档**：https://ai-sdk.dev/docs
- **You.com API 文档**：https://you.com/platform/api-keys