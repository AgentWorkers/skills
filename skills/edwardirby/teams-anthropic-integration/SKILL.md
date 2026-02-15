---
name: teams-anthropic-integration
description: 使用 @youdotcom-oss/teams-anthropic 将 Anthropic 的 Claude 模型（Opus、Sonnet、Haiku）添加到 Microsoft Teams.ai 应用程序中。可选地，可以集成 You.com MCP 服务器以实现网页搜索和内容提取功能。
license: MIT
compatibility: Node.js 18+, @microsoft/teams.ai
metadata:
  author: youdotcom-oss
  category: enterprise-integration
  version: "1.1.0"
  keywords: microsoft-teams,teams-ai,anthropic,claude,mcp,you.com,web-search,content-extraction
---

# 使用 Anthropic Claude 构建 Teams.ai 应用程序

使用 `@youdotcom-oss/teams-anthropic` 将 Claude 模型（Opus、Sonnet、Haiku）添加到 Microsoft Teams.ai 应用程序中。可选地，还可以集成 You.com MCP 服务器以实现网页搜索和内容提取功能。

## 选择您的路径

**路径 A：基本设置**（适合初学者）
- 在 Teams.ai 中使用 Anthropic Claude 模型
- 支持聊天、流式对话和函数调用
- 无需额外依赖项

**路径 B：使用 You.com MCP**（支持网页搜索功能）
- 包含路径 A 的所有功能
- 通过 You.com 实现网页搜索和内容提取
- 支持实时信息查询

## 决策点

**问题：您的 Teams 应用程序需要网页搜索和内容提取功能吗？**
- **不需要** → 选择 **路径 A：基本设置**（更简单、更快捷）
- **需要** → 选择 **路径 B：使用 You.com MCP**

---

## 路径 A：基本设置

在 Teams.ai 应用程序中使用 Anthropic Claude 模型，无需额外依赖项。

### A1. 安装包

```bash
npm install @youdotcom-oss/teams-anthropic @anthropic-ai/sdk @microsoft/teams.ai
```

### A2. 获取 Anthropic API 密钥

