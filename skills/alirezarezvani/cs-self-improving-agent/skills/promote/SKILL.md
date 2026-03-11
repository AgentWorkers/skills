---
name: "promote"
description: "将经过验证的模式从 `auto-memory.md` 文件中导出到 `CLAUDE.md` 或 `.claude/rules/` 文件中，以便进行永久性应用。"
command: /si:promote
---
# /si:promote — 将经验性知识转化为规则

将经过验证的模式从 Claude 的自动记忆系统（auto-memory）中提取出来，纳入项目的规则系统中，使其成为具有强制性的指令，而不再只是背景信息。

## 使用方法

```
/si:promote <pattern description>                    # Auto-detect best target
/si:promote <pattern> --target claude.md             # Promote to CLAUDE.md
/si:promote <pattern> --target rules/testing.md      # Promote to scoped rule
/si:promote <pattern> --target rules/api.md --paths "src/api/**/*.ts"  # Scoped with paths
```

## 工作流程

### 第一步：理解模式

解析用户的描述。如果描述不够清晰，可以提出一个澄清性问题：
- “Claude 应该遵循什么具体行为？”
- “这适用于所有文件还是特定路径？”

### 第二步：在自动记忆系统中查找匹配的模式

```bash
# Search MEMORY.md for related entries
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"
grep -ni "<keywords>" "$MEMORY_DIR/MEMORY.md"
```

展示匹配的条目，并确认它们是否符合用户的意图。

### 第三步：确定目标文件或目录

| 模式适用范围 | 目标文件或目录 | 例子 |
|---|---|---|
| 适用于整个项目 | `./CLAUDE.md` | “使用 pnpm，而不是 npm” |
| 适用于特定文件类型 | `.claude/rules/<主题>.md` | “API 处理程序需要验证” |
| 适用于所有项目 | `~/.claude/CLAUDE.md` | “优先使用显式的错误处理方式” |

如果用户没有指定目标文件或目录，可以根据模式适用范围进行推荐。

### 第四步：将经验性知识转化为简洁的规则

将自动记忆系统中的信息转化为 CLAUDE.md 的规则格式：

**转换前**（MEMORY.md — 描述性格式）：
> 该项目使用 pnpm 作为工作空间。当我尝试使用 npm install 时出现了错误。锁定文件是 pnpm-lock.yaml。因此必须使用 pnpm install 来安装依赖项。

**转换后**（CLAUDE.md — 规范性格式）：
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm). Use `pnpm install`.
```

**规则编写原则：**
- 尽量每条规则只占一行
- 使用祈使句式（例如：“使用 X”，“始终使用 Y”，“永远不要使用 Z”）
- 包括具体的命令或示例，而不仅仅是概念
- 不要添加背景信息，只提供指令内容

### 第五步：将规则写入目标文件

**对于 CLAUDE.md：**
1. 阅读现有的 CLAUDE.md 文件
2. 找到合适的部分（如果不存在则创建一个新的部分）
3. 将新规则添加到相应的标题下
4. 如果规则内容超过 200 行，建议将其放入 `.claude/rules/` 目录中

**对于 `.claude/rules/` 目录：**
1. 如果文件还不存在，则创建该文件
2. 如果规则有适用范围，请添加包含 `paths` 的 YAML 标头信息
3. 编写规则内容

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "tests/api/**/*"
---

# API Development Rules

- All endpoints must validate input with Zod schemas
- Use `ApiError` class for error responses (not raw Error)
- Include OpenAPI JSDoc comments on handler functions
```

### 第六步：清理自动记忆系统

将规则添加到 CLAUDE.md 或 `.claude/rules/` 后，删除或标记 MEMORY.md 中的原始条目：

```bash
# Show what will be removed
grep -n "<pattern>" "$MEMORY_DIR/MEMORY.md"
```

请用户确认是否删除该条目。然后编辑 MEMORY.md 以移除该条目，从而为新的经验性知识腾出空间。

### 第七步：确认规则的有效性

```
✅ Promoted to {{target}}

Rule: "{{distilled rule}}"
Source: MEMORY.md line {{n}} (removed)
MEMORY.md: {{lines}}/200 lines remaining

The pattern is now an enforced instruction. Claude will follow it in all future sessions.
```

## 规则推广决策指南

### 何时推广：
- 某个模式在自动记忆系统中出现超过 3 次
- 你多次提醒 Claude 遵循该规则
- 这是所有贡献者都应该了解的项目规范
- 该规则能够防止重复出现错误

### 何时不要推广：
- 这只是一个临时性的调试记录（保留其在自动记忆系统中）
- 这是特定会话的上下文信息（会话记忆系统可以处理这类信息）
- 该规则可能会很快发生变化（例如，在项目迁移期间）
- 该规则已经被现有的规则覆盖

### CLAUDE.md 与 `.claude/rules/` 的区别

| 使用 CLAUDE.md 的场景 | 使用 `.claude/rules/` 的场景 |
|---|---|
| 全局项目规则 | 针对特定文件类型的规则 |
| 构建命令 | 测试规范 |
| 架构决策 | API 设计规则 |
| 团队规范 | 某个框架特有的注意事项 |

## 提示：
- 保持 CLAUDE.md 的内容在 200 行以内——超过 200 行的建议将其放入 `.claude/rules/` 目录
- 每条规则占一行更易于维护
- 包括具体的命令或示例，而不仅仅是概念
- 每季度审查一次推广的规则——移除不再相关的规则