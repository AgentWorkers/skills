---
name: bmad-method
description: "使用 BMad（Breakthrough Method of Agile AI Driven Development）框架进行人工智能驱动的开发。该框架适用于：架构分析、冲刺计划制定、故事点生成、产品需求文档（PRD）的创建以及整个开发工作流程。需要具备使用 Claude Code 进行编码的技能。"
---
# BMad方法技能

> 使用BMad框架进行人工智能驱动的开发，并支持自主代理工作流程。

**详细参考，请参阅：**
- [docs/reference/commands.md](docs/reference/commands.md) - 完整的命令参考
- [docs/reference/agents.md](docs/reference/agents.md) - 可用的代理
- [docs/how-to/install-bmad.md](docs/how-to/install-bmad.md) - 详细的安装指南
- [docs/tutorials/getting-started.md](docs/tutorials/getting-started.md) - 快速入门

## 依赖项

**此技能需要已安装Claude Code的coding-agent技能。**
- 必须安装Claude Code（路径通常为`~/.local/bin/claude`）
- 所有Claude Code的调用都应使用`bash pty:true`选项

## 描述

BMad（敏捷人工智能驱动开发的突破性方法）是一个分为四个阶段的框架：
1. **分析** — 探索问题空间
2. **规划** — 定义要构建的内容
3. **解决方案** — 决定如何构建
4. **实施** — 实际构建

每个阶段都会生成文档，为下一个阶段提供上下文支持。

---

## 安装

要在项目中使用BMad，请执行以下操作：

> ⚠️ **安全提示：** `npx bmad-method install` 会从npm下载代码。只有在您信任BMad包的情况下才运行此命令。安装前请仔细检查该包。

```bash
cd ~/project && npx bmad-method install
```

根据提示选择Claude Code。

### ⚠️ 安装过程是交互式的

**⚠️ `npx bmad-method install` 会询问一些问题！**

安装时请注意：
- **不要使用`background:true`选项** — 您需要回答所有问题
- **保持会话状态** 并回答每个问题
- **监控日志**，注意以下常见提示：

| 日志中的提示 | 预期答案 | 备注 |
|---------------|----------------|-------|
| “BMad应该安装在哪里？” | `.` 或 `~path/to/project` | 当前目录 |
| “您使用的是哪种AI工具？” | `Claude Code` 或相应的数字 | 选择Claude |
| “选择要安装的模块” | `a` 或 `enter` | 选择全部/默认 |
| “在当前目录安装BMad吗？” | `y` 或 `enter` | 确认 |

```bash
# Installation must be interactive!
bash pty:true workdir:~/project command:"cd ~/project && npx bmad-method install"
# Stay present, answer each prompt:
# - Monitor log for prompts
# - Submit answer via: process action:submit sessionId:XXX data:"y"
```

### ⚠️ 安装前的检查

**在运行任何/bmad-命令之前，请确认BMad已安装：**

```bash
ls -la ~/project/_bmad/  # or _bmad-output/
```

如果未找到BMad，请先进行安装：
```bash
bash pty:true workdir:~/project command:"cd ~/project && npx bmad-method install"
```

---

## 模型选择

**为了提高效率，请选择合适的模型：**

| 模型 | 最适合的场景 |
|-------|----------------|
| **Sonnet** | 架构设计、解决方案制定、快速开发（复杂任务） |
| **Haiku** | 头脑风暴、故事生成、代码审查（重复性/结构化任务） |
| **Opus** | 大规模重构、复杂的架构决策 |

```bash
# Examples
claude --model sonnet "Create the architecture"
claude --model haiku "Generate stories from the epic"
```

---

## 可用的命令（通过/bmad-执行）

