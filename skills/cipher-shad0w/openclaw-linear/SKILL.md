---
name: linear
description: 使用 `linear CLI` 通过命令行来管理 Linear 的问题、项目、团队和文档。可以创建、更新、列出和跟踪问题；管理项目和里程碑；并与 Linear 的 GraphQL API 进行交互。
homepage: https://github.com/cipher-shad0w/openclaw-linear
metadata: {"openclaw": {"emoji": "🖇️", "os": ["darwin", "linux", "win32"], "requires": {"bins": ["linear"]}, "install": [{"id": "brew", "kind": "brew", "formula": "schpet/tap/linear", "bins": ["linear"], "label": "Install linear CLI (brew)", "os": ["darwin", "linux"]}]}}
---

# Linear

这是一个用于通过命令行管理 Linear 项目问题的 CLI 工具，支持与 Git 和 jj 的集成。

## 前提条件

`linear` 命令必须在系统的 PATH 环境变量中可用。您可以通过以下命令进行检查：

```bash
linear --version
```

如果尚未安装 `linear`：
- **使用 Homebrew**：`brew install schpet/tap/linear`
- **使用 Deno**：`deno install -A --reload -f -g -n linear jsr:@schpet/linear-cli`
- **二进制文件**：[下载地址](https://github.com/schpet/linear-cli/releases/latest)

## 设置

1. 在 [https://linear.app/settings/account/security](https://linear.app/settings/account/security) 创建一个 API 密钥。
2. 登录：`linear auth login`
3. 配置您的项目：`cd my-project-repo && linear config`

## 可用的命令

```text
linear auth               # Manage Linear authentication
linear issue              # Manage Linear issues
linear team               # Manage Linear teams
linear project            # Manage Linear projects
linear project-update     # Manage project status updates
linear milestone          # Manage Linear project milestones
linear initiative         # Manage Linear initiatives
linear initiative-update  # Manage initiative status updates
linear label              # Manage Linear issue labels
linear document           # Manage Linear documents
linear config             # Interactively generate .linear.toml configuration
linear schema             # Print the GraphQL schema to stdout
linear api                # Make a raw GraphQL API request
```

## 常见的工作流程

### 列出和查看问题

```bash
# List your unstarted issues
linear issue list

# List issues in a specific state
linear issue list -s started
linear issue list -s completed

# List all assignees' issues
linear issue list -A

# View the current branch's issue
linear issue view

# View a specific issue
linear issue view ABC-123
```

### 创建和管理问题

```bash
# Create an issue interactively
linear issue create

# Create non-interactively
linear issue create -t "Fix login bug" -d "Users can't log in with SSO" -s "In Progress" -a self --priority 1

# Update an issue
linear issue update ABC-123 -s "Done" -t "Updated title"

# Add a comment
linear issue comment add ABC-123 -b "This is fixed in the latest build"

# Delete an issue
linear issue delete ABC-123 -y
```

### 开始处理问题

```bash
# Pick an issue interactively, creates a git branch and marks it as started
linear issue start

# Start a specific issue
linear issue start ABC-123

# Create a PR with issue details pre-filled
linear issue pr
```

### 项目与里程碑

```bash
# List projects
linear project list

# Create a project
linear project create -n "Q1 Launch" -t ENG -s started --target-date 2026-03-31

# List milestones for a project
linear milestone list --project <projectId>
```

### 文档

```bash
# List documents
linear document list

# Create a document from a file
linear document create --title "Design Spec" --content-file ./spec.md --project <projectId>

# View a document
linear document view <slug>
```

### 团队

```bash
# List teams
linear team list

# List team members
linear team members
```

## 查看帮助信息

在任意命令后加上 `--help` 可以查看该命令的参数和选项：

```bash
linear --help
linear issue --help
linear issue list --help
linear issue create --help
```

## 直接使用 Linear 的 GraphQL API

**建议使用 CLI 进行所有操作；`api` 命令仅用于处理 CLI 未覆盖的查询。**

### 查看 GraphQL 数据结构

```bash
linear schema -o "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -i "cycle" "${TMPDIR:-/tmp}/linear-schema.graphql"
grep -A 30 "^type Issue " "${TMPDIR:-/tmp}/linear-schema.graphql"
```

### 发起 GraphQL 请求

```bash
# Simple query
linear api '{ viewer { id name email } }'

# With variables
linear api 'query($teamId: String!) { team(id: $teamId) { name } }' --variable teamId=abc123

# Complex filter via JSON
linear api 'query($filter: IssueFilter!) { issues(filter: $filter) { nodes { title } } }' \
  --variables-json '{"filter": {"state": {"name": {"eq": "In Progress"}}}}'

# Pipe to jq
linear api '{ issues(first: 5) { nodes { identifier title } } }' | jq '.data.issues.nodes[].title'
```

### 直接使用 curl

```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: $(linear auth token)" \
  -d '{"query": "{ viewer { id } }"}'
```

## 参考文档

有关各个子命令的详细文档（包括所有参数和选项）：

- [issue](references/issue.md) - 管理 Linear 项目中的问题（列出、创建、更新、开始处理、查看、评论、提交 Pull Request、删除）
- [team](references/team.md) - 管理 Linear 团队（列出、创建、删除、查看团队成员、自动生成团队链接）
- [project](references/project.md) - 管理 Linear 项目（列出、查看、创建）
- [document](references/document.md) - 管理 Linear 文档（列出、查看、创建、更新、删除）
- [api](references/api.md) - 发起原始的 GraphQL API 请求

## 配置

CLI 支持使用环境变量或 `.linear.toml` 配置文件进行配置：

| 参数 | 环境变量 | TOML 键 | 示例 |
|---|---|---|---|
| 团队 ID | `LINEAR_TEAM_ID` | `team_id` | `"ENG"` |
| 工作空间 | `LINEAR_WORKSPACE` | `workspace` | `"mycompany"` |
| 问题排序方式 | `LINEAR_ISSUE_sort` | `issue_sort` | `"priority"` 或 `"manual"` |
| 版本控制系统 | `LINEAR_VCS` | `vcs` | `"git"` 或 `"jj"` |

配置文件的位置（按优先级查找）：
1. `./linear.toml` 或 `./.linear.toml`（当前目录）
2. `<repo-root>/linear.toml` 或 `<repo-root>/.linear.toml`
3. `<repo-root>/.config/linear.toml`
4. `~/.config/linear/linear.toml`