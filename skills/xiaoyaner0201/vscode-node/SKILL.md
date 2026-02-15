---
name: vscode-node
description: 通过连接到 OpenClaw Node 的 VS Code/Cursor IDE 来操作代码。该工具提供了 40 多个命令，用于文件操作、语言智能、Git 管理、测试、调试以及与 Cursor Agent CLI 的集成。当您需要读取/写入/编辑代码、导航代码定义/引用、运行测试、进行调试，或将编码任务委托给 Cursor Agent 时，可以使用该工具。
metadata:
  {"openclaw": {"requires": {"tools": ["nodes"]}}}
---
# VS Code / Cursor Node 技能

通过 OpenClaw Node 协议远程控制 VS Code 或其他支持 Cursor 的 IDE。

## 前提条件

- 安装了 `openclaw-node-vscode` 扩展程序，并已成功连接（状态栏显示 🟢）  
- 相关 Node 对象已在 `nodes status` 中显示  
- 所使用的命令必须在 Gateway 的 `allowCommands` 白名单中  

## 调用模式  

```
nodes invoke --node "<name>" --invokeCommand "<cmd>" --invokeParamsJson '{"key":"val"}'
```  

对于耗时较长的操作，需要同时设置 `invokeTimeoutMs`（Gateway 内部计时）和 `timeoutMs`（HTTP 层计时），且 `timeoutMs` 必须大于 `invokeTimeoutMs`。  

**超时设置指南：**  
| 类型 | invokeTimeoutMs | timeoutMs |  
|------|----------------|-----------|  
| 文件/编辑器/语言 | 15000 | 20000 |  
| Git | 30000 | 35000 |  
| 测试 | 60000 | 65000 |  
| 代理计划/请求 | 180000 | 185000 |  
| 代理执行 | 300000 | 305000 |  

## 命令分类  

| 分类 | 前缀 | 常用命令 | 参考文档 |  
|----------|--------|-------------|-----------|  
| **文件** | `vscode.file.*` | 读取、写入、编辑、删除 | [commands/file.md](references/commands/file.md) |  
| **目录** | `vscode.dir.*` | 列出文件 | [commands/file.md](references/commands/file.md) |  
| **语言** | `vscode.lang.*` | 查看定义、语法高亮、悬停提示、重命名、代码格式化 | [commands/language.md](references/commands/language.md) |  
| **编辑器** | `vscode.editor.*` | 切换活动文件、打开文件、选择内容 | [commands/editor.md](references/commands/editor.md) |  
| **诊断** | `vscode.diagnostics.*` | 获取诊断信息 | [commands/editor.md](references/commands/editor.md) |  
| **Git** | `vscode.git.*` | 查看状态、比较差异、查看提交历史、暂存文件 | [commands/git.md](references/commands/git.md) |  
| **测试** | `vscode.test.*` | 列出测试用例、运行测试、查看结果 | [commands/test-debug.md](references/commands/test-debug.md) |  
| **调试** | `vscode.debug.*` | 启动调试会话、停止调试、设置断点、计算表达式、查看堆栈跟踪 | [commands/test-debug.md](references/commands/test-debug.md) |  
| **终端** | `vscode.terminal.*` | 运行命令（默认禁用） | [commands/terminal.md](references/commands/terminal.md) |  
| **代理** | `vscode.agent.*` | 查看代理状态、运行代理任务（仅限 Cursor） | [commands/agent.md](references/commands/agent.md) |  
| **工作区** | `vscode/workspace.*` | 查看工作区信息 | [commands/editor.md](references/commands/editor.md) |  

## 快速示例  

### 读取文件  
```
nodes invoke --node "my-vscode" --invokeCommand "vscode.file.read" --invokeParamsJson '{"path":"src/main.ts"}'
→ { content, totalLines, language }
```  

### 查找所有引用  
```
nodes invoke --node "my-vscode" --invokeCommand "vscode.lang.references" --invokeParamsJson '{"path":"src/main.ts","line":10,"character":5}'
→ { locations: [{ path, line, character }] }
```  

### 查看 Git 状态并提交更改  
```
nodes invoke --node "my-vscode" --invokeCommand "vscode.git.status"
→ { branch, staged, modified, untracked, ahead, behind }

nodes invoke --node "my-vscode" --invokeCommand "vscode.git.stage" --invokeParamsJson '{"paths":["src/main.ts"]}'
nodes invoke --node "my-vscode" --invokeCommand "vscode.git.commit" --invokeParamsJson '{"message":"fix: resolve type error"}'
```  

### 将任务委托给 Cursor 代理  
```
nodes invoke --node "my-vscode" --invokeCommand "vscode.agent.run" --invokeParamsJson '{"prompt":"Add error handling to all API endpoints","mode":"plan"}' --invokeTimeoutMs 180000 --timeoutMs 185000
→ { output, exitCode }
```  

## 常见工作流程  

详细的工作流程请参阅 [references/workflows.md](references/workflows.md)：  
- 修复类型错误  
- 安全地进行跨文件重构  
- 将复杂任务委托给 Cursor 代理执行  

## 错误处理  

| 错误类型 | 原因 | 解决方案 |  
|-------|-------|----------|  
| “不允许执行该 Node 命令” | 命令不在 Gateway 的允许列表中 | 将该命令添加到 `gateway.nodes.allowCommands` 中 |  
| “找不到 Node” | 扩展程序未连接 | 检查扩展程序的状态栏显示 |  
| 超时 | 操作耗时过长 | 增加 `invokeTimeoutMs` 和 `timeoutMs` 的值 |  
| 路径遍历失败 | 路径超出工作区范围 | 仅使用相对路径 |  
| 文件处于只读模式 | 扩展程序处于只读状态 | 取消 `openclaw.readOnly` 设置 |  

## 安全性注意事项  

- 所有路径均以工作区根目录为基准（绝对路径和 `../` 路径被禁止使用）  
- 写入操作会尊重扩展程序的 `readOnly` 和 `confirmWrites` 设置  
- 终端功能默认禁用，仅允许在白名单中的命令使用  
- 每个设备都有唯一的 Ed25519 密钥，必须经过 Gateway 的授权才能执行操作