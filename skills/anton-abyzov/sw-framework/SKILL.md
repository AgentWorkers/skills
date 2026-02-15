---
name: framework
description: **SpecWeave框架结构、规则及规范驱动开发惯例专家**  
适用于学习SpecWeave的最佳实践、理解其增量开发生命周期（incremental lifecycle），或配置相关钩子（hooks）。内容涵盖“单一事实来源”（source-of-truth）原则、`tasks.md`/`spec.md`文件格式、动态文档同步（living docs sync）以及文件组织模式（file organization patterns）。
allowed-tools: Read, Grep, Glob
---

# SpecWeave框架专家

我是SpecWeave框架的专家——这是一个基于规范驱动的开发框架，专为Claude Code（以及其他AI编码助手）设计。我对它的结构、规则、惯例和最佳实践有着深入的了解。

## 核心理念

SpecWeave遵循**规范驱动的开发**模式，并采用**增量式工作流程**：

1. **规范先行**——在讨论如何实现之前，先明确“做什么”以及“为什么这样做”。
2. **增量交付**——每次只发布一个完整的功能模块。
3. **动态文档**——文档会通过自动化脚本实时更新。
4. **单一事实来源**——所有代码和配置都存储在同一个地方，避免重复。
5. **多工具支持**——兼容Claude、Cursor、Copilot等多种AI编码助手。

## 增量式开发

### 什么是增量？

一个增量指的是一个完整的功能模块，它包含以下文件：
- `spec.md`：产品需求（“做什么”以及“为什么这样做”）——**必需**。
- `plan.md`：技术实现方案——**可选**，仅针对复杂的功能。
- `tasks.md`：任务分解列表——**必需**。
- `metadata.json`：任务状态跟踪——**必需**。

> **何时可以省略`plan.md`**：在修复漏洞、进行简单迁移、发布热修复或执行`spec.md`中已经详细描述的任务时。

### `spec.md`的必填字段

**重要提示**：`spec.md`的YAML头部必须包含项目名称（对于二级结构的项目，还需包含项目所属的板名称）：

```yaml
# 1-level structure (single-project or multiProject):
---
increment: 0001-feature-name
project: my-project          # REQUIRED
---

# 2-level structure (ADO area paths, JIRA boards, umbrella teams):
---
increment: 0001-feature-name
project: acme-corp           # REQUIRED
board: digital-operations    # REQUIRED for 2-level
---
```

**为什么这样要求？**这样可以确保增量文件被正确地添加到文档系统中。如果没有明确的项目/板名称，同步过程可能会出错，导致规范文件被放置到错误的文件夹中。

**检测方法**：使用`src/utils/structure-level-detector.ts`来判断项目是采用一级结构还是二级结构。

**参见**：[ADR-0190](/internal/architecture/adr/0190-spec-project-board-requirement.md)

### 增量命名规则

**重要规则**：所有增量的名称都必须具有描述性，不能仅使用数字！

**命名格式**：`####-描述性-kebab-case-name`（例如：`0001-core-framework`）

**示例**：
- ✅ `0001-core-framework`  
- ✅ `0002-core-enhancements`  
- ✅ `0003-intelligent-model-selection`  
- ✅ `0004-plugin-architecture`  
- ✅ `0006-llm-native-i18n`  
- ❌ `0003`（过于通用，会被拒绝！）  
- ❌ `0004`（没有描述性，也会被拒绝！）

**理由**：
- 便于一目了然地理解增量的用途。  
- 在交流中更容易引用。  
- 有助于维护清晰的Git版本历史记录。  
- 可以通过名称快速搜索相关内容。  
- 增量文件夹本身就是一个很好的文档来源。

### 增量生命周期

```
1. Plan    → /sw:inc "feature-name"
            ↓ PM agent creates spec.md, plan.md, tasks.md, tests.md

2. Execute → /sw:do
            ↓ Selects next task, executes, marks complete

3. Validate → /sw:validate 0001
            ↓ Checks spec compliance, test coverage

4. Close   → /sw:done 0001
            ↓ Creates COMPLETION-SUMMARY.md, archives
```

### 增量开发规则

**铁律**：在当前增量未完成之前，不得开始下一个增量的工作！

**执行方式**：
- 如果之前的增量尚未完成，`/sw:inc`命令会阻止新的增量启动。
- 使用`/sw:status`命令查看所有增量的状态。
- 使用`/sw:close`命令关闭未完成的工作。
- 在紧急情况下可以使用`--force`标志（但应谨慎使用）。

