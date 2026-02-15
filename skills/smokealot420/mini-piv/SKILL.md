---
name: mini-piv
description: "轻量级 PIV 工作流程——基于发现驱动的功能构建工具。无需编写产品需求文档（PRD）。用户可以快速提出问题，系统会自动生成项目请求（PRP），并执行相应的功能开发流程，同时包含验证环节。适用于开发小型到中型功能时，当您希望跳过传统的产品需求文档编写流程时。"
user-invocable: true
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"zap","homepage":"https://github.com/SmokeAlot420/ftw","requires":{"bins":["git"]},"os":["darwin","linux"]}}
---

# Mini PIV Ralph - 轻量级特性构建工具

## 参数：$ARGUMENTS
解析参数：
```
FEATURE_NAME = $ARGUMENTS[0] or null (will ask user during discovery)
PROJECT_PATH = $ARGUMENTS[1] or current working directory
```

---

## 设计理念：快速且高质量
> “当你只是想快速构建某个功能，而不想先编写产品需求文档（PRD）时，Mini PIV Ralph就是你的最佳选择。”

使用与常规流程相同的质量控制流程（执行 → 验证 → 调试），但整个过程从简短的沟通开始，而非编写PRD。

**你是整个流程的协调者**——保持流程的简洁性，为需要处理复杂任务的子代理分配相应的任务。

**子代理的创建**：使用`sessions_spawn`工具来创建新的子代理会话。每个子代理的创建都是非阻塞的，你可以通过通知机制获取其执行结果。在进入下一步之前，请务必等待所有子代理完成它们的工作。

---

## 各角色所需阅读的文档
| 角色 | 需要阅读的文档 |
|------|-------------|
| 协调者 | 仅阅读本文件 |
| 研究代理 | {baseDir}/references/codebase-analysis.md + {baseDir}/references/generate-prp.md |
| 执行代理 | {baseDir}/references/piv-executor.md + {baseDir}/references/execute-prp.md |
| 验证代理 | {baseDir}/references/piv-validator.md |
| 调试代理 | {baseDir}/references/piv-debugger.md |

---

## 可视化工作流程
```
┌──────────────────────────────────────────────────────────┐
│ 1. DISCOVERY → Ask 3-5 questions                          │
│ 2. RESEARCH & PRP → Codebase analysis + PRP generation    │
│ 3. EXECUTE → Implement PRP                                │
│ 4. VALIDATE → PASS / GAPS_FOUND / HUMAN_NEEDED            │
│ 5. DEBUG LOOP → Fix gaps (max 3x)                         │
│ 6. COMMIT → feat(mini): {description}                     │
└──────────────────────────────────────────────────────────┘
```

---

## 第1步：发现阶段
### 1a. 确定特性名称
- 如果名称未提供：询问用户或根据上下文推断；
- 将名称转换为驼峰式命名法（kebab-case）。

### 1b. 检查是否存在现有的产品需求文档（PRP）
```bash
ls -la PROJECT_PATH/PRPs/ 2>/dev/null | grep -i "mini-{FEATURE_NAME}"
```

如果存在PRP，请询问用户：“是直接覆盖现有文档、重命名该特性，还是跳过此步骤直接进入执行阶段？”

### 1c. 提出相关问题
以对话的形式向用户提出以下问题：
```
I've got a few quick questions so I can build this right:

1. **What does this feature do?** Quick rundown.
2. **Where in the codebase does it live?** Files, folders, components?
3. **Any specific libraries, patterns, or existing code to follow?**
4. **What does "done" look like?** 1-3 concrete success criteria.
5. **Anything explicitly OUT of scope?**
```

根据特性的类型（UI、API、合同、集成等）调整问题内容。

### 1d. 整理用户的回答
```yaml
feature:
  name: {FEATURE_NAME}
  scope: {Q1}
  touchpoints: {Q2}
  dependencies: {Q3}
  success_criteria: {Q4}
  out_of_scope: {Q5}
```

---

## 第2步：研究及生成产品需求文档（PRP）
使用`sessions_spawn`创建一个新的子代理来执行特性相关的研究工作：
```
MINI PIV: RESEARCH & PRP GENERATION
====================================

Project root: {PROJECT_PATH}
Feature name: {FEATURE_NAME}

## Discovery Input
{paste structured YAML}

## Step 1: Codebase Analysis
Read {baseDir}/references/codebase-analysis.md for the process.
Save to: {PROJECT_PATH}/PRPs/planning/mini-{FEATURE_NAME}-analysis.md

## Step 2: Generate PRP (analysis context still loaded)
Read {baseDir}/references/generate-prp.md for the process.

### Discovery → PRP Translation
| Discovery | PRP Section |
|-----------|-------------|
| Scope (Q1) | Goal + What |
| Touchpoints (Q2) | Implementation task locations |
| Dependencies (Q3) | Context YAML, Known Gotchas |
| Success Criteria (Q4) | Success Criteria + Validation |
| Out of Scope (Q5) | Exclusions in What section |

Use template: PRPs/templates/prp_base.md
Output to: {PROJECT_PATH}/PRPs/mini-{FEATURE_NAME}.md

Do BOTH steps yourself. DO NOT spawn sub-agents.
```

