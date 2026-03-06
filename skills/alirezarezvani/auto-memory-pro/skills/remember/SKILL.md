---
name: remember
description: "**将重要知识显式保存到自动记忆系统中，并附带时间戳和上下文信息。**  
**适用于那些过于重要、无法依赖自动捕获机制的情况。**"
command: /si:remember
---
# /si:remember — 显式保存知识

当某些信息足够重要，以至于你不想依赖Claude自动识别时，可以使用此命令将其显式地保存到自动记忆系统中。

## 使用方法

```
/si:remember <what to remember>
/si:remember "This project's CI requires Node 20 LTS — v22 breaks the build"
/si:remember "The /api/auth endpoint uses a custom JWT library, not passport"
/si:remember "Reza prefers explicit error handling over try-catch-all patterns"
```

## 适用场景

| 情况 | 例子 |
|-----------|---------|
| 艰苦获得的调试线索 | “/api/upload上的CORS错误是由CDN引起的，而非后端问题” |
| 未在CLAUDE.md中记录的项目规范 | “我们在src/components/目录中使用了‘barrel exports’模式” |
| 与特定工具相关的注意事项 | “Jest需要`--forceExit`标志，否则会在数据库测试中卡住” |
| 关于架构的选择 | “我们选择了Drizzle而非Prisma来实现类型安全的SQL” |
| 希望Claude了解的偏好设置 | “不要为显而易见的代码添加注释” |

## 工作流程

### 第1步：解析知识

从用户输入中提取以下信息：
- **具体内容**：需要保存的事实或模式
- **重要性**：相关背景信息（如果有的话）
- **适用范围**：是仅适用于当前项目，还是全局通用？

### 第2步：检查是否存在重复条目

```bash
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"
grep -ni "<keywords>" "$MEMORY_DIR/MEMORY.md" 2>/dev/null
```

如果已经存在类似的条目：
- 显示给用户，并询问：“是更新现有条目，还是新建一条？”

### 第3步：将信息写入MEMORY.md

将新信息添加到`MEMORY.md`文件的末尾：

```markdown
- {{concise fact or pattern}}
```

条目应保持简洁——尽可能用一行表达。自动记忆条目不需要时间戳、ID或元数据，它们只是笔记，而非数据库记录。

如果`MEMORY.md`文件的长度超过180行，应提醒用户：

```
⚠️ MEMORY.md is at {{n}}/200 lines. Consider running /si:review to free space.
```

### 第4步：建议将条目提升为规则

如果这些知识具有普遍性（即“必须/禁止这样做”或属于项目规范），可以考虑将其提升为规则：

```
💡 This sounds like it could be a CLAUDE.md rule rather than a memory entry.
   Rules are enforced with higher priority. Want to /si:promote it instead?
```

### 第5步：确认信息准确性

```
✅ Saved to auto-memory

  "{{entry}}"

  MEMORY.md: {{n}}/200 lines
  Claude will see this at the start of every session in this project.
```

## 不适用的情况

- **临时性信息**：使用会话内存或在对话中直接告知Claude。
- **强制性的规则**：使用`/si:promote`命令将信息直接写入CLAUDE.md。
- **跨项目通用规则**：请将信息保存到`~/.claude/CLAUDE.md`中。
- **敏感数据**：切勿在内存文件中存储凭证、令牌或机密信息。

## 提示

- 保持简洁——一行比一段话更有效。
- 包括具体的命令或值，而不仅仅是概念。
  - ✅ “使用`pnpm build`进行构建，使用`pnpm test:e2e`进行测试。”
  - ❌ “该项目使用pnpm进行构建和测试。”
- 如果同一条信息被多次提及，建议将其提升为CLAUDE.md中的规则。