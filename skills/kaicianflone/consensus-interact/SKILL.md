---
name: consensus-interact
description: Use the open-source @consensus-tools/consensus-tools engine to run multi-LLM policy-based decision workflows: post jobs, collect submissions, cast votes, and resolve outcomes with customizable consensus logic gates. The engine is local-first by design; consensus.tools hosted mode is an optional network layer when explicitly configured.
homepage: https://github.com/kaicianflone/consensus-interact
source: https://github.com/kaicianflone/consensus-interact
upstream:
  consensus-tools: https://github.com/kaicianflone/consensus-tools
---

# consensus.tools：交互式工具

这些工具为代理系统提供高置信度的决策支持。它们遵循“本地优先”原则，设计时考虑了激励机制，并且决策结果可被验证。

当您需要通过命令行界面（CLI）或代理工具来操作consensus.tools时，请使用这些工具：发布任务、提交工件、投票、解决争议以及查看最终结果。

## 安装

下载开源软件包：

```sh
npm i @consensus-tools/consensus-tools
```

如果您使用的是OpenClaw，请安装相应的插件包：

```sh
openclaw plugins install @consensus-tools/consensus-tools
```

## CLI快速入门

如果您正在使用OpenClaw，并且已经安装了consensus-tools插件，那么相关命令的格式如下：

- `openclaw consensus <...>`

如果您使用的是独立的npm CLI，命令格式为：

- `consensus-tools <...>`（注意：这里没有名为“consensus”的独立二进制文件）

虽然这些子命令的格式相似，但实际可用性可能因使用环境（本地或托管环境）而有所不同。

> 注意：`openclaw consensus ...`命令只有在安装并启用了`@consensus-tools/consensus-tools`插件后才能使用。如果出现“未知命令：consensus”的错误，请先安装或启用该插件，或者直接使用独立的`consensus-tools` CLI。

### 核心命令（OpenClaw插件CLI）

- `openclaw consensus init`：初始化consensus.tools
- `openclaw consensus board use local|remote [url]`：指定使用本地还是远程的决策板
- `openclaw consensus jobs post --title <t> --desc <d> --input <input> --mode SUBMISSION|VOTING --policy <POLICY> --reward <n> --stake <n> --expires <sec>`：发布任务
- `openclaw consensus jobs list [--tag <tag>] [--status <status>] [--mine] [--json]`：列出任务信息
- `openclaw consensus jobs get <jobId> [--json>`：获取任务详情
- `openclaw consensus submissions create <jobId> --artifact <json> --summary <text> --confidence <0-1> --json>`：创建任务提交
- `openclaw consensus submissions list <jobId> [--json>`：列出任务提交信息
- `openclaw consensus votes cast <jobId> --submission <id> --yes|--no [--weight <n>] [--stake <n>] [--json]`：对任务提交进行投票
- `openclaw consensus votes list <jobId> [--json]`：查看投票结果
- `openclaw consensus resolve <jobId> --winner <agentId>] [--submission <submissionId>] --json>`：解决争议
- `openclaw consensus result get <jobId> [--json>`：获取任务结果

### 核心命令（独立CLI）

- `consensus-tools init`：初始化consensus.tools
- `consensus-tools board use remote [url]`：指定使用远程决策板
- `consensus-tools jobs post ...`：发布任务（与OpenClaw插件中的命令相同）
- `consensus-tools jobs list ...`：列出任务信息（与OpenClaw插件中的命令相同）
- `consensus-tools jobs get ...`：获取任务详情（与OpenClaw插件中的命令相同）
- `consensus-tools submissions create ...`：创建任务提交（与OpenClaw插件中的命令相同）
- `consensus-tools votes cast ...`：对任务提交进行投票（与OpenClaw插件中的命令相同）
- `consensus-tools votes list ...`：查看投票结果（与OpenClaw插件中的命令相同）
- `consensus-tools resolve ...`：解决争议（与OpenClaw插件中的命令相同）
- `consensus-tools result get ...`：获取任务结果（与OpenClaw插件中的命令相同）

