---
name: antigravity-bridge
version: 1.2.2
description: >
  **从 Google Antigravity IDE 到 OpenClaw 的单向知识传输机制**  
  该机制能够将项目开发过程中的相关信息实时传输到 OpenClaw 中，同时不会取代 Antigravity 作为主要的代码编辑工具。Antigravity 具备对项目代码库的深入理解（包括代码编辑、代码提示、代码跟踪、注释等功能），而 OpenClaw 则具备更广泛的功能（如 24/7 可用性、跨项目协作支持、业务运营管理、监控以及通信能力）。该知识传输机制可同步以下内容：  
  - 知识点（.agent/knowledge/）  
  - 任务信息（.agent/tasks/）  
  - 经验总结（.agent/memory/）  
  - 规则设置  
  - 技能信息  
  - 工作流程  
  - 会话数据  
  **适用场景：**  
  1. 将 Antigravity 中的知识同步到 OpenClaw 环境中  
  2. 分析任务以生成后续任务建议  
  3. 实现跨工具的自我优化（同时更新两个系统）  
  4. 查看 Antigravity 会话产生的结果  
  **不适用场景：**  
  - 作为主要的代码编辑工具（请继续使用 Antigravity）  
  - 配置模型或服务提供者相关操作  
  - 启动 IDE（请使用 `agy` 命令行工具）
  One-directional knowledge bridge from Google Antigravity IDE to OpenClaw.
  Keeps the OpenClaw agent informed about project development without replacing
  Antigravity as the primary coding agent. Antigravity has deep codebase awareness
  (IDE, LSP, vectors, code tracker, annotations) — OpenClaw has breadth (24/7 availability,
  cross-project awareness, business ops, monitoring, communications).
  The bridge syncs: Knowledge Items, tasks (.agent/tasks.md), lessons learned
  (.agent/memory/), rules, skills, workflows, and session handoffs.
  Use when: (1) syncing Antigravity knowledge to OpenClaw context,
  (2) analyzing tasks for next-task recommendations,
  (3) running cross-agent self-improve (updates both systems),
  (4) checking what Antigravity sessions produced,
  (5) user says "sync antigravity", "pick task", "what did antigravity do",
  "bridge sync", or "antigravity status".
  NOT for: primary coding (use Antigravity), model/provider config,
  or starting the IDE (use `agy` CLI).
homepage: https://github.com/heintonny/antigravity-bridge
metadata: {"openclaw":{"emoji":"🌉","tags":["antigravity","gemini","knowledge-sync","multi-agent","bridge","ide","tasks","coding"]}}
---
# **Antigravity Bridge**  
这是一个用于在 OpenClaw 与 Google Antigravity IDE 之间实现双向知识同步的工具。两个系统共享相同的知识库、任务和学习内容，因此无需手动进行数据同步。  

## **先决条件**  
- 已安装 Google Antigravity IDE（并包含 `~/.gemini/antigravity/` 目录）  
- 项目必须包含 `.agent/` 目录（Antigravity 的标准代理配置文件）  
- 确保系统已安装 Python 3.10 或更高版本（用于同步脚本的运行）。  

## **配置**  
在使用前，请创建一个配置文件：  
```bash
python3 "$(dirname "$0")/scripts/configure.py"
```  
或者手动创建 `~/.openclaw/antigravity-bridge.json` 文件：  
```json
{
  "knowledge_dir": "~/.gemini/antigravity/knowledge",
  "project_dir": "~/path/to/your/project",
  "agent_dir": "~/path/to/your/project/.agent",
  "gemini_md": "~/path/to/your/project/.gemini/GEMINI.md",
  "auto_commit": false
}
```  

## **同步命令——核心工作流程**  
### **执行同步**  
执行同步命令后，系统会将同步结果以结构化 JSON 格式输出到标准输出（stdout）中，内容包含两个部分：  
- `diff`：自上次同步以来发生的变化（如果没有之前的同步记录，则显示“首次同步”信息）  
- `current`：当前 Antigravity 系统的完整状态快照。  

系统状态会保存在 `~/.openclaw/workspace/antigravity-sync-state.json` 文件中。  

### **同步后的代理职责**  
**同步后的更新工作由代理负责，而非同步脚本本身**：  
执行同步脚本后，代理必须：  
1. **读取 JSON 输出结果**，重点关注 `diff` 部分。  
2. **如果 `diff.is_first_sync` 为 `true` 或 `diff.summary` 显示有变化**：  
   - 更新 `MEMORY.md` 文件，记录重要的变更内容：  
     - 任务数量的变化（已完成/待办任务的增减）  
     - 新增或删除的知识项（KI）  
     - 新的活跃任务或任务阶段的变更  
     - 新的学习内容（来自内存文件）  
   - 在 `memory/YYYY-MM-DD.md` 文件中添加同步日志记录：  
     ```
     HH:MM — Antigravity Bridge sync: <diff.summary>
     ```  
3. **如果 `diff.summary` 显示“自上次同步以来没有变化”**：  
   - 无需进行任何更新；可选地记录同步尝试日志。  

