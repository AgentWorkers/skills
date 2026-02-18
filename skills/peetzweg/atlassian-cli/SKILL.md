---
name: acli
description: "Atlassian CLI（acli）参考指南：  
Atlassian CLI（acli）是一款用于与Jira Cloud及Atlassian组织管理进行交互的命令行工具。当用户需要执行Jira相关操作（如创建/编辑/搜索/转移工作项、管理项目、看板、冲刺、过滤器、仪表板），或通过终端来管理Atlassian组织（如管理用户、处理身份验证），以及自动化Atlassian工作流程时，可以使用该工具。  
本指南涵盖了所有acli命令，包括：  
- Jira工作项相关命令：创建、编辑、搜索、分配、转移、评论、克隆、链接、归档  
- Jira项目相关命令：创建、列出、更新、归档  
- Jira看板/冲刺相关命令  
- Jira过滤器/仪表板相关命令  
- 管理用户相关命令  
- Rovo Dev（Rovo Dev AI代理）相关命令  
使用acli之前，请确保系统中已安装经过身份验证的acli二进制文件。"
required_tools:
  - acli
env_vars:
  - name: API_TOKEN
    description: "Atlassian API token for non-interactive Jira authentication (optional — only needed for CI/automation, not for interactive OAuth login)"
    required: false
  - name: API_KEY
    description: "Atlassian Admin API key for organization administration commands (optional — only needed for admin commands)"
    required: false
---
# Atlassian CLI (acli) 参考

## 前提条件

使用此功能需要先安装并登录 `acli`。该工具的二进制文件并未包含在本文档中。

如果尚未安装 `acli`，请引导用户访问以下链接进行安装：  
https://developer.atlassian.com/cloud/acli/guides/install-acli/

验证 `acli` 是否已安装：
```bash
acli --help
```

## 登录认证

在运行命令之前，请检查登录状态：
```bash
acli jira auth status
acli admin auth status
```

如果未登录，有以下三种登录方式：

**OAuth（交互式，推荐给用户使用）：**
```bash
acli jira auth login --web
```

**API Token（非交互式，推荐用于持续集成/自动化场景）：**
```bash
echo "$API_TOKEN" | acli jira auth login --site "mysite.atlassian.net" --email "user@atlassian.com" --token
```

**管理员 API 密钥（仅用于管理员命令）：**
```bash
echo "$API_KEY" | acli admin auth login --email "admin@atlassian.com" --token
```

在多个账户之间切换：
```bash
acli jira auth switch --site mysite.atlassian.net --email user@atlassian.com
acli admin auth switch --org myorgname
```

## 安全性

### 保密性处理
- **切勿在命令中硬编码 API Token 或密钥**。始终使用环境变量（如 `$API_TOKEN`、`$API_KEY`）或基于文件的输入方式（例如 `<token.txt>`）。
- **切勿在输出中记录、显示或打印 API Token**。避免通过中间文件（这些文件可能长期保存在磁盘上）传递敏感信息。
- **对于交互式操作，优先使用 OAuth（`--web`）**；只有在 OAuth 不可行时，才使用基于 Token 的认证方式。
- **不要将 API Token 存储在 shell 历史记录中**。如果使用 `echo "$API_TOKEN" | acli ...`，请确保该变量是通过环境变量设置的，而不是作为字面值直接嵌入命令中。

### 破坏性操作

以下命令具有破坏性或不可逆的效果——在执行前务必获得用户确认：
- `acli jira workitem delete` — 永久删除工作项
- `acli jira project delete` — 永久删除项目及其所有工作项
- `acli admin user delete` — 删除用户账户
- `acli admin user deactivate` — 停用用户账户
- `acli jira field delete` — 将自定义字段移至“回收站”

以下命令虽然具有破坏性，但操作结果是可逆的：
- `acli jira workitem archive` / `unarchive` — 归档/解压工作项
- `acli jira project archive` / `restore` — 归档/恢复项目
- `acli admin user cancel-delete` — 取消删除操作
- `acli jira field cancel-delete` — 从“回收站”中恢复字段

