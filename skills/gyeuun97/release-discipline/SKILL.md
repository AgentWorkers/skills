---
name: release-discipline
description: **强制实施AI代理和开发者的发布规范**：  
- 防止版本混乱（即避免频繁发布低质量或重复的版本）；  
- 强制在发布前进行质量检查；  
- 确保每次发布之间有24小时的冷却时间（即禁止在指定时间内再次发布新版本）。  

**适用场景**：  
当用户需要执行以下操作时使用该规则：  
- 发布（release）  
- 公布（publish）  
- 部署（deploy）  
- 升级版本（version bump）  
- 使用npm命令发布（npm publish）  

**触发条件**：  
- 触发命令包括：`release`、`publish`、`deploy`、`version bump`、`npm publish`。
---

# 🛑 发布规范

杜绝版本滥发，追求质量而非数量。

**核心原则：“只有完成的工作才有价值。”**

## 规范触发条件

在所有发布、公开或部署操作之前，必须执行预发布检查流程。

## 预发布检查清单（所有项目都必须通过）

在任何版本更新或发布之前，必须完成以下检查：

### 第一关：冷却期检查
```
❓ When was the last release?
→ If < 24 hours ago: 🛑 BLOCKED — "Cool down. Last release was {X}h ago. Wait until 24h."
→ If ≥ 24 hours: ✅ PASS
```

### 第二关：用户反馈检查
```
❓ Has anyone used the previous version?
→ Check: GitHub issues, npm downloads, ClawHub installs, user messages
→ If no feedback exists: ⚠️ WARNING — "No one has used v{X} yet. Why release v{X+1}?"
→ If feedback exists: ✅ PASS — Summarize feedback
```

### 第三关：文档完整性检查
```
❓ Is documentation updated?
→ Check for: README.md, CHANGELOG, English docs
→ Missing README: 🛑 BLOCKED
→ Missing English: ⚠️ WARNING — "Global users can't read this"
→ All present: ✅ PASS
```

### 第四关：质量检查
```
❓ Does this release have substance?
→ Ask: "What's the ONE thing this release does better than the last?"
→ If answer is vague ("minor fixes", "improvements"): ⚠️ WARNING — "Be specific. What changed?"
→ If answer is clear: ✅ PASS
```

### 第五关：不符合发布标准的判断标准检查
```
❓ What kills this project?
→ If no kill criteria defined: ⚠️ WARNING — "Define when to stop: 'If X doesn't happen in Y weeks, shut it down.'"
→ If defined: ✅ PASS — Remind user of their kill criteria
```

### 第六关：自相矛盾内容的检查
```
❓ Does this action match your stated principles?
→ Read SOUL.md (or equivalent principles file)
→ Look for contradictions:
  - "Ship one thing at a time" + releasing 3 things = 🛑
  - "Quality over quantity" + 5 releases in 3 days = 🛑
  - "Finish before starting new" + new project while old unfinished = ⚠️
→ If contradiction found: 🛑 BLOCKED — Quote the principle and show the contradiction
→ If consistent: ✅ PASS
```

## 评分机制

```
🛑 BLOCKED (any) → Cannot release. Fix the issue first.
⚠️ WARNING only → Can release, but agent must voice concern clearly.
✅ ALL PASS → Release approved. Proceed.
```

## 发布日志

每次发布（无论是通过还是被拒绝）后，都需要将相关记录写入 `memory/release-log.md` 文件中：
```markdown
## {date} — v{version}
- Status: ✅ APPROVED / 🛑 BLOCKED / ⚠️ WARNED
- Gates: [1:✅ 2:⚠️ 3:✅ 4:✅ 5:✅ 6:✅]
- Reason: {why released or why blocked}
- User feedback on previous: {summary or "none"}
- Time since last release: {hours}
```

## 每周回顾

每隔 7 天，对发布日志进行一次回顾：
- 本周发布的总版本数
- 被拒绝的版本比例（理想范围：20-40%；如果比例过低，说明检查流程不够严格）
- 如果所有版本都被通过，需要重新审视检查标准
- 分析是否存在重复出现的问题

## 该规范能防止的常见问题：

1. **版本滥发**（例如：3 天内发布 17 个版本）
2. **盲目开发、毫无成果**（只是大量开发却没有任何成品）
3. **文档缺失**（发布代码时没有配套的文档）
4. **闭门造车**（在没有用户反馈的情况下发布产品）
5. **违反自身制定的规则**
6. **过早优化**（对无人使用的功能进行过度优化）

## 哲学理念

> “急于发布并不意味着产品已经准备好。”
> “害怕产品被忽视并不是发布的理由。”
> “一个优秀的发布产品胜过十个平庸的产品。”

这个规范的作用是**制动器**，而非**加速器**。它的存在是因为，软件开发过程中最困难的部分并不在于创造产品本身，而在于知道何时该停止开发、何时该完成产品。