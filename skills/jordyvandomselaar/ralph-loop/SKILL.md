---
name: ralph-loop
description: 生成可复制的 Bash 脚本，用于实现 Ralph Wiggum 或 AI 代理的循环执行逻辑（适用于 Codex、Claude Code、OpenCode、Goose 等平台）。当需要使用 “Ralph 循环” 或 “Ralph Wiggum 循环” 时，这些脚本可以根据 PROMPT.md、AGENTS.md、SPECS 和 IMPLEMENTATION_PLAN.md 文件的内容来规划或构建代码。脚本应支持规划（PLANNING）与构建（BUILDING）两种模式，并具备回压（backpressure）控制、沙箱环境（sandboxing）以及完成条件（completion conditions）等功能。
---

# Ralph 循环（Ralph Loop）

## 概述  
生成一个可立即运行的 Bash 脚本，用于循环执行 AI 编程命令行界面（CLI）工具。该脚本遵循 Ralph 演练流程：  

1) **定义需求** → 任务待定（JTBD, “To-Be-Done”） → 相关主题 → `specs/*.md` 文件  
2) **规划阶段** → 创建/更新 `IMPLEMENTATION_PLAN.md` 文件（此时不进行实际开发）  
3) **执行阶段** → 实施任务、运行测试（使用“背压”机制）、更新计划并提交代码  

该循环通过 `PROMPT.md` 和 `AGENTS.md` 文件来保持上下文信息（每次迭代时都会加载这些文件），同时依赖磁盘上的计划和规范文件。  

## 工作流程  

### 1) 收集输入（如信息缺失则进行询问）  
- **目标/任务待定**（需要实现什么结果）  
- 可使用的 CLI 工具：`codex`、`claude-code`、`opencode`、`goose` 等  
- **模式**：`PLANNING`（规划阶段）、`BUILDING`（执行阶段）或 `BOTH`（同时进行规划与执行）  
- **完成条件**：  
  - 用于检测完成状态的字符串；  
  - 每次迭代需要执行的测试或命令；  
  - `IMPLEMENTATION PLAN.md` 文件中的完成标志（例如 `STATUS: COMPLETE`）；  
- 最大迭代次数；  
- 沙箱环境选择（`none`、`docker` 等）及相应的安全配置；  
- 需要嵌入到 `AGENTS.md` 中的测试/代码检查命令；  
- **自动批准选项**（需明确请求）：  
  - `Codex`：`--full-auto`  
  - `Claude Code`：`--dangerously-skip-permissions`  

### 2) 第一阶段 — 定义需求 → 编写规范文件  
如果用户希望使用完整的 Ralph 工作流程（或需求不明确），请执行以下操作：  
- 将任务待定内容分解为具体的主题（每个主题对应一个规范文件 `specs/<topic>.md`）；  
- 使用辅助工具（subagents）加载相关 URL 或现有文档，以提升规范文件的质量；  
- 保持规范文件的简洁性，并确保其可被有效测试。  

### 3) 第二/三阶段 — 加载 `PROMPT.md` 和 `AGENTS.md`  
- 每次迭代时都会加载 `PROMPT.md` 和 `AGENTS.md` 文件：  
- `AGENTS.md` 应包含：  
  - 项目测试命令；  
  - 构建/执行指令；  
  - 任何运营过程中的经验或反馈；  
- `PROMPT.md` 应引用：  
  - 所有的规范文件（`specs/*.md`）；  
  - `IMPLEMENTATION_PLAN.md`；  
  - 任何相关的项目文件或目录。  

### 4) 创建两种提示模板（用于规划与执行阶段）  
根据当前模式切换使用不同的提示模板：  
**规划阶段提示（不进行实际开发）：**  
```
You are running a Ralph PLANNING loop for: <JTBD/GOAL>.

Read specs/* and the current codebase. Do a gap analysis and update IMPLEMENTATION_PLAN.md only.
Rules:
- Do NOT implement.
- Do NOT commit.
- Prioritize tasks and keep plan concise.
- If requirements are unclear, write clarifying questions into the plan.

Completion:
If the plan is complete, add line: STATUS: COMPLETE
```  

