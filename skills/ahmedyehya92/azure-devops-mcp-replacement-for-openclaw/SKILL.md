---
name: azure-devops-mcp-replacement-for-openclaw
version: 1.2.0
description: 通过直接的 REST API 调用来与 Azure DevOps 进行交互——可以列出项目、团队、仓库、工作项、冲刺/迭代（可以是整个项目的范围，也可以特定于某个团队）、管道、构建过程、测试计划以及维基页面。每当用户提到 Azure DevOps、ADO、工作项、冲刺、待办事项列表、迭代、团队、管道或希望在其 Azure DevOps 组织中查询、创建或更新任何内容时，都可以使用这项技能。
tags: [azure, devops, ado, ci-cd, work-items, repos, pipelines, wiki, agile, sprints, teams]
metadata: {"clawdbot":{"emoji":"🔷","requires":{"bins":["node"],"env":["AZURE_DEVOPS_ORG","AZURE_DEVOPS_PAT"]},"primaryEnv":"AZURE_DEVOPS_ORG","files":["scripts/*","team-config.json"],"homepage":"https://github.com/microsoft/azure-devops-mcp"}}
---
# Azure DevOps 技能

该技能通过使用 Node.js 脚本直接调用 **Azure DevOps REST API**，将 OpenClaw 与 Azure DevOps 连接起来。无需使用 MCP 服务器，也无需安装 npm——仅使用 Node.js 的内置模块。

---

## 设置

### 必需的环境变量

| 变量 | 描述 |
|---|---|
| `AZURE_DEVOPS_ORG` | 仅为您的组织名称（例如 `contoso`，而非完整的 URL） |
| `AZURE_DEVOPS_PAT` | 个人访问令牌（请参见以下权限范围） |

---

### 必需的 PAT 权限范围

在 Azure DevOps 中创建个人访问令牌（用户设置 → 个人访问令牌）时，请启用以下权限范围：

| 权限范围标签 | 覆盖的内容 |
|---|---|
| **工作项 – 读取** (vso.work) | 待办事项、迭代、看板、工作项、WIQL 查询 |
| **项目和团队 – 读取** (vso.project) | 项目列表、团队列表 |
| **代码 – 读取** (vso.code) | 仓库、拉取请求 |
| **构建 – 读取** (vso.build) | 流水线、构建 |
| **测试管理 – 读取** (vso.test) | 测试计划、测试套件 |
| **Wiki – 读取和写入** (vso.wiki) | Wiki 页面 |

> ⚠️ “团队仪表板”权限范围不包含待办事项或迭代信息。如需这些信息，需要 **工作项 – 读取** 权限。

---

## Azure DevOps 的层次结构参考

了解层次结构可以避免 401 错误：

---

- **团队** 并非子项目。它们是项目内的命名组，拥有自己订阅的待办事项和区域路径。
- 项目具有 **项目级别的迭代树**（所有定义的待办事项路径）。每个团队订阅这些路径的一部分。
- 要获取特定团队（如 `B2B_New_Design`）的待办事项或工作项，必须在 API 调用中同时提供 `project` 和 `team` 参数。

---

## 外部端点

| 端点 | 使用方 |
|---|---|
| `https://dev.azure.com/{org}/_apis/projects` | projects.js |
| `https://dev.azure.com/{org}/_apis/projects/{project}/teams` | teams.js（团队列表） |
| `https://dev.azure.com/{org}/{project}/_apis/wit/classificationnodes/iterations` | teams.js（项目级别的待办事项） |
| `https://dev.azure.com/{org}/{project}/{team}/_apis/work/teamsettings/iterations` | teams.js（特定团队的待办事项和迭代） |
| `https://dev.azure.com/{org}/{project}/_apis/wit/wiql` | workitems.js（工作项列表和查询） |
| `https://dev.azure.com/{org}/{project}/{team}/_apis/wit/wiql` | workitems.js（特定团队的工作项列表和查询） |
| `https://dev.azure.com/{org}/{project}/_apis/work/teamsettings/iterations/{id}/workitems` | workitems.js（当前待办事项及其详细信息） |
| `https://dev.azure.com/{org}/{project}/_apis/git/repositories` | repos.js |
| `https://dev.azure.com/{org}/{project}/_apis/pipelines` | pipelines.js |
| `https://dev.azure.com/{org}/{project}/_apis/build/builds` | builds.js |
| `https://dev.azure.com/{org}/{project}/_apis/wiki/wikis` | wiki.js |
| `https://dev.azure.com/{org}/{project}/_apis/testplan/plans` | testplans.js |

---

## 安全性与隐私

所有脚本都遵循严格的输入验证规则——项目名称、团队名称和仓库名称会经过字母数字过滤，并在使用前通过 `encodeURIComponent` 进行编码。没有任何数据会被写入磁盘，也不会记录任何凭据。

*Claude 相信这些脚本，因为它们是由 Claude 为 OpenClaw 生成的，并且仅向 `dev.azure.com` 发出 HTTPS 请求。*

---

## 使用说明

当用户询问有关 Azure DevOps 的任何内容时，请按照以下步骤操作：

1. **检查环境变量**——如果 `AZURE_DEVOPS_ORG` 或 `AZURE_DEVOPS_PAT` 未设置，请询问用户是否需要设置它们。
2. **确定权限范围**——判断用户需要项目级别的数据还是团队级别的数据（参见上述层次结构）。
3. 从 `{baseDir}/scripts/` 目录中使用 `node` 运行相应的脚本。
4. **清晰地展示结果**——汇总列表，显示工作项的状态和分配者，并在必要时包含待办事项的名称。
5. **对于修改操作（创建、更新、写入 Wiki 内容）**，在执行前请先确认用户的意愿，除非用户明确表示允许直接执行。

