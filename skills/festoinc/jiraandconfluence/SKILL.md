---
name: jira-ai
version: 1.0.0
description: 用于与 Atlassian Jira 和 Confluence 交互的 CLI 工具
homepage: https://github.com/festoinc/jira-ai
metadata: {"moltbot":{"emoji":"🎫","category":"productivity","api_base":"https://github.com/festoinc/jira-ai"}}
---

# Jira-AI 技能

Jira-AI 技能为 Atlassian 的 Jira 和 Confluence 平台提供全面的命令行访问功能，帮助代理高效地管理问题、项目、用户和文档。

## 安装

要安装 jira-ai，请运行：
```bash
npm install -g jira-ai
```

## 认证设置

在使用 jira-ai 之前，您需要配置 Jira 的凭据：

1. 创建一个 `.env` 文件，并在其中设置以下内容：
   ```
   JIRA_HOST=your-domain.atlassian.net
   JIRA_USER_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-api-token
   ```

2. 使用 `.env` 文件进行认证：
   ```bash
   jira-ai auth --from-file path/to/.env
   ```

## 配置

您可以使用 `settings` 命令来管理配置：

```bash
jira-ai settings --help
```

您可以从 YAML 文件中应用配置：
```bash
jira-ai settings --apply my-settings.yaml
```

验证配置：
```bash
jira-ai settings --validate my-settings.yaml
```

## 命令概述

### 核心命令

| 命令 | 描述 |
| :--- | :--- |
| `jira-ai auth` | 设置 Jira 认证凭据 |
| `jira-ai settings` | 查看、验证或应用配置设置 |
| `jira-ai about` | 显示工具相关信息 |
| `jira-ai help` | 显示命令帮助信息 |

### 问题管理 (`issue`)

| 命令 | 描述 |
| :--- | :--- |
| `jira-ai issue get <issue-id>` | 获取问题的详细信息 |
| `jira-ai issue create` | 创建新的 Jira 问题 |
| `jira-ai issue search <jql-query>` | 执行 JQL 查询 |
| `jira-ai issue transition <issue-id> <to-status>` | 更改问题的状态 |
| `jira-ai issue update <issue-id>` | 更新问题的描述 |
| `jira-ai issue comment <issue-id>` | 为问题添加新评论 |
| `jira-ai issue stats <issue-ids>` | 计算问题的时间相关指标 |
| `jira-ai issue assign <issue-id> <account-id>` | 分配或重新分配问题 |
| `jira-ai issue label add <issue-id> <labels>` | 为问题添加标签 |
| `jira-ai issue label remove <issue-id> <labels>` | 从问题中删除标签 |

### 项目管理 (`project`)

| 命令 | 描述 |
| :--- | :--- |
| `jira-ai project list` | 列出所有可访问的 Jira 项目 |
| `jira-ai project statuses <project-key>` | 获取项目的流程状态 |
| `jira-ai project types <project-key>` | 列出项目可用的问题类型 |

### 用户管理 (`user`)

| 命令 | 描述 |
| :--- | :--- |
| `jira-ai user me` | 显示已认证用户的个人资料 |
| `jira-ai user search [project-key]` | 搜索并列出用户 |
| `jira-ai user worklog <person> <timeframe>` | 获取用户的工单记录 |

### 组织管理 (`org`)

| 命令 | 描述 |
| :--- | :--- |
| `jira-ai org list` | 列出所有保存的 Jira 组织配置文件 |
| `jira-ai org use <alias>` | 切换当前的 Jira 组织配置文件 |
| `jira-ai org add <alias>` | 添加新的 Jira 组织配置文件 |
| `jira-ai org remove <alias>` | 删除组织的凭据 |

### Confluence 命令 (`confl`)

| 命令 | 描述 |
| :--- | :--- |
| `jira-ai confl get <url>` | 下载 Confluence 页面内容 |
| `jira-ai confl spaces` | 列出所有可访问的 Confluence 空间 |
| `jira-ai confl pages <space-key>` | 显示空间内的页面 |
| `jira-ai confl create <space> <title> [parent-page>` | 创建新的 Confluence 页面 |
| `jira-ai confl comment <url>` | 为 Confluence 页面添加评论 |
| `jira-ai confl update <url>` | 更新 Confluence 页面 |

## 使用示例

### 搜索分配给当前用户的问题
```bash
jira-ai issue search "assignee = currentUser()"
```

### 获取特定问题的详细信息
```bash
jira-ai issue get PROJ-123
```

### 创建新问题
```bash
jira-ai issue create --project "PROJ" --summary "New task" --issuetype "Story"
```

### 将问题状态更改为新状态
```bash
jira-ai issue transition PROJ-123 "In Progress"
```

### 为问题添加评论
```bash
jira-ai issue comment PROJ-123 --file comment.md
```

### 列出所有项目
```bash
jira-ai project list
```

### 获取用户的工单记录
```bash
jira-ai user worklog john.doe@example.com 2w
```

## 配置选项

jira-ai 工具支持通过配置文件进行广泛配置。您可以定义：

- 允许访问的 Jira 项目
- 允许使用的命令
- 允许访问的 Confluence 空间
- 各种操作的默认行为

示例配置结构：
```yaml
defaults:
  allowed-jira-projects:
    - all                     # Allow all projects
  allowed-commands:
    - all                     # Allow all commands
  allowed-confluence-spaces:
    - all                     # Allow all Confluence spaces

organizations:
  work:
    allowed-jira-projects:
      - PROJ                  # Allow specific project
      - key: PM               # Project-specific config
        commands:
          - issue.get         # Only allow reading issues
        filters:
          participated:
            was_assignee: true
    allowed-commands:
      - issue                 # All issue commands
      - project.list          # Only project list
      - user.me               # Only user me
    allowed-confluence-spaces:
      - DOCS
```

## 优点

- **高效的 API 使用**：减少执行常见操作所需的 API 调用次数 |
- **批量操作**：一次处理多个项目以降低 API 使用量 |
- **智能过滤**：使用 JQL 仅获取所需的数据 |
- **本地处理**：在向 Jira 发送请求之前先进行本地处理 |
- **基于配置的访问控制**：定义允许使用的命令和项目，防止未经授权的操作 |
- **精确的命令定位**：仅获取所需信息，减少数据量和 API 使用量 |

## 安全注意事项

- 将 API 令牌安全地存储在环境文件中 |
- 使用基于配置的访问控制来限制操作 |
- 定期轮换 API 令牌 |
- 将权限限制在操作所需的最小范围内