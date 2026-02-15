---
name: plane
description: "使用 `plane` CLI 管理 Plane.so 项目和工作项。可以列出项目、创建/更新/搜索问题、管理周期和模块、添加评论以及分配成员。"
metadata: {"moltbot":{"requires":{"bins":["plane"],"env":["PLANE_API_KEY","PLANE_WORKSPACE"]},"primaryEnv":"PLANE_API_KEY","emoji":"✈️","homepage":"https://github.com/JinkoLLC/plane-skill","install":[{"id":"github","kind":"download","url":"https://raw.githubusercontent.com/JinkoLLC/plane-skill/main/scripts/plane","targetDir":"~/.local/bin/","bins":["plane"],"label":"Download plane CLI from GitHub"}]}}
---

# Plane Skill

通过 `plane` 命令行界面（CLI）与 [Plane.so](https://plane.so) 项目管理工具进行交互。

## 安装

下载 CLI 脚本并将其设置为可执行文件：

```bash
curl -o ~/.local/bin/plane https://raw.githubusercontent.com/JinkoLLC/plane-skill/main/scripts/plane
chmod +x ~/.local/bin/plane
```

确保 `~/.local/bin` 被添加到系统的 PATH 环境变量中。

## 设置

```bash
export PLANE_API_KEY="your-api-key"
export PLANE_WORKSPACE="your-workspace-slug"
```

从 **Plane → 个人设置 → 个人访问令牌** 获取您的 API 密钥。

工作区的路径段称为“slug”（例如，对于 `https://app.plane.so/my-team/`，slug 为 `my-team`）。

## 命令

### 当前用户

```bash
plane me                      # Show authenticated user info
```

### 工作区成员

```bash
plane members                 # List all workspace members (name, email, role, ID)
```

### 项目

```bash
plane projects list                                      # List all projects
plane projects get PROJECT_ID                            # Get project details
plane projects create --name "My Project" --identifier "PROJ"  # Create project
```

### 工作项（问题）

```bash
# List work items
plane issues list -p PROJECT_ID
plane issues list -p PROJECT_ID --priority high --assignee USER_ID

# Get details
plane issues get -p PROJECT_ID ISSUE_ID

# Create
plane issues create -p PROJECT_ID --name "Fix login bug" --priority high
plane issues create -p PROJECT_ID --name "Feature" --assignee USER_ID --label LABEL_ID

# Update
plane issues update -p PROJECT_ID ISSUE_ID --state STATE_ID --priority medium

# Assign to members
plane issues assign -p PROJECT_ID ISSUE_ID USER_ID_1 USER_ID_2

# Delete
plane issues delete -p PROJECT_ID ISSUE_ID

# Search across workspace
plane issues search "login bug"
```

### 评论

```bash
plane comments list -p PROJECT_ID -i ISSUE_ID            # List comments on a work item
plane comments list -p PROJECT_ID -i ISSUE_ID --all      # Show all activity (not just comments)
plane comments add -p PROJECT_ID -i ISSUE_ID "Looks good, merging now"  # Add a comment
```

### 循环（冲刺）

```bash
plane cycles list -p PROJECT_ID
plane cycles get -p PROJECT_ID CYCLE_ID
plane cycles create -p PROJECT_ID --name "Sprint 1" --start 2026-01-27 --end 2026-02-10
```

### 模块

```bash
plane modules list -p PROJECT_ID
plane modules get -p PROJECT_ID MODULE_ID
plane modules create -p PROJECT_ID --name "Auth Module" --description "Authentication features"
```

### 状态与标签

```bash
plane states -p PROJECT_ID    # List workflow states (useful for getting state IDs)
plane labels -p PROJECT_ID    # List labels (useful for getting label IDs)
```

## 输出格式

默认输出为格式化的表格。若需获取原始 JSON 数据，可使用 `-f json` 标志：

```bash
plane projects list -f json
plane issues list -p PROJECT_ID -f json
```

## 典型工作流程

1. `plane projects list` — 查找项目 ID
2. `plane states -p PROJECT_ID` — 查看可用的项目状态
3. `plane members` — 查找成员 ID 以分配任务
4. `plane issues create -p PROJECT_ID --name "Task" --priority high --assignee USER_ID` — 创建新问题
5. `plane comments add -p PROJECT_ID -i ISSUE_ID "Started working on this"` — 为问题添加评论