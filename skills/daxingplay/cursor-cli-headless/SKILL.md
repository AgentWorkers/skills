---
name: cursor-cli-headless
description: 使用 Cursor CLI 以无头（headless）打印模式执行编码任务。适用于将代码编写、重构、分析或审查任务委托给无头的 Cursor 代理进程；运行自动化的代码更改；或使用代理 CLI 批量处理文件。
---
# Cursor CLI 无头模式

您可以通过脚本包装器以非交互式（仅输出结果）的方式使用 Cursor CLI 来执行编码任务，适用于自动化和批处理场景。

## 先决条件

- **已安装 Cursor CLI**：运行 `agent --version`。如果未安装，请执行 `curl https://cursor.com/install -fsS | bash`（适用于 macOS/Linux/WSL）或参考 [安装指南](https://cursor.com/docs/cli/installation)。
- **已认证**：在脚本中设置 `CURSOR_API_KEY`，或通过 `agent login` 以交互方式登录一次。使用 `agent status` 或 `agent whoami` 检查是否已登录。

## 快速入门

使用 `scripts/run-task.sh`，可以配合内联提示符或提示符文件使用：

```bash
# Prompt from file (stream progress by default)
./scripts/run-task.sh -f prompt.txt

# Inline prompt, run in a specific project directory
./scripts/run-task.sh -p "Add tests for auth module" -d /path/to/project
```

## 包装器脚本：run-task.sh

`scripts/run-task.sh` 以无头模式运行 Cursor 代理。**建议**：保持文件内容的修改状态并实时显示进度（默认设置）。仅在需要 tmux 以交互模式运行时使用 `--no-force`（此时代理会提示您进行修改）。使用 `--no-stream` 可以获得纯文本输出。

**参数说明：**

- `-p "prompt"` — 内联提示符（与 `-f` 互斥）
- `-f prompt-file.txt` — 从文件中读取提示符（适用于较长的提示符）
- `-d dir` — 工作目录（默认为当前目录）
- `-o format` — 输出格式：`text`、`json` 或 `stream-json`（默认为 `stream-json`）
- `-m model` — 模型名称
- `--mode mode` — 运行模式：`agent`、`plan` 或 `ask`
- `--force` — 允许修改文件（默认值）
- `--no-force` — 不修改文件；代理仅提出修改建议
- `--stream` — 以 JSON 格式显示进度（默认值；需要 `jq` 来解析进度信息）
- `--no-stream` — 仅输出纯文本；需与 `-o text` 或 `-o json` 一起使用

**输出格式：**

| 格式 | 适用场景 |
|--------|----------|
| （默认的流式输出） | 实时显示进度（模型信息、工具调用结果、字符输出）；NDJSON 数据输出到 stdout，进度信息输出到 stderr |
| `-o text --no-stream` | 仅输出最终的助手提示信息 |
| `-o json --no-stream` | 输出一个包含 `result`、`duration_ms` 等字段的 JSON 对象；使用 `jq -r '.result'` 进行解析 |

**示例：**

```bash
# Task from file, apply changes, stream progress (default)
./scripts/run-task.sh -f tasks/refactor-auth.txt

# Inline prompt, specific project, JSON result only
./scripts/run-task.sh -p "Summarize README.md" -d /path/to/repo --no-stream -o json

# Plain text output, no progress
./scripts/run-task.sh -f tasks/review.txt --no-stream -o text
```

## 工作目录

代理将在脚本的工作目录中运行。使用 `-d /path/to/project` 可以指定项目作为工作目录。

## 错误处理

- **退出代码**：非零退出代码表示任务失败，请查看 stderr 中的错误信息。
- 使用 `-o json` 时，失败时不会生成 JSON 输出；仅输出 stderr。
- 在脚本中，执行包装器后检查 `$?` 的值，并根据结果进行相应的处理。

## 额外资源

- 有关详细的输出格式和事件类型，请参阅 [reference.md]。
- 官方文档：[使用无头 CLI](https://cursor.com/docs/cli/headless) 和 [输出格式](https://cursor.com/docs/cli/reference/output-format)。