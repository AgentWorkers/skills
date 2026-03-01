---
name: openclaw-todo
description: OpenClaw插件为markdown格式的TODO.md文件提供了TODO相关的命令。
---
# openclaw-todo

该插件用于管理本地的 Markdown 待办事项列表（默认路径为 `~/.openclaw/workspace/TODO.md`）。

## 命令

- `/todo-list` - 显示所有待办事项（过期的待办事项会优先显示）
- `/todo-add <text>` - 添加新的待办事项（支持 `@due(YYYY-MM-DD)`、`#tag`、`!priority` 标签）
- `/todo-done <index>` - 将指定的待办事项标记为已完成（索引来自 `/todo-list`）
- `/todo-edit <index> <new text>` - 编辑指定待办事项的文本内容
- `/todo-remove <index>` - 完全删除指定的待办事项
- `/todo-search <query>` - 根据文本、`#tag`、`!priority`、`@due`、`@overdue` 或 `@today` 条件搜索待办事项

## 内联标记

- **标签：** `#tag-name` - 用于对待办事项进行分类（例如：`#dev`、`#ops`）
- **优先级：** `!high`、`!medium`、`!low` - 用于设置待办事项的紧急程度
- **截止日期：** `@due(YYYY-MM-DD)` - 用于设置待办事项的截止日期；过期的待办事项会优先显示

## 安装

```bash
clawhub install openclaw-todo
```

## 注意事项

- 该插件适用于公共仓库（无需使用任何敏感信息）。
- 你可以通过本地 `openclaw.json` 文件中的插件配置来修改文件路径。