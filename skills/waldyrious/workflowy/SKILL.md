---
name: workflowy
description: 这是一个用于阅读、搜索和编辑 Workflowy 大纲的命令行工具（CLI）。当用户需要与他们的 Workflowy 大纲进行交互时，可以使用该工具：搜索内容、添加新项目、查看大纲结构、标记已完成的项目、执行批量操作或生成使用报告等。
homepage: https://github.com/mholzen/workflowy
metadata:
  {
    "openclaw":
      {
        "emoji": "📝",
        "requires": { "bins": ["workflowy"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "mholzen/workflowy/workflowy-cli",
              "bins": ["workflowy"],
              "label": "Install workflowy-cli (brew)",
            },
          ],
      },
  }
---

# Workflowy

可以使用非官方的 `workflowy` 命令行工具（[mholzen/workflowy](https://github.com/mholzen/workflowy)）来管理 Workflowy 的大纲。使用该工具需要先设置 API 密钥。

## 设置（仅一次）

在 https://workflowy.com/api-key/ 获取你的 API 密钥，并将其保存到 `~/.workflowy/api.key` 文件中：

```bash
mkdir -p ~/.workflowy
echo "your-api-key-here" > ~/.workflowy/api.key
```

## 常用命令

### 阅读

```bash
# Get root nodes (depth 2 by default)
workflowy get

# Get specific node by UUID or short ID
workflowy get <item-id>
workflowy get https://workflowy.com/#/59fc7acbc68c

# Show a node's children as a flat list
workflowy list <item-id>

# Search (full text, case-insensitive)
workflowy search -i "meeting notes"

# Search with extended regex
workflowy search -E "<time.*>"

# Search within a subtree
workflowy search "bug" --item-id <parent-id>
```

### 编写

```bash
# Add a new node to the Inbox
workflowy create "Buy groceries" --parent-id=inbox

# Add a node to a specific parent
workflowy create "Task" --parent-id=<uuid>

# Update a node
workflowy update <item-id> --name "New name"

# Complete/uncomplete
workflowy complete <item-id>
workflowy uncomplete <item-id>

# Move a node
workflowy move <item-id> <new-parent-id>

# Delete a node (includes its children!)
workflowy delete <item-id>
```

### 批量操作

```bash
# Search and replace (dry run first!)
workflowy replace --dry-run "foo" "bar"
workflowy replace --interactive "foo" "bar"

# Regex find/replace using capture groups
workflowy replace "TASK-([0-9]+)" 'ISSUE-$1'

# Transform: split by newlines into children
workflowy transform <item-id> split -s "\n"

# Transform: trim whitespace
workflowy transform <item-id> trim
```

### 统计信息

```bash
# Where is most content?
workflowy report count --threshold 0.01

# Nodes with most children
workflowy report children --top-n 20

# Stale content (oldest modified)
workflowy report modified --top-n 50

# Most mirrored nodes (requires backup)
workflowy report mirrors --top-n 20
```

## 数据访问方法

| 方法                | 速度          | 数据更新频率 | 适用场景           |
|-------------------|---------------|-----------|-------------------|
| `--method=get`    | 中等          | 实时        | 查看特定项目        |
| `--method=export` | 快速（缓存数据）    | 约 1 分钟     | 访问整个大纲结构     |
| `--method=backup` | 最快          | 数据已过时     | 批量操作、离线使用     |

若需离线使用 Workflowy，需启用其 Dropbox 备份功能：
```bash
workflowy get --method=backup
```

## 简短 ID

Workflowy 支持使用从“复制内部链接”菜单获得的短 ID：
- 网址示例：`https://workflowy.com/#/59fc7acbc68c`
- 可直接使用，例如：`workflowy get https://workflowy.com/#/59fc7acbc68c`

## 特殊命名的目标节点

- `inbox`    — 用户的收件箱
- `home`    — 大纲的根节点

```bash
workflowy create "Quick note" --parent-id=inbox
workflowy id inbox  # resolve to UUID
```

## 注意事项

- 删除一个节点会同时删除其所有子节点。
- 结果会按照优先级排序显示。
- 对于大型大纲结构，建议使用 `--method=export` 命令进行操作（该命令会使用缓存，速度更快）。
- 需要使用备份功能才能进行镜像分析。
- 在执行批量替换操作前，请务必确认操作内容。