---
name: glab-workitems
description: 列出并管理 GitLab 的工作项（任务、OKR、关键成果、史诗级项目）。适用于处理 GitLab 中超出标准问题类型的工作项时。该功能会在工作项、任务、OKR、关键成果或史诗级项目列表发生变化时触发相应的操作。
---
# glab workitems

**glab workitems** 用于列出和管理 GitLab 的工作项（Work Items）——这是 GitLab 中的新一代工作跟踪机制，支持任务（Tasks）、目标与关键结果（OKRs）、关键成果（Key Results）、大型项目（Epics）等多种类型的工作内容。

> **新增于 glab v1.87.0**

## 什么是工作项（Work Items）？

工作项（Work Items）是 GitLab 的统一工作跟踪模型。它不仅涵盖了传统的 Issues（问题），还支持以下类型：
- **任务（Tasks）**： Issues 内部的子任务
- **目标与关键结果（OKRs）**：可衡量的工作目标
- **关键成果（Key Results）**：与 OKRs 相关联的可衡量成果
- **大型项目（Epics）**：跨越多个里程碑的大型工作项目
- **事件（Incidents）**：与事件管理相关联的工作项

## 快速入门

```bash
# List work items in current project
glab workitems list

# List in a specific project
glab workitems list --repo owner/project

# Output as JSON
glab workitems list --output json
```

## 常见工作流程

### 列出工作项

```bash
# All work items (default: open)
glab workitems list

# Filter by type
glab workitems list --type Task
glab workitems list --type OKR
glab workitems list --type KeyResult
glab workitems list --type Epic

# Filter by state
glab workitems list --state opened
glab workitems list --state closed

# JSON for scripting
glab workitems list --output json | python3 -c "
import sys, json
items = json.load(sys.stdin)
for item in items:
    print(f\"{item['iid']}: {item['title']} [{item['type']}]\")
"
```

### 在特定仓库或组中使用

```bash
# Specific repo
glab workitems list --repo mygroup/myproject

# Group-level work items
glab workitems list --group mygroup
```

## 工作项与 Issues 的区别

| 功能         | Issues    | Work Items   |
|--------------|---------|-----------|
| 标准的错误/功能跟踪    | ✅       | ✅         |
| 任务（子任务）       | ❌       | ✅         |
| 目标与关键结果     | ❌       | ✅         |
| 大型项目（下一代）    | ❌       | ✅         |
| 命令行界面支持     | 完全支持   | `list`（v1.87.0 及以上版本） |

- 对于标准的 Issue 工作流程，使用 `glab issue` 命令。
- 当需要处理任务、目标与关键结果或大型项目时，使用 `glab workitems` 命令。

## 常见问题与解决方法

- **“workitems: 命令未找到”**：需要使用 glab v1.87.0 或更高版本。请通过 `glab version` 命令检查版本信息。
- **期望看到结果但为空**：工作项与 Issues 是不同的类型；作为 Issues 创建的工作项不会自动显示在这里，除非它们被转换成工作项形式。
- **类型过滤器无结果**：并非所有 GitLab 实例都支持所有类型的工作项。GitLab SaaS 版本的支持范围比自托管实例更广泛。

## 相关技能

- `glab-issue`：用于标准 Issue 的管理
- `glab-milestone`：用于里程碑的管理（常与目标与关键结果结合使用）
- `glab-iteration`：用于冲刺/迭代的管理
- `glab-incident`：用于事件管理（也是一种工作项类型）

## 命令参考

```
glab workitems list [--flags]

Flags:
  --group        Select a group/subgroup
  --output       Format output as: text, json
  --page         Page number
  --per-page     Number of items per page
  --repo         Select a repository
  --state        Filter by state: opened, closed, all
  --type         Filter by work item type
  -h, --help     Show help
```