---
name: ogment
description: 通过 Ogment CLI 调用 MCP 工具——通过 Ogment 的治理层实现安全访问 Linear、Notion、Gmail、PostHog 以及 100 多种 SaaS 服务。
version: 1.0.3
metadata:
  openclaw:
    requires:
      bins:
        - ogment
      anyBins:
        - jq
    install:
      - kind: node
        package: "@ogment-ai/cli"
        bins: [ogment]
      - kind: brew
        formula: jq
        bins: [jq]
    emoji: "🔌"
    homepage: https://ogment.ai
---
# Ogment CLI 功能

通过 Ogment CLI 安全地调用 MCP 工具。您可以通过 Ogment 的管理层访问已连接的 SaaS 工具（如 Linear、Notion、Gmail、Slack、Supabase 等）。

## 快速入门

### 第 1 步：检查登录状态
```bash
ogment auth status
```
- 如果 `loggedIn: true` → 转到第 3 步
- 如果 `loggedIn: false` → 继续执行第 2 步

### 第 2 步：登录（如需要）
```bash
ogment auth login
```

从响应中提取 `verificationUri`，并将其以可点击链接的形式发送给相关人员：
> **🔐 批准 Ogment 的访问权限：**
> 👉 [点击批准](https://dashboard.ogment.ai/cli/approve?authRequestId=...)

等待批准，然后使用 `ogment auth status` 验证登录状态。

### 第 3 步：查看可用的功能
```bash
ogment catalog
ogment catalog <serverId>
```

### 第 4 步：向相关人员汇总信息
> **✅ 已成功连接到 Ogment！** 我可以访问以下内容：
> - **Gmail：** 11 个工具（消息、主题、草稿）
> - **Notion：** 5 个工具（搜索、获取、评论）
> - **Slack：** 7 个工具（对话记录、用户信息）
>
> 您需要我帮忙做什么？

## 核心工作流程

### 发现可用的服务器
```
auth status → catalog → catalog <server> → invoke <server> <tool>
```

### 列出所有工具
```bash
ogment catalog <serverId>
```

### 查看工具的详细信息
```bash
ogment catalog <serverId> <toolName>
```

### 调用某个工具
```bash
ogment invoke <serverId> <toolName> --input '<json>'
```

## 常用操作模式

### Gmail（需要 `userId: "me"`）
```bash
ogment invoke <server> gmail_listMessages --input '{"userId": "me", "maxResults": 10}'
ogment invoke <server> gmail_getMessage --input '{"userId": "me", "messageId": "<id>"}'
```

### Notion
```bash
ogment invoke <server> Notion_notion-search --input '{"query": "quarterly review"}'
```

### Supabase
```bash
ogment invoke <server> Supabase_execute_sql --input '{"query": "SELECT * FROM users LIMIT 5"}'
```

### Linear
```bash
ogment invoke <server> Linear_list_issues --input '{}'
```