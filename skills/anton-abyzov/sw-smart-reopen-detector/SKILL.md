---
name: smart-reopen-detector
description: 当用户报告最近完成的工作存在问题时，该系统会建议重新启动相关任务或进行进一步的修改/优化。适用于报告软件中的错误（bug）、功能退化（regression）或新完成的功能存在的问题。系统会扫描过去7天内完成的所有工作，并在检查任务进度（WIP）限制的同时，根据问题的严重程度提供相应的处理建议。
---

# 智能重开检测器（Smart Reopen Detector）

## 目的

当您报告最近完成的工作中出现问题时，我会自动执行以下操作：
1. 🔍 **扫描您最近完成的工作**（过去7天内完成或正在处理中的任务）
2. 🎯 **通过关键词匹配识别相关问题**
3. 💡 **根据相关性评分建议需要重新处理的问题**
4. ⚠️ **在建议重新处理之前检查当前任务的进度限制**

## 激活条件

当您在消息中提到以下关键词时，我会自动激活：
- **功能故障**：`not working`、`broken`、`failing`、`error`、`crash`
- **质量问题**：`bug`、`issue`、`problem`、`wrong`、`incorrect`、`missing`
- **功能退化**：`still broken`、`regression`、`broken again`、`came back`

## 功能说明

### 示例 1：问题报告
```
User: "The GitHub sync isn't working, it was just completed yesterday"
```

我的回复如下：
```
🔍 Scanning recent work...

Found 2 related item(s) in recent work:

📦 INCREMENT: 0031-external-tool-status-sync
   Increment: 0031-external-tool-status-sync
   Completed: 2 days ago
   Relevance: 15 points
   Matched: github, sync

✓ TASK: T-003 GitHub Content Sync
   Increment: 0031-external-tool-status-sync
   Completed: 1 day ago
   Relevance: 14 points
   Matched: github, sync

💡 Suggested action:
   /sw:reopen 0031-external-tool-status-sync --reason "GitHub sync not working"

Would you like me to:
1. Reopen the entire increment (checks WIP limits)
2. Reopen just task T-003 (targeted fix)
3. Show me the WIP status first
```

### 示例 2：特定功能出现故障
```
User: "The authentication is broken after the recent deployment"
```

我的回复如下：
```
🔍 Scanning recent work...

Found 3 related item(s) in recent work:

✓ TASK: T-012 Authentication Service
   Increment: 0025-user-auth
   Completed: 3 days ago
   Relevance: 10 points
   Matched: authentication

✓ TASK: T-014 JWT Token Validation
   Increment: 0025-user-auth
   Completed: 3 days ago
   Relevance: 7 points
   Matched: authentication

💡 Suggested action:
   /sw:reopen 0025-user-auth --task T-012 --reason "Authentication broken after deployment"

⚠️  Note: Increment 0025 was completed 3 days ago. Consider checking deployment config first.
```

### 示例 3：未找到最近完成的工作
```
User: "The payment flow is not working"
```

我的回复如下：
```
🔍 Scanning recent work...

🔍 No related work found in recent activity (last 7 days)

The payment functionality might be:
1. From an older increment (>7 days ago)
2. Not yet implemented
3. Part of external dependencies

Would you like me to:
1. Search all increments (not just recent)
2. Create a new bug increment for investigation
3. Check the backlog for related work
```

## 工作流程

### 第一步：提取关键词
从您的消息中提取相关关键词：
- 功能名称（如 authentication、github、payment）
- 动作词（如 sync、deploy、validate）
- 组件名称（如 api、database、frontend）

### 第二步：扫描最近完成的工作
我会扫描以下内容：
- ✅ **当前正在处理中的任务**
- ✅ **过去7天内完成的任务**
- ✅ **这些任务中的所有子任务**

### 第三步：评分匹配
根据以下标准分配相关性分数：
- **+10 分**：标题/ID 完全匹配
- **+7 分**：标题部分匹配
- **+5 分**：子任务 ID 匹配
- **+3 分**：描述或备注中包含相关内容

### 第四步：提供建议
我会提供：
- 最相关的 5 个匹配结果
- 相关性评分
- 建议使用的命令 `/sw:reopen`
- （如适用）关于任务进度的警告

## 智能建议

### 对于子任务（Increments）
```bash
# Reopen entire increment
/sw:reopen 0031-external-tool-status-sync --reason "GitHub sync failing"

# Check WIP limits first (recommended)
/sw:status
```

### 对于具体任务（Specific Tasks）
```bash
# Reopen single task (surgical fix)
/sw:reopen 0031 --task T-003 --reason "GitHub API 500 error"

# Reopen multiple related tasks
/sw:reopen 0031 --user-story US-001 --reason "All GitHub features broken"
```

### 强制重新处理（绕过进度限制）
```bash
# Use --force for critical production issues
/sw:reopen 0031 --force --reason "Production down, critical fix needed"
```

## 进度限制检查

在建议重新处理任务之前，我会检查：
- ✅ 当前正在处理的任务数量
- **特定类型的任务限制**（例如：功能相关任务最多 2 个，重构任务最多 1 个等）
- ⚠️ 如果重新处理会超出限制，会发出警告

**示例警告**：
```
⚠️  WIP LIMIT WARNING:
   Current active: 2 features
   Limit: 2 features
   Reopening 0031-external-tool-status-sync will EXCEED the limit!

   Options:
   1. Pause another feature first: /sw:pause 0030
   2. Complete another feature: /sw:done 0029
   3. Force reopen (not recommended): --force
```

## 与命令的集成

我可以与以下命令无缝配合使用：
- `/sw:reopen` - 执行重新处理操作
- `/sw:status` - 检查任务进度限制
- `/sw:progress` - 查看任务进度
- `/sw:pause` - 暂停其他任务以释放资源

## 使用场景

**不适用的情况**：
- ❌ 有关代码的一般性问题
- ❌ 功能请求（请使用 `/sw:increment`）
- ❌ 文档相关的问题
- ❌ 任务状态查询（请使用 `/sw:status`）

**仅当您明确报告功能故障或系统异常时，我才会激活。**

## 技术实现

**核心逻辑**：
- 使用 `RecentWorkScanner` 来查找匹配项
- 从用户消息中提取关键词
- 应用相关性评分算法
- 在提供建议之前检查任务进度限制

**智能特性**：
- 去重（避免重复提示相同任务）
- 优先处理最近完成的任务
- 根据上下文提供提示（例如：是否涉及部署、配置或依赖关系）

## 激活示例

### 会激活的情况：
- “GitHub 同步功能无法使用”
- “认证功能出现故障”
- “最后一次提交后测试失败”
- “部署过程中出现崩溃”
- “API 返回 500 错误”
- “修复后问题仍然存在”

### 不会激活的情况：
- “GitHub 同步的原理是什么？”
- “能否添加认证功能？”
- “任务 0031 的状态如何？”
- “请显示任务进度”
- “创建一个新的支付功能”

## 成功标准

当以下条件满足时，说明我的功能成功：
- ✅ 您能快速找到相关问题（<30 秒）
- ✅ 提供的正确建议能够解决问题
- ✅ 没有误报（仅显示相关结果）
- ✅ 遵守了任务进度限制
- ✅ 提供了明确的下一步操作指南

---

**自动触发条件**：当您报告最近完成的工作出现问题时
**可用命令**：`/sw:reopen`、`/sw:status`
**相关技能**：`increment-planner`、`tdd-workflow`