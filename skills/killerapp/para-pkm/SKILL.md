---
name: para-pkm
description: 使用“项目（Projects）”、“领域（Areas）”、“资源（Resources）”和“档案（Archives）”的组织方法来管理基于PARA的个人知识管理系统（PKM）。适用于以下场景：  
1. 创建新的PARA知识库；  
2. 将现有知识库组织或重新组织为PARA结构；  
3. 确定内容应归类到项目的哪个部分（项目、领域、资源或档案）；  
4. 为知识库创建适合AI使用的导航文件；  
5. 将已完成的项目归档；  
6. 验证PARA结构的正确性；  
7. 学习适用于特定场景的PARA组织模式（适用于开发人员、顾问、研究人员等）。
---

# PARA 知识库（Para Knowledge Base）

**组织结构**：按照可操作性（actionability）进行分类，而非按主题（topic）。通过项目（Projects）、领域（Areas）、资源（Resources）和归档文件（Archives）来优化知识库的导航体验。建议每月进行一次内容审查。

## 核心概念

- **项目（Projects）**：具有明确截止日期的阶段性目标（完成项目后将其归档）；包括用于记录工作进展的 `projects/stories/` 文件夹。
- **领域（Areas）**：当前正在处理的职责或任务；每个领域使用单独的 `_overview.md` 文件来提供背景信息。
- **资源（Resources）**：参考资料；在不确定如何分类时，可暂时将其放入此文件夹。
- **归档文件（Archives）**：任何类别中不再使用的旧内容或已完成的项目。

## 决策树（Decision Tree）

```
Has deadline/end state? → Projects
Ongoing responsibility? → Areas
Reference material? → Resources (default for uncertain items)
Completed/inactive? → Archives
```

## 快速入门

1. 使用 `python scripts/init_para_kb.py <name>` 命令创建知识库的基本结构，包括 `projects/stories/` 文件夹以及导航系统。
2. 首先识别项目及其截止日期，然后确定它们所属的领域，最后查找相关的参考资源。
3. 使用 `python scripts/generate_nav.py` 命令生成易于使用的 AI 导航结构。

## 脚本（Scripts）

| 脚本（Script） | 功能（Function） | 使用方法（Usage） |
|--------|---------|-------|
| `init_para_kb.py` | 创建新的知识库框架 | `<name> [--path <dir>]` |
| `validate_para.py` | 检查知识库的结构，检测不良组织方式 | `[path]` |
| `archive_project.py` | 为项目添加元数据（如日期、来源）后将其归档 | `<project-file> [--kb-path]` |
| `generate_nav.py` | 生成简洁的 AI 导航结构（代码量少于 100 行） | `[--kb-path] [--output]` |

## 模板（Templates）

| 模板（Template） | 用途（Purpose） |
|----------|---------|
| `assets/AGENTS.md.template` | AI 导航索引页面 |
| `assets/project.md.template` | 项目文件的结构模板 |
| `assets/area-overview.md.template` | 领域概述文件的模板 |
| `assets/README.md.template` | 知识库的说明文档（README） |

## 不同角色的内容组织方式

- **开发者（Developers）**：将相关内容归类到 `projects/active/`（正在进行的项目）、`areas/professional-development/`（专业发展相关内容）或 `resources/coding-standards/`（编码标准）文件夹中。
- **咨询师（Consultants）**：将项目文件放入 `projects/active/`（交付物）、`projects/stories/`（项目进展记录），同时将相关资料存放在 `areas/consulting/clients/` 文件夹中。
- **研究人员（Researchers）**：将项目文件存放在 `projects/active/`（研究项目/资助申请），相关资料存放在 `resources/literature-review/` 文件夹中。
- **产品经理（Product Managers）**：将项目文件分为 `projects/active/`（新发布的产品）、`areas/product-development/`（正在开发的产品）等不同类别。

## 复杂场景下的内容组织

- **客户与项目的关系**：将项目文件存放在 `projects/active/client-x.md` 中，同时记录与客户的合作关系（`areas/consulting/clients/client-x.md`）。
- **研究项目的生命周期**：内容按 `areas/product-development/{research → graduated → active → legacy}` 的顺序组织，并设置交叉引用。

## 需避免的不良组织方式（Anti-Patterns）

- 不应将文件直接放入 `inbox` 或其他临时文件夹中，而应将其归类到相应的类别中。
- 避免过度嵌套（建议最多使用 2-3 层结构）；扁平化结构更易于管理。
- 不要按主题（如“工作/个人”）来组织文件，而应按照可操作性来分类。
- 不要将任务单独存放在“待办事项”文件夹中，而应将其关联到相应的项目或领域。
- 不要过度追求文件内容的完美性；定期进行内容审查有助于发现文件放置不当的问题。

## 内容的生命周期管理

```
Resources → Projects → Archives (research → active work → completed)
Areas → Archives (no longer responsible)
Projects ⟺ Areas (goal becomes ongoing or vice versa)
```

## AI 导航与使用技巧

- 保持导航结构简洁（代码量少于 100 行），确保链接指向的是文件路径而非文件本身。
- 从简单的导航结构开始使用（例如“我目前正在处理什么任务？”），每个项目或任务都应有一个明确的入口页面。
- 每月进行一次内容审查，将已完成的项目归档，并重新评估各个领域的内容结构，以便逐步形成最佳的组织模式。

## 参考资料

- [para-principles.md](references/para-principles.md)：完整的 PARA 知识库组织方法，强调“按可操作性分类而非按主题”。
- [decision-guide.md](references/decision-guide.md)：包含详细决策流程及边缘情况的指南。
- [common-patterns.md](references/common-patterns.md)：适用于不同角色的最佳实践模式。
- [ai-navigation.md](references/ai-navigation.md)：专为 AI 用户设计的导航最佳实践指南。