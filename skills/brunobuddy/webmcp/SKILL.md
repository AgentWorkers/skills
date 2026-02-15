---
name: webmcp
description: 此技能适用于在浏览或自动化通过 WebMCP API（`window.navigator.modelContext`）提供工具的网页时使用。它教会代理如何发现、检查并调用网站上的 WebMCP 工具，而不是依赖于 DOM 抓取或用户界面操作。
---

# WebMCP — 发现并使用网站工具

## 什么是 WebMCP

WebMCP 是一个浏览器 API，它允许网站将 JavaScript 函数暴露为结构化的工具，供 AI 代理使用。页面通过 `window.navigator.modelContext` 注册这些工具，每个工具都包含一个名称、描述、JSON Schema 输入格式以及一个 `execute` 回调函数。可以将其视为运行在网页内部的 MCP 服务器。

规范：https://github.com/webmachinelearning/webmcp

## 检测 WebMCP 支持

在与工具交互之前，请先检查当前页面是否支持 WebMCP：

```js
const supported = "modelContext" in window.navigator;
```

如果返回 `false`，则表示该页面不支持 WebMCP 工具——此时应切换到使用 DOM 进行交互或执行其他操作。

## 发现可用工具

工具由页面通过 `provideContext()` 或 `registerTool()` 方法进行注册。浏览器负责处理对这些工具的访问。要从代理的角度列出所有可用工具，可以执行以下操作：

```js
// Browser-specific — the exact discovery API depends on the agent runtime.
// Typically the browser exposes registered tools to connected agents automatically.
// From page-script perspective, tools are registered like this:
window.navigator.modelContext.provideContext({
  tools: [
    {
      name: "tool-name",
      description: "What this tool does",
      inputSchema: { type: "object", properties: { /* ... */ }, required: [] },
      execute: (params, agent) => { /* ... */ }
    }
  ]
});
```

- 每个工具都包含 `name`（名称）、`description`（描述）、`inputSchema`（JSON Schema 输入格式）以及 `execute`（执行函数）。
- `provideContext()` 会替换之前注册的所有工具（这对于单页应用程序（SPA）的状态更新非常有用）。
- `registerTool()` 和 `unregisterTool()` 可以单独添加或删除工具，而不会重置整个工具列表。
- 随着用户浏览或单页应用程序状态的更新，工具列表可能会发生变化——页面切换后需要重新检查可用工具。

## 工具的输入格式

工具的输入格式遵循 JSON Schema 规范（与 MCP SDK 和 Prompt API 的工具使用方式保持一致）：

```js
{
  name: "add-stamp",
  description: "Add a new stamp to the collection",
  inputSchema: {
    type: "object",
    properties: {
      name: { type: "string", description: "The name of the stamp" },
      year: { type: "number", description: "Year the stamp was issued" },
      imageUrl: { type: "string", description: "Optional image URL" }
    },
    required: ["name", "year"]
  },
  execute({ name, year, imageUrl }, agent) {
    // Implementation — updates UI and app state
    return {
      content: [{ type: "text", text: `Stamp "${name}" added.` }]
    };
  }
}
```

## 调用工具

当作为代理连接到页面时，可以通过工具的名称发送请求，并提供符合其输入格式的参数。`execute` 回调函数会在页面的主线程上执行，可以更新用户界面，并返回结构化的响应：

```js
// Response format from execute():
{
  content: [
    { type: "text", text: "Result description" }
  ]
}
```

- 工具在主线程上按顺序执行（一次一个）。
- `execute` 函数可能是异步的（返回一个 Promise）。
- 第二个参数 `agent` 提供了 `agent.requestUserInteraction()` 方法，用于处理用户确认流程。

## 工具执行过程中的用户交互

某些工具在执行敏感操作之前可能会请求用户的确认：

```js
async function buyProduct({ product_id }, agent) {
  const confirmed = await agent.requestUserInteraction(async () => {
    return confirm(`Buy product ${product_id}?`);
  });
  if (!confirmed) throw new Error("Cancelled by user.");
  executePurchase(product_id);
  return { content: [{ type: "text", text: `Product ${product_id} purchased.` }] };
}
```

务必尊重用户的拒绝操作——不要重试被取消的工具调用。

## 代理的工作流程

1. 导航到目标网站。
2. 通过 `window navigator.modelContext` 检查是否支持 WebMCP。
3. 发现已注册的工具（包括名称、描述和输入格式）。
4. 根据用户的目标和工具描述选择合适的工具。
5. 使用符合输入格式的参数调用该工具。
6. 读取工具返回的结构化响应，并将结果展示给用户。
7. 在单页应用程序导航或状态发生变化后，重新检查可用工具——工具列表可能会更新。
8. 如果没有合适的 WebMCP 工具能够完成任务，则切换到使用 DOM 进行交互。

## 重要限制

- **需要浏览器上下文**——工具仅在实时浏览环境中（例如标签页或网页视图中）可用，无法在无浏览器的环境中使用。
- **顺序执行**——工具调用在主线程上依次执行。
- **不允许跨源共享工具**——工具的作用范围仅限于注册它们的页面。
- **需要权限验证**——浏览器可能会在允许工具使用之前提示用户授权。
- **工具是动态的**——单页应用程序可以根据用户界面状态动态地注册或删除工具。