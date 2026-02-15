---
name: planka
description: 通过一个自定义的 Python CLI（命令行接口）来管理 Planka（看板）项目、看板、列表、卡片以及通知。
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["planka-cli"]}}}
---

# Planka CLI

本技能提供了一个基于 `plankapy` 库的命令行界面（CLI）封装，用于与 Planka 实例进行交互。

## 设置

1. **通过 Homebrew tap 安装：**
    ```bash
    brew tap voydz/homebrew-tap
    brew install planka-cli
    ```

2. **配置：**
    使用 `login` 命令来存储凭据：
    ```bash
    planka-cli login --url https://planka.example --username alice --password secret
    # or: python3 scripts/planka_cli.py login --url https://planka.example --username alice --password secret
    ```

## 使用方法

运行已安装的 `planka-cli` 可执行文件来使用该 CLI：

```bash
# Show help
planka-cli

# Check connection
planka-cli status

# Login to planka instance
planka-cli login --url https://planka.example --username alice --password secret

# Remove stored credentials
planka-cli logout

# List Projects
planka-cli projects list

# List Boards (optionally by project ID)
planka-cli boards list [PROJECT_ID]

# List Lists in a Board
planka-cli lists list <BOARD_ID>

# List Cards in a List
planka-cli cards list <LIST_ID>

# Create a Card
planka-cli cards create <LIST_ID> "Card title"

# Update a Card
planka-cli cards update <CARD_ID> --name "New title"
planka-cli cards update <CARD_ID> --list-id <LIST_ID>
planka-cli cards update <CARD_ID> --list-id <LIST_ID> --position top

# Delete a Card
planka-cli cards delete <CARD_ID>

# Notifications
planka-cli notifications all
planka-cli notifications unread
```

## 示例

**列出所有卡片：**
```bash
planka-cli boards list
```

**显示列表 ID 1619901252164912136 中的卡片：**
```bash
planka-cli cards list 1619901252164912136
```

**在列表 ID 1619901252164912136 中创建一张卡片：**
```bash
planka-cli cards create 1619901252164912136 "Ship CLI"
```

**将一张卡片移动到另一个列表：**
```bash
planka-cli cards update 1619901252164912137 --list-id 1619901252164912136
```

**将一张卡片移动到另一个列表并将其置顶：**
```bash
planka-cli cards update 1619901252164912137 --list-id 1619901252164912136 --position top
```

**通过更新卡片名称来标记卡片为已完成：**
```bash
planka-cli cards update 1619901252164912137 --name "Done: Ship CLI"
```