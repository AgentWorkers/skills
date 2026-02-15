---
name: task-orchestrator
description: 具有依赖关系分析功能的自主多智能体任务编排系统，支持并行执行 tmux/Codex 工具，并具备自我修复的心跳监测机制。适用于需要协调并行处理多个问题/任务的大型项目。
metadata: {"clawdbot":{"emoji":"🎭","requires":{"anyBins":["tmux","codex","gh"]}}}
---

# 任务编排器

使用 tmux 和 Codex 实现多代理构建的自动化编排，并具备自我修复的监控功能。

**请同时参考“高级工程技能”以了解相关工程原理。**

## 核心概念

### 1. 任务清单（Task Manifest）
一个 JSON 文件，用于定义所有任务、它们的依赖关系、涉及的文件以及状态。

```json
{
  "project": "project-name",
  "repo": "owner/repo",
  "workdir": "/path/to/worktrees",
  "created": "2026-01-17T00:00:00Z",
  "model": "gpt-5.2-codex",
  "modelTier": "high",
  "phases": [
    {
      "name": "Phase 1: Critical",
      "tasks": [
        {
          "id": "t1",
          "issue": 1,
          "title": "Fix X",
          "files": ["src/foo.js"],
          "dependsOn": [],
          "status": "pending",
          "worktree": null,
          "tmuxSession": null,
          "startedAt": null,
          "lastProgress": null,
          "completedAt": null,
          "prNumber": null
        }
      ]
    }
  ]
}
```

### 2. 依赖规则
- **相同文件 = 顺序执行** — 涉及相同文件的任务必须按顺序执行或合并
- **不同文件 = 并行执行** — 独立的任务可以同时执行
- **显式依赖关系 = 等待** — `dependsOn` 数组用于强制执行顺序
- **阶段门控（Phase Gates）** — 下一个阶段需要等待当前阶段的完成

### 3. 执行模型
- 每个任务都有自己的 **git 工作区（git worktree，即独立的分支）**
- 每个任务都在自己的 **tmux 会话（tmux session）** 中运行
- 使用 `Codex` 并配合 `--yolo` 参数实现自动化执行
- 模型：**GPT-5.2-codex high**（可配置）

---

## 设置命令

### 初始化编排
```bash
# 1. Create working directory
WORKDIR="${TMPDIR:-/tmp}/orchestrator-$(date +%s)"
mkdir -p "$WORKDIR"

# 2. Clone repo for worktrees
git clone https://github.com/OWNER/REPO.git "$WORKDIR/repo"
cd "$WORKDIR/repo"

# 3. Create tmux socket
SOCKET="$WORKDIR/orchestrator.sock"

# 4. Initialize manifest
cat > "$WORKDIR/manifest.json" << 'EOF'
{
  "project": "PROJECT_NAME",
  "repo": "OWNER/REPO",
  "workdir": "WORKDIR_PATH",
  "socket": "SOCKET_PATH",
  "created": "TIMESTAMP",
  "model": "gpt-5.2-codex",
  "modelTier": "high",
  "phases": []
}
EOF
```

### 分析 GitHub 问题以获取依赖关系
```bash
# Fetch all open issues
gh issue list --repo OWNER/REPO --state open --json number,title,body,labels > issues.json

# Group by files mentioned in issue body
# Tasks touching same files should serialize
```

### 创建工作区
```bash
# For each task, create isolated worktree
cd "$WORKDIR/repo"
git worktree add -b fix/issue-N "$WORKDIR/task-tN" main
```

### 启动 tmux 会话
```bash
SOCKET="$WORKDIR/orchestrator.sock"

# Create session for task
tmux -S "$SOCKET" new-session -d -s "task-tN"

# Launch Codex (uses gpt-5.2-codex with reasoning_effort=high from ~/.codex/config.toml)
# Note: Model config is in ~/.codex/config.toml, not CLI flag
tmux -S "$SOCKET" send-keys -t "task-tN" \
  "cd $WORKDIR/task-tN && codex --yolo 'Fix issue #N: DESCRIPTION. Run tests, commit with good message, push to origin.'" Enter
```

---

## 监控与自我修复

