---
name: preqstation
description: "将 PREQSTATION 的编码任务委托给 Claude Code、Codex CLI 或 Gemini CLI，并确保这些工具能够以 PTY-safe 的方式执行任务（包括设置工作目录、在后台运行以及提供监控功能）。这些工具适用于在映射的工作空间中进行代码构建、重构或审查操作。**不适用于单行编辑或仅用于读取代码的检查**。"
metadata: {"openclaw":{"requires":{"anyBins":["claude","codex","gemini"]}}}
---
# preqstation

此技能用于处理与PREQSTATION相关的工作，通过本地的CLI引擎执行自然语言请求。

## 触发条件

当消息中包含以下内容时，优先触发此技能：
- `/skill preqstation`
- `preqstation`
- `preq`

**禁止使用此技能的情况：**
- 可以直接处理的简单单行手动编辑
- 仅用于读取或解释文件，不涉及执行操作
- 在`~/clawd/`或`~/.openclaw/`目录内启动任何编码代理

## 快速触发示例：
- `/skill preqstation: implement the PROJ-1`
- `preqstation: plan PROJ-76 using Claude Code`
- `preq: implement PROJ-1`

## 严格规则：
1. 始终以`pty:true`模式运行编码代理。
2. 尊重用户选择的引擎；如果没有指定，默认使用`claude`。
3. 除非会卡顿，否则不要直接终止会话；先进行轮询或记录日志。
4. 绝不在`~/clawd/`或`~/.openclaw/`目录内启动编码代理。
5. 将解析出的项目路径视为主要检出的源代码；在启动任何编码代理之前，先创建一个git工作区。
6. 绝不在主要检出路径中运行编码代理命令。
7. PR审查必须在临时克隆或git工作区中执行，切勿在主要的检出路径中执行。
8. 确保执行操作仅限于解析出的工作区`<cwd>`。
9. 工作区分支名称必须包含解析出的项目键。
10. 编码代理默认以`background:true`模式运行；只有在用户明确要求阻塞/同步执行时才使用前台模式。

## 运行时前提条件（必需）：
- 必须安装`git`，并且它必须在`PATH`环境中可用。
- 至少安装一个引擎二进制文件：`claude`、`codex`或`gemini`。
- 此技能使用的环境变量：
  - `OPENCLAW_WORKTREE_ROOT`（可选，默认为`/tmp/openclaw-worktrees`）
- 此技能会读取并更新`MEMORY.md`中的项目映射信息（使用绝对路径）。

## 执行安全检查（必需）：
在运行任何引擎命令之前：
- 执行预检：
  - `command -v git`
  - `command -v <engine>`
只有当执行目录`cwd`是为此任务解析出的git工作区路径时，才能继续执行。
- 绝不在主要检出路径或`~/clawd/`/`~/.openclaw/`目录内运行引擎命令。
- 仅在针对本地可信CLI的真正编码执行时使用`dangerously-*`或`sandbox-disable`标志。
- 对于规划或仅用于读取的请求，不要启动引擎命令。

## 输入解析：
从用户消息中解析以下信息：
- **引擎**：
  - 如果明确提供：`claude`、`codex`或`gemini`
  - 默认：`claude`
- **任务**：
  - 首个匹配的令牌格式为`<KEY>-<number>`（例如：`PRJ-284`）
  - 可选
- **分支名称**（可选）：
  - 匹配的令牌格式为：
    - `branch_name=<value>`
    - `branch_name: <value>`
    - `branch=<value>`
  - 去除`<value>`周围的引号
  - 将名称转换为小写，并用`-`替换空格
  - 如果分支名称不包含解析出的`project_key`，则在前面加上`preqstation/<project_key>/`
