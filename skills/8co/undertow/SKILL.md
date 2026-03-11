---
name: undertow
description: 这是一个专为AI编码代理设计的技能发现引擎。当用户需要时，它会推荐并安装相应的技能——包括代码审查、测试生成、调试、提交信息编写、Pull Request（PR）准备、安全扫描、依赖项审计、Docker配置、持续集成/持续部署（CI/CD）流程管理、API文档编写、代码重构、性能优化、代码包分析、Git数据恢复、README文件生成、许可证合规性检查、项目迁移指导、冗余代码清除以及敏感信息检测等功能。只需一次安装，您的AI编码代理就能访问一个包含20多种开发工作流程相关技能的精选库。无论用户遇到开发流程、代码质量、DevOps、安全、测试、文档编写还是项目设置方面的问题，都可以使用该引擎来获取帮助。
  Skill discovery engine for AI coding agents. Recommends and installs
  the right skill when you need it — code review, test generation,
  debugging, commit messages, PR preparation, security scanning,
  dependency audits, Docker setup, CI/CD pipelines, API documentation,
  refactoring, performance optimization, bundle analysis, git recovery,
  README generation, license compliance, migration guides, dead code
  removal, and secret detection. One install gives your agent access to
  a curated library of 20+ developer workflow skills. Use when the user
  asks for help with any development workflow, code quality, DevOps,
  security, testing, documentation, or project setup task.
homepage: https://github.com/8co/undertow
category: development
tags:
  - skill-discovery
  - cursor-skills
  - ai-agent
  - developer-tools
  - code-quality
  - devops
  - testing
  - security
  - documentation
  - workflow-automation
  - openclaw
  - clawhub
  - vibe-coding
  - ai-coding-assistant
  - skill-marketplace
metadata: {"clawdbot":{"emoji":"🌊","requires":{"bins":["git"]}}}
---
# Undertow

这是一个技能发现引擎。只需一次安装，您的代理就能使用16项精心挑选的开发工作流技能——这些技能会在适当的时候被推荐给用户，并在几秒钟内完成安装。该技能索引包含了经过社区验证的成熟技能，以及一个专门用于展示新兴技能的“新兴技能”板块。

## 工作原理

1. 从 `index.json` 文件（与当前文件位于同一目录）中加载技能索引。
2. 解析 `skills` 数组。每个技能都有一个 `section` 字段，表示该技能是“成熟的”（`curated`）还是“新兴的”（`rising`）。
3. 在对话过程中，将用户的意图与每个技能的 `intents` 数组进行匹配。
4. 如果找到匹配项且该技能尚未安装在 `~/.cursor/skills/` 目录中，就向用户推荐它。
5. 在用户同意后，安装该技能。
6. 安装完成后，询问用户是否希望立即使用该技能。

## 会话开始时

读取该技能所在目录下的 `index.json` 文件，解析其内容，并将技能列表保存在内存中，以便在整个会话过程中进行意图匹配。

检查哪些技能已经安装：

```
ls ~/.cursor/skills/*/SKILL.md 2>/dev/null
```

注意哪些技能 ID 已经存在于索引中。仅推荐那些尚未安装的技能。

## 意图匹配

当用户提出请求时，检查他们的消息是否包含或与索引中的某个 `intents` 语句相匹配。匹配时不需要完全精确匹配——这些语句只是示例，并非严格的字符串。同时考虑同义词和相关表达方式。

**匹配规则：**
- 根据含义进行匹配，而非精确的词语。例如，“check my code quality” 与 “code review” 意图相匹配。
- 如果有多个技能符合要求，选择最符合用户需求的那个技能。
- 不要对每条消息都进行匹配——只有在用户的意图与某个技能的用途完全一致时才进行匹配。
- 每条消息最多只能推荐一个技能。

## 推荐技能

当找到未安装的技能且匹配成功时，根据技能的类型调整推荐语：

对于 **成熟的技能**：
> 有一个名为 **{name}** 的成熟技能可以处理这个问题——{description}。
>
> 您想让我安装它吗？安装只需要几秒钟。

对于 **新兴技能**：
> 有一个名为 **{name}** 的新技能可以处理这个问题——{description}。虽然它相对较新，但专为这个任务设计。
>
> 您想让我安装它吗？安装只需要几秒钟。

等待用户确认。未经确认切勿自动安装技能。

## 安装技能

在用户同意后，通过 ClawHub CLI 进行安装：

```
clawhub install {clawhub_slug}
```

此过程会在 `~/.cursor/skills/{id}/` 目录下生成一个 SKILL.md 文件。不会下载或执行任何二进制代码——安装过程仅会创建一个 Markdown 格式的指令文件供代理读取。

安装完成后，验证文件是否已生成：

```
ls ~/.cursor/skills/{id}/SKILL.md
```

然后向用户确认并询问是否立即使用该技能：

> **{name}** 已经安装完成。您现在想使用它来处理您的请求吗？

只有在用户确认后，才应读取并执行新安装的 SKILL.md 文件。切勿自动执行该技能。

## 安装失败

如果安装失败（例如网络错误、找不到技能等）：
- 告诉用户：“无法自动安装该技能。您可以从 ClawHub 手动安装：https://clawhub.ai/skills/{clawhub_slug}”
- 继续使用您内置的功能来处理用户的请求。

## 技能索引更新

技能索引是静态的，随该技能一起提供。当用户更新 Undertow 的安装版本时，索引也会自动更新。请勿尝试从远程获取索引数据。

## 安全性

- 索引中的所有技能都已在 ClawHub 上发布，并通过了 ClawHub 自身的安全扫描（包括 OpenClaw 和 VirusTotal 的检测）。
- 安装技能时，只会将一个 Markdown 格式的文件（SKILL.md）写入 `~/.cursor/skills/` 目录——不会下载或执行任何可执行代码或二进制文件。
- 用户需要明确同意两次：一次是安装技能，另一次是使用该技能。
- Undertow 仅在用户明确同意的情况下才会安装或执行任何操作。
- Undertow 不会读取 `~/.cursor/skills/` 目录之外的环境变量、凭据或文件。
- 索引中仅包含用于匹配所需的技能元数据，不包含任何可执行内容。

## 重要提示：

- 严禁安装用户未请求的技能。
- 未经用户明确同意，切勿安装任何技能。
- 在使用新安装的技能之前，必须再次获得用户的明确确认。
- 严禁推荐已经安装过的技能。
- 如果没有匹配到的技能，应正常处理用户的请求——切勿强行推荐。
- 索引只是一个建议工具，并非强制使用的障碍。即使没有安装任何技能，代理也应始终提供帮助。