### 进度检查脚本
```bash
#!/bin/bash
# check_progress.sh - Run via heartbeat

WORKDIR="$1"
SOCKET="$WORKDIR/orchestrator.sock"
MANIFEST="$WORKDIR/manifest.json"
STALL_THRESHOLD_MINS=20

check_session() {
  local session="$1"
  local task_id="$2"
  
  # Capture recent output
  local output=$(tmux -S "$SOCKET" capture-pane -p -t "$session" -S -50 2>/dev/null)
  
  # Check for completion indicators
  if echo "$output" | grep -qE "(All tests passed|Successfully pushed|❯ $)"; then
    echo "DONE:$task_id"
    return 0
  fi
  
  # Check for errors
  if echo "$output" | grep -qiE "(error:|failed:|FATAL|panic)"; then
    echo "ERROR:$task_id"
    return 1
  fi
  
  # Check for stall (prompt waiting for input)
  if echo "$output" | grep -qE "(\? |Continue\?|y/n|Press any key)"; then
    echo "STUCK:$task_id:waiting_for_input"
    return 2
  fi
  
  echo "RUNNING:$task_id"
  return 0
}

# Check all active sessions
for session in $(tmux -S "$SOCKET" list-sessions -F "#{session_name}" 2>/dev/null); do
  check_session "$session" "$session"
done
```

### 自我修复机制
当任务卡住时，编排器应采取以下措施：
1. **等待用户输入** → 发送相应的提示或请求
   ```bash
   tmux -S "$SOCKET" send-keys -t "$session" "y" Enter
   ```

2. **出现错误/失败** → 捕获日志，分析问题并尝试修复后重新执行
   ```bash
   # Capture error context
   tmux -S "$SOCKET" capture-pane -p -t "$session" -S -100 > "$WORKDIR/logs/$task_id-error.log"
   
   # Kill and restart with error context
   tmux -S "$SOCKET" kill-session -t "$session"
   tmux -S "$SOCKET" new-session -d -s "$session"
   tmux -S "$SOCKET" send-keys -t "$session" \
     "cd $WORKDIR/$task_id && codex --model gpt-5.2-codex-high --yolo 'Previous attempt failed with: $(cat error.log | tail -20). Fix the issue and retry.'" Enter
   ```

3. **20 分钟以上无进展** → 发送提醒或重启任务
   ```bash
   # Check git log for recent commits
   cd "$WORKDIR/$task_id"
   LAST_COMMIT=$(git log -1 --format="%ar" 2>/dev/null)
   
   # If no commits in threshold, restart
   ```

### 心跳检测（Heartbeat Detection）配置
```bash
# Add to cron (every 15 minutes)
cron action:add job:{
  "label": "orchestrator-heartbeat",
  "schedule": "*/15 * * * *",
  "prompt": "Check orchestration progress at WORKDIR. Read manifest, check all tmux sessions, self-heal any stuck tasks, advance to next phase if current is complete. Do NOT ping human - fix issues yourself."
}
```

---

## 完整的编排流程

### 第 1 步：分析与规划
```bash
# 1. Fetch issues
gh issue list --repo OWNER/REPO --state open --json number,title,body > /tmp/issues.json

# 2. Analyze for dependencies (files mentioned, explicit deps)
# Group into phases:
# - Phase 1: Critical/blocking issues (no deps)
# - Phase 2: High priority (may depend on Phase 1)
# - Phase 3: Medium/low (depends on earlier phases)

# 3. Within each phase, identify:
# - Parallel batch: Different files, no deps → run simultaneously
# - Serial batch: Same files or explicit deps → run in order
```

### 第 2 步：创建任务清单
编写 `manifest.json` 文件，其中包含所有任务及其依赖关系和文件映射。

### 第 3 步：启动第一阶段
```bash
# Create worktrees for Phase 1 tasks
for task in phase1_tasks; do
  git worktree add -b "fix/issue-$issue" "$WORKDIR/task-$id" main
done

# Launch tmux sessions
for task in phase1_parallel_batch; do
  tmux -S "$SOCKET" new-session -d -s "task-$id"
  tmux -S "$SOCKET" send-keys -t "task-$id" \
    "cd $WORKDIR/task-$id && codex --model gpt-5.2-codex-high --yolo '$PROMPT'" Enter
done
```

### 第 4 步：监控与自我修复
每 15 分钟进行一次心跳检测：
1. 检查所有 tmux 会话的状态
2. 更新任务清单以反映进度
3. 自动修复卡住的任务
4. 当所有第 N 阶段的任务完成后，启动第 N+1 阶段

### 第 5 步：创建 Pull Request (PR)
```bash
# When task completes successfully
cd "$WORKDIR/task-$id"
git push -u origin "fix/issue-$issue"
gh pr create --repo OWNER/REPO \
  --head "fix/issue-$issue" \
  --title "fix: Issue #$issue - $TITLE" \
  --body "Closes #$issue

## Changes
[Auto-generated by Codex orchestrator]

## Testing
- [ ] Unit tests pass
- [ ] Manual verification"
```

