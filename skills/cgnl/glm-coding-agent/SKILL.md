---
name: glm-coding-agent
description: 使用 GLM 4.7（通过 Z.AI）运行 Claude Code CLI，具备自动 Git 安全机制（包括检查点、实验分支和代码审查工作流程）。仅需 20 万美元的成本即可获得丰富的上下文信息。
metadata: {"openclaw":{"emoji":"🤖","requires":{"bins":["claude"]}}}
---

# GLM编码代理

通过Z.AI的Anthropic兼容API，使用**Claude Code CLI**与**GLM 4.7**进行协作，同时具备**自动Git保护**功能：
- ✅ 每次运行前都会创建Git检查点
- ✅ 实验分支的隔离
- ✅ 交互式审查流程
- ✅ 一键回滚功能
- 💰 仅需20万个上下文令牌（成本较低）

## 快速入门

### 从命令行开始

#### macOS/Linux
```bash
cd ~/my-project
~/clawd/scripts/safe-glm.sh "Add error handling to the API"
```

#### Windows
```powershell
cd C:\Users\you\my-project
& "$env:USERPROFILE\clawd\scripts\safe-glm.ps1" "Add error handling to the API"
```

### 从OpenClaw开始（支持所有平台）
```bash
# macOS/Linux
bash pty:true workdir:~/project command:"~/clawd/scripts/safe-glm.sh 'Add error handling'"

# Windows
pwsh pty:true workdir:C:\project command:"$env:USERPROFILE\clawd\scripts\safe-glm.ps1 'Add error handling'"

# After completion → interactive review:
#   1️⃣ ACCEPT - Merge to main
#   2️⃣ REVIEW - Selective staging
#   3️⃣ REJECT - Discard all
#   4️⃣ KEEP   - Manual fixes

# Background mode
bash pty:true workdir:~/project background:true command:"~/clawd/scripts/safe-glm.sh 'Refactor auth module'"

# Monitor
process action:log sessionId:XXX
```

## 设置（一次性完成）

### 平台特定的设置

**macOS/Linux：** 使用bash脚本（`.sh`）
**Windows：** 使用PowerShell脚本（`.ps1`）

---

### 1. 创建glmcode封装脚本（内部使用）

**注意：** 此脚本由safe-glm内部调用，您无需直接使用。

#### macOS/Linux（Bash）
```bash
cat > ~/clawd/scripts/glmcode.sh << 'EOF'
#!/bin/bash
# GLM Code - Claude Code with GLM 4.7 via Z.AI
# Reads API key from OpenClaw config automatically

# Read Z.AI API key from OpenClaw config
CONFIG_FILE="${HOME}/.openclaw/openclaw.json"
if [ -f "$CONFIG_FILE" ]; then
  API_KEY=$(jq -r '.models.providers.zai.apiKey // empty' "$CONFIG_FILE" 2>/dev/null)
  if [ -n "$API_KEY" ]; then
    export ANTHROPIC_AUTH_TOKEN="$API_KEY"
  else
    echo "Error: Z.AI API key not found in OpenClaw config" >&2
    exit 1
  fi
else
  echo "Error: OpenClaw config not found at $CONFIG_FILE" >&2
  exit 1
fi

export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export API_TIMEOUT_MS=3000000

# Use GLM-specific settings if they exist, otherwise default
SETTINGS_FILE="${HOME}/.claude/settings-glm.json"
if [ -f "$SETTINGS_FILE" ]; then
  exec claude --settings "$SETTINGS_FILE" "$@"
else
  exec claude "$@"
fi
EOF

chmod +x ~/clawd/scripts/glmcode.sh
```

#### Windows（PowerShell）
PowerShell脚本已创建在以下路径：
- `%USERPROFILE%\clawd\scripts\glmcode.ps1`
- `%USERPROFILE%\clawd\scripts\safe-glm.ps1`

无需额外设置！只需确保OpenClaw配置文件存在：
```
%USERPROFILE%\.openclaw\openclaw.json
```

### 2. 创建GLM配置文件

#### macOS/Linux
```bash
mkdir -p ~/.claude
cat > ~/.claude/settings-glm.json << 'EOF'
{
  "model": "glm-4.7",
  "max_tokens": 8192
}
EOF
```

#### Windows
```powershell
# Create settings directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude"

# Create settings file
@"
{
  "model": "glm-4.7",
  "max_tokens": 8192
}
"@ | Out-File -FilePath "$env:USERPROFILE\.claude\settings-glm.json" -Encoding utf8
```

### 3. 加载便捷别名（推荐）

#### macOS/Linux
```bash
# Add to ~/.zshrc or ~/.bashrc
source ~/clawd/scripts/glm-alias.sh

# Provides: glm, glm-review, glm-diff, glm-log, glm-undo, glm-branches, glm-clean
```

