---
name: Bun
slug: bun
version: 1.0.0
description: "使用 Bun 运行时进行构建，可以避免与 Node.js 兼容性相关的问题、打包工具（bundler）的陷阱以及包管理器（package manager）使用中的常见错误。"
metadata: {"clawdbot":{"emoji":"🥟","requires":{"bins":["bun"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户需要快速运行 JavaScript/TypeScript 代码、使用打包工具（bundler）以及管理项目依赖包（package manager）时，Bun 是一个理想的选择。Bun 还能帮助用户从 Node.js 迁移到新的开发环境，并解决运行时兼容性问题。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| Node.js API 的差异 | `node-compat.md` |
| 打包工具配置 | `bundler.md` |
| 项目依赖管理 | `packages.md` |

## 运行时兼容性问题

- `process.nextTick` 的执行时机与 Node.js 不同，可能导致竞态条件；对于跨平台的代码，应使用 `queueMicrotask`。
- 在 ESM（ES Module Standard）模式下，`__dirname` 和 `__filename` 不存在，需要使用 `import.meta.dir` 和 `import.meta.file`；忽略这些差异可能会导致 `ReferenceError`。
- `fs.watch` 的事件检测机制与 Node.js 不同，文件变更可能无法被及时捕获；建议添加轮询机制作为备用方案。
- `child_process.spawn` 的部分参数在 Bun 中未被正确支持，某些标准输入/输出（stdio）配置可能会被忽略；需要显式测试子进程的运行情况。
- 如果代码使用了 `cluster` 模块，应用程序可能会立即崩溃；此时需要将代码重构为使用工作进程（workers）来处理任务。

## 打包工具相关问题

- 使用 `--target=browser` 选项时，Node.js 的 API 会被默默地移除；虽然构建过程成功，但在运行时可能会因为 `fs`、`path` 等模块的错误而崩溃。
- 使用 `--splitting` 选项时，必须同时指定 `--format=esm`；否则编译会出错，但错误信息不够明确。
- 默认情况下，所有代码都会被打包在一起；对于服务器端代码，需要使用 `--external:package` 选项来指定外部依赖。
- Tree-shaking（代码优化机制）可能会移除具有副作用的代码；如果代码有副作用，需要在 `package.json` 中设置 `"sideEffects": false`，否则代码可能会被删除。

## 项目依赖管理相关问题

- `bun.lockb` 文件采用二进制格式，无法直接进行差异对比或合并；Git 合并时可能会产生冲突，需要手动删除并重新生成 `bun.lockb` 文件。
- 与 npm 不同，Bun 会自动安装依赖包；版本冲突可能会在编译过程中无声地发生，且选择的版本可能与 npm 不同。
- `bun install` 的行为与 npm 不同；在某些情况下，使用 Bun 安装依赖包后，代码可能在其他开发者的机器上无法正常运行。
- 工作区（workspace）的 `link:` 协议在 Bun 中的表现与 npm 不同，可能导致导入失败。
- `bun add` 操作会修改 `package.json` 的格式，这可能会在代码提交时引起不必要的差异。
- Bun 没有类似于 npm 的安全审计工具（`npm audit`），因此安全漏洞可能无法自动被发现。

## TypeScript 相关问题

- Bun 会直接编译 TypeScript 代码，而不会通过 `tsc`；类型错误可能不会被捕获，从而导致错误代码被部署到生产环境中。
- 如果项目中只使用了类型声明（type-only imports），打包后的文件大小可能会超出预期。
- `tsconfig.json` 中的路径设置可能与 Node.js + `tsc` 的环境不同，导致导入失败。
- Bun 中的装饰器属于实验性功能，其行为可能与 `tsc` 不同，尤其是对于一些旧的装饰器。

## 测试相关问题

- `bun test` 的断言 API 与 Jest 不兼容；为 Jest 编写的测试代码可能需要进行调整。
- Bun 的模拟（mocking）机制与 Jest 不同，可能会导致测试结果不稳定。
- Bun 没有像 c8/nyc 这样的代码覆盖率工具，因此需要使用其他工具来检测代码覆盖率。
- Bun 的快照生成格式与 Jest 不兼容，无法在不同的测试环境中共享快照结果。

## 热重载相关问题

- 使用 `bun --hot` 选项时，某些原生模块不会被自动重新加载；因此，代码变更需要手动重启应用程序才能生效。
- 由于状态在重载过程中会被保留，基于旧状态产生的错误可能难以调试。
- WebSocket 连接在重载后可能无法重新建立，导致客户端看似已连接但实际上已断开连接。