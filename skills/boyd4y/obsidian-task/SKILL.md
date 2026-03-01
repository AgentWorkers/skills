---
name: obsidian-task
description: 通过 `obsidian-cli` 管理 Obsidian 任务。可以在终端中列出、切换、创建和更新任务。
compatibility: darwin,linux
metadata:
  version: 1.0.1
  requires:
    bins:
      - obsidian
---
# Obsidian 任务管理

使用官方的 Obsidian CLI 在您的 Obsidian 文档库中管理任务。

## 所需依赖项

| 依赖项 | 是否必需 | 说明 |
|------------|----------|-------------|
| `obsidian` | 是 | Obsidian CLI（需通过 Obsidian 设置进行注册） |
| Obsidian 1.12+ | 是 | 使用 CLI 需要 Catalyst 许可证 |

### 检查依赖项

```bash
# Check obsidian CLI availability
obsidian version
```

## 先决条件

- 需要 Obsidian 1.12+ 及 Catalyst 许可证
- 在 Obsidian 设置中，进入“General” → “Command line interface”并启用该功能
- 按提示注册 `obsidian` 命令
- 重启终端或执行 `source ~/.zprofile`（macOS 用户）
- **注意：** Obsidian 必须正在运行，CLI 才能正常使用

测试命令：`obsidian version`

## 使用方法

```bash
/obsidian-task [command] [options]
```

## 命令

| 命令 | 说明 |
|---------|-------------|
| （无） | 显示帮助信息及可用命令 |

## 选项

| 选项 | 说明 |
|--------|-------------|
| `--help` | 显示帮助信息 |

## 示例

```bash
# List tasks
/obsidian-task tasks file=projects/myproject/todo verbose

# Toggle task on line 2
/obsidian-task task file=projects/myproject/todo line=2 toggle

# Mark task as done
/obsidian-task task file=projects/myproject/todo line=2 done

# Mark task as todo (undo completion)
/obsidian-task task file=projects/myproject/todo line=2 todo

# Create new task
/obsidian-task append file=projects/myproject/todo content="- [ ] task name"
```

## 原始 CLI 命令

```bash
# List tasks (shows line numbers and status)
obsidian tasks file=<project_slug>/todo verbose

# Sample output:
# projects/<project_slug>/TODO.md
# 2	- [ ] 未完成的任务
# 3	- [x] 已完成的任务

# Update tasks
obsidian task file=<project_slug>/todo line=2 toggle
obsidian task file=<project_slug>/todo line=2 done
obsidian task file=<project_slug>/todo line=2 todo

# Create new task (via append)
obsidian append file=<project_slug>/todo content="- [ ] task name"
```