#### Windows
```powershell
# Add to PowerShell profile
notepad $PROFILE

# Add this function:
function glm { & "$env:USERPROFILE\clawd\scripts\safe-glm.ps1" @args }

# Reload profile
. $PROFILE
```

**注意：** Windows系统不支持所有bash别名（如glm-review、glm-diff等），请直接使用git命令：
```powershell
git status              # = glm-review
git diff HEAD~1         # = glm-diff
git log --oneline -10   # = glm-log
git reset --hard HEAD~1 # = glm-undo
```

---

## 🛡️ 安全的GLM封装工具（推荐！）

**safe-glm封装工具**（`~/clawd/scripts/safe-glm.sh`）提供自动的Git安全保护：

### 功能介绍

1. ✅ **Git检查点** - 在运行GLM之前创建备份提交
2. ✅ **实验分支** - 将更改与主分支隔离
3. ✅ **暂存未提交的更改** - 保护您的未完成工作
4. ✅ **变更审查** - 完成后显示差异及文件统计信息
5. ✅ **交互式菜单** - 可选择：接受/审查/拒绝/保留

### 工作原理

```bash
# Run in any git repo
cd ~/projects/myapp
~/clawd/scripts/safe-glm.sh "Fix auth bug"

# After GLM finishes:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 Changed files (3):
 auth.js      | 12 ++++++++++--
 utils.js     |  5 +++++
 tests/auth.js| 24 ++++++++++++++++++++++++

Choose [1/2/3/4]:
  1️⃣  ACCEPT - Merge to main
  2️⃣  REVIEW - Selective staging (git add -p)
  3️⃣  REJECT - Discard all changes
  4️⃣  KEEP   - Stay on branch for manual fixes
```

### 从OpenClaw开始的操作步骤
```bash
# Safe mode (recommended!)
bash pty:true workdir:~/project command:"~/clawd/scripts/safe-glm.sh 'Add error handling'"

# With background (interactive menu after completion)
bash pty:true workdir:~/project background:true command:"~/clawd/scripts/safe-glm.sh 'Refactor auth module'"
```

### 便捷别名设置

将以下内容添加到`~/.zshrc`文件中：
```bash
source ~/clawd/scripts/glm-alias.sh
```

现在您已经完成了配置：

```bash
glm "task"          # Run safe session
glm-review          # Show repo status
glm-diff            # Diff since last checkpoint
glm-log             # GLM commit history
glm-undo            # Rollback last commit
glm-branches        # List experiment branches
glm-clean           # Delete old branches
```

### 安全特性

| 特性 | 保护措施 |
|---------|-----------|
| Git检查点 | 可通过`glm-undo`进行回滚 |
| 实验分支 | 主分支在合并前保持不变 |
| 暂存未提交的更改 | 避免数据丢失 |
| 强制审查 | 必须明确接受或拒绝更改 |
| 差异预览 | 合并前查看所有更改 |
| 选择性提交 | 仅提交有益的更改 |

**适用场景：**
- ✅ 任何编码任务（推荐使用！）
- ✅ 涉及多个文件的代码重构
- ✅ 对GLM的输出结果不确定时
- ✅ 学习或测试GLM的功能

**文档参考：** `/Users/sander/clawd/docs/SAFE-GLM-GUIDE.md`

**系统要求：**
- ✅ 必须拥有Git仓库（如需可运行`git init`）
- ✅ 请确保没有未提交的更改，否则系统会自动暂存这些更改

---

## 安全性与沙箱机制

Claude Code具备**内置的操作系统级沙箱保护**功能，可防止恶意操作：

### 内置的沙箱保护机制

**禁止的操作：**
- ✅ 无法修改项目目录外的文件
- ✅ 无法访问`~/.ssh/`或敏感配置文件
- ✅ 无法删除系统文件
- ✅ 网络访问仅限于允许的域名
- ✅ 防止提示注入攻击

**沙箱的启用方式：**
```bash
# One-time setup (inside Claude Code session)
/sandbox
# Choose "Auto-allow mode" for automation
```

**在`~/.claude/settings.json`中进行配置：**
```json
{
  "sandbox": {
    "mode": "auto-allow",
    "filesystem": {
      "allow": ["/Users/sander/Projects"],
      "deny": ["~/.ssh", "~/.aws"]
    },
    "network": {
      "allowedDomains": ["github.com", "npmjs.org"]
    }
  }
}
```

### safe-glm如何利用这些安全特性

`safe-glm.sh`内部使用了`--dangerously-skip-permissions`选项，但Git的安全机制提供了额外的保护：
- **Git检查点** - 每次更改都可以被回滚
- **实验分支** - 主分支在合并前保持不变
- **交互式审查** - 合并前会显示所有更改
- **可选的沙箱保护** - 提供额外的操作系统级保护

