---
name: clawhub-recommender
description: "根据用户的意图和对话上下文，从 ClawHub 推荐热门且评分较高的技能。适用于：寻找新技能、发现流行的工具、将用户需求与现有的 ClawHub 技能进行匹配。"
---
# ClawHub 推荐系统

该功能通过分析用户当前的对话内容和需求，帮助用户发现 ClawHub 上最受欢迎和最实用的技能。

## 核心功能

ClawHub 推荐系统能够识别用户的需求，并将用户的需求与经过社区审核的高质量技能进行匹配。系统会优先推荐下载量高、评分高且具有官方认证的技能，以确保推荐结果的可靠性和实用性。

### 使用场景

- 当用户表达对特定功能的需求时（例如：“我需要管理我的 GitHub 问题”）。
- 当用户请求获取热门或实用技能的推荐时。
- 当用户执行的任务可以通过现有的 ClawHub 技能得到显著改进时。

## 推荐流程

为了提供最相关的推荐结果，请按照以下步骤操作：

1. **分析用户需求**：确定用户当前正在执行的任务、遇到的问题或对新功能的具体需求。
2. **确定需求所属类别**：将用户的需求归类到开发（Development）、生产力（Productivity）、沟通（Communication）或搜索（Search）等类别中。
3. **查阅参考资料**：参考以下文件以找到最合适的推荐方案：
   - `/home/ubuntu/skills/clawhub-recommender/references/popular_skills.md`：包含评分和描述的顶级技能列表。
   - `/home/ubuntu/skills/clawhub-recommender/recommendation_logic.md`：用于将用户需求与特定技能类别匹配的指南。
4. **生成推荐内容**：提供清晰简洁的推荐信息，包括技能名称、受欢迎程度、简要描述以及为什么该技能适合用户当前的需求。
5. **提供安装说明**：提供技能的官方链接和安装命令（例如：`clawhub install <slug>`）。

## 推荐准则

| 类别 | 推荐技能 | 关键指标 |
| :--- | :--- | :--- |
| **开发** | `github`, `fast-io`, `capability-evolver` | 官方认证，下载量超过 3.5 万次 |
| **生产力** | `linear`, `byterover`, `automation-workflows` | 官方认证，下载量超过 1.7 万次 |
| **沟通** | `wacli`, `bird` | 下载量超过 1.6 万次，评分较高 |
| **搜索** | `tavily`, `gog` | 下载量和评分均较高 |

### 选择标准

- **受欢迎程度**：优先推荐下载量超过 1 万次或评分较高的技能。
- **官方认证**：优先选择具有官方认证的技能（如 `github`, `linear`），以确保稳定性和安全性。
- **相关性**：确保推荐的技能能够直接解决用户当前的问题或需求。
- **可靠性**：仅推荐经过验证的技能，以增强用户的信任度。

## 推荐示例

> **技能名称**：GitHub (`github`)
> **指标**：官方认证，下载量高
> **描述**：可以直接通过该技能管理您的 GitHub 仓库、问题及拉取请求。
> **适用场景**：由于您正在开发一个 React 项目并需要跟踪项目进度，GitHub 技能可以帮助您轻松管理问题及提交记录。
> **链接**：[ClawHub 上的 GitHub 技能](https://github.com/openclaw/clawhub/tree/main/skills/github)
> **安装命令**：`clawhub install github`