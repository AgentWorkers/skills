---
name: context7
description: |
  Fetch up-to-date library documentation via Context7 API. Use PROACTIVELY when:
  (1) Working with ANY external library (React, Next.js, Supabase, etc.)
  (2) User asks about library APIs, patterns, or best practices
  (3) Implementing features that rely on third-party packages
  (4) Debugging library-specific issues
  (5) Need current documentation beyond training data cutoff
  Always prefer this over guessing library APIs or using outdated knowledge.
---

# Context7 文档获取器

通过 Context7 API 获取当前库的文档信息。

## 工作流程

### 1. 搜索库

```bash
python3 ~/.claude/skills/context7/scripts/context7.py search "<library-name>"
```

示例：
```bash
python3 ~/.claude/skills/context7/scripts/context7.py search "next.js"
```

返回库的元数据，其中包含步骤 2 所需的 `id` 字段。

### 2. 获取文档内容

```bash
python3 ~/.claude/skills/context7/scripts/context7.py context "<library-id>" "<query>"
```

示例：
```bash
python3 ~/.claude/skills/context7/scripts/context7.py context "/vercel/next.js" "app router middleware"
```

选项：
- `--type txt|md` - 输出格式（默认：txt）
- `--tokens N` - 限制响应中的令牌数量

## 快速参考

| 任务 | 命令 |
|------|---------|
| 查找 React 文档 | `search "react"` |
| 获取 React 钩子信息 | `context "/facebook/react" "useEffect cleanup"` |
| 查找 Supabase | `search "supabase"` |
| 获取 Supabase 认证信息 | `context "/supabase/supabase" "authentication row level security"` |

## 使用场景

- 在实现任何依赖库的功能之前
- 当不确定当前 API 的签名时
- 了解特定库版本的行为
- 验证最佳实践和模式