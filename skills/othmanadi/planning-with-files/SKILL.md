---
name: planning-with-files
version: "2.10.0"
description: 实现了基于文件的规划方式，适用于复杂任务的管理。会生成 `task_plan.md`、`findings.md` 和 `progress.md` 三个文件。适用于启动需要多个步骤的复杂任务、研究项目，或任何涉及超过 5 个工具调用的任务。现在支持在执行 `/clear` 命令后自动恢复会话状态。
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
  - WebSearch
hooks:
  PreToolUse:
    - matcher: "Write|Edit|Bash|Read|Glob|Grep"
      hooks:
        - type: command
          command: "cat task_plan.md 2>/dev/null | head -30 || true"
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "echo '[planning-with-files] File updated. If this completes a phase, update task_plan.md status.'"
  Stop:
    - hooks:
        - type: command
          command: |
            SCRIPT_DIR="${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/plugins/planning-with-files}/scripts"

            IS_WINDOWS=0
            if [ "${OS-}" = "Windows_NT" ]; then
              IS_WINDOWS=1
            else
              UNAME_S="$(uname -s 2>/dev/null || echo '')"
              case "$UNAME_S" in
                CYGWIN*|MINGW*|MSYS*) IS_WINDOWS=1 ;;
              esac
            fi

            if [ "$IS_WINDOWS" -eq 1 ]; then
              if command -v pwsh >/dev/null 2>&1; then
                pwsh -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                powershell -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                sh "$SCRIPT_DIR/check-complete.sh"
              else
                powershell -ExecutionPolicy Bypass -File "$SCRIPT_DIR/check-complete.ps1" 2>/dev/null ||
                sh "$SCRIPT_DIR/check-complete.sh"
              fi
            else
              sh "$SCRIPT_DIR/check-complete.sh"
            fi
---

# 使用文件进行规划

像Manus一样工作：将持久的Markdown文件作为你的“磁盘上的工作记忆”。

## 首先：检查上一次会话的内容（v2.2.0）

**在开始工作之前**，请检查上一次会话中未同步的内容：

```bash
# Linux/macOS
$(command -v python3 || command -v python) ${CLAUDE_PLUGIN_ROOT}/scripts/session-catchup.py "$(pwd)"
```

```powershell
# Windows PowerShell
& (Get-Command python -ErrorAction SilentlyContinue).Source "$env:USERPROFILE\.claude\skills\planning-with-files\scripts\session-catchup.py" (Get-Location)
```

如果发现未同步的内容：
1. 运行`git diff --stat`以查看实际的代码更改
2. 阅读当前的规划文件
3. 根据未同步的内容和`git diff`的结果更新规划文件
4. 然后继续执行任务

## 重要提示：文件的位置

- **模板**位于 `${CLAUDE_PLUGIN_ROOT}/templates/`
- **你的规划文件**应保存在**你的项目目录**中

| 位置 | 存放内容 |
|----------|-----------------|
| Skill目录（`${CLAUDE_PLUGIN_ROOT}/`） | 模板、脚本、参考文档 |
| 你的项目目录 | `task_plan.md`、`findings.md`、`progress.md` |

## 快速入门

在开始任何复杂任务之前：

1. **创建`task_plan.md`** — 参考[templates/task_plan.md](templates/task_plan.md)
2. **创建`findings.md`** — 参考[templates/findings.md](templates/findings.md)
3. **创建`progress.md`** — 参考[templates/progress.md](templates/progress.md)
4. **在做出决策前重新阅读计划** — 使目标保持在你的关注范围内
5. **每个阶段完成后更新文件** — 标记任务状态为“进行中”或“已完成”，并记录遇到的错误

> **注意：** 规划文件应保存在项目根目录中，而不是技能安装文件夹中。

## 核心工作模式

```
Context Window = RAM (volatile, limited)
Filesystem = Disk (persistent, unlimited)

→ Anything important gets written to disk.
```

## 文件的用途

| 文件 | 用途 | 何时更新 |
|------|---------|----------------|
| `task_plan.md` | 任务阶段、进度、决策 | 每个阶段完成后 |
| `findings.md` | 研究结果、发现的内容 | 发现新内容后 |
| `progress.md` | 会话日志、测试结果 | 整个会话过程中 |

## 关键规则

