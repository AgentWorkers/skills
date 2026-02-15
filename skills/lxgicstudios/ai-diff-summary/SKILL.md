---
name: diff-summary
description: 用简单的英语总结 Git 的差异（diffs）。
---

# 差异摘要（Diff Summary）

将混乱的 Git 差异信息转换为人类可读的摘要。非常适合用于 PR 描述和代码审查。

## 快速入门

```bash
npx ai-diff-summary
```

## 功能介绍

- 概述已暂存的更改内容
- 说明代码的具体功能，而不仅仅是哪些部分发生了变化
- 将相关的更改分组在一起
- 识别可能导致系统崩溃的更改（即“破坏性更改”）

## 使用示例

```bash
# Summarize staged changes
npx ai-diff-summary

# Summarize specific commit
npx ai-diff-summary --commit abc123

# Compare branches
npx ai-diff-summary --from main --to feature/auth

# Output as PR description
npx ai-diff-summary --format pr
```

## 输出示例

```markdown
## Summary
Added user authentication with JWT tokens

## Changes
- New login/logout endpoints in auth.ts
- JWT middleware for protected routes
- User model with password hashing
- Updated API docs

## Breaking Changes
- /api/users now requires authentication
```

## 系统要求

- 必须使用 Node.js 18 及以上版本。
- 需要配置 OPENAI_API_KEY。
- 该工具必须部署在 Git 仓库中。

## 许可证

MIT 许可证。永久免费使用。

---

**开发团队：LXGIC Studios**

- GitHub 仓库：[github.com/lxgicstudios/ai-diff-summary](https://github.com/lxgicstudios/ai-diff-summary)
- Twitter 账号：[@lxgicstudios](https://x.com/lxgicstudios)