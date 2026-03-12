---
name: glab-label
description: 管理 GitLab 标签，包括在项目级别和组级别执行创建、列出、更新和删除操作。适用于对带有标签的问题/任务进行组织、创建标签分类体系，或管理标签的颜色和描述。相关操作会在标签、标签组、问题标签的创建或标签管理时被触发。
---
# glab 标签

用于在项目和组级别管理标签。

## 快速入门

```bash
# Create project label
glab label create --name bug --color "#FF0000"

# Create group label
glab label create --group my-group --name priority::high --color "#FF6B00"

# List labels
glab label list

# Update label
glab label edit bug --color "#CC0000" --description "Software defects"

# Delete label
glab label delete bug
```

## 选择：使用项目级标签还是组级标签？

```
Where should this label live?
├─ Used across multiple projects in a group
│  └─ Group-level: glab label create --group <group> --name <label>
└─ Specific to one project
   └─ Project-level: glab label create --name <label>
```

**在以下情况下使用组级标签：**
- 当您希望在整个组中的所有项目中保持标签的一致性时
- 在管理全组织范围内的工作流程时
- 例如：`priority::high`、`type::bug`、`status::blocked`
- 这可以减少重复并确保标签的一致性

**在以下情况下使用项目级标签：**
- 当标签特定于某个项目的工作流程时
- 当团队希望对自己的标签进行控制时
- 例如：`needs-ux-review`、`deploy-to-staging`、`legacy-code`

## 常见工作流程

### 创建标签分类体系

**设置优先级标签（组级）：**
```bash
glab label create --group engineering --name "priority::critical" --color "#FF0000"
glab label create --group engineering --name "priority::high" --color "#FF6B00"
glab label create --group engineering --name "priority::medium" --color "#FFA500"
glab label create --group engineering --name "priority::low" --color "#FFFF00"
```

**设置类型标签（组级）：**
```bash
glab label create --group engineering --name "type::bug" --color "#FF0000"
glab label create --group engineering --name "type::feature" --color "#00FF00"
glab label create --group engineering --name "type::maintenance" --color "#0000FF"
```

### 管理项目特定的标签

**创建工作流程标签：**
```bash
glab label create --name "needs-review" --color "#428BCA"
glab label create --name "ready-to-merge" --color "#5CB85C"
glab label create --name "blocked" --color "#D9534F"
```

### 批量操作

**列出所有标签以供审核：**
```bash
glab label list --per-page 100 > labels.txt
```

**删除已弃用的标签：**
```bash
glab label delete old-label-1
glab label delete old-label-2
```

## 相关技能

**使用标签：**
- 请参阅 `glab-issue` 以将标签应用于问题
- 请参阅 `glab-mr` 以将标签应用于合并请求
- 脚本：`scripts/batch-label-issues.sh` 用于批量标记问题

## v1.89.0 更新

> **v1.89.0+：** `glab label get` 支持 `--output json` / `-F json` 选项，以获得结构化输出，非常适合自动化脚本使用。

```bash
# Get a label with JSON output (v1.89.0+)
glab label get <label-id> --output json
glab label get <label-id> -F json
```

## 命令参考

有关完整的命令文档和所有参数，请参阅 [references/commands.md](references/commands.md)。

**可用命令：**
- `create` - 创建标签（项目或组）
- `list` - 列出标签
- `edit` - 更新标签属性
- `delete` - 删除标签
- `get` - 查看单个标签的详细信息