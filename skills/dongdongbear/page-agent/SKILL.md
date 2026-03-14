---
name: page-agent
license: MIT
description: 通过 PageAgent 的 page-controller，实现了对浏览器 DOM 的增强型操作。该工具可以注入到任何网页中，从而实现精确的 DOM 提取、交互式元素检测（基于光标/指针的检测机制）以及强大的交互功能（包括完整事件链的模拟和与 React 兼容的输入操作）。当你需要对网页进行精确操作时（如点击、输入、滚动、填写表单或读取页面结构），可以使用该工具。它与前端设计技能相结合，形成了从设计到代码实现再到浏览器操作的完整工作流程。
---
# PageAgent浏览器增强技能

通过浏览器的`evaluate`动作，将[alibaba/page-agent](https://github.com/alibaba/page-agent) v1.5.6版本的`PageController`注入网页中。这比基本的浏览器操作提供了更强大的DOM操作能力。

## 相比基本浏览器工具的主要优势

1. **智能的鼠标指针检测**——即使没有语义标签也能识别可点击元素。
2. **完整的事件链**——支持`mouseenter`→`mouseover`→`mousedown`→`focus`→`mouseup`→`click`（而不仅仅是`.click()`）。
3. **兼容React/Vue的输入元素**——使用原生的值设置方式，绕过框架的拦截机制。
4. **支持可编辑内容**——正确触发`beforeinput`和`input`事件。
5. **可索引的元素**——采用`[N]<tag>`格式，便于对元素进行精确的操作。
6. **增量式变化检测**——使用`*[N]`标记来标识自上一步操作后新出现的元素。

## 使用流程

### 第1步：将PageController注入页面

使用CDP注入脚本（负责注入72KB大小的库文件）：

```bash
node ~/.openclaw/workspace/skills/page-agent/scripts/inject-cdp.mjs <TARGET_ID>
```

其中`TARGET_ID`来自`browser(action="open", ...)`。该脚本会通过CDP WebSocket注入`page-controller-global.js`和`inject.js`文件，并在成功注入后输出`✅ injected`。

### 第2步：获取页面状态（提取DOM结构）

```javascript
// Returns { url, title, header, content, footer }
// content is the LLM-readable simplified HTML with indexed interactive elements
const state = await window.__PA__.getState();
return JSON.stringify({ url: state.url, title: state.title, content: state.content, footer: state.footer });
```

`content`字段的内容如下所示：
```
[0]<a aria-label=首页 />
[1]<div >PageAgent />
[2]<button role=button>快速开始 />
[3]<input placeholder=搜索... type=text />
```

### 第3步：通过索引执行操作

```javascript
// Click element at index 2
await window.__PA__.click(2);

// Type text into input at index 3
await window.__PA__.input(3, "hello world");

// Select dropdown option
await window.__PA__.select(5, "Option A");

// Scroll down 1 page
await window.__PA__.scroll(true, 1);

// Scroll specific element
await window.__PA__.scrollElement(4, true, 1);
```

### 第4步：操作后重新读取页面状态

每次操作后，再次调用`getState()`以获取更新后的DOM结构。注意`*[N]`标记，它们表示新出现的元素。

## 实际工作流程：设计 → 编码 → 操作

1. **设计**：使用`frontend-design`技能创建页面。
2. **部署**：启动本地开发服务器（`npx serve`或框架自带的开发服务器）。
3. **打开页面**：使用`browser(action="open", targetUrl="http://localhost:3000")`打开页面。
4. **注入**：将PageController注入页面（参见第1步）。
5. **检查**：获取DOM结构以了解当前页面内容。
6. **操作**：点击、输入、滚动等，以测试和交互页面内容。
7. **迭代**：根据观察结果修改代码，重新注入脚本，重复上述步骤。

## 使用技巧

- 在页面导航后务必重新注入脚本（单页应用（SPA）的路由变化不影响注入效果，但完全重新加载页面需要重新注入脚本）。
- `content`输出结果更加高效（占用存储空间少），尽可能使用它代替截图。
- 对于长页面，使用`scroll`和`getState`来查看折叠部分以下的内容。
- 在截图前使用`window.__PA__.cleanUp()`清除高亮显示的内容。
- 使用`profile="openclaw"`来使用独立的浏览器环境，或使用`profile="chrome"`来使用Chrome扩展程序进行交互。

## 相关文件

- `scripts/page-controller.js`：PageController库文件（72KB，来自@page-agent/page-controller@1.5.6版本）。
- `scripts/inject.js`：用于创建`window.__PA__` API的辅助脚本。