**执行阶段提示：**  
```
You are running a Ralph BUILDING loop for: <JTBD/GOAL>.

Context:
- specs/*
- IMPLEMENTATION_PLAN.md
- AGENTS.md (tests/backpressure)

Tasks:
1) Pick the most important task from IMPLEMENTATION_PLAN.md.
2) Investigate relevant code (don’t assume missing).
3) Implement.
4) Run the backpressure commands from AGENTS.md.
5) Update IMPLEMENTATION_PLAN.md (mark done + notes).
6) Update AGENTS.md if you learned new operational details.
7) Commit with a clear message.

Completion:
If all tasks are done, add line: STATUS: COMPLETE
```  

### 5) 构建每次迭代的命令  
- 使用 `Codex`：`codex exec <FLAGS> "$(cat PROMPT.md)"`  
  - 需要 Git 仓库的支持；  
- 使用 `Claude Code`：`claude <FLAGS> "$(cat PROMPT.md)"`  
- 使用 `OpenCode`：`opencode run "$(cat PROMPT.md)"`  
- 使用 `Goose`：`goose run "$(cat PROMPT.md)"`（询问用户是否需要使用 Goose 工具）  

如果用户不知道具体的 CLI 命令，需在每次迭代时询问正确的命令。  

### 6) 生成可执行的脚本  
提供两种类型的脚本：  
- **最小化版本的循环脚本**；  
- **带有限制条件的循环脚本（推荐使用）**。  

**最小化版本的循环脚本（Geoff 风格）：**  
```bash
while :; do cat PROMPT.md | claude ; done
```  

**带有限制条件的循环脚本（推荐使用）：**  
```bash
#!/usr/bin/env bash
set -euo pipefail

PROMISE='...'
MAX_ITERS=...
CLI_FLAGS="..."  # optional
PLAN_SENTINEL='STATUS: COMPLETE'
TEST_CMD='...'   # optional

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ Run this inside a git repo."
  exit 1
fi

touch PROMPT.md AGENTS.md IMPLEMENTATION_PLAN.md
LOG_FILE=".ralph/ralph.log"
mkdir -p .ralph

CLI_CMD="..." # e.g. "codex exec" or "claude"

for i in $(seq 1 "$MAX_ITERS"); do
  echo -e "\n=== Ralph iteration $i/$MAX_ITERS ===" | tee -a "$LOG_FILE"

  $CLI_CMD $CLI_FLAGS "$(cat PROMPT.md)" | tee -a "$LOG_FILE"

  if [[ -n "${TEST_CMD}" ]]; then
    echo "Running tests: $TEST_CMD" | tee -a "$LOG_FILE"
    bash -lc "$TEST_CMD" | tee -a "$LOG_FILE"
  fi

  if grep -Fq "$PROMISE" "$LOG_FILE" || grep -Fq "$PLAN_SENTINEL" IMPLEMENTATION_PLAN.md; then
    echo "✅ Completion detected. Stopping." | tee -a "$LOG_FILE"
    exit 0
  fi

done

echo "❌ Max iterations reached without completion." | tee -a "$LOG_FILE"
exit 1
```  

## 安全与沙箱使用指南  
- 使用 `--dangerously-skip-permissions` 或 `--full-auto` 选项会带来信任风险；  
- 建议使用沙箱环境（如 Docker、e2b 或 Fly）以限制权限和网络访问；  
- 紧急退出方式：使用 `Ctrl+C` 停止执行；使用 `git reset --hard` 恢复到初始状态。  

## 规范与限制  
- 如果需求不明确，必须在执行构建步骤之前完成规范文件的编写；  
- 如果计划内容过时或错误，需重新进入规划阶段；  
- 如果缺少测试命令，请要求用户提供并添加到 `AGENTS.md` 中。