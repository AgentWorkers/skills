---
name: bitbucket-automation
description: 通过 Rube MCP (Composio) 自动化 Bitbucket 仓库的管理，包括拉取请求（pull requests）、分支（branches）、问题（issues）以及工作区的管理。在使用任何工具之前，请务必先搜索最新的使用规范和架构信息。
requires:
  mcp: [rube]
---

# 通过 Rube MCP 实现 Bitbucket 自动化

通过 Composio 的 Bitbucket 工具包，可以自动化 Bitbucket 的各种操作，包括仓库管理、拉取请求工作流、分支操作、问题跟踪和工作区管理。

## 先决条件

- 必须已连接 Rube MCP（支持使用 `RUBE_SEARCH_TOOLS`）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `bitbucket` 工具包建立活跃的 Bitbucket 连接
- 在执行任何操作之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具配置信息

## 设置

**获取 Rube MCP**：在客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥，只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 使用 `bitbucket` 工具包调用 `RUBE_MANAGE_CONNECTIONS`。
3. 如果连接未激活，请按照返回的链接完成 Bitbucket OAuth 验证。
4. 在运行任何工作流之前，确认连接状态显示为“ACTIVE”（活跃）。

## 核心工作流

### 1. 管理拉取请求

**使用场景**：用户需要创建、审阅或检查拉取请求。

**操作步骤**：
1. `BITBUCKET_LIST_WORKSPACES` - 查找可访问的工作区（先决条件）
2. `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` - 查找目标仓库（先决条件）
3. `BITBUCKET_LIST_BRANCHES` - 确认源分支和目标分支存在（先决条件）
4. `BITBUCKET_CREATE_pull_REQUEST` - 创建新的拉取请求，指定标题、源分支和可选的审阅者（必选）
5. `BITBUCKET_LIST_pull_REQUESTS` - 按状态（OPEN、MERGED、DECLINED）筛选拉取请求（可选）
6. `BITBUCKET_GETPull_REQUEST` - 通过 ID 获取特定拉取请求的详细信息（可选）
7. `BITBUCKET_GET.Pull_REQUEST_DIFF` - 获取代码差异以供审阅（可选）
8. `BITBUCKET_GET_pull_REQUESTDIFFSTAT` - 获取更改的文件及其添加/删除的行数（可选）

**关键参数**：
- `workspace`：工作区名称或 UUID（所有操作均需提供）
- `repo_slug`：适合 URL 的仓库名称
- `source_branch`：要合并的源分支
- `destination_branch`：目标分支（如果省略，则默认为仓库的主分支）
- `reviewers`：用于分配审阅者的对象列表（包含 `uuid` 字段）
- `state`：用于 `BITBUCKET_LIST_pull_REQUESTS` 的筛选条件（OPEN、MERGED、DECLINED）
- `max_chars`：用于 `BITBUCKET_GET_pull_REQUESTDIFF` 的截断长度，以处理大型差异

**注意事项**：
- `reviewers` 需要一个包含 `uuid` 字段的数组，而不是用户名（格式：`[{"uuid": "{...}"]`）
- UUID 格式必须使用大括号：`{123e4567-e89b-12d3-a456-426614174000}`）
- 如果省略 `destination_branch`，默认使用仓库的主分支，但主分支可能不一定是 `main` 分支
- `pull_request_id` 在 `GETPull_REQUEST` 和 `GET_pull_REQUESTDIFF` 操作中是整数，但在拉取请求列表中会以字符串形式返回
- 大型差异可能导致显示混乱；在 `GET_pull_REQUESTDIFF` 中务必设置 `max_chars`（例如 50000）

### 2. 管理仓库和工作区

**使用场景**：用户需要列出、创建或删除仓库，或探索工作区。

**操作步骤**：
1. `BITBUCKET_LIST_WorkSPACES` - 列出所有可访问的工作区（必选）
2. `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` - 列出工作区内的仓库（支持 BBQL 筛选）
3. `BITBUCKET_CREATE_REPOSITORY` - 创建新仓库，并设置语言、隐私和项目属性（可选）
4. `BITBUCKET_DELETE_REPOSITORY` - 永久删除仓库（不可恢复）（可选）
5. `BITBUCKET_LIST_WORKSPACE_MEMBERS` - 列出工作区成员（用于分配审阅者或权限检查）

**关键参数**：
- `workspace`：工作区名称（通过 `BITBUCKET_LIST_WORKSPACES` 获取）
- `repo_slug`：用于创建/删除操作的仓库名称
- `q`：BBQL 查询过滤器（例如：`name~"api"`、`project.key="PROJ"`、`is_private=true`）
- `role`：按用户角色筛选仓库（member、contributor、admin、owner）
- `sort`：排序字段，可以使用 `-` 前缀进行降序排序（例如：`-updated_on`）
- `is_private`：仓库的可见性（默认为 `true`）
- `project_key`：Bitbucket 项目键；省略时使用工作区的默认项目

