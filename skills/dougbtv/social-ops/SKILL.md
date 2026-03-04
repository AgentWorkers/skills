---
name: social-ops
description: 基于角色的社交媒体运营技能。在执行结构化的社交媒体活动时使用此技能——包括寻找机会、创作内容、发布内容、回复帖子以及分析活动效果。该技能专为 Moltbook 平台设计，但也可适用于任何平台和角色。将运营流程分为六个可组合的角色（侦察员、研究员、内容专家、回复者、发布者、分析师），以确保每次操作都能保持专注性和可追溯性。您可以激活此技能来执行任何社交媒体相关任务：机会识别、内容管理、社区互动或活动效果评估。
---
# 社交媒体运营（Social Media Operations）

社交媒体运营工作由专门的团队成员执行，每个团队成员都负责特定的任务。每个成员会阅读自己对应的职责文档，并将工作成果传递给工作流程中的下一个环节。

## 工作流程（Workflow）

```
Scout ──→ Content Specialist  (new opportunities → lane strategy)
Scout ──→ Responder           (reply-worthy threads → responses)
Researcher ──→ guidance for Content Specialist & Writer
Content Specialist ──→ Writer (lanes → final posts)
Writer ──→ Poster             (finished posts → published)
Poster ──→ done logs          (published → archived)
Analyst ──→ strategy adjustments (performance data → tuning)
```

## 团队角色（Roles）

在被分配到某个团队角色后，请在开始工作之前仔细阅读该角色的职责文档。

| 角色 | 责任 | 参考文档 |
|------|------|---------|
| **侦察员（Scout）** | 监控新兴的机会、热门话题以及新的社交媒体动态。发现潜在的营销机会，但不要直接采取行动。 | `{baseDir}/references/roles/Scout.md` |
| **研究员（Researcher）** | 深入研究相关主题、行业趋势以及竞争对手的活动，为内容创作和应对策略提供依据。 | `{baseDir}/references/roles/Researcher.md` |
| **内容专家（Content Specialist）** | 将收集到的信息转化为可发布的文本内容，制定发布计划和信息传递方式。负责内容的审核和发布，但不负责内容的创作。 | `{baseDir}/references/roles/Content-Specialist.md` |
| **回复者（Responder）** | 根据侦察员的发现撰写回复内容，确保回复符合品牌风格并具有价值。 | `{baseDir}/references/roles/Responder.md` |
| **发布者（Poster）** | 将准备好的内容发布到相应的社交媒体平台，并将已完成的任务记录到日志中。不参与内容的创意构思或修改。 | `{baseDir}/references/roles/Poster.md` |
| **分析师（Analyst）** | 监测运营效果，分析问题所在，提出策略调整建议。每周至少进行一次分析。 | `{baseDir}/references/roles/Analyst.md` |

## 分配任务（Task Assignment）

1. 确定任务需要由哪个团队角色来执行。
2. 阅读该角色的职责文档（位于 `{baseDir}/references/roles/<Role>.md`）。
3. 按照文档中的指示执行任务，确保不超出角色的职责范围。
4. 将任务成果传递给工作流程中的下一个团队成员。

## 运营策略（Strategy）

整体运营策略详细记录在 `{baseDir}/assets/strategy/Social-Networking-Plan.md` 文件中。在所有内容专家或分析师开始工作之前，请先阅读该文件。该文件定义了品牌的沟通风格、目标受众、内容发布渠道以及增长目标。

## 团队间协作与信息流（Team Collaboration and Information Flow）

团队之间的协作流程及信息传递方式详细记录在 `{baseDir}/references/ROLE-IO-MAP.md` 文件中。

## 环境变量（Environment Variables）

| 变量 | 是否必需 | 说明 |
|--------|--------|---------|
| `SOCIAL_OPS_DATA_DIR` | 是 | 指定运行时数据（日志、任务列表、待办事项、已完成任务、社交媒体数据等）的绝对路径。 |

### 环境配置（Environment Setup）

在任何团队开始工作之前，必须设置 `SOCIAL_OPS_DATA_DIR` 变量。如果该变量尚未设置：
1. 询问相关团队成员他们的社交媒体数据目录的位置。
2. 建议他们在 shell 配置文件中添加该目录的路径。

```bash
export SOCIAL_OPS_DATA_DIR=/path/to/Social
```

所有团队角色的职责文档都将 `$SOCIAL_OPS_DATA_DIR/` 视为运行时数据的根目录。这一设置取代了之前的 `<workspace>/Social/` 目录结构，以提高数据管理的可靠性。

## 路径规范（Path Conventions）

为确保技能的可移植性，请遵循以下路径规范：
- 团队成员自己的文件（文档、脚本、资源文件）：使用 `{baseDir}/...`
- 运行时的社交媒体数据文件（日志、指导文档、任务列表等）：使用 `$SOCIAL_OPS_DATA_DIR/...`
- 不属于数据目录的运行时状态文件（例如注释文件）：使用 `{baseDir}/../state/...` 作为路径，直到官方的路径规范发生变化。

在添加新的操作指令时，请避免使用特定的机器路径。

## 目录结构规范（Directory Structure）

```
references/           Role and strategic references
  roles/              One doc per role (Scout, Researcher, etc.)
  tasks/              Task queue and templates
assets/               Imported strategy artifacts and static source material
  strategy/           North-star strategy documents
scripts/              Optional helper scripts and adapters
```

## 自动化任务调度（Cron Job Setup）

有关如何自动化执行社交媒体相关任务的配置，请参考 [references/crons/InstallCrons.md](references/crons/InstallCrons.md)。

你可以使用以下命令之一来设置自动化任务：
- **基本安装：** 从仓库根目录运行 `./packaged-scripts/install-cron-jobs.sh`。
- **自定义安装/调整：** 使用 `scripts/install-cron-jobs.sh` 和 `references/crons/InstallCrons.md` 作为模板，确保遵循 `{baseDir}` 的路径规范和团队职责划分。