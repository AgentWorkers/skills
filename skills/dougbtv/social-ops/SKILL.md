---
name: social-ops
description: 基于角色的社交媒体运营技能。在执行结构化的社交媒体活动时使用此技能——包括寻找机会、创作内容、发布内容、回复用户评论以及分析活动效果。该技能专为Moltbook平台设计，但也可适用于任何平台和角色。它将运营流程分解为六个可组合的角色（侦察员、研究员、内容专家、回复者、发布者、分析师），以确保每次操作都能保持专注性和可追溯性。您可以激活此技能来执行任何社交媒体相关任务，例如机会识别、内容流程管理、社区互动或活动效果评估。
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

## 团队成员角色

在被分配到某个团队角色后，请在开始工作之前仔细阅读该角色的参考文档。

| 角色 | 参考文档 | 职责 |
|------|-----|----------------|
| **侦察员（Scout）** | `{baseDir}/references/roles/Scout.md` | 监控新兴的机会、热门话题以及新的趋势。发现潜在的营销机会，但不得直接采取行动。 |
| **研究员（Researcher）** | `{baseDir}/references/roles/Researcher.md` | 深入研究相关主题、市场趋势及竞争对手的活动，为内容创作和回应提供指导。 |
| **内容专家（Content Specialist）** | `{baseDir}/references/roles/Content-Specialist.md` | 将收集到的信息转化为可发布的文本内容，确定发布的内容方向、节奏和信息传递方式。 |
| **回复者（Responder）** | `{baseDir}/references/roles/Responder.md` | 根据侦察员的发现撰写回复内容，确保回复符合品牌风格并具有价值。 |
| **发布者（Poster）** | `{baseDir}/references/roles/Poster.md` | 将完成的内容发布到指定的平台，并将任务状态更新为“已完成”。不负责内容创意或修改。 |
| **分析师（Analyst）** | `{baseDir}/references/roles/Analyst.md` | 监测运营效果，分析问题所在，提出策略调整建议。每周至少进行一次分析。 |

## 分配任务

1. 确定任务需要由哪个团队角色来完成。  
2. 阅读该角色的参考文档（位于 `{baseDir}/references/roles/<Role>.md`）。  
3. 按照文档中的指示执行任务，确保不超出角色的职责范围。  
4. 将任务成果传递给工作流程中的下一个团队成员。  

## 运营策略

整体的运营策略详见 `{baseDir}/assets/strategy/Social-Networking-Plan.md`。在任何内容专家或分析师开始工作之前，请先阅读该文件。该文件明确了品牌语言、目标受众、内容发布结构以及增长目标。  

## 团队间协作与信息流

团队成员之间的协作流程及信息记录方式如下：

- `{baseDir}/references/ROLE-IO-MAP.md`  

## 文件路径规范

为确保技能的可移植性，请遵循以下文件路径规则：  
- 由特定团队管理的文件（如文档、脚本、资源文件）：存储在 `{baseDir}/...` 目录下。  
- 运行时产生的社交媒体相关数据文件（如日志、指导文档、待办事项/已完成事项列表）：保存在 `{baseDir}/Social/...` 目录下。  
- 非属于 `Social/` 目录下的运行时状态文件（例如注释标记文件）：请使用 `{baseDir}/../state/...` 的路径结构（直至路径规则更新）。  

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

## 创建定时任务的提示  

如需设置社交媒体运营任务的自动化执行，请参考 [references/crons/InstallCrons.md](references/crons/InstallCrons.md)。  

可以使用以下两种方式之一来安装定时任务：  
- **基本安装：** 从仓库根目录运行 `./scripts/install-cron-jobs.sh`。  
- **自定义安装/调整：** 使用 `scripts/install-cron-jobs.sh` 和 `references/crons/InstallCrons.md` 作为模板，同时遵循 `{baseDir}` 目录结构和角色职责划分。