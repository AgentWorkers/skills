---
name: social-ops
description: 基于角色的社交媒体运营技能。在执行结构化的社交媒体活动时使用此技能——包括寻找机会、制作内容、发布内容、回复帖子以及分析活动效果。该技能专为 Moltbook 平台设计，但也可适用于任何平台和角色。它将执行过程划分为六个可组合的角色（侦察员、研究员、内容专家、回复者、发布者、分析师），以确保每次操作都保持专注性和可追溯性。您可以为任何社交媒体运营任务激活此技能：机会识别、内容流程管理、社区互动或活动效果评估。
---
# 社交媒体运营

社交媒体运营工作由专门的团队成员执行，每个团队成员都有明确的职责。他们需要阅读相应的参考文档，并将工作成果传递给流程中的下一个环节。

## 工作流程

```
Scout ──→ Content Specialist  (new opportunities → drafts)
Scout ──→ Responder           (reply-worthy threads → responses)
Researcher ──→ guidance for Content Specialist & Responder
Content Specialist ──→ Poster (finished drafts → published)
Poster ──→ done logs          (published → archived)
Analyst ──→ strategy adjustments (performance data → tuning)
```

## 团队角色

在被分配到某个团队角色后，务必先仔细阅读该角色的参考文档，然后再开始执行任务。

| 角色 | 参考文档 | 职责 |
|------|-----|----------------|
| **侦察员** | `{baseDir}/references/roles/Scout.md` | 监控新的机会、热门话题以及相关的动态。发现潜在的营销机会，但不得直接采取行动。 |
| **研究员** | `{baseDir}/references/roles/Researcher.md` | 深入研究相关主题、行业趋势及竞争对手的活动，为内容创作和回应提供指导。 |
| **内容专家** | `{baseDir}/references/roles/Content-Specialist.md` | 将收集到的信息转化为可发布的文本内容，制定发布计划和沟通策略。负责内容的审核和发布，但不负责内容的创作。 |
| **回复者** | `{baseDir}/references/roles/Responder.md` | 根据侦察员提供的线索撰写回复内容，确保回复符合品牌风格并具有价值。 |
| **发布者** | `{baseDir}/references/roles/Poster.md` | 将完成的内容发布到相应的平台上，并将任务状态更新为“已完成”。不参与内容的初步构思或修改。 |
| **分析师** | `{baseDir}/references/roles/Analyst.md` | 监测运营效果，分析问题所在，提出策略调整建议。每周至少进行一次分析。 |

## 分配任务

1. 确定任务需要由哪个团队角色来执行。  
2. 阅读该角色的参考文档（位于 `{baseDir}/references/roles/<Role>.md`）。  
3. 按照文档中的指示执行任务，确保不超出角色的职责范围。  
4. 将任务成果传递给工作流程中的下一个团队成员。  

## 运营策略

整体的运营策略详细记录在 `{baseDir}/assets/strategy/Social-Networking-Plan.md` 中。在所有内容专家或分析师开始工作之前，请先阅读该文件。该文件明确了品牌风格、目标受众、内容发布计划以及增长目标。  

## 团队之间的协作与沟通机制

团队之间的协作流程及任务日志管理方式详细记录在：  
`{baseDir}/references/ROLE-IO-MAP.md`  

## 文件路径规范

为保持技能的通用性，请遵循以下文件路径规则：  
- 团队专属的文件（文档、脚本、资源文件）：存储在 `{baseDir}/...` 目录下。  
- 运行时产生的社交媒体数据文件（日志、指导信息、待办/已完成任务列表）：保存在 `<workspace>/Social/...` 目录下。  
- 非 `Social/` 目录下的运行时状态文件（例如注释标记文件）：使用 `{baseDir}/../state/...` 作为存储路径（除非有新的路径规范）。  

在添加新的操作指令时，请避免使用固定的绝对路径。  

## 目录结构说明  

```
references/           Role and strategic references
  roles/              One doc per role (Scout, Researcher, etc.)
  tasks/              Task queue and templates
assets/               Imported strategy artifacts and static source material
  strategy/           North-star strategy documents
scripts/              Optional helper scripts and adapters
```

## Cron 作业创建指南  

如需设置社交媒体运营任务的自动化执行，请参考 [references/crons/InstallCrons.md](references/crons/InstallCrons.md)。  

可以使用以下两种方式之一来安装 Cron 作业：  
- **基本安装：** 从仓库根目录运行 `./scripts/install-cron-jobs.sh`。  
- **自定义安装/调整：** 使用 `scripts/install-cron-jobs.sh` 和 `references/crons/InstallCrons.md` 作为模板，同时遵循 `{baseDir}` 目录结构和角色职责划分。