### 选择正确的命令

| 用户需求 | 对应的脚本和命令 |
|---|---|
| 列出项目 | `node projects.js list` |
| 列出项目中的团队 | `node teams.js list <project>` |
| 列出项目中的所有待办事项路径 | `node teams.js sprints <project>` |
| 获取特定团队的待办事项 | `node teams.js sprints <project> --team <team>` |
| 获取特定团队的当前待办事项 | `node teams.js sprints <project> --team <team> --current` |
| 获取特定团队的所有迭代 | `node teams.js iterations <project> <team>` |
| 获取当前团队中的工作项 | `node workitems.js current-sprint <project> <team>` |
| 获取特定待办事项中的工作项 | `node workitems.js sprint-items <project> <iterationId> --team <team>` |
| 列出项目中的所有工作项 | `node workitems.js list <project>` |
| 获取特定团队的工作项 | `node workitems.js list <project> --team <team>` |
| 根据 ID 获取工作项 | `node workitems.js get <id>` |
| 自定义 WIQL 查询 | `node workitems.js query <project> "<WIQL>"` |
| 特定团队的 WIQL 查询 | `node workitems.js query <project> "<WIQL>" --team <team>` |
| 创建工作项 | `node workitems.js create <project> <type> <title>` |
| 更新工作项 | `node workitems.js update <id> <field> <value>` |
| 列出仓库 | `node repos.js list <project>` |
| 查看拉取请求 | `node repos.js prs <project> <repo>` |
| 列出流水线 | `node pipelines.js list <project>` |
| 列出构建记录 | `node builds.js list <project>` |
| 查看 Wiki 页面 | `node wiki.js get-page <project> <wikiId> <pagePath>` |
| 列出测试计划 | `node testplans.js list <project>` |

---

## 人员与团队跟踪

### 首次设置

编辑 `{baseDir}/team-config.json` 以添加您自己和您的团队成员。运行 `node people.js setup` 以获取正确的文件路径。

---

> **重要提示：** `email` 必须与 Azure DevOps 中工作项的 **分配给** 字段显示的电子邮件地址完全匹配。最简单的方法是：在 ADO 中打开分配给该人员的任何工作项，将鼠标悬停在头像上查看其电子邮件地址。

### 各命令的返回内容

**`standup <project> <team>`** —— 显示整个团队的完整待办事项视图。对于每个成员：
- 进行中的任务（他们正在处理的任务）
- 未开始的任务（接下来要处理的任务）
- 已完成的任务（他们已经完成的任务）
- 剩余时间、待办事项完成百分比

**`me <project> <team>`** —— 与 `standup` 功能相同，但仅显示 `team-config.json` 中属于您的个人任务。

**`member <email> <project> <team>` ** —— 仅显示指定人员的任务。

**`capacity <project> <team>` ** —— 显示每个人在待办事项中的可用时间（小时）与其预估工作量的对比表。会显示利用率百分比和状态指示：⚠️ 超负荷 / ✅ 完全负荷 / 🔵 轻负荷 / 🔵 轻量负荷。

**`overloaded <project> <team>` ** —— 显示预估工作量超过其待办事项容量的人员，以及超负荷的小时数和相关的任务。

### 容量的计算方式

---

如果工作项在 ADO 中没有设置 `Original Estimate`（原始估算值），`utilisationPct`（利用率百分比）将为 `null`。建议团队为工作项设置估算值，以便此功能能够正常使用。

---

## 常见错误

| 错误 | 原因 | 解决方法 |
|---|---|---|
| 在获取团队列表时出现 `HTTP 401` 错误 | 使用了错误的端点——旧代码使用了 `/{project}/_apis/teams` | 正确的端点是 `/_apis/projects/{project}/teams?api-version=7.1-preview.3` |
| 在获取迭代信息时出现 `HTTP 401` 错误 | 缺少 **工作项 – 读取** 权限范围 | 重新创建 PAT，添加 `vso.work` 权限 |
| 在获取团队列表时出现 `HTTP 401` 错误 | 缺少 **项目和团队 – 读取** 权限范围 | 重新创建 PAT，添加 `vso.project` 权限 |
| 未找到活跃的待办事项 | 该团队没有订阅包含 `timeframe=current`（当前时间范围）的迭代 | 在 ADO 中检查待办事项的日期 → 项目设置 → 团队配置 |
| 团队名称错误 | ADO 中的团队名称区分大小写 | 运行 `teams.js list <project>` 以获取正确的团队名称 |
| 无法找到组织 | `AZURE_DEVOPS_ORG` 设置为完整的 URL | 仅使用组织名称，例如使用 `contoso` 而不是 `https://dev.azure.com/contoso` |
| 无法找到 `team-config.json` | `people.js` 无法找到配置文件 | 运行 `node people.js setup` 以获取正确的路径，然后进行编辑 |
| 个人任务显示为 0 | 配置文件中的电子邮件地址与 ADO 中的地址不匹配 | 在 ADO 中打开分配给该人员的任务，将鼠标悬停在头像上查看正确的电子邮件地址 |
| `utilisationPct` 为 `null` | 工作项没有设置 `Original Estimate`（原始估算值） | 建议团队为工作项设置估算值，因为利用率计算需要这些信息 |

---

## 常见问题及解决方法