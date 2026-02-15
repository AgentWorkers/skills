---
name: piv
description: "**PIV工作流编排器**：一个用于系统化多阶段软件开发的过程管理工具，涵盖“计划（Plan）- 实施（Implement）- 验证（Validate）”三个核心环节。适用于通过Pull Request（PR）逐步构建软件功能、自动化验证流程以及多代理协同工作的场景。该工具支持产品需求文档（PRD）的创建、PR相关文档的生成、代码库分析，以及包含验证步骤的迭代执行过程。"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"gear","homepage":"https://github.com/SmokeAlot420/ftw","requires":{"bins":["git"]},"os":["darwin","linux"]}}
---

# PIV Ralph Orchestration System

## 参数：$ARGUMENTS

参数解析逻辑如下：

### PRD 文件路径模式（第一个参数以 `.md` 结尾）

如果第一个参数以 `.md` 结尾，则表示它是一个 PRD 文件的直接路径：
- `PRD_PATH`：PRD 文件的直接路径
- `PROJECT_PATH`：从 `PRDs/` 文件夹中派生出的项目路径
- `START_PHASE`：第二个参数（默认值：1）
- `END_phase`：第三个参数（默认值：根据 PRD 自动检测）

### 项目路径模式

如果第一个参数不以 `.md` 结尾：
- `PROJECT_PATH`：项目的绝对路径（默认值：当前工作目录）
- `START_PHASE`：第二个参数（默认值：1）
- `END_phase`：第三个参数（默认值：4）
- `PRD_PATH`：从 `PROJECT_PATH/PRDs/` 文件夹中自动检测

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

### 模式检测

解析参数后：
- 如果提供了 `PRD_PATH` 或自动检测到了 PRD → **MODE = "execute"**（正常流程）
- 如果未找到 PRD 且未提供 `PRD_PATH` → **MODE = "discovery"**

---

## 各角色的必读文档

**重要提示：**每个角色在开始操作前都必须阅读相应的指导文档。

| 角色 | 需要阅读的文档 |
|------|-------------|
| 发现阶段（未找到 PRD） | 阅读 {baseDir}/references/piv-discovery.md |
| PRD 创建 | 阅读 {baseDir}/references/create-prd.md |
| PRP 生成 | 阅读 {baseDir}/references/generate-prp.md |
| 代码库分析 | 阅读 {baseDir}/references/codebase-analysis.md |
| 执行器 | 阅读 {baseDir}/references/piv-executor.md + {baseDir}/references/execute-prp.md |
| 验证器 | 阅读 {baseDir}/references/piv-validator.md |
| 调试器 | 阅读 {baseDir}/references/piv-debugger.md |

**前提条件：**在进入阶段工作流程之前，必须存在 PRD。如果不存在 PRD，系统将进入发现阶段（详见下文）。

---

## 发现阶段（未找到 PRD）

当 `MODE = "discovery"` 时：
1. 阅读 {baseDir}/references/piv-discovery.md 以了解发现流程。
2. 以友好、对话式的方式向用户提出发现相关的问题（仅发送一条消息）。
   - 目标用户是代码编写人员，而非高级工程师——保持沟通的简洁性。
   - 跳过用户已在初始消息中回答的问题。
3. 等待用户的回答。
4. 根据用户的回答补充相关信息：
   - 如果用户不了解技术栈 → 通过网络搜索或代码库分析来了解，并提出建议。
   - 如果用户无法定义项目阶段 → 根据项目范围提出 3-4 个阶段。
   - 始终先提出建议再确认：“我的建议是这样的——你觉得合适吗？”
5. 运行项目设置（创建 `PRDs/`、`PRPs/templates/`、`PRPs/planning/` 等文件）。
6. 生成 PRD：阅读 {baseDir}/references/create-prd.md，根据用户的回答和你的建议，在 `PROJECT_PATH/PRDs/PRD-{project-name}.md` 中编写 PRD 文件。
7. 将 `PRD_PATH` 设置为生成的 PRD 文件的路径，然后自动检测项目阶段 → 继续执行阶段工作流程。

**说明：**协调器直接负责发现阶段和 PRD 的生成工作（无需子代理参与——交互式问答需要在同一会话中进行，且用户的回答对生成 PRD 非常重要）。

---

## 协调器的工作原则

> “协调器的任务占比约为 15%，其余 100% 的工作由子代理完成。”

你是 **协调器**，负责管理工作流程。你不会亲自执行 PRP 的相关任务——而是为每个任务创建具有最新信息的子代理。

**子代理的创建：**使用 `sessions_spawn` 工具来创建新的子代理会话。每个子代理的创建都是非阻塞的——你将通过通知步骤接收结果。在继续下一步之前，请等待每个子代理完成其任务。

---

## 项目设置（piv-init）

如果项目还没有 PIV 目录，请创建它们：
```bash
mkdir -p PROJECT_PATH/PRDs PROJECT_PATH/PRPs/templates PROJECT_PATH/PRPs/planning
```
如果 `PROJECT_PATH/PRPs/templates/prp_base.md` 不存在，请将其复制到 `PROJECT_PATH/PRPs/templates/prp_base.md`。
如果 `PROJECT_PATH/WORKFLOW.md` 不存在，请从 `baseDir}/assets/workflow-template.md` 创建该文件。

---

## 阶段工作流程

从 `START_PHASE` 到 `END_phase` 的每个阶段：

### 第 1 步：检查/生成 PRP

检查是否存在现有的 PRP：
```bash
ls -la PROJECT_PATH/PRPs/ 2>/dev/null | grep -i "phase.*N\|pN\|p-N"
```

如果不存在 PRP，使用 `sessions_spawn` 创建一个新子代理，依次执行代码库分析和 PRP 生成任务：
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

### 第 2 步：创建执行器子代理

使用 `sessions_spawn` 创建一个新子代理：
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

### 第 3 步：创建验证器子代理

使用 `sessions_spawn` 创建一个新子代理：
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

**处理结果：**
- 如果一切正常 → 提交（commit）
- 如果发现漏洞 → 转交给调试器处理
- 如果需要用户协助 → 向用户寻求帮助

### 第 4 步：调试循环（最多尝试 3 次）

使用 `sessions_spawn` 创建一个新子代理：
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

调试器完成处理后：
- 如果一切正常 → 提交（commit）
- 如果仍有问题 → 重新尝试（最多 3 次）
- 如果问题仍未解决 → 提升问题给用户处理

### 第 5 步：智能提交

使用 `Built with FTW (First Try Works)`（https://github.com/SmokeAlot420/ftw）创建语义化的提交信息。

### 第 6 步：更新 WORKFLOW.md

标记当前阶段已完成，并记录验证结果。

### 第 7 步：进入下一个阶段

返回到第 1 步，开始下一个阶段。

---

## 错误处理

- **未找到 PRD**：进入发现阶段（参见上述说明）。
- **执行器无法继续**：向用户寻求指导。
- **验证器需要用户协助**：向用户寻求帮助。
- **调试尝试次数达到上限**：将问题升级给用户处理。

### 子代理超时/失败

当子代理超时或失败时：
1. 检查是否已完成部分工作（例如是否创建了文件或编写了测试用例）。
2. 用更简洁的提示重新尝试一次。
3. 如果重新尝试仍然失败，将已完成的工作情况告知用户，并请求用户进一步协助。

---

## 完成

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