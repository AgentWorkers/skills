---
name: acli
description: "Atlassian CLI（acli）参考指南——这是一个用于与Atlassian Cloud产品交互的命令行工具。当用户需要执行Jira操作（创建/编辑/搜索/转换工作项、管理项目、看板、冲刺、过滤器、仪表板），管理Atlassian组织（管理用户、身份验证），或通过终端自动化Atlassian工作流程时，可以使用此工具。本指南涵盖了所有acli命令，包括：  
- Jira工作项相关命令（创建、编辑、搜索、分配、转换、评论、克隆、链接、归档）  
- Jira项目相关命令（创建、列出、更新、归档）  
- Jira看板/冲刺相关命令  
- Jira过滤器/仪表板相关命令  
- 管理用户相关命令  
- Rovo Dev（Rovo Dev AI代理）相关命令  

使用本指南的前提是系统中已安装并配置好经过身份验证的acli二进制文件。"
---

# Atlassian CLI (acli) 参考文档

## 前提条件

使用本功能需要先安装并登录 `acli`。该工具的二进制文件并未包含在本文档中。

如果尚未安装 `acli`，请引导用户访问以下链接进行安装：  
https://developer.atlassian.com/cloud/acli/guides/install-acli/

请检查 `acli` 是否已安装：  
```bash
acli --help
```

## 登录/认证

在运行命令之前，请先验证登录状态：  
```bash
acli jira auth status
acli admin auth status
```

如果未登录，有以下三种认证方式可供选择：

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

**切换账户：**  
```bash
acli jira auth switch --site mysite.atlassian.net --email user@atlassian.com
acli admin auth switch --org myorgname
```

## 命令结构

```
acli <command> [<subcommand> ...] {MANDATORY FLAGS} [OPTIONAL FLAGS]
```

**主要命令组：**
- `acli jira`：Jira Cloud 相关操作（工作项、项目、看板、冲刺、筛选器、仪表板、字段）
- `acli admin`：组织管理（用户管理、认证）
- `acli rovodev`：Rovo Dev AI 编码辅助工具（测试版）
- `acli feedback`：提交反馈/错误报告

## 常用操作模式

### 输出格式

大多数列表/搜索命令支持以下格式：`--json`、`--csv` 以及默认的表格格式。

### 批量操作

- 使用逗号分隔的键值对来指定多个目标项：`--key "KEY-1,KEY-2,KEY-3"`
- 使用 JQL 查询：`--jql "project = TEAM AND status = 'To Do'"`
- 使用保存的筛选器 ID：`--filter 10001`
- 从文件中读取目标项：`--from-file "items.txt"`（文件内容以逗号、空格或换行符分隔键值对）

- 使用 `--ignore-errors` 可在批量操作中忽略错误并继续执行。
- 使用 `--yes` 或 `-y` 可跳过确认提示（适用于自动化脚本）。

### 分页

- `--limit N`：指定返回的最大项目数量（默认值可能为 30-50）
- `--paginate`：自动获取所有页面（会覆盖 `--limit` 的设置）

### JSON 模板

许多创建/编辑命令支持 `--generate-json` 生成 JSON 模板，以及 `--from-json` 使用 JSON 数据进行操作：
```bash
acli jira workitem create --generate-json > template.json
# edit template.json
acli jira workitem create --from-json template.json
```

## 常见操作快速参考

### 工作项操作  
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

### 项目操作  
```bash
acli jira project list --paginate --json
acli jira project view --key "TEAM" --json
acli jira project create --from-project "TEAM" --key "NEW" --name "New Project"
```

### 看板与冲刺操作  
```bash
acli jira board search --project "TEAM"
acli jira board list-sprints --id 123 --state active
acli jira sprint list-workitems --sprint 1 --board 6
```

## 详细命令参考

有关每个命令的完整参数和示例，请参阅以下文档：
- **Jira 工作项相关命令**（创建、编辑、搜索、分配、转移、评论、克隆、链接、归档、附件、关注者）：[references/jira-workitem-commands.md](references/jira-workitem-commands.md)
- **其他所有命令**（Jira 项目/看板/冲刺/筛选器/仪表板/字段、管理员相关操作、Rovo Dev AI、反馈）：[references/other-commands.md](references/other-commands.md)