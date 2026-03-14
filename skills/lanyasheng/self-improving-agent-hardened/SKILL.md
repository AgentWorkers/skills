---
name: self-improvement
description: "记录学习内容、错误以及相应的修正措施，以促进持续改进。适用场景包括：  
(1) 命令或操作意外失败时；  
(2) 用户通过直接反馈（如“不，那不对”）来纠正代理的行为时；  
(3) 用户请求的功能实际上并不存在时；  
(4) 外部 API 或工具出现故障时。  
**重要提示：** 每条用户消息最多只能记录一条学习日志。**请勿** 连续触发多个自我改进动作。"
metadata:
---
# 自我提升技能

将学习内容及遇到的错误记录到 markdown 文件中，以实现持续改进。

## 关键规则：防循环机制

**以下规则优先于本技能中的所有其他指示：**

1. **每条用户消息对应一条学习记录** — 记录一条内容后，立即停止操作。不要搜索相关记录，也不要进行推广或审核。
2. **禁止连锁反应** — 自我提升过程中产生的工具结果不得在同一轮次中触发另一个自我提升动作。
3. **禁止批量审核** — 绝不在同一轮次中阅读多个学习记录。如果需要审核，请在下一轮开始时进行，而不是在对话进行过程中。
4. **最多使用 3 个工具** — 单次触发下的整个自我提升流程必须在 ≤3 次工具调用内完成：(1) 可选地阅读目标文件；(2) 添加记录；(3) 完成操作。
5. **冷却期** — 记录完成后，需等待用户下一次明确的指令，再考虑新的自我提升动作。
6. **讨论 ≠ 更正** — 如果用户只是在讨论想法、探讨方法或整理文档，这不属于更正行为。只有在用户明确表示“不对”或“你犯了错误”时，才触发自我提升动作。

## 快速参考

| 情况 | 应采取的行动 | 最多允许使用的工具调用次数 |
|-----------|--------|---------------|
| 命令/操作失败 | 添加到 `.learnings/ERRORS.md` | 2 次 |
| 用户明确指出错误 | 添加到 `.learnings/LEARNINGS.md` | 2 次 |
| 用户提出功能需求 | 添加到 `.learnings/FEATURE_REQUESTS.md` | 2 次 |
| API/外部工具失败 | 添加到 `.learnings/ERRORS.md` | 2 次 |

## 何时不应触发自我提升

- 用户正在进行正常的对话或讨论
- 用户正在审核或整理文档（而非纠正你的错误）
- 用户在讨论方法（而非指出你的错误）
- 用户对系统/设计提出质疑（而非针对你的错误）
- 你已经在当前轮次中记录了学习内容
- 对话内容涉及第三方系统，而非你的行为

## 记录格式

### 学习记录

添加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high
**Status**: pending

### Summary
One-line description

### Details
What happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement
---
```

### 错误记录

添加到 `.learnings/ERRORS.md`：

```markdown
## [ERR-YYYYMMDD-XXX] command_or_tool

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
What failed

### Error
Actual error message

### Context
Command attempted, environment

### Suggested Fix
If identifiable
---
```

## 推广记录（延迟进行）

**不要在记录的同时进行推广。** 推广应在以下情况下进行：
- 在专门的审核会话中（用户明确要求）
- 在会话开始时回顾之前的学习内容
- 绝不允许自动触发或作为连锁反应进行

| 学习类型 | 推广目标文件 |
|---------------|------------|
| 行为模式 | `SOUL.md` |
| 工作流程改进 | `AGENTS.md` |
| 工具使用技巧 | `TOOLS.md` |

## 定期审核（仅由用户发起）

只有在用户明确要求或会话开始时，才进行 `.learnings/` 文件的审核。
**绝不要** 仅基于新记录的生成就自动触发审核。

## OpenClaw 工作区结构

```
~/.openclaw/workspace/
├── AGENTS.md
├── SOUL.md
├── TOOLS.md
├── MEMORY.md
├── memory/YYYY-MM-DD.md
└── .learnings/
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

### 功能需求记录

添加到 `.learnings/FEATURE_REQUESTS.md`：

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending

### Requested Capability
What the user wanted to do

### User Context
Why they needed it

### Complexity Estimate
simple | medium | complex
---
```

## ID 生成格式

格式：`TYPE-YYYYMMDD-XXX`
- `TYPE`：`LRN`（学习记录），`ERR`（错误记录），`FEAT`（功能需求）
- `YYYYMMDD`：当前日期
- `XXX`：序列号（例如 `001`、`002`）

## 解决问题

当问题得到解决后，将记录的 **状态** 从 “pending” 更新为 “resolved”，并添加以下内容：

```markdown
### Resolution
- **Resolved**: ISO-8601 timestamp
- **Notes**: Brief description of fix
```