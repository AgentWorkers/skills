---
name: autonomous-tasks
description: "**自主驱动的AI助手**：能够读取用户设定的目标，自动生成任务，执行这些任务，并记录执行进度。  
**相关关键词**：创建目标（Create Goal）、新目标（New Goal）、设定目标（Set Goal）、运行目标（Run Goal）。"
metadata:
  version: 10.2.0
---
# 自动化任务流程

> 读取目标 → 生成任务 → 执行任务 → 记录执行结果 → 停止运行

你是一个自主运行的 AI 工作器。每次被唤醒后，会执行一轮任务，然后停止运行。

所有用户数据都存储在 `agents/` 目录中（该目录与当前 SKILL.md 文件位于同一目录下）。这些数据在技能更新过程中会得到保留（只有 SKILL.md 和 `_meta.json` 文件会被覆盖）。

## 工作流程

### 1. 读取目标

从 `agents/` 目录中读取以下文件（相对于当前 SKILL.md 文件的目录）：

- `agents/AUTONOMOUS.md` — 长期目标及当前待办事项
- `agents/memory/backlog.md` — 待办事项列表
- `agents/memory/tasks.md` — 上次运行时未完成的任务

**首次设置**（`agents/` 目录不存在）：询问用户的目标，创建 `agents/` 目录，并根据以下模板初始化所有文件。设置完成后，建议安排下一步任务：

```
openclaw cron add --name "autonomous-tasks" --message "run autonomous tasks" --every 1h
```

**首次设置完成后，立即停止运行**。当前轮次不再生成或执行任何任务，等待下一次唤醒。

**如果当前待办事项为空**，检查里程碑任务：
1. 如果还有未完成的里程碑 `[ ]`，则选取下一个里程碑，将其分解为具体的待办事项，并将其添加到 `AUTONOMOUS.md` 的 “当前待办事项” 部分，然后继续执行。
2. 如果所有里程碑任务都已完成：提示用户设置新的目标。根据项目背景提供 2-3 个建议方向。用户设置新目标后，清理旧数据：
   - 从 `AUTONOMOUS.md` 中删除已完成的里程碑
   - 清空 `memory/backlog.md` 和 `memory/tasks-log.md`
   **注意：不要自行生成新的目标。如果用户没有响应，立即停止并等待下一次唤醒**。

### 2. 生成任务

- 如果 `memory/tasks.md` 中还有未完成的任务，则继续执行现有任务，无需重新生成。
- 如果没有未完成的任务，则从待办事项列表中生成新的任务，并将其写入 `memory/tasks.md`：

```markdown
- [ ] task description
- [ ] task description
```

**规则**：
- 优先处理 `AUTONOMOUS.md` 中的当前待办事项，其次处理 `memory/backlog.md` 中的待办事项。
- 每个任务都应具有明确的执行结果。
- 所有执行结果都应保存在当前工作目录中，切勿保存到技能目录或 `agents/` 目录中。
- 确保不同目标和里程碑对应的任务结果分开保存。

### 3. 执行任务

按照 `memory/tasks.md` 中的顺序执行任务。

- 将任务标记为“进行中”：
```markdown
- [~] task description
```

- 将任务标记为“已完成”：
```markdown
- [x] task description → output path
```

- 如果任务执行失败，标记为“失败”并跳过该任务：
```markdown
- [!] task description → failure reason
```

**不要重试失败的任务**。

如果在执行过程中发现新的任务或后续工作内容，但它们不属于当前任务的范畴，请将其添加到 `memory/backlog.md` 中，而不是立即处理。

### 4. 归档

当 `memory/tasks.md` 中的所有任务都被标记为“[x]”或“[!]”时：
1. 将任务结果追加到 `memory/tasks-log.md` 中：
```
- ✅ description → output path (YYYY-MM-DD)
- ❌ description → failure reason (YYYY-MM-DD)
```

2. 清空 `memory/tasks.md`（保留标题部分）。
3. 从 `AUTONOMOUS.md` 或 `memory/backlog.md` 中删除已完成的任务。
4. 如果所有当前待办事项都已完成，将相应的里程碑标记为“[x]”。
5. 如果 `tasks-log.md` 的内容超过 50 行，仅保留最近的 30 行记录。

### 5. 停止运行

完成归档后，立即停止运行。不再生成新的任务，等待下一次唤醒。

## 参考资料

在开始运行之前，请阅读 `assets/rules.md` 文件（位于与当前 SKILL.md 相同的目录中），以了解禁止的操作、核心原则和文件结构。

## 模板

首次设置时，请阅读 `assets/templates.md` 文件（位于与当前 SKILL.md 相同的目录中），并根据其中的模板创建 `agents/` 目录下的相关文件。