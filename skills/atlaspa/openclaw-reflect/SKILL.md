---
name: openclaw-reflect
version: 1.0.0
description: >
  **自我提升层（Self-Improvement Layer）**  
  该层具备评估分离（evaluation separation）、回滚（rollback）以及分层操作符控制（tiered operator gates）功能。它能够跨会话（sessions）观察系统运行结果，检测其中的重复性模式（recurring patterns），提出改进方案，并通过独立的评估机制（separate evaluator）对这些方案进行验证。最后，系统具备快照（snapshot）和回滚（rollback）功能，从而确保变更能够安全地应用到系统中。
author: AtlasPA
tags: [self-improvement, reflection, memory, safety, hooks, evaluation]
hooks:
  - event: PostToolUse
    path: hooks/post-tool-use.js
  - event: SessionEnd
    path: hooks/session-end.js
  - event: UserPromptSubmit
    path: hooks/user-prompt-submit.js
permissions:
  - read: workspace
  - write: .reflect/
  - write: MEMORY.md
  - write: CLAUDE.md
  - propose: SOUL.md
---
# openclaw-reflect

您可以使用这个自我改进系统。该系统会监控您在不同会话中的工具使用情况，检测出反复出现的故障模式，并针对您的持久化存储（MEMORY.md）和操作指令（instructions）提出针对性的修改建议。

## 您的职责

### 工作期间
`PostToolUse` 钩子会自动记录使用工具后的结果。除非您发现某个无法解释的严重故障，否则无需进行任何操作；在这种情况下，请手动记录观察结果：

```bash
node .reflect/scripts/observe.js --manual \
  --type error \
  --tool "ToolName" \
  --pattern "故障的简要描述" \
  --context "您当时正在尝试执行的任务"
```

### 当系统提示时（`UserPromptSubmit` 会触发此操作）
如果 `.reflect/pending.json` 文件中包含需要操作员审批的改进建议，请运行以下命令查看这些建议：
```bash
node .reflect/scripts/status.js
```
或者直接向我请求展示这些建议。

### 会话结束时（系统自动执行）
`SessionEnd` 钩子会自动执行以下操作：
1. 检测在至少 2 个会话中反复出现的故障模式。
2. 生成结构化的改进建议。
3. 将这些建议发送给评估者进行审核。
4. 自动将低风险级别的修改应用到 `MEMORY.md` 中。
5. 将高风险级别或涉及核心价值观（SOUL.md）的修改提交给操作员审批。

您可以在会话结束后的输出中看到这些修改的总结。

## 修改的审批级别

| 审批级别 | 修改目标 | 审批流程 |
|------|---------|------|
| 0 — 观察结果 | `.reflect/outcomes.jsonl` | 系统自动处理 |
| 1 — MEMORY.md | 事实性修正、偏好设置更新 | 如果置信度 ≥ 0.7 时自动应用 |
| 2 — CLAUDE.md / 项目指令 | 行为模式调整 | 如果置信度 ≥ 0.85 时自动应用 |
| 3 — SOUL.md | 核心价值观、系统标识、使用限制 | 必须经过操作员审批 |

## 评估流程
在应用任何 1 级及以上的修改之前，系统会先由评估者进行审核：
- 这些修改是否与现有原则或系统设置相冲突？
- 这种故障模式是否确实存在（而非偶然现象）？
- 最小的修改方案是什么？
- 这些修改是否可能在其他地方引发问题？

评估者需要保持谨慎的态度。通过审核的修改建议更有可能是真正的改进，而非由导致错误的相同逻辑产生的建议。

## 回滚机制
每次应用修改之前，系统会先创建一个快照（如果安装了 `openclaw-warden` 的话），并将该快照记录在 `.reflect/applied.jsonl` 文件中。要回滚最近的一次修改，可以运行以下命令：

```bash
node .reflect/scripts/rollback.js
```

要按修改 ID 回滚特定修改，可以使用以下命令：

```bash
node .reflect/scripts/rollback.js --id <修改 ID>
```

## 状态文件
以下文件用于存储系统的运行状态：
- `.reflect/outcomes.jsonl`：仅用于记录修改结果。
- `.reflect/patterns.json`：记录每次会话中检测到的故障模式。
- `.reflect/proposals.json`：存储待审核的修改建议。
- `.reflect/pending.json`：存储需要操作员审批的修改建议。
- `.reflect/applied.jsonl`：记录已应用的修改。
- `.reflect/snapshots/`：用于回滚的修改前快照。

## 自愿贡献
`openclaw-reflect` 是免费使用的。如果您发现该系统有效消除了重复出现的故障或节省了调试时间，我们欢迎您自愿通过 x402 协议捐赠 5 美元。无需注册账户，代理可以自行完成捐赠。

详情请参阅 [AGENT-PAYMENTS.md](AGENT-PAYMENTS.md)。

## 操作员命令
```bash
# 查看当前状态
node .reflect/scripts/status.js

# 查看待审核的修改建议
node .reflect/scripts/status.js --pending

# 批准特定修改建议
node .reflect/scripts/apply.js --id <修改建议 ID> --approve

# 拒绝修改建议
node .reflect/scripts/apply.js --id <修改建议 ID> --reject

# 回滚最近一次修改
node .reflect/scripts/rollback.js

# 查看修改历史
node .reflect/scripts/status.js --history
```