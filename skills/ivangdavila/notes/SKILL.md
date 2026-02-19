---
name: Notes
slug: notes
version: 1.0.1
homepage: https://clawic.com/skills/notes
description: 使用结构化的格式记录会议内容、决策结果以及各种想法，同时实现任务跟踪和可搜索的档案管理功能。
changelog: Added 7 note formats, action item tracking, memory storage with index
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户需要记录各种类型的笔记：会议记录、头脑风暴内容、决策事项、每日日志或项目进度。系统会负责笔记的格式化、行动项的提取、截止日期的跟踪以及笔记的检索。

## 架构

所有笔记都存储在 `~/notes/` 目录下。具体设置方法请参阅 `memory-template.md`。

```
~/notes/
├── index.md           # Search index with tags
├── meetings/          # Meeting notes by date
├── decisions/         # Decision log
├── projects/          # Project-specific notes
├── journal/           # Daily notes
└── actions.md         # Active action items tracker
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 所有笔记格式 | `formats.md` |
| 行动项管理系统 | `tracking.md` |
| 记忆系统设置 | `memory-template.md` |

## 核心规则

### 1. 始终使用结构化格式

每种类型的笔记都有固定的格式。具体模板请参阅 `formats.md`。

| 笔记类型 | 触发条件 | 关键要素 |
|-----------|---------|--------------|
| 会议记录 | "meeting notes", "call with" | 与会人员、决策内容、行动事项 |
| 决策记录 | "we decided", "decision:" | 背景信息、选项、理由 |
| 头脑风暴记录 | "ideas for", "brainstorm" | 初步想法、分类结果、下一步计划 |
| 日志记录 | "daily note", "today I" | 日期、重点内容、阻碍因素 |
| 项目进度记录 | "project update", "status" | 进展情况、阻碍因素、下一步行动 |

### 2. 积极提取行动项

当有人提到“我会做某事”或“我们需要做某事”时，这些内容都应被视为行动项。

**每个行动项必须包含：**
- [ ] **负责人**——负责执行该任务的人（@用户名）
- [ ] **具体任务**——清晰、可执行的描述
- [ ] **截止日期**——明确的日期（不能使用“尽快”或“ ASAP”）

**如果缺少截止日期，请建议一个具体的日期：**

```
⚠️ No deadline set for: "Review the proposal"
   Suggested: 2026-02-21 (2 days from now)
   Confirm or specify: ___
```

### 3. 一次回复，完整表达

切勿将笔记拆分成多条消息发送。每次发送笔记时，务必包含所有必要的信息。

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 [NOTE TYPE]: [Title] — [YYYY-MM-DD]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Formatted content per type]

⚡ ACTION ITEMS ([X] total)
1. [ ] @Owner: Task — Due: YYYY-MM-DD
2. [ ] @Owner: Task — Due: YYYY-MM-DD

📎 Saved: notes/[folder]/YYYY-MM-DD_[topic].md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 4. 文件命名规则

文件名格式应为：**YYYY-MM-DD_主题简称.md**（先写日期，再写主题）。

示例：
- ✅ 2026-02-19_product-review （正确格式）
- ❌ product-review-notes （错误格式：缺少日期）
- ❌ notes-2026-02-19 （错误格式：日期排在主题之后）

### 5. 为所有笔记添加标签以便检索

每条笔记的头部都应添加标签，以便后续查询。

```markdown
---
date: 2026-02-19
type: meeting
tags: [product, roadmap, q1-planning]
attendees: [alice, bob, carol]
---
```

每当有新笔记添加时，请更新 `~/notes/index.md` 文件。

### 6. 集中管理行动项

请将所有行动项的信息保存在 `~/notes/actions.md` 文件中，确保信息的一致性。具体操作方法请参阅 `tracking.md`。

| 状态 | 含义 |
|--------|---------|
| 🔴 过期 | 超过截止日期 |
| 🟡 即将到期 | 3天内到期 |
| 🟢 进行中 | 未来有截止日期 |
| ✅ 完成 | 已完成 |

### 7. 链接相关笔记

当笔记中引用之前的讨论内容时，请务必提供链接：
- 绝不要只写“如上所述”，而应添加链接（例如：`See [[2026-02-15_kickoff]]`）
- 创建新笔记前，请先搜索现有笔记以避免重复。

### 8. 决策记录的特殊处理

决策记录需要特别处理：

```markdown
## [DECISION] Title — YYYY-MM-DD

**Context:** Why this decision was needed
**Options Considered:**
1. Option A — pros/cons
2. Option B — pros/cons
**Decision:** What was chosen
**Rationale:** Why this option
**Owner:** Who made it
**Effective:** When it takes effect
**Reverses:** [[previous-decision]] (if applicable)
```

### 9. 评估会议效率

每条会议记录的末尾应添加对会议效果的评估。

```
📊 Meeting Effectiveness: [X/10]
   □ Clear agenda beforehand
   □ Started/ended on time  
   □ Decisions were made
   □ Actions have owners + deadlines
   □ Could NOT have been an email
```

### 10. 快速记录模式

在需要快速记录信息时，可以使用简化格式：

用户：**笔记：需要与 Sarah 通话，她要求周五前收到报告，我明天会发送草稿。**

系统会提取以下内容：
- 会议记录：与 Sarah 通话
- 行动项：发送报告草稿（发送者：@我，截止日期：明天）
- 行动项：提交最终报告（Sarah 需要在周五前收到）

## 常见错误

- **模糊的截止日期**：使用“ASAP”、“soon”或“next week”等模糊表述是不准确的。请使用具体的日期。
- **缺少负责人**：表述应为“我们应该由谁来负责某项任务”。
- **未集中管理的行动项**：未记录在 `actions.md` 中的行动项容易被遗忘。请确保所有行动项都被跟踪。
- **重复的笔记**：创建新笔记前请先搜索现有内容，避免重复。
- **没有检索标签**：没有标签的笔记将难以被找到。

## 相关工具

如果用户需要，可以使用以下工具进行扩展：
- `clawhub install meetings`：用于会议管理和议程安排
- `todo`：任务管理系统
- `documentation`：技术文档工具
- `journal`：每日日志记录工具
- `decisions`：决策记录工具

## 反馈建议

- 如果觉得这些规则有用，请给笔记点赞（使用 `clawhub star`）。
- 为了保持信息同步，请定期使用 `clawhub sync` 命令更新系统。