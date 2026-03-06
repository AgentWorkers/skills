---
name: autonomous-tasks
description: "**自主驱动的AI助手**：能够读取用户设定的目标，生成相应的任务，执行这些任务，并记录执行过程中的进度。  
**相关关键词**：创建目标（Create Goal）、新目标（New Goal）、设定目标（Set Goal）、运行目标（Run Goal）。"
metadata:
  version: 10.2.0
---
# 自动化任务

> 读取目标 → 生成任务 → 执行 → 记录日志 → 停止

你是一个自主运行的 AI 工作器。每次被唤醒后，会执行一轮任务，然后停止。

所有用户数据都存储在 `agents/` 目录中（相对于这个 SKILL.md 文件的目录）。这些数据在技能更新过程中会被保留（只有 `SKILL.md` 和 `_meta.json` 会被覆盖）。

## 工作流程

### 0. 初始化（仅首次执行）

如果 `agents/` 目录不存在（相对于这个 SKILL.md 文件的目录）：

1. 向用户询问他们的目标
2. 读取 `assets/templates.md` 并在 `agents/` 目录中创建所有必要的文件
3. **强烈建议** 用户设置定时执行任务：
   ```
   openclaw cron add --name "autonomous-tasks" --message "run autonomous tasks" --every 1h
   ```
4. **立即停止**。不要继续执行后续步骤。等待下一次唤醒。

### 1. 读取目标

从 `agents/` 目录中读取以下文件（相对于这个 SKILL.md 文件的目录）：

- `agents/AUTONOMOUS.md` — 长期目标 + 当前待办事项
- `agents/memory/backlog.md` — 待办事项列表
- `agents/memory/tasks.md` — 上次运行未完成的任务

**如果当前待办事项为空**，检查里程碑：

1. 如果有未完成的里程碑 `[ ]`：选取下一个里程碑，将其分解为具体的待办事项，并写入 `AUTONOMOUS.md` 的“当前待办事项”部分，然后继续执行
2. 如果所有里程碑都已完成：提示用户设置新的目标。根据项目背景提供 2-3 个示例方向。用户设置新目标后，清理旧的数据：
   - 从 `AUTONOMOUS.md` 中删除已完成的里程碑
   - 清空 `memory/backlog.md`
   - 清空 `memory/tasks-log.md`
   **不要随意生成新的目标**。如果用户没有响应，停止并等待下一次唤醒。

### 2. 生成任务

**如果 `memory/tasks.md` 中有未完成的任务**，则继续执行任务，无需重新生成任务。

**如果没有未完成的任务**，则从待办事项列表中生成新的任务，并写入 `memory/tasks.md`：

```markdown
- [ ] task description
- [ ] task description
```

**规则**：
- 首先优先处理 `AUTONOMOUS.md` 中的当前待办事项，然后处理 `backlog.md` 中的任务
- 每个任务都应具有明确的输出结果
- **所有输出结果都应保存在当前工作目录中**，切勿保存到技能目录或 `agents/` 目录中
- 确保不同目标和里程碑的输出结果分开保存

### 3. 执行任务

按照 `memory/tasks.md` 中的顺序执行任务。

将任务标记为“进行中”：
```markdown
- [~] task description
```

将任务标记为“已完成”：
```markdown
- [x] task description → output path
```

如果任务执行失败，标记为“失败”并跳过该任务：
```markdown
- [!] task description → failure reason
```

不要重试失败的任务。

如果在执行过程中发现新的想法或后续工作，但这些内容不属于当前任务的范畴，应将其添加到 `memory/backlog.md` 中，而不是立即处理。

### 4. 归档

当 `memory/tasks.md` 中的所有任务都被标记为“[x]”或“[!]”时：

1. 将任务结果追加到 `memory/tasks-log.md` 中：
```
- ✅ description → output path (YYYY-MM-DD)
- ❌ description → failure reason (YYYY-MM-DD)
```

2. 清空 `memory/tasks.md`（保留标题）
3. 从 `AUTONOMOUS.md` 或 `backlog.md` 中删除已完成的任务
4. 如果所有当前待办事项都已完成，将对应的里程碑标记为“[x]”
5. 当 `tasks-log.md` 的内容超过 50 行时，仅保留最近的 30 行

### 5. 停止

完成归档后，**立即停止**。不要生成新的任务。等待下一次唤醒。

## 参考资料

在开始执行之前，请阅读 `assets/rules.md` 文件（位于与这个 SKILL.md 相同的目录中），以了解禁止的操作、核心原则和文件结构。