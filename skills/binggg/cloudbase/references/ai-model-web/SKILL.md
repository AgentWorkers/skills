---
name: ai-model-web
description: 在开发需要人工智能功能的浏览器/Web应用程序（React/Vue/Angular）、静态网站或单页应用程序（SPA）时，请使用此技能。该技能支持通过 @cloudbase/js-sdk 实现文本生成（generateText）和流式传输（streamText）功能。内置的模型包括 Hunyuan（推荐使用 hunyuan-2.0-instruct-20251111）和 DeepSeek（推荐使用 deepseek-v3.2）。请注意：该技能不适用于 Node.js 后端（请使用 ai-model-nodejs）、微信小程序（请使用 ai-model-wechat），也不适用于图像生成（仅支持 Node.js SDK）。
alwaysApply: false
---
## 何时使用此技能

使用此技能可以通过 `@cloudbase/js-sdk` 在浏览器/Web 应用程序中调用 AI 模型。

**在以下情况下使用此技能：**
- 将 AI 文本生成功能集成到前端 Web 应用程序中
- 以流式方式获取 AI 响应，从而提供更好的用户体验
- 从浏览器中调用 Hunyuan 或 DeepSeek 模型

**请勿在以下情况下使用此技能：**
- Node.js 后端或云函数 → 请使用 `ai-model-nodejs` 技能
- 微信小程序 → 请使用 `ai-model-wechat` 技能
- 图像生成 → 请使用 `ai-model-nodejs` 技能（仅限 Node SDK）
- HTTP API 集成 → 请使用 `http-api` 技能

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
npm install @cloudbase/js-sdk
```

## 初始化

```js
import cloudbase from "@cloudbase/js-sdk";

const app = cloudbase.init({
  env: "<YOUR_ENV_ID>",
  accessKey: "<YOUR_PUBLISHABLE_KEY>"  // Get from CloudBase console
});

const auth = app.auth();
await auth.signInAnonymously();

const ai = app.ai();
```

**重要说明：**
- 始终使用顶层导入进行同步初始化
- 在使用 AI 功能之前，用户必须先进行身份验证
- 从 CloudBase 控制台获取 `accessKey`

---

## generateText() - 非流式调用

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

## streamText() - 流式调用

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

---

## 最佳实践：
1. **对于较长的响应，使用流式调用** – 以提供更好的用户体验
2. **优雅地处理错误** – 将 AI 调用放在 `try/catch` 块中
3. **保护 `accessKey` 的安全性** – 使用可公开的关键字（而非秘密密钥）
4. **尽早初始化** – 在应用程序的入口点初始化 SDK
5. **确保身份验证** – 在调用 AI 功能之前，用户必须登录