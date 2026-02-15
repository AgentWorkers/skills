---
name: "Coding"
version: "1.0.1"
changelog: "Migrate to external memory storage at ~/coding/"
description: "它会自动学习你的技术栈、编程风格以及个人偏好。初始状态下是空的，但随着每个项目的完成而逐渐丰富起来。"
---

## 自适应代码偏好设置

此功能会自动进行优化和更新。它会观察用户的操作，识别使用模式，并记录用户的偏好设置。

**规则：**
- 从用户的操作中识别使用模式（而不仅仅是用户的明确请求）
- 在用户连续做出相同选择两次以上后，确认这些偏好设置
- 每条偏好设置的信息应保持极简（最多5个单词）
- 查看 `dimensions.md` 文件以确定偏好设置的分类，以及查看 `criteria.md` 文件以确定何时需要添加新的偏好设置

---

## 内存存储

用户的偏好设置保存在 `~/coding/memory.md` 文件中。激活该功能时会读取这些设置。

**结构：**
```
~/coding/
├── memory.md      # Active preferences (load always)
└── history.md     # Old/archived preferences
```

**规则：**
- 在功能启动时始终加载 `memory.md` 文件
- 确保 `memory.md` 文件的行数不超过100行
- 将旧的偏好设置记录归档到 `history.md` 文件中

**`memory.md` 文件的格式：**
```markdown
# Coding Memory

## Stack
- context: tech

## Style
- rule or thing: preference

## Structure
- project organization preference

## Never
- thing user rejected

---
*Last updated: YYYY-MM-DD*
```

**首次使用时：** 如果 `memory.md` 文件不存在，请创建该文件。

---

*如果 `memory.md` 文件为空，说明用户尚未设置任何偏好设置。请继续观察用户的操作并逐步填写相关信息。*