**多重安全保障：**
- Git保护您的代码历史记录
- 沙箱保护您的文件系统
- 审查功能确保您能做出明智的决策

## 从OpenClaw的使用方法
```bash
# One-shot task
bash pty:true workdir:~/project command:"~/clawd/scripts/safe-glm.sh 'Fix the typo in README.md'"

# Background mode (interactive menu after completion)
bash pty:true workdir:~/project background:true command:"~/clawd/scripts/safe-glm.sh 'Refactor auth module'"

# Monitor background tasks
process action:log sessionId:XXX
process action:poll sessionId:XXX
```

### 完成任务后的自动通知

对于耗时较长的后台任务，可以设置唤醒触发器：
```bash
bash pty:true workdir:~/project background:true command:"~/clawd/scripts/safe-glm.sh 'Build a REST API for todos.

When completely finished, run:
openclaw gateway wake --text \"Done: Built todos REST API\" --mode now'"
```

## 为什么选择GLM 4.7？

| 特性 | 优势 |
|---------|-------|
| **成本** | 通过Z.AI使用，成本非常低！ |
| **上下文令牌** | 仅需20万个令牌 |
| **响应速度** | 回应迅速 |
| **适用场景** | 非常适合编码任务 |
| **API兼容性** | 通过Z.AI与Anthropic API兼容 |

**注意事项：** 虽然GLM 4.7不如Claude Opus智能，但适用于以下场景：
- 代码重构
- 错误修复
- 文档编写
- 简单的功能添加
- 代码审查

对于需要高级推理能力的任务，请使用Claude Opus。

## 示例

### 修复错误
```bash
bash pty:true workdir:~/myapp command:"~/clawd/scripts/safe-glm.sh 'Fix the 500 error in /api/users endpoint'"
```

### 添加测试用例
```bash
bash pty:true workdir:~/myapp command:"~/clawd/scripts/safe-glm.sh 'Add unit tests for the User model'"
```

### 代码重构（后台执行）
```bash
bash pty:true workdir:~/myapp background:true command:"~/clawd/scripts/safe-glm.sh 'Refactor auth.js to use async/await instead of callbacks'"

# Monitor progress
process action:log sessionId:XXX
```

### 代码审查
```bash
bash pty:true workdir:~/myapp command:"~/clawd/scripts/safe-glm.sh 'Review the auth module and suggest improvements'"

# If GLM doesn't change files → no git checkpoint needed
# If GLM suggests code changes → safe review workflow
```

## 使用建议

1. **先使用Git** - 始终在Git仓库中进行操作（如需可运行`git init`）
2. **运行GLM前先提交** - 清晰的提交状态有助于后续审查（safe-glm会自动暂存未提交的更改）
3. **启用交互式终端** - Claude Code支持交互式终端界面
4. **设置工作目录** - 代理程序会专注于当前项目
5. **明确任务目标** - GLM在处理具体任务时效果最佳
6. **长时间运行的任务** - 使用后台任务避免占用OpenClaw的资源
7. **使用`process:log`监控进度** - 不必关闭程序即可查看进度
8. **保持简单** - 对于复杂任务，可以考虑使用Claude Opus
9. **加载便捷别名** - 通过`source ~/clawd/scripts/glm-alias.sh`加载常用命令
10. **选择性提交** - 使用`git add -p`仅提交有益的更改

## 常见问题及解决方法

- **“claude: command not found”**：安装Claude Code：`npm install -g @anthropic-ai/claude-code`
- **Linux/WSL2环境下沙箱功能不可用**：请安装相关依赖项：
```bash
# Ubuntu/Debian
sudo apt-get install bubblewrap socat

# Fedora
sudo dnf install bubblewrap socat
```

- **超时错误**：封装工具已将API_TIMEOUT_MS设置为50分钟
- **模型找不到**：检查Z.AI的API是否正常运行：`curl https://api.z.ai/api/anthropic/v1/models`
- **GLM返回异常结果**：请在提示中提供更具体的信息，或尝试使用Claude Opus
- **沙箱阻止合法操作**：更新`~/.claude/settings.json`中的允许路径/域名设置：
```json
{
  "sandbox": {
    "filesystem": {
      "allow": ["/path/to/your/project"]
    },
    "network": {
      "allowedDomains": ["yourapi.com"]
    }
  }
}
```

## 成本对比

| 模型 | 输入数据 | 输出结果 | 所需上下文令牌 |
|-------|-------|--------|--------------|
| **GLM 4.7** | 成本较低 |
| Claude Opus | 每百万条指令15美元 | 每百万条指令75美元 | 约3美元 |
| Claude Sonnet | 每百万条指令3美元 | 每百万条指令15美元 | 约0.6美元 |
| GPT-4 | 每百万条指令30美元 | 每百万条指令60美元 | 约6美元 |

对于不需要高级推理能力的编码任务，GLM的成本优势非常明显！ 💰