### 第 6 步：清理
```bash
# After all PRs merged or work complete
tmux -S "$SOCKET" kill-server
cd "$WORKDIR/repo"
for task in all_tasks; do
  git worktree remove "$WORKDIR/task-$id" --force
done
rm -rf "$WORKDIR"
```

---

## 任务清单的状态值
| 状态 | 含义 |
|--------|---------|
| `pending` | 尚未开始 |
| `blocked` | 正在等待依赖关系完成 |
| `running` | Codex 会话正在运行 |
| `stuck` | 需要人工干预（自我修复） |
| `error` | 失败，需要重试 |
| `complete` | 任务已完成，可以提交 Pull Request |
| `pr_open` | 已创建 Pull Request |
| `merged` | Pull Request 已合并 |

---

## 示例：安全框架的编排
```json
{
  "project": "nuri-security-framework",
  "repo": "jdrhyne/nuri-security-framework",
  "phases": [
    {
      "name": "Phase 1: Critical",
      "tasks": [
        {"id": "t1", "issue": 1, "files": ["ceo_root_manager.js"], "dependsOn": []},
        {"id": "t2", "issue": 2, "files": ["ceo_root_manager.js"], "dependsOn": ["t1"]},
        {"id": "t3", "issue": 3, "files": ["workspace_validator.js"], "dependsOn": []}
      ]
    },
    {
      "name": "Phase 2: High",
      "tasks": [
        {"id": "t4", "issue": 4, "files": ["kill_switch.js", "container_executor.js"], "dependsOn": []},
        {"id": "t5", "issue": 5, "files": ["kill_switch.js"], "dependsOn": ["t4"]},
        {"id": "t6", "issue": 6, "files": ["ceo_root_manager.js"], "dependsOn": ["t2"]},
        {"id": "t7", "issue": 7, "files": ["container_executor.js"], "dependsOn": []},
        {"id": "t8", "issue": 8, "files": ["container_executor.js", "egress_proxy.js"], "dependsOn": ["t7"]}
      ]
    }
  ]
}
```

**第一阶段的并行执行：**
- `t1` 和 `t3` 并行执行（处理不同的文件）
- `t2` 等待 `t1` 的完成（处理相同的文件）

**第二阶段的并行执行：**
- `t4`、`t6`、`t7` 可以同时开始执行
- `t5` 等待 `t4` 的完成，`t8` 等待 `t7` 的完成

---

## 提示
1. 对于复杂任务，始终使用 `GPT-5.2-codex high` 模型：`--model gpt-5.2-codex-high`
2. 提交信息应包含问题编号、描述、预期结果和测试步骤
3. 使用 **原子提交（Atomic Commits）**——确保每次逻辑变更后都进行提交
4. 尽早将代码推送到远程仓库，以防会话异常导致进度丢失
5. 定期将 tmux 的输出保存到文件中
6. 在第 N 阶段 100% 完成后才能启动第 N+1 阶段
7. 如果任务卡住超过 10 分钟，应立即进行自动修复
8. 如果 CDP 自动化功能受阻，可以使用 iframe 批量抓取或手动操作浏览器来完成任务

---

## 与其他技能的集成
- **高级工程技能（Senior Engineering Skills）**：用于指导构建流程和质量控制
- **编码代理（Coding Agent）**：提供 Codex CLI 的使用规范
- **GitHub**：用于创建 Pull Request 和管理问题

---

## 经验总结（2026-01-17）
### Codex 沙箱环境的限制
使用 `codex exec --full-auto` 时，沙箱环境存在以下限制：
- **无网络访问权限** — 会导致 `git push` 失败（提示“Could not resolve host”）
- **文件系统限制** — 无法写入某些路径（如 `~/nuri_workspace`）

### 心跳检测的改进措施
心跳检测应检查以下情况：
1. **Shell 提示符是否处于空闲状态** — 如果 tmux 会话显示 `username@hostname path %`，则表示任务已完成
2. **未提交的更改** — 使用 `git log @{u}.. --oneline` 命令检查是否有未推送的更改
3. **推送失败** — 查看日志中是否有 “Could not resolve host” 的错误信息

当检测到这些问题时，应由编排器（而非任务执行者）来处理：
1. 从沙箱外部推送更改
2. 通过 `gh pr create` 命令创建 Pull Request
3. 更新任务清单并通知相关人员

### 推荐的实践模式
```bash
# In heartbeat, for each task:
cd /tmp/orchestrator-*/task-tN
if tmux capture-pane shows shell prompt; then
  # Worker finished, check for unpushed work
  if git log @{u}.. --oneline | grep -q .; then
    git push -u origin HEAD
    gh pr create --title "$(git log --format=%s -1)" --body "Closes #N" --base main
  fi
fi
```