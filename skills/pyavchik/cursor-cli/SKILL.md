---
name: cursor-cli
description: 使用 Cursor 编辑器和 Cursor 代理来完成编码任务。
metadata: {"openclaw":{"requires":{"bins":["cursor","cursor-agent"]},"emoji":"⌨️","homepage":"https://cursor.com/docs/cli/overview"}}
---
# Cursor CLI 技能

使用此技能通过 Cursor 编辑器执行编码任务。

## 命令

### 1. 在 Cursor 中打开文件
```bash
cursor --goto file.py:line
```

### 2. 使用 Cursor Agent（AI 编码助手）
```bash
cursor-agent -p "your question" --mode=ask --output-format text
```

### 3. 查看文件之间的差异
```bash
cursor --diff file1.py file2.py
```

## 示例

**在特定行打开文件：**
```
cursor --goto conftest.py:180
```

**询问 Cursor AI：**
```
cursor-agent -p "Explain what recursion is" --mode=ask --output-format text
```

**审查代码：**
```
cursor-agent -p "Review this code for bugs" --output-format text
```

## 注意事项

- 尽可能在项目目录中运行该命令。
- 对于复杂的任务，Cursor Agent 可能需要 30 至 120 秒来完成。
- 使用 Cursor Pro 可以获得完整的 AI 功能。