---
name: squad-control
version: 1.1.6
homepage: https://squadcontrol.ai
env:
  SC_API_URL:
    description: Base URL of your Squad Control instance (e.g. https://www.squadcontrol.ai)
    required: true
  SC_API_KEY:
    description: >
      API key from Squad Control Settings → API Keys. Can be workspace-scoped (single workspace)
      or account-scoped (all workspaces). Account-scoped keys are recommended for multi-workspace
      setups — tasks will include an embedded workspace object with all config needed.
    required: true
  GITHUB_TOKEN:
    description: >
      GitHub Personal Access Token for PR creation and repo cloning.
      When not set manually, the skill uses the token returned by the Squad Control API
      (workspace.githubToken) — configured in Squad Control Settings → Project Repository.
    required: false
description: >
  **与 Squad Control 卡诺巴（kanban）集成，以实现 AI 代理的任务编排**  
  ⚠️ 安全提示：此功能会处理 GitHub 令牌和 API 密钥——它会克隆私有仓库、推送代码，并代表您创建 Pull Request（PR）。在安装之前，请阅读 `setup.md` 以获取安全指南。仅连接到您信任的 Squad Control 实例。  
  **适用场景：**  
  - 当定时任务触发以检查待处理的任务时  
  - 当您需要接取、分配或完成卡诺巴任务时  
  - 当您需要创建 PR 并将其提交进行代码审查时  
  - 当您需要创建子代理来执行分配的任务时  
  - 当您需要将任务的成功或失败情况反馈给 Squad Control 时  
  - 当您需要通过编程方式创建任务（分解工作流程）时  
  **不适用场景：**  
  - 当用户提出一般性问题时（请直接回答）  
  - 当您处理的任务不在 Squad Control 中被追踪时  
  - 当您正在子代理会话中工作时（您已经被分配了任务——只需完成任务即可）  
  - 当用户希望通过用户界面管理代理/设置时（请引导他们访问 `squadcontrol.ai`）  
  **输入参数：**  
  - Squad Control API 凭据  
  - 来自 `/api/tasks/pending` 的任务数据  
  **输出结果：**  
  - 在 GitHub 上创建的 Pull Request  
  - Squad Control 中的任务状态更新  
  - 代码审查的评审结果
---
# 队伍控制集成

从队伍控制的看板中协调AI代理的任务。

## 快速参考
- **设置：** `references/setup.md`
- **完整API文档：** `references/api.md`
- **PR模板：** `references/pr-template.md`
- **审查检查表：** `references/review-checklist.md`

所需环境变量：`SC_API_URL`, `SC_API_KEY`

---

## 任务轮询流程

当cron任务触发时，会执行以下操作：
1. 运行`~/.openclaw/skills/squad-control/scripts/poll-tasks.sh`（需要`SC_API_URL`和`SC_API_KEY`环境变量）
2. 如果输出为`HEARTBEAT_OK` → 表示没有任务需要处理，停止轮询
3. 如果输出包含`PENDING_TASKS:` → 解析其中的JSON数据，然后按照下面的“任务拾取与调度”流程处理每个任务
4. 如果输出包含`REVIEW_TASKS:` → 解析其中的JSON数据，然后按照下面的“任务审查与调度”流程处理每个任务
5. 如果输出包含`STUCK_TASKS:` → 解析其中的JSON数据，然后按照下面的“任务恢复”流程处理每个任务

或者，也可以直接调用API：
- 检查待处理任务：`curl -sL "${SC_API_URL}/api/tasks/pending" -H "x-api-key: ${SC_API_KEY}"`
- 检查待审查任务：`curl -sL "${SC_API_URL}/api/tasks/list?status=review" -H "x-api-key: ${SC_API_KEY}"`

从响应中解析工作区配置（详见下面的“多工作区响应处理”部分）。

### 多工作区响应处理

使用账户级API密钥时，`/api/tasks/pending`可能会返回来自**多个工作区**的任务。每个任务都会包含一个`workspace`对象，其中包含了完成任务所需的所有配置。

**响应格式 — 工作区范围（旧版本/单工作区）：**
```json
{
  "workspace": { "_id": "wsId", "name": "MyApp", "repoUrl": "...", "githubToken": "..." },
  "tasks": [{ "_id": "taskId", "title": "...", "agent": { ... } }]
}
```
→ `workspace`位于响应的最顶层；任务本身没有自己的`workspace`对象。

**响应格式 — 账户范围（多工作区）：**
```json
{
  "tasks": [
    {
      "_id": "taskId",
      "title": "...",
      "workspace": {
        "_id": "wsId",
        "name": "MyApp",
        "repoUrl": "https://github.com/org/repo",
        "githubToken": "ghp_...",
        "agentConcurrency": 3
      },
      "agent": { ... }
    }
  ]
}
```
→ 每个任务都有自己的`workspace`对象。来自不同工作区的任务可能会出现在同一个响应中。

**代理字段 — 始终嵌套在`task.agent`下（绝不在任务根级别）：**
```json
{
  "agent": {
    "_id": "agentId",
    "name": "Cody",
    "role": "Developer",
    "model": "anthropic/claude-sonnet-4-6",
    "soulMd": "..."
  }
}
```
> ⚠️ **不要使用`task.agentName`字段** — 该字段不存在。始终使用`task.agent.name`、`task.agent.model`、`task.agent.soulMd`、`task.agent._id`。

**兼容两种响应格式：**
```javascript
// For each task:
// - If task.workspace is present → use it directly
// - If not → use the top-level workspace from the response
const wsConfig = task.workspace ?? response.workspace;
const repoUrl = wsConfig.repoUrl;
const githubToken = wsConfig.githubToken;
const concurrencyLimit = wsConfig.agentConcurrency ?? 2;
```

**每个工作区的并发限制：** 当返回来自多个工作区的任务时，**每个工作区的并发数量**需要单独计算。不要将工作区A的代理数量计入工作区B的并发限制中。

```javascript
// Group by workspace, then dispatch up to concurrency limit for each
const byWorkspace = groupBy(tasks, t => (t.workspace ?? topLevelWs)._id);
for (const [wsId, wsTasks] of Object.entries(byWorkspace)) {
  const ws = wsTasks[0].workspace ?? topLevelWs;
  const limit = ws.agentConcurrency ?? 2;
  const running = countRunningAgentsFor(wsId);
  const slots = Math.max(0, limit - running);
  for (const task of wsTasks.slice(0, slots)) {
    dispatch(task, ws);
  }
}
```

### 任务恢复

每个cron周期执行两次检查：
**检查1 — 任务处于“working”状态且包含待提交的PR：**
```bash
curl -sL "${SC_API_URL}/api/tasks/list?status=working" -H "x-api-key: ${SC_API_KEY}"
```
对于每个`deliverables`中包含PR条目且`startedAt`超过30分钟前的任务 → 自动将其状态改为“review”：
```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/set-review" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${ASSIGNED_AGENT_ID}\", \"result\": \"Auto-rescued: sub-agent completed work but did not transition status.\", \"deliverables\": ${EXISTING_DELIVERABLES}}"
```
在相关线程中发布消息：*"任务已自动转为审查状态 — 子代理完成了PR，但未调用set-review。"*

**检查2 — 任务标记为“done”但PR尚未合并：**
```bash
curl -sL "${SC_API_URL}/api/tasks/list?status=done" -H "x-api-key: ${SC_API_KEY}"
# Filter to tasks completed in the last 2 hours that have a PR deliverable
```
对于每个最近完成但PR尚未合并的任务，验证PR是否真的已经合并：
```bash
# Extract owner/repo from workspace.repoUrl
# Extract PR number from deliverable URL (e.g. https://github.com/org/repo/pull/123 → 123)
curl -sL -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/${owner}/${repo}/pulls/${PR_NUMBER}" | grep -o '"merged":[^,]*'
```
如果`"merged":false`（PR仍处于开放状态） → 代理跳过了审查步骤。需要重新为Hawk创建审查任务：
```bash
# Create a review task for Hawk
curl -sL -X POST "${SC_API_URL}/api/tasks/create" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"title\": \"Review PR #${PR_NUMBER}: ${TASK_TITLE}\", \"description\": \"Agent marked task done but PR is still open and unmerged. Please review and merge if approved.\\n\\nPR: ${PR_URL}\", \"assignedAgentId\": \"${REVIEWER_AGENT_ID}\", \"workspaceId\": \"${WORKSPACE_ID}\", \"priority\": \"high\"}"
```
在原始任务线程中发布警告：*"⚠️ 任务被标记为完成，但PR #N尚未合并。已为Hawk创建了审查任务。"*

### 任务审查与调度

找到需要审查的任务后，首先找到对应的审查代理：
```bash
curl -sL "${SC_API_URL}/api/agents" -H "x-api-key: ${SC_API_KEY}"
# Find agent with role containing "Reviewer" or name "Hawk"
```

对于每个需要审查的任务（具有PR交付物且`pickedUpAt`未设置的情况）：
**不要调用 `/api/tasks/pickup`** — 因为这会阻止状态从“review”变为“working”。直接启动审查代理，并让他们调用 `/api/tasks/review`（该接口会将状态改为“review”或“assigned”）。

使用下面的**审查流程**模板启动审查代理，并直接传递任务ID和所有相关上下文。

### 队伍负责人任务 — 合并与完成

当任务的分配代理是**队伍负责人**（角色包含“Lead”或“Orchestrator”）时，表示Hawk已经批准了PR，此时可以将其合并。**不要直接将任务标记为完成** — 首先需要合并PR。

```bash
# 1. Pick up the task
curl -sL -X POST "${SC_API_URL}/api/tasks/pickup" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${SQUAD_LEAD_ID}\"}"
# Response includes workspace.repoUrl, workspace.githubToken, task.deliverables

# 2. Find the PR deliverable — check type OR url, not just name
# Priority: type === "pr" first, then url containing "/pull/"
# Examples that all qualify: {type:"pr"}, {url:"…/pull/7"}, {name:"PR #7", type:"pr"}
# NEVER complete as done if any deliverable has type="pr" or url containing "/pull/"

# 3. Clone and merge (use credential helper — do NOT embed token in URL)
if [ -n "$GITHUB_TOKEN" ]; then
  git -c "credential.helper=!f() { echo username=x-access-token; echo password=${GITHUB_TOKEN}; }; f" clone "$REPO_URL" /tmp/merge-repo
else
  git clone "$REPO_URL" /tmp/merge-repo
fi
cd /tmp/merge-repo
git fetch origin
git checkout main && git pull origin main
git merge --no-ff origin/task/${TASK_ID} -m "Merge PR #${PR_NUMBER}: ${TASK_TITLE}"
git push origin main

# 4. Post to thread
curl -sL -X POST "${SC_API_URL}/api/threads/send" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${SQUAD_LEAD_ID}\", \"content\": \"Merged PR #${PR_NUMBER} to main.\"}"

# 5. Complete the task
curl -sL -X POST "${SC_API_URL}/api/tasks/complete" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${SQUAD_LEAD_ID}\", \"result\": \"Merged PR #${PR_NUMBER} to main.\", \"status\": \"done\"}"
```

**如果合并失败**（出现冲突）：使用`/api/tasks/fail`接口报告错误，并不要强制合并。将冲突详情发布到相关线程中。
**如果没有PR交付物**：直接完成任务。

---

### 并发限制

**在启动任何代理之前**，先检查当前有多少代理正在运行：
```
subagents(action="list")
```
统计`status = "running`的代理数量。并发限制由`workspace.agentConcurrency`决定（默认值为2，如果没有设置）。

**对于单个工作区：** 如果正在运行的代理数量达到或超过限制，则跳过当前周期的代理启动，并返回`HEARTBEAT_OK`。

**对于多工作区（账户级API密钥）：** **每个工作区的并发限制**需要单独应用。即使其他工作区的代理数量如何，一个`agentConcurrency: 3`的工作区最多也可以运行3个代理。按工作区分组任务，并分别检查每个工作区的代理数量。

此外，每次cron任务运行时，每个工作区的任务数量不得超过`workspace.agentConcurrency`的限制。剩余的任务将在下一次任务轮询时处理。

工作区所有者可以在队伍控制的“设置” → “代理并发”中更改此限制。

---

### 任务拾取与调度

```bash
# Pick up task (marks it in-progress in Squad Control)
curl -sL -X POST "${SC_API_URL}/api/tasks/pickup" \
  -H "x-api-key: ${SC_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${AGENT_ID}\", \"branch\": \"task/${TASK_ID}\"}"
# Response includes workspace.repoUrl and workspace.githubToken
```

在任务线程中发布消息，表示任务正在被调度：
```bash
curl -sL -X POST "${SC_API_URL}/api/threads/send" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${AGENT_ID}\", \"content\": \"Picking up task. Starting work now.\"}"
```

然后使用任务的代理信息启动一个子代理。在标签中包含工作区名称，以便于区分来自不同工作区的任务：

```
sessions_spawn({
  task: <see Spawn Prompt Template below>,
  model: agent.model,
  label: "${agent.name}-${workspace.name}-${taskTitle}",
  runTimeoutSeconds: 1800
})
```

### 启动提示模板

在生成启动提示时，按以下方式解析工作区配置：
- **如果`task_workspace`存在**（账户范围键）：使用`task_workspace.repoUrl`、`task_workspace.githubToken`、`task_workspace.agentConcurrency`
- **如果`task_workspace`不存在**（工作区范围键）：使用响应中的顶级`workspace`信息

```
# Identity
${agent.soulMd}

# Squad Control Credentials (use these for ALL API calls)
SC_API_URL=${SC_API_URL}
SC_API_KEY=${SC_API_KEY}
TASK_ID=${task._id}
AGENT_ID=${agent._id}

# Repository
REPO_URL=${workspace.repoUrl}
GITHUB_TOKEN=${workspace.githubToken}  # may be empty for public repos

# Clone the repo (use credential helper — do NOT embed token in URL)
if [ -n "$GITHUB_TOKEN" ]; then
  git -c "credential.helper=!f() { echo username=x-access-token; echo password=${GITHUB_TOKEN}; }; f" clone "$REPO_URL" /tmp/task-repo
else
  git clone "$REPO_URL" /tmp/task-repo
fi
cd /tmp/task-repo
git checkout -b task/${task._id}

# Task
**${task.title}**
${task.description}

# Git Workflow
- Small, focused commits (feat:, fix:, chore: prefixes)
- Scope changes to this task only
- Run `npx tsc --noEmit` or existing tests before finishing

# When Done — follow these steps EXACTLY, do not skip any

## 1. Commit and push
git add -A && git commit -m "feat: ${task.title}"
git push origin task/${task._id}

## 2. Create GitHub PR
curl -sL -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/${owner}/${repo}/pulls" \
  -d '{"title": "${task.title}", "head": "task/${task._id}", "base": "main", "body": "${summary}"}'
# Save the PR number and URL from the response

## 3. Post summary to thread
curl -sL -X POST "${SC_API_URL}/api/threads/send" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"taskId": "${TASK_ID}", "agentId": "${AGENT_ID}", "content": "Work complete. PR #N: ${PR_URL}\n\n${summary}"}'

## 4. If any files in convex/ were changed
# Deployment is handled by CI after merge to main.
# Do NOT run local deploy commands from this skill prompt.
# If a manual deploy is required, ask the squad lead to run it in a controlled environment.

## 5. Hand off for review (REQUIRED — NEVER call /complete if you opened a PR)

> ⚠️ CRITICAL: If you created a PR in step 2, you MUST call set-review — not complete.
> Calling /complete with an open PR bypasses code review entirely. This is a workflow violation.
> The ONLY time to call /complete directly is when there is NO PR (e.g. a research or docs-only task).

```
```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/set-review" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"taskId": "${TASK_ID}", "agentId": "${AGENT_ID}", "result": "${summary}", "deliverables": [{"type": "pr", "name": "PR #N", "url": "${PR_URL}"}]}
```
```

Verify the API response confirms status changed to "review". If it returns an error, retry once then call /fail with the error details.

## If anything fails
curl -sL -X POST "${SC_API_URL}/api/tasks/fail" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"taskId": "${TASK_ID}", "agentId": "${AGENT_ID}", "error": "description of what went wrong"}'
```

### 任务完成

1. 将处理结果/总结发布到任务线程：
   ```bash
   curl -sL -X POST "${SC_API_URL}/api/threads/send" \
     -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
     -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${AGENT_ID}\", \"content\": \"${SUMMARY}\"}"
   ```
2. 通过GitHub API创建PR（参见`references/pr-template.md`）
3. 如果有审查代理存在 → 将任务设置为待审查状态：
   ```bash
   curl -sL -X POST "${SC_API_URL}/api/tasks/set-review" \
     -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
     -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${AGENT_ID}\", \"result\": \"${SUMMARY}\", \"deliverables\": [{\"type\": \"pr\", \"name\": \"PR #N\", \"url\": \"${PR_URL}\"}]}"
   ```
4. 如果没有审查代理 → 直接完成任务：
   ```bash
   curl -sL -X POST "${SC_API_URL}/api/tasks/complete" \
     -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
     -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${AGENT_ID}\", \"result\": \"${SUMMARY}\", \"status\": \"done\"}"
   ```

### 任务失败

遇到失败情况时，务必报告错误 — 不要直接将任务标记为完成：
```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/fail" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d "{\"taskId\": \"${TASK_ID}\", \"agentId\": \"${AGENT_ID}\", \"error\": \"description of what went wrong\"}"
```

---

## 审查流程

在将任务分配给审查代理时，使用以下提示启动代理（填写所有必要的信息）：

```
# Identity
${reviewer.soulMd}

# Task: Review PR #${prNumber}
**Original task:** ${task.title}
**PR:** ${prUrl}
**Repo:** ${workspace.repoUrl}
**GitHub token:** ${workspace.githubToken}   # may be empty for public repos

# Extract owner/repo from repoUrl
# e.g. https://github.com/org/repo -> owner=org, repo=repo

# Step 1 — Get the diff
curl -sL -H "Authorization: token ${GITHUB_TOKEN}" \
  "https://api.github.com/repos/${owner}/${repo}/pulls/${prNumber}/files"

# Step 2 — Review the code
Check: correctness, code quality, security, edge cases.

# Step 3 — Post review to GitHub PR (REQUIRED — not just to thread)
curl -sL -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  "https://api.github.com/repos/${owner}/${repo}/pulls/${prNumber}/reviews" \
  -d '{"event": "APPROVE", "body": "<review summary>"}'
# Use "REQUEST_CHANGES" instead of "APPROVE" if changes are needed

# Step 4 — Post summary to Squad Control thread
curl -sL -X POST "${SC_API_URL}/api/threads/send" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"taskId": "${TASK_ID}", "agentId": "${REVIEWER_ID}", "content": "## Review — PR #${prNumber}\n\n${summary}"}'

# Step 5 — Submit verdict to Squad Control
curl -sL -X POST "${SC_API_URL}/api/tasks/review" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"taskId": "${TASK_ID}", "agentId": "${REVIEWER_ID}", "verdict": "approve", "comments": "${summary}"}'
# Use "request_changes" if not approving
```

**注意：** `workspace.githubToken`来自`/api/tasks/pending`或`/api/tasks/pickup`的响应。切勿从凭证文件中读取该信息 — 因为该信息可能在该机器上不存在。

---

## 代理发现

```bash
curl -sL "${SC_API_URL}/api/agents" -H "x-api-key: ${SC_API_KEY}"
```

查找`role: "Code Reviewer"`的角色来识别审查代理。

## 程序化创建任务

```bash
curl -sL -X POST "${SC_API_URL}/api/tasks/create" \
  -H "x-api-key: ${SC_API_KEY}" -H "Content-Type: application/json" \
  -d '{"title": "...", "description": "...", "assignedAgentId": "..."}'
```

---

## 常见错误

1. **未完成工作就直接标记为完成** — 在标记任务完成之前，务必将结果发布到线程中，并创建PR（如果任务涉及代码审查）。如果结果为空且没有线程消息，说明任务实际上并未完成。
2. **子代理在打开PR后调用`/complete`而不是`/set-review` — 这是最常见的工作流程错误。如果已经打开了PR，正确的下一步应该是调用`set-review`。直接调用`complete`会跳过代码审查步骤，导致PR处于未合并状态。现在，任务恢复机制会自动为这些未合并的PR创建审查任务。
3. **队伍负责人跳过合并步骤** — 当任务被分配给队伍负责人且包含PR交付物时，必须先合并PR，然后再将其标记为完成。
4. **在启动代理时未传递`SC_API_URL/SC_API_KEY` — 子代理无法在没有这些信息的情况下与队伍控制进行通信。务必在启动模板中包含这些参数。
5. **未使用`workspace.repoUrl` — 待处理任务和任务拾取响应中包含了`workspace.repoUrl`和`workspace.githubToken`。请使用这些信息，不要使用默认的仓库路径。
6. **忘记报告失败情况** — 如果出现问题，务必使用`/api/tasks/fail`接口进行报告。否则，处于“working”状态的任务会永远阻塞任务队列。
7. **在私有仓库克隆代码时未使用token** — 请检查`workspace.githubToken`，并使用git凭证辅助工具：`git -c "credential.helper=!f() { echo username=x-access-token; echo password=<token>; }; f" clone "$REPO_URL"` — 切勿直接在URL中嵌入token，因为这可能导致token泄露。
8. **在分支之前未拉取最新代码** — 这可能会导致基于过时的代码创建PR，从而引发合并冲突。
9. **使用全局并发限制而不是针对每个工作区的限制** — 当处理来自多个工作区的任务（账户级API）时，每个工作区都有其自身的并发限制。不要将工作区A的代理数量计入工作区B的并发限制中。
10. **忽略`task_workspace`字段，始终使用顶级配置** — 账户级密钥会将工作区配置直接嵌入到每个任务中。如果`task_workspace`存在，请使用它；如果不存在，则使用顶级工作区配置。