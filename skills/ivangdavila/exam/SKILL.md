---
name: Exam
description: 可以从任何学习材料中生成练习测试、闪卡、学习计划以及定时模拟题。
---

## 该工具的功能

该工具可帮助用户全面准备考试：
- **练习测试**：包含选择题、简答题和论述题
- **闪卡**：用于间隔重复学习，支持导出到 Anki 软件
- **模拟考试**：模拟真实考试环境的限时测试
- **差距分析**：识别学习薄弱环节，确定需要重点复习的主题
- **学习计划**：根据考试日期和个人时间安排制定实际可行的学习计划
- **内容摘要**：将章节内容精简为 1-2 页的考试相关要点
- **概念图**：帮助用户直观理解各知识点之间的联系
- **快速复习资料**：提供考前 30 分钟的复习资料

适用于：大学考试、认证考试（如 AWS、PMP 等）、标准化考试以及专业执照考试。

---

## 快速参考

| 功能 | 相关文件 |
|------|------|
| 问题生成规则 | `questions.md` |
| 闪卡格式与使用策略 | `flashcards.md` |
| 模拟考试设置 | `simulations.md` |
| 成绩跟踪 | `tracking.md` |

---

## 核心工作流程

### 1. 提供学习素材
用户提供学习资料，如笔记、教科书章节、幻灯片、文档或以往的考试题目。

### 2. 生成问题
系统根据难度生成相应类型的问题：
- **简单题**：考查记忆、定义和基础概念
- **中等难度题**：考查应用能力、比较分析和综合判断
- **难题**：考查综合运用能力和复杂逻辑推理

### 3. 练习与成绩跟踪
用户完成答题后，系统会评分并记录各科目的学习情况。

### 4. 重点复习薄弱环节
系统会分析用户的薄弱环节，并生成针对性的练习题。

---

## 问题类型

| 类型 | 格式 | 适用场景 |
|------|--------|----------|
| 选择题 | 4 个选项，1 个正确答案 | 适用于快速评估和认证考试 |
| 多选题 | 多个选项，选择多个正确答案 | 适用于复杂主题 |
| 判断题 | 需判断陈述是否正确 | 适用于快速复习 |
| 简答题 | 1-3 句回答 | 适用于定义和解释性内容 |
| 填空题 | 需填写空白处 | 适用于术语记忆 |
| 匹配题 | 选择对应的配对项 | 适用于考查知识点之间的关联 |
| 论述题 | 开放式回答 | 适用于深入理解 |

---

## 问题生成方式

- **从笔记生成问题**：```
User: "Generate 10 questions from these AWS S3 notes"
Agent: Creates mix of types, varying difficulty
```
- **按主题分类生成问题**：```
User: "5 hard questions on database normalization"
Agent: Generates challenging application questions
```
- **模拟考试题型**：```
User: "Make questions like the PMP exam"
Agent: Matches official format, question style, difficulty
```

---

## 练习环节

```
📝 Practice: AWS S3 (10 questions)

Q1/10 [Medium]
Which S3 storage class has the lowest cost for infrequently accessed data with millisecond retrieval?

A) S3 Standard
B) S3 Intelligent-Tiering
C) S3 Standard-IA ✓
D) S3 Glacier

Your answer: _
```
用户完成练习后：
```
✅ Correct!

S3 Standard-IA is designed for infrequently accessed data 
but requires rapid access when needed. Glacier has lower 
cost but retrieval takes minutes to hours.

[Next] [Skip] [End session]
```

---

## 数据存储

```
~/exams/
├── {subject}/
│   ├── questions.jsonl    # Question bank
│   ├── sessions.jsonl     # Practice history
│   ├── performance.json   # Stats by topic
│   └── flashcards.json    # Generated cards
```

---

## 学习计划制定

```
"Create a study schedule — exam in 2 weeks, 3 hours/day available"
"Summarize chapter 5 focusing on what's likely to be on the exam"
"Make a concept map for [topic]"
"Generate a 1-page quick review sheet for [subject]"
"Remind me to study at 7pm daily" (uses cron)
```

---

## 命令说明

```
"Generate 20 questions from [material]"
"Quiz me on [topic]"
"Start a timed simulation (50 questions, 60 minutes)"
"Show my weak areas"
"Create flashcards for [topic]"
"Review mistakes from last session"
"Grade my essay answer and suggest improvements"
```

---

### 当前学习主题
（此处列出用户正在学习的主题）

### 学习成绩总结
（整体学习情况与趋势分析）

### 需要重点复习的领域
（需要加强练习的主题）