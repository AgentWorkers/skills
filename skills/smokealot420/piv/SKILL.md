---
name: piv
description: "**PIV工作流编排器**：一种用于系统化多阶段软件开发的“计划（Plan）- 实施（Implement）- 验证（Validate）”循环工具。适用于通过Pull Request（PR）逐步构建功能、自动化验证流程或多代理协同工作的场景。该工具支持产品需求文档（PRD）的创建、PR的生成、代码库分析以及包含验证环节的迭代执行过程。"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"gear","homepage":"https://github.com/SmokeAlot420/ftw","requires":{"bins":["git"]},"os":["darwin","linux"]}}
---

# PIV Ralph Orchestrator

## 参数：$ARGUMENTS

参数解析逻辑如下：

### PRD 路径模式（第一个参数以 `.md` 结尾）

如果第一个参数以 `.md` 结尾，则表示它是一个 PRD 文件的直接路径：
- `PRD_PATH`：PRD 文件的直接路径
- `PROJECT_PATH`：从 `PRDs/` 文件夹开始向上导航得到的项目路径
- `START_phase`：第二个参数（默认值：1）
- `END_phase`：第三个参数（默认值：根据 PRD 自动检测）

### 项目路径模式

如果第一个参数不以 `.md` 结尾：
- `PROJECT_PATH`：项目的绝对路径（默认值：当前工作目录）
- `START_phase`：第二个参数（默认值：1）
- `END_phase`：第三个参数（默认值：4）
- `PRD_PATH`：从 `PROJECT_PATH/PRDs/` 文件夹自动检测

### 检测逻辑
```
If $ARGUMENTS[0] ends with ".md":
  PRD_PATH = $ARGUMENTS[0]
  PROJECT_PATH = dirname(dirname(PRD_PATH))
  START_PHASE = $ARGUMENTS[1] or 1
  END_PHASE = $ARGUMENTS[2] or auto-detect from PRD
  PRD_NAME = basename without extension
Else:
  PROJECT_PATH = $ARGUMENTS[0] or current working directory
  START_PHASE = $ARGUMENTS[1] or 1
  END_PHASE = $ARGUMENTS[2] or 4
  PRD_PATH = auto-discover from PROJECT_PATH/PRDs/
  PRD_NAME = discovered PRD basename
```

---

## 各角色的必读文档

**重要提示：**每个角色在执行任务前必须阅读相应的操作指南文件。

| 角色 | 需要阅读的文档 |
|------|-------------|
| PRD 创建 | 阅读 {baseDir}/references/create-prd.md |
| PRP 生成 | 阅读 {baseDir}/references/generate-prp.md |
| 代码库分析 | 阅读 {baseDir}/references/codebase-analysis.md |
| 执行器 | 阅读 {baseDir}/references/piv-executor.md + {baseDir}/references/execute-prp.md |
| 验证器 | 阅读 {baseDir}/references/piv-validator.md |
| 调试器 | 阅读 {baseDir}/references/piv-debugger.md |

**前提条件：**必须存在 PRD 文件。如果找不到 PRD 文件，请提示用户先创建一个。

---

## Orchestrator 的工作原理

> “上下文预算分配：约 15% 用于 Orchestrator，95% 用于每个子代理的任务。”

您是 **Orchestrator**，负责协调整个工作流程。您不会直接执行 PRP 任务，而是为每个任务创建具有最新上下文的专用子代理。

**子代理的创建：**使用 `sessions_spawn` 工具来创建新的子代理会话。每个子代理的创建都是非阻塞的——您会通过 `announce` 步骤收到结果。在继续执行下一步之前，请等待所有子代理完成它们的任务。

---

## 项目设置（piv-init）

如果项目中没有 PIV 目录，请进行以下操作：
```bash
mkdir -p PROJECT_PATH/PRDs PROJECT_PATH/PRPs/templates PROJECT_PATH/PRPs/planning
```
- 如果 `PROJECT_PATH/PRPs/templates/prp_base.md` 不存在，请将其从 `{baseDir}/assets/prp_base.md` 复制到该目录。
- 如果 `PROJECT_PATH/WORKFLOW.md` 不存在，请使用 `{baseDir}/assets/workflow-template.md` 创建该文件。

---

## 各阶段的工作流程

从 `START_phase` 到 `END_phase`，每个阶段的工作流程如下：

