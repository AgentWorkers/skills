---
name: openai-codex-operator
description: 在目标项目目录中，通过 OpenClaw 运行 OpenAI Codex CLI 来执行编码任务。当用户要求 OpenClaw 使用 Codex 进行实现、调试、重构、代码审查或脚本化编码工作时，可以使用此方法。
---
# OpenAI Codex 操作符

使用此操作符可以可靠地通过 OpenClaw 调用 Codex CLI。

## 核心规则

1. 在执行第一个任务之前，先验证 Codex CLI 是否存在（使用 `codex --version` 命令）。
2. 始终通过 OpenClaw 的 `exec` 命令来运行 Codex，并设置 `pty:true` 以开启终端交互模式。
3. 必须明确指定 `workdir` 为目标代码仓库的路径。
4. 对于耗时较长的任务，应设置 `background:true` 并使用 `process` 命令来跟踪任务进度。
5. 明确记录任务的状态：开始、等待输入、完成或失败。

## 执行模式

### 一次性编码任务

使用以下命令：
- `exec.command`: `codex exec "<task>"`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

### 交互式会话

使用以下命令：
- `exec_command`: `codex`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

### 长期运行的后台任务

1. 使用以下命令启动任务：`exec/background:true, pty:true, workdir, command="codex exec ...")`
2. 记录返回的 `sessionId`。
3. 使用 `process action:poll` 命令来检查任务进度。
4. 使用 `process action:log` 命令来查看任务输出。
5. 如果 Codex 需要用户输入，使用 `process action:submit` 命令来提交输入。

## 推荐的命令提示

- “实现 <feature> 并编写测试用例，运行测试，然后总结所有被修改的文件。”
- “找出该代码仓库中 CI 测试失败的根本原因，并提出最小的修复方案。”
- “查看当前分支的差异，并优先处理高风险问题。”

## 安全注意事项

- 除非日志显示任务已完成，否则不要声称文件已被修改。
- 如果 `codex` 无法正常运行或认证失败，必须提供具体的解决方法。
- 将 OpenClaw 的配置参数（`pty`, `workdir`, `background`）与 CLI 的参数分开设置。

## 参考资料

- `references/codex-doc-summary.md`
- `references/codex-usage-recipes.md`
- `scripts/run-codex-example.sh`