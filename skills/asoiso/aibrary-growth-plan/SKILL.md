---
name: aibrary-growth-plan
description: "[图书馆] 创建一个结构化的个人成长计划，包括书籍推荐、里程碑以及可执行的每周任务。适用于用户需要制定学习计划、安排学习时间表、系统地提升某项技能、规划个人或职业发展，或制定成长路线图的情况。触发条件包括使用类似“创建学习计划”、“帮助我在某方面成长”或“我想提升自己”等表达。"
---
# 成长计划 — 图书馆

制定一个结构化、有时间限制的个人成长计划，通过阅读书籍和进行实际操作来促进学习。该计划基于学习科学的原则：间隔重复、主动回忆以及逐步增加学习难度。

## 输入信息

- **成长目标**（必填）：用户希望实现的目标（技能提升、知识拓展、职业转型等）
- **时间框架**（可选）：用户可用的时间（默认：12周）
- **每周可用时间**（可选）：用户每周可以投入的学习时间（默认：5小时）
- **当前水平**（可选）：初学者、中级者、高级者（根据上下文推断）
- **限制条件**（可选）：预算、语言要求、阅读格式偏好

## 工作流程

1. **明确目标**：将成长目标分解为可衡量的成果：
   - 学习结束后，用户将能够完成哪些目前无法完成的任务？
   - 需要填补哪些知识空白？
   - 需要练习哪些技能？

2. **划分阶段**：将时间框架分为3-4个阶段：
   - **第一阶段 — 基础阶段**（约25%的时间）：建立核心理解
   - **第二阶段 — 深化阶段**（约35%的时间）：培养关键技能和知识
   - **第三阶段 — 应用阶段**（约25%的时间）：将所学知识应用于实际情境
   - **第四阶段 — 整合阶段**（约15%的时间）：反思、总结并规划下一步行动

3. **为每个阶段挑选资源**：
   - 为每个阶段选择1-2本主要参考书籍（学习的基石）
   - 补充活动（练习题、项目、反思记录）
   - 里程碑式检查点

4. **制定每周任务**：将每个阶段的具体内容分解为每周可执行的行动：
   - 阅读任务（指定章节，而非“阅读整本书”）
   - 反思提示（用于写日记或思考的问题）
   - 实践活动（应用所学知识）
   - 周度检查点（用于评估学习进度）

5. **建立问责机制**：
   - 每周自我评估问题
   - 计划中期回顾
   - 计划结束时的反思模板

6. **语言设置**：根据用户输入的语言生成相应的计划内容。

## 输出格式

```
# 🌱 Growth Plan: [Goal]

**Duration**: [X weeks] | **Weekly commitment**: [X hours] | **Current level**: [Level]

## Goal Definition
**By the end of this plan, you will**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

---

## Phase 1: Foundation (Weeks 1-[X])
*Goal: [What this phase achieves]*

📖 **Primary book**: [Book Title] by [Author]
*Why*: [How this book serves the foundation]

### Week 1
- [ ] **Read**: [Book], Chapters [X-Y] (~[Z] pages)
- [ ] **Reflect**: [Specific reflection prompt]
- [ ] **Practice**: [Specific activity]
- [ ] **Checkpoint**: [How to verify understanding]

### Week 2
- [ ] **Read**: [Book], Chapters [X-Y]
- [ ] **Reflect**: [Reflection prompt]
- [ ] **Practice**: [Activity]
- [ ] **Checkpoint**: [Verification]

...

---

## Phase 2: Depth (Weeks [X]-[Y])
*Goal: [What this phase achieves]*

📖 **Primary book**: [Book Title] by [Author]

### Week [X]
...

---

## Phase 3: Application (Weeks [X]-[Y])
*Goal: [What this phase achieves]*

📖 **Primary book**: [Book Title] by [Author]

### Week [X]
...

---

## Phase 4: Integration (Weeks [X]-[Y])
*Goal: [What this phase achieves]*

### Week [X]
- [ ] **Review**: Revisit key concepts from Phase 1-3
- [ ] **Reflect**: [Deep reflection prompt]
- [ ] **Create**: [Synthesis project — write, teach, or build something]
- [ ] **Plan next**: Identify the next growth goal

---

## 📊 Mid-Plan Review (Week [X])

Ask yourself:
1. Which concepts have clicked? Which still feel unclear?
2. Am I applying what I'm learning? Where?
3. Does the pace feel right? Adjust if needed.

## 🎯 End-of-Plan Reflection

1. What were my 3 biggest insights?
2. What skill or knowledge did I gain that I didn't have before?
3. How has my thinking changed?
4. What's my next growth goal?

---

*Growth plan created by Aibrary — structured learning for lasting growth.*
```

## 制定计划的指南

- 每项任务都必须具体且可操作（例如：“阅读第3-5章”，而非“阅读部分内容”）
- 设定检查点，让用户能够验证自己的理解程度，而不仅仅是完成阅读任务
- 计划应符合用户的时间安排，避免让每周的任务过于繁重
- 反思提示应激发用户的深度思考，而不仅仅是简单的“你学到了什么？”
- 实践活动应侧重于应用所学知识，而不仅仅是阅读更多内容
- 如果目标过于模糊，请在制定计划前要求用户进一步明确
- 包括计划中期回顾环节，以便根据实际情况进行调整
- 每个阶段都应建立在前一个阶段的基础上，逐步增加学习难度
- 建议选择较少的书籍，但深入阅读每本书的内容，注重学习质量而非数量