- **项目工作目录`（执行前必需）**：
  - 如果提供了绝对路径，则使用该路径
  - 否则，根据`MEMORY.md`中的`project`键进行解析
  - 如果任务前缀键与`MEMORY.md`中的项目键匹配，则使用该路径
  - 如果未解析出项目键/名称，请询问用户并提供项目键/路径，更新`MEMORY.md`后继续执行
  - 如果`MEMORY.md`中不存在确切的项目键，在执行前必须询问用户
- **目标**：
  - 使用用户请求作为执行目标
- **执行目录`（必需）**：
  - 默认值：根据`project_cwd`派生的每个任务的工作区路径
  - 在启动引擎命令之前创建工作区
  - 如果`project_cwd`不是git检出目录，请在执行前询问用户的工作区路径
- **进度模式**（用于状态更新）：
  - 如果用户明确指定`live`、`realtime`、`frequent`、`detailed`，则使用`live`模式
  - 如果用户指定`sparse`、`concise`、`summary-only`、`key events only`，则使用`sparse`模式
  - 如果用户指令不明确或存在冲突，仅询问一次
- **上下文压缩**：
  - 默认情况下，保持当前会话/对话的紧凑性，而不是启动新的会话
  - 避免重复显示完整日志；发送简短的检查点摘要并从中继续
  - 仅在用户明确请求或平台限制不允许继续当前会话时，才启动新的会话

## `MEMORY.md`解析：
- 从仓库根目录读取`MEMORY.md`文件。
- 使用`Projects`表（`key | cwd | note`）。
- 仅通过确切的项目键进行匹配（不区分大小写，不支持模糊/部分匹配）。
- 如果缺少确切的项目键，在继续之前询问用户正确的键/路径。
- 如果用户请求添加/更新项目路径映射，请先更新`MEMORY.md`，然后确认。
- 如果任务ID存在，将前缀视为候选项目键（例如：`PROS-102` -> `pros`）。

## `MEMORY.md`更新规则：
- 仅将映射信息保存在`Projects`表中。
- 使用以下格式添加或更新条目：`| <key> | <absolute-path> | <note> |`。
- 每个键对应一行。如果键已存在，则替换该行。
- 始终存储绝对路径（不使用相对路径）。
- 在写入之前将键转换为小写和kebab-case格式。
- 如果用户提供了项目名称，将其存储在`note`字段中；否则使用`workspace`。

## 缺少项目映射的处理流程（必需）：
当无法解析`project_cwd`或`MEMORY.md`中缺少确切的项目键时：
- 向用户询问以下信息：
  - 项目键（或根据任务前缀推断的键）
  - 绝对的工作区路径
  - 可选的项目名称（用于备注）
- 验证路径是否为绝对路径。
- 立即更新或插入`MEMORY.md`中的条目。
- 用一条简短的消息确认映射。
- 使用新解析出的`project_cwd`继续执行原始任务，然后创建任务工作区`cwd`并执行。

## 分支命名规则（基于项目键）：
使用以下优先级确定分支名称：
1. 从用户消息中解析出的`branch_name`
2. 备用方案：`preqstation/<project_key>`

规则：
- `<project_key>`必须是`MEMORY.md`中解析出的项目键。
- 将名称转换为小写和kebab-case格式。
- 分支名称必须包含解析出的`project_key`；如果缺失，则在前面加上`preqstation/<project_key>/`。
- 拒绝不安全的名称（如`..`、以`/`开头或为空的名称），并请求用户提供有效的分支名称。

## 工作区优先的执行方式（默认要求）：
在解析出`project_cwd`和`project_key`后，准备执行环境：
- 使用此技能的规则构建分支名称：
  - `<branch_name>`
- 构建每个任务的工作区路径：
  - 默认根目录：`${OPENCLAW_WORKTREE_ROOT:-/tmp/openclaw-worktrees>`
  - 目录：`<worktree_root>/<project_key>/<branch_slug>`
  - `branch_slug` = `<branch_name>`，其中`/`替换为`-`
