---
name: mcp-atlassian
description: 在 Docker 中运行 Model Context Protocol (MCP) Atlassian 服务器，以实现与 Jira、Confluence 及其他 Atlassian 产品的集成。当您需要查询 Jira 问题、搜索 Confluence 内容或以编程方式与 Atlassian 服务交互时，请使用该功能。此操作需要 Docker 以及有效的 Jira API 凭据。
---

# MCP Atlassian

## 概述

MCP Atlassian 服务器通过 Model Context Protocol 提供对 Jira 及其他 Atlassian 服务的程序化访问。您可以使用 Docker 运行该服务器，并使用您的 Jira 凭据来查询问题、管理项目以及与 Atlassian 工具进行交互。

## 快速入门

使用您的 Jira 凭据拉取并运行容器：

```bash
docker pull ghcr.io/sooperset/mcp-atlassian:latest

docker run --rm -i \
  -e JIRA_URL=https://your-company.atlassian.net \
  -e JIRA_USERNAME=your.email@company.com \
  -e JIRA_API_TOKEN=your_api_token \
  ghcr.io/sooperset/mcp-atlassian:latest
```

**使用脚本（更快）：**

使用您的 API 令牌运行捆绑的脚本：

```bash
JIRA_API_TOKEN=your_token bash scripts/run_mcp_atlassian.sh
```

## 环境变量

- **JIRA_URL**：您的 Atlassian 实例 URL（例如：`https://company.atlassian.net`）
- **JIRA_USERNAME**：您的 Jira 电子邮件地址
- **JIRA_API_TOKEN**：您的 Jira API 令牌（在 [账户设置 → 安全](https://id.atlassian.com/manage-profile/security/api-tokens) 中创建）

## 将 MCP Atlassian 与 Clawdbot 配合使用

运行完成后，MCP 服务器将提供对 Jira 工具的访问权限。您可以在 Clawdbot 的配置中将此容器作为 MCP 源来查询问题、创建任务或直接管理 Jira。

## 资源

### 脚本
- **run_mcp_atlassian.sh**：一个简化版的运行脚本，用于处理凭据