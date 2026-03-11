---
name: copilot-cli-operator
description: 在目标项目目录中，通过 OpenClaw 运行 GitHub Copilot CLI 来执行编码任务。当用户要求 OpenClaw 使用 Copilot 进行实现、调试、重构、代码审查或脚本化编码工作时，可以使用此功能。
---
# GitHub Copilot CLI Operator

使用此技能可以通过 OpenClaw 来可靠地调用 Copilot CLI。

## 核心规则

1. 在执行第一个任务之前，先验证 Copilot CLI 是否存在（`copilot --version`）。
2. 始终通过 OpenClaw 的 `exec` 命令来运行 Copilot，并设置 `pty:true`。
3. 必须将 `workdir` 明确设置为目标仓库的路径。
4. 对于耗时较长的任务，使用 `background:true` 并通过 `process` 功能来跟踪任务进度。
5. 明确报告任务的各个阶段：开始、等待输入、完成或失败。

## 执行模式

### 一次性编码任务

使用以下命令：
- `exec_command`: `copilot -p "<task>" --allow-all-tools`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

### 有范围限制的工具使用

使用 `--allow-tool` 和 `--deny-tool` 来控制 Copilot 可以执行的操作：
- `exec_command`: `copilot -p "<task>" --allow-tool 'shell(git)' --allow-tool 'write'`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

### 阻止危险操作

使用以下命令来阻止可能造成数据丢失的操作：
- `copilot -p "<task>" --allow-all-tools --deny-tool 'shell(rm)' --deny-tool 'shell(git push)'`

### 交互式会话

使用以下命令：
- `exec_command`: `copilot`
- `exec.pty`: `true`
- `exec.workdir`: `<repo path>`

### 长时间运行的后台任务

1. 使用以下命令启动任务：`exec(background:true, pty:true, workdir, command:"copilot -p '...' --allow-all-tools")`
2. 记录返回的 `sessionId`。
3. 使用 `process action:poll` 来定期检查任务进度。
4. 使用 `process action:log` 来查看任务输出。
5. 如果 Copilot 需要用户输入，使用 `process action:submit` 来提交输入。

### 恢复之前的会话

使用以下命令：
- `exec_command`: `copilot --resume`（从会话列表中选择要恢复的会话）
- `exec_command`: `copilot --continue`（恢复最近的会话）

## 推荐的提示语

- “实现 <feature> 并编写测试代码，运行测试，然后总结所有被修改的文件。”
- “找出该仓库中导致持续集成（CI）失败的根本原因，并提出最小的修复方案。”
- “先查看当前分支的差异，列出高风险的问题。”
- “在新分支中处理问题 https://github.com/owner/repo/issues/123。”
- “创建一个 Pull Request（PR），更新 README 文件以包含最新的 API 使用说明。”

## 安全注意事项

- 除非日志显示任务已经完成，否则不要声称文件已被修改。
- 如果 Copilot 无法正常工作或认证失败，必须提供具体的修复步骤。
- 将 OpenClaw 的工具配置（`pty`, `workdir`, `background`）与 CLI 参数分开设置。
- 为了安全起见，建议使用 `--allow-tool` 来指定允许使用的工具范围，而不是 `--allow-all-tools`。
- 在处理包含重要数据的目录时，务必使用 `--deny-tool 'shell(rm)'` 来阻止删除文件的操作。

## 参考资料

- `references/copilot-doc-summary.md`
- `references/copilot-usage-recipes.md`
- `scripts/run-copilot-example.sh`