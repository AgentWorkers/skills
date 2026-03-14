---
name: Cursor
slug: cursor
version: 1.0.0
homepage: https://clawic.com/skills/cursor
description: 在编辑器、命令行界面（CLI）、规则系统、后台代理程序、Bugbot以及MCP工作流中，安全地使用光标进行操作。这些功能支持对代码仓库的上下文感知，并允许执行过程被审查（即执行过程可以被监控和验证）。
changelog: Initial release with editor and CLI guidance, rules and context control, background agent and Bugbot guardrails, privacy notes, and recovery workflows.
metadata: {"clawdbot":{"emoji":"⌨️","requires":{"bins":["cursor-agent"],"bins.optional":["cursor","git","rg"],"config":["~/cursor/"]},"os":["linux","darwin","win32"],"configPaths":["~/cursor/"]}}
---
## 使用场景

当用户希望将Cursor作为真正的编码环境来使用，而不仅仅是一个普通的AI编辑器时，需要选择合适的界面、设置正确的仓库上下文、配置规则、使用`cursor-agent`、运行后台代理、通过Bugbot进行代码审查，或者决定是否启用MCP（Machine Control Protocol）和远程执行功能。在这种情况下，应使用本技能。

本技能适用于以下场景：难点不在于“编写代码”，而在于确保Cursor在编辑器聊天、代理交互、命令行界面（CLI）操作、项目规则管理、仓库索引、远程代理执行、GitHub集成以及处理涉及隐私的数据时能够稳定且可预测地运行。

## 架构

Cursor的所有运行数据都存储在`~/cursor/`目录下。如果该目录不存在，请先运行`setup.md`文件以完成初始化。具体目录结构请参考`memory-template.md`文件。