- 在启动引擎之前，从`project_cwd`创建工作区：
  - 新分支：`git -C <project_cwd> worktree add -b <branch_name> <cwd> HEAD`
  - 已存在的分支：`git -C <project_cwd> worktree add <cwd> <branch_name>`
- 使用此工作区路径作为提示显示和引擎执行的`<cwd>`。

## 提示显示（必需的模板）：
不要直接显示用户的原始文本。使用以下模板进行显示：
在提示中，`<cwd>`必须是任务的工作区路径（而不是主要检出路径）。

```text
Task ID: <task or N/A>
Project Key: <project key or N/A>
Branch Name: <branch_name or N/A>
User Objective: <objective>
Execution Requirements:
1) Work only inside <cwd>.
2) Complete the requested work.
3) Use branch <branch_name> for commits/pushes when provided.
4) After completion, return a short completion summary.
```

## 引擎命令（保留当前策略）：
所有引擎命令都必须通过bash以`PTY`模式和明确的`workdir`参数来执行。

**保留`dangerously-*`标志的原因：**
- 此技能针对非交互式的`PTY`/后台执行。
- 权限提示可能会阻止无人值守的运行；这些标志可以避免这种阻塞行为。
- 只有在通过上述安全检查后，且仅在解析出的任务工作区内，才能使用这些标志。
- 如果您的环境不允许使用这些标志，请立即失败，并给出简短的原因。

### Claude Code
```bash
bash pty:true workdir:<cwd> command:"claude --dangerously-skip-permissions '<rendered_prompt>'"
```

### Codex CLI
```bash
bash pty:true workdir:<cwd> command:"codex exec --dangerously-bypass-approvals-and-sandbox '<rendered_prompt>'"
```

### Gemini CLI
```bash
bash pty:true workdir:<cwd> command:"GEMINI_SANDBOX=false gemini -p '<rendered_prompt>'"
```

## Bash执行接口（必需）：
默认使用带有`PTY`模式和后台模式的bash。

### Bash参数：
| 参数 | 类型 | 是否必需 | 用途 |
| ---- | ---- | -------- | -------- |
| `command` | 字符串 | 是 | 要运行的引擎命令 |
| `pty` | 布尔值 | 是 | 对于编码代理CLI，必须设置为`true` |
| `workdir` | 字符串 | 是 | 每个任务的工作区`<cwd>` |
| `background` | 布尔值 | 否 | 异步运行并返回会话ID（此技能默认设置为`true`） |
| `timeout` | 数字 | 否 | 硬性超时时间（以秒为单位） |
| `elevated` | 布尔值 | 否 | 如果策略允许，允许在主机上执行 |

## 背景会话的处理动作：
使用以下动作作为标准控制：
- `list`：列出会话
- `poll`：检查运行/完成状态
- `log`：读取增量输出
- `write`：发送原始标准输入
- `submit`：发送标准输入加上换行符
- `kill`：仅在必要时终止会话

## 执行模式（工作区 + 背景 + PTY）：
### 一次性示例：
创建一个任务工作区，然后在该工作区内运行（默认为后台模式）：
```bash
git -C <project_cwd> worktree add -b <branch_name> /tmp/openclaw-worktrees/<project_key>/<branch_slug> HEAD
bash pty:true workdir:/tmp/openclaw-worktrees/<project_key>/<branch_slug> background:true command:"codex exec --dangerously-bypass-approvals-and-sandbox '<rendered_prompt>'"
```

**模式说明：**工作区 + 背景 + PTY
对于较长的任务，使用带有`PTY`模式的后台执行：
```
# Start agent in task worktree (with PTY!)
bash pty:true workdir:<cwd> background:true command:"codex exec --full-auto 'Build a snake game'"
# Returns sessionId for tracking

# Monitor progress
process action:log sessionId:XXX

# Check if done
process action:poll sessionId:XXX

# Send input (if agent asks a question)
process action:write sessionId:XXX data:"y"

# Submit with Enter (like typing "yes" and pressing Enter)
process action:submit sessionId:XXX data:"yes"

# Kill if needed
process action:kill sessionId:XXX
```