### **数据存储位置**  
| 变更类型 | 目录 | 更新内容 |  
|---|---|---|  
| 任务数量变化 | `MEMORY.md` → `CodePact` 部分 | 更新已完成/待办任务的数量 |  
| 新的活跃任务 | `MEMORY.md` → `Current Phase` 部分 | 更新活跃任务的详细信息 |  
| 新的知识项 | `MEMORY.md` → `CodePact` 部分 | 记录新知识项的名称 |  
| 新的内存/学习文件 | `MEMORY.md` → 相关部分 | 总结关键学习内容 |  
| 新的规则/技能/工作流程 | `MEMORY.md` → `CodePact` 部分 | 更新知识库中的相关条目 |  
| 会话交接信息 | `MEMORY.md` → `CodePact` 部分 | 记录当前的交接情况 |  
| 任何同步事件 | `memory/YYYY-MM-DD.md` | 添加带有时间戳的日志记录 |  

### **禁止的操作**  
- **禁止** 创建独立的参考文档（如 `ANTIGRAVITY.md` 或 `antigravity-sync.md`）。  
- **禁止** 将原始的同步数据直接写入文件——应将其整合到 `MEMORY.md` 中。  
- **禁止** 询问用户是否需要更新 `MEMORY.md`——系统会自动完成更新。  

## **其他命令**  
### **显示任务变化 (`diff`)**  
该命令用于显示自上次同步以来任务内容的变化：  
```bash
python3 scripts/diff_tasks.py
```  

### **选择下一个任务 (`pick-task`)**  
该命令类似于 Antigravity 的 `/next-task` 功能，用于收集项目背景信息以辅助任务选择：  
```bash
python3 scripts/pick_task.py
```  
该命令会输出结构化的 JSON 数据（不会修改 `tasks.md` 文件）。代理会根据这些数据来推荐合适的任务。  

**代理在执行 `pick-task` 后的工作流程：**  
1. 读取 JSON 输出内容（包括任务、Git 日志和会话信息）。  
2. 分析：  
   - 需要完成的活跃任务  
   - 来自 Antigravity 的会话交接信息  
   - 最近的提交记录  
   - 阻碍项目进展的环节  
3. 向用户推荐 2-3 个任务，提供以下信息：  
   - 任务背景  
   - 任务范围  
   - 需要投入的努力程度（简单/中等/复杂）  
4. 以编号形式向用户展示推荐任务：  
   ```
   🎯 Recommended Next Tasks — Reply 1, 2, or 3

   ### Option 1: [Task Name] ⭐
   - Context: ...
   - Scope: ...
   - Effort: Medium

   ### Option 2: [Task Name]
   ...
   ```  
5. 用户选择任务后，代理会在 `tasks.md` 文件中标记该任务为活跃状态（`[>]`）。  
6. 代理会启动一个子代理来执行任务，提供任务的相关信息（规则、所需知识项等）。  
7. 任务完成后，用户需在任务状态标记为 `[x]`，然后代理会执行自我优化流程。  

**任务优先级排序：**  
1. 活跃但未完成的任务  
2. 可以解除阻碍的其他任务  
3. 需要快速完成的任务（低难度、高价值）  
4. 存在技术问题的任务（在审计或学习记录中标记）  
5. 符合当前工作阶段的下一步任务  

### **自我优化 (`self-improve`)**  
该命令用于同步两个知识系统中的学习内容：  
```bash
python3 scripts/self_improve.py --topic "<topic>" --lesson "<what was learned>"
```  
具体操作包括：  
1. **更新 OpenClaw 系统中的 `MEMORY.md` 和 `memory/YYYY-MM-DD.md` 文件**。  
2. **更新 Antigravity 系统中的内容**：  
   - 创建/更新 `.agent/memory/lessons-learned-<topic>.md` 文件  
   - 在 `knowledge/<topic>/artifacts/` 目录中创建/更新知识项文件  
   - 更新 `metadata.json` 和 `timestamps.json` 文件  
   （可选：将更改提交到版本控制系统）  

### **写入知识项 (`write-ki`)**  
该命令用于直接将学习内容写入 Antigravity 的原生知识管理系统：  
```bash
python3 scripts/write_ki.py \
  --topic "my_topic" \
  --title "My Topic" \
  --summary "What this knowledge covers" \
  --artifact "pattern_name" \
  --content "# Pattern\n\nDetailed content here..."
```  

### **创建 Antigravity 技能 (`create-agy-skill`)**  
该命令用于在 OpenClaw 与 Antigravity 之间创建双向技能关联：  
```bash
python3 scripts/create_agy_skill.py --project-dir ~/path/to/project
```  

## **系统架构**  
整个系统基于以下文件结构运行：  
`~/.openclaw/workspace/antigravity-sync-state.json` 文件用于记录同步状态，包括：  
- 最后一次同步的时间戳  
- 知识项的哈希值及数量  
- 任务文件的哈希值及数量  
- 内存/规则/技能/工作流程文件的哈希值  
这种设计使得无需使用 Markdown 格式进行差异对比即可准确检测变化。  

## **安全与隐私**  
- **所有数据均存储在本地**，不涉及任何外部 API 调用或云同步。  
- 脚本仅在配置的目录内读写文件。  
- 无需用户提供任何凭证或令牌。  
- 该工具仅修改知识库、任务和内存文件，不会修改代码。  

## **外部接口**  
该工具完全在本地文件系统中运行，不提供任何外部接口。  

## **信任声明**  
该工具仅读取和写入您的项目目录（`~/.gemini/antigravity/`）和 `.agent/` 目录中的文件，不会向外部服务发送任何数据。  
请仅在您信任该工具能够安全地修改这些目录的情况下才安装它。