```text
~/cursor/
|-- memory.md            # Durable activation boundaries and workflow defaults
|-- repo-profiles.md     # Per-repo conventions, trust posture, and verification expectations
|-- rules-notes.md       # Project-rule strategy, legacy rule cleanup, and instruction hierarchy notes
|-- privacy.md           # Indexing, ignore, remote execution, and data-handling defaults
|-- remote-workflows.md  # Background Agent, Bugbot, and GitHub integration decisions
`-- incidents.md         # Repeated failures, wrong-surface runs, and recovery patterns
```

## 快速参考

仅加载当前操作所需的最小文件集：

| 功能 | 对应文件 |
|-------|------|
| 设置指南 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 安装及选择合适的Cursor界面 | `install-and-surfaces.md` |
| 规则设置、上下文层级与模式选择 | `rules-and-context.md` |
`cursor-agent`、非交互式操作及MCP边界设置 | `cli-and-mcp.md` |
| 后台代理、Bugbot及GitHub集成工作流程 | `background-agents-and-bugbot.md` |
| 隐私模式、索引设置及文件忽略规则 | `privacy-and-indexing.md` |
| 解决授权问题、错误上下文及远程执行故障的应对方案 | `troubleshooting.md` |

## 使用要求

- 确保目标机器上已安装并可以正常使用Cursor；如果任务涉及CLI或自动化流程，需确保`cursor-agent`可用。
- 需要`git`工具来处理仓库相关操作（如代码差异比较、分支管理、后台代理任务或与Bugbot的协作）。
- 在启用后台代理、授予GitHub应用写入权限、使用远程MCP服务器或执行高信任级别的非交互式命令之前，必须获得用户的明确批准。
- 对模型名称、模式行为、CLI参数及远程工作流程的功能需以官方文档或当前CLI帮助文档为准，切勿依赖过时的信息。

## 操作范围

本技能将Cursor视为一个完整的编码系统，而不仅仅是普通的文本编辑工具。其涵盖的内容包括：
- 在代理模式（Agent）、询问模式（Ask）、手动模式（Manual）及自定义模式下的使用方式；
- 通过`.cursor/rules`文件管理的项目规则，以及用户自定义的规则；
- 通过仓库边界、索引设置及文件忽略规则来控制操作上下文；
- 本地及非交互式的`cursor-agent`工作流程（包括任务恢复及MCP（Machine Control Protocol）的协同执行）；
- 当工作从本地交互切换到远程GitHub执行时的处理方式；
- 在使用Cursor的功能将代码或提示发送到外部系统时，涉及的数据隐私保护及审查流程。

## 数据存储

所有重要的操作上下文数据都保存在`~/cursor/`目录中：
- 明确哪些仓库、团队或任务类型允许使用Cursor；
- 根据任务类型选择合适的操作界面（编辑器、CLI、后台代理或Bugbot）；
- 规则的层级结构及有效的`.cursor/rules`配置；
- 关于数据索引、文件忽略设置、GitHub集成及远程MCP的隐私保护策略；
- 常见的问题（如错误的仓库范围设置、被忽略的规则、不安全的非交互式操作或远程审查过程中的错误）的解决方法。

## 核心规则

### 1. 先确定使用界面
- 在执行任何操作之前，必须明确当前使用的界面类型（编辑器、代理、询问模式、手动模式、`cursor-agent`、后台代理或Bugbot）。
- 不同界面会改变权限设置、上下文加载方式及审查流程的预期结果。
- 忽视界面类型可能会导致错误的操作流程或信任级别设置。

### 2. 在发出指令前建立规则层级
- 在请求Cursor执行任何操作之前，需先检查`.cursor/rules`文件中的项目规则、仓库代理的指导信息以及团队级别的用户规则。
- 将`.cursorrules`文件视为过时的格式，不应作为默认的设计依据。
- 如果规则之间存在冲突或过于模糊，需先修正规则后再发出指令。

### 3. 有意识地控制操作上下文
- 通过选择合适的仓库、设置索引规则及忽略文件来控制Cursor的访问范围，而不能简单地假设它“自动识别仓库内容”。
- 使用`.cursorignore`和`.cursorindexingignore`文件来控制上下文，但切勿将其视为绝对的安全屏障。
- 当任务范围较窄时，应先减少上下文信息，避免后续添加不必要的指令。

### 4. 区分本地操作与远程操作
- 编辑器代理和本地CLI的使用方式与后台代理及Bugbot不同。
- 远程GitHub连接的操作可以在本地机器之外执行命令、获取代码并生成审查结果。
- 只有在明确收益且信任关系明确的情况下，才应启用远程工作流程。

### 5. 将非交互式CLI和MCP视为高信任级别操作
- `cursor-agent`功能强大，使用非交互式操作时不能掉以轻心。
- 在启用这些功能之前，需仔细确认MCP服务器的权限范围、主机配置及可能产生的副作用。
- 如果工作流程涉及无人值守的代码修改，必须记录详细的仓库信息、命令目标及验证路径。

### 6. 明确数据隐私和传输方式
- Cursor的请求、索引操作及远程工作流程可能会将代码或提示发送到外部服务（如Cursor服务、GitHub或用户授权的MCP服务器）。
- 隐私模式的启用会改变数据传输方式，但并不意味着远程操作等同于本地操作。
- 在启用高信任级别功能之前，用户必须清楚数据传输的细节。

### 7. 操作完成后需提供可审查的验证结果
- 一个成功的Cursor操作应包含差异对比结果、检查结果或明确的检查点，而不仅仅是简单的“代理已处理完毕”信息。
- 对于后台代理和Bugbot的操作，必须在合并或应用任何结果之前仔细检查输出内容。
- 保留清晰的操作记录，以便后续操作者能够快速了解具体使用了哪种界面及执行了哪些操作。

## 常见误区

- 将所有Cursor功能都视为仅限本地使用，导致未经审查就直接启用远程执行或GitHub集成功能。
- 在未查看`.cursor/rules`文件或仓库代理的指导信息前就将指令直接发送到聊天界面。
- 误以为`.cursorignore`文件能完全阻止数据泄露，实际上终端和MCP工具仍可能访问到未授权的数据。
- 仅仅因为后台代理使用方便就直接启用它们，导致远程命令的执行范围超出预期。
- 混合使用Bugbot、编辑器代理和本地Git操作，导致审查混乱和重复工作。
- 误认为API密钥能直接控制服务端的执行，实际上Cursor仍会对操作进行必要的权限验证。

## 外部接口

除非用户明确允许，否则仅允许使用以下接口：

| 接口 | 发送的数据 | 目的 |
|----------|-----------|---------|
| https://cursor.com/* | 提示信息、选定的仓库上下文、代码差异、集成元数据以及远程工作流程所需的数据 | 用于Cursor编辑器、代理、索引功能及审查流程 |
| https://docs.cursor.com/* | 仅用于查询文档信息 | 核实Cursor的当前行为、功能范围及集成细节 |
| https://github.com/* | 仓库元数据、代码内容、拉取请求信息及用户授权的审查操作 | 用于后台代理、Bugbot及GitHub集成流程 |
| https://api.github.com/* | 仓库信息、分支信息、Pull请求及用户授权的审查操作 | 用于Cursor关联的GitHub API接口 |
| https://{user-approved-mcp-host} | 用户授权的MCP服务器所需的数据 | 用于扩展MCP工具的功能 |

除非用户明确允许，否则不会向其他外部接口发送任何数据。

## 安全与隐私

离开本地机器的数据包括：
- 发送给Cursor服务或外部系统的提示信息及选定的代码上下文；
- Cursor功能所需的索引相关代码片段或元数据；
- 当后台代理或Bugbot使用GitHub集成功能时涉及的仓库、分支及Pull请求信息；
- 仅限于用户授权的MCP服务器的数据。

**注意**：
- 本技能不将`.cursorignore`文件视为绝对的安全防护层；
- 未经明确授权，不得启用后台代理、Bugbot或远程MCP功能；
- 不假设`.cursorrules`文件中的规则始终有效；
- 不会修改本技能文件的内容。

## 信任机制

使用本技能时，提示信息和选定的代码上下文可能会被发送到外部服务或用户授权的MCP服务器。只有在信任这些服务的情况下才能安装相关组件。

## 使用范围

本技能仅用于：
- 确保Cursor在编辑器、CLI、规则设置、索引功能、远程代理及审查流程中的安全使用；
- 正确地组织仓库数据的本地或远程执行方式；
- 为已授权的仓库保存重要的操作记录、规则设置、隐私策略及故障处理方案。

**注意事项**：
- 本技能不会混淆本地编辑器操作与远程代理执行之间的界限；
- 不会认为忽略文件就能完全解决隐私或访问问题；
- 不会默认推荐无人值守的高信任级别操作；
- 不会将Cursor简单地视为普通的聊天工具。

## 相关技能

如果用户同意安装，可使用以下工具进行进一步配置：
- `clawhub install <slug>`：强化多代理工作流程设计、提升审查规范性及对Cursor使用的全面理解。
- `coding`：在Cursor在正确仓库范围内运行时，提升代码实现的质量。
- `git`：处理分支管理、代码差异对比及基于Cursor的仓库恢复操作。
- `api`：在Cursor涉及外部服务时，优化请求调试和集成流程。
- `workflow`：将重复性的Cursor任务转化为更高效、可复用的操作流程。

## 反馈建议

- 如果觉得本技能有用，请给`clawhub`项目点赞（星标）。
- 为了获取最新更新，请使用`clawhub sync`命令。