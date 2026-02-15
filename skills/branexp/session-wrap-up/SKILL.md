---
name: session-wrap-up
description: 在开始新的对话会话之前，先结束当前的对话会话。当用户说“结束对话”、“结束本次会话”或使用 `/session_wrap_up` 命令时，应执行此操作。该操作会将对话内容刷新到内存文件中，更新 PARA 笔记，提交更改，并提供会话的总结。
---

# 会话总结

本协议用于在会话结束时保存上下文信息，确保会话之间的连贯性。

## 触发条件

当用户表示希望在开始新会话之前结束当前会话时，执行本协议。

## 协议步骤

按以下顺序执行这些步骤：

### 1. 将内容写入每日日志

将相关信息写入 `memory/YYYY-MM-DD.md` 文件（如果文件不存在则创建）：
- 本次会话中讨论的关键主题
- 作出的决策
- 成功执行的命令、配置或代码
- 解决的问题及其解决方法
- 遇到的问题或学到的经验

### 2. 更新长期记忆记录

如果有了重要的学习成果，更新 `MEMORY.md` 文件：
- 新发现的用户偏好设置
- 重要的学习内容
- 长期决策
- 工作流程的变更

### 3. 更新 PARA 笔记

检查并更新 `notes/`（或 `memory/notes/`）目录下的 PARA 结构：
- **未完成的任务**（`notes/areas/open-loops.md`）：添加新的未完成事项，并用 ✅ 标记已完成的事项
- **项目**（`notes/projects/`）：更新正在进行的项目的进度
- **职责**（`notes/areas/`）：添加新的职责内容
- **资源**（`notes/resources/`）：添加新的参考资料或操作指南

### 4. 提交更改

```bash
cd <workspace>
git add -A
git status
git commit -m "wrap-up: YYYY-MM-DD session summary"
git push
```

**注意：**
- 提交更改的操作是**自动执行的**（无需确认提示）。
- 如果 `git push` 失败，请报告错误并将更改保留在本地。

### 5. 提供总结

向用户提供简要的总结：
- 已记录的内容
- 已更新的文件
- 下次会话需要跟进的事项
- 确认更改是否已成功提交（以及是否已推送）

## 示例输出

```
## Session Wrap-Up Complete ✅

**Captured to daily log:**
- Configured PARA second brain
- Fixed vector indexing for notes
- Set up weekly memory review cron

**Updated:**
- MEMORY.md: Added memory system learnings
- notes/areas/open-loops.md: Marked .gitignore task complete

**Committed:** `wrap-up: 2026-01-30 session summary`

**Follow-up next session:**
- Check LanceDB autoCapture setting
- Consider morning briefing cron

Ready for new session! ⚡
```

## 注意事项：
- 如果每日日志文件不存在，请务必创建它。
- 使用当前日期作为文件名和提交信息。
- 保持总结的简洁性，同时确保信息完整。
- 在总结末尾添加 ⚡ 表情符号（GigaBot 的标识）。