| 命令 | 功能 | 输出 |
|---------|---------|--------|
| `/bmad-help` | 交互式指南 | - |
| `/bmad-brainstorming` | 项目想法的头脑风暴（请谨慎使用） | `brainstorming-report.md` |
| `/bmad-bmm-create-prd` | 定义产品需求文档（PRD） | `PRD.md` |
| `/bmad-bmm-create-ux-design` | 设计用户界面（UX） | `ux-spec.md` |
| `/bmad-bmm-create-architecture` | 技术决策 | `architecture.md` + 需求文档（ADRs） |
| `/bmad-bmm-create-epics-and-stories` | 将任务拆分为故事 | 结果文件存储在 `_bmad-output/` 目录下 |
| `/bmad-bmm-check-implementation-readiness` | 检查实施准备情况 | 结果为PASS/CONCERNS/FAIL |
| `/bmad-bmm-sprint-planning` | 初始化冲刺计划 | `sprint-status.yaml` |
| `/bmad-bmm-create-story` | 准备下一个任务 | `story-[slug].md` |
| `/bmad-bmm-dev-story` | 实现任务 | 可运行的代码 + 测试 |
| `/bmad-bmm-code-review` | 验证代码质量 | 提出修改建议 |
| `/bmad-bmm-quick-spec` | 快速制定规范（跳过前三个阶段） | `tech-spec.md` |
| `/bmad-bmm-quick-dev` | 快速实现 | 可运行的代码 |

---

## ⚠️ 重要提示：Claude Code的执行方式

### 尽可能使用非交互式模式

对于不需要实时交互的命令，请使用非交互式模式：

```bash
# Non-interactive (recommended for most BMad workflows)
claude -p --dangerously-skip-permissions "Your prompt"
```

### 何时使用后台模式

仅在以下情况下使用`background:true`选项：
- 顺序执行多个BMad工作流程
- 预计工作流程会花费较长时间

**请每隔10-30秒使用`process action:log`命令监控Claude Code的运行状态，以确保其正常进行。**

### 权限配置

为了避免Claude Code因权限请求而阻塞：

> ⚠️ **安全提示：** 使用`--dangerously-skip-permissions`或`--permission-mode bypassPermissions`会跳过权限检查。请谨慎使用这些选项——仅限于信任的代码执行。在生产环境中，建议使用默认权限设置或先验证代码。

```bash
# Skip all permission prompts (use with caution!)
claude --dangerously-skip-permissions "prompt"

# Or use specific permission mode
claude --permission-mode bypassPermissions "prompt"
```

### 权限确认

**如果Claude Code需要用户确认（如Y/n、提交等操作）：**

1. 查看日志：`process action:log sessionId:XXX`
2. 根据提示类型做出相应操作：
   - **Shell命令（Y/n）**：输入“y”
   - **Git提交提示**：输入“n”（详见下文）
   - **其他情况**：如果知道答案则直接回答，否则询问用户

### 任务完成确认（后台模式）

**如何判断Claude Code是否真正完成：**

1. **日志中显示完成信息**：查找“Task completed”、“Done!”或“All tasks finished”
2. **命令提示返回**：命令提示符重新出现
3. **超时情况**：如果日志超过2分钟仍未显示完成信息，请检查Claude Code的运行状态：
   ```bash
   ps aux | grep claude
   process action:log sessionId:XXX
   ```

**⚠️ 只有在看到明确的完成信息或命令提示符返回时，才能确认任务完成。**

### 长时间运行的任务（如/bmad-bmm-dev-story或大规模重构）

**对于运行时间超过5分钟的工作流程：**

**每隔60秒检查一次日志输出：**
```bash
# Check if process is still alive
ps aux | grep claude

# If stalled but alive → check if waiting for input
process action:log sessionId:XXX

# If process died → trigger recovery (see below)
```

---

## 自主工作流程模式

### 模式1：全面分析 + 规划请求

**用户请求：**“分析当前架构并为项目X生成产品简报”

**代理应执行以下操作：**
1. **安装检查**：确认BMad已安装（`ls _bmad/`）
2. **检查project-context.md**：如果文件缺失或过时，请先生成该文件（详见下文）
3. 在项目目录中启动Claude Code：
   ```bash
   bash pty:true workdir:~/path/to/project background:true command:"claude --dangerously-skip-permissions '/bmad-bmm-create-architecture'"
   ```
