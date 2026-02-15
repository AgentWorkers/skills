---
name: NodeJS
description: 避免常见的 Node.js 错误：事件循环阻塞、异步错误处理问题、ESM（ECMAScript Modules）的使用误区以及内存泄漏。
metadata: {"clawdbot":{"emoji":"💚","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## 事件循环（Event Loop）
- `fs.readFileSync` 会阻塞整个服务器的运行——建议使用 `fs.promises.readFile` 或带有回调函数的版本。
- 需要大量 CPU 资源的代码块应卸载到工作线程或子进程中执行。
- `setImmediate` 与 `process.nextTick` 的区别：`process.nextTick` 会在 I/O 操作之前执行，而 `setImmediate` 会在 I/O 操作之后执行。
- 长时间运行的循环会占用过多的 I/O 资源——可以使用 `setImmediate` 将循环拆分成多个小块来执行。

## 异步错误处理（Async Error Handling）
- 在 Node.js 15 及更高版本中，未处理的 Promise 拒绝（rejection）会导致程序崩溃——务必使用 `.catch()` 或 `try/catch` 语句，并结合 `await`。
- 使用 `process.on('unhandledRejection')` 来全局处理未处理的错误——记录错误并优雅地退出程序。
- 回调函数中的错误需要显式处理——否则错误不会传播到外层的 `try/catch` 语句中。
- `Promise.all` 会快速失败：如果有一个 Promise 被拒绝，所有 Promise 都会被拒绝；如果需要获取所有结果，可以使用 `Promise.allSettled`。

## CommonJS 与 ESM（CommonJS vs ESM）
- 在 `package.json` 中，ESM 模块的类型应设置为 `"module"`；否则应使用 `.mjs` 扩展名。
- ESM：`import x from 'y'`；CommonJS：`const x = require('y')`。
- ESM 模块中没有 `__dirname` 属性——可以使用 `import.meta.url` 和 `fileURLToPath` 来获取文件路径。
- 无法直接使用 `require()` 来加载 ESM 模块——需要使用动态的 `import()` 函数，该函数会返回一个 Promise。
- `exports` 是对 `module.exports` 的引用——重新赋值 `exports = x` 会破坏模块的导出机制。

## 环境变量（Environment Variables）
- `process.env` 中的值始终是字符串类型——例如 `PORT=3000` 表示 `"3000"`，而不是 `3000`。
- 如果环境变量缺失，其值为 `undefined`，而不是错误——应显式检查或使用默认值。
- `.env` 文件需要使用 `dotenv` 来加载环境变量——`dotenv` 不是内置的，需要提前调用 `dotenv.config()`。
- 不要直接修改 `.env` 文件——可以使用包含虚拟值的 `.env.example` 文件来进行测试。

## 内存泄漏（Memory Leaks）
- 事件监听器可能会累积——使用 `removeListener` 在不再需要时移除监听器，或者使用 `once` 函数来确保监听器只执行一次。
- 如果闭包捕获了大型对象，使用 `null` 来释放对这些对象的引用。
- 全局缓存可能会无限增长——使用具有大小限制的 LRU（最近最少使用）缓存机制。
- 可以通过 `--max-old-space-size` 参数来增加内存堆的大小——但首先需要修复内存泄漏问题。

## 流（Streams）
- 当缓冲区满时，`write()` 方法会返回 `false`——需要等待 `drain` 事件才能继续写入。
- `.pipe()` 方法可以自动处理背压（backpressure）——建议优先使用它而不是手动进行读写操作。
- 所有流都需要进行错误处理——使用 `stream.on('error', handler)` 来捕获错误，或者让错误在管道中默默地被忽略。
- 使用 `pipeline()` 而不是 `.pipe()` 可以更好地处理错误并确保资源得到正确清理。

## 常见错误（Common Mistakes）
- `JSON.parse` 在遇到无效的 JSON 数据时会抛出异常——应使用 `try/catch` 语句来捕获异常。
- `require()` 会缓存已加载的模块——多次调用时会返回相同的模块实例。
- 循环依赖关系可能部分生效——但在模块被加载时，导出的内容可能还不完整。
- `async` 函数总是返回一个 Promise——即使你返回的是普通值也是如此。
- `Buffer.from(string)` 的编码方式很重要——默认编码是 UTF-8，如果需要使用其他编码方式，请明确指定。