**“已完成”的定义**：
- `tasks.md`中的所有任务都被标记为`[x] Completed`。
- 或者存在`COMPLETION-SUMMARY.md`文件，并且状态为“✅ COMPLETE”。
- 或者通过`/sw:close`命令明确关闭了增量。

**关闭增量的三种方式**：
1. **调整范围**：从`spec.md`中移除相关功能，并重新生成任务列表。
2. **转移范围**：将未完成的任务转移到下一个增量中。
3. **扩展现有增量**：更新`spec.md`，添加新的任务，继续在同一增量中工作。

**示例**：
```bash
# Check status
/sw:status
# Shows: 0002 (73% complete), 0003 (50% complete)

# Try to start new increment
/sw:inc "0004-new-feature"
# ❌ Blocked! "Close 0002 and 0003 first"

# Close previous work
/sw:close
# Interactive: Choose force-complete, move tasks, or reduce scope

# Now can proceed
/sw:inc "0004-new-feature"
# ✅ Works! Clean slate
```

## 目录结构

### 根目录`.specweave/`（必需）

**重要规则**：SpecWeave仅支持根目录下的`.specweave/`文件夹。

**正确的结构**：
```
my-project/
├── .specweave/              ← ONE source of truth (root-level)
│   ├── increments/
│   │   ├── 0001-core-framework/
│   │   │   ├── spec.md
│   │   │   ├── plan.md
│   │   │   ├── tasks.md
│   │   │   ├── tests.md
│   │   │   ├── logs/        ← Session logs
│   │   │   ├── scripts/     ← Helper scripts
│   │   │   └── reports/     ← Analysis files
│   │   └── _backlog/
│   ├── docs/
│   │   ├── internal/        ← Strategic docs (NEVER published)
│   │   │   ├── strategy/    ← Business strategy
│   │   │   ├── architecture/ ← ADRs, RFCs, diagrams
│   │   │   └── delivery/    ← Implementation notes
│   │   └── public/          ← User-facing docs (can publish)
│   └── logs/
├── frontend/
├── backend/
└── infrastructure/
```

**错误的结构**（嵌套的`.specweave/`文件夹是不被支持的）：
```
my-project/
├── .specweave/              ← Root level
├── backend/
│   └── .specweave/          ← ❌ NESTED - PREVENTS THIS!
└── frontend/
    └── .specweave/          ← ❌ NESTED - PREVENTS THIS!
```

**为什么只能使用根目录？**
- ✅ 确保所有代码和配置都存储在同一个地方，避免重复和混乱。
- ✅ 便于管理和维护。
- ✅ 有助于简化文档的同步过程。

**多仓库解决方案**：
对于包含多个仓库的大型项目，可以创建一个**父文件夹**：
```
my-big-project/              ← Create parent folder
├── .specweave/              ← ONE source of truth for ALL repos
├── auth-service/            ← Separate git repo
├── payment-service/         ← Separate git repo
├── frontend/                ← Separate git repo
└── infrastructure/          ← Separate git repo
```

## 单一事实来源原则

**重要原则**：SpecWeave有严格的单一事实来源规则！

### 三个目录及其用途

```
src/                         ← SOURCE OF TRUTH (version controlled)
├── skills/                  ← Source for skills
├── agents/                  ← Source for agents
├── commands/                ← Source for slash commands
├── hooks/                   ← Source for hooks
├── adapters/                ← Tool adapters (Claude/Cursor/Copilot/Generic)
└── templates/               ← Templates for user projects

.claude/                     ← INSTALLED (gitignored in user projects)
├── skills/                  ← Installed from src/skills/
├── agents/                  ← Installed from src/agents/
├── commands/                ← Installed from src/commands/
└── hooks/                   ← Installed from src/hooks/

.specweave/                  ← FRAMEWORK DATA (always present)
├── increments/              ← Feature development
├── docs/                    ← Strategic documentation
└── logs/                    ← Logs and execution history
```

### 重要规则

1. **务必在`src/`目录中编辑所有文件**——这是所有代码和配置的存储位置。
2. **运行安装脚本`install`以将更改同步到`.claude/`目录。
3. **严禁直接编辑`.claude/`目录中的文件**——否则会导致文件被覆盖。
4. **严禁在项目根目录下创建新文件**——请使用增量文件夹。

**示例工作流程**：
```bash
# CORRECT: Edit source
vim src/skills/increment-planner/SKILL.md

# Sync to .claude/
npm run install:skills

# Test (skill activates from .claude/)
/sw:inc "test feature"

# WRONG: Edit installed file
vim .claude/skills/increment-planner/SKILL.md  # ❌ Gets overwritten!
```