从 [console.anthropic.com](https://console.anthropic.com/) 获取您的 API 密钥。

```bash
# Add to .env
ANTHROPIC_API_KEY=your-anthropic-api-key
```

### A3. 选择新应用还是现有应用？
- **新创建的应用程序**：使用以下完整模板
- **现有应用程序**：将 Claude 模型添加到现有设置中

### A4. 基本模板

**对于新创建的应用程序：**

```typescript
import { App } from '@microsoft/teams.apps';
import { AnthropicChatModel, AnthropicModel } from '@youdotcom-oss/teams-anthropic';

if (!process.env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY environment variable is required');
}

const model = new AnthropicChatModel({
  model: AnthropicModel.CLAUDE_SONNET_4_5,
  apiKey: process.env.ANTHROPIC_API_KEY,
  requestOptions: {
    max_tokens: 2048,
    temperature: 0.7,
  },
});

const app = new App();

app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });

  const response = await model.send(
    { role: 'user', content: activity.text }
  );

  if (response.content) {
    await send(response.content);
  }
});

app.start().catch(console.error);
```

**对于现有应用程序：**

在现有代码中添加以下内容：
```typescript
import { AnthropicChatModel, AnthropicModel } from '@youdotcom-oss/teams-anthropic';
```

替换现有的模型：
```typescript
const model = new AnthropicChatModel({
  model: AnthropicModel.CLAUDE_SONNET_4_5,
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

### A5. 选择模型

```typescript
// Most capable - best for complex tasks
AnthropicModel.CLAUDE_OPUS_4_5

// Balanced intelligence and speed (recommended)
AnthropicModel.CLAUDE_SONNET_4_5

// Fast and efficient
AnthropicModel.CLAUDE_HAIKU_3_5
```

### A6. 测试基本设置

在 Teams 中发送一条消息，以验证 Claude 是否能够正常响应。

---

## 路径 B：使用 You.com MCP

在基于 Claude 的 Teams 应用程序中添加网页搜索和内容提取功能。

### B1. 安装包

```bash
npm install @youdotcom-oss/teams-anthropic @anthropic-ai/sdk @microsoft/teams.ai @microsoft/teams.mcpclient
```

### B2. 获取 API 密钥

- **Anthropic API 密钥**：[console.anthropic.com](https://console.anthropic.com/)
- **You.com API 密钥**：[you.com/platform/api-keys](https://you.com/platform/api-keys)

```bash
# Add to .env
ANTHROPIC_API_KEY=your-anthropic-api-key
YDC_API_KEY=your-you-com-api-key
```

### A3. 选择新应用还是现有应用？
- **新创建的应用程序**：使用以下完整模板
- **现有应用程序**：将 MCP 功能添加到现有的 Claude 设置中

### B4. MCP 模板

**对于新创建的应用程序：**

```typescript
import { App } from '@microsoft/teams.apps';
import { ChatPrompt } from '@microsoft/teams.ai';
import { ConsoleLogger } from '@microsoft/teams.common';
import { McpClientPlugin } from '@microsoft/teams.mcpclient';
import {
  AnthropicChatModel,
  AnthropicModel,
  getYouMcpConfig,
} from '@youdotcom-oss/teams-anthropic';

// Validate environment
if (!process.env.ANTHROPIC_API_KEY) {
  throw new Error('ANTHROPIC_API_KEY environment variable is required');
}

if (!process.env.YDC_API_KEY) {
  throw new Error('YDC_API_KEY environment variable is required');
}

// Configure logger
const logger = new ConsoleLogger('mcp-client', { level: 'info' });

// Create prompt with MCP integration
const prompt = new ChatPrompt(
  {
    instructions: 'You are a helpful assistant with access to web search and content extraction. Use these tools to provide accurate, up-to-date information.',
    model: new AnthropicChatModel({
      model: AnthropicModel.CLAUDE_SONNET_4_5,
      apiKey: process.env.ANTHROPIC_API_KEY,
      requestOptions: {
        max_tokens: 2048,
      },
    }),
  },
  [new McpClientPlugin({ logger })],
).usePlugin('mcpClient', getYouMcpConfig());

const app = new App();

app.on('message', async ({ send, activity }) => {
  await send({ type: 'typing' });

  const result = await prompt.send(activity.text);
  if (result.content) {
    await send(result.content);
  }
});

app.start().catch(console.error);
```

**对于已使用 Claude 的现有应用程序：**

如果您已经完成了路径 A 的设置，需要添加 MCP 集成：
1. **安装 MCP 依赖项：**
   ```bash
   npm install @microsoft/teams.mcpclient
   ```

2. **添加导入语句：**
   ```typescript
   import { ChatPrompt } from '@microsoft/teams.ai';
   import { ConsoleLogger } from '@microsoft/teams.common';
   import { McpClientPlugin } from '@microsoft/teams.mcpclient';
   import { getYouMcpConfig } from '@youdotcom-oss/teams-anthropic';
   ```

3. **验证 You.com API 密钥：**
   ```typescript
   if (!process.env.YDC_API_KEY) {
     throw new Error('YDC_API_KEY environment variable is required');
   }
   ```

4. **将模型替换为 ChatPrompt：**
   ```typescript
   const logger = new ConsoleLogger('mcp-client', { level: 'info' });

   const prompt = new ChatPrompt(
     {
       instructions: 'Your instructions here',
       model: new AnthropicChatModel({
         model: AnthropicModel.CLAUDE_SONNET_4_5,
         apiKey: process.env.ANTHROPIC_API_KEY,
       }),
     },
     [new McpClientPlugin({ logger })],
   ).usePlugin('mcpClient', getYouMcpConfig());
   ```

5. **使用 `prompt.send()` 替代 `model.send()`：**
   ```typescript
   const result = await prompt.send(activity.text);
   ```

### B5. 测试 MCP 集成

向 Claude 提出一个需要网页搜索的问题：
- “AI 的最新发展是什么？”
- “搜索 React 的文档”
- “从 https://example.com 提取内容”

---

## 可用的 Claude 模型

| 模型 | 枚举值 | 适用场景 |
|-------|------|----------|
| Claude Opus 4.5 | `AnthropicModel.CLAUDE_OPUS_4_5` | 适合复杂任务，功能最强大 |
| Claude Sonnet 4.5 | `AnthropicModel.CLAUDE_SONNET_4_5` | 智能与速度平衡（推荐） |
| Claude Haiku 3.5 | `AnthropicModel.CLAUDE_HAIKU_3_5` | 响应速度快，效率高 |
| Claude Sonnet 3.5 | `AnthropicModel.CLAUDE_SONNET_3_5` | 旧版本，稳定性较好 |

## 高级功能

### 流式响应

```typescript
const response = await model.send(
  { role: 'user', content: 'Write a short story' },
  {
    onChunk: async (delta) => {
      // Stream each token as it arrives
      process.stdout.write(delta);
    },
  }
);
```

### 函数调用

```typescript
const response = await model.send(
  { role: 'user', content: 'What is the weather in San Francisco?' },
  {
    functions: {
      get_weather: {
        description: 'Get the current weather for a location',
        parameters: {
          location: { type: 'string', description: 'City name' },
        },
        handler: async (args: { location: string }) => {
          // Your API call here
          return { temperature: 72, conditions: 'Sunny' };
        },
      },
    },
  }
);
```

### 对话记忆功能

```typescript
import { LocalMemory } from '@microsoft/teams.ai';

const memory = new LocalMemory();

// First message
await model.send(
  { role: 'user', content: 'My name is Alice' },
  { messages: memory }
);

// Second message - Claude remembers
const response = await model.send(
  { role: 'user', content: 'What is my name?' },
  { messages: memory }
);
// Response: "Your name is Alice."
```

## 验证清单

### 路径 A 的验证清单

- [ ] 已安装 `@youdotcom-oss/teams-anthropic` 包
- [ ] 环境变量 `ANTHROPIC_API_KEY` 已设置
- [ ] 模型配置为 `AnthropicChatModel`
- [ ] 选择了合适的模型（Opus/Sonnet/Haiku）
- [ ] 应用程序已通过基本消息进行测试

### 路径 B 的验证清单

- [ ] 已完成路径 A 的所有步骤
- [ ] 安装了 `@microsoft/teams.mcpclient` 包
- [ ] 环境变量 `YDC_API_KEY` 已设置
- [ ] 日志记录器已配置
- [ ] `ChatPrompt` 已通过 `getYouMcpConfig()` 进行配置
- [ ] 应用程序已通过网页搜索查询进行测试

## 常见问题

### 路径 A 的问题

- **“无法找到模块 @youdotcom-oss/teams-anthropic”**
  解决方法：确保已正确安装该包。

- **“需要设置 ANTHROPIC_API_KEY 环境变量”**
  从 [console.anthropic.com](https://console.anthropic.com/) 获取密钥，并将其添加到 `.env` 文件中（例如：`ANTHROPIC_API_KEY=your-key-here`）。

- **“模型标识符无效”**
  使用正确的枚举值：`AnthropicModel.CLAUDE_SONNET_4_5`，不要使用字符串格式（如 `'claude-sonnet-4-5-20250929'`）。

### 路径 B 的问题

- **“需要设置 YDC_API_KEY 环境变量”**
  从 [you.com/platform/api-keys](https://you.com/platform/api-keys) 获取密钥，并将其添加到 `.env` 文件中（例如：`YDC_API_KEY=your-key-here`）。

- **“MCP 连接失败”**
  确保 API 密钥有效，并检查网络连接；查看日志以获取更多信息。

- **“无法找到模块 @microsoft/teams.mcpclient”**
  确保已正确安装该包。

## getYouMcpConfig() 工具

该工具可自动配置 You.com MCP 连接：
- **URL**：`https://api.you.com/mcp`
- **认证方式**：使用 `YDC_API_KEY` 生成的 bearer token
- **User-Agent**：包含包版本信息，用于日志记录

```typescript
// Option 1: Use environment variable (recommended)
getYouMcpConfig()

// Option 2: Custom API key
getYouMcpConfig({ apiKey: 'your-custom-key' })
```

## 资源

- **包**：[https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/teams-anthropic](https://github.com/youdotcom-oss/dx-toolkit/tree/main/packages/teams-anthropic)
- **You.com MCP**：[https://documentation.you.com/developer-resources/mcp-server](https://documentation.you.com/developer-resources/mcp-server)
- **Anthropic API**：[https://console.anthropic.com/](https://console.anthropic.com/)
- **You.com API 密钥**：[https://you.com/platform/api-keys](https://you.com/platform/api-keys)