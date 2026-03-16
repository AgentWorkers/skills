---
name: linear-cli
description: 使用 `linear cli` 从命令行管理 Linear 问题。该技能可实现 Linear 问题的自动化管理。
allowed-tools: Bash(linear:*), Bash(curl:*)
---
# Linear CLI

这是一个用于通过命令行管理Linear问题的工具，集成了git和jj功能。

## 前提条件

`linear`命令必须已经在系统的PATH环境中可用。可以通过以下命令进行检查：

```bash
linear --version
```

如果尚未安装，请按照以下链接的说明进行安装：
https://github.com/kyaukyuai/linear-cli?tab=readme-ov-file#install

## Markdown内容的最佳实践

在处理包含Markdown的 issue 描述或评论内容时，**始终建议使用基于文件的参数**，而不是将内容作为命令行参数传递：

- 对于 `issue create` 和 `issue update` 命令，使用 `--description-file` 参数。
- 对于 `comment add` 和 `comment update` 命令，使用 `--body-file` 参数。

**使用基于文件的参数的原因：**

- 可以确保Linear Web界面的格式正确显示。
- 可以避免因换行符和特殊字符导致的shell转义问题。
- 可防止Markdown中出现字面意义上的 `\n` 序列。
- 更便于处理多行内容。

**示例工作流程：**

```bash
# Write markdown to a temporary file
cat > /tmp/description.md <<'EOF'
## Summary

- First item
- Second item

## Details

This is a detailed description with proper formatting.
EOF

# Create issue using the file
linear issue create --title "My Issue" --description-file /tmp/description.md

# Or for comments
linear issue comment add ENG-123 --body-file /tmp/comment.md
```

对于简单的一行内容，**仅使用内联参数**（如 `--description`、`--body`）。

## 可用的命令

```
linear auth               # Manage Linear authentication
linear issue              # Manage Linear issues
linear team               # Manage Linear teams
linear project            # Manage Linear projects
linear project-update     # Manage project status updates
linear cycle              # Manage Linear team cycles
linear milestone          # Manage Linear project milestones
linear initiative         # Manage Linear initiatives
linear initiative-update  # Manage initiative status updates (timeline posts)
linear label              # Manage Linear issue labels
linear document           # Manage Linear documents
linear notification       # Manage Linear notifications
linear webhook            # Manage Linear webhooks
linear workflow-state     # Manage Linear workflow states
linear user               # Manage Linear users
linear project-label      # Manage Linear project labels
linear config             # Interactively generate .linear.toml configuration
linear schema             # Print the GraphQL schema to stdout
linear api                # Make a raw GraphQL API request
```

## 参考文档

- [auth](references/auth.md) - 管理Linear认证
- [issue](references/issue.md) - 管理Linear问题
- [team](references/team.md) - 管理Linear团队
- [project](references/project.md) - 管理Linear项目
- [project-update](references/project-update.md) - 管理项目状态更新
- [cycle](references/cycle.md) - 管理Linear团队周期
- [milestone](references/milestone.md) - 管理Linear项目里程碑
- [initiative](references/initiative.md) - 管理Linear计划
- [initiative-update](references/initiative-update.md) - 管理计划状态更新（时间线帖子）
- [label](references/label.md) - 管理Linear问题标签
- [document](references/document.md) - 管理Linear文档
- [notification](references/notification.md) - 管理Linear通知
- [webhook](references/webhook.md) - 管理Linear Webhook
- [workflow-state](references/workflow-state.md) - 管理Linear工作流状态
- [user](references/user.md) - 管理Linear用户
- [project-label](references/project-label.md) - 管理Linear项目标签
- [config](references/config.md) - 交互式生成 `.linear.toml` 配置文件
- [schema](references/schema.md) - 将GraphQL模式输出到标准输出
- [api](references/api.md) - 发送原始GraphQL API请求

有关组织功能的详细示例（计划、标签、项目、批量操作等），请参阅 [organization-features](references/organization-features.md)。

## 查看可用选项

要查看所有可用的子命令和参数，请在任何命令后运行 `--help`：

```bash
linear --help
linear issue --help
linear issue list --help
linear issue create --help
```

每个命令都会提供详细的帮助信息，说明所有可用的参数和选项。

## 直接使用Linear GraphQL API

**对于所有支持的操作，优先使用CLI。** `api` 命令仅应在CLI无法处理的查询情况下作为备用方案使用。

### 查看可用类型和字段

将GraphQL模式写入临时文件，然后进行查询：

```bash
linear schema -o "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -i "cycle" "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -A 30 "^type Issue " "${TMPDIR:-/tmp}/linear-schema.graphql"
```

### 发送GraphQL请求

**重要提示：** 包含非空类型标记（例如 `String` 后面跟着感叹号）的GraphQL查询必须通过 heredoc 标准输入（stdin）传递，以避免转义问题。不包含这些标记的简单查询可以直接内联传递。

```bash
# Simple query (no type markers, so inline is fine)
linear api '{ viewer { id name email } }'

# Query with variables — use heredoc to avoid escaping issues
linear api --variable teamId=abc123 <<'GRAPHQL'
query($teamId: String!) { team(id: $teamId) { name } }
GRAPHQL

# Search issues by text
linear api --variable term=onboarding <<'GRAPHQL'
query($term: String!) { searchIssues(term: $term, first: 20) { nodes { identifier title state { name } } } }
GRAPHQL

# Numeric and boolean variables
linear api --variable first=5 <<'GRAPHQL'
query($first: Int!) { issues(first: $first) { nodes { title } } }
GRAPHQL

# Complex variables via JSON
linear api --variables-json '{"filter": {"state": {"name": {"eq": "In Progress"}}}}' <<'GRAPHQL'
query($filter: IssueFilter!) { issues(filter: $filter) { nodes { title } } }
GRAPHQL

# Pipe to jq for filtering
linear api '{ issues(first: 5) { nodes { identifier title } } }' | jq '.data.issues.nodes[].title'
```

### 高级用法：直接使用curl

在需要完全控制HTTP请求的情况下，请使用 `linear auth token`：

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $(linear auth token)" \
  -d '{"query": "{ viewer { id } }"}'
```