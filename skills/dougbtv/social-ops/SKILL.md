---
name: social-ops
description: 基于角色的社交媒体运营技能。在执行结构化的社交媒体活动时使用此技能——包括寻找机会、创作内容、发布内容、回复用户评论以及分析活动效果。该技能专为Moltbook平台设计，但也可适配任何其他平台和用户角色。操作流程被划分为六个可组合的角色（侦察员、研究员、内容专家、回复者、发布者、分析师），以确保每次操作都能保持专注性和可追溯性。您可以为任何社交媒体运营任务激活此技能：机会识别、内容管理、社区互动或活动效果评估。
---
# 社交媒体运营（Social Media Operations）

社交媒体运营工作由专门的团队成员执行，每个团队成员都有明确的职责。他们需要阅读相应的参考文档，并将工作成果传递给流程中的下一个环节。

## 工作流程（Workflow）

```
Scout ──→ Content Specialist  (new opportunities → drafts)
Scout ──→ Responder           (reply-worthy threads → responses)
Researcher ──→ guidance for Content Specialist & Responder
Content Specialist ──→ Poster (finished drafts → published)
Poster ──→ done logs          (published → archived)
Analyst ──→ strategy adjustments (performance data → tuning)
```

## 团队角色（Roles）

在接到任务后，请先仔细阅读相应的参考文档，再开始执行。

| 角色 | 参考文档 | 职责 |
|------|-----|----------------|
| **侦察员（Scout）** | `{baseDir}/references/roles/Scout.md` | 监控新兴的营销机会、热门话题以及新的市场动态。发现潜在的营销机会，但不要直接采取行动。 |
| **研究员（Researcher）** | `{baseDir}/references/roles/Researcher.md` | 深入研究相关主题、市场趋势及竞争对手的活动，为内容创作和应对策略提供依据。 |
| **内容专家（Content Specialist）** | `{baseDir}/references/roles/Content-Specialist.md` | 将收集到的信息转化为可发布的文本内容，制定发布计划和沟通策略。负责内容的审核与发布，但不负责内容的创作。 |
| **回复者（Responder）** | `{baseDir}/references/roles/Responder.md` | 根据侦察员提供的线索撰写回复内容，确保回复与品牌风格一致，并能增加价值。 |
| **发布者（Poster）** | `{baseDir}/references/roles/Poster.md` | 将完成的内容发布到指定的平台，并将任务状态更新为“已完成”。 |
| **分析师（Analyst）** | `{baseDir}/references/roles/Analyst.md` | 监测运营效果，分析问题所在，提出策略调整建议。每周至少进行一次分析。 |

## 分配任务（Task Assignment）

1. 确定任务需要由哪个团队角色来执行。  
2. 阅读该角色的参考文档（位于 `{baseDir}/references/roles/<Role>.md`）。  
3. 按照文档中的指示完成任务，确保不超出角色的职责范围。  
4. 将任务成果传递给工作流程中的下一个团队成员。  

## 运营策略（Strategy）

整体的运营策略文件位于 `{baseDir}/assets/strategy/Social-Networking-Plan.md`。在内容专家或分析师开始工作之前，请先阅读该文件。该文件明确了品牌定位、目标受众、内容发布计划及增长目标。  

## 团队间协作与信息流转（Team Collaboration and Information Flow）

团队之间的协作流程及信息记录方式如下：

- 文件存储路径：`{baseDir}/references/ROLE-IO-MAP.md`  

## 文件路径规范（File Path Conventions）

为确保技能的通用性，请遵循以下文件路径规则：  
- 由特定团队管理的文件（如参考文档、脚本、资源文件）：存储在 `{baseDir}/...` 目录下。  
- 运行时产生的数据文件（如日志、指导信息、待办事项等）：存储在 `{baseDir}/Social/...` 目录下。  
- 非属于 `Social/` 目录的运行时状态文件（例如注释标记文件）：请使用指定的路径 `{baseDir}/../state/...`（请根据实际情况调整）。  

在添加新的操作指令时，请避免使用固定的绝对路径。  

## 目录结构说明（Directory Structure Explanation）  

```
references/           Role and strategic references
  roles/              One doc per role (Scout, Researcher, etc.)
  tasks/              Task queue and templates
assets/               Imported strategy artifacts and static source material
  strategy/           North-star strategy documents
scripts/              Optional helper scripts and adapters
```