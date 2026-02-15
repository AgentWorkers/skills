---
name: ultra-agent-stinct
description: "内部调试与编程技能：当你在执行任务时遇到代码错误、构建失败、堆栈跟踪异常或程序出现意外行为时，该技能会自动激活。这是一种帮助你解决问题的本能反应，而非由用户主动触发的功能。如果某个命令执行失败、脚本抛出错误，或者系统在运行过程中出现故障，你可以利用这一技能自行进行调试和修复。"
version: 1.2.0
author: grimmjoww
homepage: https://github.com/grimmjoww/ultra-agent-stinct
metadata: {"openclaw": {"emoji": "\u26a1", "os": ["darwin", "linux", "win32"]}}
---

# Ultra Agent Stinct

这是你的内部调试工具。当你在工作时遇到问题时，就可以使用它来解决问题。

## 每次修改代码时都必须遵守这些规则

无论进行多么简单的修复，这些规则都必须严格遵守，没有任何例外。

### 安全性
1. **先阅读再编辑。** 在编辑之前，务必先阅读相关内容——必须精确匹配文本，否则操作会失败。
2. **修改会覆盖原有内容。** 使用“编辑”功能来修改现有文件。
3. **修改前请先询问。** 相比使用`rm -rf`，更安全的做法是先确认是否需要删除文件。
4. **推送代码前请先询问。** 只有在用户明确要求时，才能使用`git push`。
5. **提交代码前请先询问。** 只有在得到请求时，才能将代码添加到暂存区并提交。
6. **注意备份。** 在进行大规模代码重构之前，建议创建一个新的分支或使用暂存区来保存原始代码。

### 良好的编程习惯
7. **务必验证你的修复效果。** 每次修改后，重新运行出现问题的命令或测试用例。不要想当然地认为问题已经解决。
8. **告知用户问题所在以及你做了什么修改。** 修复问题后，简要说明问题是什么以及你做了哪些更改。
9. **先阅读错误信息。** 在修改代码之前，请先阅读实际的错误信息、堆栈跟踪或测试输出。
10. **尽量进行最小化的修改。** 仅修复具体的错误，不要对周围代码进行大规模重构。保持代码差异的简洁性和针对性。

## 何时启用完整的调试流程

如果在执行任务时遇到错误，可以先尝试快速修复，同时遵循上述规则。但如果遇到以下情况：
- **修复失败**：第一次的修复没有效果，或者仍然出现相同的错误或新的错误；
- **遇到复杂问题**：错误涉及多个文件、不熟悉的代码或存在架构上的问题；
- **需要系统化的解决方法**：不确定问题的根源或从哪里开始解决，

那么就需要**启用Ultra Agent Stinct**，并按照以下步骤逐步执行完整的调试流程。

---

## 调试流程

当你遇到错误或系统出现故障时，请按照以下步骤操作：

**1. 重现问题**：运行出错的命令：
```
exec command:"<failing command>" workdir:"<project dir>"
```

**2. 阅读错误信息**：分析堆栈跟踪，确定出错的文件和行号。

**3. 阅读相关代码**：阅读相关的文件：
```
read path:"<file from stack trace>"
```

**4. 查找问题原因**：追踪代码的执行流程，检查导入语句、依赖关系和配置文件。注意以下问题：
- 拼写错误、变量名错误
- 缺少导入或依赖项
- 类型不匹配、访问空值或未定义的变量
- 路径错误、环境变量缺失
- 条件判断中的逻辑错误

**5. 修复问题**：应用最简单的正确修复方法：
```
read path:"<file>"
edit path:"<file>" old:"<exact broken code>" new:"<fixed code>"
```

**6. 验证修复效果**：重新运行出错的命令，确认修复是否有效。

**7. 报告问题**：简要告知用户问题所在以及你修复了什么，然后继续执行原来的任务。

## 编写新代码

当需要创建或修改代码时，请按照以下步骤操作：

**1. 了解项目结构**：查看现有的代码模式：
```
exec command:"ls -la" workdir:"<project dir>"
```
阅读`package.json`、`pyproject.toml`、`Cargo.toml`等文件，遵循项目中的代码风格和规范。

**2. 先制定计划**：在编写代码之前，先规划好要创建的内容，思考好代码的结构、依赖关系和处理各种边缘情况。

**3. 编写代码**：创建新的文件：
```
write path:"<new file path>" content:"<complete file content>"
```

**4. 验证代码**：运行新代码，进行测试，确保其能够正常工作后再继续下一步。

## 运行测试

**1. 找到测试工具：**
- **Node.js**：`npm test` / `npx jest` / `npx vitest`
- **Python**：`pytest` / `python -m unittest`
- **Rust**：`cargo test`
- **Go**：`go test ./...`

**2. 运行测试**：
```
exec command:"<test command>" workdir:"<project>" timeout:120
```

**3. 如果测试失败**：阅读失败的测试用例，查看相关的源代码，并按照调试流程进行排查。

**4. 如果测试通过**：生成测试报告，然后继续执行后续任务。

## Git集成

只有在用户要求提交代码、将代码添加到暂存区或查看Git状态时，才进行相应的操作。
```
exec command:"git status" workdir:"<project>"
exec command:"git diff --stat" workdir:"<project>"
exec command:"git add <specific files>" workdir:"<project>"
exec command:"git commit -m '<message>'" workdir:"<project>"
```

有关详细的Git工作流程，请参考[references/git-workflow.md]。

## 启动后台调试代理（处理大型任务）

对于涉及多个文件的代码重构、完整功能的开发或耗时较长的构建任务，可以启动一个后台调试代理：
```
exec pty:true workdir:"<project>" background:true command:"claude '<detailed task>'"
```

监控代理的运行情况：
```
process action:list
process action:log sessionId:<id>
process action:poll sessionId:<id>
```

关于何时应该自行处理问题或寻求帮助，请参考[references/escalation-guide.md]。

## 跨平台操作快速参考

| 任务 | macOS/Linux | Windows (Git Bash) |
|------|-------------|-------------------|
| 查找文件 | `find . -name "*.ts" -not -path "*/node_modules/*"` | 同样适用 |
| 搜索代码 | `grep -rn "pattern" --include="*.ts" .` | 同样适用 |
| 查看进程列表 | `ps aux \| grep node` | `tasklist \| findstr node` |
| 结束进程 | `kill -9 <PID>` | `taskkill //f //pid <PID>` |
| 运行Python脚本 | `python3` (或 `python`) | `python` |
| 打开文件 | `open <file>` | `start <file>` |

## 上下文管理
- 每次操作应专注于一个具体的任务；
- 不要在系统命令行中同时显示系统中已存在的文件内容；
- 对于较大的文件，只读取需要查看的部分，而不是全部内容；
- 如果上下文信息过于复杂，在继续操作之前，请先总结关键信息。