### 文件组织规则

**允许放在根目录下的文件**：
- `CLAUDE.md`（项目配置文件）
- `README.md`、`CHANGELOG.md`、`LICENSE`（文档文件）
- 标准配置文件（`package.json`、`tsconfig.json`、`.gitignore`）
- 构建生成的文件（`dist/`，仅在临时需要时使用）

**严禁放在根目录下的文件**：
所有由AI生成的文件都必须放在增量文件夹中：

```
❌ WRONG:
/SESSION-SUMMARY-2025-10-28.md          # NO!
/ADR-006-DEEP-ANALYSIS.md               # NO!
/ANALYSIS-MULTI-TOOL-COMPARISON.md      # NO!

✅ CORRECT:
.specweave/increments/0002-core-enhancements/
├── reports/
│   ├── SESSION-SUMMARY-2025-10-28.md
│   ├── ADR-006-DEEP-ANALYSIS.md
│   └── ANALYSIS-MULTI-TOOL-COMPARISON.md
├── logs/
│   └── execution-2025-10-28.log
└── scripts/
    └── migration-helper.sh
```

**为什么这样规定？**
- ✅ 可以完全追踪每个增量创建了哪些文件。
- ✅ 清理起来非常方便（删除增量文件夹即可删除所有相关文件）。
- ✅ 有助于保持文件结构的清晰性。
- ✅ 避免根目录变得杂乱无章。

## 钩子系统

### 什么是钩子？

钩子是会在SpecWeave事件发生时自动执行的Shell脚本：
- `post-task-completion`：每个任务完成后触发。
- `pre-task-plugin-detect`：任务执行前触发（用于检测是否需要插件）。
- `post-increment-plugin-detect`：增量创建后触发。
- `pre-implementation`：实施开始前触发。

### 当前的`post-task-completion`钩子

**触发条件**：每次`TodoWrite`命令执行完成后都会触发。

**功能**：
- ✅ 检测会话是否结束（基于用户15秒内的活动情况）。
- ✅ 播放完成通知音效（macOS/Linux/Windows系统）。
- ✅ 显示完成提示信息。
- ✅ 将日志记录到`.specweave/logs/hooks-debug.log`文件中。
- ✅ 防止重复触发（每次触发之间有2秒的延迟）。

**目前尚未实现的功能**：
- ✳ 自动更新`tasks.md`中的任务完成状态。
- ✳ 自动同步文档。
- ✳ 合并GitHub和Jira中的任务信息。
- ✳ 计算增量的完成百分比。

### 智能会话结束检测机制
```
Problem: Claude creates multiple todo lists → sound plays multiple times
Solution: Track inactivity gaps between TodoWrite calls
- Rapid completions (< 15s gap) = Claude still working → skip sound
- Long gap (> 15s) + all done = Session ending → play sound!
```

### 钩子配置

**配置文件**：`.specweave/config.json`

```json
{
  "hooks": {
    "post_task_completion": {
      "enabled": true,
      "update_tasks_md": false,
      "sync_living_docs": false,
      "play_sound": true,
      "show_message": true
    }
  }
}
```

### 手动操作

在钩子完全自动化之前，**你必须**：
- 当项目结构发生变化时，更新`CLAUDE.md`文件。
- 当用户界面相关的内容发生变化时，更新`README.md`文件。
- 当API相关的内容发生变化时，更新`CHANGELOG.md`文件。
- 手动更新`tasks.md`中的任务完成状态（或谨慎使用`TodoWrite`命令）。

## 插件架构

### 核心组件与插件

**核心组件**（始终会被加载）：
- 8个核心功能模块（增量规划器、规范生成器、上下文加载器等）。
- 3个核心代理（项目经理、架构师、技术负责人）。
- 7个核心命令（`/sw:inc`、`/sw:do`等）。

**插件**（可选）：
- `specweave-github`：与GitHub集成（用于同步问题和建议创建PR）。
- `specweave-jira`：与Jira集成（用于同步任务）。
- `specweave-kubernetes`：用于Kubernetes部署。
- `specweave-frontend-stack`：用于React/Vue/Angular框架的集成。
- `specweave-ml-ops`：用于机器学习相关的功能。

### 插件对性能的影响

**插件启用前的情况**：
- 简单的React应用程序：需要约50K个系统资源。
- 后端API：需要约50K个系统资源。
- 机器学习管道：需要约50K个系统资源。

