---
name: rejection-logger
description: 记录代理评估后决定不执行的选项、选择或提示。无论是在跳过某个任务、拒绝某种方法，还是选择另一种方法时，都应使用此功能，以便清晰地展示您的决策过程。
---
# 拒绝处理日志（Rejection Logger）

透明度不仅仅意味着展示你做了什么，更重要的是解释你没有做什么。这项技能有助于你记录那些被拒绝的解决方案或请求。

## 核心工作流程

### 1. 识别拒绝情况
- 当你在评估多种解决问题的方法后选择其中一种时，
- 或者当你判断用户的请求存在安全风险或超出了你的职责范围时，
- 需要记录下这一情况。

### 2. 记录日志
将相关信息添加到 `.learnings/REJECTIONS.md` 文件中（如果文件不存在，请先创建它）：

```markdown
## [REJ-YYYYMMDD-XXX] <short_title>

**Timestamp**: ISO-8601
**Target**: <What was requested or considered>
**Decision**: REJECTED
**Reason**: <Why it was rejected (e.g., safety, complexity, better alternative)>
**Alternative**: <What was done instead>
```

## 使用场景
- 当用户提出请求而你回答“不行”或“我无法满足”时，
- 当你在两个工具之间进行选择时，
- 当你重构代码并决定不使用某个特定的库时，

## 好处
- **审计追踪**：其他人可以了解你的内部决策过程。
- **建立信任**：记录拒绝情况可以证明你是经过深思熟虑的，而不仅仅是随意猜测。
- **自我改进**：回顾这些拒绝记录有助于你更清晰地界定自己的决策边界。