**工作区的重要性：**代理会在指定的目录中运行，不会读取无关文件（例如`your灵魂.md`文件）。

## 如果运行过程中需要用户输入：
```bash
process action:write sessionId:<id> data:"y"
process action:submit sessionId:<id> data:"yes"
```

## PR审查的安全模式（仅限临时目录/工作区）：
绝不在实时的OpenClaw文件夹中运行PR审查。
```bash
# default: git worktree review (resolved branch naming)
git worktree add -b <branch_name> /tmp/<project_key>-review <base_branch>
bash pty:true workdir:/tmp/<project_key>-review command:"codex review --base <base_branch>"

# fallback: temp clone review (only when local checkout is unavailable)
REVIEW_DIR=$(mktemp -d)
git clone <repo> "$REVIEW_DIR"
cd "$REVIEW_DIR" && gh pr checkout <pr_number>
bash pty:true workdir:"$REVIEW_DIR" command:"codex review --base origin/main"
```

## 问题工作区模式：
```bash
git worktree add -b <branch_name> /tmp/<project_key> main

bash pty:true workdir:/tmp/<project_key> background:true command:"codex exec --dangerously-bypass-approvals-and-sandbox 'Fix issue #101. Commit after validation.'"
bash pty:true workdir:/tmp/<project_key> background:true command:"codex exec --dangerously-bypass-approvals-and-sandbox 'Fix issue #102. Commit after validation.'"

process action:list
process action:log sessionId:<id>
```

## 进度更新（关键点）：
对于后台运行，选择以下两种模式之一：
- **sparse**（默认）：仅在状态发生变化时进行低频率更新
- **live**：在运行过程中进行更频繁的更新
- **sparse**模式的主要目的是减少令牌使用量和消息成本，同时保持关键信息的可见性。

**用户如何通过消息请求模式：**
- `... progress live`
- `... live updates`
- `... progress sparse`
- `... sparse updates`

在后台启动编码代理时，根据用户选择的模式保持用户的知情状态：
- 在`sparse`模式下：
  - 启动时发送一条简短的消息（正在运行的任务和位置）。
  - 仅在以下情况下再次更新：
    - 里程碑完成（构建完成、测试通过）
    - 代理需要用户输入
    - 发生错误或需要用户操作
    - 代理完成（包括更改的内容和位置）
- 在`live`模式下：
  - 发送与`sparse`模式相同的状态更新。
  - 在运行过程中定期发送简短的状态更新（例如，每1-2分钟一次），包括最新的活动步骤。
- 如果终止会话，立即告知用户原因。

**长时间运行的上下文压缩：**
在长时间运行的任务中，保持上下文的紧凑性：
- 除非用户明确要求`live`模式，否则优先使用`sparse`模式。
- 在里程碑处发送简短的检查点摘要；避免重复显示之前的日志。
- 仅包括：当前状态、更改的内容、下一步操作、障碍（如果有）。
- 如果线程变得过大或过于复杂，发送一次压缩摘要，然后继续在同一会话中。

**自动完成通知：**
对于长时间运行的任务，在显示的提示中添加完成通知：
```text
When completely finished, run this command:
openclaw system event --text "Done: <brief summary>" --mode now
```

**示例：**
```bash
bash pty:true workdir:<cwd> background:true command:"codex exec --dangerously-bypass-approvals-and-sandbox '<rendered_prompt>

When completely finished, run:
openclaw system event --text \"Done: implemented requested PREQSTATION task\" --mode now'"
```

**输出策略：**
仅返回简短的完成摘要。
成功格式：
`completed: <task or N/A> via <engine> at <cwd>`

失败格式：
`failed: <task or N/A> via <engine> at <cwd or N/A> - <简短原因>`

除非用户明确要求，否则不要显示原始的stdout/stderr输出。