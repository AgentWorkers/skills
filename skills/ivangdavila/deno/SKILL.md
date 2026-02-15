---
name: Deno
slug: deno
version: 1.0.0
description: "使用 Deno 运行时进行构建，可以避免权限问题、URL 导入错误以及 Node.js 迁移过程中可能遇到的陷阱。"
metadata: {"clawdbot":{"emoji":"🦕","requires":{"bins":["deno"]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户需要利用Deno的强大功能时，Deno能够为TypeScript运行时环境提供安全保障，并支持权限管理。Deno的代理服务器负责处理权限配置、通过URL或npm管理依赖项，以及帮助应用程序从Node.js环境进行迁移。

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 权限系统 | `permissions.md` |
| 导入与依赖项 | `imports.md` |
| 从Node.js迁移 | `node-compat.md` |

## 常见问题与陷阱

### 权限配置相关问题
- 在开发环境中使用`--allow-all`选项可能会导致生产环境崩溃，因为此时你并不知道应用程序实际需要哪些权限。
- 使用`--allow-read`选项时如果没有指定路径，将会允许访问整个文件系统，从而引发安全风险。
- 使用`--allow-run`选项时如果没有指定允许执行的命令，子进程可能会执行任意操作；正确的用法是`--allow-run=git,npm`。
- 使用`--allow-env`选项时如果没有指定允许访问的环境变量，所有环境变量都会被暴露；正确的用法是`--allow-env=API_KEY,DATABASE_URL`。
- 使用`--allow-net`选项时如果没有指定允许访问的域名，应用程序可能会连接到任何网站；正确的用法是`--allow-net=api.example.com`。
- 在持续集成（CI）环境中如果未设置`--no-prompt`选项，系统会无限等待用户输入权限确认，此时应添加该选项以避免卡顿。

### 导入相关问题
- 在生产环境中使用远程URL时，如果网络失败，应用程序可能无法启动；此时应确保依赖项为本地版本。
- 默认情况下Deno不使用锁文件（`deno.lock`），这可能导致每次运行时依赖项版本发生变化；务必使用`deno.lock`来锁定依赖项版本。
- 如果项目中不存在`@^1.0.0`这样的Semver版本格式，应使用具体的URL或导入映射文件。
- 如果导入映射文件的位置不正确（应在`deno.json`中，而不是单独的文件中），可能会导致导入失败（适用于Deno 2.x版本）。
- 如果需要使用HTTPS，由于默认情况下HTTP导入被禁止，因此可能需要手动配置；虽然大多数CDN支持HTTPS，但自托管环境可能需要特殊处理。
- 如果URL拼写错误，只有在运行时导入失败时才会发现问题。

### TypeScript相关问题
- 在导入文件时必须使用`.ts`扩展名，否则Deno会生成错误的导入语句。
- `tsconfig.json`中的路径设置会被忽略，Deno会使用`deno.json`中的导入映射文件，而不是`tsconfig.json`中的设置。
- 如果仅导入类型信息（type-only imports），必须使用`import type`语句，否则打包工具可能会出错。
- 注解（decorators）在Deno中的使用方式与TSC（TypeScript Compiler）不同，可能会导致兼容性问题。
- `/// <reference>`这样的导入语句在Deno中的处理方式也与TSC不同，可能会被忽略。

### 部署相关问题
- 使用`deno compile`命令编译代码时，生成的二进制文件大小至少为50MB。
- 使用`--cached-only`选项时需要先存在缓存文件；新服务器启动前需要先清除缓存。
- Deno的部署功能有限，不支持文件系统操作、子进程调用以及外部函数调用（FFI，Foreign Function Interface）。
- 环境变量的获取方式不同：在Deno中应使用`Deno.env.get("VAR")`，而不是`process.env.VAR`。
- 信号处理方式也有所不同：在Deno中应使用`Deno.addSignalListener`，而不是`process.on("SIGTERM")`。

### 测试相关问题
- `Deno.test`的测试框架与Jest不同，没有`describe`函数和类似的断言方式。
- 异步测试中如果未使用`await`关键字，测试可能会在Promise解析完成之前就视为通过。
- 如果没有正确关闭文件或连接资源，测试可能会失败。
- 测试环境可能需要与主代码不同的权限设置。
- 快照测试的格式与Jest的快照格式不同。

### npm兼容性问题
- 使用`npm:`作为依赖项指定符时，大多数包可以正常导入，但某些原生插件可能无法正常工作。
- 必须使用`node:`作为依赖项指定符；例如`import fs from 'fs'`在Deno中会失败，正确的写法是`import fs from 'node:fs'`。
- `node_modules`目录是可选的，可以通过在`deno.json`中设置`"nodeModulesDir": true`来启用它的使用。
- `package.json`中的脚本在Deno中可能不会被自动执行，需要通过`deno.json`中的任务来触发。
- 项目中的依赖项管理方式与Node.js不同，可能会导致依赖项版本不一致。

### 运行时差异
- `Deno.readTextFile`和`fs.readFile`的方法API不同，错误类型也有所不同。
- `fetch`函数是全局可用的，无需单独导入；这与Node.js 18及更高版本不同。
- 在Deno中，顶层`await`语句可以在任何地方使用，无需额外的包装。
- 权限是在运行时动态请求的，用户必须批准才能执行某些操作。