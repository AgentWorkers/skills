---
name: zettelkasten
description: **Zettelkasten** – 一种结合人工智能功能的卡片式笔记记录系统
keywords: note-taking,knowledge-management,zettelkasten,ai,insights
metadata:
  openclaw:
    emoji: "📝"
    bins: ["python"]
    pip: []
    os:
      - darwin
      - linux
      - windows
    requires: []
---

# Zettelkasten卡片盒系统

## 产品描述
这是一个完整的Zettelkasten笔记记录方法实现，具备以下功能：
- 想法的捕捉与整理
- 人工智能生成的见解与建议
- 自动检测想法之间的关联
- 每日复习功能

## 使用方法

### 记录想法
```
Record Idea: [Your idea content here]
```

示例：
```
Record Idea: I found that meditating 10 minutes daily improves focus and sleep quality
```

## 主要功能
1. **想法捕捉**：自动生成带有元数据的结构化卡片
2. **人工智能见解**：提供扩展性的建议和研究方向
3. **关联检测**：发现不同想法之间的联系
4. **每日复习**：随机抽取卡片进行知识巩固

## 输出格式
```markdown
---
ID: [timestamp]
Tags: #tag1 #tag2 #tag3
Type: Flash
Date: [date]
---

## [Title]
[Content]

> AI Insight: [Generated insight]
```