---
name: sc
description: >
  **Supernal Coding CLI：用于开发工作流程的工具**  
  该工具集提供了全面的功能，涵盖任务管理、需求跟踪、测试自动化、Git操作、代码审查流程（如Ralph Loop）、合规性检查以及文档生成等。  
  **主要用途：**  
  - **任务管理**：支持创建、分配和跟踪开发任务。  
  - **项目健康检查**：定期评估项目的开发状态和进度。  
  - **可追溯性**：确保所有开发活动都有明确的记录和来源。  
  - **需求管理**：帮助团队有效管理项目需求。  
  - **自动化执行**：支持自动化执行重复性或繁琐的开发任务。  
  **核心功能：**  
  - **任务分配与跟踪**：允许团队成员高效协作，确保任务按时完成。  
  - **Git集成**：自动化处理Git仓库的版本控制操作（如推送、拉取、合并等）。  
  - **代码审查流程**：提供代码审查的模板和工具，提升代码质量。  
  - **合规性检查**：确保开发过程符合相关标准和规范。  
  - **文档生成**：自动生成项目相关的文档，便于团队成员查阅和学习。  
  **适用场景：**  
  - **敏捷开发**：支持Scrum或Kanban等敏捷开发方法。  
  - **项目管理**：适用于各类软件开发项目。  
  **优势：**  
  - **高度定制化**：提供丰富的配置选项，以满足不同团队的需求。  
  - **易于使用**：界面友好，操作简单。  
  - **集成性强**：可与现有的开发工具和流程无缝集成。  
  **更多信息：**  
  访问[Supernal Coding CLI官方网站](https://supernalcoding.com/)了解更多详情和下载方式。
---
# sc - Supernal Coding CLI

sc 是一个用于自动化开发工作流程、任务管理、需求跟踪以及自主执行任务的命令行工具（CLI）。

**主要功能范围：**
- `sc` 用于执行与开发者/项目工作流程相关的命令。
- `orch` 用于协调运行时操作（如资源分配、任务创建、任务分类、心跳检测以及自动化流程）。
**注意：** 不要假设不同 CLI 中具有相同名称的命令具有相同的功能或含义。

## 安装

```bash
npm install -g @supernalintelligence/supernal-coding
```

## 快速参考

### 任务管理（核心功能）
```bash
sc task create "Title" --assignee @me --priority P2
sc task list                         # Your tasks  
sc task list --all                   # All repos
sc task list --status in-progress    # Filter by status
sc task view TASK-123                # View task details
sc task start TASK-123               # Begin work (sets in-progress)
sc task done TASK-123 --notes "..."  # Complete task
sc task next                         # Get next task (ralph mode)
sc task verify TASK-123              # Check evidence (optional)
sc task edit TASK-123                # Edit in $EDITOR

# Session linkage (dashboard only - requires localhost:3006)
sc task link TASK-123                # Link to current session (needs OPENCLAW_SESSION_KEY)
sc task link TASK-123 --session "..."  # Link with explicit session
sc task linked                       # List linked tasks
sc task unlink TASK-123              # Remove link
```

**存储路径：** `.supernal/tasks/`（每个仓库专用）或 `~/.supernal/tasks/`（全局）

**工作流程指南：** 请参阅 `docs/TASK_WORKFLOW.md`，以了解任务、需求、功能及规格之间的协作方式。

### 项目健康状况与状态监控
```bash
sc health                    # Run health checks
sc monitor                   # Development status dashboard
sc status                    # Alias for monitor
```

### 需求管理及可追溯性
```bash
sc trace                     # Traceability matrix
sc planning                  # Manage epics, features, requirements, tasks
sc audit                     # Audit features, requirements, tests
```

### Git 与工作流程集成
```bash
sc git                       # Git workflow operations
sc git smart                 # Smart commits, branch management
sc workflow                  # Project workflow management
```

### Ralph（自主执行循环）
```bash
sc ralph                     # Autonomous task execution
sc spec <action> [target]    # Spec file management for ralph loops
```

### 代码质量控制
```bash
sc code <action>             # Code quality and contracts
sc compliance                # HIPAA, SOC 2, ISO 27001 validation
sc security                  # Database security verification
```

### 文档编写
```bash
sc docs                      # Documentation management
sc search <query>            # Search across all content
```

### 系统管理
```bash
sc init [dir]                # Initialize project
sc update                    # Check for updates
sc system                    # Config, upgrade, sync, license
```

## 常见使用模式

### 新功能开发流程
```bash
sc planning feature create "Add user auth"
sc spec create auth-feature.md
sc ralph execute auth-feature.md
```

### 提交代码前的健康检查
```bash
sc health
sc audit
sc compliance check
```

### 知识库与工作区维护
```bash
# Run knowledge store cleanup (pair with sc health)
know tidy              # Audit knowledge store
know tidy --fix        # Auto-fix issues (normalize tags, move misplaced files)
know reindex           # Rebuild INDEX.md
know validate          # Check frontmatter schema

# Recommended: add to heartbeat or nightly cron
know tidy --fix && know reindex
```

### 可追溯性报告
```bash
sc trace report --format markdown
```

## 与代理（Agents）的集成

### 任务分配流程
```bash
# Orchestrator assigns task
sc task create "Build API endpoint" --assignee @codex-coder --priority P1

# Agent picks up work
sc task next                # Get your next assigned task
sc task start TASK-123      # Mark as in-progress
# ... do work ...
sc task done TASK-123 --notes "Completed, PR #456"
```

### Ralph 循环（自主执行机制）
```bash
# Create spec
sc spec create task-name.md

# Execute with ralph
sc ralph execute task-name.md --max-iterations 10
```

有关代理的协调与任务创建功能，请参阅 `orch` 文档。