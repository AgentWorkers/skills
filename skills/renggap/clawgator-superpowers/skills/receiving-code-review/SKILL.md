---
name: receiving-code-review
description: **使用场景：**  
在收到代码审查反馈后，在实施这些建议之前使用。特别是当反馈内容不明确或存在技术上的疑问时，需要经过严格的技术验证，而不仅仅是表面上的同意或盲目执行。
---

# 代码审查流程

## 概述

代码审查需要的是技术上的评估，而不是表面的赞同或反对。

**核心原则：** 在实施之前先验证；在假设之前先询问；技术正确性优先于社交上的舒适感。

## 回应模式

```
WHEN receiving code review feedback:

1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## 禁止的回应方式

**绝对禁止：**
- “你完全正确！”（这明显违反了 CLAUDE.md 的规定）
- “非常好的观点！” / “很棒的反馈！”（只是为了表示赞同）
- “我现在就实现它”（在验证之前）

**正确的回应方式：**
- 重新陈述技术要求
- 提出澄清问题
- 如果有错误，用技术理由进行反驳
- 直接开始行动（行动胜过空话）

## 处理不明确的反馈

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**示例：**
```
your human partner: "Fix 1-6"
You understand 1,2,3,6. Unclear on 4,5.

❌ WRONG: Implement 1,2,3,6 now, ask about 4,5 later
✅ RIGHT: "I understand items 1,2,3,6. Need clarification on 4 and 5 before proceeding."
```

## 针对不同来源的反馈处理方式

### 来自你的团队成员的反馈：
- **可信赖的反馈**：理解后直接实施
- 如果范围不明确，仍然需要询问
- 不要只是表面同意，而要提出具体问题
- 直接采取行动或给予技术上的认可

### 来自外部审阅者的反馈：
```
BEFORE implementing:
  1. Check: Technically correct for THIS codebase?
  2. Check: Breaks existing functionality?
  3. Check: Reason for current implementation?
  4. Check: Works on all platforms/versions?
  5. Check: Does reviewer understand full context?

IF suggestion seems wrong:
  Push back with technical reasoning

IF can't easily verify:
  Say so: "I can't verify this without [X]. Should I [investigate/ask/proceed]?"

IF conflicts with your human partner's prior decisions:
  Stop and discuss with your human partner first
```

**你的团队成员的准则：** “对待外部反馈要保持怀疑态度，但要认真核实。”

## 对“YAGNI”（Don’t Add What You Don’t Need）原则的遵守

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage

  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

**你的团队成员的准则：** “你和审阅者都要向我汇报。如果不需要某个功能，就不要添加它。”

## 实施顺序

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Then implement in this order:
     - Blocking issues (breaks, security)
     - Simple fixes (typos, imports)
     - Complex fixes (refactoring, logic)
  3. Test each fix individually
  4. Verify no regressions
```

## 何时应该提出反驳

在以下情况下应该提出反驳：
- 建议会破坏现有的功能
- 审阅者缺乏完整的背景信息
- 建议的功能未被使用（违反 YAGNI 原则）
- 从技术上来说不适用于当前的技术栈
- 与团队成员的架构决策存在冲突

**如何提出反驳：**
- 使用技术理由，而不是采取防御性态度
- 提出具体问题
- 提供可运行的测试或代码作为依据
- 如果涉及架构问题，要与团队成员共同讨论

**如果觉得公开反驳会让人不适，可以这样说：** “团队中有些情况不太对劲……”

## 对正确反馈的认可

当反馈确实正确时：
```
✅ "Fixed. [Brief description of what changed]"
✅ "Good catch - [specific issue]. Fixed in [location]."
✅ [Just fix it and show in the code]

❌ "You're absolutely right!"
❌ "Great point!"
❌ "Thanks for catching that!"
❌ "Thanks for [anything]"
❌ ANY gratitude expression
```

**为什么不需要说“谢谢”：** 行动本身已经表达了感谢。代码本身就能证明你收到了反馈。

**如果你发现自己想要写下“谢谢”，请删除这句话**，而是直接说明你将如何根据反馈进行修改。

## 如何优雅地纠正自己的反驳

如果你在反驳时犯了错：
```
✅ "You were right - I checked [X] and it does [Y]. Implementing now."
✅ "Verified this and you're correct. My initial understanding was wrong because [reason]. Fixing."

❌ Long apology
❌ Defending why you pushed back
❌ Over-explaining
```

客观地说明错误，并继续处理问题。

## 常见错误

| 错误 | 应对方法 |
|---------|-----|
| 只是表面同意 | 重新陈述技术要求或直接采取行动 |
| 不先验证就盲目实施 | 先根据代码库进行验证 |
- 不进行测试就批量修改代码 | 一次修改一个功能，逐一测试 |
- 假设审阅者总是对的 | 核实建议是否会导致问题 |
- 因害怕反驳而回避问题 | 技术正确性永远比个人感受更重要 |
- 只部分实施修改 | 先澄清所有问题 |
- 无法验证就贸然继续 | 说明自己的局限性，并寻求指导

## 实际案例

**表面同意的错误示例：**
```
Reviewer: "Remove legacy code"
❌ "You're absolutely right! Let me remove that..."
```

**正确的技术验证示例：**
```
Reviewer: "Remove legacy code"
✅ "Checking... build target is 10.15+, this API needs 13+. Need legacy for backward compat. Current impl has wrong bundle ID - fix it or drop pre-13 support?"
```

**正确应用 YAGNI 原则的示例：**
```
Reviewer: "Implement proper metrics tracking with database, date filters, CSV export"
✅ "Grepped codebase - nothing calls this endpoint. Remove it (YAGNI)? Or is there usage I'm missing?"
```

**反馈不明确的示例：**
```
your human partner: "Fix items 1-6"
You understand 1,2,3,6. Unclear on 4,5.
✅ "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
```

## 在 GitHub 上的回复方式

在 GitHub 上回复审阅者的评论时，请在评论线程中回复（路径：`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`），而不是在 PR 的顶层评论中回复。

## 总结

**外部反馈只是供你参考的建议，并非必须遵循的命令。**

先验证，再提问，最后再实施。

永远要坚持技术上的严谨性，不要只是表面上的赞同或反对。