### 第 1 步：检查/生成 PRP

检查是否存在 PRP 文件：
```bash
ls -la PROJECT_PATH/PRPs/ 2>/dev/null | grep -i "phase.*N\|pN\|p-N"
```

如果不存在 PRP 文件，使用 `sessions_spawn` 创建一个新的子代理，依次执行代码库分析和 PRP 生成任务：
```
RESEARCH & PRP GENERATION MISSION - Phase {N}
==============================================

Project root: {PROJECT_PATH}
PRD Path: {PRD_PATH}

## Phase {N} Scope (from PRD)
{paste phase scope}

## Step 1: Codebase Analysis
Read {baseDir}/references/codebase-analysis.md for the process.
Save to: {PROJECT_PATH}/PRPs/planning/{PRD_NAME}-phase-{N}-analysis.md

## Step 2: Generate PRP (analysis context still loaded)
Read {baseDir}/references/generate-prp.md for the process.
Use template: PRPs/templates/prp_base.md
Output to: {PROJECT_PATH}/PRPs/PRP-{PRD_NAME}-phase-{N}.md

Do BOTH steps yourself. DO NOT spawn sub-agents.
```

### 第 2 步：创建执行器（Executor）

使用 `sessions_spawn` 创建一个新的子代理：
```
EXECUTOR MISSION - Phase {N}
============================

Read {baseDir}/references/piv-executor.md for your role definition.
Read {baseDir}/references/execute-prp.md for the execution process.

PRP Path: {PRP_PATH}
Project: {PROJECT_PATH}

Follow: Load PRP → Plan Thoroughly → Execute → Validate → Verify
Output EXECUTION SUMMARY with Status, Files, Tests, Issues.
```

### 第 3 步：创建验证器（Validator）

使用 `sessions_spawn` 创建一个新的子代理：
```
VALIDATOR MISSION - Phase {N}
=============================

Read {baseDir}/references/piv-validator.md for your validation process.

PRP Path: {PRP_PATH}
Project: {PROJECT_PATH}
Executor Summary: {SUMMARY}

Verify ALL requirements independently.
Output VERIFICATION REPORT with Grade, Checks, Gaps.
```

**结果处理：**
- 如果验证通过（PASS），则提交代码；  
- 如果发现错误（GAPS_FOUND），则转交给调试器（debugger）；  
- 如果需要人工干预（HUMAN_NEEDED），则请求用户协助。

### 第 4 步：调试循环（最多尝试 3 次）

使用 `sessions_spawn` 创建一个新的子代理：
```
DEBUGGER MISSION - Phase {N} - Iteration {I}
============================================

Read {baseDir}/references/piv-debugger.md for your debugging methodology.

Project: {PROJECT_PATH}
PRP Path: {PRP_PATH}
Gaps: {GAPS}
Errors: {ERRORS}

Fix root causes, not symptoms. Run tests after each fix.
Output FIX REPORT with Status, Fixes Applied, Test Results.
```

在调试器完成处理后：
- 如果验证通过（PASS），则提交代码；  
- 如果仍然存在问题（循环最多 3 次），则请求用户进一步协助；  
- 如果问题仍然无法解决，则需要向上级报告。

### 第 5 步：智能提交（Smart Commit）

使用 `Built with FTW (First Try Works)` 提交代码：https://github.com/SmokeAlot420/ftw。

### 第 6 步：更新 WORKFLOW.md

标记当前阶段已完成，并记录验证结果。

### 第 7 步：进入下一个阶段

返回到第 1 步，开始下一个阶段的处理。

---

## 错误处理

- **没有 PRD 文件**：提示用户先创建一个 PRD 文件。
- **执行器执行失败**：请求用户提供帮助。
- **验证器需要人工干预**：请求用户提供帮助。
- **调试循环尝试 3 次仍未解决问题**：向上级报告。

### 子代理超时/失败

当子代理超时或失败时：
1. 检查子代理是否完成了部分工作（例如是否生成了文件、编写了测试用例）。
2. 使用简化后的提示重新尝试一次。
3. 如果重试仍然失败，将已完成的操作情况上报给用户。

---

## 任务完成

```
## PIV RALPH COMPLETE

Phases Completed: START to END
Total Commits: N
Validation Cycles: M

### Phase Summary:
- Phase 1: [feature] - validated in N cycles
...

All phases successfully implemented and validated.
```