**注意事项**：
- `BITBUCKET_DELETE_REPOSITORY` 是不可逆操作，且不会影响仓库的分支
- BBQL 字符串值必须使用双引号括起来（例如：`name~"my-repo"`）
- `repository` 不是一个有效的 BBQL 字段，应使用 `name` 代替
- 默认每页显示 10 个结果；如需完整列表，请明确设置 `pagelen`
- `CREATE_REPOSITORY` 默认创建私有仓库；如需公共仓库，请设置 `is_private: false`

### 3. 管理问题

**使用场景**：用户需要创建、更新、列出或评论仓库中的问题。

**操作步骤**：
1. `BITBUCKET_LIST_ISSUES` - 列出问题（支持状态、优先级和类型的筛选）
2. `BITBUCKET_CREATE_ISSUE` - 创建新问题，并指定标题、内容和优先级（必选）
3. `BITBUCKET_UPDATE_ISSUE` - 修改问题属性（如状态、优先级、分配者等）（可选）
4. `BITBUCKET_CREATE_ISSUECOMMENT` - 为现有问题添加 Markdown 评论（可选）
5. `BITBUCKET_DELETE_ISSUE` - 永久删除问题（可选）

**关键参数**：
- `issue_id`：问题的唯一标识符
- `title`、`content`：创建问题时必填
- `kind`：问题类型（bug、enhancement、proposal、task）
- `priority`：问题的优先级（trivial、minor、major、critical、blocker）
- `state`：问题的状态（new、open、resolved、on hold、invalid、duplicate、wontfix、closed）
- `assignee`：创建问题时使用 Bitbucket 用户名；更新问题时使用 `assignee_account_id`（UUID）
- `due_on`：问题的截止日期（ISO 8601 格式字符串）

**注意事项**：
- 仓库必须启用问题跟踪功能（`has_issues: true`），否则 API 调用会失败
- `CREATE_ISSUE` 使用 `assignee`（用户名字符串），而 `UPDATE_ISSUE` 使用 `assignee_account_id`（UUID）——这两个字段不同
- `DELETE_ISSUE` 是不可逆操作，无法撤销
- `state` 值中包含空格（例如：`on hold` 应写为 `"on_hold"`）
- 在 `LIST_ISSUES` 中按 `assignee` 筛选时使用账户 ID，而不是用户名；未分配问题时使用 `"null"` 字符串

### 4. 管理分支

**使用场景**：用户需要创建分支或查看分支结构。

**操作步骤**：
1. `BITBUCKET_LIST_BRANCHES` - 列出分支（支持 BBQL 筛选和排序）
2. `BITBUCKET_CREATE.Branch` - 根据特定的提交哈希创建新分支（必选）

**关键参数**：
- `name`：分支名称（不包含 `refs/heads/` 前缀）
- `target_hash`：要创建分支的提交哈希（必须存在于仓库中）
- `q`：BBQL 筛选器（例如：`name~"feature/"`、`name="main"`）
- `sort`：按名称排序或按提交日期降序排序（`-target.date`）
- `pagelen`：每页显示 1-100 个结果（默认为 10）

**注意事项**：
- `CREATE.Branch` 需要完整的提交哈希，而不是分支名称
- 分支名称必须遵循 Bitbucket 的命名规则（字母数字、`/`、`.`、`_`）
- BBQL 字符串值必须使用双引号括起来（例如：`name~"feature/"`）

### 5. 为拉取请求添加评论

**使用场景**：用户需要为拉取请求添加评论，包括内联代码评论。

**操作步骤**：
1. `BITBUCKET_GET_pull_REQUEST` - 获取拉取请求的详细信息并确认其存在（先决条件）
2. `BITBUCKET_GET.Pull_REQUESTDIFF` - 查看实际的代码更改（先决条件）
3. `BITBUCKET_GET_pull_REQUESTDIFFSTAT` - 获取更改的文件列表（可选）
4. `BITBUCKET_CREATE_pull_REQUESTCOMMENT` - 发布评论（必选）

**关键参数**：
- `pull_request_id`：拉取请求的 ID
- `content_raw`：Markdown 格式的评论文本
- `content_markup`：默认为 `markdown`；也支持 `plaintext`
- `inline`：包含 `path`、`from`、`to` 的对象，用于创建内联评论
- `parent_comment_id`：现有评论的 ID（用于创建关联的回复）

**注意事项**：
- `pull_request_id` 在 `CREATE_pull_REQUESTCOMMENT` 中是字符串类型，但在 `GET_pull_REQUEST` 中是整数类型
- 创建内联评论时至少需要提供 `inline.path`；`from`/`to` 是可选的行号
- `parent_comment_id` 用于创建关联的回复；对于顶级评论可以省略

## 常见模式

### ID 解析

在操作之前，始终将人类可读的名称转换为 ID：
- **工作区**：使用 `BITBUCKET_LIST_WORKSPACES` 获取工作区名称
- **仓库**：使用 `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` 和 `q` 筛选器获取仓库名称
- **分支**：使用 `BITBUCKET_LIST_BRANCHES` 在创建拉取请求前确认分支存在
- **成员**：使用 `BITBUCKET_LIST_WORKSPACE_MEMBERS` 获取审阅者的 UUID

