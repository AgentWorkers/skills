---
name: release-discipline
description: >
  **强制执行AI代理和开发者的发布规范**：  
  - 防止版本混乱（即同一版本被多次发布）；  
  - 强制在发布前进行质量检查；  
  - 确保每次发布之间有24小时的冷却时间（即必须等待至少24小时才能再次发布新版本）。  
  **适用场景**：  
  当用户需要执行“发布（release）”、“部署（deploy）”或“升级版本（version bump）”等操作时，该规则会自动触发。  
  **相关命令/事件**：  
  - `release`  
  - `publish`  
  - `deploy`  
  - `version bump`  
  - `npm publish`  
  - `릴리즈`  
  - `배포`  
  - `버전`
author: 무펭이 🐧
---
# 🛑 发布规范

杜绝版本滥发，追求质量而非数量。

**核心原则：“只有完成的工作才有价值。”**

## 规范触发条件

在任何发布、推送或部署操作之前，必须执行预发布检查列表。

## 预发布检查列表（所有项目都必须通过）

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

### 第三关：文档检查
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

### 第五关：项目是否符合发布标准
```
❓ What kills this project?
→ If no kill criteria defined: ⚠️ WARNING — "Define when to stop: 'If X doesn't happen in Y weeks, shut it down.'"
→ If defined: ✅ PASS — Remind user of their kill criteria
```

### 第六关：是否存在自相矛盾的情况
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

## 周度回顾

每隔 7 天，对发布日志进行回顾：
- 本周发布的总版本数
- 被拒绝的版本比例（理想范围：20-40%；如果比例过低，说明检查不够严格）
- 如果所有版本都被通过，说明检查流程流于形式，需要重新审视检查标准
- 分析是否存在重复出现的问题

## 该规范能防止的常见问题：

1. **版本滥发**：在 3 天内发布过多版本
2. **盲目开发**：大量开发但没有任何项目真正完成
3. **文档缺失**：在代码未完成的情况下就进行发布
4. **闭门造车**：在没有用户反馈的情况下发布产品
5. **违反自身规则**：违背自己设定的原则
6. **过早优化**：对无人使用的功能进行过度优化

## 哲学理念

> “急于发布并不等同于产品已经准备好发布。”
> “害怕产品变得过时并不是发布的理由。”
> “一个出色的发布产品胜过十个平庸的产品。”

这个规范的作用是**制动器**，而非**加速器**。它的存在是因为，软件开发中最困难的部分并不在于创造产品本身，而在于知道何时应该停止开发，何时应该专注于完成产品。

---
> 🐧 由 **무펭이** 制作 — [무펭이즘(Mupengism)](https://github.com/mupeng) 生态系统中的技能之一