**等待研究结果完成。**

---

## 第3步：创建执行代理
使用`sessions_spawn`创建一个新的子代理来执行特性的实现工作：
```
EXECUTOR MISSION - Mini PIV
============================

Read {baseDir}/references/piv-executor.md for your role.
Read {baseDir}/references/execute-prp.md for the execution process.

PRP: {PROJECT_PATH}/PRPs/mini-{FEATURE_NAME}.md
Project: {PROJECT_PATH}

Follow: Load PRP → Plan Thoroughly → Execute → Validate → Verify
Output EXECUTION SUMMARY.
```

---

## 验证阶段的决策
在创建完整的验证代理之前，先评估以下情况：
- 如果更改的文件少于5个，代码行数少于100行，且没有涉及外部API调用，则进行快速验证（协调者自行审核更改内容）；
- 否则，创建完整的验证代理（进入第4步）。

## 第4步：创建验证代理
使用`sessions_spawn`创建一个新的子代理来进行验证工作：
```
VALIDATOR MISSION - Mini PIV
=============================

Read {baseDir}/references/piv-validator.md for your process.

PRP: {PROJECT_PATH}/PRPs/mini-{FEATURE_NAME}.md
Project: {PROJECT_PATH}
Executor Summary: {SUMMARY}

Verify ALL requirements independently.
Output VERIFICATION REPORT with Grade, Checks, Gaps.
```

**处理验证结果**：
- 如果验证通过 → 提交代码；
- 如果发现漏洞 → 交由调试代理处理；
- 如果需要人工干预 → 请用户提供进一步的信息或指导。

---

## 第5步：调试循环（最多3次迭代）
使用`sessions_spawn`创建一个新的子代理来进行调试：
```
DEBUGGER MISSION - Mini PIV - Iteration {I}
============================================

Read {baseDir}/references/piv-debugger.md for your methodology.

Project: {PROJECT_PATH}
PRP: {PROJECT_PATH}/PRPs/mini-{FEATURE_NAME}.md
Gaps: {GAPS}
Errors: {ERRORS}

Fix root causes. Run tests after each fix.
Output FIX REPORT.
```

调试完成后：
- 如果验证通过 → 提交代码；
- 如果仍然存在问题 → 进入第5次迭代；
- 如果问题持续存在 → 提升问题处理级别。

---

## 智能提交代码
```bash
cd PROJECT_PATH && git status && git diff --stat
git add -A
git commit -m "feat(mini): implement {FEATURE_NAME}

- {bullet 1}
- {bullet 2}

Built via Mini PIV Ralph

Built with FTW (First Try Works) - https://github.com/SmokeAlot420/ftw"
```

---

## 工作完成
```
## MINI PIV RALPH COMPLETE

Feature: {FEATURE_NAME}
Project: {PROJECT_PATH}

### Artifacts
- PRP: PRPs/mini-{FEATURE_NAME}.md
- Analysis: PRPs/planning/mini-{FEATURE_NAME}-analysis.md

### Implementation
- Validation cycles: {N}
- Debug iterations: {M}

### Files Changed
{list}

All requirements verified and passing.
```

---

## 错误处理
- 如果执行代理遇到阻塞或无法继续执行 → 请用户提供帮助；
- 如果验证代理需要人工干预 → 请用户提供指导；
- 如果经过3次调试循环问题仍未解决 → 提升问题处理级别，并附上问题清单。

### 子代理的超时/失败处理
当某个子代理超时或失败时：
1. 检查该子代理是否完成了部分工作（例如：是否生成了必要的文件、编写了测试代码）；
2. 用更简洁的提示重新尝试一次；
- 如果重试仍然失败，将已完成的成果以及存在的问题提交给用户处理。

---

## 快速参考指南
| 使用场景 | 选择哪种工具 |
|----------|----------|
| 规模较小/中等的特性，无需编写PRD | **Mini PIV Ralph** |
| 规模较大、包含多个开发阶段的特性 | **完整的PIV流程（/piv）** |

### 文件命名规则
```
PRPs/mini-{feature-name}.md                  # PRP
PRPs/planning/mini-{feature-name}-analysis.md # Analysis
```