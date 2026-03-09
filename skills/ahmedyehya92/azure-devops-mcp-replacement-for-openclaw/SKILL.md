---
name: azure-devops-mcp-replacement-for-openclaw
version: 1.0.0
description: 与 Azure DevOps 交互：列出并管理项目、代码仓库、工作项、管道、构建任务、维基页面、测试计划以及团队。每当用户在讨论 Azure DevOps、ADO（Azure DevOps 的简称）、工作项、冲刺（Sprints）、看板（Boards）、迭代（Iterations）、拉取请求（Pull Requests）、构建任务（Builds）或维基页面时，都可以使用此技能。
homepage: https://github.com/microsoft/azure-devops-mcp
metadata:
  clawdbot:
    emoji: "🔷"
    requires:
      env: ["AZURE_DEVOPS_ORG", "AZURE_DEVOPS_PAT"]
    primaryEnv: "AZURE_DEVOPS_PAT"
    files: ["scripts/*"]
---
# Azure DevOps 技能

该技能通过 REST API 将 OpenClaw 与 Azure DevOps 连接起来。所有请求均使用个人访问令牌（Personal Access Token, PAT），并在本地通过 Node.js 脚本执行——无需 Microsoft Connect Portal (MCP)。

## 设置

### 1. 创建个人访问令牌 (PAT)

1. 访问 `https://dev.azure.com/<your-org>/_usersSettings/tokens`
2. 点击 **新建令牌**
3. 授予以下权限：**工作项**（读取和写入）、**代码**（读取）、**构建**（读取）、**发布**（读取）、**测试管理**（读取）、**Wiki**（读取和写入）、**项目和团队**（读取）
4. 复制令牌内容——该令牌不会再次显示

### 2. 设置环境变量

```bash
export AZURE_DEVOPS_ORG=contoso          # your org name only, no URL
export AZURE_DEVOPS_PAT=your_token_here
```

或者将它们添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "azure-devops": {
        "enabled": true,
        "env": {
          "AZURE_DEVOPS_ORG": "contoso",
          "AZURE_DEVOPS_PAT": "your_token_here"
        }
      }
    }
  }
}
```

### 3. 安装脚本依赖项

```bash
cd {baseDir}
npm install
```

---

## 可用的脚本

所有脚本都位于 `{baseDir}/scripts/` 目录下。通过 OpenClaw 的 `exec` 工具来运行这些脚本。脚本的参数总是按位置传递的，并在脚本中明确列出。

### 项目与团队

```bash
node {baseDir}/scripts/projects.js list
node {baseDir}/scripts/projects.js get <project>
node {baseDir}/scripts/teams.js list <project>
node {baseDir}/scripts/teams.js iterations <project> <team>
```

### 工作项

```bash
node {baseDir}/scripts/workitems.js list <project>
node {baseDir}/scripts/workitems.js get <id>
node {baseDir}/scripts/workitems.js current-sprint <project> <team>
node {baseDir}/scripts/workitems.js create <project> <type> <title>
node {baseDir}/scripts/workitems.js update <id> <field> <value>
node {baseDir}/scripts/workitems.js query <project> "<WIQL query>"
```

### 仓库与拉取请求

```bash
node {baseDir}/scripts/repos.js list <project>
node {baseDir}/scripts/repos.js get <project> <repo>
node {baseDir}/scripts/repos.js prs <project> <repo> [status]
node {baseDir}/scripts/repos.js pr-detail <project> <repo> <pr-id>
```

### 管道与构建

```bash
node {baseDir}/scripts/pipelines.js list <project>
node {baseDir}/scripts/pipelines.js runs <project> <pipeline-id> [limit]
node {baseDir}/scripts/builds.js list <project> [limit]
node {baseDir}/scripts/builds.js get <project> <build-id>
```

### Wiki

```bash
node {baseDir}/scripts/wiki.js list <project>
node {baseDir}/scripts/wiki.js get-page <project> <wiki-id> <page-path>
node {baseDir}/scripts/wiki.js create-page <project> <wiki-id> <page-path> "<content>"
node {baseDir}/scripts/wiki.js update-page <project> <wiki-id> <page-path> "<content>"
```

### 测试计划

```bash
node {baseDir}/scripts/testplans.js list <project>
node {baseDir}/scripts/testplans.js suites <project> <plan-id>
```

---

## 使用说明

当用户需要使用 Azure DevOps 功能时，请按照以下步骤操作：

1. **确认凭据**——如果 `AZURE_DEVOPS_ORG` 或 `AZURE_DEVOPS_PAT` 未设置，请在继续之前获取这些信息。
2. **选择合适的脚本**——根据用户的需求选择相应的脚本（参见上面的列表）。
3. **通过 `exec` 命令运行脚本**——使用 OpenClaw 的 `exec` 工具来执行 `{baseDir}/scripts/` 目录下的 Node.js 脚本。
4. **展示输出结果**——脚本返回 JSON 格式的数据；请对其进行解析并清晰地总结。对于列表类型的数据，仅显示关键字段（id、title/name、state）；如需详细信息，请显示所有相关字段。
5. **对于数据修改操作（创建、更新）**——在运行之前务必先与用户确认，除非另有明确指示。

---

## 外部端点

| 端点 | 功能 | 发送的数据 |
|---|---|---|
| `https://dev.azure.com/{org}/` | 所有项目/工作项/仓库/管道/Wiki 的 API | 包含 PAT 认证头、查询参数和 JSON 数据体 |
| `https://vsrm.dev.azure.com/{org}/` | 发布管理（构建相关操作） | 包含 PAT 认证头 |
| `https://vssps.visualstudio.com/{org}/` | 个人资料/身份信息相关 API | 包含 PAT 认证头 |

## 安全性与隐私

- 您的个人访问令牌（PAT）和组织名称不会离开您的设备，仅作为 HTTP 请求头发送到 Microsoft 的 Azure DevOps 服务器。
- 脚本在适用的情况下使用了 `set -euo pipefail` 选项；Node.js 脚本会在执行前验证所有输入内容。
- 任何数据都不会被发送给第三方。

**信任声明：** 该技能会使用您的个人访问令牌（PAT）向 `dev.azure.com` 发送经过认证的请求。仅当您信任 Microsoft 的 Azure DevOps 服务并愿意将其用于处理您的工作数据时，才建议安装此技能。