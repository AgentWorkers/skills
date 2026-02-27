---
name: openclaw-todo
description: OpenClaw插件为Markdown格式的TODO.md文件提供了TODO相关的命令。
---
# openclaw-todo

该插件用于管理本地的 Markdown 待办事项列表（默认路径：`~/.openclaw/workspace/TODO.md`）。

## 命令

- `/todo-list` — 显示所有未完成的待办事项
- `/todo-add <text>` — 添加一个新的待办事项
- `/todo-done <index>` — 将指定的待办事项标记为已完成（`<index>` 为 `/todo-list` 中的待办事项索引）

## 安装

```bash
clawhub install openclaw-todo
```

## 注意事项

- 该插件适用于公共仓库（无需任何敏感信息）。
- 你可以通过本地 `openclaw.json` 文件中的插件配置来自定义文件路径。