4. 使用`process action:log`监控进度（每隔10-30秒检查一次）
5. 如果Claude Code需要更多信息，直接询问用户
6. 完成后，运行`ls _bmad-output/`确认文件是否生成
7. **验证输出**：`grep -i "error" _bmad-output/architecture.md || head -20 _bmad-output/architecture.md`
8. 阅读`architecture.md`以确保内容符合用户需求
9. 然后启动产品简报生成：`/bmad-bmm-create-product-brief`

### 模式2：结合故事生成的冲刺准备

**用户请求：**“为RoundVision准备冲刺计划，并将任务添加到OCM（OpenClaw任务中心）”

**代理应执行以下操作：**
1. **安装检查**：确认BMad已安装
2. 启动Claude Code：
   ```bash
   bash pty:true workdir:~/path/to/project background:true command:"claude --dangerously-skip-permissions '/bmad-bmm-sprint-planning && /bmad-bmm-create-epics-and-stories'"
   ```
3. 等待 `_bmad-output/epics/` 目录下生成任务
4. **刷新上下文**：运行`ls -R _bmad-output/`确认文件存在
5. **高效地读取任务内容**（详见“安全读取故事”部分）
6. **根据每个任务创建OCM任务**（使用task-manager技能）
7. 提交任务列表以完成冲刺准备

#### OCM任务的可追溯性

**在创建OCM任务时，务必包含BMad任务的相关信息：**

```
Task: Implement login form validation
Description: [full story content]
---
Ref: _bmad-output/epics/auth/stories/story-login-validation.md
Epic: auth
Created from: BMad Sprint 1
```

**原因：**这样可以确保OCM任务与原始故事之间的关联，便于追踪。

### 模式3：快速功能实现

**用户请求：**“使用快速开发模式实现功能X”

**代理应执行以下操作：**
1. 启动Claude Code并选择快速开发模式：
   ```bash
   bash pty:true workdir:~/path/to/project command:"claude --dangerously-skip-permissions '/bmad-bmm-quick-dev [feature description]'"
   ```

---

## ⚠️ 快速开发与标准模式的区别

**快速开发模式更快，但缺乏安全保障。请谨慎使用：**

| ✅ 可以使用快速开发 | ❌ 绝对不能使用快速开发 |
|---------------------|------------------------|
| 用户界面调整 | 认证机制更改 |
| 错误修复 | 加密/安全相关更改 |
| 新端点开发 | 数据库迁移 |
| 简单功能 | 支付逻辑 |
| | 数据库架构更改 |

**规则：** 如果更改涉及安全、认证、加密或数据库迁移，请**使用完整的BMad流程**（分析 → 解决方案 → 实施）。

---

## project-context.md的管理

BMad依赖于`project-context.md`作为项目的“核心文档”。它是指导所有决策的持久性上下文文件。

### 在执行/bmad-bmm-create-prd之前

**务必检查：**

```bash
ls ~/project/project-context.md
```

### 如果文件缺失或过时

**请生成或更新它：**
```bash
# Option 1: Generate from codebase
bash pty:true workdir:~/project command:"claude '/bmad-bmm-generate-project-context'"

# Option 2: Update manually with user's latest direction
# Ask user: "What's the current vision for this project?"
# Then create/update project-context.md with that info
```

### 用户改变计划时

如果用户在项目进行过程中改变方向（例如添加新功能或调整方向）：
1. 更新`project-context.md`以反映新的需求
2. 如果架构受到影响，重新生成`architecture.md`
3. 根据更新后的上下文继续执行任务

---

## 安全读取故事内容

**不要一次性加载所有故事！** 请按照以下步骤操作：

1. **先列出所有故事：**
   ```bash
   ls _bmad-output/epics/*/stories/
   ```