**插件启用后的情况**：
- 简单的React应用程序：核心组件 + 前端框架 + GitHub集成约需要16K个系统资源（减少了68%）。
- 后端API：核心组件 + Node.js后端 + GitHub集成约需要15K个系统资源（减少了70%）。
- 机器学习管道：核心组件 + 机器学习相关功能 + GitHub集成约需要18K个系统资源（减少了64%）！

### 插件检测流程

1. **初始化时**：扫描`package.json`文件、目录结构和环境变量，建议是否启用某些插件。
2. **创建新增量时**：分析增量描述中的关键词，建议是否需要某些插件。
3. **任务执行前**：检查任务描述，提示是否需要相关插件。
4. **增量创建后**：检查Git变更，建议是否需要新的插件。

### 混合式插件系统

SpecWeave插件支持两种部署方式：
1. **NPM包**：通过`npm install -g specweave`安装，然后使用`specweave plugin install sw-github`进行配置。
2. **Claude Code内置插件市场**：通过`/plugin marketplace add`命令安装插件（适用于Claude Code用户）。

**插件所需的文件**：
- `plugin.json`：Claude Code内置的插件格式。
- `manifest.json`：SpecWeave自定义的插件格式（包含更详细的元数据）。

## 多工具支持

SpecWeave兼容多种AI编码助手：

### Claude Code（评分：⭐⭐⭐⭐⭐ 100%兼容）
- 支持原生安装。
- 自动激活相关功能模块。
- 钩子会自动执行。
- 命令能够直接在Claude Code中使用。
- 代理能够隔离不同功能的上下文。

### Cursor 2.0（评分：⭐⭐⭐⭐ 85%兼容）
- 支持`AGENTS.md`文件的编译。
- 可通过仪表板执行团队命令。
- 提供`@context`快捷键。
- 支持多代理并行执行任务。

### GitHub Copilot（评分：⭐⭐⭐ 60%兼容）
- 需要编译`.github/copilot/instructions.md`文件。
- 需要手动编写指令。
- 不支持钩子或命令行操作。

### Generic（评分：⭐⭐ 40%兼容）
- 需要手动编辑`SPECWEAVE-MANUAL.md`文件。
- 所有操作都需要手动完成。

**推荐使用**：建议使用Claude Code，因为它提供了更好的使用体验。

## 关键命令

### 增量生命周期相关命令
- `/sw:inc "feature-name"`：规划新的增量。
- `/sw:do`：执行下一个任务。
- `/sw:progress`：显示进度信息。
- `/sw:validate 0001`：验证规范文件、执行测试并检查质量。
- `/sw:done 0001`：关闭当前增量。
- `/sw:next`：如果条件满足，自动关闭当前增量并建议下一个任务。

### 增量管理相关命令
- `/sw:status`：显示所有增量及其完成状态。
- `/sw:close`：交互式关闭未完成的增量。

### 文档同步相关命令
- `/sw:sync-docs review`：在实施前审查文档。
- `/sw:sync-docs update`：从已完成的增量中更新文档。

### 外部平台同步相关命令
- `/sw:sync-github`：与GitHub进行双向同步。
- `/sw:sync-jira`：与Jira进行双向同步。

### 常见问题解答

### 问：在哪里创建新的增量？
**答**：使用`/sw:inc "####-描述性名称"`命令。

### 问：分析文件应该放在哪里？
**答**：放在增量的`reports/`文件夹中。

### 问：如何查看剩余的任务？
**答**：使用`/sw:progress`命令或查看`.specweave/increments/####/tasks.md`文件。

### 问：可以在当前增量未完成时开始新的增量吗？
**答**：不可以！框架会阻止这样做。请使用`/sw:status`查看进度，使用`/sw:close`关闭当前增量。

### 问：在哪里编辑功能模块、代理或命令？
**答**：在`src/`目录中编辑相关文件，然后运行`npm run install:all`将更改同步到`.claude/`目录。

### 问：如何判断是否需要插件？
**答**：SpecWeave会自动检测并提示是否需要插件。

### 问：为什么钩子会播放声音？
**答**：这是为了检测会话是否结束。如果所有任务都已完成且用户超过15秒没有操作，系统会认为用户已完成工作。这个设置可以在`.specweave/config.json`中修改。

### 问：如何禁用某个钩子？
**答**：编辑`hooks/hooks.json`文件，将对应的钩子的`enabled`字段设置为`false`。

## 常见问题解答（关于SpecWeave的使用）

当您询问关于SpecWeave的规则、命名规范、增量生命周期、文件存放位置、单一事实来源、钩子系统、插件架构等方面的问题时，我会为您提供详细的解答。

希望这些信息能帮助您更好地理解和使用SpecWeave！🚀