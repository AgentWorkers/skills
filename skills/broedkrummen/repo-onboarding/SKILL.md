---
name: repo-onboarding
description: Onboard a coding repository with both technical architecture intake and execution governance. Use when starting in a new/existing repo and you need: (1) architecture snapshot + dependency analysis, (2) run/build/test bootstrap map, and (3) ROADMAP + feature KANBAN workflow setup for multi-agent execution.
---

# 仓库入职流程

将 `senior-architect`（技术评估）与 `repo-kanban-pm`（执行治理）流程结合起来。

## 工作流程

1. **技术评估（架构设计及依赖关系确认）**
2. **安装执行管理系统（包括ROADMAP、KANBAN工具及问题跟踪工具）**
3. **生成入职报告以供交接**

---

## 第一步 — 技术评估

从目标仓库的根目录执行以下命令：

```bash
# 1) architecture assessment
python /home/broedkrummen/.openclaw/workspace-cody/skills/senior-architect/scripts/project_architect.py . --output json > docs/pm/architecture-assessment.json

# 2) dependency analysis
python /home/broedkrummen/.openclaw/workspace-cody/skills/senior-architect/scripts/dependency_analyzer.py . --output json > docs/pm/dependency-analysis.json

# 3) architecture diagram (mermaid)
python /home/broedkrummen/.openclaw/workspace-cody/skills/senior-architect/scripts/architecture_diagram_generator.py . --format mermaid -o docs/pm/architecture-diagram.md
```

如果脚本执行失败，请采取手动补救措施：
- 确定项目所使用的开发框架（`package.json`、`pyproject.toml`、`go.mod`等文件）
- 收集项目的运行、构建和测试命令
- 在 `docs/pm/ONBOARDING.md` 文件中总结项目文件夹结构及核心功能模块的边界

---

## 第二步 — 安装执行管理系统

```bash
bash /home/broedkrummen/.openclaw/workspace-cody/skills/repo-kanban-pm/scripts/init_repo_pm.sh "$(pwd)"
```

可选的每日项目经理审核流程：

```bash
bash /home/broedkrummen/.openclaw/workspace-cody/skills/repo-kanban-pm/scripts/add_daily_pm_cron.sh "$(pwd)" --agent cody --tz UTC --time 09:30
```

---

## 第三步 — 创建入职报告

使用 `references/onboarding-template.md` 模板生成 `docs/pm/ONBOARDING.md` 文件。报告必须包含以下内容：
- 项目架构概述
- 依赖关系风险及循环依赖问题
- 运行、构建和测试的配置信息
- 环境配置要求
- 初始的项目路线图及KANBAN状态
- 首批推荐开发的特性列表

---

## 完成入职流程的条件

只有满足以下所有条件后，才能认为流程完成：
- `docs/pm/architecture-assessment.json` 文件存在（或已有等效的手动文档）
- `docs/pm/dependency-analysis.json` 文件存在（或已有等效的手动文档）
- `docs/roadmap/ROADMAP.md` 文件存在
- 至少有一个 `docs/features/<feature>/KANBAN.md` 文件存在
- `docs/pm/ONBOARDING.md` 文件内容完整且可执行

## 注意事项

- 如果仓库已经使用了项目经理管理系统（PM系统），请避免重复安装。
- 如果已有类似的工作流程，请将其与现有流程集成，并仅补充缺失的部分。
- 保持入职流程的简洁性，确保其他团队成员能够在10分钟内完成整个流程。