---
name: Chrome
description: Chrome DevTools 协议、扩展程序 Manifest V3 以及能够防止常见自动化故障的调试技巧。
---

## Chrome 开发者工具协议（CDP）

**先获取标签页的 WebSocket URL**：切勿直接连接到 `ws://localhost:9222/devtools/browser`。请先获取 `http://localhost:9222/json/list`，并使用当前活动标签页中的 `webSocketDebuggerUrl`。

**使用前需启用相关功能**：在执行任何 `Runtime.evaluate` 或 `Page.navigate` 命令之前，必须先调用 `Runtime.enable` 和 `Page.enable`。

**CDP 是异步的**：在发送下一个命令之前，请等待响应。建议使用基于 Promise 的封装方式，并跟踪响应 ID。

**高 DPI 显示器的截图**：在调用 `Page.captureScreenshot` 时，需设置参数 `fromSurface: true` 和 `scale: 2` 以适应 Retina 显示器。

**单独获取响应体**：`Network.responseReceived` 不包含响应内容。请在响应完成后，使用 `Network.getResponseBody` 并传入请求 ID。

## Chrome 扩展程序manifest V3**

**权限分离**：将 API 的权限放在 `permissions` 中，将 URL 的权限放在 `hostPermissions` 中。切勿在权限设置中使用 `http://*/*`。

**服务工作者的终止**：不要使用持久化状态。请使用 `chrome.storage.local` 代替全局变量，使用 `chrome.alarms` 代替 `setInterval`。

**内容脚本的隔离**：内容脚本无法访问页面的全局变量。请使用 `chrome.scripting.executeScript` 并指定函数上下文（`func`），以实现内容脚本与页面之间的通信。使用 `window.postMessage` 进行内容脚本与页面之间的数据交换。

**存储操作是异步的**：`chrome.storage.local.get()` 返回的是一个 Promise，而不是直接的数据。请务必使用 `await` 来等待结果，并处理可能出现的 `QUOTA_EXCEEDED` 错误。

## 上下文检测**

**确认当前环境是否为 Chrome**：检查 `window.chrome` 以及 `navigator.vendor` 是否等于 “Google Inc.”，以排除 Opera 或 Edge 浏览器。

**扩展程序的上下文类型**：
- 如果 `chrome.runtime.id` 存在，则表示当前处于内容脚本环境；
- 如果 `chrome.runtime.getManifest` 存在，则表示当前处于弹出窗口/后台选项页面环境；
- 如果 `chrome.loadTimes` 存在但 `chrome.runtime` 不存在，则表示当前处于普通的 Chrome 网页环境。

**manifest 版本检查**：调用 `chrome.runtime.getManifest()` 时，请使用 try-catch 语句来处理可能的错误。对于 V3 版本的扩展程序，使用 `chrome.action`；对于 V2 版本的扩展程序，使用 `chrome.browserAction`。

## 性能调试**

**条件性使用内存 API**：在访问 `performance.memory.usedJSHeapSize` 之前，请先检查 `‘memory’` 是否存在于 `performance` 对象中。

**使用性能标记**：使用 `performance.mark()` 和 `performance.measure()` 来记录子帧的耗时。使用 `performance.mark()` 清除不必要的性能标记，以防止内存泄漏。

**布局抖动检测**：使用 `PerformanceObserver` 并设置 `entryTypes` 为 `['measure', 'paint', 'largest-contentful-paint']`。将耗时超过 16.67ms 的操作标记记录下来。

## 网络调试**

**在导航前进行拦截**：请在调用 `Page.navigate` 之前，先调用 `Network.setBlockedURLs`。

**请求拦截**：使用 `Network 请求拦截` 并设置 `requestStage` 为 `Request`，以实现更细粒度的控制。如果需要阻止某个请求，可以返回 `errorReason: 'BlockedByClient`。

## 安全上下文**

**混合内容**：HTTPS 页面无法加载 HTTP 资源。请检查 `location.protocol` 与资源 URL 是否一致。

**CORS 错误**：跨源请求时出现 `TypeError` 通常表示存在 CORS 问题。请查看 Chrome 开发者工具的网络面板以获取具体的错误信息。

**安全上下文要求**：使用文件系统访问 API 或剪贴板 API 时，必须确保 `window.isSecureContext === true` 并且用户已进行相应的操作（如授权）。