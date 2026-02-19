---
name: unified-find-skills
description: 帮助用户从 skills.sh、clawhub.com 和 tessl.io 网站中发现并安装代理技能（agent skills）。当用户需要为某项任务寻找合适的技能、扩展代理的功能，或搜索工具/工作流程时，可以使用该功能。
---
# 查找技能

此技能可帮助您从三个注册库中发现并安装所需技能：
- **skills.sh**：原始的开放代理技能生态系统
- **clawhub.com**：基于向量的技能搜索平台，支持简单的技能名称查询（需要安装 `clawhub` 命令行工具）
- **tessl.io**：提供带有版本信息的技能和工具的注册库

## 何时使用此技能

当用户遇到以下情况时，可以使用此技能：
- 询问“如何完成某项任务”（例如，该任务可能已有对应的技能）
- 询问“是否有用于完成某项任务的技能”
- 表达出扩展代理功能的愿望
- 希望搜索工具、模板或工作流程
- 提到希望在某个特定领域（如设计、测试、部署等）获得帮助

## 搜索可用注册库

系统会搜索所有可用的注册库。如果未安装 `clawhub` 命令行工具，则会跳过该注册库。

### 第一步：了解用户需求

当用户寻求帮助时，需要明确以下信息：
- 需要帮助的领域（例如：React、测试、设计、部署）
- 具体的任务（例如：编写测试代码、创建动画、审核代码提交）
- 该任务是否属于常见任务（即是否存在相应的技能）

### 第二步：搜索可用注册库

检查可用的命令行工具（CLIs），并同时在这些注册库中进行搜索：

```bash
# skills.sh (always available via npx)
npx skills find [query] --limit 5

# clawhub (only if installed)
if command -v clawhub &> /dev/null; then
  clawhub search "[query]" --limit 5
fi

# tessl.io (via web scraping)
curl -s "https://tessl.io/registry/discover?contentType=skills" | grep -o 'name:"[^"]*"' | head -10
```

**示例：**
- 用户询问：“如何让我的 React 应用运行得更快？” → 在可用注册库中搜索 “react performance”
- 用户询问：“你能帮我审核代码提交吗？” → 在可用注册库中搜索 “pr review”
- 用户询问：“我需要创建一个变更日志” → 在可用注册库中搜索 “changelog”

**关于 clawhub 的说明：** 需要安装 `clawhub` 命令行工具。如果尚未安装，请使用 `npm install -g clawhub` 进行安装。

**关于 tessl.io 的说明：** tessl.io 注册库不提供简单的命令行搜索功能。您可以：
- 访问 https://tessl.io/registry/discover?contentType=skills 进行浏览
- 使用 `curl + grep` 从页面中提取技能名称
- 使用 `tessl skill search [查询内容]`（仅支持交互式搜索）

### 第三步：向用户展示搜索结果

找到相关技能后，按注册库分类展示结果：
- **对于 skills.sh 提供的技能**：
  - 技能名称及功能说明
  - 可以运行的安装命令
  - 链接（用于在 skills.sh 网站上获取更多信息）
- **对于 clawhub 提供的技能**：
  - 技能名称及版本信息
  - （如有的话）技能描述
  - 可以运行的安装命令
- **对于 tessl.io 提供的技能**：
  - 技能名称
  - （如有的话）技能描述（来自注册库页面）
  - 可以运行的安装命令

**示例响应：**
```
I found some skills that might help!

**From skills.sh:**
- "vercel-react-best-practices" - React and Next.js performance optimization guidelines from Vercel Engineering
  Install: npx skills add vercel-labs/agent-skills@vercel-react-best-practices
  Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

**From clawhub:**
- "react-expert v0.1.0" - React Expert
  Install: clawhub install react-expert

**From tessl.io:**
- "react-doctor" - Diagnose and fix React codebase health issues
  Browse: https://tessl.io/registry/discover?contentType=skills
  Install: tessl install <skill-name> (requires tessl CLI)
```

### 第四步：提供安装选项

如果用户希望安装某项技能：
- **对于 skills.sh 提供的技能**：
  使用 `-g` 标志进行全局安装（用户级别），`-y` 标志可跳过确认提示。

- **对于 clawhub 提供的技能**：
  （具体安装命令根据实际情况填写）

**可选：指定技能版本：**
```bash
clawhub install <slug> --version <version>
```

- **对于 tessl.io 提供的技能**：
  （具体安装命令根据实际情况填写）

**从 GitHub 安装技能：**
```bash
tessl install github:user/repo
```

## 注册库对比

| 功能                | skills.sh                          | clawhub.com                      | tessl.io                         |
|------------------|-----------------------------------|---------------------------------|---------------------------------|
| 搜索格式            | `npx skills find <查询内容>`          | `clawhub search "<查询内容>"`        | 在网页上浏览或使用 `tessl skill search`         |
| 安装格式            | `npx skills add <所有者/仓库@技能名称>`       | `clawhub install <技能名称>`         | `tessl install <技能名称>`                     |
| 版本管理            | 基于 Git 的版本管理（所有者/仓库@技能名称）      | 语义化版本管理（vX.Y.Z）                | 语义化版本管理                         |
| 浏览方式            | https://skills.sh/                 | https://clawhub.ai/              | https://tessl.io/registry/discover             |
| 是否需要命令行工具？        | 不需要（使用 npx 命令）                   | 需要 `clawhub` 命令行工具                | 可选（tessl.io 支持）                     |
| 更新方式            | `npx skills update`                | `clawhub update <技能名称>` 或 `--all`       | `tessl update`                         |

## 常见技能类别

搜索时，请参考以下常见技能类别：
| 类别                | 示例查询内容                          |
|------------------|----------------------------------------|
| Web 开发            | react, nextjs, typescript, css, tailwind       |
| 测试                | testing, jest, playwright, e2e                |
| DevOps             | deploy, docker, kubernetes, ci-cd           |
| 文档编写            | docs, readme, changelog, api-docs         |
| 代码质量            | review, lint, refactor, best-practices       |
| 设计                | ui, ux, design-system, accessibility        |
| 生产力工具            | workflow, automation, git                 |

## 提高搜索效率的技巧：
1. **搜索所有可用注册库**：每个注册库可能包含不同的技能
2. **使用具体关键词**：例如，使用 “react testing” 而不是简单的 “testing”
3. **尝试替代关键词**：如果 “deploy” 没有找到结果，可以尝试 “deployment” 或 “ci-cd”
4. **查看热门来源**：许多 skills.sh 中的技能来自 `vercel-labs/agent-skills` 或 `ComposioHQ/awesome-claude-skills`
5. **对于 tessl.io**：由于仅支持交互式搜索，建议直接在网页上浏览
6. **对于 clawhub**：如果未安装命令行工具，请先使用 `npm install -g clawhub` 进行安装

## 未找到相关技能时

如果在任何可用注册库中都未找到所需技能：
1. 告知用户未找到相关技能
2. 表示可以使用自己的技能来帮助用户完成任务
3. 建议用户自行创建所需的技能

**示例响应：**
```
I searched all available registries for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
- With skills.sh: npx skills init my-xyz-skill
- With tessl.io: tessl skill new --name "My X Skill" --description "..."
```

## 安装缺失的命令行工具

如果用户希望使用 clawhub 但尚未安装该工具：

```bash
npm install -g clawhub
```

**对于 tessl.io 的安装说明：**
```bash
npm install -g tessl
```