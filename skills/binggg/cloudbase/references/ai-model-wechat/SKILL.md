---
name: ai-model-wechat
description: 在开发需要人工智能功能的微信小程序（WeChat Mini Programs）、企业微信小程序（WeCom Mini Programs）或基于 wx.cloud 的应用程序时，请使用此技能。该技能支持文本生成（generateText）和流式文本处理（streamText）功能，并提供了回调接口（onText、onEvent、onFinish）以处理相关事件。这些功能是通过 wx.cloud.extend.AI 实现的。内置的模型包括 Hunyuan（推荐使用版本：hunyuan-2.0-instruct-20251111）和 DeepSeek（推荐使用版本：deepseek-v3.2）。需要注意的是，该 API 与 JavaScript/Node.js SDK 的实现方式有所不同：streamText 需要数据封装处理，而 generateText 则直接返回原始响应。此技能不适用于浏览器/Web 应用程序（请使用 ai-model-web），也不适用于 Node.js 后端（请使用 ai-model-nodejs），同时也不支持图像生成功能。
alwaysApply: false
---
## 何时使用此技能

使用此技能可以通过 `wx.cloud.extend.AI` 在微信小程序中调用 AI 模型。

**适用场景：**
- 将 AI 文本生成功能集成到小程序中
- 以流式方式获取 AI 响应，并支持回调函数
- 从微信环境中调用 Hunyuan 模型

**不适用场景：**
- 浏览器/Web 应用程序 → 使用 `ai-model-web` 技能
- Node.js 后端或云函数 → 使用 `ai-model-nodejs` 技能
- 图像生成 → 使用 `ai-model-nodejs` 技能（在小程序中不可用）
- HTTP API 集成 → 使用 `http-api` 技能

---

## 可用的提供者和模型

CloudBase 提供了以下内置的提供者和模型：

| 提供者 | 模型 | 推荐模型 |
|----------|--------|-------------|
| `hunyuan-exp` | `hunyuan-turbos-latest`, `hunyuan-t1-latest`, `hunyuan-2.0-thinking-20251109`, `hunyuan-2.0-instruct-20251111` | ✅ `hunyuan-2.0-instruct-20251111` |
| `deepseek` | `deepseek-r1-0528`, `deepseek-v3-0324`, `deepseek-v3.2` | ✅ `deepseek-v3.2` |

---

## 先决条件

- WeChat 基础库版本需达到 3.7.1 或更高
- 无需额外安装 SDK

---

## 初始化

```js
// app.js
App({
  onLaunch: function() {
    wx.cloud.init({ env: "<YOUR_ENV_ID>" });
  }
})
```

---

## generateText() - 非流式调用

⚠️ **与 JS/Node SDK 不同：** 返回值是模型的原始响应。

```js
const model = wx.cloud.extend.AI.createModel("hunyuan-exp");

const res = await model.generateText({
  model: "hunyuan-2.0-instruct-20251111",  // Recommended model
  messages: [{ role: "user", content: "你好" }],
});

// ⚠️ Return value is RAW model response, NOT wrapped like JS/Node SDK
console.log(res.choices[0].message.content);  // Access via choices array
console.log(res.usage);                        // Token usage
```

---

## streamText() - 流式调用

⚠️ **与 JS/Node SDK 不同：** 参数必须封装在 `data` 对象中，并支持回调函数。

```js
const model = wx.cloud.extend.AI.createModel("hunyuan-exp");

// ⚠️ Parameters MUST be wrapped in `data` object
const res = await model.streamText({
  data: {                              // ⚠️ Required wrapper
    model: "hunyuan-2.0-instruct-20251111",  // Recommended model
    messages: [{ role: "user", content: "hi" }]
  },
  onText: (text) => {                  // Optional: incremental text callback
    console.log("New text:", text);
  },
  onEvent: ({ data }) => {             // Optional: raw event callback
    console.log("Event:", data);
  },
  onFinish: (fullText) => {            // Optional: completion callback
    console.log("Done:", fullText);
  }
});

// Async iteration also available
for await (let str of res.textStream) {
  console.log(str);
}

// Check for completion with eventStream
for await (let event of res.eventStream) {
  console.log(event);
  if (event.data === "[DONE]") {       // ⚠️ Check for [DONE] to stop
    break;
  }
}
```

---

## API 对比：JS/Node SDK 与微信小程序

| 功能 | JS/Node SDK | 微信小程序 |
|---------|-------------|---------------------|
| **命名空间** | `app.ai()` | `wx.cloud.extend.AI` |
| **generateText` 参数** | 直接传递对象 | 直接传递对象 |
| **generateText` 返回值** | `{ text, usage, messages }` | 原始返回值： `{ choices, usage }` |
| **streamText` 参数** | 直接传递对象 | ⚠️ 必须封装在 `data: {...}` 中 |
| **streamText` 返回值** | `{ textStream, dataStream }` | `{ textStream, eventStream }` |
| **回调函数** | 不支持 | 支持 `onText`, `onEvent`, `onFinish` |
| **图像生成** | 仅支持 Node SDK | 在微信小程序中不可用 |

---

## 类型定义

### streamText() 的输入参数

```ts
interface WxStreamTextInput {
  data: {                              // ⚠️ Required wrapper object
    model: string;
    messages: Array<{
      role: "user" | "system" | "assistant";
      content: string;
    }>;
  };
  onText?: (text: string) => void;     // Incremental text callback
  onEvent?: (prop: { data: string }) => void;  // Raw event callback
  onFinish?: (text: string) => void;   // Completion callback
}
```

### streamText() 的返回值

```ts
interface WxStreamTextResult {
  textStream: AsyncIterable<string>;   // Incremental text stream
  eventStream: AsyncIterable<{         // Raw event stream
    event?: unknown;
    id?: unknown;
    data: string;                      // "[DONE]" when complete
  }>;
}
```

### generateText() 的返回值

```ts
// Raw model response (OpenAI-compatible format)
interface WxGenerateTextResponse {
  id: string;
  object: "chat.completion";
  created: number;
  model: string;
  choices: Array<{
    index: number;
    message: {
      role: "assistant";
      content: string;
    };
    finish_reason: string;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}
```

---

## 最佳实践：
1. **检查基础库版本**：确保使用 3.7.1 或更高版本以支持 AI 功能。
2. **使用回调函数进行 UI 更新**：`onText` 非常适合实时显示结果。
3. **检查完成信号**：在使用 `eventStream` 时，检查 `event.data === "[DONE]" 以停止调用。
4. **优雅地处理错误**：使用 try/catch 语句处理 AI 调用可能出现的错误。
5. **注意参数封装**：`streamText` 的参数必须使用 `data: {...}` 进行封装。