### 分页

Bitbucket 使用基于页面的分页机制（非基于游标的）：
- 使用 `page`（从 1 开始）和 `pagelen`（每页显示的项数）参数
- 默认每页显示 10 个结果；请明确设置 `pagelen`（拉取请求最多 50 个，其他操作最多 100 个）
- 通过检查响应中的 `next` URL 或总记录数来判断是否存在更多页面
- 为获取完整结果，请遍历所有页面

### BBQL 筛选

Bitbucket 的查询语言支持在列表端点中使用：
- 字符串值必须使用双引号括起来（例如：`name~"pattern"`）
- 运算符：`=`（等于）、`~`（包含）、`!=`（不等于）、`>`、`>=`、`<`、`<=`
- 可以使用 `AND` / `OR` 进行组合（例如：`name~"api" AND is_private=true`

## 常见问题

### ID 格式

- **工作区**：使用字符串格式（例如：`my-workspace`）或大括号中的 UUID（例如：`{uuid}`）
- **审阅者 UUID** 必须使用大括号括起来（例如：`{123e4567-e89b-12d3-a456-426614174000}`）
- **问题 ID** 是字符串；在某些工具中拉取请求 ID 是整数，在其他工具中是字符串
- 提交哈希必须是完整的 SHA1 格式（40 个字符）

### 参数注意事项

- `assignee` 与 `assignee_account_id`：`CREATE_ISSUE` 使用用户名，`UPDATE_ISSUE` 使用 UUID
- 问题状态的值中包含空格（例如：`on hold` 应写为 `"on_hold"`）
- 如果省略 `destination_branch`，默认使用仓库的主分支，但主分支不一定是 `main`
- `repository` 不是一个有效的 BBQL 字段，应使用 `name`

### 速率限制

Bitbucket Cloud API 有速率限制；批量操作时应适当延迟
- 分页请求会计入速率限制；尽量减少不必要的页面请求

### 破坏性操作

- `BITBUCKET_DELETE_REPOSITORY` 是不可逆操作，且不会删除分支
- `BITBUCKET_DELETE_ISSUE` 是永久性的操作，无法恢复
- 在执行删除操作前请务必确认用户同意

## 快速参考

| 操作 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 列出工作区 | `BITBUCKET_LIST_WORKSPACES` | `q`, `sort` |
| 列出仓库 | `BITBUCKET_LIST_REPOSITORIES_IN_WORKSPACE` | `workspace`, `q`, `role` |
| 创建仓库 | `BITBUCKET_CREATE_REPOSITORY` | `workspace`, `repo_slug`, `is_private` |
| 删除仓库 | `BITBUCKET_DELETE_REPOSITORY` | `workspace`, `repo_slug` |
| 列出分支 | `BITBUCKET_LIST_BRANCHES` | `workspace`, `repo_slug`, `q` |
| 创建分支 | `BITBUCKET_CREATE.Branch` | `workspace`, `repo_slug`, `name`, `target_hash` |
| 列出拉取请求 | `BITBUCKET_LIST_pull_REQUESTS` | `workspace`, `repo_slug`, `state` |
| 创建拉取请求 | `BITBUCKET_CREATE_pull_REQUEST` | `workspace`, `repo_slug`, `title`, `source_branch` |
| 获取拉取请求详细信息 | `BITBUCKET_GET_pull_REQUEST` | `workspace`, `repo_slug`, `pull_request_id` |
| 获取拉取请求差异 | `BITBUCKET_GET_pull_REQUESTDIFF` | `workspace`, `repo_slug`, `pull_request_id`, `max_chars` |
| 获取拉取请求差异统计信息 | `BITBUCKET_GET_pull_REQUESTDIFFSTAT` | `workspace`, `repo_slug`, `pull_request_id` |
| 为拉取请求添加评论 | `BITBUCKET_CREATE_pull_REQUESTCOMMENT` | `workspace`, `repo_slug`, `pull_request_id`, `content_raw` |
| 列出问题 | `BITBUCKET_LIST_ISSUES` | `workspace`, `repo_slug`, `state`, `priority` |
| 创建问题 | `BITBUCKET_CREATE_ISSUE` | `workspace`, `repo_slug`, `title`, `content` |
| 更新问题 | `BITBUCKET_UPDATE_ISSUE` | `workspace`, `repo_slug`, `issue_id` |
| 为问题添加评论 | `BITBUCKET_CREATE_ISSUECOMMENT` | `workspace`, `repo_slug`, `issue_id`, `content` |
| 删除问题 | `BITBUCKET_DELETE_ISSUE` | `workspace`, `repo_slug`, `issue_id` |
| 列出工作区成员 | `BITBUCKET_LIST_WORKSPACE_MEMBERS` | `workspace` |