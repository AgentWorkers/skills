---
name: Coding
slug: coding
version: 1.0.2
description: 根据用户的明确反馈来了解其编程偏好。初始状态为空，随着用户不断纠正错误并提供指导，系统会逐渐完善自身功能。
changelog: Replace vague observe/detect with explicit feedback learning, require user confirmation before storing preferences
metadata: {"clawdbot":{"emoji":"💻","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 该技能的学习方式

该技能仅通过以下方式了解您的偏好：
- **明确的反馈**：例如 “实际上，我更喜欢X而不是Y”。
- **直接的指令**：例如 “始终使用snake_case命名规则”。
- **重复的请求**：如果您多次请求相同的内容，该技能会记录下来。

该技能绝对不会：
- 读取您的项目文件来推断您的偏好；
- 在您不知情的情况下观察您的行为；
- 存储您未明确同意的数据。

## 偏好信息的存储

您的偏好信息存储在 `~/coding/memory.md` 文件中。该文件会在您首次使用该技能时自动生成。

```
~/coding/
├── memory.md      # Active preferences (≤100 lines)
└── history.md     # Archived old preferences
```

**创建该文件的方法：** `mkdir -p ~/coding`

## 偏好信息的格式

```markdown
# Coding Memory

## Stack
- python: prefer 3.11+
- js: use TypeScript always

## Style
- naming: snake_case for Python, camelCase for JS
- imports: absolute over relative

## Structure
- tests: same folder as code, not separate /tests

## Never
- var in JavaScript
- print debugging in production
```

## 偏好信息的添加流程

1. **用户纠正输出结果** → 该技能会询问：“我应该记住这个偏好设置吗？”
2. **用户确认** → 该技能会将偏好信息添加到 `~/coding/memory.md` 文件中。
3. **用户可以查看自己的偏好设置** → 通过 “Show my coding preferences” 功能可以查看当前的偏好设置列表。

任何偏好信息在未经用户明确确认的情况下都不会被存储。

## 规则

- 每条偏好信息的描述长度应控制在5个单词以内。
- 在添加任何偏好信息之前，必须先得到用户的确认。
- 请参考 `dimensions.md` 文件以确定偏好信息的分类。
- 请参考 `criteria.md` 文件来决定何时添加新的偏好信息。
- `memory.md` 文件中的内容不得超过100行。
- 旧有的偏好设置会被自动归档到 `history.md` 文件中。

## 会话开始时的处理流程

1. 如果 `~/coding/memory.md` 文件存在，会加载该文件。
2. 将存储的偏好信息应用到系统的响应中。
3. 如果文件不存在，则系统会以默认设置开始运行。

## 辅助文件

| 文件名 | 用途 |
|------|---------|
| `dimensions.md` | 用于记录偏好信息的分类 |
| `criteria.md` | 用于确定何时建议添加新的偏好设置 |