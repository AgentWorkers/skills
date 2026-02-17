---
name: duely
description: >
  **从命令行跟踪重复性的维护任务**  
  适用于安排、检查以及记录定期执行的任务（如备份、审查或任何重复性的工作）。该工具能够显示逾期未完成的任务，并维护详细的执行日志。
metadata:
  openclaw:
    emoji: "🔁"
    os: ["darwin"]
    requires:
      bins: ["duely"]
    install:
      - id: brew
        kind: brew
        formula: halbotley/tap/duely
        bins: ["duely"]
        label: "Install duely (brew)"
---
# duely

这是一个用于跟踪重复性维护任务的命令行工具（CLI）。它可以帮你了解哪些任务即将到期，标记任务是否已完成，并记录执行日志。

## 为什么选择 duely？

- **简单的重复性任务管理**：无需使用日历来管理维护任务。
- **逾期提醒**：让你知道哪些任务被你拖延了。
- **执行日志**：随时了解任务上次执行的时间。

## 安装

```bash
brew tap halbotley/tap
brew install duely
```

## 命令

### 添加一个重复性任务

```bash
duely add backups --name "Database backups" --every 1d
duely add vault-review --name "Vault review" --every 3d
duely add oil-change --name "Oil change" --every 90d --start 2025-06-01
```

可选的时间间隔：`12h`（12小时）、`1d`（1天）、`3d`（3天）、`1w`（1周）、`30d`（30天）等。

### 列出所有任务

```bash
duely list
```

### 显示当前到期的任务

```bash
duely due
```

会用 ⚠️ 标记过期的任务。

### 将任务标记为已完成

```bash
duely run backups
duely run backups --notes "Full backup completed"
```

### 跳过某个任务（重新安排任务时间，但不执行）

```bash
duely skip vault-review
duely skip vault-review --reason "On vacation"
```

### 查看执行日志

```bash
duely log
```

### 删除一个任务

```bash
duely remove old-task
```

## 与代理的集成

duely 可以与代理的心跳检测机制或 cron 触发器很好地配合使用：

```bash
# Check for due tasks and act on them
duely due
# After completing the task:
duely run <task-id> --notes "Completed by agent"
```

## 注意事项：

- 任务 ID 必须为小写字母，且不能包含空格。
- 如果未指定，`--start` 参数默认设置为“现在”。
- `--every` 参数可以接受小时（h）、天（d）和周（w）作为时间单位。
- 数据存储在本地目录 `~/.duely/` 中。