**代理安全规则：**
1. 未经用户明确确认，切勿执行任何破坏性命令，即使提供了 `--yes` 选项。
2. 当通过 `--jql` 或 `--filter` 进行批量操作时，先使用相同的查询进行搜索，以显示受影响的对象。
3. 在执行破坏性操作前，优先选择 `--json` 输出格式来验证操作目标。
4. 除非用户明确要求无人值守执行，否则不要将 `--yes` 与破坏性批量操作结合使用。

## 命令结构

```
acli <command> [<subcommand> ...] {MANDATORY FLAGS} [OPTIONAL FLAGS]
```

主要分为四个命令组：
- `acli jira` — Jira Cloud 相关操作（工作项、项目、看板、冲刺、过滤器、仪表板、字段）
- `acli admin` — 组织管理（用户管理、认证）
- `acli rovodev` — Rovo Dev AI 编码代理（测试版）
- `acli feedback` — 提交反馈/错误报告

## 常见用法

### 输出格式

大多数列表/搜索命令支持以下输出格式：
- `--json`
- `--csv`
- 默认的表格格式

### 批量操作

通过以下方式指定多个操作对象：
- `--key "KEY-1,KEY-2,KEY-3"` — 以逗号分隔的键值对
- `--jql "project = TEAM AND status = 'To Do'"` — JQL 查询语句
- `--filter 10001` — 保存的过滤器 ID
- `--from-file "items.txt"` — 包含键值对的文件（以逗号、空格或换行符分隔）

在批量操作中，可以使用 `--ignore-errors` 忽略错误。
使用 `--yes` / `-y` 可跳过确认提示（适用于自动化场景）。

### 分页

- `--limit N` — 每页返回的最大项目数量（默认值因版本而异，通常为 30-50）
- `--paginate` — 自动获取所有页面（会覆盖 `--limit` 的设置）

### JSON 模板

许多创建/编辑命令支持 `--generate-json` 生成 JSON 模板，以及 `--from-json` 从 JSON 文件中读取数据：
```bash
acli jira workitem create --generate-json > template.json
# edit template.json
acli jira workitem create --from-json template.json
```

## 常见操作快速参考

### 工作项相关操作
```bash
# Create
acli jira workitem create --summary "Fix login bug" --project "TEAM" --type "Bug"
acli jira workitem create --summary "New feature" --project "TEAM" --type "Story" --assignee "@me" --label "frontend,p1"

# Search
acli jira workitem search --jql "project = TEAM AND assignee = currentUser()" --json
acli jira workitem search --jql "project = TEAM AND status = 'In Progress'" --fields "key,summary,assignee" --csv

# View
acli jira workitem view KEY-123
acli jira workitem view KEY-123 --json --fields "*all"

# Edit
acli jira workitem edit --key "KEY-123" --summary "Updated title" --assignee "user@atlassian.com"

# Transition
acli jira workitem transition --key "KEY-123" --status "Done"
acli jira workitem transition --jql "project = TEAM AND sprint in openSprints()" --status "In Progress"

# Assign
acli jira workitem assign --key "KEY-123" --assignee "@me"

# Comment
acli jira workitem comment create --key "KEY-123" --body "Work completed"

# Bulk create
acli jira workitem create-bulk --from-csv issues.csv
```

### 项目相关操作
```bash
acli jira project list --paginate --json
acli jira project view --key "TEAM" --json
acli jira project create --from-project "TEAM" --key "NEW" --name "New Project"
```

### 看板与冲刺相关操作
```bash
acli jira board search --project "TEAM"
acli jira board list-sprints --id 123 --state active
acli jira sprint list-workitems --sprint 1 --board 6
```

## 详细命令参考

有关每个命令的完整参数和示例，请参阅：
- **Jira 工作项相关命令**（创建、编辑、搜索、分配、转换状态、添加评论、复制、链接、归档、附加文件、设置观察者）：[references/jira-workitem-commands.md](references/jira-workitem-commands.md)
- **其他所有命令**（Jira 项目/看板/冲刺/过滤器/仪表板/字段管理、管理员操作、Rovo Dev AI 相关操作、反馈提交）：[references/other-commands.md](references/other-commands.md)