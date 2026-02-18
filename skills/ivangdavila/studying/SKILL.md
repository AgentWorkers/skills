---
name: "Studying"
version: "1.0.1"
changelog: "Preferences now persist across skill updates"
description: "它会自动学习你的学习习惯，以帮助你取得学术上的成功。它会根据你的个人情况调整学习方法、学习时间以及学习材料。"
---
## 自适应学习偏好设置

该功能会自动进行优化。用户的偏好设置会保存在 `~/studying/memory.md` 文件中。首次使用时需要手动创建这些设置：

```markdown
## Techniques
<!-- Study methods that work. Format: "method: context (level)" -->
<!-- Examples: Active recall for facts (confirmed), Mind maps for concepts (pattern) -->

## Schedule
<!-- When/how they study best. Format: "preference (level)" -->
<!-- Examples: Morning sessions (confirmed), 25min blocks (pattern) -->

## Materials
<!-- Preferred formats. Format: "type: context (level)" -->
<!-- Examples: Video lectures for intro (confirmed), Textbooks for deep (pattern) -->

## Exams
<!-- Exam prep patterns. Format: "pattern (level)" -->
<!-- Examples: Past papers week before (confirmed), Cramming doesn't work (locked) -->

## Never
<!-- Approaches that fail. Format: "approach (level)" -->
<!-- Examples: Rereading (confirmed), Highlighting only (pattern) -->
```

*如果某个部分为空，表示用户尚未设置任何偏好。请观察用户的学习行为并填写相应的内容。偏好设置分为三个等级：**模式（Pattern）** → **确认（Confirmed）** → **锁定（Locked）***

**规则：**
- 通过分析哪些学习方法有效、哪些无效来识别用户的学习模式。
- 该功能主要适用于学术场景（如考试、课程、成绩管理等）。
- 需要连续收到两次或更多次相同的反馈后，才能确认用户的偏好设置。
- 请参考 `dimensions.md` 文件了解偏好设置的分类规则，以及 `criteria.md` 文件中的格式要求。