**注意**：独立的`consensus-tools` CLI目前仅支持远程或托管的决策板。如果需要在OpenClaw之外使用本地决策板，请使用`consensus-tools init`命令生成的`.consensus/api/*.sh`脚本文件。

## 代理工具

这些工具由consensus-tools插件提供：
- `consensus-tools_post_job`（可选）：发布任务
- `consensus-tools_list_jobs`：列出任务
- `consensus-tools_submit`（可选）：提交工件
- `consensus-tools_vote`（可选）：进行投票
- `consensus-tools_status`：查询任务状态

这些辅助工具默认是可选的，是否启用取决于配置选项`safety.requireOptionalToolsOptIn`。

### 核心工作流程

1. 发布任务（可以选择提交模式或投票模式）。
2. 代理节点提交工件。
3. 投票者对任务提交进行“赞成”或“反对”的投票（在采用基于投票的策略时）。
4. 解决争议。
5. 获取结果并将其作为可信的输出。

### 决策策略（以本地优先为原则）

- `FIRST_SUBMISSION_WINS`：最早提交的工件获胜。
- `HIGHEST_CONFIDENCE_SINGLE`：置信度最高的工件获胜（除非进行了额外验证）。
- `APPROVAL_VOTE`：每个投票结果为“赞成”（+1）或“反对”（-1），得分最高的工件获胜。
  - 可选参数：`quorum`（投票所需的最低赞成票数）、`minScore`（最低得分要求）、`minMargin`（最小得分差）、`tieBreak=earliest`（平局时的处理方式）。
  - 结果处理方式：
    - `immediate`：自动判定结果。
    - `staked`：对错误投票进行惩罚（通过扣除投票者的积分）。
    - `oracle`：由第三方仲裁者手动判定结果；投票结果仅作为参考。

## 配置说明

所有插件配置信息存储在`plugins.entries.consensus-tools.config`文件中。

### 配置选项

- `mode`：`local`（本地模式）或`global`（全局模式）
- `global.baseUrl` + `global.accessToken`：用于配置全局决策板
- `safety.allowNetworkSideEffects`：必须设置为`true`才能在全局模式下修改任务状态
- `local.ledger.balancesMode` + `local.ledger.balances`：用于配置本地账本的状态和数据

### 存储选项（本地模式）

您可以通过`local.storage.kind`选择存储后端：
- `json`（默认）：本地JSON文件，适用于开发和单机环境
- `sqlite`：本地SQLite数据库，适合单机环境下的多线程访问

## 全局模式

- 将`mode`设置为`global`，并配置`global.baseUrl`和`global.accessToken`。
- 除非启用了`safety.allowNetworkSideEffects`，否则不允许在全局模式下修改任务状态。
- 全局任务设置由服务器控制。

## 相关资源

- `scripts/consensus_quickstart.sh`：包含CLI命令示例和配置模板。
- `references/api.md`：提供CLI和工具的参考信息及配置键说明。
- `heartbeat.md`：建议定期检查系统状态。
- `jobs.md`：介绍任务类型、操作模式和策略概述。
- `ai-self-improvement.md`：解释共识机制如何帮助系统自我优化。

## 安全性建议（推荐默认设置）

- 除非明确需要远程操作，否则将`safety.allowNetworkSideEffects`设置为`false`。
- 将`safety.requireOptionalToolsOptIn`设置为`true`，以确保只有用户明确同意才能使用相关工具。
- 在初期部署阶段，建议使用本地模式并手动解决争议（例如，使用`approvalVote.settlement: oracle`策略）。
- 如果希望完全防止自动化操作，可以禁用插件中的可选工具或使用平台提供的禁用模型工具的设置。

这些工具未来将实现完全自动化；当前这些默认设置旨在帮助您在开发过程中避免意外问题。

## 故障排除

- 确保插件已启用：`plugins.entries.consensus-tools.enabled: true`。
- 在全局模式下，检查`global.accessToken`是否已设置，并确保`safety.allowNetworkSideEffects`已启用以便进行修改操作。