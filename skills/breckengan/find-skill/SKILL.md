---
name: find-skills
description: 该功能帮助用户在提出诸如“我该如何做某事？”、“如何找到适用于某任务的技能？”或“是否有可以用于实现某功能的技能？”等问题时，发现并安装相应的技能。当用户需要查找可通过安装来获得的特定功能时，应使用该功能。
---

# 查找技能

此技能可帮助您从 open agent 技能生态系统中发现并安装所需的技能。

## 何时使用此技能

当用户遇到以下情况时，请使用此技能：

- 提问“我该如何完成某项任务？”（其中“某项任务”可能是可以通过现有技能完成的常见操作）
- 询问“有没有适用于某项任务的技能”或“是否有专门用于某项任务的工具”
- 表示希望扩展代理的功能
- 希望搜索工具、模板或工作流程
- 提到他们在某个特定领域（如设计、测试、部署等）需要帮助

## 什么是 Skills CLI？

Skills CLI (`npx skills`) 是 open agent 技能生态系统的包管理器。这些技能是以模块化形式存在的包，它们通过提供专业知识、工作流程和工具来扩展代理的功能。

**常用命令：**

- `npx skills find [查询关键词]` - 通过关键词交互式地搜索技能
- `npx skills add <包名>` - 从 GitHub 或其他来源安装技能
- `npx skills check` - 检查技能是否有更新
- `npx skills update` - 更新所有已安装的技能

**访问技能列表的网址：** https://skills.sh/

## 如何帮助用户查找技能

### 第一步：了解用户的需求

当用户寻求帮助时，需要明确以下信息：

1. 所需技能涉及的领域（例如：React、测试、设计、部署）
2. 具体的任务（例如：编写测试用例、创建动画、审核 Pull Request）
3. 该任务是否属于常见任务（即是否存在相应的技能）

### 第二步：搜索技能

使用相应的查询关键词运行 `npx skills find` 命令：

```bash
npx skills find [query]
```

例如：

- 用户询问：“如何让我的 React 应用运行得更快？” → `npx skills find react performance`
- 用户询问：“你能帮我审核 Pull Request 吗？” → `npx skills find pr review`
- 用户询问：“我需要创建一个变更日志。” → `npx skills find changelog`

命令执行后会返回相关结果：

```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 第三步：向用户展示搜索结果

找到相关技能后，向用户展示以下信息：

1. 技能的名称及其功能
2. 可以执行的安装命令
3. 访问 skills.sh 以获取更多信息的链接

示例回答：

```
I found a skill that might help! The "vercel-react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

To install it:
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### 第四步：提供安装帮助

如果用户同意安装技能，您可以代为完成安装操作：

```bash
npx skills add <owner/repo@skill> -g -y
```

`-g` 标志表示全局安装（用户级别），`-y` 标志表示跳过确认提示。

## 常见技能分类

搜索时可以参考以下分类：

| 分类            | 常见查询关键词                          |
| ---------------------- | ---------------------------------------- |
| Web 开发          | react, nextjs, typescript, css, tailwind         |
| 测试              | testing, jest, playwright, e2e                   |
| DevOps            | deploy, docker, kubernetes, ci-cd                |
| 文档编写          | docs, readme, changelog, api-docs                |
| 代码质量          | review, lint, refactor, best-practices           |
| 设计              | ui, ux, design-system, accessibility             |
| 提高效率          | workflow, automation, git                        |

## 提高搜索效率的技巧：

1. **使用具体的关键词**：例如使用“react testing”而非“testing”
2. **尝试替代词汇**：如果“deploy”无法找到合适的技能，可以尝试“deployment”或“ci-cd”
3. **查看热门来源**：许多技能来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`

## 未找到相关技能时的处理方式

如果未找到合适的技能：

1. 告知用户没有找到相应的技能
2. 表示可以使用您自身的能力直接帮助用户完成任务
3. 建议用户使用 `npx skills init` 命令创建自己的技能

示例：

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```