---
name: progressive-memory
description: 用于实现“渐进式内存（Progressive Memory）”模式的元技能。该技能会将复杂的细节数据卸载到索引化的子文件中，从而保持主界面（上下文窗口）的简洁性。
---

# 进阶记忆技能（Progressive Memory Skill）

这是一种用于规范AI代理“渐进式记忆”（Progressive Memory）模式的元技能。

**问题**：`MEMORY.md` 文件会无限增长，消耗大量上下文信息（context tokens），导致代理因信息过载而难以理解实际情况。
**解决方案**：将 `MEMORY.md` 作为轻量级的**索引**文件使用，将复杂的细节（如日志、列表、配置文件等）存储到 `memory/topic.md` 中。只有当索引指出某个文件相关时，代理才会读取该文件。

## 工具

### memorize
将内容保存到子文件中，并自动在 `MEMORY.md` 中创建相应的索引。

```bash
node skills/progressive-memory/index.js memorize "Visual Identity" "White hair, red eyes..."
```

- 创建/更新 `memory/visual_identity.md` 文件。
- 在 `MEMORY.md` 中添加条目：“- **视觉标识（Visual Identity）**：参见 `memory/visual_identity.md`”。

### recall
读取特定的记忆主题文件。

```bash
node skills/progressive-memory/index.js recall "Visual Identity"
```

## 最佳实践

1. **先创建索引**：在向 `MEMORY.md` 中添加50行内容之前，先思考“这个信息每一轮都需要使用吗？”如果不需要，就使用渐进式记忆模式。
2. **命名规范**：使用清晰、易于搜索的文件名（例如 `suno_presets`、`project_alpha_specs`）。
3. **提供上下文说明**：`MEMORY.md` 中的索引条目应包含简短的描述，以便代理明白为什么要读取该文件。