### 1. 先制定计划
在没有`task_plan.md`的情况下，切勿开始复杂的任务。这是不可商量的。

### 2. 两步操作规则
> “每进行两次查看、浏览或搜索操作后，立即将关键发现内容保存到文本文件中。”

这可以防止视觉信息或多模态信息丢失。

### 3. 决策前先阅读
在做出重要决策之前，请先阅读计划文件。这样可以让你始终清楚自己的目标。

### 4. 行动后更新文件
完成某个阶段后：
- 将阶段状态从“进行中”更改为“已完成”
- 记录遇到的任何错误
- 记录创建或修改的文件

### 5. 记录所有错误
所有的错误都应记录在计划文件中。这有助于积累知识并避免重复犯错。

```markdown
## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| FileNotFoundError | 1 | Created default config |
| API timeout | 2 | Added retry logic |
```

### 6. 不要重复失败
```
if action_failed:
    next_action != same_action
```
记录你尝试过的方法，并调整策略。

## 三重检查错误处理机制

```
ATTEMPT 1: Diagnose & Fix
  → Read error carefully
  → Identify root cause
  → Apply targeted fix

ATTEMPT 2: Alternative Approach
  → Same error? Try different method
  → Different tool? Different library?
  → NEVER repeat exact same failing action

ATTEMPT 3: Broader Rethink
  → Question assumptions
  → Search for solutions
  → Consider updating the plan

AFTER 3 FAILURES: Escalate to User
  → Explain what you tried
  → Share the specific error
  → Ask for guidance
```

## 阅读与写入的决策矩阵

| 情况 | 应采取的行动 | 原因 |
|-----------|--------|--------|
| 刚刚写完文件 | 不要立即阅读 | 内容仍在上下文中 |
| 查看了图片/PDF | 立即将发现的内容写入文件 | 多模态信息可能会丢失 |
| 浏览器返回了数据 | 将数据写入文件 | 屏幕截图可能无法长期保存 |
| 开始新阶段 | 重新阅读计划和发现的内容 | 如果上下文已经过时，需要重新调整方向 |
| 发生错误 | 阅读相关的文件 | 需要了解当前的状态来解决问题 |
| 中断后恢复工作 | 阅读所有的规划文件 | 恢复工作状态 |

## 五个问题重启测试

如果你能够回答以下问题，说明你的上下文管理能力很扎实：

| 问题 | 答案来源 |
|----------|---------------|
| 我现在处于什么阶段？ | `task_plan.md`中的当前阶段 |
| 我的目标是什么？ | 计划中的目标陈述 |
| 我学到了什么？ | `findings.md`中的内容 |
| 我做了什么？ | `progress.md`中的记录 |

## 何时使用这种模式

**适用于：**
- 多步骤任务（3个以上步骤）
- 研究任务
- 构建/创建项目
- 需要使用多种工具的任务
- 需要组织信息的任务

**不适用的情况：**
- 简单的问题
- 单个文件的编辑
- 快速查找

## 模板

请复制以下模板以开始使用：

- [templates/task_plan.md](templates/task_plan.md) — 任务阶段跟踪
- [templates/findings.md](templates/findings.md) — 研究结果记录
- [templates/progress.md](templates/progress.md) — 会话日志

## 脚本

用于自动化的辅助脚本：

- `scripts/init-session.sh` — 初始化所有规划文件
- `scripts/check-complete.sh` — 验证所有阶段是否已完成
- `scripts/session-catchup.py` — 从上一次会话中恢复上下文（v2.2.0）

## 高级主题

- **Manus的原则：** 请参阅[reference.md]
- **实际示例：** 请参阅[examples.md]

## 应避免的做法

| 不要做 | 应该做 |
|-------|------------|
| 使用TodoWrite工具来保存数据 | 直接创建`task_plan.md`文件 |
| 只声明一次目标后就忽略它 | 在做出决策前重新阅读计划 |
| 隐藏错误并默默重试 | 将错误记录在计划文件中 |
| 将所有内容都放在同一个文件中 | 将大量内容分散存储在多个文件中 |
| 立即开始执行任务 | 先创建计划文件 |
| 重复失败的尝试 | 记录尝试过程并调整方法 |
| 在技能目录中创建文件 | 在你的项目目录中创建文件 |