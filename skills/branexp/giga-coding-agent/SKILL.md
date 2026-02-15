---
name: giga-coding-agent
description: 通过后台进程运行 Codex CLI、Claude Code、OpenCode 或 Pi Coding Agent，以实现程序化的控制。
metadata: {"clawdbot":{"emoji":"🧩","requires":{"anyBins":["claude","codex","opencode","pi"]}}}
---

# 编码代理（优先使用后台模式）

对于非交互式的编码任务，请使用 **bash 背景模式**。对于交互式的编码会话，请始终使用 **tmux** 工具（除非是简单的、一次性完成的命令）。

## 模式：工作目录 + 背景模式

**为什么工作目录很重要？** 编码代理会在一个特定的工作目录中启动，不会去浏览无关的文件（比如你的 `soul.md` 文件 😅）。

---

## Codex CLI

默认使用的模型是 `gpt-5.2-codex`（配置在 `~/.codex/config.toml` 中）。

### 构建/创建项目（使用 `--full-auto` 或 `--yolo` 参数）

### 查看 Pull Request（基础用法，无需任何特殊参数）

**⚠️ 重要提示：** **绝对不要在 Clawdbot 的项目文件夹内查看 Pull Request！**  
- 请在 Pull Request 被提交的项目目录中查看（如果该项目不在 `~/Projects/clawdbot` 目录下）；  
- 或者先将其克隆到一个临时文件夹中再查看。

**为什么这样操作？** 在正在运行的 Clawdbot 仓库中切换分支可能会导致系统崩溃！

### 批量查看 Pull Request（并行处理）

### 查看 Pull Request 的建议：
- **先获取引用信息：** `git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'`  
- **使用 `git diff` 命令：** 告诉 Codex 使用 `git diff origin/main...origin/pr/XX` 来比较代码差异  
- **不要直接切换分支：** 并行查看多个 Pull Request 可能会导致分支冲突  
- **发布审查结果：** 使用 `gh pr comment` 将审查结果发布到 GitHub 上

---

## Claude Code

---

## OpenCode

---

## Pi 编码代理

---

## Pi 命令行参数（常用参数）

- `--print` / `-p`：非交互式模式；运行命令后直接退出。  
- `--provider <名称>`：选择代码生成服务提供商（默认为 google）。  
- `--model <ID>`：选择代码生成模型（默认为 gemini-2.5-flash）。  
- `--api-key <密钥>`：覆盖 API 密钥（默认使用环境变量中的密钥）。  

示例：

---

## tmux（交互式会话）

对于交互式的编码会话，请始终使用 tmux 工具（除非是简单的、一次性完成的命令）。对于非交互式的任务，建议使用 bash 背景模式。

---

## 使用 git worktrees 和 tmux 并行修复多个问题

要并行修复多个问题，可以使用 git worktrees（创建隔离的分支）和 tmux 会话：

**为什么使用 worktrees？** 每个代码生成任务都在独立的分支中运行，不会产生冲突，可以同时进行多个修复操作！  
**为什么选择 tmux 而不是 bash 背景模式？** 因为 Codex 是交互式工具，需要 TTY（终端）来正确显示输出；tmux 可以保持会话的持久性，并记录完整的操作历史。

---

## ⚠️ 规则：
1. **尊重用户的选择** — 如果用户请求使用 Codex，就使用 Codex；**绝对不要自己尝试构建它！**  
2. **要有耐心** — 即使会话运行缓慢，也不要强制终止它们。  
3. **使用 `process:log` 监控进程进度** — 在不干扰会话运行的情况下查看进度。  
4. **使用 `--full-auto` 参数进行构建** — 代码生成工具会自动批准修改。  
5. **查看 Pull Request 时使用基础参数** — 不需要任何特殊参数。  
6. **并行操作是允许的** — 可以同时运行多个 Codex 进程以进行批量处理。  
7. **绝对不要在 `~/clawd/** 目录下启动 Codex** — 那里存放的是 Clawdbot 的运行实例文件，可能会影响其正常运行；请在目标项目目录或 `/tmp` 目录下使用 Codex。  
8. **绝对不要在 `~/Projects/clawdbot/** 目录下切换分支** — 那里是 Clawdbot 的运行环境！请将项目克隆到 `/tmp` 或使用 git worktree 进行 Pull Request 的查看和修改。  

---

## Pull Request 模板（推荐格式）

在向外部仓库提交 Pull Request 时，请使用以下格式，以确保代码质量和便于维护者阅读：

```
```markdown
## Original Prompt
[Exact request/problem statement]

## What this does
[High-level description]

**Features:**
- [Key feature 1]
- [Key feature 2]

**Example usage:**
```bash
# 示例
command example
```

## Feature intent (maintainer-friendly)
[Why useful, how it fits, workflows it enables]

## Prompt history (timestamped)
- YYYY-MM-DD HH:MM UTC: [Step 1]
- YYYY-MM-DD HH:MM UTC: [Step 2]

## How I tested
**Manual verification:**
1. [Test step] - Output: `[result]`
2. [Test step] - Result: [result]

**Files tested:**
- [Detail]
- [Edge cases]

## Session logs (implementation)
- [What was researched]
- [What was discovered]
- [Time spent]

## Implementation details
**New files:**
- `path/file.ts` - [description]

**Modified files:**
- `path/file.ts` - [change]

**Technical notes:**
- [Detail 1]
- [Detail 2]

---
*Submitted by Razor 🥷 - Mariano's AI agent*
```
```

**关键原则：**
1. 由人类编写的描述（避免使用 AI 生成的文本）。  
2. 为维护者提供关于功能用途的清晰说明。  
3. 提供带有时间戳的命令执行历史记录。  
4. 如果使用了 Codex 或其他代码生成工具，记录会话日志。  

**示例：** https://github.com/steipete/bird/pull/22