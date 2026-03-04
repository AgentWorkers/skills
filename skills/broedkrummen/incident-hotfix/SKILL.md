---
name: incident-hotfix
description: 面向开发者的事件响应机制及生产问题的紧急修复流程。适用于需要可复现的问题分类、补丁/回滚决策、适用于持续集成（CI）环境的紧急修复分支、证据收集，以及与代码变更相关的事后分析跟踪场景。
---
# 事件热修复（Incident Hotfix）

在需要代码级修复时，请结合更全面的事件响应流程来使用本指南。

## 工作流程

1. **根据 `references/severity-matrix.md` 对事件的严重程度进行分类**。
2. **从当前的生产环境标签/提交（production tag/commit）创建一个热修复分支**。
3. **在尽可能少的失败测试用例的情况下重现问题并隔离问题**。
4. **应用修复代码，并制定回滚计划**。
5. **运行针对性的持续集成（CI）检查**。
6. **收集所有相关证据**。
7. **合并代码、验证修复效果，并进行事后分析**。

## 第一步 — 创建事件工作区（Create Incident Workspace）

```bash
bash scripts/start_hotfix.sh --id INC-1234 --base main
```

此步骤将创建：
- `hotfix/INC-1234-<slug>` 分支
- `docs/incidents/INC-1234/` 文件夹
- 包含时间线、回滚方案及后续处理步骤的起始文件

## 第二步 — 收集证据（Collect Evidence）

```bash
bash scripts/capture_evidence.sh --id INC-1234
```

将以下内容收集到 `docs/incidents/INC-1234/evidence/` 文件夹中：
- 最新的提交记录及差异摘要
- 变更的文件列表
- 本地环境的快照（仅包含必要的数据）
- 测试输出日志

## 第三步 — 修复前的验证（Patch Verification）

在提交代码之前，请确保：
- 失败的测试用例已被重现（或已有详细的文档记录）
- 修复的范围尽可能小
- 回滚命令已记录在 `ROLLBACK.md` 文件中
- 相关的测试用例通过，且没有新的代码风格/类型错误出现

## 第四步 — 事后分析（Postmortem Analysis）

使用 `references/action-template.md` 将分析结果转化为具体的任务，包括：
- 负责人
- 任务完成截止日期
- 验证标准

## 必需的输出文件

- `docs/incidents/<id>/TIMELINE.md`（事件时间线）
- `docs/incidents/<id>/ROLLBACK.md`（回滚方案）
- `docs/incidents/<id>/ACTIONS.md`（后续处理步骤）
- `docs/incidents/<id>/evidence/`（证据包）

## 注意事项

- 在处理事件时，优先选择最小范围的、安全的修复方案，而非进行大规模的代码重构。
- 如果根本原因尚不明确，应先采取临时措施控制问题，再实施永久性修复。
- 绝不要在没有回滚方案的情况下合并热修复代码。