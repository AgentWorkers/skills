---
name: social-ops
description: 基于角色的社交媒体运营技能。在执行结构化的社交媒体活动时使用此技能——包括寻找机会、创作内容、发布内容、回复用户评论以及分析活动效果。该技能专为Moltbook平台设计，但也可适用于任何平台和角色。技能操作被划分为六个可组合的角色（侦察员、研究员、内容专家、回复者、发布者、分析师），以确保每次操作都能保持专注性和可追溯性。您可以针对任何社交媒体运营任务激活此技能：机会识别、内容流程管理、社区互动或活动效果评估。
---
# 社交媒体运营

社交媒体运营工作由专门的团队成员执行。每个团队成员都有明确的职责，他们会阅读相应的参考文档，并将工作成果传递给工作流程中的下一个环节。

## 工作流程

```
Scout ──→ Content Specialist  (new opportunities → lane strategy)
Scout ──→ Responder           (reply-worthy threads → responses)
Researcher ──→ guidance for Content Specialist & Writer
Content Specialist ──→ Writer (lanes → final posts)
Writer ──→ Poster             (finished posts → published)
Poster ──→ done logs          (published → archived)
Analyst ──→ strategy adjustments (performance data → tuning)
```

## 团队角色

在被分配到某个团队角色后，请在开始工作之前仔细阅读该角色的参考文档。

| 角色 | 参考文档 | 职责 |
|------|-----|----------------|
| **侦察员** | `{baseDir}/references/roles/Scout.md` | 监控新的机会、热门话题以及潜在的营销机会。发现这些机会后，不要直接采取行动。 |
| **研究员** | `{baseDir}/references/roles/Researcher.md` | 深入研究相关主题、趋势以及竞争对手的活动，为内容创作和回应提供指导。 |
| **内容专家** | `{baseDir}/references/roles/Content-Specialist.md` | 将收集到的信息转化为可发布的内容素材，确定发布的内容方向、节奏和信息传递方式。**不负责直接发布内容**。 |
| **回复者** | `{baseDir}/references/roles/Responder.md` | 根据侦察员发现的热门话题撰写回复，确保回复符合品牌风格并具有价值。 |
| **发布者** | `{baseDir}/references/roles/Poster.md` | 将准备好的内容发布到相应的平台上，并将已完成的任务记录到日志中。**不负责内容创意或修改**。 |
| **分析师** | `{baseDir}/references/roles/Analyst.md` | 监测运营效果，分析问题所在，提出策略调整建议。每周至少进行一次分析。 |

## 分配任务

1. 确定任务需要由哪个团队角色来完成。  
2. 阅读该角色的参考文档（位于 `{baseDir}/references/roles/<Role>.md`）。  
3. 按照文档中的指示执行任务，确保不超出其职责范围。  
4. 将完成任务的结果传递给工作流程中的下一个团队成员。  

## 运营策略

整体的运营策略文件位于 `{baseDir}/assets/strategy/Social-Networking-Plan.md`。在内容专家或分析师开始工作之前，请先阅读该文件。该文件定义了品牌的沟通风格、目标受众、内容发布结构以及增长目标。  

## 团队间协作与信息流

团队之间的协作流程及信息记录方式如下：

- `{baseDir}/references/ROLE-IO-MAP.md`  

## 文件路径规范

为了保证技能的通用性，请遵循以下文件路径规则：  
- 由特定团队管理的文件（如文档、脚本、资源文件）：存放在 `{baseDir}/...` 目录下。  
- 运行时产生的社交媒体数据文件（如日志、指导信息、待办事项/已完成任务列表）：存放在 `<workspace>/Social/...` 目录下。  
- 非属于 `Social/` 目录的运行时状态文件（例如注释标记文件）：请使用 `{baseDir}/../state/...` 的路径进行存储（直到路径规则发生变化）。  

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

## 创建 Cron 作业的提示

有关如何自动化执行社交媒体运营任务的说明，请参考 [references/crons/InstallCrons.md](references/crons/InstallCrons.md)。  

你可以使用以下两种方式之一来设置 Cron 作业：  
- **基本安装：** 从仓库根目录运行 `./packaged-scripts/install-cron-jobs.sh`。  
- **自定义安装/调整：** 使用 `scripts/install-cron-jobs.sh` 和 `references/crons/InstallCrons.md` 作为模板，同时遵循 `{baseDir}` 目录结构和团队角色划分规则。