2. **在阅读每个故事之前先检查其标题：**
   ```bash
   head -10 _bmad-output/epics/*/stories/story-*.md
   ```

3. **逐个阅读故事并创建相应的OCM任务：**
   - 阅读故事1 → 创建OCM任务
   - 阅读故事2 → 创建OCM任务
   - 依此类推

4. **批量处理时**，按故事所属的epic分类：
   ```bash
   for f in _bmad-output/epics/*/stories/*.md; do head -20 "$f"; done | head -100
   ```

## 命令链的安全性

### ❌ 避免这种操作（可能导致意外失败）

```bash
claude "/bmad-cmd1 && /bmad-cmd2"  # If cmd1 fails, cmd2 still runs
```

### ✅ 建议按顺序执行命令

**规则：** 在执行下一步之前，请务必验证每个步骤的正确性。

---

## 故障恢复

**场景：** Claude Code出现故障（例如API错误500、超时或进程被终止）

### 第一步：终止异常进程（在重启之前！）

**⚠️ 必须先检查是否存在异常进程：**

```bash
# Check if Claude is still running
ps aux | grep claude

# Kill any zombie processes for this project
pkill -f "claude.*projects/roundvision" || echo "No zombie processes"

# Also kill any hanging node processes
pkill -f "npx.*bmad" || echo "No zombie npx"
```

### 第二步：检查生成的内容

1. **查看生成了哪些文件：**
   ```bash
   ls -lt _bmad-output/*.md | head -10
   ```

2. **找到最新的有效文件：**
   ```bash
   # Read the most recently modified output
   ls -t _bmad-output/*.md | head -1 | xargs head -30
   ```

3. **从上次停止的位置继续执行：**
   - 如果`architecture.md`存在但`stories/`目录缺失，则重新生成故事相关文件
   - 如果`stories/`目录存在但OCM任务缺失，则根据现有故事创建任务
   - 如果输出不完整，则仅重新生成缺失的部分

4. **如果已有部分输出，请勿从头开始重新启动**

---

## 处理Claude Code的请求

当Claude Code在执行过程中提出问题时：

1. **首先查看日志**（使用`process action:log sessionId:XXX`）
2. **如果知道答案**，通过`process action:submit`提供答案
3. **如果需要用户协助**，请暂停并获取更多信息
4. **如果Claude Code无法继续执行，请让它再次请求所需信息**

**示例：**
```bash
# Claude asks: "What's your preferred authentication provider?"
# If you don't know → ask user: "Claude needs to know auth provider - Auth0, Firebase, or Supabase?"

# Then provide the answer:
process action:submit sessionId:XXX data:"Auth0"
```

## 何时使用BMad，何时直接使用coding-agent

### 适用场景：**
- 新功能或大型项目的架构调整
- 使用BMad进行冲刺计划和故事生成
- 需要生成技术文档（如产品需求文档、架构设计）
- 任何涉及安全性的任务

### 适用场景（直接使用coding-agent）：

- 快速修复和简单修改
- 简单的代码审查
- 单个文件的修改
- 实验或原型设计

**经验法则：** 如果需要详细的故事分解和冲刺计划，请使用BMad；如果是简单的编辑工作，则直接使用coding-agent。**

---

## BMad输出文件的阅读

BMad工作流程完成后，相关文档会保存在以下路径：

```
project/
├── _bmad/
│   └── config.yaml
├── _bmad-output/
│   ├── brainstorming-report.md
│   ├── product-brief.md
│   ├── PRD.md
│   ├── ux-spec.md
│   ├── architecture.md
│   ├── epics/
│   │   └── epic-[name]/
│   │       └── stories/
│   │           └── story-[slug].md
│   └── sprint-status.yaml
└── project-context.md
```

**⚠️ 在每次执行完工作流程后，请使用`ls _bmad-output/`或`ls -R _bmad-output/`确认文件是否存在。**