## 使用git worktrees并行解决问题

利用GLM代理并行处理多个问题，节省成本！

### 设置方法
```bash
# 1. Create worktrees for each issue
git worktree add -b fix/issue-42 /tmp/issue-42 main
git worktree add -b fix/issue-55 /tmp/issue-55 main
git worktree add -b fix/issue-67 /tmp/issue-67 main

# 2. Launch safe-glm in each (background + PTY!)
bash pty:true workdir:/tmp/issue-42 background:true command:"~/clawd/scripts/safe-glm.sh 'Fix issue #42: Button color bug'"

bash pty:true workdir:/tmp/issue-55 background:true command:"~/clawd/scripts/safe-glm.sh 'Fix issue #55: API timeout'"

bash pty:true workdir:/tmp/issue-67 background:true command:"~/clawd/scripts/safe-glm.sh 'Fix issue #67: Typo in docs'"

# 3. Monitor all at once
process action:list

# 4. Check individual logs
process action:log sessionId:XXX

# 5. After fixes complete, review each worktree
cd /tmp/issue-42
git log -1 --stat  # Review the commit
git push -u origin fix/issue-42
gh pr create --title "fix: button color (#42)" --body "Fixes #42"

cd /tmp/issue-55
git log -1 --stat
git push -u origin fix/issue-55
gh pr create --title "fix: increase API timeout (#55)" --body "Fixes #55"

# 6. Cleanup worktrees
git worktree remove /tmp/issue-42
git worktree remove /tmp/issue-55
git worktree remove /tmp/issue-67
```

### 原理说明

**隔离机制：** 每个工作树都是独立的代码环境，因此代理之间不会相互干扰。

**成本优势：** 使用GLM时，可以以较低的成本同时运行多个代理！

**效率提升：** 所有问题可以同时得到解决，无需依次处理。

**安全性保障：** 工作树确保主仓库的整洁，错误只会保存在`/tmp/`目录中。

### 使用建议

1. **选择简单的问题** - GLM在处理具体任务（如拼写错误、小错误或文档修改）时效果最佳
2. **明确提交信息** - 指定GLM应使用的提交信息
3. **使用`process:list`监控进度** - 查看哪些代理已完成任务
4. **完成后务必清理** - 使用`git worktree remove`删除临时工作树
5. **使用标签** - 为每个任务添加`openclaw gateway wake`以实现自动通知

### 示例：同时修复5个问题

```bash
# Issues: 42, 55, 67, 71, 89
for i in 42 55 67 71 89; do
  git worktree add -b fix/issue-$i /tmp/issue-$i main
  bash pty:true workdir:/tmp/issue-$i background:true command:"~/clawd/scripts/safe-glm.sh 'Fix issue #$i from GitHub. When done, run: openclaw gateway wake --text \"Fixed issue #$i\" --mode now'"
done

# Monitor
process action:list

# After all finish, bulk create PRs
for i in 42 55 67 71 89; do
  cd /tmp/issue-$i
  git push -u origin fix/issue-$i
  gh pr create --title "fix: issue #$i" --body "Fixes #$i" --assignee @me
done

# Cleanup
for i in 42 55 67 71 89; do
  git worktree remove /tmp/issue-$i
done
```

**结果：** 以较低的成本同时解决了5个问题，并生成了5个Pull Request。这就是GLM的优势！ 💰

## 与session_spawn的集成

您还可以将GLM编码任务作为子代理来执行：
```javascript
sessions_spawn({
  task: "Build a todo API in ~/projects/todos using Express.js",
  model: "zai/glm-4.7",
  label: "glm-todo-api"
})
```

这种方式会在隔离的会话中运行GLM，并在任务完成后通知您。比使用bash和后台任务更简洁！

---

## 相关资源

- **安全GLM使用指南：** `/Users/sander/clawd/docs/SAFE-GLM-GUIDE.md`（macOS/Linux版本）
- **Windows使用指南：** `/Users/sander/clawd/docs/SAFE-GLM-WINDOWS.md`（Windows PowerShell版本）
- **脚本文件（macOS/Linux）：**
  - `~/clawd/scripts/safe-glm.sh` - 主要安全封装脚本（Bash）
  - `~/clawd/scripts/glm-alias.sh` - 便捷别名脚本（Bash）
  - `~/clawd/scripts/glmcode.sh` - 内部Z.AI封装脚本（Bash）
- **Windows脚本：**
  - `%USERPROFILE%\clawd\scripts\safe-glm.ps1` - 主要安全封装脚本（PowerShell）
  - `%USERPROFILE%\clawd\scripts\glmcode.ps1` - 内部Z.AI封装脚本（PowerShell）
- **相关工具：** `glm-coding-agent`（用于配置代理）

**最后更新时间：** 2026-02-02（新增了safe-glm封装工具）