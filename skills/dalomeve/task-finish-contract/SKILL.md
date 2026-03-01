---
name: task-finish-contract
description: 通过明确的目标（Goal）、进度（Progress）和下一步操作（Next）状态来强制任务完成。防止任务在执行过程中出现停滞，并确保任务完成过程有据可查（即完成情况有明确的记录和验证）。
---
# 任务完成规范

为防止任务在运行过程中突然停止，每个任务都必须以明确的状态和相应的证据作为结束标志。

## 问题

代理在执行任务时经常会出现以下问题：
- 在没有解释的情况下突然停止任务
- 只输出计划而未实际执行
- 缺乏明确的完成标准
- 缺少完成任务所需的证据文件

## 工作流程

### 1. 状态输出（每个关键步骤）

```markdown
**Goal**: What finished looks like
**Progress**: What has been done
**Next**: One concrete action executing now
```

### 2. 完成证明格式

对于包含两个以上步骤的任务，需要提供以下证明：

```markdown
**DONE_CHECKLIST**:
- [ ] Item 1 completed
- [ ] Item 2 completed

**EVIDENCE**:
- Executed: command/action summary
- Artifact: path/URL/id
- Verified: check command result

**NEXT_AUTONOMOUS_STEP**:
- One follow-up that runs without user input
```

### 3. 防止任务停滞规则

- 仅用于规划阶段的回复：最多允许1条
- 下一条回复必须包含实际执行的证据
- 绝不能以“我现在将……”这样的表述结束，而没有任何工具执行的结果

## 可执行的完成标准

| 标准 | 验证方式 |
|----------|-------------|
| 目标已明确 | `Select-String "Goal" memory/{date}.md` 的内容与目标一致 |
| 进度已记录 | `Select-String "Progress" memory/{date}.md` 的内容显示了任务进度 |
| 下一步行动已确定 | `Select-String "Next" memory/{date}.md` 的内容说明了下一步的具体操作 |
| 有证据文件 | 相关证据文件（artifact）的路径或URL存在 |
| 无未解决的标记 | 使用 `Select-String "TODO|PENDING|TBD"` 命令查询时，不应返回任何结果 |

## 隐私/安全要求

- 完成证据中不得包含任何敏感数据
- 证据文件的路径应使用相对路径或工作区路径
- 任务日志中不得包含任何凭据信息

## 自动触发条件

在以下情况下需要执行此规范：
- 开始任何多步骤任务时
- 任务中断后恢复执行时
- 将任务交接给其他代理时

---

**开始的任务必须完成，并用证据来证明其完成情况。**