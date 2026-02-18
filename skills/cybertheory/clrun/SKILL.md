---
name: clrun
description: 运行并控制交互式的命令行界面（CLI）会话。支持处理图形用户界面（TUI）中的提示（如选择列表、复选框、确认操作），以及维护 shell 的持久状态和长时间运行的进程。适用于需要执行终端命令、响应交互式提示、使用诸如 `create-vue` 或 `create-vite` 之类的开发工具来构建项目结构，或管理开发服务器的场景。
license: MIT
metadata:
  author: cybertheory
  version: "1.0.1"
compatibility: Requires Node.js >= 18 and clrun installed (npm install -g clrun or npx clrun).
---
# clrun — 用于 AI 代理的交互式命令行界面 (CLI)

每当您需要运行需要交互式输入、TUI 导航、长时间运行的进程或确定性执行控制的命令时，请使用 `clrun`。无需再使用 `--yes` 标志或命令重试功能。

## 何时使用 clrun

- **交互式工具**：`create-vue`、`create-vite`、`create-astro`、`npm init`
- **带有选择列表、复选框和确认对话框的 TUI 工具**
- **长时间运行的进程**：开发服务器、测试套件、Docker 构建
- **有状态的会话**：设置环境变量，然后稍后查询它们
- **任何需要用户输入的命令**

## 快速参考

| 动作 | 命令 |
|--------|---------|
| 运行命令 | `clrun <命令>` |
| 发送文本并按 Enter | `clrun <id> "文本"` |
| 发送按键输入 | `clrun <id> 键 <按键> 下方 键入` |
| 切换复选框 | `clrun <id> 键 <按键> 空格` |
| 接受默认值 | `clrun <id> 键 <按键> Enter` |
| 查看最新输出 | `clrun tail <id>` 或 `clrun <id>` |
| 检查所有会话 | `clrun status` |
| 结束会话 | `clrun kill <id>` |
| 中断（Ctrl+C） | `clrun <id> 键 <按键> Ctrl+C` |

## 两种输入模式

### 文本输入 (`clrun <id> "文本"`)

发送文本后按 Enter。适用于：
- 在提示框中输入文本（项目名称、描述等）
- 向正在运行的会话发送 Shell 命令
- 回答简单的“是/否”或 readline 风格的提示

```bash
clrun <id> "my-project-name"    # Type text and press Enter
clrun <id> ""                    # Just press Enter (accept default for readline)
```

### 键盘输入 (`clrun 键 <id> <按键...>`)

发送原始按键输入。适用于：
- 在选择列表中导航（`上`、`下`、`Enter`）
- 切换复选框（`空格`）
- 接受 TUI 的默认值（`Enter`）
- 切换“是/否”选项（`左`、`右`）
- 中断进程（`Ctrl+C`）

```bash
clrun key <id> down down enter           # Select 3rd item in a list
clrun key <id> space down space enter    # Toggle checkboxes 1 and 2, confirm
clrun key <id> enter                      # Accept default / confirm
```

**可用按键：**
`上`、`下`、`左`、`右`、`Enter`、`Tab`、`Esc`、`空格`、
`Backspace`、`Delete`、`Home`、`End`、`PageUp`、`PageDown`、
`Ctrl-C`、`Ctrl-D`、`Ctrl-Z`、`Ctrl-L`、`Ctrl-A`、`Ctrl-E`、`Y`、`N`

## 识别提示类型

当您查看会话输出时，可以识别提示的类型：

| 看到的内容 | 类型 | 动作 |
|---------|------|--------|
| `◆ 项目名称:` | 默认文本输入 | `clrun <id> "名称"` 或 `clrun 键 <id> Enter` |
| `● 选项1  ○ 选项2  ○ 选项3` | 单选 | `clrun 键 <id> 下方... Enter` |
| `◻ 选项1  ◻ 选项2  ◻ 选项3` | 多选 | `clrun 键 <id> 空格 下方... Enter` |
| `● 是 / ○ 否` | 确认 | `clrun 键 <id> Enter` 或 `clrun 键 <id> 右方 Enter` |
| `(y/n)`、`[Y/n]` | 简单确认 | `clrun <id> "y"` 或 `clrun <id> "n"` |
| `包名称: (默认)` | Readline 输入 | `clrun <id> "值"` 或 `clrun <id> ""` |

## 选择列表导航

默认情况下，**第一个选项**总是高亮的。每次按下 `Down` 键会向下移动一个位置。
要选择第 N 个选项：先按 `N-1` 次 `Down` 键，然后按 `Enter`。

```
◆  Select a framework:
│  ● Vanilla       ← position 1 (0 downs)
│  ○ Vue           ← position 2 (1 down)
│  ○ React         ← position 3 (2 downs)
│  ○ Svelte        ← position 4 (3 downs)
```

## 多选模式

从上到下依次按 `空格`（切换）和 `Down`（跳过）来选择选项，最后按 `Enter` 完成选择：

```bash
# Select TypeScript (1st), skip JSX (2nd), select Router (3rd), confirm:
clrun key <id> space down down space enter
```

## 会话生命周期

```
1. START    →  clrun <command>                    → get terminal_id
2. OBSERVE  →  clrun tail <id>                    → read output, identify prompt
3. INTERACT →  clrun <id> "text" / clrun key <id> → send input
4. REPEAT   →  go to 2 until done
5. VERIFY   →  clrun status                       → check exit codes
6. CLEANUP  →  clrun kill <id>                    → if needed
```

## 阅读响应

所有响应都是 YAML 格式。关键字段包括：
- **`terminal_id`** — 请保存此字段，因为它在所有操作中都必不可少
- **`output`** — 清理后的终端输出（去除了 ANSI 标记，过滤了提示信息）
- **`status`** — `运行中`、`暂停`、`退出`、`终止`、`分离`
- **`hints`** — 可以执行的下一步命令（可直接复制粘贴）
- **`warnings`** — 输入或输出中存在的问题
- **`restored`** — 如果会话是从暂停状态自动恢复的，则值为 `true`

## Shell 变量引用

使用 **单引号** 防止 Shell 变量被提前展开：

```bash
clrun <id> 'echo $MY_VAR'          # Correct — variable reaches the session
clrun <id> "echo $MY_VAR"          # Wrong — your shell expands it first
```

## 暂停的会话

如果会话在 5 分钟内没有活动，它会自动暂停。只需正常输入即可，系统会自动恢复会话，无需先检查状态。

## 重要规则

1. **解析 YAML** — 所有响应都是结构化的 YAML 格式
2. **阅读提示信息** — 它们会明确告诉您下一步该做什么
3. **使用 `key` 来处理 TUI 提示** — 绝不要将转义序列作为普通文本输入
4. **对于 readline 提示，使用文本输入** — `clrun <id> "文本"`
5. **使用单引号 `$` 来引用变量** — 防止 Shell 变量被提前展开
6. **对于 TUI 提示，使用 `key Enter` 来接受默认值** — 而不是输入空字符串
7. **对于选择列表，从顶部开始计数选项** — 要选择第 N 个选项，需按 `N-1` 次 `Down` 键

有关实际使用的示例，请参阅 [references/tui-patterns.md](references/tui-patterns.md)。