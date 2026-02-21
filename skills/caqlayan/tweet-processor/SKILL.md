# 推文处理技能

从推文链接中提取有价值的见解，并将其分类整理成结构化的笔记。

## 使用方法

当用户发送推文链接时，系统会自动执行以下操作：
1. 访问该推文
2. 提取关键信息（工具、技术、人物、学习内容）
3. 将这些信息分类到相应的文件中（如 `tweet-notes/tools.md`、`tweet-notes/tech.md`、`tweet-notes/design.md`、`tweet-notes/people.md`、`tweet-notes/misc.md`）
4. 以规范的格式保存这些信息

## 输入

- 推文链接（可以是任何形式的链接，例如 `x.com` 或 `twitter.com`）

## 输出

输出结果会被保存到以下文件中：
- `tweet-notes/tools.md` — 涉及的软件、服务、API
- `tweet-notes/tech.md` — 开发技术、工作流程
- `tweet-notes/design.md` — 用户界面/用户体验方面的见解
- `tweet-notes/people.md` — 需要关注的用户账号
- `tweet-notes/misc.md` — 其他有价值的见解

## 格式

```markdown
## [Brief Title]
**Date:** YYYY-MM-DD
**URL:** [tweet URL]
**Key takeaway:** [What matters]
**Why it matters:** [Brief context]

---
```

## 规则：
- 仅保留真正有用的信息
- 忽略无关的内容和冗余信息
- 如果某个见解适用于多个类别，可以将其分录到多个文件中
- 必须包含原始推文的链接
- 每条笔记都需要标注日期