**在阅读之前，请验证文件内容的有效性：**
```bash
# Quick check
ls -la _bmad-output/architecture.md

# Validate content
head -20 _bmad-output/architecture.md

# Check for errors
grep -i "error\|fail" _bmad-output/architecture.md
```

### 缓存更新

**注意：** Claude Code修改源代码后，缓存内容可能会失效！

**规则：** 每次Claude Code成功修改源代码后：
1. **不要假设** 之前的文件内容仍然有效
2. **如果需要继续处理文件，请重新读取**
3. **清除缓存**，确保读取的是最新的文件内容

```bash
# Bad: Assuming old read is still valid
read path:"~/project/src/auth.js"  # ❌ May be outdated

# Good: Read fresh after Claude modified it
exec command:"cat ~/project/src/auth.js"  # ✅ Fresh content
```

## 验证步骤

在进入实施阶段之前：

1. 阅读生成的`architecture.md`（或快速开发模式的`tech-spec.md`）
2. 确认内容是否符合用户的原始需求
3. 如果内容不一致，请重新生成文件或与用户确认

## 错误处理

| 错误类型 | 处理方法 |
|-------|----------|
| 命令未找到 | 检查环境变量`PATH`和`which claude` |
| `npx: 命令未找到` | 安装Node.js 20+版本 |
| `_bmad/ 未找到` | 先运行`npx bmad-method install` |
| Claude Code在权限处理时卡住 | 使用`--dangerously-skip-permissions` |
| API错误500 | 触发故障恢复机制（参见“故障恢复”部分） |
| 进程超时 | 检查进程是否仍在运行，必要时重新启动**

### 安全注意事项
- **切勿通过Claude Code执行`rm -rf`等命令，除非得到明确授权**
- **对于涉及安全性的更改，切勿使用快速开发模式**
- **对于Git提交操作，建议用户明确选择“n”**

---

## Git提交处理

Claude Code通常会询问：“您是否要提交这些更改？[y/N]”

- **如果用户希望保留Git控制权，请回复“n”**
- **只有在用户明确要求完全自主提交时，才回复“y”**

```bash
# When Claude asks to commit, default to "n"
process action:submit sessionId:XXX data:"n"
```

## 示例

### 示例1：架构分析 + 产品简报（顺序执行）

**用户请求：**“分析PingRoot项目的当前架构并生成产品简报”

**代理执行步骤：**
```bash
# 1. Pre-flight check
ls ~/projects/pingroot/_bmad/ || echo "Need to install BMad"

# 2. Check/update project-context.md
ls ~/projects/pingroot/project-context.md || echo "Need to create project-context.md"

# 3. Launch architecture workflow
bash pty:true workdir:~/projects/pingroot background:true command:"claude --dangerously-skip-permissions '/bmad-bmm-create-architecture'"

# 4. Monitor, wait for completion
process action:poll sessionId:XXX

# 5. Verify output
ls _bmad-output/architecture.md
head -20 _bmad-output/architecture.md
grep -i "error" _bmad-output/architecture.md || echo "OK"

# 6. If OK, verify coherence with user request
# 7. If coherent, launch product brief
bash pty:true workdir:~/projects/pingroot command:"claude --dangerously-skip-permissions '/bmad-bmm-create-product-brief'"

# 8. Deliver outputs
```

### 示例2：冲刺准备 + OCM任务生成（包含安全检查）

**用户请求：**“为RoundVision项目准备冲刺计划，并将任务添加到OCM”

