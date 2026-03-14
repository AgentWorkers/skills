---
name: ai-model-nodejs
description: 在开发需要人工智能功能的 Node.js 后端服务或 CloudBase 云函数（Express/Koa/NestJS、无服务器架构、后端 API）时，请使用此技能。该技能支持通过 @cloudbase/node-sdk ≥3.16.0 实现文本生成（generateText）、流式数据传输（streamText）以及图像生成（generateImage）功能。内置的模型包括 Hunyuan（推荐使用 hunyuan-2.0-instruct-20251111 版本）、DeepSeek（推荐使用 deepseek-v3.2 版本）以及用于图像处理的 hunyuan-image。这是唯一支持图像生成的 SDK。不适用于浏览器/Web 应用（请使用 ai-model-web）或微信小程序（请使用 ai-model-wechat）。
alwaysApply: false
---
## 何时使用此技能

使用此技能可以在 Node.js 后端或 CloudBase 云函数中通过 `@cloudbase/node-sdk` 调用 AI 模型。

**适用场景：**
- 将 AI 文本生成功能集成到后端服务中
- 使用 Hunyuan Image 模型生成图片
- 从 CloudBase 云函数中调用 AI 模型
- 进行服务器端的 AI 处理

**不适用场景：**
- 浏览器/Web 应用 → 使用 `ai-model-web` 技能
- 微信小程序 → 使用 `ai-model-wechat` 技能
- HTTP API 集成 → 使用 `http-api` 技能

---

## 可用的提供者和模型

CloudBase 提供了以下内置的提供者和模型：

| 提供者 | 模型 | 推荐模型 |
|----------|--------|-------------|
| `hunyuan-exp` | `hunyuan-turbos-latest`, `hunyuan-t1-latest`, `hunyuan-2.0-thinking-20251109`, `hunyuan-2.0-instruct-20251111` | ✅ `hunyuan-2.0-instruct-20251111` |
| `deepseek` | `deepseek-r1-0528`, `deepseek-v3-0324`, `deepseek-v3.2` | ✅ `deepseek-v3.2` |

---

## 安装

```bash
npm install @cloudbase/node-sdk
```

⚠️ **AI 功能需要 Node.js 版本 3.16.0 或更高。** 请使用 `npm list @cloudbase/node-sdk` 进行版本检查。

---

## 初始化

### 在 Cloud Functions 中

```js
const tcb = require('@cloudbase/node-sdk');
const app = tcb.init({ env: '<YOUR_ENV_ID>' });

exports.main = async (event, context) => {
  const ai = app.ai();
  // Use AI features
};
```

### 用于 AI 模型的 Cloud Function 配置

⚠️ **重要提示：** 在创建使用 AI 模型的云函数时（尤其是 `generateImage()` 和大型语言模型生成操作），请设置较长的超时时间，因为这些操作可能会比较耗时。

**使用 MCP 工具 `createFunction` 时：**
在 `func` 对象中设置 `timeout` 参数：
- **参数**：`func.timeout`（数值）
- **单位**：秒
- **范围**：1 - 900
- **默认值**：20 秒（通常对于 AI 操作来说太短）

**推荐的超时时间值：**
- **文本生成 (`generateText`)**：60-120 秒
- **流式文本生成 (`streamText`)**：60-120 秒
- **图像生成 (`generateImage`)**：300-900 秒（推荐值：900 秒）
- **组合操作**：900 秒（最大允许值）

### 在常规 Node.js 服务器中

```js
const tcb = require('@cloudbase/node-sdk');
const app = tcb.init({
  env: '<YOUR_ENV_ID>',
  secretId: '<YOUR_SECRET_ID>',
  secretKey: '<YOUR_SECRET_KEY>'
});

const ai = app.ai();
```

---

## generateText() - 非流式处理

```js
const model = ai.createModel("hunyuan-exp");

const result = await model.generateText({
  model: "hunyuan-2.0-instruct-20251111",  // Recommended model
  messages: [{ role: "user", content: "你好，请你介绍一下李白" }],
});

console.log(result.text);           // Generated text string
console.log(result.usage);          // { prompt_tokens, completion_tokens, total_tokens }
console.log(result.messages);       // Full message history
console.log(result.rawResponses);   // Raw model responses
```

---

## streamText() - 流式处理

```js
const model = ai.createModel("hunyuan-exp");

const res = await model.streamText({
  model: "hunyuan-2.0-instruct-20251111",  // Recommended model
  messages: [{ role: "user", content: "你好，请你介绍一下李白" }],
});

// Option 1: Iterate text stream (recommended)
for await (let text of res.textStream) {
  console.log(text);  // Incremental text chunks
}

// Option 2: Iterate data stream for full response data
for await (let data of res.dataStream) {
  console.log(data);  // Full response chunk with metadata
}

// Option 3: Get final results
const messages = await res.messages;  // Full message history
const usage = await res.usage;        // Token usage
```

---

## generateImage() - 图像生成

⚠️ **图像生成功能仅支持 Node.js SDK，不支持 JS SDK（Web）或微信小程序。**

```js
const imageModel = ai.createImageModel("hunyuan-image");

const res = await imageModel.generateImage({
  model: "hunyuan-image",
  prompt: "一只可爱的猫咪在草地上玩耍",
  size: "1024x1024",
  version: "v1.9",
});

console.log(res.data[0].url);           // Image URL (valid 24 hours)
console.log(res.data[0].revised_prompt);// Revised prompt if revise=true
```

### 图像生成参数

```ts
interface HunyuanGenerateImageInput {
  model: "hunyuan-image";      // Required
  prompt: string;                       // Required: image description
  version?: "v1.8.1" | "v1.9";         // Default: "v1.8.1"
  size?: string;                        // Default: "1024x1024"
  negative_prompt?: string;             // v1.9 only
  style?: string;                       // v1.9 only
  revise?: boolean;                     // Default: true
  n?: number;                           // Default: 1
  footnote?: string;                    // Watermark, max 16 chars
  seed?: number;                        // Range: [1, 4294967295]
}

interface HunyuanGenerateImageOutput {
  id: string;
  created: number;
  data: Array<{
    url: string;                        // Image URL (24h valid)
    revised_prompt?: string;
  }>;
}
```

---

## 类型定义

```ts
interface BaseChatModelInput {
  model: string;                        // Required: model name
  messages: Array<ChatModelMessage>;    // Required: message array
  temperature?: number;                 // Optional: sampling temperature
  topP?: number;                        // Optional: nucleus sampling
}

type ChatModelMessage =
  | { role: "user"; content: string }
  | { role: "system"; content: string }
  | { role: "assistant"; content: string };

interface GenerateTextResult {
  text: string;                         // Generated text
  messages: Array<ChatModelMessage>;    // Full message history
  usage: Usage;                         // Token usage
  rawResponses: Array<unknown>;         // Raw model responses
  error?: unknown;                      // Error if any
}

interface StreamTextResult {
  textStream: AsyncIterable<string>;    // Incremental text stream
  dataStream: AsyncIterable<DataChunk>; // Full data stream
  messages: Promise<ChatModelMessage[]>;// Final message history
  usage: Promise<Usage>;                // Final token usage
  error?: unknown;                      // Error if any
}

interface Usage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}
```