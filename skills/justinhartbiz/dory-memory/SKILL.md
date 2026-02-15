---
name: dory-memory
description: 基于文件的AI代理内存系统，适用于那些在会话之间会丢失记忆的AI代理。该系统采用了“Dory-Proof”模式来确保在上下文重置后数据的连续性。适用于设置代理内存、构建工作区结构、实现任务跟踪以及防止上下文丢失错误等场景。相关功能可通过“内存系统”、“跨会话记忆”、“Dory模式”、“代理连续性”或“工作区设置”等选项进行触发。
---

# Dory-Proof 记忆系统

AI 代理在会话之间会忘记所有信息。该技能实现了一个基于文件的记忆系统，能够在上下文重置后仍然保留数据。

## 核心原理

**文本 > 大脑。** 将所有内容都记录下来。文件就是记忆。代理“记住”的只有磁盘上的内容。

## Dory-Proof 模式（关键步骤）

当用户给出任务时：
1. **立即** 将用户的原话写入 `state/ACTIVE.md` 文件中。
2. 然后解释这些话的含义。
3. 接着执行任务。
4. 完成任务后进行标记。

**原因：** 改述会导致信息失真。使用原话可以在上下文变化时准确保留用户的意图。

## 工作区结构

```
workspace/
├── AGENTS.md        # Operating rules (system file, don't rename)
├── SOUL.md          # Identity + personality
├── USER.md          # About the human
├── MEMORY.md        # Curated long-term memory (<10KB)
├── LESSONS.md       # "Never again" safety rules
├── TOOLS.md         # Tool-specific notes
│
├── state/           # Active state (check every session)
│   ├── ACTIVE.md    # Current task (exact user words)
│   ├── HOLD.md      # Blocked items (check before acting!)
│   ├── STAGING.md   # Drafts awaiting approval
│   └── DECISIONS.md # Recent choices with timestamps
│
├── memory/          # Historical
│   ├── YYYY-MM-DD.md
│   ├── recent-work.md
│   └── archive/
│
└── ops/             # Operational
    └── WORKSPACE-INDEX.md
```

## 启动序列（每次会话）

1. 读取 `state/HOLD.md` 文件——被“阻止”（暂时不执行的）任务。
2. 读取 `state/ACTIVE.md` 文件——当前正在执行的任务。
3. 读取 `state/DECISIONS.md` 文件——用户最近的选择。
4. 读取 `memory/recent-work.md` 文件——过去 48 小时的工作记录。
5. 读取 `MEMORY.md` 文件——长期存储的数据（仅限当前会话）。

启动后的输出状态行：
```
📋 Boot: ACTIVE=[task] | HOLD=[n] items | STAGING=[n] drafts
```

## 状态文件格式

### state/ACTIVE.md
```markdown
## Current Instruction
**User said:** "[exact quote]"
**Interpretation:** [what you think it means]
**Status:**
- [ ] Step 1
- [ ] Step 2
```

### state/HOLD.md
```markdown
[YYYY-MM-DD HH:MM | session] Item — reason blocked
```
**所有代理在采取任何行动之前都必须先检查这些文件。**

### state/DECISIONS.md
```markdown
[YYYY-MM-DD HH:MM | session] Decision made
```

## 冲突解决

当文件之间存在冲突时，按照优先级处理（从高到低）：
1. `state/HOLD.md` 文件——被阻止的任务优先级最高。
2. `state/ACTIVE.md` 文件——当前正在执行的任务。
3. `state/DECISIONS.md` 文件——用户最近的选择。
4. `AGENTS.md` 文件——通用规则。

## 内存评分（在保存到 `MEMORY.md` 之前）

根据以下四个维度进行评分（每个维度 0–3 分）：

| 维度 | 0 | 1 | 2 | 3 |
|------|---|---|---|---|
| 持久性 | 明天就会消失 | 几周 | 几个月 | 几年+ |
| 重用性 | 一次性使用 | 偶尔使用 | 经常使用 | 每次会话都使用 |
| 影响程度 | 微不足道 | 了解这些信息有帮助 | 会改变输出结果 | 会改变决策 |
| 独特性 | 明显有用 | 有点帮助 | 难以重新生成 | 没有这个信息就无法完成 |

**满足以下条件时保存到 `MEMORY.md`：** 总分 ≥ 8 分，或者任意一个维度的得分 ≥ 3 分且总分 ≥ 6 分。

## 快速设置

将模板文件从 `assets/templates/` 复制到你的工作区：
```bash
cp -r skills/dory-memory/assets/templates/* ~/.openclaw/workspace/
```

然后根据你的代理需求自定义 `SOUL.md` 和 `USER.md` 文件。

## 参考资料

- `references/IMPLEMENTATION-GUIDE.md` — 完整的设置指南
- `references/ANTI-PATTERNS.md` — 需要避免的常见错误