**代理执行步骤：**
```bash
# 1. Pre-flight check
ls ~/projects/roundvision/_bmad/ || npx bmad-method install

# 2. Check project-context.md
ls ~/projects/roundvision/project-context.md || echo "Update this first!"

# 3. Launch sprint planning + story creation
bash pty:true workdir:~/projects/roundvision background:true command:"claude --dangerously-skip-permissions '/bmad-bmm-sprint-planning && /bmad-bmm-create-epics-and-stories'"

# 4. Monitor and wait for completion
process action:poll sessionId:XXX  # repeat until done

# 5. Refresh context - verify files exist
ls -R ~/projects/roundvision/_bmad-output/epics/

# 6. List stories first (don't dump all at once!)
ls ~/projects/roundvision/_bmad-output/epics/*/stories/

# 7. Read and process stories one by one
for story in ~/projects/roundvision/_bmad-output/epics/*/stories/*.md; do
  echo "=== $(basename $story) ==="
  head -20 "$story"
  # Create OCM task from this story
done

# 8. Report: "Created X tasks in OCM for Sprint 1"
#    IMPORTANT: Each OCM task must include story path as reference!
```

### 示例3：快速修复（无需使用BMad）

**用户请求：**“修复登录页面的拼写错误”

**代理执行步骤：**
```bash
# Direct coding-agent, no BMad workflow needed
bash pty:true workdir:~/projects/login command:"claude 'Fix the typo on line 42: \"Passowrd\" → \"Password\"'"
```

### 示例4：故障恢复**

**场景：** Claude Code在生成故事时崩溃**

**代理执行步骤：**
```bash
# 0. Cleanup zombies FIRST!
ps aux | grep claude
pkill -f "claude.*projects/roundvision" || echo "Clean"

# 1. Check what was generated
ls -lt ~/project/_bmad-output/ | head -10

# 2. Find last valid file
ls -t ~/project/_bmad-output/epics/*/stories/ | head -1

# 3. Check if partial stories exist
ls ~/project/_bmad-output/epics/*/stories/*.md | wc -l

# 4. If partial → resume from last point
# If 3 stories out of 5 → generate remaining 2
# If 0 stories → restart story generation

# 5. Continue without restarting from zero
```

## ⚠️ 重要提示：子代理的权限设置

**子代理（minion）没有自动访问项目文件的权限！** 在分配任务时，必须提供以下信息：

### 1. 项目目录的访问权限**

```bash
# Minion needs workdir to access project files
sessions_spawn workdir:"~/projects/roundvision" ...
```

### 2. 相关的故事内容、项目上下文和架构信息

**⚠️ 绝不能仅提供故事内容！** 例如，如果任务是添加登录按钮，需要提供以下信息：
- 使用的编程语言（React、Vue还是原生JavaScript）
- 是否使用了Tailwind或Bootstrap框架
- 现有的认证机制是什么

**必须提供的信息包括：**
- **任务内容**（需要构建的具体功能）
- **project-context.md**（项目规则和技术栈信息）
- **architecture.md**（技术决策相关内容）

```bash
# Step 1: Read all three
cat ~/projects/roundvision/project-context.md
cat ~/projects/roundvision/_bmad-output/architecture.md  
cat ~/projects/roundvision/_bmad-output/epics/auth.md

# Step/stories/story-login 2: Combine into a comprehensive prompt
sessions_spawn task:"You are implementing this story: [STORY]. 
Project context: [CONTEXT].
Architecture: [ARCHITECTURE].
Follow the patterns defined in architecture.md."
```

### 3. OCM任务中必须包含故事链接

**⚠️ 如果没有这些信息，子代理将无法执行任务！**

---

## 备注

- **BMad用于头脑风暴时请谨慎使用**。OpenClaw本身具有强大的头脑风暴功能，对于技术性的结构化工作，建议使用BMad来辅助决策。
- BMad生成的文件保存在 `_bmad-output/` 目录下
- 请确保`project-context.md`始终是最新的
- 使用`/bmad-help`可以获得交互式指导
- 使用`pty:true`选项启动Claude Code
- 根据需求选择合适的模型（`sonnet`、`haiku`或`opus`）
- 对于简单任务，建议直接使用coding-agent；对于复杂的工作流程，再使用BMad
- 在执行多个步骤之前，请务必逐一验证每个步骤的正确性

---

## 相关技能

- **coding-agent**：启动Claude Code所必需的技能
- **task-manager**：用于根据BMad生成的结果创建OCM任务