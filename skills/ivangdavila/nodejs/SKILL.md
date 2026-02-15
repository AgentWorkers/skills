---
name: NodeJS
slug: nodejs
version: 1.0.1
description: 编写可靠的 Node.js 代码时，需要避免以下问题：事件循环阻塞、异步编程中的常见陷阱、ESM（ECMAScript Modules）的使用误区以及内存泄漏。
metadata: {"clawdbot":{"emoji":"💚","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## 快速参考

| 主题 | 文件 |
|-------|------|
| 回调函数、Promise、async/await、事件循环 | `async.md` |
| CommonJS 与 ESM、`require` 与 `import` | `modules.md` |
| 错误处理、未捕获的异常 | `errors.md` |
| 可读性、可写性、数据转换、背压机制 | `streams.md` |
| 内存泄漏、事件循环阻塞、性能分析 | `performance.md` |
| 输入验证、依赖管理、环境变量 | `security.md` |
| Jest、Mocha、模拟测试、集成测试 | `testing.md` |
| npm、`package.json`、锁文件、代码发布 | `packages.md` |

## 常见陷阱

- `fs.readFileSync` 会阻塞整个服务器进程——请使用 `fs.promises.readFile`  
- 在 Node.js 15 及更高版本中，未处理的异常会导致程序崩溃——务必使用 `.catch()` 或 `try/catch` 来捕获异常  
- `process.env` 的值是字符串类型——“3000” 应该被转换为数字（使用 `parseInt`）  
- `JSON.parse` 在遇到无效数据时会抛出错误——需要使用 `try/catch` 来处理  
- `require()` 会缓存模块的导出内容——这可能导致不同地方的代码使用到相同的模块实例  
- 循环依赖关系会导致导出不完整——请重新设计代码结构以避免这种情况  
- 事件监听器会不断累积——请使用 `removeListener` 或 `once()` 来清理监听器  
- 即使只是简单的返回语句，`async` 代码也会返回一个 Promise  
- 使用 `pipeline()` 而不是 `.pipe()` 可以更好地处理错误并确保资源得到正确清理  
- 在 ESM 模块中无法直接使用 `__dirname`——请使用 `fileURLToPath(import.meta.url)` 来获取文件路径  
- `Buffer.from(string)` 的编码方式很重要，默认使用 UTF-8 编码